#!/bin/sh
# bandit26's login shell: pages a short text file and exits. Normally
# invisible/instant on a full-size terminal (more shows everything at
# once and exits) -- the lesson is resizing your terminal to just a few
# rows BEFORE/while connecting so `more` has to pause with "--More--",
# at which point pressing `v` launches an editor (vi) that can escape to
# a real shell.
echo "Executing showtext"
export TERM=linux
more /home/bandit26/text.txt
exit 0
