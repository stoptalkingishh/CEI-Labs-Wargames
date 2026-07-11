import os


def _flags_yaml(flag) -> str:
    """A challenge's `flag` field is either a plain string (the historical
    shorthand -- ctfcli treats it as a static, case-sensitive flag) or a
    dict (per_team_dynamic_fixed and any future non-static type) --
    ctfcli's _create_flags() POSTs a non-string entry to /api/v1/flags
    verbatim, so the dict's keys must already match that API's real
    fields (type/content/data)."""
    if isinstance(flag, dict):
        lines = [f"  - type: {flag['type']}\n"]
        lines.append(f"    content: \"{flag['content']}\"\n")
        if "data" in flag:
            lines.append(f"    data: \"{flag['data']}\"\n")
        return "".join(lines)
    return f'  - "{flag}"\n'


# Self-hosted image reference (see docs/self-hosted-wargames-blueprint.md
# Phase 2's "Wire Bandit into CTFd" task). Not yet published by a CI
# workflow -- until it is, build+tag locally with this exact name/tag
# before deploying (`docker build -t ghcr.io/stoptalkingishh/cei-labs-
# wargames/bandit-target:latest targets/bandit`) so `docker stack deploy`
# can find it.
BANDIT_IMAGE = "ghcr.io/stoptalkingishh/cei-labs-wargames/bandit-target:latest"

# All 34 challenges deliberately share ONE instance_group -- launching any
# of them creates/reuses the SAME persistent container (see
# InstanceChallengeConfig.resolved_instance_key() in cei-labs-engine),
# matching the real game's "one box, 34 levels" design. Only the final
# level opts into shutdown_on_solve: with several challenges sharing a
# group, the auto-shutdown countdown only starts once every
# shutdown_on_solve=True challenge in the group is solved (see
# cei-labs-engine's solve_hook.py) -- so setting it on level 33 alone
# means the shared box stays up for the whole run and tears down once a
# team actually finishes the game, not after their first solve.
INSTANCE_GROUP = "bandit"

# A player's connection details (host/port, live status) come from the
# "Launch Environment" control on this challenge itself -- injected into
# the challenge view by cei-labs-engine's instance-launcher plugin, not
# written into these descriptions, since the port is only known once an
# instance actually exists. See the "Bandit: Start Here" challenge for how
# that control works.
#
# All 34 levels connect as a Linux user named after the level (`bandit0`,
# `bandit1`, ...) using the previous level's flag as that account's
# password, so that pairing is stated once here rather than in every
# description below.

# Define the dataset for Bandit Levels 0 to 33
challenges_data = [
    {
        "id": "bandit-start-here",
        "name": "Bandit: Start Here",
        "points": 10,
        "desc": (
            "**Goal:** Learn the launch controls, then prove you used them.\n\n"
            "Every challenge in Bandit that needs a live environment has a launch control "
            "attached to it, right here on the challenge itself:\n"
            "- **Launch Environment** -- starts your box, or reconnects you to one that's "
            "already running. All 34 Bandit levels share this one box.\n"
            "- **Reboot Host** -- restarts it in place if it gets stuck. Same connection "
            "details afterward.\n"
            "- **Relaunch Environment** -- destroys and recreates it from scratch. Use this "
            "if something's broken beyond a reboot; anything you changed inside it is lost.\n"
            "- **+5 more minutes** -- shows up only once you've solved every level in this "
            "track and a shutdown countdown has started. Extends it if you're not done "
            "looking around yet.\n\n"
            "Click Launch, wait for it to show a host and port, then connect as `bandit0` "
            "with password `bandit0` and read `welcome.txt` in the home directory (not "
            "`readme` -- that one's level 0's real puzzle). Submit its contents as your flag."
        ),
        "flag": "WELCOME_TO_BANDIT"
    },
    {
        "id": "bandit-00",
        "name": "Bandit 0 -> 1: The First Step",
        "points": 100,
        "desc": "**Goal:** Connect to the server and retrieve the flag.\n\nLog in as `bandit0` with password `bandit0`.\n\nRead the `readme` file in the home directory to find the password for the next level. Submit that password here as your flag.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit0"}
    },
    {
        "id": "bandit-01",
        "name": "Bandit 1 -> 2: Dashed Hopes",
        "points": 150,
        "desc": "**Goal:** Read a file whose name looks like a command-line flag.\n\nLog in as `bandit1`. The next password is hidden in a file named `-` (a single dash) in the home directory.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit1"}
    },
    {
        "id": "bandit-02",
        "name": "Bandit 2 -> 3: Spaces in Places",
        "points": 200,
        "desc": "**Goal:** Read a file whose name contains spaces.\n\nLog in as `bandit2`. The next password is in a file called `spaces in this filename`, in the home directory.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit2"}
    },
    {
        "id": "bandit-03",
        "name": "Bandit 3 -> 4: Hidden in Plain Sight",
        "points": 250,
        "desc": "**Goal:** Find a hidden (dotfile) password.\n\nLog in as `bandit3`. The next password is hidden inside the `inhere` directory -- you'll need to show hidden files to find it.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit3"}
    },
    {
        "id": "bandit-04",
        "name": "Bandit 4 -> 5: Human Readable",
        "points": 300,
        "desc": "**Goal:** The password for the next level is stored in one of the files in the `inhere` directory. It is the only file that contains human-readable text.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit4"}
    },
    {
        "id": "bandit-05",
        "name": "Bandit 5 -> 6: The Needle",
        "points": 350,
        "desc": "**Goal:** Find one specific file among many nested decoys.\n\nLog in as `bandit5`. Somewhere under `inhere` (which has subdirectories) is a file matching all three properties:\n1. Human-readable\n2. Exactly 1033 bytes in size\n3. Not executable",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit5"}
    },
    {
        "id": "bandit-06",
        "name": "Bandit 6 -> 7: Server Search",
        "points": 400,
        "desc": "**Goal:** Search the whole filesystem by owner, group, and size.\n\nLog in as `bandit6`. The next password is somewhere on the server (not necessarily under your home directory) -- owned by user `bandit7`, group `bandit6`, exactly 33 bytes.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit6"}
    },
    {
        "id": "bandit-07",
        "name": "Bandit 7 -> 8: The Millionth Word",
        "points": 450,
        "desc": "**Goal:** Extract a value next to a known marker word.\n\nLog in as `bandit7`. The next password is in `data.txt`, on the same line as the word `millionth`.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit7"}
    },
    {
        "id": "bandit-08",
        "name": "Bandit 8 -> 9: The Only One",
        "points": 500,
        "desc": "**Goal:** Find the one line that appears only once in a large file.\n\nLog in as `bandit8`. The next password is the one line in `data.txt` that occurs exactly once.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit8"}
    },
    {
        "id": "bandit-09",
        "name": "Bandit 9 -> 10: Strings Attached",
        "points": 550,
        "desc": "**Goal:** Pull the readable text out of a mostly-binary file.\n\nLog in as `bandit9`. The next password is one of the few human-readable strings in `data.txt`, preceded by several `=` characters.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit9"}
    },
    {
        "id": "bandit-10",
        "name": "Bandit 10 -> 11: Base Operations",
        "points": 600,
        "desc": "**Goal:** Decode a base64-encoded password.\n\nLog in as `bandit10`. `data.txt` holds the next password encoded in base64 -- decode it.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit10"}
    },
    {
        "id": "bandit-11",
        "name": "Bandit 11 -> 12: Substitution",
        "points": 650,
        "desc": "**Goal:** Reverse a ROT13 substitution.\n\nLog in as `bandit11`. `data.txt` holds the next password with every letter rotated 13 positions (ROT13) -- reverse it.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit11"}
    },
    {
        "id": "bandit-12",
        "name": "Bandit 12 -> 13: Matryoshka",
        "points": 700,
        "desc": "**Goal:** Unwrap several layers of hexdump and compression.\n\nLog in as `bandit12`. `data.txt` is a hexdump of a file that's been compressed multiple times. Revert the hexdump, then decompress repeatedly (gzip, bzip2, tar -- the file type at each step tells you which) to reach the password.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit12"}
    },
    {
        "id": "bandit-13",
        "name": "Bandit 13 -> 14: Private Keys",
        "points": 750,
        "desc": "**Goal:** Use a provided private key to log in as another account.\n\nLog in as `bandit13`. Use the provided private SSH key (`sshkey.private`, in the home directory) to log into `bandit14` on localhost, then read the password from `/etc/bandit_pass/bandit14`.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit13"}
    },
    {
        "id": "bandit-14",
        "name": "Bandit 14 -> 15: Port Submission",
        "points": 800,
        "desc": "**Goal:** Submit a password to a listening TCP service.\n\nLog in as `bandit14`. Submit the current password to **port 30000 on localhost** to receive the next one.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit14"}
    },
    {
        "id": "bandit-15",
        "name": "Bandit 15 -> 16: SSL Encryption",
        "points": 850,
        "desc": "**Goal:** Submit a password over a TLS-encrypted connection.\n\nLog in as `bandit15`. Submit the current password to **port 30001 on localhost**, this time over SSL/TLS.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit15"}
    },
    {
        "id": "bandit-16",
        "name": "Bandit 16 -> 17: SSL Port Scan",
        "points": 900,
        "desc": "**Goal:** Find the one correct service among a range of listening ports.\n\nLog in as `bandit16`. The next credentials come from submitting the current password to the right port somewhere in the range **31000-32000 on localhost** -- scan the range to find which one actually wants it.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit16"}
    },
    {
        "id": "bandit-17",
        "name": "Bandit 17 -> 18: File Comparisons",
        "points": 950,
        "desc": "**Goal:** Diff two large, nearly-identical files.\n\nLog in as `bandit17`. The home directory has `passwords.old` and `passwords.new`. The next password is on the one line that changed between them.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit17"}
    },
    {
        "id": "bandit-18",
        "name": "Bandit 18 -> 19: Shell Bypass",
        "points": 1000,
        "desc": "**Goal:** Read a file without getting an interactive shell.\n\nLog in as `bandit18` -- this account's `.bashrc` has been modified to log you out immediately on interactive login. Find a way to still read the `readme` file in its home directory.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit18"}
    },
    {
        "id": "bandit-19",
        "name": "Bandit 19 -> 20: SUID Escalation",
        "points": 1050,
        "desc": "**Goal:** Use a setuid binary to read a file you otherwise couldn't.\n\nLog in as `bandit19`. The home directory has a setuid binary -- use it to reach the next password.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit19"}
    },
    {
        "id": "bandit-20",
        "name": "Bandit 20 -> 21: Port Listener Connection",
        "points": 1100,
        "desc": "**Goal:** Have a setuid binary connect back to a listener you control.\n\nLog in as `bandit20`. The home directory has a setuid binary that connects to a port on localhost you supply as an argument, reads a line, and checks it against the current password. Set up a listener of your own first, then trigger the connection.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit20"}
    },
    {
        "id": "bandit-21",
        "name": "Bandit 21 -> 22: Cron Jobs",
        "points": 1150,
        "desc": "**Goal:** Read what a cron job does and follow it to the password.\n\nLog in as `bandit21`. A job runs automatically on a schedule via cron -- check `/etc/cron.d/` for the configuration and see where it leads.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit21"}
    },
    {
        "id": "bandit-22",
        "name": "Bandit 22 -> 23: Cron Debugging",
        "points": 1200,
        "desc": "**Goal:** Trace a cron job to the script it actually runs.\n\nLog in as `bandit22`. Same starting point as before (`/etc/cron.d/`), but this time you'll need to find and read the script the job executes to see where it writes the password.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit22"}
    },
    {
        "id": "bandit-23",
        "name": "Bandit 23 -> 24: Cron Scripting",
        "points": 1250,
        "desc": "**Goal:** Write your own script for a cron job to run on your behalf.\n\nLog in as `bandit23`. This cron job runs whatever script matches a pattern you can influence -- write your own to copy out the password.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit23"}
    },
    {
        "id": "bandit-24",
        "name": "Bandit 24 -> 25: PIN Brute Force",
        "points": 1300,
        "desc": "**Goal:** Brute-force a 4-digit PIN against a listening daemon.\n\nLog in as `bandit24`. A daemon on port 30002 returns the next password if you send it the current password plus the correct 4-digit PIN -- script the brute force.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit24"}
    },
    {
        "id": "bandit-25",
        "name": "Bandit 25 -> 26: Shell Breakout",
        "points": 1350,
        "desc": "**Goal:** Escape a restricted, non-bash login shell.\n\nLog in as `bandit25`. Account `bandit26`'s login shell isn't `/bin/bash` -- find out what it actually is and how to break out of it into a real shell.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit25"}
    },
    {
        "id": "bandit-26",
        "name": "Bandit 26 -> 27: Text UI Breakout",
        "points": 1400,
        "desc": "**Goal:** Break out of a terminal pager into a shell.\n\nLog in as `bandit26` (this account's shell pages a short file and exits immediately -- shrinking your terminal window before connecting buys you a window to act in). Once you've broken out, look around the filesystem to find the flag.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit26"}
    },
    {
        "id": "bandit-27",
        "name": "Bandit 27 -> 28: Git Clone",
        "points": 1450,
        "desc": "**Goal:** Clone a git repository and find a password committed to it.\n\nA repository is reachable at `ssh://bandit27-git@<your-instance-host>/home/bandit27-git/repo` (use the SSH port your launch panel shows). Log in with `bandit27`'s own password (the previous level's flag), clone it, and find the next password.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit27"}
    },
    {
        "id": "bandit-28",
        "name": "Bandit 28 -> 29: Git Commits",
        "points": 1500,
        "desc": "**Goal:** Find a secret that was committed and later removed.\n\nRepository: `ssh://bandit28-git@<your-instance-host>/home/bandit28-git/repo`, login with `bandit28`'s own password. Clone it and check the commit history -- the current tree isn't the only place a password could have been.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit28"}
    },
    {
        "id": "bandit-29",
        "name": "Bandit 29 -> 30: Git Branches",
        "points": 1550,
        "desc": "**Goal:** Find a secret that only exists on a non-default branch.\n\nRepository: `ssh://bandit29-git@<your-instance-host>/home/bandit29-git/repo`, login with `bandit29`'s own password. Clone it and check every branch, not just the default.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit29"}
    },
    {
        "id": "bandit-30",
        "name": "Bandit 30 -> 31: Git Tags",
        "points": 1600,
        "desc": "**Goal:** Find a secret attached to a git tag.\n\nRepository: `ssh://bandit30-git@<your-instance-host>/home/bandit30-git/repo`, login with `bandit30`'s own password. Clone it and check the tags.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit30"}
    },
    {
        "id": "bandit-31",
        "name": "Bandit 31 -> 32: Git Push",
        "points": 1650,
        "desc": "**Goal:** Satisfy a repository's own stated requirements to earn the next password.\n\nRepository: `ssh://bandit31-git@<your-instance-host>/home/bandit31-git/repo`, login with `bandit31`'s own password. Clone it, read the README for the exact requirements, then push a file that meets them to receive the password.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit31"}
    },
    {
        "id": "bandit-32",
        "name": "Bandit 32 -> 33: Shell Overrides",
        "points": 1700,
        "desc": "**Goal:** Reach a real shell from one that mangles every command you type.\n\nLog in as `bandit32` -- this account's shell uppercases every command before running it. Find a way around that limitation to reach a normal shell, then locate the next password.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit32"}
    },
    {
        "id": "bandit-33",
        "name": "Bandit 33 -> 34: Final Escape",
        "points": 1750,
        "desc": "**Goal:** One last escape to finish the track.\n\nLog in as `bandit33`. After all that git work, it's time for one more escape. Good luck.",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit33"}
    }
]

# "Commands you may need" + "Helpful reading" shown directly in the
# description, free -- matching OverTheWire's own real page structure
# exactly (real OTW pages for these same techniques were used as the
# source for the command lists and reading links below, provided
# directly by the user). Distinct from the hints' tier 1, which exists
# for players mid-challenge who skip the description or want a nudge
# without leaving the launch flow -- some overlap between the two is
# intentional, matching how OTW's own reading links are themselves a
# form of always-visible, free hint.
EXTRA_INFO = {
    "bandit-00": (["ssh"], [("Secure Shell (SSH) on Wikipedia", "https://en.wikipedia.org/wiki/Secure_Shell")]),
    "bandit-01": (["ls", "cat", "find"], [("Advanced Bash-Scripting Guide -- Special Characters", "https://linux.die.net/abs-guide/special-chars.html")]),
    "bandit-02": (["ls", "cat"], []),
    "bandit-03": (["ls", "cat"], []),
    "bandit-04": (["ls", "cat", "file"], [("The file command on Wikipedia", "https://en.wikipedia.org/wiki/File_%28command%29")]),
    "bandit-05": (["find", "file", "cat"], []),
    "bandit-06": (["find", "cat"], []),
    "bandit-07": (["grep"], []),
    "bandit-08": (["sort", "uniq"], []),
    "bandit-09": (["strings", "grep"], []),
    "bandit-10": (["base64"], [("Base64 on Wikipedia", "https://en.wikipedia.org/wiki/Base64")]),
    "bandit-11": (["tr"], [("ROT13 on Wikipedia", "https://en.wikipedia.org/wiki/ROT13")]),
    "bandit-12": (["mkdir", "cp", "mv", "file", "xxd", "gunzip", "bunzip2"], [("Hex dump on Wikipedia", "https://en.wikipedia.org/wiki/Hex_dump")]),
    "bandit-13": (["ssh", "chmod"], [("SSH/OpenSSH/Keys", "https://help.ubuntu.com/community/SSH/OpenSSH/Keys")]),
    "bandit-14": (["nc"], []),
    "bandit-15": (["openssl"], [("Transport Layer Security on Wikipedia", "https://en.wikipedia.org/wiki/Transport_Layer_Security")]),
    "bandit-16": (["nmap", "openssl", "nc"], [("Port scanner on Wikipedia", "https://en.wikipedia.org/wiki/Port_scanner")]),
    "bandit-17": (["diff"], []),
    "bandit-18": (["ssh"], []),
    "bandit-19": (["find"], [("Setuid on Wikipedia", "https://en.wikipedia.org/wiki/Setuid")]),
    "bandit-20": (["nc", "bash job control (&, fg, jobs)"], []),
    "bandit-21": (["crontab"], []),
    "bandit-22": (["crontab", "cat"], []),
    "bandit-23": (["crontab", "chmod"], []),
    "bandit-24": (["nc", "bash scripting"], []),
    "bandit-25": (["more"], []),
    "bandit-26": (["vi"], []),
    "bandit-27": (["git"], [("Installing Git", "https://git-scm.com/book/en/v2/Getting-Started-Installing-Git"), ("Git from the Bottom Up", "https://jwiegley.github.io/git-from-the-bottom-up/")]),
    "bandit-28": (["git"], [("Installing Git", "https://git-scm.com/book/en/v2/Getting-Started-Installing-Git"), ("Git from the Bottom Up", "https://jwiegley.github.io/git-from-the-bottom-up/")]),
    "bandit-29": (["git"], [("Installing Git", "https://git-scm.com/book/en/v2/Getting-Started-Installing-Git"), ("Git from the Bottom Up", "https://jwiegley.github.io/git-from-the-bottom-up/")]),
    "bandit-30": (["git"], [("Installing Git", "https://git-scm.com/book/en/v2/Getting-Started-Installing-Git"), ("Git from the Bottom Up", "https://jwiegley.github.io/git-from-the-bottom-up/")]),
    "bandit-31": (["git"], [("Installing Git", "https://git-scm.com/book/en/v2/Getting-Started-Installing-Git"), ("Git from the Bottom Up", "https://jwiegley.github.io/git-from-the-bottom-up/")]),
    "bandit-32": (["bash"], []),
    "bandit-33": (["find", "sh"], []),
}

# Crawl/walk/run hints per level (not bandit-start-here -- its
# description is already a full walkthrough). A HINTS entry is either a
# single (content, cost) tuple (legacy) or a list of up to 3 tuples,
# cheapest first:
#   tier 1 "crawl" -- near-free. ONLY the bare tool/manpage name or a
#     single reading link, nothing more -- no explanation of what it
#     does or how it applies here. Same spirit as the description's own
#     "Commands you may need" list. For someone who already knows the
#     concept but is rusty on the exact tool/syntax.
#   tier 2 "walk" -- about half the challenge's points. A real
#     explanation of the underlying concept that explicitly names tier
#     1's tool/reference, but stops short of the literal exact command
#     line, flag combination, or payload -- the player still connects it
#     to the problem themselves. A real lifeline, not a finished command.
#   tier 3 "run" -- most of the challenge's points (deliberately: using
#     it should leave almost nothing to "win" by solving after). A
#     close-to-complete walkthrough of the METHOD, explaining WHY it
#     works and HOW to execute it, condensed from real writeups where the
#     technique isn't obvious -- still requires the player to run the
#     commands and read output themselves rather than being handed the
#     literal flag value.
# Content must not contain a literal double-quote character (this script
# builds YAML by hand, not via PyYAML -- use backticks/single quotes for
# anything that needs quoting).
HINTS = {
    "bandit-00": [
        ("`man ssh`.", 5),
        ("SSH is a secure remote login program: `ssh <user>@<host> -p <port>` opens a login session on another machine. Once logged in, standard commands like `ls` and `cat` work exactly as they would on your own machine.", 50),
        ("Connect with `ssh bandit0@<host> -p <port>`, enter password `bandit0` when prompted, then run `cat readme` once logged in. Whatever it prints is the flag for this level -- submit it here.", 75),
    ],
    "bandit-01": [
        ("`man cat`.", 10),
        ("Most command-line tools treat a filename starting with `-` as an option flag, not a literal filename, because `-` conventionally introduces flags. `cat`'s manual page documents a standard way to tell it 'everything after this point is a filename, not a flag.'", 75),
("A filename of just `-` gets misread by `cat` -- and not just as a flag: even `cat -- -` (which does stop flag-parsing) still treats a bare `-` argument as a request to read from standard input by long-standing Unix convention, so it will hang waiting for input rather than reading the file. Prefix the filename with a path instead: `cat ./-` makes it unambiguously a real path, not standard input.", 112),
    ],
    "bandit-02": [
        ("`man ls`.", 15),
        ("A space normally separates one argument from the next on a command line, so a filename containing spaces has to be passed as a single argument somehow -- either by wrapping the whole name in quotes, or by escaping each individual space character.", 100),
        ("`ls -la` in the home directory shows a file literally named `spaces in this filename`. Read it with `cat 'spaces in this filename'` (single quotes around the whole name) or `cat spaces\\ in\\ this\\ filename` (a backslash before each space).", 150),
    ],
    "bandit-03": [
        ("`man ls`.", 15),
        ("On Linux, any filename starting with a `.` is hidden from a plain directory listing by convention -- not a real permission, just a display convention every standard tool respects. `ls` has a documented flag to show hidden entries too.", 100),
        ("`ls -la inhere` (the `-a` flag shows hidden entries) reveals a dotfile. `cat` that filename directly to read the password.", 150),
    ],
    "bandit-04": [
        ("`man file`.", 5),
        ("`file` identifies a file's actual content type by reading its bytes, independent of what it's named -- useful when several identically-patterned filenames hide one real difference. It also accepts a wildcard/glob to check many files in one call.", 150),
        ("`cd inhere`, then `file ./*` (or `file -- *` if any names start with a dash) checks every file's real type in one pass -- the decoys are named to look identical, but `file` reads actual bytes, not names. The binary ones report as 'data'; exactly one reports as ASCII/text. Once you've spotted that filename, `cat` it (quoting or escaping the name if it starts with a dash) to read the password.", 225),
    ],
    "bandit-05": [
        ("`man find`.", 15),
        ("`find` can filter by multiple properties at once -- size, type, permissions -- by chaining several tests on one command line, narrowing the result set with each added test. Combining every property mentioned in the goal text into one search should leave very few candidates.", 175),
        ("`find inhere -size 1033c -type f ! -executable` chains all three stated properties (size, regular file, not executable) into one search. If more than one result comes back, run `file` on each -- only the genuinely human-readable one is the password file; the rest are decoys.", 262),
    ],
    "bandit-06": [
        ("`man find`.", 20),
        ("`find` can search starting from any directory, including the whole filesystem from `/`, and filter by owner and group as well as size. Searching from `/` also means it will try to look inside directories you can't read, which prints a lot of permission-denied noise you'll want to suppress.", 200),
        ("`find / -user bandit7 -group bandit6 -size 33c 2>/dev/null` searches the entire filesystem for the three stated properties at once; `2>/dev/null` throws away the permission-denied errors so the one real result isn't buried in noise. `cat` whatever path it returns.", 300),
    ],
    "bandit-07": [
        ("`man grep`.", 25),
        ("A text-search tool can jump straight to the line containing a specific word instead of you scrolling through a large file by hand -- the goal text names the exact marker word to search for.", 225),
        ("`grep millionth data.txt` prints only the line(s) containing that word -- the password is the value right next to it on that same line.", 337),
    ],
    "bandit-08": [
        ("`man uniq`.", 30),
        ("`uniq` only detects duplicate lines that are directly ADJACENT to each other, so a file needs sorting first before `uniq` can group identical lines together. Once sorted, `uniq` has a documented flag for printing only the lines with no duplicate at all.", 250),
        ("`sort data.txt | uniq -u` sorts the file so identical lines become adjacent, then prints only the lines that occur exactly once -- that's the password, since every decoy line in the file appears more than once.", 375),
    ],
    "bandit-09": [
        ("`man strings`.", 30),
        ("`strings` pulls out only the human-readable runs of characters from an otherwise binary/garbage file -- once the readable text is visible, the goal text tells you the password is preceded by several `=` characters, which a text-search tool can filter for.", 250),
        ("`strings data.txt | grep '^='` extracts the readable text from the binary file, then filters to just the line(s) that start with one or more `=` characters -- the password follows the equals signs on that line.", 375),
    ],
    "bandit-10": [
        ("`man base64`.", 35),
        ("The password isn't hidden this time, just encoded in a standard, reversible text format -- recognizing the character set (letters, digits, `+`, `/`, `=` padding) is the tell for which encoding it is, and that encoding's own tool has a documented flag for reversing it.", 275),
        ("`base64 -d data.txt` decodes the file directly back to the plaintext password -- no other steps needed.", 412),
    ],
    "bandit-11": [
        ("`man tr`.", 35),
        ("ROT13 shifts every letter 13 places through the alphabet, wrapping at the end. Because the alphabet has 26 letters and 13 is exactly half, applying the SAME shift twice returns you to the original text -- meaning encoding and decoding are the identical operation. `tr` can perform an arbitrary letter-for-letter substitution given two character ranges.", 275),
        ("`tr 'A-Za-z' 'N-ZA-Mn-za-m' < data.txt` maps every letter to the one 13 positions ahead (wrapping past Z back to A), which both encodes and decodes ROT13 since it's a self-inverse cipher. Running the file through this once reveals the password.", 412),
    ],
    "bandit-12": [
        ("`man xxd`.", 40),
        ("A hexdump is a text representation of raw binary bytes, not a file you read directly -- `xxd` can convert a hexdump back into real binary. Once it's real bytes again, `file` can tell you what kind of (likely compressed) data it actually is, and the process may need repeating more than once.", 350),
        ("Copy `data.txt` to a scratch directory, then `xxd -r data.txt > data.bin` to reverse the hexdump back to real bytes. Run `file data.bin` to see what compression it actually is (in this deployment: gzip, then bzip2 underneath that) -- decompress one layer (`gunzip`/`bunzip2`), checking `file` again after each step, until what's left is plain text: the password.", 525),
    ],
    "bandit-13": [
        ("`man ssh`.", 40),
        ("SSH doesn't only support password logins -- a private key file can authenticate you directly, as long as the matching public key is already trusted by the target account. SSH's manual documents both how to specify a key file and how strict it is about that file's permissions.", 350),
        ("`chmod 600 sshkey.private` first if SSH complains the key's permissions are too open, then `ssh -i sshkey.private bandit14@localhost` logs you straight into `bandit14` on the SAME box using that key instead of a password. Once in, `cat /etc/bandit_pass/bandit14` reads the next password.", 525),
    ],
    "bandit-14": [
        ("`man nc`.", 45),
        ("'Submitting' a password to a port just means opening a raw TCP connection to that port and sending the password as a line of text -- netcat is the standard, minimal tool for opening a raw connection and sending/receiving whatever text you type.", 375),
        ("`nc localhost 30000` opens a connection to the port; once connected, type the CURRENT level's password (bandit14's own password) and press enter. The service reads it, and if correct, sends back the password for bandit15.", 562),
    ],
    "bandit-15": [
        ("`man openssl`.", 45),
        ("This port speaks the same protocol as the last level, but wrapped in SSL/TLS encryption -- plain netcat can't perform a TLS handshake, so you need a client that can. OpenSSL ships a subcommand specifically for opening an encrypted client connection by hand.", 400),
        ("`openssl s_client -connect localhost:30001` performs the TLS handshake and drops you into an encrypted session; once connected, type bandit15's password and press enter, same as the netcat step before. The response contains bandit16's password.", 600),
    ],
    "bandit-16": [
        ("`man nmap`.", 50),
        ("Not every port in the given range is actually listening, and among the ones that are, only one both speaks SSL/TLS AND expects your password. A port scanner can narrow down which ports in a range are even open before you try connecting to each by hand, and can also try to identify which protocol each one speaks.", 425),
        ("`nmap -p 31000-32000 --open localhost` lists which ports in the range actually have something listening; adding `-sV` additionally tries to identify which of those speak SSL. Connect to each SSL-speaking candidate with `openssl s_client -connect localhost:<port>` and send bandit16's password -- only one will respond with bandit17's.", 637),
    ],
    "bandit-17": [
        ("`man diff`.", 50),
        ("Both files are large, but only ONE line changed between them -- a diff tool exists specifically to surface exactly what changed between two versions of similar text, rather than you comparing them line-by-line by hand.", 425),
        ("`diff passwords.old passwords.new` prints only the lines that differ between the two files (conventionally prefixed with `<` for the old version and `>` for the new one). The `>` line is the current password for bandit18.", 637),
    ],
    "bandit-18": [
        ("`man ssh`.", 55),
        ("The account's `.bashrc` is what's logging you out, but `.bashrc` only runs for INTERACTIVE login shells. SSH's manual documents a form of the command that runs a single remote command directly, without starting an interactive shell session at all.", 475),
        ("`ssh bandit18@<host> -p <port> cat readme` appends a command directly to the SSH invocation -- SSH runs just that one command non-interactively over the connection and returns its output, entirely bypassing the interactive-shell startup (and therefore `.bashrc`) that would otherwise log you out immediately.", 712),
    ],
    "bandit-19": [
        ("[Setuid on Wikipedia](https://en.wikipedia.org/wiki/Setuid).", 55),
        ("A setuid binary runs with the FILE OWNER's permissions, not the permissions of whoever launched it -- meaning if a more-privileged account owns this binary, running it lets you act with THAT account's privileges for as long as it's running. Running an unfamiliar binary with no arguments often prints a usage message telling you how it expects to be invoked.", 475),
        ("Run the setuid binary in bandit19's home directory with no arguments to see its usage message -- it expects a command to run with elevated privilege. Passing it something like `./bandit20-do cat /etc/bandit_pass/bandit20` (quoted as one argument if needed) runs that `cat` as the binary's owner, printing bandit20's password directly.", 712),
    ],
    "bandit-20": [
        ("`man nc`.", 60),
        ("The setuid binary here doesn't read a password from a file -- it CONNECTS OUT to a port on localhost that YOU choose, expecting to receive the previous level's password over that connection. That means something needs to be listening on that port BEFORE the binary is triggered; netcat can act as a listener (`-l`) as well as a client, and basic shell job control (`&`, `fg`) lets you run two things in one SSH session.", 525),
        ("In one terminal (or backgrounded with `&`), start a listener: `nc -lvp <some port>`. In a second connection (or foreground job), run the setuid binary with that same port number as its argument. Back in the listener's session, type bandit20's password and press enter -- the binary reads it, validates it, and sends back bandit21's password over that same connection, which the listener will print.", 787),
    ],
    "bandit-21": [
        ("`man 5 crontab`.", 60),
        ("Cron runs commands automatically on a schedule, configured by plain text files under `/etc/cron.d/` that name WHICH user runs WHAT command and how often. Reading the config directly tells you exactly what's about to run and as whom, without needing to reverse-engineer anything.", 525),
        ("`cat /etc/cron.d/*` lists every scheduled job on the box, including one that already does the work of writing the next password somewhere for you (as a bandit22-privileged process) -- read the command it runs and follow where it writes its output to get the password.", 787),
    ],
    "bandit-22": [
        ("`man 5 crontab`.", 65),
        ("The cron job here calls a shell script by path rather than running a command directly -- since that script runs with bandit23's privileges (not yours), reading the script's own source (which you CAN do) tells you exactly where it writes its output, even if that destination isn't obvious ahead of time.", 562),
        ("`cat /etc/cron.d/*` shows the job runs a script under `/usr/bin/cronjob_bandit22.sh` (or similarly named) as bandit23. `cat` that script directly -- it computes an output filename from `whoami` piped through `md5sum`, which you can reproduce yourself by substituting `bandit23` for the username, then `cat` the resulting path under `/tmp` to read the password it wrote there.", 837),
    ],
    "bandit-23": [
        ("`man 5 crontab`.", 65),
        ("This cron job scans a shared, world-writable directory for files matching a pattern, then RUNS each one it finds (as bandit24) before deleting it. If you can predict or control that pattern, you can place your own script where the cron job will pick it up and execute it with bandit24's privileges.", 562),
        ("Read the cron script under `/etc/cron.d/` (as bandit22) to see exactly which directory it scans and what naming pattern qualifies a file to be executed. Write a small script of your own into that directory matching the pattern -- one that copies `/etc/bandit_pass/bandit24` somewhere you (bandit23) can read, e.g. into `/tmp` -- make it executable, and wait a minute for the next cron sweep to run it for you.", 837),
    ],
    "bandit-24": [
        ("`man nc`.", 70),
        ("10,000 possible 4-digit PINs is small enough to try every single one programmatically in well under a minute -- a shell loop can generate every PIN from 0000 through 9999 and pipe each attempt, one per line, into a single netcat connection.", 650),
        ("A brute-force loop, e.g. in bash: `for pin in $(seq -w 0 9999); do echo <bandit24-password> $pin; done | nc -q1 localhost 30002 > /tmp/results.txt`, then `grep -v Wrong /tmp/results.txt` to filter out every failed attempt and surface the one real response containing bandit25's password. (`-q1` tells netcat to close shortly after input ends, so it doesn't hang waiting on the socket forever.)", 975),
    ],
    "bandit-25": [
        ("`man more`.", 70),
        ("bandit26's shell is set up to display one short file with a pager (`more`) and then immediately exit. On a normal, tall terminal `more` shows the whole file at once and exits before you can act -- but `more` pauses with an interactive `--More--` prompt once the file is too long to fit on screen, which you can force by shrinking your terminal window to just a few lines before connecting.", 650),
        ("`grep bandit26 /etc/passwd` (from bandit25) confirms the unusual shell. Shrink your terminal to just a handful of rows, then `ssh bandit26@<host> -p <port>` with bandit25's password -- `more` will pause on `--More--` instead of exiting immediately. From that prompt, pressing `v` launches an editor (vi) on the file being paged, which is a real, escapable program -- continue from there in the next level.", 975),
    ],
    "bandit-26": [
        ("`man vi`.", 75),
        ("Once `v` has opened the paged file in vi (from the previous level's escape), you're in a real, general-purpose text editor -- and like most editors, it has a documented (if power-user) command for shelling out to run external programs, which can be used to spawn a real login shell.", 675),
        ("From inside vi (reached via `v` at `more`'s `--More--` prompt), type `:set shell=/bin/bash` followed by `:shell` (or simply `:!/bin/bash`) -- this spawns a real, unrestricted bash shell as bandit26. From there, explore the filesystem normally (`ls`, `find`, `cat`) to locate and read the flag file.", 1050),
    ],
    "bandit-27": [
        ("`man git-clone`.", 75),
        ("This is a real git repository, reachable the same way any private git repo over SSH would be -- `git clone` accepts an `ssh://` URL just like any other remote, authenticating the same way a normal SSH login would.", 675),
        ("`git clone ssh://bandit27-git@<host>:<port>/home/bandit27-git/repo` (substituting your instance's real host/port), entering bandit27's password when prompted. Once cloned, `cd repo` and look at the files it checked out (e.g. `cat README.md`) -- the next password is right there in the working tree.", 1050),
    ],
    "bandit-28": [
        ("`man git-log`.", 80),
        ("Git keeps a full history: deleting or editing something in a later commit does NOT remove it from earlier commits, which remain fully readable forever unless deliberately rewritten. `git log` has a documented flag for showing the actual line-by-line change each commit made, not just its message.", 700),
        ("Clone the repo, then run `git log -p` inside it to see every historical change in full, not just the latest state. Scroll (or search) through the diff output for an earlier version of the file that still shows the real password before it was edited out.", 1125),
    ],
    "bandit-29": [
        ("`man git-branch`.", 80),
        ("A git repository can have multiple branches -- independent lines of development -- and checking out the default branch only shows you ONE of them. `git branch` has a documented flag for listing every branch, not just the checked-out one.", 700),
        ("Clone the repo, then `git branch -a` to list every branch (including ones not checked out locally by default). `git checkout <branch-name>` for each one you find and look through its files -- the real password is in a file on a non-default branch.", 1125),
    ],
    "bandit-30": [
        ("`man git-tag`.", 85),
        ("Besides commits and branches, git supports tags -- often used to mark releases or other significant points -- which can point at a state of the repo that never made it onto any branch's current tip.", 750),
        ("Clone the repo, then `git tag` to list any tags. `git show <tagname>` displays what that tag points at (and its own message, if any) -- the password is attached to a tag rather than living in any branch's current files.", 1200),
    ],
    "bandit-31": [
        ("`man git-push`.", 85),
        ("This level isn't about finding something already in the repo -- it wants you to ADD something and push it back. Reading the repository's own README first is essential here: it spells out precisely what file, name, and content it's checking for, and git won't accept just anything.", 750),
        ("Clone the repo and `cat README.md` (or similar) for the exact filename and content it demands (in this deployment, a specific short message in a specific filename). Create that exact file, then `git add <file>`, `git commit -m '...'`, and `git push origin master` (or `main`, matching the repo's default branch) -- the push itself, if it satisfies the stated requirement, reveals or returns the next password.", 1200),
    ],
    "bandit-32": [
        ("`man bash`.", 90),
        ("The uppercase wrapper only transforms LOWERCASE letters before evaluating your input -- anything that isn't a lowercase letter (digits, symbols, punctuation) passes through completely untouched. Bash's manual documents what a bare `$0` evaluates to, and how that value is affected by how the enclosing shell itself was launched.", 850),
        ("Typing `$0` at the UPPERCASE-shell prompt survives the `tr 'a-z' 'A-Z'` transform untouched (it contains no lowercase letters at all) and gets evaluated as-is. Because this wrapper shell was itself launched via `bash -c '...'`, `$0` inside that context defaults to the literal string `bash` -- so evaluating `$0` spawns a fresh, completely unrestricted bash shell, breaking you out of the uppercase loop entirely.", 1275),
    ],
    "bandit-33": [
        ("`man find`.", 90),
        ("This final shell only allows a couple of harmless-looking tools on its PATH and blocks you from directly naming a command that contains a `/` -- but that restriction applies to what YOU type at the prompt, not to what an ALLOWED program does internally. `find`'s manual documents an action that launches an arbitrary program of your choosing.", 875),
        ("`find` is one of the few tools available in this restricted shell, and its `-exec` action can launch an arbitrary program -- rbash's restrictions apply to what you type at the prompt, not to what an allowed program execs on your behalf. Running `find . -exec /bin/sh \\\\;` (the trailing backslash-semicolon terminates the -exec clause) launches a real, unrestricted `/bin/sh` via `find`, sidestepping the restricted shell entirely. That new shell still inherits the old restricted PATH though -- unlike the rbash you just escaped, this one actually lets you reassign it (`PATH=/usr/bin:/bin` then `export PATH`), after which normal commands like `cat` work again to find the final flag.", 1312),
    ],
}

# Generate folder and files relative to the repo root folder dynamically
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(script_dir, "..", "challenges"))
os.makedirs(base_dir, exist_ok=True)

for i, ch in enumerate(challenges_data):
    folder_path = os.path.join(base_dir, ch["id"])
    os.makedirs(folder_path, exist_ok=True)

    full_desc = ch["desc"]
    extra_info = EXTRA_INFO.get(ch["id"])
    if extra_info:
        cmds, reading = extra_info
        if cmds:
            cmd_list = ", ".join(f"`{c}`" for c in cmds)
            full_desc += f"\n\n**Commands you may need to solve this level:** {cmd_list}"
        if reading:
            links = "\n".join(f"- [{title}]({url})" for title, url in reading)
            full_desc += f"\n\n**Helpful reading:**\n{links}"

    escaped_desc = full_desc.replace('\n', '\n  ')
    is_final_level = (i == len(challenges_data) - 1)
    yaml_content = f"""name: "{ch['name']}"
author: "CEI Labs (self-hosted recreation of OverTheWire's Bandit)"
category: "Linux Basics"
description: |
  {escaped_desc}
value: {ch['points']}
type: standard
flags:
{_flags_yaml(ch['flag'])}state: visible
version: "0.1"
instance_type: single-target
image: {BANDIT_IMAGE}
instance_group: {INSTANCE_GROUP}
shutdown_on_solve: {"true" if is_final_level else "false"}
show_launcher: {"true" if ch["id"] == "bandit-start-here" else "false"}
"""

    hint = HINTS.get(ch["id"])
    if hint:
        # A HINTS entry is either one (content, cost) tuple (legacy,
        # single-tier) or a list of them (crawl/walk/run, multiple tiers,
        # cheapest first) -- normalize to a list either way.
        tiers = hint if isinstance(hint, list) else [hint]
        yaml_content += "hints:\n"
        for hint_content, hint_cost in tiers:
            yaml_content += f'  - content: "{hint_content}"\n    cost: {hint_cost}\n'

    file_path = os.path.join(folder_path, "challenge.yml")
    with open(file_path, "w") as f:
        f.write(yaml_content)

print(f"Successfully generated {len(challenges_data)} Bandit challenges inside '{base_dir}'!")
