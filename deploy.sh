#!/bin/bash
# CEI-Labs-Wargames Deployment Script
# This script generates all challenge files and uploads them to CTFd non-interactively.
set -e

# Prevent glob expansion failures if no directories match
shopt -s nullglob

echo "=========================================="
echo "🚩 Starting CEI-Labs-Wargames Deployment"
echo "=========================================="

# 1. Dependency Checks
echo "[1/4] Verifying dependencies..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed. Please install Python 3." >&2
    exit 1
fi

if ! command -v ctf &> /dev/null; then
    echo "❌ Error: 'ctfcli' (ctf command) is not installed." >&2
    echo "   Please install it using: pip install ctfcli" >&2
    exit 1
fi
echo "✓ All dependencies met."

# 2. Challenge File Generation
echo "[2/4] Generating Challenge Files..."
python3 scripts/build_bandit.py
python3 scripts/build_krypton.py
python3 scripts/build_natas.py

# 3. Connection and Authentication Configuration
echo "[3/4] Checking CTFd Connection..."
if [ -n "$CTFD_URL" ] && [ -n "$CTFD_TOKEN" ]; then
    echo "Found CTFD environment variables. Configuring ctfcli non-interactively..."
    mkdir -p .ctf
    cat << EOF > .ctf/config
[config]
url = $CTFD_URL
access_token = $CTFD_TOKEN
EOF
    if [ "${CTFD_INSECURE:-false}" = "true" ]; then
        echo "ssl_verify = false" >> .ctf/config
        echo "⚠️  CTFD_INSECURE=true — TLS certificate verification is disabled."
    fi
    printf '
[challenges]
' >> .ctf/config
elif [ ! -d ".ctf" ]; then
    echo "⚠️  No existing configuration found and CTFD environment variables are empty."
    echo "   Prompting for interactive initialization..."
    ctf init
fi

# Pushes a challenge's instance_type/image/instance_group/etc. (if its
# challenge.yml declares any) into CTFd's instance-launcher plugin, so a
# "Launch Environment" button appears. Mirrors cei-labs-engine's
# scripts/challenges-load.sh sync_instance_mapping() function exactly —
# same payload shape, same endpoint, same header name — but reads the
# shared secret from an env var instead of a local secrets file, since
# this repo isn't colocated with cei-labs-engine's docker/secrets/.
# ctfcli itself has no concept of instance_type; without this step those
# fields in challenge.yml are silently ignored.
sync_instance_mapping() {
    local challenge_dir="$1"
    local challenge_yaml="$challenge_dir/challenge.yml"

    if [ -z "${CTFD_SYNC_SECRET:-}" ] || [ ! -f "$challenge_yaml" ]; then
        return 0
    fi

    local payload
    payload=$(python3 - "$challenge_yaml" <<'PYEOF' 2>/dev/null || true
import json
import sys

import yaml

with open(sys.argv[1]) as f:
    data = yaml.safe_load(f) or {}

instance_type = data.get("instance_type")
if not instance_type:
    sys.exit(0)

print(json.dumps({
    "challenge_name": data.get("name"),
    "instance_type": instance_type,
    "image": data.get("image"),
    "port": data.get("port"),
    "target_image": data.get("target_image"),
    "attacker_image": data.get("attacker_image"),
    "attacker_port": data.get("attacker_port"),
    "instance_group": data.get("instance_group"),
    "shutdown_on_solve": data.get("shutdown_on_solve", True),
}))
PYEOF
    )

    [ -z "$payload" ] && return 0

    local http_code
    http_code=$(curl -sk -o /dev/null -w '%{http_code}' \
        -X POST "${CTFD_URL}/plugins/instance-launcher/admin/mappings/sync" \
        -H "X-Sync-Auth: ${CTFD_SYNC_SECRET}" \
        -H "Content-Type: application/json" \
        -d "$payload")

    if [ "$http_code" = "200" ]; then
        echo "Synced instance mapping for $(basename "$challenge_dir")"
    else
        echo "⚠️  Instance mapping sync returned HTTP ${http_code} for $(basename "$challenge_dir")"
    fi
}

# 4. Challenge Upload and Sync Loop
echo "[4/4] Syncing Challenges to CTFd..."
if [ -z "${CTFD_SYNC_SECRET:-}" ]; then
    echo "ℹ️  CTFD_SYNC_SECRET not set — challenge content will sync, but no"
    echo "   'Launch Environment' buttons will be wired up. Set it (the same"
    echo "   value as cei-labs-engine's plugin_shared_secret Docker secret)"
    echo "   to enable instance-launcher mapping sync."
fi
challenges_found=0

for dir in challenges/*/ ; do
    challenges_found=$((challenges_found + 1))
    # Strip trailing slash for consistent ctfcli paths
    dir_trimmed="${dir%/}"
    echo "----------------------------------------"
    echo "Syncing challenge from: $dir_trimmed"

    # Try syncing first (which updates changes). If it fails because the
    # challenge doesn't exist yet on the server, install it.
    if ! ctf challenge sync "$dir_trimmed" 2>/dev/null; then
        echo "Challenge not found on CTFd. Installing challenge as new..."
        ctf challenge install "$dir_trimmed"
    else
        echo "Successfully synced challenge metadata!"
    fi

    sync_instance_mapping "$dir_trimmed"
done

echo "=========================================="
if [ "$challenges_found" -eq 0 ]; then
    echo "⚠️  Warning: No challenges were found inside the 'challenges/' directory."
else
    echo "✅ Deployment Complete! All $challenges_found challenges are synced & live."
fi
echo "=========================================="

