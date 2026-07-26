import os
import json

from hint_economy import managed_tiers

# Self-hosted image reference (see docs/self-hosted-wargames-blueprint.md
# Phase 3's "Wire Krypton into CTFd" task). Not yet published by a CI
# workflow -- until it is, build+tag locally with this exact name/tag
# before deploying (`docker build -t ghcr.io/stoptalkingishh/cei-labs-
# wargames/krypton-target:latest targets/krypton`) so `docker stack
# deploy` can find it.
KRYPTON_IMAGE = os.environ.get(
    "KRYPTON_IMAGE",
    "ghcr.io/stoptalkingishh/cei-labs-wargames/krypton-target:latest",
)


def _flags_yaml(flag) -> str:
    """A challenge's `flag` field is either a plain string (the historical
    shorthand -- ctfcli treats it as a static, case-sensitive flag) or a
    dict (per_team_dynamic and any future non-static type) -- ctfcli's
    _create_flags() POSTs a non-string entry to /api/v1/flags verbatim, so
    the dict's keys must already match that API's real fields
    (type/content/data)."""
    if isinstance(flag, dict):
        lines = [f"  - type: {flag['type']}\n"]
        lines.append(f"    content: \"{flag['content']}\"\n")
        if "data" in flag:
            lines.append(f"    data: \"{flag['data']}\"\n")
        return "".join(lines)
    return f'  - "{flag}"\n'

# All 7 challenges share ONE instance_group -- same "one box, many
# levels" design as Bandit. Only the final level opts into
# shutdown_on_solve.
INSTANCE_GROUP = "krypton"

# A player's connection details (host/port, live status) come from the
# "Launch Environment" control on this challenge itself -- injected into
# the challenge view by cei-labs-engine's instance-launcher plugin, not
# written into these descriptions, since the port is only known once an
# instance actually exists. See the "Krypton: Start Here" challenge for
# how that control works. All levels 0-6 connect as a Linux user named
# after the level (`krypton0`, `krypton1`, ...) using the previous level's
# flag as that account's password -- except `krypton0` itself, which has
# no previous level to chain from and uses a fixed, publicly-known
# password instead (`krypton0`, matching Bandit's own `bandit0` front
# door; see targets/krypton/build/02-set-passwords.sh).

# Shown once, in krypton-start-here only -- identical wording to Bandit's
# own SSH_CONNECT_GUIDE (scripts/build_bandit.py) since it's the same
# underlying connection mechanism for both tracks, just duplicated rather
# than imported since neither build script otherwise depends on the
# other. Every app name here is plain text, deliberately not a clickable
# link -- see build_bandit.py's SSH_CONNECT_GUIDE comment for why.
SSH_CONNECT_GUIDE = (
    "**Connecting via SSH:** Once launched, the panel below shows a Host and Port. "
    "Every level in this track connects the same way: `ssh <username>@<host> -p <port>`, "
    "then enter the password when prompted. How you run that command depends on your "
    "own device -- most players will be on Windows, which is covered below, but every "
    "common platform works:\n"
    "- **Windows 10/11:** Open PowerShell (search for it in the Start menu) -- `ssh` is "
    "already built in, no install needed.\n"
    "- **macOS:** Open Terminal (Spotlight search -> \"Terminal\") -- `ssh` is already "
    "built in.\n"
    "- **Linux:** Open your terminal emulator of choice -- `ssh` is already built in on "
    "virtually every distribution.\n"
    "- **iOS (iPhone/iPad):** No built-in terminal. Install a free SSH client app first, "
    "e.g. Termius, from the App Store.\n"
    "- **Android:** No built-in terminal either. Install a free SSH client app first, "
    "e.g. Termius or Termux, from the Play Store."
)

# Define the dataset for Krypton Levels 0 to 6 based on OverTheWire specifications
challenges_data = [
    {
        "id": "krypton-start-here",
        "name": "Krypton: Start Here",
        "points": 10,
        "desc": (
            "**Goal:** Learn the launch controls, then prove you used them.\n\n"
            "Levels 0-6 in Krypton share one box, launched from a control attached to each "
            "of those challenges, right there on the challenge itself:\n"
            "- **Launch Environment** -- starts the box, or reconnects you to one already "
            "running.\n"
            "- **Reboot Host** -- restarts it in place if it gets stuck. Same connection "
            "details afterward.\n"
            "- **Relaunch Environment** -- destroys and recreates it from scratch. Use this "
            "if something's broken beyond a reboot; anything you changed inside it is lost.\n"
            "- **+5 more minutes** -- shows up only once every level in this track is solved "
            "and a shutdown countdown has started. Extends it if you're not done yet.\n\n"
            + SSH_CONNECT_GUIDE +
            "\n\nClick Launch, wait for it to show a Host and Port, then connect as `krypton0` "
            "with password `krypton0` (the fixed, publicly-known entry password for Krypton "
            "-- same idea as Bandit's own `bandit0`/`bandit0`). The moment you log in, a "
            "banner prints automatically -- no file to go read, it's already on your screen. "
            "Its last three lines are an acceptable-use notice; the middle one is about not "
            "using AI or outside tools/services to cheat. Copy that exact line, word for "
            "word (punctuation included), and submit it as your flag -- proof you actually "
            "read it, not just that you connected."
        ),
        "flag": "Do not use AI or external tools/services to cheat or obtain answers."
    },
    {
        "id": "krypton-00",
        "name": "Krypton 0 -> 1: Base64 Decoding",
        "points": 200,
        "desc": (
            "**Goal:** Decode a Base64-encoded password.\n\n"
            "Click Launch, wait for it to show a host and port, then connect as `krypton0` "
            "with password `krypton0` (the fixed, publicly-known entry password for Krypton "
            "-- same idea as Bandit's own `bandit0`/`bandit0`). Your home directory contains "
            "`encoded.txt`, a Base64-encoded string. Decode it to find the password for "
            "krypton1."
        ),
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "krypton0"}
    },
    {
        "id": "krypton-01",
        "name": "Krypton 1 -> 2: ROT13 Substitution Cipher",
        "points": 250,
        "desc": "**Goal:** Reverse a ROT13 rotation cipher.\n\nThe next password is in `/home/krypton1/krypton2`, encrypted with a simple ROT13 rotation.",
        "flag": {"type": "per_team_dynamic_alpha", "content": "per-team-dynamic (placeholder, not read)", "data": "krypton1"}
    },
    {
        "id": "krypton-02",
        "name": "Krypton 2 -> 3: Caesar Cipher (Unknown Shift)",
        "points": 300,
        "desc": (
            "**Goal:** The password for level 3 is in the file `krypton3`, encrypted with a Caesar cipher whose "
            "shift comes from a keyfile you can't read directly -- but you can use the `encrypt` binary next to "
            "it, which reads that keyfile every time it runs."
        ),
        # Per-team dynamic flag: the orchestrator generates a fresh random
        # value per team at instance-creation time (env key "krypton2"),
        # and cei-labs-engine's routes.py persists it for CTFd to validate
        # against -- no longer an identical hardcoded string every team
        # gets (see docs/security-audit-status.md). See ctfcli's
        # _create_flags(): a non-string flags[] entry is POSTed to
        # /api/v1/flags verbatim, so {"type": ..., "content": ..., "data":
        # ...} becomes that Flags row directly.
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "krypton2"}
    },
    {
        "id": "krypton-03",
        "name": "Krypton 3 -> 4: Frequency Analysis",
        "points": 350,
        "desc": "**Goal:** Break a substitution cipher using letter-frequency analysis.\n\n`/home/krypton3/krypton4` is English text under a simple substitution cipher (each letter always maps to the same other letter). Count letter frequencies and match them against typical English letter frequency to recover the substitution alphabet.\n\n*Hint: E, T, A, O, I, N are the most common letters in English.*",
        "flag": {"type": "per_team_dynamic_alpha", "content": "per-team-dynamic (placeholder, not read)", "data": "krypton3"}
    },
    {
        "id": "krypton-04",
        "name": "Krypton 4 -> 5: Vigenere Cipher (Known Key Length)",
        "points": 400,
        "desc": "**Goal:** Break a Vigenere cipher when the key length is already known.\n\n`/home/krypton4/krypton5` is a Vigenere cipher with a key exactly 6 letters long (see the README next to it). Split the ciphertext into 6 interleaved groups and solve each independently as its own Caesar shift.",
        "flag": {"type": "per_team_dynamic_alpha", "content": "per-team-dynamic (placeholder, not read)", "data": "krypton4"}
    },
    {
        "id": "krypton-05",
        "name": "Krypton 5 -> 6: Vigenere Cipher (Kasiski Test)",
        "points": 450,
        "desc": "**Goal:** Break a Vigenere cipher when the key length isn't given.\n\n`/home/krypton5/krypton6` is another Vigenere cipher, but this time you don't know the key length. Use the Kasiski examination (repeating ciphertext patterns) to estimate it -- likely 3, 6, or 9 -- then apply frequency analysis per group to recover the key.",
        "flag": {"type": "per_team_dynamic_alpha", "content": "per-team-dynamic (placeholder, not read)", "data": "krypton5"}
    },
    {
        "id": "krypton-06",
        "name": "Krypton 6 -> 7: Stream Cipher / LFSR",
        "points": 500,
        "desc": "**Goal:** Recover a repeating keystream and use it to decrypt the final password.\n\nThis is the final Krypton level. `/home/krypton6/final` is encrypted with a stream cipher whose keystream repeats every 30 characters -- the `encrypt` binary next to it implements it. Encrypt a long run of identical characters (30+ of them) to read the repeating keystream straight off the output, then use it to decrypt the final flag.",
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "krypton6"}
    }
]

# "Commands you may need" + "Helpful reading" shown directly in the
# description, free -- matching OverTheWire's own real page structure
# (see build_bandit.py's EXTRA_INFO comment for the full rationale).
EXTRA_INFO = {
    "krypton-00": (["base64"], []),
    "krypton-01": (["tr"], [("ROT13 on Wikipedia", "https://en.wikipedia.org/wiki/ROT13")]),
    "krypton-02": (["mktemp", "ln", "chmod", "tr"], [("Known-plaintext attack on Wikipedia", "https://en.wikipedia.org/wiki/Known-plaintext_attack"), ("Caesar cipher on Wikipedia", "https://en.wikipedia.org/wiki/Caesar_cipher")]),
    "krypton-03": (["tr", "sort", "uniq", "fold"], [("Frequency analysis on Wikipedia", "https://en.wikipedia.org/wiki/Frequency_analysis")]),
    "krypton-04": (["tr"], [("Vigenere cipher on Wikipedia", "https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher")]),
    "krypton-05": (["tr"], [("Kasiski examination on Wikipedia", "https://en.wikipedia.org/wiki/Kasiski_examination")]),
    "krypton-06": (["xxd"], [("Stream cipher on Wikipedia", "https://en.wikipedia.org/wiki/Stream_cipher")]),
}

# Crawl/walk/run hints per level (not krypton-start-here -- its
# description is already a full walkthrough). See build_bandit.py's
# HINTS comment for the tier structure and the quoting constraint (no
# literal double-quotes -- this script builds YAML by hand). Krypton is
# concept-heavy, so tier 1 is often a reading link rather than a bare
# command, matching each description's own "Helpful reading" section.
HINTS = {
    'krypton-00': [
        'Log in as `krypton0` with password `krypton0` (the fixed, publicly-known entry password), then run `base64 --help` on the Krypton target.',
        "Your home directory has a file called `encoded.txt`. Base64 turns arbitrary bytes into a fixed set of readable characters (letters, digits, `+`, `/`, `=` padding). Recognizing that character set -- including the trailing `=` padding -- is the tell that it's Base64, not an actual cipher, and Base64's own tooling has a documented decode flag.",
        "`base64 -d ~/encoded.txt` (or `cat ~/encoded.txt | base64 -d`) decodes the file straight back to the plaintext password for krypton1 -- no key, shift, or other secret involved.\n\nIllustrative example only -- your real value will differ:\n```\nkrypton0@krypton:~$ cat encoded.txt\nUzFKWlVGUlBUa2xUUjFKRlFWUT0=\nkrypton0@krypton:~$ base64 -d ~/encoded.txt\n<the next password>\n```",
    ],
    'krypton-01': [
        'ROT13 on Wikipedia.',
        'ROT13 shifts every letter 13 positions through the alphabet, wrapping at the end. Since the alphabet has 26 letters, shifting by 13 twice returns you to the start -- meaning the SAME transformation both encrypts and decrypts. `tr` can perform an arbitrary letter-for-letter substitution given two character ranges.',
        "Log in as `krypton1`, then `tr '[:alpha:]' 'N-ZA-Mn-za-m' < /home/krypton1/krypton2` maps every letter 13 positions ahead (wrapping past Z to A) -- applying this once to the ciphertext reverses the ROT13 and reveals the password.\n\nIllustrative example only -- your real value will differ:\n```\nkrypton1@krypton:~$ cat /home/krypton1/krypton2\nGBAXUZAIMI\nkrypton1@krypton:~$ tr '[:alpha:]' 'N-ZA-Mn-za-m' < /home/krypton1/krypton2\n<the next password>\n```",
    ],
    'krypton-02': [
        'Known-plaintext attack on Wikipedia.',
        'The `encrypt` binary looks for `keyfile.dat` in your CURRENT directory, not a fixed path, and will encrypt any plaintext you give it using that key. If you feed it text whose plaintext you already know, comparing your known input against its output reveals exactly what the cipher did to it.',
        "`mktemp -d` for a scratch directory, `cd` into it, then `ln -s /home/krypton2/keyfile.dat` so `encrypt` (which only looks in your current directory) can find it. Run `/home/krypton2/encrypt` against a file of your own containing many repeated `A` characters -- since every `A` shifts by the exact same amount, the output tells you precisely which letter `A` became, and that letter's position in the alphabet is the shift (e.g. if `A` becomes `M`, the shift is 12). Once you know the shift, reverse it against `krypton3` with `tr`, e.g. `tr 'A-Za-z' 'N-ZA-Mn-za-m'` for a shift of 13, adjusting the rotation to match what you actually found.\n\nIllustrative example only -- your real shift/value will differ:\n```\n$ cd $(mktemp -d)\n$ ln -s /home/krypton2/keyfile.dat\n$ echo AAAAAAAAAA > probe.txt\n$ /home/krypton2/encrypt probe.txt\nMMMMMMMMMM\n$ tr 'A-Za-z' 'N-ZA-Mn-za-m' < /home/krypton2/krypton3\n<the next password>\n```",
    ],
    'krypton-03': [
        'Frequency analysis on Wikipedia.',
        "In normal English text, letters don't appear equally often -- E, T, A, O, I, N are consistently the most common. If a substitution cipher always maps the same plaintext letter to the same ciphertext letter, counting ciphertext letter frequencies and matching the ranking against known English frequency order recovers the substitution alphabet, one letter at a time. The extra intercepted files (`found1`, `found2`, `found3`) were encrypted with the SAME key, so combining them gives more data for the same statistics.",
        "Combine the ciphertext with the extra intercepted files and count letter frequency: `cat /home/krypton3/found1 /home/krypton3/found2 /home/krypton3/found3 /home/krypton3/krypton4 | tr -cd 'A-Za-z' | tr 'a-z' 'A-Z' | fold -w1 | sort | uniq -c | sort -rn`. Map the most frequent output letter to E, next to T, and so on down the standard English frequency order (E T A O I N ...), then apply that substitution with `tr` against `krypton4` to reveal the password. Some letters may need manual correction/guessing once partial words start appearing.\n\nIllustrative example only -- your real ranking/value will differ:\n```\n$ cat ...krypton3/found1 ...found2 ...found3 ...krypton4 | tr -cd 'A-Za-z' | tr 'a-z' 'A-Z' | fold -w1 | sort | uniq -c | sort -rn\n 812 Q\n 601 X\n ...\n$ tr 'QXVJ...' 'ETAO...' < /home/krypton3/krypton4\n<the next password, possibly needing manual touch-ups>\n```",
    ],
    'krypton-04': [
        'Vigenere cipher on Wikipedia.',
        'A Vigenere cipher with a 6-letter key actually applies 6 DIFFERENT Caesar shifts in rotation -- character 1 uses shift A, character 2 uses shift B, ..., character 7 goes back to shift A, and so on. Pulling out every 6th character starting from each of the 6 starting positions produces 6 groups, each encrypted with just ONE consistent shift -- solvable the same way as a normal Caesar cipher.',
        "Split the ciphertext into 6 interleaved groups (characters at positions 0, 6, 12, ... form group 1; positions 1, 7, 13, ... form group 2; and so on). Run frequency analysis (same technique as the previous level) on EACH group independently to find its own Caesar shift, then reassemble the 6 recovered shifts back into their original character positions to read the full plaintext password.\n\nIllustrative example only (a small Python-style sketch of the grouping step, not the full solve):\n```\nciphertext = open('krypton5').read().strip()\ngroups = ['' for _ in range(6)]\nfor i, c in enumerate(ciphertext):\n    groups[i % 6] += c\n# frequency-analyze each of the 6 groups independently, then reassemble\n```",
    ],
    'krypton-05': [
        'Kasiski examination on Wikipedia.',
        'Look for repeated 3+ character substrings appearing more than once in the ciphertext, and note the DISTANCE (in characters) between each repeat. The true key length usually divides most of these distances evenly, since a repeated plaintext fragment only produces identical ciphertext when it lines up with the same position in the repeating key.',
        "Search the ciphertext for repeated 3-4 character sequences and record the distance between each occurrence; find the greatest common factor across those distances (in this deployment, that points to a key length of 9). Once the key length is known, split into that many interleaved groups exactly as in the previous level, solve each group's Caesar shift via frequency analysis, and reassemble.\n\nIllustrative example only -- your real distances/value will differ:\n```\nrepeated substring 'QXR' found at positions 12 and 93 -- distance 81\nrepeated substring 'MZP' found at positions 40 and 121 -- distance 81\ngcd(81, 81, ...) = 9  -- key length is likely 9\n```",
    ],
    'krypton-06': [
        'Run `xxd --help` on the Krypton target.',
        "The stream cipher combines each plaintext byte with a 'random' keystream byte -- but that keystream turns out to repeat every 30 characters. If you can get the encryption binary to encrypt a LONG run of identical known characters, the relationship between your known input and its output at each position directly reveals the repeating keystream itself, byte for byte.",
        'Run `/home/krypton6/encrypt` on an input of 30+ repeated identical characters (e.g. a long run of `A`s) -- since every plaintext byte is the same known value, the corresponding output bytes reveal the raw keystream directly (compare your known plaintext byte against each output byte, matching whatever operation the cipher uses). Once you have the 30-byte repeating keystream, apply the same relationship between it and `/home/krypton6/final` (cycling the keystream every 30 bytes) to recover the final plaintext password.\n\nIllustrative example only -- your real keystream/value will differ:\n```\n$ yes A | head -c 40 | /home/krypton6/encrypt | xxd\n00000000: 4f2a 9c11 ...  O*..\n<derive the 30-byte repeating keystream from this, then apply it to final>\n```',
    ],
}


def _progression_note(challenge_id: str) -> str:
    """Return the common, current-instance account-transition instruction.
    Mirrors build_bandit.py's _progression_note -- see that function's
    docstring/comment for the full rationale. Krypton's account chain now
    runs the full 0-6 range, same shape as Bandit's: `krypton-00` used to
    be a pure Base64 decode with no environment/account of its own (see
    build/01-create-users.sh's history and cei-labs-event#17), but it now
    has a real `krypton0` account like every other level, so it falls
    through to the same generic progression note the other non-final
    levels use -- no more special-casing needed here."""
    if challenge_id == "krypton-start-here":
        return (
            "\n\n**Next challenge:** After submitting this flag, begin Krypton 0 -> 1: "
            "Base64 Decoding. Connect as `krypton0` (password `krypton0`, the fixed "
            "public entry password) and decode the Base64 string in your home "
            "directory to find the password for `krypton1`."
        )

    level = int(challenge_id.rsplit("-", 1)[1])

    if level == 6:
        return (
            "\n\n**Finish:** You are working as `krypton6`. Submit the recovered "
            "password here to complete the Krypton track; no further account switch is required."
        )

    return (
        f"\n\n**Account progression:** You are working as `krypton{level}`. After "
        "recovering and submitting this password, exit and reconnect to the current "
        f"host and port shown by the launch panel as `krypton{level + 1}`, using the "
        "recovered password, before starting the next level."
    )


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _render_description(challenge: dict) -> str:
    full_desc = challenge["desc"]
    extra_info = EXTRA_INFO.get(challenge["id"])
    if extra_info:
        cmds, reading = extra_info
        if cmds:
            cmd_list = ", ".join(f"`{command}`" for command in cmds)
            full_desc += f"\n\n**Commands you may need to solve this level:** {cmd_list}"
        if reading:
            # No live links: the venue network runs with no internet access
            # (see docs/offline-dependency-audit.md and
            # cei-labs-event#8/live-hint-links-offline-gap), so these are
            # rendered as plain reference titles rather than clickable
            # [title](url) markdown links, which would be dead at the venue.
            links = "\n".join(f"- {title}" for title, url in reading)
            full_desc += f"\n\n**Helpful reading:**\n{links}"
    return full_desc + _progression_note(challenge["id"])


def _validate_krypton_content() -> None:
    """Keep help guidance and account transitions aligned with this curriculum.
    In particular, this guarantees every level 0-6 states which account
    it's working as and which account to switch to next -- generated
    here instead of hand-typed per description, so a gap like krypton-02
    previously shipping with no login instruction at all can't recur."""
    hint_text = "\n".join(content for tiers in HINTS.values() for content in tiers)
    _require("man " not in hint_text, "Krypton hints must use image-supported built-in help")

    challenge_ids = {challenge["id"] for challenge in challenges_data}
    _require("krypton-start-here" in challenge_ids, "missing krypton-start-here")
    start_note = _progression_note("krypton-start-here")
    _require("krypton1" in start_note, "krypton-start-here omits the next account")
    start_rendered = _render_description(next(challenge for challenge in challenges_data if challenge["id"] == "krypton-start-here"))
    _require(start_rendered.count(start_note) == 1, "krypton-start-here does not append progression exactly once")

    for level in range(7):
        challenge_id = f"krypton-{level:02d}"
        _require(challenge_id in challenge_ids, f"missing {challenge_id}")
        note = _progression_note(challenge_id)
        if level == 6:
            _require("`krypton6`" in note, f"{challenge_id} omits its current account")
            _require("no further account switch is required" in note, f"{challenge_id} omits completion guidance")
        else:
            _require(f"`krypton{level}`" in note, f"{challenge_id} omits its current account")
            _require(f"`krypton{level + 1}`" in note, f"{challenge_id} omits its next account")
        if level != 6:
            _require("launch panel" in note, f"{challenge_id} omits launch-panel access")
        rendered = _render_description(next(challenge for challenge in challenges_data if challenge["id"] == challenge_id))
        _require(rendered.count(note) == 1, f"{challenge_id} does not append progression exactly once")


_validate_krypton_content()

# Generate folder and files relative to the repo root folder dynamically
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(script_dir, "..", "challenges"))

os.makedirs(base_dir, exist_ok=True)

assert "man " not in "\n".join(tiers[0] for tiers in HINTS.values() if tiers)
for i, ch in enumerate(challenges_data):
    folder_path = os.path.join(base_dir, ch["id"])
    os.makedirs(folder_path, exist_ok=True)

    full_desc = _render_description(ch)

    escaped_desc = full_desc.replace('\n', '\n  ')
    is_final_level = (i == len(challenges_data) - 1)
    yaml_content = f"""name: "{ch['name']}"
author: "CEI Labs (self-hosted recreation of OverTheWire's Krypton)"
category: "Cryptography"
description: |
  {escaped_desc}
value: {ch['points']}
type: standard
flags:
{_flags_yaml(ch['flag'])}state: visible
version: "0.1"
"""
    # Every Krypton challenge, including krypton-00 and krypton-start-here,
    # gets an instance mapping -- krypton-00 used to be excluded (its
    # puzzle was a static string in the description itself, no login
    # needed), but now that it has a real krypton0 account on the same
    # shared box as every other level, it needs the mapping too.
    yaml_content += f"""instance_type: single-target
image: {KRYPTON_IMAGE}
instance_group: {INSTANCE_GROUP}
shutdown_on_solve: {"true" if is_final_level else "false"}
show_launcher: {"true" if ch["id"] == "krypton-start-here" else "false"}
"""

    # Managed by the plugin manifest, never CTFd native hints.

    file_path = os.path.join(folder_path, "challenge.yml")
    with open(file_path, "w") as f:
        f.write(yaml_content)

print(f"Successfully generated {len(challenges_data)} Krypton challenges inside '{base_dir}'!")
with open(os.path.join(base_dir, "krypton-hint-wallet.json"), "w", encoding="utf-8") as manifest:
    json.dump({"schema_version": 1, "track": "krypton", "entries": [{"name": c["name"], "tiers": [{"tier": n, "cost": cost, "content": text} for n, (text, cost) in enumerate(managed_tiers(c["points"], HINTS[c["id"]]), 1)]} for c in challenges_data if c["id"] in HINTS]}, manifest)
