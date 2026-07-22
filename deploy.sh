#!/bin/bash
# CEI-Labs-Wargames Deployment Script
# This script generates all challenge files and uploads them to CTFd non-interactively.
set -Eeuo pipefail
umask 077

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

if { [ -n "${CTFD_URL:-}" ] && [ -z "${CTFD_TOKEN:-}" ]; } || \
   { [ -z "${CTFD_URL:-}" ] && [ -n "${CTFD_TOKEN:-}" ]; }; then
    echo "Error: CTFD_URL and CTFD_TOKEN must be set together." >&2
    exit 1
fi
if [ -z "${CTFD_URL:-}" ] || [ -z "${CTFD_TOKEN:-}" ]; then
    echo "Error: non-interactive deployment requires CTFD_URL and CTFD_TOKEN." >&2
    exit 1
fi
if [ -z "${CTFD_SYNC_SECRET:-}" ]; then
    echo "Error: CTFD_SYNC_SECRET is required so launcher mappings cannot be silently skipped." >&2
    exit 1
fi
echo "✓ All dependencies met."

# 2. Challenge File Generation
echo "[2/4] Generating Challenge Files..."
python3 scripts/build_bandit.py
python3 scripts/build_krypton.py
python3 scripts/build_natas.py
python3 scripts/validate_game_stages.py
python3 scripts/validate_generated.py --output deployment-manifest.json

# 3. Connection and Authentication Configuration
echo "[3/4] Checking CTFd Connection..."
if [ -n "${CTFD_URL:-}" ] && [ -n "${CTFD_TOKEN:-}" ]; then
    echo "Found CTFD environment variables. Configuring ctfcli non-interactively..."
    mkdir -p .ctf
    cat << EOF > .ctf/config
[config]
url = $CTFD_URL
access_token = $CTFD_TOKEN
EOF
    chmod 600 .ctf/config
    if [ "${CTFD_INSECURE:-false}" = "true" ]; then
        echo "ssl_verify = false" >> .ctf/config
        echo "⚠️  CTFD_INSECURE=true — TLS certificate verification is disabled."
    fi
    printf '
[challenges]
' >> .ctf/config
fi

curl_opts=(--silent --show-error --location)
if [ "${CTFD_INSECURE:-false}" = "true" ]; then
    curl_opts+=(--insecure)
fi

if [ -n "${CTFD_URL:-}" ] && [ -n "${CTFD_TOKEN:-}" ]; then
    # CTFd only honors the Authorization header on requests it recognizes as
    # JSON (see CTFd/utils/initialization's `tokens()` before_request hook,
    # which gates token lookup on request.mimetype == "application/json").
    # Without this header the token is silently ignored, --location follows
    # the resulting redirect to the (HTTP 200) login page, and every
    # challenge_exists() check below then reads that HTML as an empty
    # inventory — every challenge takes the "install as new" path even when
    # it already exists, silently creating duplicates on a second run.
    preflight_code=$(curl "${curl_opts[@]}" -o .ctf/preflight-challenges.json -w '%{http_code}' \
        -H "Authorization: Token ${CTFD_TOKEN}" \
        -H "Content-Type: application/json" \
        "${CTFD_URL}/api/v1/challenges?per_page=100")
    if [ "$preflight_code" != "200" ]; then
        echo "Error: CTFd authentication preflight returned HTTP ${preflight_code}." >&2
        exit 1
    fi
fi

challenge_exists() {
    python3 - "$1" .ctf/preflight-challenges.json <<'PYEOF'
import json
import sys
import yaml

with open(sys.argv[1], encoding="utf-8") as challenge_file:
    wanted = (yaml.safe_load(challenge_file) or {}).get("name")
with open(sys.argv[2], encoding="utf-8") as inventory_file:
    inventory = json.load(inventory_file)
names = {row.get("name") for row in inventory.get("data", [])}
raise SystemExit(0 if wanted in names else 1)
PYEOF
}

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
    payload=$(python3 - "$challenge_yaml" <<'PYEOF'
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
    http_code=$(curl "${curl_opts[@]}" -o /dev/null -w '%{http_code}' \
        -X POST "${CTFD_URL}/plugins/instance-launcher/admin/mappings/sync" \
        -H "X-Sync-Auth: ${CTFD_SYNC_SECRET}" \
        -H "Content-Type: application/json" \
        -d "$payload")

    if [ "$http_code" = "200" ]; then
        echo "Synced instance mapping for $(basename "$challenge_dir")"
    else
        echo "Error: instance mapping sync returned HTTP ${http_code} for $(basename "$challenge_dir")" >&2
        return 1
    fi
}

# Wallet tiers are deliberately not native CTFd hints.  Upload their local,
# generated manifests only after challenge sync has established the server IDs.
# The token is passed as a header and neither it nor manifest content is logged.
sync_hint_wallet_bundle() {
    # Opt-in: the Engine-side plugin this posts to may not be deployed yet,
    # so an unset secret skips the sync instead of failing every deploy.
    if [ -z "${HINT_WALLET_SYNC_SECRET:-}" ]; then
        echo "HINT_WALLET_SYNC_SECRET not set; skipping hint-wallet sync."
        return 0
    fi
    [ -n "${CTFD_URL:-}" ] || { echo "CTFD_URL is required for hint wallet sync" >&2; return 1; }
    local secret="${HINT_WALLET_SYNC_SECRET}"
    [ "${#secret}" -ge 32 ] || { echo "HINT_WALLET_SYNC_SECRET must be at least 32 characters" >&2; return 1; }
    [[ "${HINT_WALLET_REVISION:-}" =~ ^[1-9][0-9]*$ ]] || { echo "HINT_WALLET_REVISION must be a positive integer" >&2; return 1; }
    local payload
    payload=$(python3 - challenges/bandit-hint-wallet.json challenges/krypton-hint-wallet.json challenges/natas-hint-wallet.json <<'PYEOF'
import hashlib, hmac, json, os, sys
manifests=[]
for path in sys.argv[1:]:
    manifests.append(json.load(open(path, encoding="utf-8")))
for item in manifests:
    item["digest"] = hashlib.sha256(json.dumps({k:item[k] for k in ("schema_version","track","entries")}, sort_keys=True, separators=(",",":"), ensure_ascii=False).encode()).hexdigest()
bundle={"schema_version":1,"revision":int(os.environ["HINT_WALLET_REVISION"]),"manifests":manifests}
raw=json.dumps(bundle, sort_keys=True, separators=(",",":"), ensure_ascii=False).encode()
print(hmac.new(os.environ["HINT_WALLET_SYNC_SECRET"].encode(), raw, hashlib.sha256).hexdigest())
print(json.dumps(bundle, separators=(",",":"), ensure_ascii=False))
PYEOF
    ) || return 1
    local signature="${payload%%$'\n'*}"; payload="${payload#*$'\n'}"
    local curl_insecure=()
    [ "${CTFD_INSECURE:-false}" = "true" ] && curl_insecure=(-k)
    curl --fail --silent --show-error "${curl_insecure[@]}" -X POST "${CTFD_URL}/plugins/hint-wallet/machine/sync" \
        -H "X-Hint-Wallet-Signature: ${signature}" -H "Content-Type: application/json" -d "$payload" >/dev/null
    echo "Synced hint-wallet bundle"
}

# 4. Challenge Upload and Sync Loop
echo "[4/4] Syncing Challenges to CTFd..."
challenges_found=0

for dir in challenges/*/ ; do
    challenges_found=$((challenges_found + 1))
    # Strip trailing slash for consistent ctfcli paths
    dir_trimmed="${dir%/}"
    echo "----------------------------------------"
    echo "Syncing challenge from: $dir_trimmed"

    # Decide install versus sync from the authenticated preflight inventory.
    # A sync failure is now fatal instead of being misclassified as "missing".
    if challenge_exists "$dir_trimmed/challenge.yml"; then
        ctf challenge sync "$dir_trimmed"
        echo "Successfully synced challenge metadata!"
    else
        echo "Challenge not found on CTFd. Installing challenge as new..."
        ctf challenge install "$dir_trimmed"
    fi

    sync_instance_mapping "$dir_trimmed"
done

sync_hint_wallet_bundle

echo "=========================================="
if [ "$challenges_found" -eq 0 ]; then
    echo "Error: no challenges were found inside the 'challenges/' directory." >&2
    exit 1
elif [ "$challenges_found" -ne 59 ]; then
    echo "Error: expected 59 challenges, deployed ${challenges_found}." >&2
    exit 1
else
    echo "✅ Deployment Complete! All $challenges_found challenges are synced & live."
fi
echo "=========================================="
