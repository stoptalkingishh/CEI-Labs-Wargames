#!/bin/bash
# Krypton level 6 (LFSR stream cipher, final level). Uses the ALREADY-
# COMPILED /krypton/krypton6/encrypt binary to produce the final
# ciphertext -- same single-source-of-truth reasoning as level 2.
set -e

FINAL_FLAG="LFSRISNOTRANDOM"

mkdir -p /krypton/krypton6
cd /krypton/krypton6
printf '%s' "$FINAL_FLAG" | ./encrypt > /krypton/krypton6/final

cat > /krypton/krypton6/README <<'EOF'
The final Krypton flag is in the file 'final' in this directory,
encrypted with a stream cipher whose keystream repeats every 30
characters (the 'encrypt' binary here implements it).

Encrypt a long run of identical letters (e.g. 30+ 'A's) with 'encrypt'
to read the repeating keystream directly off the output, then use it to
decrypt 'final'.
EOF

chown -R krypton6:krypton6 /krypton/krypton6
chmod 750 /krypton/krypton6
chmod 440 /krypton/krypton6/final
chmod 444 /krypton/krypton6/README
chmod 550 /krypton/krypton6/encrypt

echo "Level 6 (LFSR stream cipher, final) ciphertext generated."
