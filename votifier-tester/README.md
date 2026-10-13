# Votifier / NuVotifier test vote

`votifier_test.py` sends one test vote to your server so you can check that the port is open,
the token or key is right and your vote listener (VotingPlugin, SuperbVote, ...) gives the reward.
It needs Python 3.8+ and nothing else.

## Protocol v2 (NuVotifier, token)

The token is in `plugins/Votifier/config.yml` under `tokens:` → `default:`.

```bash
python3 votifier_test.py v2 --host play.example.net --port 8192 --token YOUR_TOKEN --username Notch
# or keep the token out of your shell history:
VOTIFIER_TOKEN=YOUR_TOKEN python3 votifier_test.py v2 --host play.example.net --username Notch
```

Possible results:

| Output | Meaning |
|---|---|
| `OK: vote ... accepted` | Votifier accepted the vote. Check the console for your listener. |
| `REJECTED: CorruptedFrameException Signature is not valid (invalid token?)` | Wrong token, or `--service` does not match a key under `tokens` and there is no `default`. |
| `ERROR: ... Connection refused` / `timed out` | Port closed, wrong port, or a firewall in front of the server. |
| `ERROR: unexpected greeting` | Something else answers on that port (often the game port instead of the Votifier port). |
| `server greeting has no challenge` | Old v1-only Votifier: use the v1 command. |

## Protocol v1 (RSA public key)

```bash
python3 votifier_test.py v1 --host play.example.net --port 8192 \
  --public-key plugins/Votifier/rsa/public.key --username Notch
```

v1 sends no answer. Look for `Got a protocol v1 vote record` in the server console.

## Tests

```bash
python3 -m unittest test_votifier.py
```

The tests start a fake listener on localhost. The v1 test uses the `cryptography` package and is skipped without it.
We also ran the script against NuVotifier 2.7.3 on Paper 1.21.11 (v2 accepted, wrong token rejected, v1 received).

Step-by-step server setup: [NuVotifier on Paper and Velocity](https://bestmcserverlist.net/guides/nuvotifier-setup-paper-velocity).
