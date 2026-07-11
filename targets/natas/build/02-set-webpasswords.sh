#!/bin/bash
# /etc/natas_webpass/natasN holds natasN's OWN HTTP Basic Auth password
# (owner natasN, group natas(N-1), mode 640) -- readable by natasN
# itself AND by natas(N-1), whose vulnerability is what's supposed to
# leak this file's contents to a player who hasn't logged in as natasN
# yet. No file for natas0 -- its password (the literal string "natas0")
# is public/given, matching the real game.
#
# Security: these are now PER-TEAM secrets, generated fresh by
# entrypoint.sh at container START from $LEVEL_SECRETS -- not identical
# hardcoded values baked into every build (see
# docs/security-audit-status.md). This script only creates empty
# placeholder files with correct ownership/permissions so the directory
# structure exists before entrypoint.sh writes the real per-team values;
# if entrypoint.sh doesn't run for some reason, these stay empty (no
# valid password at all -- a safe failure mode, not a shared-credential
# one), matching the same principle already used for Bandit/Krypton's
# per-team secrets.
set -e

mkdir -p /etc/natas_webpass
for i in $(seq 1 14); do
    prev=$((i - 1))
    : > "/etc/natas_webpass/natas${i}"
    chown "natas${i}:natas${prev}" "/etc/natas_webpass/natas${i}"
    chmod 640 "/etc/natas_webpass/natas${i}"
done
