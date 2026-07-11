#!/bin/bash
# No background daemons for Krypton (all 7 levels are pure crypto
# puzzles, nothing needs a listening service beyond sshd itself).
#
# Level 2's ciphertext/keyfile/README and krypton3's login password ARE
# generated here, at container START, from a per-team secret in
# $LEVEL_SECRETS (a JSON blob the orchestrator injects -- see
# cei-labs-engine's instance_types.py generate_track_secrets()). This is
# what makes them unique per team instead of an identical hardcoded value
# baked into every build (see docs/security-audit-status.md). If
# $LEVEL_SECRETS has no "krypton2" key (e.g. CTFd content hasn't been
# synced with the per_team_dynamic flag yet), krypton3 is simply left
# with no usable password -- a locked account is a safe failure mode,
# not a shared-credential one, so this does not refuse to start the
# whole box over it. krypton1/4/5/6 are still build-time hardcoded for
# now -- see docs/self-hosted-wargames-status.md for what's converted
# so far.
set -e

KRYPTON2_SECRET=""
if [ -n "${LEVEL_SECRETS:-}" ]; then
    KRYPTON2_SECRET=$(python3 -c "
import json, os
print(json.loads(os.environ.get('LEVEL_SECRETS', '{}')).get('krypton2', ''))
")
fi

if [ -n "$KRYPTON2_SECRET" ]; then
    echo "krypton3:${KRYPTON2_SECRET}" | chpasswd

    # Random, non-zero, non-human-readable shift byte -- deliberately NOT
    # a plain ASCII digit, so `cat keyfile.dat` doesn't just hand the
    # shift over. Same source and property as the build-time version this
    # replaces.
    head -c1 /dev/urandom > /krypton/krypton2/keyfile.dat
    (cd /krypton/krypton2 && printf '%s' "$KRYPTON2_SECRET" | ./encrypt > /krypton/krypton2/krypton3)

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
else
    echo "WARNING: no krypton2 key in LEVEL_SECRETS -- level 2/3 will not be playable until content is synced." >&2
fi

exec /usr/sbin/sshd -D
