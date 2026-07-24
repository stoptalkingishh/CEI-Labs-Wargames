#!/bin/bash
# Level 13: bandit13's home gets a private key that logs into bandit14
# (whose account password isn't discoverable any other way -- you have to
# use the key to get in and read /etc/bandit_pass/bandit14, exactly
# mirroring the real level). bandit14's own login password (set in
# 02-set-passwords.sh) equals bandit-13's flag, so once discovered via the
# key it also works as a normal password for the next step.
#
# Security: the SSH keypair itself is NOT generated here anymore --
# entrypoint.sh now generates it fresh per container (i.e. per team) at
# start, the same way every other per-team secret is handled. Generating
# it at build time meant every team's image shipped the literal same
# keypair, so any team reaching level 13 could also SSH straight into
# every OTHER team's bandit14 with it -- a team-isolation break, not just
# a level-isolation one (see docs/security-audit-status.md). This script
# only lays down the fixed-length placeholder below; entrypoint.sh
# substitutes the real per-team value (and sets bandit14's actual login
# password to match) at container start.
set -e

mkdir -p /etc/bandit_pass
echo "BANDITPLACEHOLDER13ZZZZZZZZZZZZZ" > /etc/bandit_pass/bandit14
chown bandit14:bandit14 /etc/bandit_pass/bandit14
chmod 400 /etc/bandit_pass/bandit14
