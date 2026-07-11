#!/bin/bash
# Password chain: krypton(N)'s login password = krypton(N-1) challenge's
# flag in CEI-Labs-Wargames/scripts/build_krypton.py -- keep these in sync
# if that script's flags ever change. krypton6's own flag is the FINAL
# flag, submitted directly, not used as any login password (there is no
# krypton7).
#
# Only krypton1 is set here. krypton1's password is level 0's flag, which
# is embedded directly in the CTFd challenge description text (a Base64
# puzzle) rather than anything this container serves -- CTFd descriptions
# don't vary per team, so there's no mechanism to make this per-team
# unique, and it gates no privileged access of its own (level 0 itself
# needs no target instance at all). This is a deliberate scope decision,
# not an oversight -- see docs/security-audit-status.md.
#
# krypton2/4/5/6 are NOT set here -- levels 1/3/4/5's flags (which become
# those passwords) are now per-team secrets generated at container START
# by entrypoint.sh, not build-time hardcoded values shared by every team.
# Until entrypoint.sh runs, those accounts have no usable password at all
# (a locked account is a safe failure mode, not a shared-credential one).
set -e

chpasswd <<'EOF'
krypton1:KRYPTONISGREAT
EOF
