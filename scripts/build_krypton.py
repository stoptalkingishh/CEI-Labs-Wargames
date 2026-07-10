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
        "desc": "**Goal:** Reverse a ROT13 rotation cipher.\n\nLog in as `krypton1`. The next password is in `/krypton/krypton1/krypton2`, encrypted with a simple ROT13 rotation.",
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

# Crawl/walk/run hints per level (not krypton-start-here -- its
# description is already a full walkthrough). See build_bandit.py's
# HINTS comment for the tier structure and the quoting constraint (no
# literal double-quotes -- this script builds YAML by hand). Krypton is
# concept-heavy, so tier 1 is often a reading link rather than a bare
# command, matching each description's own "Helpful reading" section.
HINTS = {
    "krypton-00": [
        ("`man base64`.", 10),
        ("Base64 turns arbitrary bytes into a fixed set of readable characters (letters, digits, `+`, `/`, `=` padding). Recognizing that character set -- including the trailing `=` padding -- is the tell that it's Base64, not an actual cipher, and Base64's own tooling has a documented decode flag.", 100),
        ("`echo 'S1JZUFRPTklTR1JFQVQ=' | base64 -d` decodes the string straight back to the plaintext password -- no key, shift, or other secret involved.", 150),
    ],
    "krypton-01": [
        ("[ROT13 on Wikipedia](https://en.wikipedia.org/wiki/ROT13).", 15),
        ("ROT13 shifts every letter 13 positions through the alphabet, wrapping at the end. Since the alphabet has 26 letters, shifting by 13 twice returns you to the start -- meaning the SAME transformation both encrypts and decrypts. `tr` can perform an arbitrary letter-for-letter substitution given two character ranges.", 125),
        ("Log in as `krypton1`, then `tr '[:alpha:]' 'N-ZA-Mn-za-m' < /krypton/krypton1/krypton2` maps every letter 13 positions ahead (wrapping past Z to A) -- applying this once to the ciphertext reverses the ROT13 and reveals the password.", 187),
    ],
    "krypton-02": [
        ("[Known-plaintext attack on Wikipedia](https://en.wikipedia.org/wiki/Known-plaintext_attack).", 15),
        ("The `encrypt` binary looks for `keyfile.dat` in your CURRENT directory, not a fixed path, and will encrypt any plaintext you give it using that key. If you feed it text whose plaintext you already know, comparing your known input against its output reveals exactly what the cipher did to it.", 150),
        ("`mktemp -d` for a scratch directory, `cd` into it, then `ln -s /krypton/krypton2/keyfile.dat` so `encrypt` (which only looks in your current directory) can find it. Run `/krypton/krypton2/encrypt` against a file of your own containing many repeated `A` characters -- since every `A` shifts by the exact same amount, the output tells you precisely which letter `A` became, and that letter's position in the alphabet is the shift (e.g. if `A` becomes `M`, the shift is 12). Once you know the shift, reverse it against `krypton3` with `tr`, e.g. `tr 'A-Za-z' 'N-ZA-Mn-za-m'` for a shift of 13, adjusting the rotation to match what you actually found.", 225),
    ],
    "krypton-03": [
        ("[Frequency analysis on Wikipedia](https://en.wikipedia.org/wiki/Frequency_analysis).", 20),
        ("In normal English text, letters don't appear equally often -- E, T, A, O, I, N are consistently the most common. If a substitution cipher always maps the same plaintext letter to the same ciphertext letter, counting ciphertext letter frequencies and matching the ranking against known English frequency order recovers the substitution alphabet, one letter at a time. The extra intercepted files (`found1`, `found2`, `found3`) were encrypted with the SAME key, so combining them gives more data for the same statistics.", 175),
        ("Combine the ciphertext with the extra intercepted files and count letter frequency: `cat /krypton/krypton3/found1 /krypton/krypton3/found2 /krypton/krypton3/found3 /krypton/krypton3/krypton4 | tr -cd 'A-Za-z' | tr 'a-z' 'A-Z' | fold -w1 | sort | uniq -c | sort -rn`. Map the most frequent output letter to E, next to T, and so on down the standard English frequency order (E T A O I N ...), then apply that substitution with `tr` against `krypton4` to reveal the password. Some letters may need manual correction/guessing once partial words start appearing.", 262),
    ],
    "krypton-04": [
        ("[Vigenere cipher on Wikipedia](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher).", 20),
        ("A Vigenere cipher with a 6-letter key actually applies 6 DIFFERENT Caesar shifts in rotation -- character 1 uses shift A, character 2 uses shift B, ..., character 7 goes back to shift A, and so on. Pulling out every 6th character starting from each of the 6 starting positions produces 6 groups, each encrypted with just ONE consistent shift -- solvable the same way as a normal Caesar cipher.", 200),
        ("Split the ciphertext into 6 interleaved groups (characters at positions 0, 6, 12, ... form group 1; positions 1, 7, 13, ... form group 2; and so on). Run frequency analysis (same technique as the previous level) on EACH group independently to find its own Caesar shift, then reassemble the 6 recovered shifts back into their original character positions to read the full plaintext password.", 300),
    ],
    "krypton-05": [
        ("[Kasiski examination on Wikipedia](https://en.wikipedia.org/wiki/Kasiski_examination).", 20),
        ("Look for repeated 3+ character substrings appearing more than once in the ciphertext, and note the DISTANCE (in characters) between each repeat. The true key length usually divides most of these distances evenly, since a repeated plaintext fragment only produces identical ciphertext when it lines up with the same position in the repeating key.", 200),
        ("Search the ciphertext for repeated 3-4 character sequences and record the distance between each occurrence; find the greatest common factor across those distances (in this deployment, that points to a key length of 9). Once the key length is known, split into that many interleaved groups exactly as in the previous level, solve each group's Caesar shift via frequency analysis, and reassemble.", 300),
    ],
    "krypton-06": [
        ("`man xxd`.", 25),
        ("The stream cipher combines each plaintext byte with a 'random' keystream byte -- but that keystream turns out to repeat every 30 characters. If you can get the encryption binary to encrypt a LONG run of identical known characters, the relationship between your known input and its output at each position directly reveals the repeating keystream itself, byte for byte.", 225),
        ("Run `/krypton/krypton6/encrypt` on an input of 30+ repeated identical characters (e.g. a long run of `A`s) -- since every plaintext byte is the same known value, the corresponding output bytes reveal the raw keystream directly (compare your known plaintext byte against each output byte, matching whatever operation the cipher uses). Once you have the 30-byte repeating keystream, apply the same relationship between it and `/krypton/krypton6/final` (cycling the keystream every 30 bytes) to recover the final plaintext password.", 337),
    ],
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
