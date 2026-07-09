#!/bin/bash
# Level 21->22: world-readable script (bandit21 can cat this directly to
# see what it does), copies bandit22's password to a world-readable
# output file cron re-creates every minute.
chmod 644 /etc/bandit_pass/bandit22
cp /etc/bandit_pass/bandit22 /tmp/cronjob_bandit22/output
chmod 644 /tmp/cronjob_bandit22/output
