#!/bin/bash
# Level 21->22: world-readable script (bandit21 can cat this directly to
# see what it does), copies bandit22's password to a world-readable
# output file cron re-creates every minute. The source file itself is
# NOT chmodded -- that would make bandit22's password world-readable
# outright instead of gated behind reading this script and waiting a tick.
cp /etc/bandit_pass/bandit22 /tmp/cronjob_bandit22/output
chmod 644 /tmp/cronjob_bandit22/output
