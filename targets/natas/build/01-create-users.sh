#!/bin/bash
# Creates natas0-natas34. No shell/home directory needed -- these
# accounts exist purely so Apache MPM-ITK's AssignUserID can run each
# level's PHP as a distinct, unprivileged Unix identity (there is no SSH
# on this box at all).
set -e

for i in $(seq 0 34); do
    useradd -M -s /usr/sbin/nologin "natas${i}"
done
