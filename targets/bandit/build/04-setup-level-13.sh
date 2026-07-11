#!/bin/bash
# Level 13: bandit13's home gets a private key that logs into bandit14
# (whose account password isn't discoverable any other way -- you have to
# use the key to get in and read /etc/bandit_pass/bandit14, exactly
# mirroring the real level). bandit14's own login password (set in
# 02-set-passwords.sh) equals bandit-13's flag, so once discovered via the
# key it also works as a normal password for the next step.
set -e

ssh-keygen -t ed25519 -N "" -C "bandit14-access" -f /tmp/bandit13-14-key

install -m 700 -d /home/bandit13/.ssh
install -m 600 -o bandit13 -g bandit13 /tmp/bandit13-14-key /home/bandit13/sshkey.private
chown bandit13:bandit13 /home/bandit13/sshkey.private

install -m 700 -d -o bandit14 -g bandit14 /home/bandit14/.ssh
cp /tmp/bandit13-14-key.pub /home/bandit14/.ssh/authorized_keys
chmod 600 /home/bandit14/.ssh/authorized_keys
chown bandit14:bandit14 /home/bandit14/.ssh/authorized_keys

rm -f /tmp/bandit13-14-key /tmp/bandit13-14-key.pub

# /etc/bandit_pass/bandit14 -- readable only by bandit14 (and bandit13, who
# already has the key granting direct access to bandit14 anyway) --
# contains bandit-13's flag, which is ALSO bandit14's actual login
# password, matching the real level's design where the "next password"
# file and the account's real password are the same value.
#
# Security: a fixed-length placeholder here -- entrypoint.sh substitutes
# the real per-team value (and sets bandit14's actual login password to
# match) at container start (see docs/security-audit-status.md). The SSH
# keypair above is still generated fresh per BUILD (not per team) for
# now -- a known remaining gap, not yet converted to per-team.
mkdir -p /etc/bandit_pass
echo "BANDITPLACEHOLDER13ZZZZZZZZZZZZZ" > /etc/bandit_pass/bandit14
chown bandit14:bandit14 /etc/bandit_pass/bandit14
chmod 400 /etc/bandit_pass/bandit14
