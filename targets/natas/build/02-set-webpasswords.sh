#!/bin/bash
# /etc/natas_webpass/natasN holds natasN's OWN HTTP Basic Auth password
# (owner natasN, group natas(N-1), mode 640) -- readable by natasN
# itself AND by natas(N-1), whose vulnerability is what's supposed to
# leak this file's contents to a player who hasn't logged in as natasN
# yet. No file for natas0 -- its password (the literal string "natas0")
# is public/given, matching the real game.
#
# Values here are natas(N-1)'s challenge flag in
# CEI-Labs-Wargames/scripts/build_natas.py -- keep in sync if those flags
# ever change. natas14's OWN flag is the FINAL flag, revealed directly by
# the SQLi bypass rather than stored in a webpass file (there is no
# natas15).
set -e

mkdir -p /etc/natas_webpass
declare -A PASS=(
  [1]="g9D9cREhslqBKtcA2uVOCe7MbL6WAocT"
  [2]="ZluruAthQk7Q2MqmDeTiUij2ZvWy2mBi"
  [3]="sJIJNW6ucpu6HPZ1ZAyN8VRdTepNnQA4"
  [4]="Z9mAndu1YccU99H73fsu6mptUz2uEAte"
  [5]="iCOgHandNo6eV127665PhSAsgS2abV0M"
  [6]="f94020Bh6bUNF6M9776QvSAsSgS2abV0"
  [7]="7z3hDeo6i6vF9M9776QvSAsSgS2abV0M"
  [8]="8Ps3hDeo6i6vF9M9776QvSAsSgS2abV0"
  [9]="W0608Rh6bUNF6M9776QvSAsSgS2abV0M"
  [10]="n94020Bh6bUNF6M9776QvSAsSgS2abV0"
  [11]="U0608Rh6bUNF6M9776QvSAsSgS2abV0M"
  [12]="ED9020Bh6bUNF6M9776QvSAsSgS2abV0"
  [13]="j0608Rh6bUNF6M9776QvSAsSgS2abV0M"
  [14]="L0608Rh6bUNF6M9776QvSAsSgS2abV0M"
)

for i in "${!PASS[@]}"; do
    prev=$((i - 1))
    echo -n "${PASS[$i]}" > "/etc/natas_webpass/natas${i}"
    chown "natas${i}:natas${prev}" "/etc/natas_webpass/natas${i}"
    chmod 640 "/etc/natas_webpass/natas${i}"
done
