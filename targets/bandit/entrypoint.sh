#!/bin/bash
# Starts every level's background daemon (port listeners for levels
# 14-24ish -- see /opt/bandit-daemons/) and the cron daemon (levels
# 21-23's lessons depend on it actually firing on schedule), then execs
# sshd in the foreground as PID 1's replacement. Port-listener daemons
# run as the unprivileged `banditd` user, never as root or as any
# bandit* player account; cron necessarily runs as root (it's what lets
# it su into each level's own user per /etc/cron.d's user field), same
# trust level as sshd itself.
set -e

for daemon in /opt/bandit-daemons/*.py; do
    [ -e "$daemon" ] || continue
    su banditd -s /bin/bash -c "python3 '$daemon'" &
done

cron

exec /usr/sbin/sshd -D
