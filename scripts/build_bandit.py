import os

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
        "flag": "NH2SXQwcBdpmTEzi3bvBHRW9NXrY9B1b"
    },
    {
        "id": "bandit-01",
        "name": "Bandit 1 -> 2: Dashed Hopes",
        "points": 150,
        "desc": "**Goal:** Read a file whose name looks like a command-line flag.\n\nLog in as `bandit1`. The next password is hidden in a file named `-` (a single dash) in the home directory.",
        "flag": "rRGizSaX8Mk1RTb1CNQoXTcYZUR6OUZY"
    },
    {
        "id": "bandit-02",
        "name": "Bandit 2 -> 3: Spaces in Places",
        "points": 200,
        "desc": "**Goal:** Read a file whose name contains spaces.\n\nLog in as `bandit2`. The next password is in a file called `spaces in this filename`, in the home directory.",
        "flag": "aBZ0W5EmUfAf7kHTQeOwd8bauFJ2lEWG"
    },
    {
        "id": "bandit-03",
        "name": "Bandit 3 -> 4: Hidden in Plain Sight",
        "points": 250,
        "desc": "**Goal:** Find a hidden (dotfile) password.\n\nLog in as `bandit3`. The next password is hidden inside the `inhere` directory -- you'll need to show hidden files to find it.",
        "flag": "2EW7BBsr6aMMoJ2HjW067zg8WNkNzbpm"
    },
    {
        "id": "bandit-04",
        "name": "Bandit 4 -> 5: Human Readable",
        "points": 300,
        "desc": (
            "**Goal:** The password for the next level is stored in one of the files in the `inhere` directory. "
            "It is the only file that contains human-readable text.\n\n"
            "**Commands you may need to solve this level:** `ls`, `cd`, `cat`, `file`, `find`\n\n"
            "**Helpful reading:** [The file command (Wikipedia)](https://en.wikipedia.org/wiki/File_%28command%29)"
        ),
        "flag": "lrIWWI6bB37kxfiCQZqUdOIYfr6eEeqR"
    },
    {
        "id": "bandit-05",
        "name": "Bandit 5 -> 6: The Needle",
        "points": 350,
        "desc": "**Goal:** Find one specific file among many nested decoys.\n\nLog in as `bandit5`. Somewhere under `inhere` (which has subdirectories) is a file matching all three properties:\n1. Human-readable\n2. Exactly 1033 bytes in size\n3. Not executable",
        "flag": "P4L4vucdmLnm8I7Vl7jG1ApGSfjYKqJU"
    },
    {
        "id": "bandit-06",
        "name": "Bandit 6 -> 7: Server Search",
        "points": 400,
        "desc": "**Goal:** Search the whole filesystem by owner, group, and size.\n\nLog in as `bandit6`. The next password is somewhere on the server (not necessarily under your home directory) -- owned by user `bandit7`, group `bandit6`, exactly 33 bytes.",
        "flag": "z7WtoNQU2XfjmMtWA8u5rN4vzqu4v99S"
    },
    {
        "id": "bandit-07",
        "name": "Bandit 7 -> 8: The Millionth Word",
        "points": 450,
        "desc": "**Goal:** Extract a value next to a known marker word.\n\nLog in as `bandit7`. The next password is in `data.txt`, on the same line as the word `millionth`.",
        "flag": "TESKZC0XvTetK0S9xNwm25STk5iWrBvP"
    },
    {
        "id": "bandit-08",
        "name": "Bandit 8 -> 9: The Only One",
        "points": 500,
        "desc": "**Goal:** Find the one line that appears only once in a large file.\n\nLog in as `bandit8`. The next password is the one line in `data.txt` that occurs exactly once.",
        "flag": "EN632PlfYiZbn3PhVK3XOGSlNInNE00t"
    },
    {
        "id": "bandit-09",
        "name": "Bandit 9 -> 10: Strings Attached",
        "points": 550,
        "desc": "**Goal:** Pull the readable text out of a mostly-binary file.\n\nLog in as `bandit9`. The next password is one of the few human-readable strings in `data.txt`, preceded by several `=` characters.",
        "flag": "G7w8LIi6J3kTb8O7jPdkOYOsDhmi0n0m"
    },
    {
        "id": "bandit-10",
        "name": "Bandit 10 -> 11: Base Operations",
        "points": 600,
        "desc": "**Goal:** Decode a base64-encoded password.\n\nLog in as `bandit10`. `data.txt` holds the next password encoded in base64 -- decode it.",
        "flag": "6zPeziLdR2RKNdNYFNb6nVCKzphlXHpt"
    },
    {
        "id": "bandit-11",
        "name": "Bandit 11 -> 12: Substitution",
        "points": 650,
        "desc": "**Goal:** Reverse a ROT13 substitution.\n\nLog in as `bandit11`. `data.txt` holds the next password with every letter rotated 13 positions (ROT13) -- reverse it.",
        "flag": "JVNBBFSmZwKKOP0XbFXOoW8chDz5yVRv"
    },
    {
        "id": "bandit-12",
        "name": "Bandit 12 -> 13: Matryoshka",
        "points": 700,
        "desc": "**Goal:** Unwrap several layers of hexdump and compression.\n\nLog in as `bandit12`. `data.txt` is a hexdump of a file that's been compressed multiple times. Revert the hexdump, then decompress repeatedly (gzip, bzip2, tar -- the file type at each step tells you which) to reach the password.",
        "flag": "wbWdlBxEir4c8X3x5l9m5o5Wv8n9Uj4J"
    },
    {
        "id": "bandit-13",
        "name": "Bandit 13 -> 14: Private Keys",
        "points": 750,
        "desc": "**Goal:** Use a provided private key to log in as another account.\n\nLog in as `bandit13`. Use the provided private SSH key (`sshkey.private`, in the home directory) to log into `bandit14` on localhost, then read the password from `/etc/bandit_pass/bandit14`.",
        "flag": "fGrHPx402xGC7U7rXKDaxiWFTOiF0ENq"
    },
    {
        "id": "bandit-14",
        "name": "Bandit 14 -> 15: Port Submission",
        "points": 800,
        "desc": "**Goal:** Submit a password to a listening TCP service.\n\nLog in as `bandit14`. Submit the current password to **port 30000 on localhost** to receive the next one.",
        "flag": "jN2kgmIXJ6fShzhT2avhotn4Zcka6tnt"
    },
    {
        "id": "bandit-15",
        "name": "Bandit 15 -> 16: SSL Encryption",
        "points": 850,
        "desc": "**Goal:** Submit a password over a TLS-encrypted connection.\n\nLog in as `bandit15`. Submit the current password to **port 30001 on localhost**, this time over SSL/TLS.",
        "flag": "JQttfApK4SeyHwDlI9SXGR50qclOAil1"
    },
    {
        "id": "bandit-16",
        "name": "Bandit 16 -> 17: SSL Port Scan",
        "points": 900,
        "desc": "**Goal:** Find the one correct service among a range of listening ports.\n\nLog in as `bandit16`. The next credentials come from submitting the current password to the right port somewhere in the range **31000-32000 on localhost** -- scan the range to find which one actually wants it.",
        "flag": "VwOSWtCAcEBcCU5TOk540Rh04UvwB1O8"
    },
    {
        "id": "bandit-17",
        "name": "Bandit 17 -> 18: File Comparisons",
        "points": 950,
        "desc": "**Goal:** Diff two large, nearly-identical files.\n\nLog in as `bandit17`. The home directory has `passwords.old` and `passwords.new`. The next password is on the one line that changed between them.",
        "flag": "kfBf3eYk5BPBRzwjqutbbfE887SVc5ac"
    },
    {
        "id": "bandit-18",
        "name": "Bandit 18 -> 19: Shell Bypass",
        "points": 1000,
        "desc": "**Goal:** Read a file without getting an interactive shell.\n\nLog in as `bandit18` -- this account's `.bashrc` has been modified to log you out immediately on interactive login. Find a way to still read the `readme` file in its home directory.",
        "flag": "IueksS7Ubh8G3DXwAFbnnjJ1XWeqro5r"
    },
    {
        "id": "bandit-19",
        "name": "Bandit 19 -> 20: SUID Escalation",
        "points": 1050,
        "desc": "**Goal:** Use a setuid binary to read a file you otherwise couldn't.\n\nLog in as `bandit19`. The home directory has a setuid binary -- use it to reach the next password.",
        "flag": "GbKksEFF4yrVs6il55v6gwY5aVje5f0j"
    },
    {
        "id": "bandit-20",
        "name": "Bandit 20 -> 21: Port Listener Connection",
        "points": 1100,
        "desc": "**Goal:** Have a setuid binary connect back to a listener you control.\n\nLog in as `bandit20`. The home directory has a setuid binary that connects to a port on localhost you supply as an argument, reads a line, and checks it against the current password. Set up a listener of your own first, then trigger the connection.",
        "flag": "gE269g2h3mw3pwgrj0LuIpTpNcfS1KMc"
    },
    {
        "id": "bandit-21",
        "name": "Bandit 21 -> 22: Cron Jobs",
        "points": 1150,
        "desc": "**Goal:** Read what a cron job does and follow it to the password.\n\nLog in as `bandit21`. A job runs automatically on a schedule via cron -- check `/etc/cron.d/` for the configuration and see where it leads.",
        "flag": "Yk7oeL4H2E45qp7Z9EaA8F4e8G4Z5Jj7"
    },
    {
        "id": "bandit-22",
        "name": "Bandit 22 -> 23: Cron Debugging",
        "points": 1200,
        "desc": "**Goal:** Trace a cron job to the script it actually runs.\n\nLog in as `bandit22`. Same starting point as before (`/etc/cron.d/`), but this time you'll need to find and read the script the job executes to see where it writes the password.",
        "flag": "jc1udXDznI2mD8tE8Zq2P17ZtGv6z5M0"
    },
    {
        "id": "bandit-23",
        "name": "Bandit 23 -> 24: Cron Scripting",
        "points": 1250,
        "desc": "**Goal:** Write your own script for a cron job to run on your behalf.\n\nLog in as `bandit23`. This cron job runs whatever script matches a pattern you can influence -- write your own to copy out the password.",
        "flag": "UoMYTrfrBFHyQXmg6R1YI7mIfUIna55J"
    },
    {
        "id": "bandit-24",
        "name": "Bandit 24 -> 25: PIN Brute Force",
        "points": 1300,
        "desc": "**Goal:** Brute-force a 4-digit PIN against a listening daemon.\n\nLog in as `bandit24`. A daemon on port 30002 returns the next password if you send it the current password plus the correct 4-digit PIN -- script the brute force.",
        "flag": "uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG"
    },
    {
        "id": "bandit-25",
        "name": "Bandit 25 -> 26: Shell Breakout",
        "points": 1350,
        "desc": "**Goal:** Escape a restricted, non-bash login shell.\n\nLog in as `bandit25`. Account `bandit26`'s login shell isn't `/bin/bash` -- find out what it actually is and how to break out of it into a real shell.",
        "flag": "5czgV9L3Xx8JPOyU3jO5B9I0A3bM9E3z"
    },
    {
        "id": "bandit-26",
        "name": "Bandit 26 -> 27: Text UI Breakout",
        "points": 1400,
        "desc": "**Goal:** Break out of a terminal pager into a shell.\n\nLog in as `bandit26` (this account's shell pages a short file and exits immediately -- shrinking your terminal window before connecting buys you a window to act in). Once you've broken out, look around the filesystem to find the flag.",
        "flag": "3ba3118a22e93127a4ed485be72ef5ea"
    },
    {
        "id": "bandit-27",
        "name": "Bandit 27 -> 28: Git Clone",
        "points": 1450,
        "desc": "**Goal:** Clone a git repository and find a password committed to it.\n\nA repository is reachable at `ssh://bandit27-git@<your-instance-host>/home/bandit27-git/repo` (use the SSH port your launch panel shows). Log in with `bandit27`'s own password (the previous level's flag), clone it, and find the next password.",
        "flag": "0ef186ac70e04ea33b4c1853d2526fa2"
    },
    {
        "id": "bandit-28",
        "name": "Bandit 28 -> 29: Git Commits",
        "points": 1500,
        "desc": "**Goal:** Find a secret that was committed and later removed.\n\nRepository: `ssh://bandit28-git@<your-instance-host>/home/bandit28-git/repo`, login with `bandit28`'s own password. Clone it and check the commit history -- the current tree isn't the only place a password could have been.",
        "flag": "bbc96594b4e001778eee9975372716b2"
    },
    {
        "id": "bandit-29",
        "name": "Bandit 29 -> 30: Git Branches",
        "points": 1550,
        "desc": "**Goal:** Find a secret that only exists on a non-default branch.\n\nRepository: `ssh://bandit29-git@<your-instance-host>/home/bandit29-git/repo`, login with `bandit29`'s own password. Clone it and check every branch, not just the default.",
        "flag": "5b90576ed34ce8c56ad62351ab66e47c"
    },
    {
        "id": "bandit-30",
        "name": "Bandit 30 -> 31: Git Tags",
        "points": 1600,
        "desc": "**Goal:** Find a secret attached to a git tag.\n\nRepository: `ssh://bandit30-git@<your-instance-host>/home/bandit30-git/repo`, login with `bandit30`'s own password. Clone it and check the tags.",
        "flag": "47e603bb428404d265f59c42920d81e5"
    },
    {
        "id": "bandit-31",
        "name": "Bandit 31 -> 32: Git Push",
        "points": 1650,
        "desc": "**Goal:** Satisfy a repository's own stated requirements to earn the next password.\n\nRepository: `ssh://bandit31-git@<your-instance-host>/home/bandit31-git/repo`, login with `bandit31`'s own password. Clone it, read the README for the exact requirements, then push a file that meets them to receive the password.",
        "flag": "56a9bf19c63d650ce78e6ec0354ee45e"
    },
    {
        "id": "bandit-32",
        "name": "Bandit 32 -> 33: Shell Overrides",
        "points": 1700,
        "desc": "**Goal:** Reach a real shell from one that mangles every command you type.\n\nLog in as `bandit32` -- this account's shell uppercases every command before running it. Find a way around that limitation to reach a normal shell, then locate the next password.",
        "flag": "c9c3199ddf4121b10fb58bb24580d440"
    },
    {
        "id": "bandit-33",
        "name": "Bandit 33 -> 34: Final Escape",
        "points": 1750,
        "desc": "**Goal:** One last escape to finish the track.\n\nLog in as `bandit33`. After all that git work, it's time for one more escape. Good luck.",
        "flag": "OdqthX2eZq2fFft2q3B5mJz7eIq3Zk2d"
    }
]

# One real, technique-specific hint per level (not bandit-start-here --
# its description is already a full walkthrough). Cost scales roughly
# with the level's own point value; content must not contain a literal
# double-quote character (this script builds YAML by hand, not via
# PyYAML, so the hint text is interpolated straight into a double-quoted
# YAML scalar below -- use backticks/single quotes for anything that
# needs quoting).
HINTS = {
    "bandit-00": ("Connect with `ssh bandit0@<host> -p <port>`, password `bandit0`, then `cat readme`.", 5),
    "bandit-01": ("A leading dash looks like an option to most commands. Reference it as `./-` or `cat -- -` instead.", 10),
    "bandit-02": ("Quote the whole filename: `cat 'spaces in this filename'`.", 15),
    "bandit-03": ("`ls -la inhere` -- dotfiles never show up in a plain `ls`.", 15),
    # bandit-04: SAMPLE for the new 3-tier crawl/walk/run hint format --
    # a list of (content, cost) tiers instead of a single tuple. Tier 1 is
    # near-free (a tool pointer, same spirit as OTW's own "Commands you
    # may need" list); tier 2 costs half the challenge's points for a real
    # technique explanation; tier 3 costs most of the points for something
    # close to a full walkthrough, condensed from real internet writeups
    # (see https://mayadevbe.me/posts/overthewire/bandit/level5/ and
    # https://sysadmin-central.com/2021/07/08/overthewire-bandit-level-4-solution/).
    "bandit-04": [
        ("`man file` -- it identifies a file's actual content type, independent of what it's named.", 5),
        ("Run `file ./inhere/*` to check every file in the directory in one command. Most will report as generic 'data'; exactly one will report as some form of text.", 150),
        ("Full method: `cd inhere`, then `file ./*` (or `file -- *` if any names start with a dash) to see every file's real type in one pass -- the decoys are named to look identical, but `file` reads actual bytes, not names. The binary ones will report as 'data'; exactly one will report as ASCII/text. Once you've spotted that filename, `cat` it (quoting or escaping the name if it starts with a dash) to read the password.", 225),
    ],
    "bandit-05": ("Chain the three properties in one `find`: `find inhere -size 1033c -type f ! -executable`, then `file` whatever it returns.", 20),
    "bandit-06": ("`find / -user bandit7 -group bandit6 -size 33c 2>/dev/null` -- redirect stderr so permission-denied noise doesn't bury the real result.", 25),
    "bandit-07": ("`grep millionth data.txt`.", 25),
    "bandit-08": ("`sort data.txt | uniq -u` prints only the lines with no duplicates.", 30),
    "bandit-09": ("`strings data.txt | grep '^='` filters to the human-readable lines that start with the marker.", 30),
    "bandit-10": ("`base64 -d data.txt`.", 35),
    "bandit-11": ("`tr 'A-Za-z' 'N-ZA-Mn-za-m' < data.txt` -- ROT13 is its own inverse.", 35),
    "bandit-12": ("Copy data.txt somewhere writable, `xxd -r` it back to binary, then run `file` after every decompression step to know what to run next.", 40),
    "bandit-13": ("`chmod 600 sshkey.private` if SSH complains about permissions, then `ssh -i sshkey.private bandit14@localhost`.", 40),
    "bandit-14": ("`nc localhost 30000`, then type the current password and press enter.", 45),
    "bandit-15": ("`openssl s_client -connect localhost:30001` opens the encrypted connection; type the password once it's up.", 45),
    "bandit-16": ("`nmap -p 31000-32000 localhost` first, to see which port(s) in the range are even open, before trying SSL against each.", 50),
    "bandit-17": ("`diff passwords.old passwords.new`.", 50),
    "bandit-18": ("Skip the interactive shell entirely: `ssh bandit18@host -p port cat readme` runs one command over SSH without ever sourcing `.bashrc`.", 55),
    "bandit-19": ("`./bandit20-do cat /etc/bandit_pass/bandit20` -- quote the whole command as one argument.", 55),
    "bandit-20": ("Start a listener first (`nc -lvp <port>`) in one session, then trigger the setuid binary with that same port from another.", 60),
    "bandit-21": ("`cat /etc/cron.d/*`.", 60),
    "bandit-22": ("`cat /etc/cron.d/*` for the schedule, then `cat` the script path it points to.", 65),
    "bandit-23": ("Read the cron script closely -- it runs anything matching a glob pattern in a world-writable temp directory. Drop your own script there.", 65),
    "bandit-24": ("Script the brute force: loop PIN 0000-9999, sending `CURRENT_PASSWORD PIN` to port 30002 each time and checking the response.", 70),
    "bandit-25": ("`grep bandit26 /etc/passwd` shows the shell. Shrink your terminal small before connecting so its pager can't display everything and drops you to its own prompt.", 70),
    "bandit-26": ("Most pagers accept a shell-escape from their own command prompt (commonly `!` followed by a shell, e.g. `!/bin/sh`).", 75),
    "bandit-27": ("`git clone ssh://bandit27-git@<host>:<port>/home/bandit27-git/repo`.", 75),
    "bandit-28": ("`git log -p` -- the password isn't in the current tree, only in an earlier commit.", 80),
    "bandit-29": ("`git branch -a`, then `git checkout` each one you find.", 80),
    "bandit-30": ("`git tag`, then `git show <tagname>`.", 85),
    "bandit-31": ("`cat README` inside the clone for the exact filename it wants, then `git add`, `git commit`, `git push origin master`.", 85),
    "bandit-32": ("The wrapper only uppercases what it reads as a command line -- a direct shell invocation via a different mechanism (find a way to spawn `/bin/bash` that bypasses the wrapper reading it) sidesteps it entirely.", 90),
    "bandit-33": ("Same family of problem as bandit25/26: identify the restricted shell bandit33 lands you in, then break out of it the same way.", 90),
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
author: "CEI Labs (self-hosted recreation of OverTheWire's Bandit)"
category: "Linux Basics"
description: |
  {escaped_desc}
value: {ch['points']}
type: standard
flags:
  - "{ch['flag']}"
state: visible
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
