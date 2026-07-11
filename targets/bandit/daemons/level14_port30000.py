#!/usr/bin/env python3
"""Bandit level 14: submit bandit14's current password to port 30000,
get bandit-14's flag (bandit15's password) back.

Runs as an unprivileged daemon user (not bandit14/root). Security: reads
its expected/next passwords from $LEVEL_SECRETS at process start (this
daemon is (re)started fresh by entrypoint.sh on every container boot) --
per-team values, not identical hardcoded strings shared by every team
(see docs/security-audit-status.md). If the relevant keys are missing
(e.g. content not yet synced), the daemon simply never accepts any
password -- a safe failure mode, not a shared-credential one.
"""
import json
import os
import socketserver

_secrets = json.loads(os.environ.get("LEVEL_SECRETS", "{}"))
EXPECTED_PASSWORD = _secrets.get("bandit13")
NEXT_PASSWORD = _secrets.get("bandit14")


class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        try:
            line = self.rfile.readline(256).decode(errors="replace").strip()
        except Exception:
            return
        if line == EXPECTED_PASSWORD:
            self.wfile.write((NEXT_PASSWORD + "\n").encode())
        else:
            self.wfile.write(b"Wrong password\n")


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    with Server(("0.0.0.0", 30000), Handler) as server:
        server.serve_forever()
