#!/bin/bash
# Level 23->24: world-readable script (revealing the mechanic) that runs
# EVERY script dropped into a world-writable spool directory, as bandit24
# -- letting bandit23 drop their own script to read bandit24's password.
for i in /var/spool/bandit24/*; do
    timeout -s SIGKILL 60 su - bandit24 -c "bash -c \"cd /var/spool/bandit24 && source $i\""
    rm -f "$i"
done
