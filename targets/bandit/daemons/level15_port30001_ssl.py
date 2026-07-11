#!/usr/bin/env python3
"""Bandit level 15: same idea as level 14, but over TLS on port 30001.
Solved with e.g. `openssl s_client -connect localhost:30001 -quiet`, then
pasting the password.

Security: reads its expected/next passwords from $LEVEL_SECRETS at
process start -- per-team values, see level14_port30000.py's docstring
for the full reasoning."""
import json
import os
import socketserver
import ssl

_secrets = json.loads(os.environ.get("LEVEL_SECRETS", "{}"))
EXPECTED_PASSWORD = _secrets.get("bandit14")
NEXT_PASSWORD = _secrets.get("bandit15")
CERTFILE = "/opt/bandit-daemons/tls/server.pem"


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
    with Server(("0.0.0.0", 30001), Handler) as server:
        server.serve_forever()
