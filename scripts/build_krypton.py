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

# Shown once, in krypton-start-here only, under its own
# "### Connecting from your device" heading -- same body wording as
# Bandit's own SSH_CONNECT_GUIDE (scripts/build_bandit.py) since it's the
# same underlying connection mechanism for both tracks, just duplicated
# rather than imported since neither build script otherwise depends on the
# other. Bandit still inlines a "**Connecting via SSH:**" bold lead-in;
# Krypton drops it because the section heading now carries that label.
# Every app name here is plain text, deliberately not a clickable
# link -- see build_bandit.py's SSH_CONNECT_GUIDE comment for why.
SSH_CONNECT_GUIDE = (
    "Once launched, the panel below shows a Host and Port. "
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
        # Custom multi-section body (no "### The task" / EXTRA_INFO) --
        # _render_description splices this in between the "## Goal"
        # header and the "### Up next" progression note.
        "goal": "Learn the launch controls, then prove you used them.",
        "body": (
            "### The launch controls\n"
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
            "### Connecting from your device\n"
            + SSH_CONNECT_GUIDE +
            "\n\n### Prove you connected\n"
            "Click Launch, wait for it to show a Host and Port, then connect as `krypton0` "
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
        "goal": "Decode a Base64-encoded password.",
        "task": (
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
        "goal": "Reverse a ROT13 rotation cipher.",
        "task": "The next password is in `/home/krypton1/krypton2`, encrypted with a simple ROT13 rotation.",
        "flag": {"type": "per_team_dynamic_alpha", "content": "per-team-dynamic (placeholder, not read)", "data": "krypton1"}
    },
    {
        "id": "krypton-02",
        "name": "Krypton 2 -> 3: Caesar Cipher (Unknown Shift)",
        "points": 300,
        # The whole brief is the goal here -- there is no separate task
        # paragraph, so "### The task" is followed directly by the
        # commands/reading lines.
        "goal": (
            "The password for level 3 is in the file `krypton3`, encrypted with a Caesar cipher whose "
            "shift comes from a keyfile you can't read directly -- but you can use the `encrypt` binary next to "
            "it, which reads that keyfile every time it runs."
        ),
        "task": "",
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
        "goal": "Break a substitution cipher using letter-frequency analysis.",
        "task": "`/home/krypton3/krypton4` is English text under a simple substitution cipher (each letter always maps to the same other letter). The `found1`, `found2`, and `found3` samples use the same alphabet. Combine them, count letter frequencies, and use word patterns to refine the mapping.\n\n*Hint: E, T, A, O, I, N are the most common letters in English.*",
        "flag": {"type": "per_team_dynamic_alpha", "content": "per-team-dynamic (placeholder, not read)", "data": "krypton3"}
    },
    {
        "id": "krypton-04",
        "name": "Krypton 4 -> 5: Vigenere Cipher (Known Key Length)",
        "points": 400,
        "goal": "Break a Vigenere cipher when the key length is already known.",
        "task": "`/home/krypton4/krypton5` is a Vigenere cipher with a key exactly 6 letters long (see the README next to it). Split the ciphertext LETTERS into 6 interleaved groups (spaces and punctuation do not advance the key) and solve each independently as its own Caesar shift.",
        "flag": {"type": "per_team_dynamic_alpha", "content": "per-team-dynamic (placeholder, not read)", "data": "krypton4"}
    },
    {
        "id": "krypton-05",
        "name": "Krypton 5 -> 6: Vigenere Cipher (Kasiski Test)",
        "points": 450,
        "goal": "Break a Vigenere cipher when the key length isn't given.",
        "task": "`/home/krypton5/krypton6` is another Vigenere cipher, but this time you don't know the key length. Use the Kasiski examination (repeating ciphertext patterns) to estimate it -- likely 3, 6, or 9 -- then apply frequency analysis per group to recover the key.",
        "flag": {"type": "per_team_dynamic_alpha", "content": "per-team-dynamic (placeholder, not read)", "data": "krypton5"}
    },
    {
        "id": "krypton-06",
        "name": "Krypton 6 -> 7: Stream Cipher / LFSR",
        "points": 500,
        "goal": "Recover a repeating keystream and use it to decrypt the final password.",
        "task": "This is the final Krypton level. `/home/krypton6/final` is encrypted with a stream cipher whose keystream repeats every 30 characters -- the `encrypt` binary next to it implements it. Encrypt a long run of identical characters (30+ of them) to read the repeating keystream straight off the output, then use it to decrypt the final flag.",
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "krypton6"}
    }
]

# "Commands you may need" + "Helpful reading" shown directly in the
# description, free -- matching OverTheWire's own real page structure
# (see build_bandit.py's EXTRA_INFO comment for the full rationale).
EXTRA_INFO = {
    "krypton-00": (["base64"], []),
    "krypton-01": (["tr"], [("ROT13 on Wikipedia", "https://en.wikipedia.org/wiki/ROT13")]),
    "krypton-02": (["mktemp", "ln", "krypton-tools rotate"], [("Known-plaintext attack on Wikipedia", "https://en.wikipedia.org/wiki/Known-plaintext_attack"), ("Caesar cipher on Wikipedia", "https://en.wikipedia.org/wiki/Caesar_cipher")]),
    "krypton-03": (["krypton-tools freq", "tr"], [("Frequency analysis on Wikipedia", "https://en.wikipedia.org/wiki/Frequency_analysis")]),
    "krypton-04": (["krypton-tools columns", "krypton-tools vigenere-key", "krypton-tools vigenere-decrypt"], [("Vigenere cipher on Wikipedia", "https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher")]),
    "krypton-05": (["krypton-tools kasiski", "krypton-tools vigenere-key", "krypton-tools vigenere-decrypt"], [("Kasiski examination on Wikipedia", "https://en.wikipedia.org/wiki/Kasiski_examination")]),
    "krypton-06": (["krypton-tools stream-decrypt", "xxd"], [("Stream cipher on Wikipedia", "https://en.wikipedia.org/wiki/Stream_cipher")]),
}

# Crawl/walk/run hints per level (not krypton-start-here -- its
# description is already a full walkthrough). See build_bandit.py's
# HINTS comment for the tier structure and the quoting constraint (no
# literal double-quotes -- this script builds YAML by hand). Krypton is
# concept-heavy, so tier 1 is often a reading link rather than a bare
# command, matching each description's own "Helpful reading" section.
HINTS = {
    'krypton-00': [
        "Your home directory has a file of what looks like scrambled text -- but not every scrambled-looking file is actually encrypted. Some are just encoded in a standard, fully reversible text format. What might tell you which kind you're looking at?",
        "Base64 turns arbitrary bytes into a fixed, recognizable set of characters: letters, digits, `+`, `/`, and trailing `=` padding. That specific character set, especially the padding, is the tell that something is Base64 rather than an actual cipher, and Base64's own tooling has a documented flag for decoding straight back to the original data, no key or shift involved at all.",
        "`base64 -d ~/encoded.txt` decodes the file straight back to plaintext.\n\nIllustrative example only -- your real value will differ:\n```\nkrypton0@krypton:~$ cat encoded.txt\nUzFKWlVGUlBUa2xUUjFKRlFWUT0=\nkrypton0@krypton:~$ base64 -d ~/encoded.txt\n<the next password>\n```",
    ],
    'krypton-01': [
        "Every letter here has been shifted a fixed number of positions through the alphabet. If you knew that shift amount was exactly half of the alphabet's length, would applying that same shift a second time actually undo it?",
        "ROT13 shifts every letter 13 positions, wrapping at the end. Since the alphabet has 26 letters and 13 is exactly half, shifting by 13 twice returns you to where you started -- meaning the same transformation both encrypts and decrypts. A letter-substitution tool given two matching character ranges can apply that shift directly.",
        "`tr '[:alpha:]' 'N-ZA-Mn-za-m' < /home/krypton1/krypton2` applies the 13-position shift once, reversing the ROT13.\n\nIllustrative example only -- your real value will differ:\n```\nkrypton1@krypton:~$ tr '[:alpha:]' 'N-ZA-Mn-za-m' < /home/krypton1/krypton2\n<the next password>\n```",
    ],
    'krypton-02': [
        "There's an `encrypt` program here that will encrypt anything you give it using some fixed shift. If you already knew exactly what you fed it as input, and could see exactly what came out, would that tell you the shift directly?",
        "The `encrypt` binary looks for its key file in your CURRENT directory and reads plaintext from standard input, NOT from a filename argument. Make a scratch directory, symlink the key file there, and pipe or redirect known text into the program. If `A` becomes `M`, for example, the encryption shift is +12 because A is position 0 and M is position 12.",
        "Use these commands exactly. The output letter reveals the random shift; convert that letter to its zero-based position (`A=0`, `B=1`, ..., `Z=25`) and give the NEGATIVE value to the installed rotation helper.\n\nIllustrative example -- your observed letter and shift will differ:\n```\n$ work=$(mktemp -d)\n$ cd \"$work\"\n$ ln -s /home/krypton2/keyfile.dat\n$ printf 'AAAAAAAAAA' | /home/krypton2/encrypt\nMMMMMMMMMM\n$ krypton-tools rotate -12 /home/krypton2/krypton3\n<the next password>\n```\nDo not run `encrypt probe.txt`: this binary reads stdin and would wait for input instead of reading that file.",
    ],
    'krypton-03': [
        "This cipher substitutes one letter for another consistently throughout the text -- but English text itself isn't random: some letters show up far more often than others. Could counting how often each letter appears in the ciphertext hint at what it actually stands for?",
        "In normal English, letters like E, T, A, O, I, N appear consistently more often than the rest. If a substitution cipher always maps the same plaintext letter to the same ciphertext letter, counting ciphertext letter frequencies and matching that ranking against the known English frequency order recovers the substitution, one letter at a time. The extra intercepted files given alongside this one were encrypted with the same key, so combining them gives more data to count from.",
        "Combine all the files and count letter frequency, then map the most common ciphertext letters onto the most common English letters (E, T, A, O, I, N...).\n\nIllustrative example only -- your real ranking/value will differ:\n```\n$ krypton-tools freq found1 found2 found3 krypton4\nletter count percent\n     Q   812  12.70\n$ tr 'QXVJ...' 'ETAO...' < /home/krypton3/krypton4\n<the next password, possibly needing manual touch-ups>\n```",
    ],
    'krypton-04': [
        "This cipher uses a repeating multi-letter key rather than a single shift, meaning it's really several different Caesar shifts applied in rotation. If you knew the key's length, could you split the ciphertext into that many separate groups, each one shifted by just a single, consistent amount?",
        "A Vigenere cipher with a 6-letter key applies 6 different shifts in rotation: character 1 uses shift A, character 2 uses shift B, and so on, cycling back to shift A every 6th character. Pulling out every 6th character starting from each of the 6 positions produces 6 separate groups, each one encrypted with only a single, consistent shift, solvable the same way as an ordinary Caesar cipher, one group at a time.",
        "Split the LETTERS into 6 interleaved groups; spaces and punctuation do not consume a key character. Frequency-analyze each group independently, then reassemble.\n\nThe installed helper performs the easy-to-get-wrong grouping step. If comparing six frequency tables by hand stalls, its scorer tries all 26 Caesar shifts per column, prints the candidate key, and shows a preview you can judge as English:\n```\n$ krypton-tools columns 6 /home/krypton4/krypton5 | less\n$ krypton-tools vigenere-key 6 /home/krypton4/krypton5\ncandidate-key=......\npreview:\n...\n$ krypton-tools vigenere-decrypt <candidate-key> /home/krypton4/krypton5\n```",
    ],
    'krypton-05': [
        "This time you're not told the key length up front. Repeated chunks of plaintext, if they happen to line up with the same position in a REPEATING key, produce identical repeated chunks of ciphertext too -- could the DISTANCE between repeated ciphertext fragments hint at how long that key actually is?",
        "Look for repeated 3+ character sequences appearing more than once in the ciphertext, and note the distance, in characters, between each repeat. The true key length usually divides most of those distances evenly, since a repeated plaintext fragment only produces matching ciphertext when it lines up with the same key position both times. Once you know the key length, the rest is the same interleaved-grouping technique as before.",
        "Find repeated substrings and their distances; a common factor across several distances suggests the key length (here, 9). Split into 9 groups, solve each with frequency analysis, and reassemble.\n\nThe installed helper reports evidence rather than silently choosing a key. Prefer factors supported by several gaps; an incidental repeat can make the raw GCD equal 1. Then score and decrypt with the candidate length:\n```\n$ krypton-tools kasiski /home/krypton5/krypton6\n...\ncandidate-length-support=3:... 9:...\n$ krypton-tools vigenere-key 9 /home/krypton5/krypton6\n$ krypton-tools vigenere-decrypt <candidate-key> /home/krypton5/krypton6\n```",
    ],
    'krypton-06': [
        "This cipher combines each byte of plaintext with a byte from what's supposed to be a random keystream, except that keystream turns out to repeat after a fixed number of characters. If you already knew a long, predictable stretch of plaintext, could feeding it through the cipher directly reveal that repeating keystream?",
        "Feeding the encryption program a long run of identical, known characters (since every input byte is the same known value) means the corresponding output bytes reveal the raw keystream itself, byte for byte, wherever the relationship between a known plaintext byte and its output byte can be reversed. Once you've recovered the full repeating keystream (30 bytes long here), applying that same relationship to the real ciphertext, cycling the keystream every 30 bytes, recovers the final plaintext.",
        "Create 60 known `A` characters, encrypt them, then give the known input, its encrypted output, and the real ciphertext to the installed helper. It derives the repeating additive shifts and applies them to `final`:\n```\n$ python3 -c 'print(\"A\" * 60, end=\")' > known.txt\n$ /home/krypton6/encrypt < known.txt > encrypted.txt\n$ krypton-tools stream-decrypt known.txt encrypted.txt /home/krypton6/final\n<the final flag>\n```",
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
            "\n\n---\n\n### Up next\n"
            "After submitting this flag, begin Krypton 0 -> 1: "
            "Base64 Decoding. Connect as `krypton0` (password `krypton0`, the fixed "
            "public entry password) and decode the Base64 string in your home "
            "directory to find the password for `krypton1`."
        )

    level = int(challenge_id.rsplit("-", 1)[1])

    if level == 6:
        return (
            "\n\n---\n\n### Finish line\n"
            "You are working as `krypton6`. Submit the recovered "
            "password here to complete the Krypton track; no further account switch is required."
        )

    return (
        "\n\n---\n\n### Moving on\n"
        f"You are working as `krypton{level}`. After "
        "recovering and submitting this password, exit and reconnect as "
        f"`krypton{level + 1}` at the host and port shown by the launch panel, "
        "using the recovered password, before starting the next level."
    )


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _render_description(challenge: dict) -> str:
    """Sectioned layout: `## Goal` header, `---` separator, the middle
    section(s), another `---`, then the progression note's own `###`
    section (see _progression_note). krypton-start-here supplies a fully
    custom multi-section `body`; every other level gets a `### The task`
    section built from its `task` text plus the EXTRA_INFO commands and
    reading lists."""
    if "body" in challenge:
        middle = challenge["body"]
    else:
        task_parts = []
        task = challenge.get("task", "")
        if task:
            task_parts.append(task)
        extra_info = EXTRA_INFO.get(challenge["id"])
        if extra_info:
            cmds, reading = extra_info
            if cmds:
                cmd_list = ", ".join(f"`{command}`" for command in cmds)
                task_parts.append(f"**Commands you may need:** {cmd_list}")
            if reading:
                # No live links: the venue network runs with no internet access
                # (see docs/offline-dependency-audit.md and
                # cei-labs-event#8/live-hint-links-offline-gap), so these are
                # rendered as plain reference titles rather than clickable
                # [title](url) markdown links, which would be dead at the venue.
                links = "\n".join(f"- {title}" for title, url in reading)
                task_parts.append(f"**Helpful reading:**\n{links}")
        middle = "### The task"
        if task_parts:
            middle += "\n" + "\n\n".join(task_parts)
    return f"## Goal\n{challenge['goal']}\n\n---\n\n{middle}" + _progression_note(challenge["id"])


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

    # Indent continuation lines for the YAML block scalar (the template
    # already indents the first line); leave blank lines truly empty
    # rather than whitespace-only.
    escaped_desc = "\n".join(
        ("  " + line) if line and n else line
        for n, line in enumerate(full_desc.split("\n"))
    )
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
