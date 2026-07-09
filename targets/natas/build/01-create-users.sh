#!/bin/bash
# Creates natas0-natas14. No shell/home directory needed -- these
# accounts exist purely so Apache MPM-ITK's AssignUserID can run each
# level's PHP as a distinct, unprivileged Unix identity (there is no SSH
# on this box at all).
set -e

for i in $(seq 0 14); do
    useradd -M -s /usr/sbin/nologin "natas${i}"
done
