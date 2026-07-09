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

CONNECT_NOTE = (
    "Launch your Krypton environment from this challenge (shared across "
    "all Krypton levels -- launching any one of them starts the same "
    "persistent box) and connect via SSH to the host/port CTFd shows you "
    "once it's ready."
)

# Define the dataset for Krypton Levels 0 to 6 based on OTW specifications
challenges_data = [
    {
        "id": "krypton-00",
        "name": "Krypton 0 -> 1: Base64 Decoding",
        "points": 200,
        "desc": "**Goal:** Decrypt the first password using Base64 decoding.\n\nWelcome to Krypton! The first level is easy and needs no SSH connection at all. The following string encodes the password for level 1 using Base64:\n\n`S1JZUFRPTklTR1JFQVQ=`\n\nUse a Base64 decoder (like the `base64 -d` command) to find the flag.",
        "flag": "KRYPTONISGREAT"
    },
    {
        "id": "krypton-01",
        "name": "Krypton 1 -> 2: ROT13 Substitution Cipher",
        "points": 250,
        "desc": f"{CONNECT_NOTE} Log in as `krypton1` using the flag from the previous level as your password.\n\nThe password for level 2 is located in `/krypton/krypton1/krypton2`. It is encrypted with a simple ROT13 rotation cipher.\n\n*Hint: The `tr` command is very useful for translating characters (e.g., `tr \"[:alpha:]\" \"N-ZA-Mn-za-m\"`).*",
        "flag": "ROTTEN"
    },
    {
        "id": "krypton-02",
        "name": "Krypton 2 -> 3: Caesar Cipher (Unknown Shift)",
        "points": 300,
        "desc": f"{CONNECT_NOTE} Log in as `krypton2` using the flag from the previous level as your password.\n\nThe password for level 3 is in `/krypton/krypton2/krypton3`, encrypted with a Caesar cipher whose shift is derived from `/krypton/krypton2/keyfile.dat` (not human-readable -- don't just `cat` it). Symlink the keyfile into a scratch directory and use the `encrypt` binary next to it on a known plaintext (a long string of 'A's) to observe the shift, then reverse it to read the next password.",
        "flag": "CAESARISEASY"
    },
    {
        "id": "krypton-03",
        "name": "Krypton 3 -> 4: Frequency Analysis",
        "points": 350,
        "desc": f"{CONNECT_NOTE} Log in as `krypton3` using the flag from the previous level as your password.\n\n`/krypton/krypton3/krypton4` is intercepted English text encrypted with a simple substitution cipher (each letter always maps to the same other letter). Count the frequency of the letters to determine the substitution alphabet.\n\n*Hint: E, T, A, O, I, N are the most common letters in the English language.*",
        "flag": "BRUTE"
    },
    {
        "id": "krypton-04",
        "name": "Krypton 4 -> 5: Vigenère Cipher (Known Key Length)",
        "points": 400,
        "desc": f"{CONNECT_NOTE} Log in as `krypton4` using the flag from the previous level as your password.\n\n`/krypton/krypton4/krypton5` is a Vigenère cipher with a key exactly 6 letters long (see the README next to it). Split the ciphertext into 6 interleaved groups and solve each as its own Caesar shift to recover the password.",
        "flag": "CLEARTEXT"
    },
    {
        "id": "krypton-05",
        "name": "Krypton 5 -> 6: Vigenère Cipher (Kasiski Test)",
        "points": 450,
        "desc": f"{CONNECT_NOTE} Log in as `krypton5` using the flag from the previous level as your password.\n\n`/krypton/krypton5/krypton6` is a Vigenère cipher, but this time the key length isn't given. Use the Kasiski examination method to find repeating patterns in the ciphertext and estimate the key length (likely 3, 6, or 9). Once the length is known, apply frequency analysis to recover the key.",
        "flag": "RANDOM"
    },
    {
        "id": "krypton-06",
        "name": "Krypton 6 -> 7: Stream Cipher / LFSR",
        "points": 500,
        "desc": f"{CONNECT_NOTE} Log in as `krypton6` using the flag from the previous level as your password.\n\nThis is the final Krypton level. `/krypton/krypton6/final` is encrypted with a stream cipher whose keystream repeats every 30 characters -- the `encrypt` binary next to it implements it. Encrypt a long run of identical letters (e.g. 30+ 'A's) to read the repeating keystream directly off the output, then use it to decrypt the final flag.",
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
