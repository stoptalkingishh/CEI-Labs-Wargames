#!/bin/bash
# Password chain: krypton(N)'s login password = krypton(N-1) challenge's
# flag in CEI-Labs-Wargames/scripts/build_krypton.py -- keep these in sync
# if that script's flags ever change. krypton6's own flag is the FINAL
# flag, submitted directly, not used as any login password (there is no
# krypton7).
#
# krypton0 is the one exception, and it's the ONLY account set here:
# it's the entry point, with no level -1 flag to chain from. Bandit has
# the identical problem for its own level 0 and solves it the same way
# -- a fixed, publicly-known initial password (bandit0/bandit0). krypton0
# follows that exact precedent: the login password is the fixed,
# publicly-known literal string "krypton0" (same as the username), set
# here at build time since it isn't -- and can't be -- scoped to any
# per-team secret. Anyone starting Krypton knows it already, same as
# Bandit's front door; it gates no privileged access of its own beyond
# krypton0's per-team puzzle content (written by entrypoint.sh).
#
# krypton1-6 are NOT set here. This used to be true only for krypton2-6
# -- krypton1's password was previously level 0's flag, which was a
# static string embedded directly in the CTFd challenge description
# (CTFd descriptions don't vary per team, so there was no per-team
# mechanism for it; see docs/security-audit-status.md and
# cei-labs-event#17). krypton0 now has a real per-team secret of its
# own, so krypton1's password is generated the same way as krypton2-6:
# at container START by entrypoint.sh from a per-team secret, not a
# build-time hardcoded value shared by every team. Until entrypoint.sh
# runs, krypton1-6 have no usable password at all (a locked account is a
# safe failure mode, not a shared-credential one).
set -e

chpasswd <<'EOF'
krypton0:krypton0
EOF
