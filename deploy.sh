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

# 4. Challenge Upload and Sync Loop
echo "[4/4] Syncing Challenges to CTFd..."
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
done

echo "=========================================="
if [ "$challenges_found" -eq 0 ]; then
    echo "⚠️  Warning: No challenges were found inside the 'challenges/' directory."
else
    echo "✅ Deployment Complete! All $challenges_found challenges are synced & live."
fi
echo "=========================================="

