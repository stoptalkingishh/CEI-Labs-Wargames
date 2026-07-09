#!/usr/bin/env python3
"""Bandit level 15: same idea as level 14, but over TLS on port 30001.
Solved with e.g. `openssl s_client -connect localhost:30001 -quiet`, then
pasting the password."""
import socketserver
import ssl

EXPECTED_PASSWORD = "jN2kgmIXJ6fShzhT2avhotn4Zcka6tnt"
NEXT_PASSWORD = "JQttfApK4SeyHwDlI9SXGR50qclOAil1"
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
