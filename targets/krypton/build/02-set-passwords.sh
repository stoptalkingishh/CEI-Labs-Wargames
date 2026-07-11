#!/bin/bash
# Password chain: krypton(N)'s login password = krypton(N-1) challenge's
# flag in CEI-Labs-Wargames/scripts/build_krypton.py -- keep these in sync
# if that script's flags ever change. krypton6's own flag
# (LFSRISNOTRANDOM) is the FINAL flag, submitted directly, not used as
# any login password (there is no krypton7).
#
# krypton3 is deliberately NOT set here -- level 2's flag (which becomes
# krypton3's password) is now a per-team secret generated at container
# START by entrypoint.sh, not a build-time hardcoded value shared by every
# team (see docs/security-audit-status.md). Until entrypoint.sh runs,
# krypton3 has no usable password at all (a locked account is a safe
# failure mode, not a shared-credential one). krypton1/4/5/6 are still
# build-time hardcoded for now -- see docs/self-hosted-wargames-status.md
# for what's converted so far.
set -e

chpasswd <<'EOF'
krypton1:KRYPTONISGREAT
krypton2:ROTTEN
krypton4:BRUTE
krypton5:CLEARTEXT
krypton6:RANDOM
EOF
