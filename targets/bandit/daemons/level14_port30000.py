#!/usr/bin/env python3
"""Bandit level 14: submit bandit14's current password to port 30000,
get bandit-14's flag (bandit15's password) back.

Runs as an unprivileged daemon user (not bandit14/root) -- the expected
password is baked in at build time, same trust model as
/etc/bandit_pass/bandit14 (a fixed, known-at-build-time value), not a
runtime secret read.
"""
import socketserver

EXPECTED_PASSWORD = "fGrHPx402xGC7U7rXKDaxiWFTOiF0ENq"
NEXT_PASSWORD = "jN2kgmIXJ6fShzhT2avhotn4Zcka6tnt"


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
