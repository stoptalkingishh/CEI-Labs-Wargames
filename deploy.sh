#!/bin/bash
# CEI-Labs-Wargames Deployment Script
# This script generates all challenge files and uploads them to CTFd.

echo "=========================================="
echo "🚩 Starting CEI-Labs-Wargames Deployment"
echo "=========================================="

echo "[1/3] Generating Challenge Files..."
# Run the Python scripts to build the directories
python3 scripts/build_bandit.py
python3 scripts/build_krypton.py
python3 scripts/build_natas.py

echo "[2/3] Checking CTFd Connection..."
# The 'ctf init' command connects your terminal to your web scoreboard.
# If you haven't connected yet, it will prompt you for your URL and Admin Token.
if [ ! -d ".ctf" ]; then
    ctf init
fi

echo "[3/3] Uploading Challenges to CTFd..."
# Loop through every folder inside /challenges/ and upload it
for dir in challenges/*/ ; do
    echo "Installing challenge from: $dir"
    ctf challenge install "$dir"
    # ctf challenge sync "$dir" # Uncomment this if updating existing challenges
done

echo "=========================================="
echo "✅ Deployment Complete! All challenges are live."
echo "=========================================="
