#!/bin/bash
# Self-signed cert for levels 15/16's TLS-wrapped port daemons. Bundled
# directly into the image (not a runtime secret) -- these levels are about
# teaching "connect with openssl s_client" and "scan for the TLS port,"
# not about certificate trust, so a fixed, image-baked cert is appropriate.
set -e

mkdir -p /opt/bandit-daemons/tls
openssl req -x509 -newkey rsa:2048 -keyout /tmp/key.pem -out /tmp/cert.pem \
    -days 3650 -nodes -subj "/CN=bandit-target"
cat /tmp/key.pem /tmp/cert.pem > /opt/bandit-daemons/tls/server.pem
chmod 600 /opt/bandit-daemons/tls/server.pem
rm -f /tmp/key.pem /tmp/cert.pem
