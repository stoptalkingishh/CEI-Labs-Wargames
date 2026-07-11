#!/usr/bin/env python3
"""Bandit level 16: same idea as level 15, but the listening port is
somewhere in 31000-32000 and not told to the player -- the lesson is
scanning the range (e.g. `nmap -sT -sV --script ssl-enum-ciphers -p
31000-32000 localhost` or similar) to find the one port that speaks TLS
and responds correctly. Only this one port (31046, arbitrary) actually
binds; every other port in the range is simply closed, which is what
makes the range genuinely scannable rather than a fixed answer.

Security: reads its expected/next passwords from $LEVEL_SECRETS at
process start -- per-team values, see level14_port30000.py's docstring
for the full reasoning."""
import json
import os
import socketserver
import ssl

_secrets = json.loads(os.environ.get("LEVEL_SECRETS", "{}"))
EXPECTED_PASSWORD = _secrets.get("bandit15")
NEXT_PASSWORD = _secrets.get("bandit16")
CERTFILE = "/opt/bandit-daemons/tls/server.pem"
PORT = 31046


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

    def get_request(self):
        newsocket, fromaddr = self.socket.accept()
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(certfile=CERTFILE)
        connstream = ctx.wrap_socket(newsocket, server_side=True)
        return connstream, fromaddr


if __name__ == "__main__":
    with Server(("0.0.0.0", PORT), Handler) as server:
        server.serve_forever()
