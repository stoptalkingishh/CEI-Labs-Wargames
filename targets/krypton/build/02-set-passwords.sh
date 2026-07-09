#!/bin/bash
# Password chain: krypton(N)'s login password = krypton(N-1) challenge's
# flag in CEI-Labs-Wargames/scripts/build_krypton.py -- keep these in sync
# if that script's flags ever change. krypton6's own flag
# (LFSRISNOTRANDOM) is the FINAL flag, submitted directly, not used as
# any login password (there is no krypton7).
set -e

chpasswd <<'EOF'
krypton1:KRYPTONISGREAT
krypton2:ROTTEN
krypton3:CAESARISEASY
krypton4:BRUTE
krypton5:CLEARTEXT
krypton6:RANDOM
EOF
