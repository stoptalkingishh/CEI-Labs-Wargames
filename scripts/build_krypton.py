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
        "id": "krypton-start-here",
        "name": "Krypton: Start Here",
        "points": 10,
        "desc": (
            "**Goal:** Learn the launch controls, then prove you used them.\n\n"
            "Levels 1-6 in Krypton (level 0 needs no environment at all) share one box, "
            "launched from a control attached to each of those challenges, right there on "
            "the challenge itself:\n"
            "- **Launch Environment** -- starts the box, or reconnects you to one already "
            "running.\n"
            "- **Reboot Host** -- restarts it in place if it gets stuck. Same connection "
            "details afterward.\n"
            "- **Relaunch Environment** -- destroys and recreates it from scratch. Use this "
            "if something's broken beyond a reboot; anything you changed inside it is lost.\n"
            "- **+5 more minutes** -- shows up only once every level in this track is solved "
            "and a shutdown countdown has started. Extends it if you're not done yet.\n\n"
            "Click Launch, wait for it to show a host and port, then connect as `krypton1` "
            "with password `KRYPTONISGREAT` (level 0's own flag) and read `welcome.txt` in "
            "the home directory. Submit its contents as your flag."
        ),
        "flag": "WELCOME_TO_KRYPTON"
    },
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
        "desc": (
            "**Goal:** The password for level 3 is in the file `krypton3`, encrypted with a Caesar cipher whose "
            "shift comes from a keyfile you can't read directly -- but you can use the `encrypt` binary next to "
            "it, which reads that keyfile every time it runs.\n\n"
            "**Commands you may need to solve this level:** `mktemp`, `ln -s`, `chmod`, `tr`\n\n"
            "**Helpful reading:** [Known-plaintext attack (Wikipedia)](https://en.wikipedia.org/wiki/Known-plaintext_attack), "
            "[Caesar cipher (Wikipedia)](https://en.wikipedia.org/wiki/Caesar_cipher)"
        ),
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

# One real, technique-specific hint per level (not krypton-start-here --
# its description is already a full walkthrough). See build_bandit.py's
# HINTS comment for the quoting constraint (no literal double-quotes).
HINTS = {
    "krypton-00": ("`base64 -d` decodes it directly -- there's no cipher here, just an encoding.", 10),
    "krypton-01": ("`tr '[:alpha:]' 'N-ZA-Mn-za-m' < /krypton/krypton1/krypton2` reverses ROT13 in one line.", 15),
    # krypton-02: SAMPLE for the new 3-tier crawl/walk/run hint format.
    # Tier 3 condensed from real writeups, e.g.
    # https://mayadevbe.me/posts/overthewire/krypton/level2/ and
    # https://medium.com/secttp/overthewire-krypton-level-2-ba52015667d6
    "krypton-02": [
        ("`man tr` -- you'll need it to apply the shift once you know it.", 15),
        ("The `encrypt` binary looks for `keyfile.dat` in your CURRENT directory, not a fixed path. Make a scratch directory, symlink the real keyfile into it, then run `encrypt` on a string you already know the plaintext of (like a long run of `A`s) -- comparing input to output tells you the exact shift.", 150),
        ("Full method: `mktemp -d` for a scratch directory, `cd` into it, then `ln -s /krypton/krypton2/keyfile.dat` so `encrypt` (which only looks in your current directory) can find it. Run `/krypton/krypton2/encrypt` against a file of your own containing many repeated `A` characters -- since every `A` shifts by the exact same amount, the output tells you precisely which letter `A` became, and that letter's position in the alphabet is the shift (e.g. if `A` becomes `M`, the shift is 12). Once you know the shift, reverse it against `krypton3` with `tr`, e.g. `tr 'A-Za-z' 'N-ZA-Mn-za-m'` for a shift of 13, adjusting the rotation to match what you actually found.", 225),
    ],
    "krypton-03": ("Count letters with something like `tr -cd 'A-Za-z' < /krypton/krypton3/krypton4 | fold -w1 | sort | uniq -c | sort -rn`, then map the most frequent letters to E, T, A, O, I, N in order.", 20),
    "krypton-04": ("Every 6th character belongs to the same Caesar shift -- extract characters at positions 0,6,12,... as one group, 1,7,13,... as the next, and so on, then solve each group's shift separately.", 25),
    "krypton-05": ("Look for repeated 3+ character substrings in the ciphertext and note the distances between their repeats -- the key length usually divides most of those distances evenly.", 25),
    "krypton-06": ("Run `/krypton/krypton6/encrypt` on 30+ identical characters (e.g. a string of `A`s) -- since the keystream repeats every 30 characters, the output directly IS the keystream, ready to XOR/subtract against the real ciphertext.", 30),
}

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
    if ch["id"] != "krypton-00":
        # Level 0 needs no SSH/instance at all -- it's a static string in
        # the description itself, so it gets no instance mapping. Every
        # other challenge, including krypton-start-here, does.
        yaml_content += f"""instance_type: single-target
image: {KRYPTON_IMAGE}
instance_group: {INSTANCE_GROUP}
shutdown_on_solve: {"true" if is_final_level else "false"}
show_launcher: {"true" if ch["id"] == "krypton-start-here" else "false"}
"""

    hint = HINTS.get(ch["id"])
    if hint:
        tiers = hint if isinstance(hint, list) else [hint]
        yaml_content += "hints:\n"
        for hint_content, hint_cost in tiers:
            yaml_content += f'  - content: "{hint_content}"\n    cost: {hint_cost}\n'

    file_path = os.path.join(folder_path, "challenge.yml")
    with open(file_path, "w") as f:
        f.write(yaml_content)

print(f"Successfully generated {len(challenges_data)} Krypton challenges inside '{base_dir}'!")
