#!/bin/bash
# Starts every level's background daemon (port listeners for levels
# 14-24ish -- see /opt/bandit-daemons/), then execs sshd in the foreground
# as PID 1's replacement. Daemons run as the unprivileged `banditd` user,
# never as root or as any bandit* player account.
set -e

for daemon in /opt/bandit-daemons/*.py; do
    [ -e "$daemon" ] || continue
    su banditd -s /bin/bash -c "python3 '$daemon'" &
done

exec /usr/sbin/sshd -D
