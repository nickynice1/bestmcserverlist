"""Tests against a tiny in-process fake NuVotifier listener.

Run: python3 -m unittest test_votifier.py
The v1 test needs the 'cryptography' package to decrypt; it is skipped without it.
"""

import base64
import hashlib
import hmac
import json
import socket
import struct
import threading
import unittest

import votifier_test as vt

TOKEN = "s3cr3t-test-token"


class FakeV2Server(threading.Thread):
    def __init__(self, token):
        super().__init__(daemon=True)
        self.token = token
        self.sock = socket.socket()
        self.sock.bind(("127.0.0.1", 0))
        self.sock.listen(1)
        self.port = self.sock.getsockname()[1]
        self.vote = None

    def run(self):
        conn, _ = self.sock.accept()
        with conn:
            challenge = "abc123challenge"
            conn.sendall(f"VOTIFIER 2 {challenge}\n".encode())
            magic, length = struct.unpack(">HH", conn.recv(4))
            data = b""
            while len(data) < length:
                data += conn.recv(length - len(data))
            msg = json.loads(data)
            expected = base64.b64encode(hmac.new(self.token.encode(), msg["payload"].encode(),
                                                 hashlib.sha256).digest()).decode()
            payload = json.loads(msg["payload"])
            ok = magic == 0x733A and msg["signature"] == expected and payload["challenge"] == challenge
            self.vote = payload
            reply = {"status": "ok"} if ok else {"status": "error", "cause": "BadSignature", "error": "bad"}
            conn.sendall((json.dumps(reply) + "\r\n").encode())


class V2Test(unittest.TestCase):
    def test_accepts_valid_vote(self):
        srv = FakeV2Server(TOKEN)
        srv.start()
        reply = vt.send_v2("127.0.0.1", srv.port, TOKEN, "test", "Notch", "1.2.3.4", 3)
        srv.join(3)
        self.assertEqual(reply["status"], "ok")
        self.assertEqual(srv.vote["username"], "Notch")

    def test_wrong_token_is_rejected(self):
        srv = FakeV2Server(TOKEN)
        srv.start()
        reply = vt.send_v2("127.0.0.1", srv.port, "wrong", "test", "Notch", "1.2.3.4", 3)
        srv.join(3)
        self.assertEqual(reply["status"], "error")


try:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import padding, rsa
except ImportError:  # pragma: no cover
    rsa = None


@unittest.skipIf(rsa is None, "cryptography not installed")
class V1Test(unittest.TestCase):
    def test_block_decrypts(self):
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        der = key.public_key().public_bytes(serialization.Encoding.DER,
                                            serialization.PublicFormat.SubjectPublicKeyInfo)
        n, e = vt.parse_public_key(base64.b64encode(der).decode())
        self.assertEqual(n, key.public_key().public_numbers().n)
        block = vt.build_v1_block("test", "Notch", "1.2.3.4", 1700000000000)
        cipher = vt.rsa_pkcs1_encrypt(block, n, e)
        self.assertEqual(len(cipher), 256)
        self.assertEqual(key.decrypt(cipher, padding.PKCS1v15()), block)


if __name__ == "__main__":
    unittest.main()
