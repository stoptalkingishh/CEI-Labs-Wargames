#!/bin/bash
# Creates bandit0-bandit33, each with a home dir and bash shell.
# Passwords are set in 02-set-passwords.sh (kept separate so the password
# chain -- which must match CTFd's already-defined flags exactly -- is easy
# to audit on its own).
set -e

for i in $(seq 0 33); do
    useradd -m -s /bin/bash --no-log-init "bandit${i}"
    # 0750, not 0755: each level's home directory must stay traversable by
    # its own owner (and, via the group bit, that owner's own group -- no
    # one else is ever a member of it) but NOT by "other" -- otherwise any
    # other player (trivially bandit0) can cd/cat straight into a later
    # level's home directory and read its flag without ever solving the
    # level. See docs/security-audit-status.md.
    chmod 750 "/home/bandit${i}"
done
