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
python3 scripts/build_agent.py
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

# Secret HTTP headers (CTFD_TOKEN, CTFD_SYNC_SECRET, ...) must never be handed
# to curl as a literal argv value: while curl is running, any other user on
# the same box can read its full command line via `ps aux` / `/proc/<pid>/cmdline`.
# Instead we write "Header-Name: value" to a private temp file and pass it as
# `curl --header @file`, so the secret only ever touches disk (mode 0600,
# under a mode 0700 dir, cleaned up on exit/error via trap) — never argv.
secret_headers_dir=""
cleanup_secret_headers() {
    if [ -n "$secret_headers_dir" ] && [ -d "$secret_headers_dir" ]; then
        rm -rf -- "$secret_headers_dir"
    fi
}
trap cleanup_secret_headers EXIT
secret_headers_dir=$(mktemp -d)

write_secret_header() {
    # Usage: write_secret_header "Header-Name" "value"; prints the temp file path.
    local header_name="$1" header_value="$2" header_file
    header_file=$(mktemp "${secret_headers_dir}/header.XXXXXX")
    printf '%s: %s\n' "$header_name" "$header_value" > "$header_file"
    printf '%s' "$header_file"
}

if [ -n "${CTFD_URL:-}" ] && [ -n "${CTFD_TOKEN:-}" ]; then
    # CTFd only honors the Authorization header on requests it recognizes as
    # JSON (see CTFd/utils/initialization's `tokens()` before_request hook,
    # which gates token lookup on request.mimetype == "application/json").
    # Without this header the token is silently ignored, --location follows
    # the resulting redirect to the (HTTP 200) login page, and every
    # challenge_exists() check below then reads that HTML as an empty
    # inventory — every challenge takes the "install as new" path even when
    # it already exists, silently creating duplicates on a second run.
    # `view=admin` is required so this preflight also sees challenges in the
    # "hidden"/"locked" state. CTFd's /api/v1/challenges endpoint filters
    # those out unconditionally unless the caller is an admin AND passes
    # view=admin -- an admin token alone is not enough (see
    # CTFd/api/v1/challenges.py ChallengeList.get(): `admin_view = is_admin()
    # and request.args.get("view") == "admin"`, which feeds
    # get_all_challenges(admin=admin_view)). Without this, every
    # already-installed-but-hidden challenge (e.g. because the wargame-stages
    # plugin hides everything until a stage starts) looks "not found" below,
    # deploy.sh tries to install it fresh, and CTFd's name-uniqueness check
    # fails the run on the first such challenge. See cei-labs-event#30.
    auth_header_file=$(write_secret_header "Authorization" "Token ${CTFD_TOKEN}")
    preflight_code=$(curl "${curl_opts[@]}" -o .ctf/preflight-challenges.json -w '%{http_code}' \
        --header @"$auth_header_file" \
        -H "Content-Type: application/json" \
        "${CTFD_URL}/api/v1/challenges?per_page=100&view=admin")
    rm -f -- "$auth_header_file"
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

    local sync_auth_header_file http_code
    sync_auth_header_file=$(write_secret_header "X-Sync-Auth" "${CTFD_SYNC_SECRET}")
    http_code=$(curl "${curl_opts[@]}" -o /dev/null -w '%{http_code}' \
        -X POST "${CTFD_URL}/plugins/instance-launcher/admin/mappings/sync" \
        --header @"$sync_auth_header_file" \
        -H "Content-Type: application/json" \
        -d "$payload")
    rm -f -- "$sync_auth_header_file"

    if [ "$http_code" = "200" ]; then
        echo "Synced instance mapping for $(basename "$challenge_dir")"
    else
        echo "Error: instance mapping sync returned HTTP ${http_code} for $(basename "$challenge_dir")" >&2
        return 1
    fi
}

# Wallet tiers are deliberately not native CTFd hints.  Upload their local,
# generated manifests only after challenge sync has established the server IDs.
# The signature is passed as a header (via write_secret_header, never argv)
# and neither it nor manifest content is logged.
#
# IMPORTANT: "ctf challenge sync" (called in the loop above, for every
# already-existing challenge) unconditionally DELETES that challenge's
# existing native CTFd hints and only recreates them if challenge.yml
# declares a "hints:" key. None of the generated challenge.yml files do --
# hint content lives solely in the challenges/*-hint-wallet.json manifests
# synced here. So if there IS wallet-bundle content to sync but this step
# gets silently skipped, every native hint on the live instance is wiped
# with nothing to replace it. See docs/P0-CONTENT-DEPLOY-LOG-2026-07-23.md.
sync_hint_wallet_bundle() {
    # NOTE: challenges/agent-hint-wallet.json (AI Copilot Setup's hints) is
    # deliberately NOT included here yet. cei-labs-engine's orchestrator
    # (docker/orchestrator/app/wallet.py) hard-validates the bundle to
    # EXACTLY the 3 tracks {bandit, krypton, natas} and rejects a 4th with
    # HTTP 400 (incomplete_tracks) -- see REQUIRED_TRACKS there. Add it back
    # here once that validation is updated to accept "agent" too (and the
    # orchestrator image is rebuilt/redeployed with that change).
    local wallet_files=(challenges/bandit-hint-wallet.json challenges/krypton-hint-wallet.json challenges/natas-hint-wallet.json)

    # Determine whether there is actually any hint-wallet content that a sync
    # would push. A missing file or a manifest with zero "entries" means this
    # genuinely is a hint-less deploy (nothing for "ctf challenge sync" above
    # to have clobbered a replacement for), so opting out is safe. Non-empty
    # content changes the calculus below.
    local has_content
    has_content=$(python3 - "${wallet_files[@]}" <<'PYEOF'
import json
import sys

found = False
for path in sys.argv[1:]:
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        continue
    if data.get("entries"):
        found = True
        break
print("1" if found else "0")
PYEOF
    ) || { echo "Error: failed to inspect hint-wallet manifests for content." >&2; return 1; }

    # Opt-in secret: the Engine-side plugin this posts to may not be deployed
    # yet. An unset secret is only a safe, silent opt-out when there is no
    # wallet content to sync in the first place. If there IS content, the
    # unconditional native-hint deletion above means silently skipping here
    # would wipe live hints with no replacement -- hard-fail instead.
    if [ -z "${HINT_WALLET_SYNC_SECRET:-}" ]; then
        if [ "$has_content" = "1" ]; then
            echo "❌ FATAL: hint-wallet bundle content exists (${wallet_files[*]}) but HINT_WALLET_SYNC_SECRET is not set." >&2
            echo "   'ctf challenge sync' unconditionally deletes each challenge's native CTFd hints and only" >&2
            echo "   recreates them if challenge.yml declares a 'hints:' key (none do here -- hint content now" >&2
            echo "   lives in the hint-wallet bundle). Skipping this sync would silently wipe every hint on the" >&2
            echo "   live CTFd instance with nothing to replace them. Refusing to proceed." >&2
            echo "   Provision HINT_WALLET_SYNC_SECRET (and HINT_WALLET_REVISION) before rerunning. If this is" >&2
            echo "   genuinely meant to be a hint-less deploy, remove/empty the challenges/*-hint-wallet.json" >&2
            echo "   manifests first so this check can tell the two cases apart." >&2
            return 1
        fi
        echo "HINT_WALLET_SYNC_SECRET not set and no hint-wallet content to sync; skipping hint-wallet sync."
        return 0
    fi
    [ -n "${CTFD_URL:-}" ] || { echo "CTFD_URL is required for hint wallet sync" >&2; return 1; }
    local secret="${HINT_WALLET_SYNC_SECRET}"
    [ "${#secret}" -ge 32 ] || { echo "HINT_WALLET_SYNC_SECRET must be at least 32 characters" >&2; return 1; }
    [[ "${HINT_WALLET_REVISION:-}" =~ ^[1-9][0-9]*$ ]] || { echo "HINT_WALLET_REVISION must be a positive integer" >&2; return 1; }
    # The payload (easily tens of KB -- three tracks' worth of tiered hints)
    # used to round-trip through a shell variable: printed by Python, captured
    # via $(...) command substitution, split on the first newline, then
    # written back out with printf. Confirmed on Windows/Git Bash that this
    # silently DROPS BYTES somewhere in that stdout-capture round-trip --
    # the file that then got signed-and-sent no longer matched what the
    # signature (computed in-process over the same bytes) was actually
    # generated from, so the orchestrator's HMAC check correctly rejected it
    # as invalid_signature every time, with no indication of *why*. Python
    # now writes the signature and payload straight to their own files in
    # binary mode -- no stdout, no shell variable, no text-mode translation
    # of any kind for the large payload to go through.
    local payload_file signature_file
    payload_file=$(mktemp)
    signature_file=$(mktemp)
    HINT_WALLET_PAYLOAD_FILE="$payload_file" HINT_WALLET_SIGNATURE_FILE="$signature_file" \
        python3 - challenges/bandit-hint-wallet.json challenges/krypton-hint-wallet.json challenges/natas-hint-wallet.json <<'PYEOF'
import hashlib, hmac, json, os, sys
manifests=[]
for path in sys.argv[1:]:
    manifests.append(json.load(open(path, encoding="utf-8")))
for item in manifests:
    item["digest"] = hashlib.sha256(json.dumps({k:item[k] for k in ("schema_version","track","entries")}, sort_keys=True, separators=(",",":"), ensure_ascii=False).encode()).hexdigest()
bundle={"schema_version":1,"revision":int(os.environ["HINT_WALLET_REVISION"]),"manifests":manifests}
raw=json.dumps(bundle, sort_keys=True, separators=(",",":"), ensure_ascii=False).encode()
signature=hmac.new(os.environ["HINT_WALLET_SYNC_SECRET"].encode(), raw, hashlib.sha256).hexdigest()
with open(os.environ["HINT_WALLET_PAYLOAD_FILE"], "wb") as f:
    f.write(raw)
with open(os.environ["HINT_WALLET_SIGNATURE_FILE"], "wb") as f:
    f.write(signature.encode("ascii"))
PYEOF
    if [ $? -ne 0 ]; then
        rm -f -- "$payload_file" "$signature_file"
        return 1
    fi
    local signature
    signature=$(cat "$signature_file")
    local curl_insecure=()
    [ "${CTFD_INSECURE:-false}" = "true" ] && curl_insecure=(-k)
    local signature_header_file
    signature_header_file=$(write_secret_header "X-Hint-Wallet-Signature" "$signature")
    curl --fail --silent --show-error "${curl_insecure[@]}" -X POST "${CTFD_URL}/plugins/hint-wallet/machine/sync" \
        --header @"$signature_header_file" -H "Content-Type: application/json" -d @"$payload_file" >/dev/null
    rm -f -- "$signature_header_file" "$payload_file" "$signature_file"
    echo "Synced hint-wallet bundle"
}

# Tells cei-labs-engine's wargame-stages plugin to (re)hide every challenge
# belonging to a game that hasn't started yet. Challenges land from the sync
# loop above at whatever state ctfcli/CTFd gave them (typically visible) --
# without this call, newly-deployed or re-synced challenges sit visible
# under CTFd's Challenges tab until an admin remembers to click "Sync" on
# the plugin's own admin page. Making this automatic on every deploy closes
# that gap. Uses the same CTFD_SYNC_SECRET / X-Sync-Auth pattern as
# sync_instance_mapping above. Fatal on failure -- a deploy that silently
# leaves challenges visible ahead of schedule is worse than one that stops
# and says so.
sync_wargame_stages() {
    if [ -z "${CTFD_SYNC_SECRET:-}" ]; then
        return 0
    fi
    local sync_auth_header_file http_code
    sync_auth_header_file=$(write_secret_header "X-Sync-Auth" "${CTFD_SYNC_SECRET}")
    http_code=$(curl "${curl_opts[@]}" -o /dev/null -w '%{http_code}' \
        -X POST "${CTFD_URL}/plugins/wargame-stages/machine/reconcile" \
        --header @"$sync_auth_header_file" \
        -H "Content-Type: application/json")
    rm -f -- "$sync_auth_header_file"

    if [ "$http_code" = "200" ]; then
        echo "Synced wargame-stages hidden-by-default state"
    else
        echo "Error: wargame-stages reconcile returned HTTP ${http_code}" >&2
        return 1
    fi
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
sync_wargame_stages

echo "=========================================="
if [ "$challenges_found" -eq 0 ]; then
    echo "Error: no challenges were found inside the 'challenges/' directory." >&2
    exit 1
elif [ "$challenges_found" -ne 65 ]; then
    echo "Error: expected 65 challenges, deployed ${challenges_found}." >&2
    exit 1
else
    echo "✅ Deployment Complete! All $challenges_found challenges are synced & live."
fi
echo "=========================================="
