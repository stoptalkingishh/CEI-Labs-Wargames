#!/bin/bash
# Creates krypton0-krypton6. krypton0 is now a real account like every
# other level (it used to be skipped -- level 0's puzzle lived directly
# in the CTFd challenge description text as a shared Base64 string, with
# no per-team mechanism; see docs/security-audit-status.md and
# cei-labs-event#17 for that history). krypton0's login password is a
# fixed, publicly-known value set in 02-set-passwords.sh (matching
# Bandit's own bandit0 front door), and its per-team Base64 puzzle
# content is written into its home directory at container start by
# entrypoint.sh, same mechanism as every other level.
set -e

for i in $(seq 0 6); do
    useradd -m -s /bin/bash --no-log-init "krypton${i}"
    chmod 755 "/home/krypton${i}"
done
