#!/usr/bin/env python3
"""Send a test vote to a Votifier / NuVotifier listener.

No third-party packages needed (Python 3.8+ standard library only).

Protocol v2 (NuVotifier, token based, recommended):
    python3 votifier_test.py v2 --host play.example.net --port 8192 \
        --token YOUR_TOKEN --username Notch

Protocol v1 (classic Votifier, RSA public key):
    python3 votifier_test.py v1 --host play.example.net --port 8192 \
        --public-key plugins/Votifier/rsa/public.key --username Notch

The token is in plugins/nuvotifier/config.yml (``tokens: default: ...``),
the public key in plugins/nuvotifier/rsa/public.key (or plugins/Votifier/rsa/).
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import socket
import struct
import sys
import time

V2_MAGIC = 0x733A


# --------------------------------------------------------------------------
# shared helpers
# --------------------------------------------------------------------------

def read_greeting(sock: socket.socket) -> str:
    """Read the 'VOTIFIER <version> [challenge]' line the server sends first."""
    data = b""
    while not data.endswith(b"\n"):
        chunk = sock.recv(1)
        if not chunk:
            break
        data += chunk
        if len(data) > 512:
            break
    line = data.decode("utf-8", "replace").strip()
    if not line.startswith("VOTIFIER"):
        raise RuntimeError(f"unexpected greeting (is this really a Votifier port?): {line!r}")
    return line


# --------------------------------------------------------------------------
# protocol v2
# --------------------------------------------------------------------------

def build_v2_packet(service: str, username: str, address: str, token: str,
                    challenge: str, timestamp_ms: int) -> bytes:
    payload = json.dumps({
        "serviceName": service,
        "username": username,
        "address": address,
        "timestamp": timestamp_ms,
        "challenge": challenge,
    }, separators=(",", ":"))
    signature = base64.b64encode(
        hmac.new(token.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).digest()
    ).decode("ascii")
    message = json.dumps({"payload": payload, "signature": signature},
                         separators=(",", ":")).encode("utf-8")
    if len(message) > 0xFFFF:
        raise ValueError("vote message too long")
    return struct.pack(">HH", V2_MAGIC, len(message)) + message


def send_v2(host: str, port: int, token: str, service: str, username: str,
            address: str, timeout: float) -> dict:
    with socket.create_connection((host, port), timeout=timeout) as sock:
        greeting = read_greeting(sock)
        parts = greeting.split()
        if len(parts) < 3:
            raise RuntimeError(
                f"server greeting has no challenge ({greeting!r}). "
                "This looks like a v1-only Votifier: use the v1 command with the public key."
            )
        challenge = parts[2]
        sock.sendall(build_v2_packet(service, username, address, token, challenge,
                                     int(time.time() * 1000)))
        reply = b""
        while not reply.endswith(b"\n"):
            chunk = sock.recv(1024)
            if not chunk:
                break
            reply += chunk
    text = reply.decode("utf-8", "replace").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        raise RuntimeError(f"unexpected reply: {text!r}")


# --------------------------------------------------------------------------
# protocol v1 (RSA PKCS#1 v1.5, implemented with the standard library)
# --------------------------------------------------------------------------

def _der_read(data: bytes, pos: int):
    tag = data[pos]
    pos += 1
    length = data[pos]
    pos += 1
    if length & 0x80:
        n = length & 0x7F
        length = int.from_bytes(data[pos:pos + n], "big")
        pos += n
    return tag, data[pos:pos + length], pos + length


def parse_public_key(text: str) -> tuple[int, int]:
    """Return (modulus, exponent) from a Votifier public.key (base64 X.509 / PEM)."""
    body = "".join(
        line.strip() for line in text.splitlines() if line.strip() and not line.startswith("-----")
    )
    der = base64.b64decode(body)
    tag, spki, _ = _der_read(der, 0)                 # SubjectPublicKeyInfo SEQUENCE
    if tag != 0x30:
        raise ValueError("not an X.509 public key")
    _, _algo, pos = _der_read(spki, 0)               # AlgorithmIdentifier
    tag, bitstring, _ = _der_read(spki, pos)          # BIT STRING
    if tag != 0x03:
        raise ValueError("public key BIT STRING missing")
    rsa = bitstring[1:]                               # skip unused-bits byte
    _, seq, _ = _der_read(rsa, 0)                     # RSAPublicKey SEQUENCE
    _, n_bytes, pos = _der_read(seq, 0)
    _, e_bytes, _ = _der_read(seq, pos)
    return int.from_bytes(n_bytes, "big"), int.from_bytes(e_bytes, "big")


def rsa_pkcs1_encrypt(message: bytes, n: int, e: int) -> bytes:
    k = (n.bit_length() + 7) // 8
    if len(message) > k - 11:
        raise ValueError("vote too long for this key")
    padding = b""
    while len(padding) < k - 3 - len(message):
        padding += bytes(b for b in os.urandom(k) if b != 0)
    padding = padding[: k - 3 - len(message)]
    block = b"\x00\x02" + padding + b"\x00" + message
    return pow(int.from_bytes(block, "big"), e, n).to_bytes(k, "big")


def build_v1_block(service: str, username: str, address: str, timestamp_ms: int) -> bytes:
    return f"VOTE\n{service}\n{username}\n{address}\n{timestamp_ms}\n".encode("utf-8")


def send_v1(host: str, port: int, public_key: str, service: str, username: str,
            address: str, timeout: float) -> None:
    n, e = parse_public_key(public_key)
    packet = rsa_pkcs1_encrypt(build_v1_block(service, username, address,
                                              int(time.time() * 1000)), n, e)
    with socket.create_connection((host, port), timeout=timeout) as sock:
        read_greeting(sock)
        sock.sendall(packet)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Send a test vote to a (Nu)Votifier listener.")
    sub = parser.add_subparsers(dest="protocol", required=True)
    for name in ("v1", "v2"):
        p = sub.add_parser(name)
        p.add_argument("--host", required=True)
        p.add_argument("--port", type=int, default=8192)
        p.add_argument("--username", required=True, help="Minecraft name that receives the vote")
        p.add_argument("--service", default="votifier-test",
                       help="service name (v2: must match a key under 'tokens' or use 'default')")
        p.add_argument("--address", default="127.0.0.1", help="voter IP sent in the vote")
        p.add_argument("--timeout", type=float, default=5.0)
        if name == "v1":
            p.add_argument("--public-key", required=True, help="path to rsa/public.key")
        else:
            p.add_argument("--token", default=os.environ.get("VOTIFIER_TOKEN"),
                           help="NuVotifier token (or env VOTIFIER_TOKEN)")
    args = parser.parse_args(argv)

    try:
        if args.protocol == "v2":
            if not args.token:
                parser.error("--token or VOTIFIER_TOKEN is required for v2")
            reply = send_v2(args.host, args.port, args.token, args.service, args.username,
                            args.address, args.timeout)
            if reply.get("status") == "ok":
                print(f"OK: vote for {args.username} accepted by {args.host}:{args.port}")
                return 0
            print(f"REJECTED: {reply.get('cause', '')} {reply.get('error', '')}".strip())
            return 2
        with open(args.public_key, encoding="utf-8") as fh:
            key = fh.read()
        send_v1(args.host, args.port, key, args.service, args.username, args.address,
                args.timeout)
        print(f"SENT: v1 vote for {args.username} to {args.host}:{args.port} "
              "(v1 has no reply, check the server console)")
        return 0
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
