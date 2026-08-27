#!/bin/sh
set -eu

# Runtime generation is the only process that receives the team secret blob.
python3 /opt/sentinel/runtime.py
unset LEVEL_SECRETS
exec /usr/sbin/sshd -D -e
