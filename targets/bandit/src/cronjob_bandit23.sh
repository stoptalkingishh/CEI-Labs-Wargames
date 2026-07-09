#!/bin/bash
# Level 22->23: this script is NOT readable by bandit22 (mode 700) --
# the lesson is figuring out where its output lands without reading the
# source, via the predictable $(whoami) filename (this script runs AS
# bandit23 per the cron.d entry, so $(whoami) is always "bandit23").
cp /etc/bandit_pass/bandit23 "/tmp/cronjob_bandit23/$(whoami)"
chmod 644 "/tmp/cronjob_bandit23/$(whoami)"
