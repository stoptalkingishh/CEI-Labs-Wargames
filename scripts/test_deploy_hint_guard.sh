#!/bin/bash
# Regression test for deploy.sh's sync_hint_wallet_bundle() guard.
#
# deploy.sh has no test harness of its own (it's meant to run end-to-end
# against a live CTFd + ctfcli), so this extracts just the
# sync_hint_wallet_bundle() function definition out of deploy.sh via `sed`
# and exercises it directly in an isolated temp directory, without touching
# any of deploy.sh's dependency checks, network calls, or the rest of the
# pipeline.
#
# What this guards against: HINT_WALLET_SYNC_SECRET unset must be a silent,
# safe no-op ONLY when there is genuinely no hint-wallet content to sync.
# When wallet content exists, an unset secret must hard-fail (non-zero exit)
# instead of silently skipping -- because "ctf challenge sync" unconditionally
# deletes native CTFd hints and nothing else would recreate them. See
# docs/P0-CONTENT-DEPLOY-LOG-2026-07-23.md for the real near-incident this
# guards against.
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DEPLOY_SH="$REPO_ROOT/deploy.sh"

pass_count=0
fail_count=0

note() { echo "  $*"; }
pass() { pass_count=$((pass_count + 1)); echo "PASS: $*"; }
fail() { fail_count=$((fail_count + 1)); echo "FAIL: $*" >&2; }

# Extract just the sync_hint_wallet_bundle() function body out of deploy.sh
# (from its `name() {` line to the matching top-of-line `}`) and source it
# into this shell, so we test the actual production code rather than a copy.
extracted="$(sed -n '/^sync_hint_wallet_bundle() {/,/^}/p' "$DEPLOY_SH")"
if [ -z "$extracted" ]; then
    echo "FATAL: could not extract sync_hint_wallet_bundle() from $DEPLOY_SH -- has it been renamed/moved?" >&2
    exit 1
fi
eval "$extracted"

work_dir="$(mktemp -d)"
cleanup() { rm -rf "$work_dir"; }
trap cleanup EXIT

run_case() {
    # Runs sync_hint_wallet_bundle() with CWD set to a fresh scenario
    # directory so relative challenges/*.json paths resolve as deploy.sh
    # expects. Sets $case_output and $case_status. Deliberately does NOT
    # let a non-zero return here trip this test script's own `set -e`
    # (several cases below are expected to fail) -- an `if`/`else` around
    # the command substitution is what keeps `set -e` from applying to it.
    local scenario_dir="$1"
    if case_output="$( cd "$scenario_dir" && sync_hint_wallet_bundle 2>&1 )"; then
        case_status=0
    else
        case_status=$?
    fi
}

# --- Case 1: secret unset, real hint content present -> must hard-fail ---
case1_dir="$work_dir/case1-content-no-secret"
mkdir -p "$case1_dir/challenges"
cat > "$case1_dir/challenges/bandit-hint-wallet.json" <<'JSON'
{"schema_version": 1, "track": "bandit", "entries": [{"name": "bandit-00", "tiers": [{"tier": 1, "cost": 5, "content": "ssh -h"}]}]}
JSON
cat > "$case1_dir/challenges/krypton-hint-wallet.json" <<'JSON'
{"schema_version": 1, "track": "krypton", "entries": []}
JSON
cat > "$case1_dir/challenges/natas-hint-wallet.json" <<'JSON'
{"schema_version": 1, "track": "natas", "entries": []}
JSON

unset HINT_WALLET_SYNC_SECRET HINT_WALLET_REVISION CTFD_URL || true
run_case "$case1_dir"
if [ "$case_status" -ne 0 ]; then
    pass "unset secret + real wallet content hard-fails (exit $case_status)"
else
    fail "unset secret + real wallet content should hard-fail but exited 0"
    note "output was: $case_output"
fi
if echo "$case_output" | grep -q "FATAL"; then
    pass "hard-fail case prints a loud FATAL error message"
else
    fail "hard-fail case did not print an obvious FATAL error message"
    note "output was: $case_output"
fi

# --- Case 2: secret unset, no wallet content at all -> must stay a clean, non-fatal skip ---
case2_dir="$work_dir/case2-no-content-no-secret"
mkdir -p "$case2_dir/challenges"
cat > "$case2_dir/challenges/bandit-hint-wallet.json" <<'JSON'
{"schema_version": 1, "track": "bandit", "entries": []}
JSON
cat > "$case2_dir/challenges/krypton-hint-wallet.json" <<'JSON'
{"schema_version": 1, "track": "krypton", "entries": []}
JSON
cat > "$case2_dir/challenges/natas-hint-wallet.json" <<'JSON'
{"schema_version": 1, "track": "natas", "entries": []}
JSON

unset HINT_WALLET_SYNC_SECRET HINT_WALLET_REVISION CTFD_URL || true
run_case "$case2_dir"
if [ "$case_status" -eq 0 ]; then
    pass "unset secret + no wallet content stays a clean skip (exit 0)"
else
    fail "unset secret + no wallet content should exit 0 but exited $case_status"
    note "output was: $case_output"
fi

# --- Case 3: secret unset, manifests missing entirely -> must also be a clean skip ---
case3_dir="$work_dir/case3-missing-files-no-secret"
mkdir -p "$case3_dir/challenges"

unset HINT_WALLET_SYNC_SECRET HINT_WALLET_REVISION CTFD_URL || true
run_case "$case3_dir"
if [ "$case_status" -eq 0 ]; then
    pass "unset secret + missing manifests stays a clean skip (exit 0)"
else
    fail "unset secret + missing manifests should exit 0 but exited $case_status"
    note "output was: $case_output"
fi

# --- Case 4: secret set but too short -> existing validation must still fire ---
case4_dir="$work_dir/case4-short-secret"
mkdir -p "$case4_dir/challenges"
cp "$case1_dir/challenges/"*.json "$case4_dir/challenges/"

HINT_WALLET_SYNC_SECRET="tooshort"
CTFD_URL="https://example.invalid"
export HINT_WALLET_SYNC_SECRET CTFD_URL
run_case "$case4_dir"
unset HINT_WALLET_SYNC_SECRET CTFD_URL
if [ "$case_status" -ne 0 ]; then
    pass "secret set but under 32 chars still fails validation (exit $case_status)"
else
    fail "secret set but under 32 chars should still fail but exited 0"
    note "output was: $case_output"
fi

echo "----------------------------------------"
echo "$pass_count passed, $fail_count failed"
[ "$fail_count" -eq 0 ]
