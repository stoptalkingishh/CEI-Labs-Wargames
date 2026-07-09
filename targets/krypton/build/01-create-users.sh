#!/bin/bash
# Creates krypton1-krypton6 (no krypton0 -- level 0 needs no SSH login at
# all, it's just a Base64 string given directly in the challenge
# description, matching build_krypton.py's own level-0 text).
set -e

for i in $(seq 1 6); do
    useradd -m -s /bin/bash --no-log-init "krypton${i}"
    chmod 755 "/home/krypton${i}"
done
