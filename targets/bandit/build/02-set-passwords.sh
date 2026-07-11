#!/bin/bash
# Password chain: bandit(N)'s login password = bandit-(N-1) challenge's
# flag. bandit0 uses the fixed starting credential matching the challenge
# text ("Username: bandit0, Password: bandit0") -- OverTheWire's
# well-known public bootstrap credential, not a secret, so it stays
# static (same scope decision as Natas/Krypton's level 0).
#
# Every other account is intentionally left WITHOUT a password here --
# bandit1-33's passwords are now per-team secrets generated at container
# START by entrypoint.sh (see docs/security-audit-status.md), not
# build-time hardcoded values shared by every team. Until entrypoint.sh
# runs, those accounts have no usable password at all (a locked account
# is a safe failure mode, not a shared-credential one).
set -e

chpasswd <<'EOF'
bandit0:bandit0
EOF
