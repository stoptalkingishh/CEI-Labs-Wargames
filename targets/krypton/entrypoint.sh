#!/bin/bash
# No background daemons for Krypton (all 7 levels are pure crypto
# puzzles, nothing needs a listening service beyond sshd itself).
set -e

exec /usr/sbin/sshd -D
