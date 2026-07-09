#!/bin/bash
# Krypton level 2 (Caesar cipher, unknown shift). Uses the ALREADY-
# COMPILED /krypton/krypton2/encrypt binary itself to produce krypton3's
# ciphertext -- single source of truth for the shift, no risk of a
# second from-scratch implementation drifting out of sync with the real
# binary players actually run.
set -e

FLAG_2="CAESARISEASY"  # -> krypton3's password

mkdir -p /krypton/krypton2
# Random, non-zero, non-human-readable shift byte -- deliberately NOT a
# plain ASCII digit, so `cat keyfile.dat` doesn't just hand the shift over.
head -c1 /dev/urandom > /krypton/krypton2/keyfile.dat

cd /krypton/krypton2
printf '%s' "$FLAG_2" | ./encrypt > /krypton/krypton2/krypton3

cat > /krypton/krypton2/README <<'EOF'
The password for krypton3 is in the file 'krypton3' in this directory,
encrypted with a Caesar cipher using an unknown shift.

The shift is derived from 'keyfile.dat' in this directory (not human-
readable -- don't just cat it). Symlink it into a scratch directory,
then use the 'encrypt' binary here on a known plaintext (like a long
string of 'A's) to observe the shift empirically, and reverse it to
decrypt krypton3.
EOF

chown -R krypton2:krypton2 /krypton/krypton2
chmod 750 /krypton/krypton2
chmod 440 /krypton/krypton2/keyfile.dat /krypton/krypton2/krypton3
chmod 444 /krypton/krypton2/README
chmod 550 /krypton/krypton2/encrypt

echo "Level 2 (Caesar, unknown shift) ciphertext generated."
