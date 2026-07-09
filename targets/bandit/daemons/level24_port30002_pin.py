#!/usr/bin/env python3
"""Bandit level 24: submit bandit24's current password AND a secret
4-digit PIN, in one line, space-separated, to port 30002. One connection
per guess, matching the real level's actual design -- the point is
brute-forcing the PIN space (10,000 combinations), not the protocol."""
import socketserver

EXPECTED_PASSWORD = "UoMYTrfrBFHyQXmg6R1YI7mIfUIna55J"
SECRET_PIN = "7568"
NEXT_PASSWORD = "uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG"


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
