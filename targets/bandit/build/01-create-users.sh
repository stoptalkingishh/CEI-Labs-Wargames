#!/bin/bash
# Creates bandit0-bandit33, each with a home dir and bash shell.
# Passwords are set in 02-set-passwords.sh (kept separate so the password
# chain -- which must match CTFd's already-defined flags exactly -- is easy
# to audit on its own).
set -e

for i in $(seq 0 33); do
    useradd -m -s /bin/bash --no-log-init "bandit${i}"
    chmod 755 "/home/bandit${i}"
done
