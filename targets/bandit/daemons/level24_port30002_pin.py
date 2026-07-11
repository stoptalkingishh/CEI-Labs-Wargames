#!/usr/bin/env python3
"""Bandit level 24: submit bandit24's current password AND a secret
4-digit PIN, in one line, space-separated, to port 30002. One connection
per guess, matching the real level's actual design -- the point is
brute-forcing the PIN space (10,000 combinations), not the protocol.

Security: EXPECTED_PASSWORD/NEXT_PASSWORD are per-team secrets read from
$LEVEL_SECRETS (see level14_port30000.py's docstring). SECRET_PIN was
previously a FIXED "7568" shared by every build ever (not even
per-instance, let alone per-team) -- now generated fresh, locally, every
time this daemon process starts (once per container boot). The PIN
itself is never submitted to CTFd (it's a local brute-force gate, not a
validated flag), so it doesn't need to come from the orchestrator's
synced secrets at all -- just genuinely random per container."""
import json
import os
import secrets
import socketserver

_secrets = json.loads(os.environ.get("LEVEL_SECRETS", "{}"))
EXPECTED_PASSWORD = _secrets.get("bandit23")
NEXT_PASSWORD = _secrets.get("bandit24")
SECRET_PIN = f"{secrets.randbelow(10000):04d}"


class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        try:
            line = self.rfile.readline(256).decode(errors="replace").strip()
        except Exception:
            return
        parts = line.split()
        if len(parts) == 2 and parts[0] == EXPECTED_PASSWORD and parts[1] == SECRET_PIN:
            self.wfile.write((NEXT_PASSWORD + "\n").encode())
        else:
            self.wfile.write(b"Wrong!\n")


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    with Server(("0.0.0.0", 30002), Handler) as server:
        server.serve_forever()
