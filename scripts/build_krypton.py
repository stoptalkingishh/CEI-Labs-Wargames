import os

# Self-hosted image reference (see docs/self-hosted-wargames-blueprint.md
# Phase 3's "Wire Krypton into CTFd" task). Not yet published by a CI
# workflow -- until it is, build+tag locally with this exact name/tag
# before deploying (`docker build -t ghcr.io/stoptalkingishh/cei-labs-
# wargames/krypton-target:latest targets/krypton`) so `docker stack
# deploy` can find it.
KRYPTON_IMAGE = "ghcr.io/stoptalkingishh/cei-labs-wargames/krypton-target:latest"

# All 7 challenges share ONE instance_group -- same "one box, many
# levels" design as Bandit. Only the final level opts into
# shutdown_on_solve.
INSTANCE_GROUP = "krypton"

# A player's connection details (host/port, live status) come from the
# "Launch Environment" control on this challenge itself -- injected into
# the challenge view by cei-labs-engine's instance-launcher plugin, not
# written into these descriptions, since the port is only known once an
# instance actually exists. See the "Krypton: Start Here" challenge for
# how that control works. All levels 1-6 connect as a Linux user named
# after the level (`krypton1`, `krypton2`, ...) using the previous level's
# flag as that account's password.

# Define the dataset for Krypton Levels 0 to 6 based on OTW specifications
challenges_data = [
    {
        "id": "krypton-00",
        "name": "Krypton 0 -> 1: Base64 Decoding",
        "points": 200,
        "desc": "**Goal:** Decode a Base64-encoded password.\n\nThis level needs no environment at all -- the following string encodes the password for level 1 in Base64:\n\n`S1JZUFRPTklTR1JFQVQ=`\n\nDecode it (e.g. with the `base64 -d` command) to find the flag.",
        "flag": "KRYPTONISGREAT"
    },
    {
        "id": "krypton-01",
        "name": "Krypton 1 -> 2: ROT13 Substitution Cipher",
        "points": 250,
        "desc": "**Goal:** Reverse a ROT13 rotation cipher.\n\nLog in as `krypton1`. The next password is in `/krypton/krypton1/krypton2`, encrypted with a simple ROT13 rotation.\n\n*Hint: the `tr` command translates characters directly, e.g. `tr \"[:alpha:]\" \"N-ZA-Mn-za-m\"`.*",
        "flag": "ROTTEN"
    },
    {
        "id": "krypton-02",
        "name": "Krypton 2 -> 3: Caesar Cipher (Unknown Shift)",
        "points": 300,
        "desc": "**Goal:** Recover a Caesar cipher's shift by observing a known-plaintext encryption.\n\nLog in as `krypton2`. `/krypton/krypton2/krypton3` is encrypted with a Caesar shift derived from `/krypton/krypton2/keyfile.dat` (not human-readable -- don't just `cat` it). Symlink the keyfile into a scratch directory, then run the `encrypt` binary next to it on a known plaintext (a long run of `A`s) to observe the shift it produces, and reverse that shift to read the next password.",
        "flag": "CAESARISEASY"
    },
    {
        "id": "krypton-03",
        "name": "Krypton 3 -> 4: Frequency Analysis",
        "points": 350,
        "desc": "**Goal:** Break a substitution cipher using letter-frequency analysis.\n\nLog in as `krypton3`. `/krypton/krypton3/krypton4` is English text under a simple substitution cipher (each letter always maps to the same other letter). Count letter frequencies and match them against typical English letter frequency to recover the substitution alphabet.\n\n*Hint: E, T, A, O, I, N are the most common letters in English.*",
        "flag": "BRUTE"
    },
    {
        "id": "krypton-04",
        "name": "Krypton 4 -> 5: Vigenere Cipher (Known Key Length)",
        "points": 400,
        "desc": "**Goal:** Break a Vigenere cipher when the key length is already known.\n\nLog in as `krypton4`. `/krypton/krypton4/krypton5` is a Vigenere cipher with a key exactly 6 letters long (see the README next to it). Split the ciphertext into 6 interleaved groups and solve each independently as its own Caesar shift.",
        "flag": "CLEARTEXT"
    },
    {
        "id": "krypton-05",
        "name": "Krypton 5 -> 6: Vigenere Cipher (Kasiski Test)",
        "points": 450,
        "desc": "**Goal:** Break a Vigenere cipher when the key length isn't given.\n\nLog in as `krypton5`. `/krypton/krypton5/krypton6` is another Vigenere cipher, but this time you don't know the key length. Use the Kasiski examination (repeating ciphertext patterns) to estimate it -- likely 3, 6, or 9 -- then apply frequency analysis per group to recover the key.",
        "flag": "RANDOM"
    },
    {
        "id": "krypton-06",
        "name": "Krypton 6 -> 7: Stream Cipher / LFSR",
        "points": 500,
        "desc": "**Goal:** Recover a repeating keystream and use it to decrypt the final password.\n\nLog in as `krypton6`. This is the final Krypton level. `/krypton/krypton6/final` is encrypted with a stream cipher whose keystream repeats every 30 characters -- the `encrypt` binary next to it implements it. Encrypt a long run of identical characters (30+ of them) to read the repeating keystream straight off the output, then use it to decrypt the final flag.",
        "flag": "LFSRISNOTRANDOM"
    }
]

# Generate folder and files relative to the repo root folder dynamically
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(script_dir, "..", "challenges"))

os.makedirs(base_dir, exist_ok=True)

for i, ch in enumerate(challenges_data):
    folder_path = os.path.join(base_dir, ch["id"])
    os.makedirs(folder_path, exist_ok=True)

    escaped_desc = ch['desc'].replace('\n', '\n  ')
    is_final_level = (i == len(challenges_data) - 1)
    yaml_content = f"""name: "{ch['name']}"
author: "CEI Labs (self-hosted recreation of OverTheWire's Krypton)"
category: "Cryptography"
description: |
  {escaped_desc}
value: {ch['points']}
type: standard
flags:
  - "{ch['flag']}"
state: visible
version: "0.1"
"""
    if i > 0:
        # Level 0 needs no SSH/instance at all -- it's a static string in
        # the description itself, so it gets no instance mapping.
        yaml_content += f"""instance_type: single-target
image: {KRYPTON_IMAGE}
instance_group: {INSTANCE_GROUP}
shutdown_on_solve: {"true" if is_final_level else "false"}
"""

    file_path = os.path.join(folder_path, "challenge.yml")
    with open(file_path, "w") as f:
        f.write(yaml_content)

print(f"Successfully generated {len(challenges_data)} Krypton challenges inside '{base_dir}'!")
