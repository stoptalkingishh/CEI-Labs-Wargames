import os
import json

from hint_economy import managed_tiers


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
BANDIT_IMAGE = os.environ.get(
    "BANDIT_IMAGE",
    "ghcr.io/stoptalkingishh/cei-labs-wargames/bandit-target:latest",
)

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

# Shown once, in bandit-start-here only -- every later level assumes the
# player already knows how to open a terminal and run `ssh`, so repeating
# this per-level would just be noise. Every app name here is plain text,
# deliberately not a clickable link: this venue's network has no internet
# access during the event (see docs/offline-dependency-audit.md, the same
# reason EXTRA_INFO's own reading-material links are plain titles, not
# URLs) -- a player installs an app on their own device beforehand, over
# their own connection, not from inside the venue.
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
            + SSH_CONNECT_GUIDE +
            "\n\nClick Launch, wait for it to show a Host and Port, then connect as `bandit0` "
            "with password `bandit0`. The moment you log in, a banner prints automatically -- "
            "no file to go read, it's already on your screen. Its last three lines are an "
            "acceptable-use notice; the middle one is about not using AI or outside "
            "tools/services to cheat. Copy that exact line, word for word (punctuation "
            "included), and submit it as your flag -- proof you actually read it, not just "
            "that you connected."
        ),
        "flag": "Do not use AI or external tools/services to cheat or obtain answers."
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
        "desc": "**Goal:** Recover the password from the `inhere` directory.\n\nLog in as `bandit3`. The next password is in a file inside the `inhere` directory in your home folder -- but it doesn't show up in an ordinary listing. Work out how to reveal it (the hints walk you through it if you get stuck).",
        "flag": {"type": "per_team_dynamic_fixed", "content": "per-team-dynamic (placeholder, not read)", "data": "bandit3"}
    },
    {
        "id": "bandit-04",
        "name": "Bandit 4 -> 5: Human Readable",
        "points": 300,
        "desc": "**Goal:** The password for the next level is stored in one of the files in the `inhere` directory. It is the only file that contains human-readable text. Log in as `bandit4`.",
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
    "bandit-00": (["ls", "cd", "cat", "file", "du", "find"], []),
    "bandit-01": (["ls", "cd", "cat", "file", "du", "find"], [("Google Search for \"dashed filename\"", "https://www.google.com/search?q=dashed+filename"), ("Advanced Bash-Scripting Guide -- Special Characters", "https://linux.die.net/abs-guide/special-chars.html")]),
    "bandit-02": (["ls", "cd", "cat", "file", "du", "find"], [("Google Search for \"spaces in filename\"", "https://www.google.com/search?q=spaces+in+filename")]),
    "bandit-03": (["ls", "cd", "cat", "file", "du", "find"], []),
    "bandit-04": (["ls", "cd", "cat", "file", "du", "find"], []),
    "bandit-05": (["ls", "cd", "cat", "file", "du", "find"], []),
    "bandit-06": (["ls", "cd", "cat", "file", "du", "find", "grep"], []),
    "bandit-07": (["man", "grep", "sort", "uniq", "strings", "base64", "tr", "tar", "gzip", "bzip2", "xxd"], []),
    "bandit-08": (["grep", "sort", "uniq", "strings", "base64", "tr", "tar", "gzip", "bzip2", "xxd"], [("Piping and Redirection", "https://ryanstutorials.net/linuxtutorial/piping.php")]),
    "bandit-09": (["grep", "sort", "uniq", "strings", "base64", "tr", "tar", "gzip", "bzip2", "xxd"], []),
    "bandit-10": (["grep", "sort", "uniq", "strings", "base64", "tr", "tar", "gzip", "bzip2", "xxd"], [("Base64 on Wikipedia", "https://en.wikipedia.org/wiki/Base64")]),
    "bandit-11": (["grep", "sort", "uniq", "strings", "base64", "tr", "tar", "gzip", "bzip2", "xxd"], [("ROT13 on Wikipedia", "https://en.wikipedia.org/wiki/ROT13")]),
    "bandit-12": (["grep", "sort", "uniq", "strings", "base64", "tr", "tar", "gzip", "bzip2", "xxd", "mkdir", "cp", "mv", "file"], [("Hex dump on Wikipedia", "https://en.wikipedia.org/wiki/Hex_dump")]),
    "bandit-13": (["ssh", "scp", "umask", "chmod", "cat", "nc", "install"], [("SSH/OpenSSH/Keys", "https://help.ubuntu.com/community/SSH/OpenSSH/Keys"), ("Transferring Files via SCP", "https://help.ubuntu.com/community/SSH/TransferFiles")]),
    "bandit-14": (["ssh", "telnet", "nc", "openssl", "s_client", "nmap"], [("How the Internet works in 5 minutes (YouTube)", "https://www.youtube.com/watch?v=7_LPdttKXPc"), ("IP Addresses", "https://computer.howstuffworks.com/web-server5.htm"), ("IP Address on Wikipedia", "https://en.wikipedia.org/wiki/IP_address"), ("Localhost on Wikipedia", "https://en.wikipedia.org/wiki/Localhost"), ("Ports", "https://computer.howstuffworks.com/web-server8.htm"), ("Port (computer networking) on Wikipedia", "https://en.wikipedia.org/wiki/Port_(computer_networking)")]),
    "bandit-15": (["ssh", "telnet", "nc", "ncat", "socat", "openssl", "s_client", "nmap", "netstat", "ss"], [("Secure Socket Layer/Transport Layer Security on Wikipedia", "https://en.wikipedia.org/wiki/Transport_Layer_Security"), ("OpenSSL Cookbook -- Testing with OpenSSL", "https://www.feistyduck.com/library/openssl-cookbook/online/testing-with-openssl/index.html")]),
    "bandit-16": (["ssh", "telnet", "nc", "ncat", "socat", "openssl", "s_client", "nmap", "netstat", "ss"], [("Port scanner on Wikipedia", "https://en.wikipedia.org/wiki/Port_scanner")]),
    "bandit-17": (["cat", "grep", "ls", "diff"], []),
    "bandit-18": (["ssh", "ls", "cat"], []),
    "bandit-19": ([], [("Setuid on Wikipedia", "https://en.wikipedia.org/wiki/Setuid")]),
    "bandit-20": (["ssh", "nc", "cat", "bash", "screen", "tmux", "Unix 'job control' (bg, fg, jobs, &, CTRL-Z, ...)"], []),
    "bandit-21": (["cron", "crontab", "crontab(5)"], []),
    "bandit-22": (["cron", "crontab", "crontab(5)"], []),
    "bandit-23": (["chmod", "cron", "crontab", "crontab(5)"], []),
    "bandit-24": ([], []),
    "bandit-25": (["ssh", "cat", "more", "vi", "ls", "id", "pwd"], []),
    "bandit-26": (["ls"], []),
    "bandit-27": (["git"], [("Installing Git", "https://git-scm.com/book/en/v2/Getting-Started-Installing-Git"), ("Git from the Bottom Up", "https://jwiegley.github.io/git-from-the-bottom-up/")]),
    "bandit-28": (["git"], [("Installing Git", "https://git-scm.com/book/en/v2/Getting-Started-Installing-Git"), ("Git from the Bottom Up", "https://jwiegley.github.io/git-from-the-bottom-up/")]),
    "bandit-29": (["git"], [("Installing Git", "https://git-scm.com/book/en/v2/Getting-Started-Installing-Git"), ("Git from the Bottom Up", "https://jwiegley.github.io/git-from-the-bottom-up/")]),
    "bandit-30": (["git"], [("Installing Git", "https://git-scm.com/book/en/v2/Getting-Started-Installing-Git"), ("Git from the Bottom Up", "https://jwiegley.github.io/git-from-the-bottom-up/")]),
    "bandit-31": (["git"], [("Installing Git", "https://git-scm.com/book/en/v2/Getting-Started-Installing-Git"), ("Git from the Bottom Up", "https://jwiegley.github.io/git-from-the-bottom-up/")]),
    "bandit-32": (["sh", "man"], []),
    "bandit-33": (["find", "sh"], []),
}

# Crawl/walk/run hints per level (not bandit-start-here -- its
# description is already a full walkthrough). A HINTS entry is a list of
# exactly 3 hint-text strings, cheapest/least-revealing first. There is no
# authored cost here -- managed_tiers() (scripts/hint_economy.py) prices
# every tier exclusively from tier_costs(value), so a hand-typed number
# would never be read and would only mislead future editors:
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
    'bandit-00': [
        "Working with a remote CTF box, your very first job is just getting logged in remotely at all -- every step after this happens over that same kind of remote connection. What's the standard, secure way to open a command-line session on another machine over a network?",
        "SSH (Secure Shell) is the standard tool for this: it opens an encrypted remote login session on another machine, and once you're in, everyday commands like `ls` and `cat` behave exactly like they would locally. All you need is the target's address, a port number if it's non-standard, a username, and a password.",
        "Connect with `ssh <user>@<host> -p <port>`, enter the password when prompted, then once logged in, run `cat readme` -- whatever it prints is the flag.\n\nIllustrative example only -- your real host/port and the printed value will differ:\n```\n$ ssh bandit0@<host> -p <port>\nbandit0@<host>'s password:\nbandit0@bandit:~$ cat readme\n<the next password, a long random-looking string>\n```",
    ],
    'bandit-01': [
        "There's a file in your home directory, but its name is just a single dash -- a character with a special meaning to most command-line tools. That special meaning might get in the way of simply reading the file normally.",
        "A bare `-` is a widely-used convention meaning 'read from standard input' rather than a real filename, so tools like `cat` treat a lone `-` argument specially instead of looking for a file with that literal name. Giving the tool an explicit path, even a very short one, sidesteps that special meaning entirely and tells it 'this is definitely a filename, not the special dash.'",
        "From the home directory, `cat ./-` reads the file: `./` makes the dash part of a path, so `cat` doesn't treat it as standard input.\n\nIllustrative example only -- your real value will differ:\n```\nbandit1@bandit:~$ ls\n-\nbandit1@bandit:~$ cat ./-\n<the next password>\n```",
    ],
    'bandit-02': [
        "The file you need has spaces right in its name -- and on a command line, a space is normally what separates one argument from the next. How do you tell a tool that several words joined by spaces are actually all ONE filename?",
        "Shells offer a couple of ways to make a filename with spaces count as a single argument: wrapping the whole name in quotes, or putting a backslash directly before each individual space. Either way, the quotes/backslashes are shell syntax that gets stripped before the command runs -- they aren't literally part of the file's actual name.",
        "Use `ls` to see the exact filename, then pass that whole name to `cat` as one argument, wrapped in single quotes.\n\nIllustrative example only -- your real filename/value will differ:\n```\nbandit2@bandit:~$ ls\nspaces in this filename\nbandit2@bandit:~$ cat 'spaces in this filename'\n<the next password>\n```",
    ],
    'bandit-03': [
        "A plain directory listing doesn't necessarily show you every file that's actually there. Linux has a long-standing convention for marking a file as normally invisible to casual browsing -- is there a way to ask for everything, hidden files included?",
        "Any filename starting with a `.` is hidden from a plain listing by convention only -- it's not a real permission or protection, just something every standard tool respects by default unless told otherwise. `ls` has a flag specifically for showing hidden entries alongside the normal ones.",
        "`ls -la inhere` (the `-a` flag shows hidden entries too) reveals a dotfile. `cat` that filename directly.\n\nIllustrative example only -- your real filename/value will differ:\n```\nbandit3@bandit:~$ ls -la inhere\n-rw-r----- 1 bandit4 bandit3   33 ...hidden\nbandit3@bandit:~$ cat inhere/...hidden\n<the next password>\n```",
    ],
    'bandit-04': [
        "A folder full of similarly-named files hides one real, human-readable file among several decoys. A file's NAME doesn't have to reflect what kind of data is actually inside it -- is there a way to check a file's real content type directly, rather than guessing from how it's named?",
        "`file` identifies a file's actual content type by reading its bytes, completely independent of its filename. Running it against every candidate at once, rather than one by one, is the fast way to spot which single file reports back as readable text instead of raw, meaningless `data`.",
        "`cd inhere`, then `file ./*` inspects every candidate in one pass. The decoys report as `data`; find the one ASCII/text result and `cat` that path.\n\nIllustrative example only -- your real filenames/value will differ:\n```\nbandit4@bandit:~/inhere$ file ./*\n./-file07: ASCII text\nbandit4@bandit:~/inhere$ cat ./-file07\n<the next password>\n```",
    ],
    'bandit-05': [
        "This time the real file is buried somewhere inside a maze of nested subdirectories, not sitting in one flat folder. You already know a few specific facts about it though: its exact size, that it's a regular file, and that it's human-readable rather than a program. Is there a tool built for searching an entire directory tree by criteria like that, instead of opening every folder by hand?",
        "`find` searches a whole directory tree recursively and can chain multiple filters together at once: file type, exact size in bytes, and whether or not a file is executable. Combined with `file`'s content-type check as a final filter on whatever candidates survive, you can narrow a huge tree down to exactly one match without ever opening a folder by hand.",
        "`find inhere -type f -size 1033c ! -executable -exec file '{}' \\; | grep -i ascii` applies every filter and runs `file` on the survivors, keeping only the human-readable one.\n\nIllustrative example only -- your real path/value will differ:\n```\nbandit5@bandit:~$ find inhere -type f -size 1033c ! -executable -exec file '{}' \\; | grep -i ascii\ninhere/maybehere07/.file2: ASCII text\nbandit5@bandit:~$ cat inhere/maybehere07/.file2\n<the next password>\n```",
    ],
    'bandit-06': [
        "This time the file isn't anywhere under your home directory at all -- it's somewhere on the ENTIRE filesystem. You know who owns it and what group it belongs to, though, along with its exact size. Can a search tool look across the whole filesystem using facts like ownership, not just a filename?",
        "`find` can start its search from `/`, the root of the entire filesystem, and filter by owner, group, and size all at once, not just within one folder. Searching from `/` will also try to peek into a lot of directories you don't have permission to read, which floods the output with error noise you'll want to throw away rather than read through.",
        "`find / -user bandit7 -group bandit6 -size 33c 2>/dev/null` searches everywhere for all three properties at once; `2>/dev/null` discards the permission-denied noise.\n\nIllustrative example only -- your real path/value will differ:\n```\nbandit6@bandit:~$ find / -user bandit7 -group bandit6 -size 33c 2>/dev/null\n/var/lib/dpkg/info/some-hidden-path\nbandit6@bandit:~$ cat /var/lib/dpkg/info/some-hidden-path\n<the next password>\n```",
    ],
    'bandit-07': [
        "The password is sitting somewhere inside a big file, next to a specific marker word the level names for you. Scrolling through a large file by eye to find one line isn't the efficient way to do this -- is there a tool built specifically for jumping straight to lines containing a given word?",
        "A text-search tool scans a file and prints only the lines matching whatever you ask it for, instead of you reading the whole thing. The marker word named in the goal text is exactly what you should search for -- the password sits right next to it, on that same line.",
        "`grep millionth data.txt` prints only the matching line(s) -- the password sits right beside the marker word.\n\nIllustrative example only -- your real value will differ:\n```\nbandit7@bandit:~$ grep millionth data.txt\nmillionth <the next password>\n```",
    ],
    'bandit-08': [
        "Somewhere in this file, one line appears only ONCE while every other line appears more than once. Is there a way to isolate lines by how many times they repeat, rather than searching for specific text?",
        "A tool for finding duplicate lines only catches duplicates that sit directly NEXT TO each other, so an unsorted file needs sorting first, which brings identical lines together. Once sorted, that same tool can be told to print only the lines that have NO duplicate at all, rather than the ones that do.",
        "`sort data.txt | uniq -u` sorts so identical lines become adjacent, then prints only the line that appears exactly once.\n\nIllustrative example only -- your real value will differ:\n```\nbandit8@bandit:~$ sort data.txt | uniq -u\n<the next password>\n```",
    ],
    'bandit-09': [
        "This file is mostly binary garbage, but somewhere inside it a stretch of real, human-readable text is hiding. Is there a tool that pulls out only the readable parts of an otherwise unreadable file?",
        "A tool exists for extracting just the human-readable runs of characters from a binary file, ignoring everything else. Once that readable text is visible, the goal text tells you the password is preceded by a run of `=` characters -- worth filtering the readable output down to lines that actually start with those.",
        "`strings data.txt | grep '^='` extracts readable text, then keeps only lines starting with `=` -- the password follows right after them.\n\nIllustrative example only -- your real value will differ:\n```\nbandit9@bandit:~$ strings data.txt | grep '^='\n========== <the next password>\n```",
    ],
    'bandit-10': [
        "This time the password isn't hidden behind a puzzle -- it's just written in a different, but completely standard and reversible, text format. Recognizing WHICH standard encoding it is comes down to what characters actually show up in the file.",
        "A file made up only of letters, digits, `+`, `/`, and trailing `=` padding characters is the unmistakable signature of Base64, a standard, fully reversible way of representing arbitrary bytes as plain text. Base64's own tooling has a documented flag for decoding straight back to the original data.",
        "`base64 -d data.txt` decodes the file directly back to the plaintext password.\n\nIllustrative example only -- your real value will differ:\n```\nbandit10@bandit:~$ base64 -d data.txt\n<the next password>\n```",
    ],
    'bandit-11': [
        "The text has been shifted somehow -- every letter replaced by another letter a fixed number of positions away in the alphabet. If you knew the exact shift amount, could reversing it be as simple as applying the very same shift a second time?",
        "ROT13 shifts every letter 13 places through the alphabet, wrapping around at the end. Because the alphabet has exactly 26 letters and 13 is precisely half of that, applying the identical shift a second time lands you right back where you started -- meaning encoding and decoding ROT13 are literally the same operation. A tool that performs letter-for-letter substitution given two character ranges can apply that shift directly.",
        "`tr 'A-Za-z' 'N-ZA-Mn-za-m' < data.txt` maps every letter 13 positions ahead, wrapping past Z back to A.\n\nIllustrative example only -- your real value will differ:\n```\nbandit11@bandit:~$ tr 'A-Za-z' 'N-ZA-Mn-za-m' < data.txt\n<the next password>\n```",
    ],
    'bandit-12': [
        "The file looks like a wall of hex digit pairs rather than any recognizable data -- that's a text representation of raw bytes, not the bytes themselves. And once you get back to real bytes, what's inside might not be plain text either; it could be one thing wrapped inside another.",
        "A hexdump can be converted back into the real binary bytes it represents. Once you have real bytes again, a content-identification tool can tell you what TYPE of data you're actually looking at, and if that turns out to be a compressed format, decompressing it might just reveal ANOTHER compressed format underneath, meaning this may take more than one round of 'identify, then decompress.'",
        "`xxd -r data.txt > data.bin` reverses the hexdump to real bytes. `file data.bin` shows what compression it is; decompress that layer, then run `file` again, repeating until what's left is plain text.\n\nIllustrative example only -- your real chain of compression types and value will differ:\n```\n$ file data.bin\ndata.bin: gzip compressed data\n$ mv data.bin data.gz && gunzip data.gz\n$ file data\ndata: bzip2 compressed data\n$ mv data data.bz2 && bunzip2 data.bz2\n$ file data\ndata: ASCII text\n$ cat data\n<the next password>\n```",
    ],
    'bandit-13': [
        "You have a private key file instead of a password this time. SSH supports more than one way to prove who you are -- what's the other common method, besides typing a password?",
        "SSH can authenticate you directly using a private key file instead of a password, as long as the matching public key is already trusted by the target account. SSH is also strict about that key file's permissions -- if they're too open, it will refuse to use it until you tighten them.",
        "`chmod 600 sshkey.private` first if SSH complains the permissions are too open, then `ssh -i sshkey.private bandit14@localhost` logs you into bandit14 using that key.\n\nIllustrative example only -- your real value will differ:\n```\nbandit13@bandit:~$ chmod 600 sshkey.private\nbandit13@bandit:~$ ssh -i sshkey.private bandit14@localhost\nbandit14@bandit:~$ cat /etc/bandit_pass/bandit14\n<the next password>\n```",
    ],
    'bandit-14': [
        "You need to 'submit' your current password to a service listening on a specific port. What does 'submitting' something to a port actually mean at the network level, and is there a simple tool for opening a raw connection and typing text into it directly?",
        "Netcat is the standard minimal tool for opening a raw TCP connection to a port and sending or receiving plain text through it, with no protocol of its own layered on top. Opening a connection and typing your password as a line of text is literally all 'submitting' it to a raw port means here.",
        "`nc localhost 30000` opens the connection; type bandit14's own password and press enter.\n\nIllustrative example only -- your real value will differ:\n```\nbandit14@bandit:~$ nc localhost 30000\n<type bandit14's own password, then Enter>\nCorrect!\n<the next password>\n```",
    ],
    'bandit-15': [
        "This port looks the same as the last one, but plain netcat won't get you anywhere against it. What's different about a port that expects an encrypted connection, and is there a tool that speaks that encryption?",
        "This port wraps the same interaction in SSL/TLS encryption -- plain netcat has no idea how to perform the cryptographic handshake that requires, so it just fails silently. OpenSSL, though, ships a client subcommand specifically for opening a proper encrypted connection by hand, dropping you into the session the same way netcat would once the handshake completes.",
        "`openssl s_client -connect localhost:30001` performs the handshake; once connected, type bandit15's password and press enter, same as before.\n\nIllustrative example only -- your real value will differ:\n```\nbandit15@bandit:~$ openssl s_client -connect localhost:30001 -quiet\n<type bandit15's own password, then Enter>\nCorrect!\n<the next password>\n```",
    ],
    'bandit-16': [
        "This time you're not told which exact port to connect to, just a wide range to search. Not every port in that range is even open, and among the ones that are, only one both speaks encryption AND wants your password. Is there a tool for quickly figuring out which ports in a range are actually listening, before trying each by hand?",
        "A port scanner can check a whole range at once and report back which ports actually have something listening, saving you from trying every single one manually. Many scanners can also make an educated guess at which protocol each open port is speaking, which narrows things down to the SSL-capable candidates worth trying with an encrypted client.",
        "`nmap -p 31000-32000 --open -sV localhost` lists open ports and guesses their protocol. Connect to each SSL-speaking candidate with `openssl s_client` and send bandit16's password.\n\nIllustrative example only -- your real open ports and value will differ:\n```\nbandit16@bandit:~$ nmap -p 31000-32000 --open -sV localhost\n31046/tcp open  ssl/unknown\nbandit16@bandit:~$ openssl s_client -connect localhost:31046 -quiet\n<type bandit16's own password, then Enter>\n<the next password>\n```",
    ],
    'bandit-17': [
        "You're given two large, mostly-identical files, and exactly one line differs between them. Comparing them by eye would take forever -- is there a tool built specifically for surfacing what changed between two versions of similar text?",
        "A diff tool compares two files and shows only the lines that are actually different between them, leaving everything identical out of the output entirely. Conventionally, the OLD version's differing line is marked one way and the NEW version's differing line another -- the new, current value is the one you want.",
        "`diff passwords.old passwords.new` prints only the differing lines. The `>`-marked line is the current password.\n\nIllustrative example only -- your real value will differ:\n```\nbandit17@bandit:~$ diff passwords.old passwords.new\n42c42\n< <old, irrelevant line>\n---\n> <the next password>\n```",
    ],
    'bandit-18': [
        "Logging in normally gets you kicked straight back out before you can do anything -- something in the account's own login setup is doing that. Is there a way to run a single command on a remote machine over SSH WITHOUT going through the normal interactive login process that's causing the problem?",
        "It's the account's `.bashrc` doing the kicking, but `.bashrc` only runs for INTERACTIVE login shells, not for every possible way of using SSH. SSH supports appending a single command directly to the connection command itself, which runs that one command remotely and returns its output, without ever starting the interactive shell session that triggers `.bashrc` in the first place.",
        "`ssh bandit18@<host> -p <port> cat readme` runs just that command remotely, bypassing the interactive shell (and `.bashrc`) entirely.\n\nIllustrative example only -- your real value will differ:\n```\n$ ssh bandit18@<host> -p <port> cat readme\nbandit18@<host>'s password:\n<the next password>\n```",
    ],
    'bandit-19': [
        "There's a special binary in your home directory that, when run, acts with permissions belonging to a DIFFERENT, more privileged account, not your own. What's the mechanism that lets a program run with its owner's permissions rather than the permissions of whoever launched it?",
        "A setuid binary runs with the permissions of the account that OWNS the file, regardless of who actually launches it. If a more-privileged account owns this particular binary, running it lets you act with that account's privileges for as long as it's running. Running an unfamiliar binary with no arguments at all often just prints a usage message explaining how it expects to be invoked.",
        "Run the binary with no arguments to see its usage message -- it expects a command to execute with elevated privilege.\n\nIllustrative example only -- your real value will differ:\n```\nbandit19@bandit:~$ ./bandit20-do cat /etc/bandit_pass/bandit20\n<the next password>\n```",
    ],
    'bandit-20': [
        "This setuid binary doesn't read a password from a file at all -- it connects OUT to a port on your own machine that YOU get to choose, expecting to receive the current password over that connection. For that to work, something has to already be listening on that port before you trigger the binary.",
        "Netcat can act as a LISTENER, not just a client that connects out, meaning it can sit waiting for an incoming connection on a port you choose. Basic shell job control lets you run a listener in the background (or a second session) while triggering the setuid binary in the foreground, so both are running at the same time.",
        "Start a listener: `nc -lvp <some port> &`. Then run the setuid binary with that port as its argument. Back in the listener, type bandit20's password and press enter.\n\nIllustrative example only -- your real value will differ:\n```\nbandit20@bandit:~$ nc -lvp 12345 &\nbandit20@bandit:~$ ./suconnect 12345\n<type bandit20's own password into the nc session, then Enter>\n<the next password appears in the nc session>\n```",
    ],
    'bandit-21': [
        "Something is scheduled to run automatically and periodically on this system, as a MORE privileged account than yours. Is there somewhere you can read exactly what's scheduled to run, as whom, and how often, without needing to guess or reverse-engineer anything?",
        "Cron runs commands on a schedule, and its configuration lives in plain, readable text files under a standard system location, naming exactly which user runs what command and how frequently. Reading that configuration directly tells you precisely what's about to run automatically, including any job that might already be doing useful work on your behalf.",
        "`cat /etc/cron.d/*` lists every scheduled job, including one running as bandit22 that writes the next password somewhere readable.\n\nIllustrative example only -- your real path/value will differ:\n```\nbandit21@bandit:~$ cat /etc/cron.d/*\n* * * * * bandit22 /usr/bin/cronjob_bandit22.sh\nbandit21@bandit:~$ cat /usr/bin/cronjob_bandit22.sh\ncat /etc/bandit_pass/bandit22 > /tmp/some-file\nbandit21@bandit:~$ cat /tmp/some-file\n<the next password>\n```",
    ],
    'bandit-22': [
        "The scheduled job here runs an actual SCRIPT rather than a simple one-line command, and that script runs with more privileged permissions than yours. Even though you can't run it AS that privileged user yourself, is there anything stopping you from just reading the script's own source to see exactly what it does?",
        "The cron script computes where it writes its output using a value derived from the running user's own name, piped through a hashing function, rather than a fixed, predictable path. You can read the script's source directly (even though you can't execute it as the privileged user), which tells you the exact formula it uses, and you can reproduce that same formula by hand, substituting the privileged account's name for your own.",
        "`cat` the cron script to see it computes an output filename via `whoami | md5sum`. Reproduce that with `bandit23` substituted for the username, then read the resulting path under `/tmp`.\n\nIllustrative example only -- your real value will differ:\n```\nbandit22@bandit:~$ echo -n bandit23 | md5sum\n<a hex hash>  -\nbandit22@bandit:~$ cat /tmp/<that hex hash>\n<the next password>\n```",
    ],
    'bandit-23': [
        "This cron job scans a directory that anyone can write into, looking for files matching a certain pattern, and then actually RUNS whatever it finds there, as a more privileged user, before deleting it. If you knew that pattern, what could you place in that directory yourself?",
        "Reading the cron script (as the previous level's user) tells you exactly which shared, writable directory it scans and what naming pattern qualifies a file to be executed. If you can write your own script into that directory matching the pattern, the next scheduled sweep will run YOUR code with the privileged account's permissions, including copying a normally-unreadable password file somewhere you can read it.",
        "Write a script into that directory (matching the required pattern) that copies the next password into somewhere you can read, make it executable, and wait for the next cron sweep.\n\nIllustrative example only -- your real path/value will differ:\n```\nbandit23@bandit:~$ cat > /var/spool/<matching-dir>/mine.sh <<EOF\n#!/bin/bash\ncp /etc/bandit_pass/bandit24 /tmp/out24\nchmod 644 /tmp/out24\nEOF\nbandit23@bandit:~$ chmod +x /var/spool/<matching-dir>/mine.sh\n<wait up to a minute>\nbandit23@bandit:~$ cat /tmp/out24\n<the next password>\n```",
    ],
    'bandit-24': [
        "You need to send the right 4-digit PIN alongside your current password to a service on a port, and you don't know the PIN. 10,000 possibilities is a lot to guess by hand, but is it actually a lot for a computer to try in sequence?",
        "A 4-digit PIN has exactly 10,000 possible values (0000 through 9999), small enough for a simple shell loop to generate every single one and send each attempt, one per line, over a single connection, all in well under a minute. Filtering the flood of responses down to just the one that DIDN'T fail is the last step.",
        "A brute-force loop: `for pin in $(seq -w 0 9999); do echo <bandit24-password> $pin; done | nc -q1 localhost 30002 > /tmp/results.txt`, then `grep -v Wrong /tmp/results.txt` to find the real response.\n\nIllustrative example only -- your real value will differ:\n```\nbandit24@bandit:~$ grep -v Wrong /tmp/results.txt\nCorrect! <the next password>\n```",
    ],
    'bandit-25': [
        "Logging into the next account immediately kicks you out again, but this time it's not `.bashrc` -- the account's shell shows you one file with a pager and exits. A pager only shows the WHOLE file at once and exits immediately if the file fits entirely on your screen. What happens if the file doesn't fit?",
        "If a file is too long to fit on a single screen, a pager pauses at an interactive `--More--` prompt instead of exiting right away, and you can force that condition by shrinking your terminal window to just a few lines before connecting, so even a short file no longer 'fits.' Interactive prompts inside programs like this often accept single-key commands you wouldn't expect, including ones that launch other programs.",
        "Shrink your terminal to a handful of rows, then SSH in -- `more` will pause on `--More--` instead of exiting. From that prompt, pressing `v` launches an editor (vi) on the file being paged.\n\nIllustrative example only -- shrink your terminal window first, then:\n```\n$ ssh bandit26@<host> -p <port>\nbandit26@<host>'s password:\n--More--(bytes 0-500/1200)\n<press v here to open vi on the paged file>\n```",
    ],
    'bandit-26': [
        "You've landed inside a real text editor now, launched from the previous level's escape. A general-purpose editor is still a full program with its own features -- does it have any documented way of running OTHER programs from inside it?",
        "Most text editors, vi included, support 'shelling out': a documented command for launching an external program without leaving the editor. Since the editor itself is running as the more-privileged account, a shell launched from inside it inherits those same privileges, giving you a real, unrestricted login shell instead of just a paused file view.",
        "From inside vi, type `:set shell=/bin/bash` then `:shell` (or `:!/bin/bash`) -- this spawns a real bash shell as the privileged account.\n\nIllustrative example only:\n```\n:set shell=/bin/bash\n:shell\nbandit26@bandit:~$ find / -user bandit27 2>/dev/null\n/usr/bin/bandit27-do\nbandit26@bandit:~$ ./bandit27-do cat /etc/bandit_pass/bandit27\n<the next password>\n```",
    ],
    'bandit-27': [
        "This time the password lives inside a git repository, reachable over the network. Is there a way to clone a git repo the same way you'd normally authenticate over SSH?",
        "`git clone` accepts an `ssh://` URL just like any other remote source, and it authenticates over that connection exactly the way a normal SSH login would: a username, host, port, and password (or key). Once cloned, the repository's files sit on your own disk like any other checked-out project, ready to read normally.",
        "`git clone ssh://bandit27-git@<host>:<port>/home/bandit27-git/repo`, entering the password when prompted. Then read the files it checked out.\n\nIllustrative example only -- your real value will differ:\n```\n$ git clone ssh://bandit27-git@<host>:<port>/home/bandit27-git/repo\n$ cat repo/README.md\n<the next password>\n```",
    ],
    'bandit-28': [
        "The password used to be visible in this repository's files, but a later change removed or edited it out. Does deleting something in a NEWER version of a file actually erase it from the project's history entirely?",
        "Git keeps a complete history of every change ever made -- editing or deleting content in a later commit doesn't erase it from EARLIER commits, which remain fully readable forever unless someone deliberately rewrites history. Git has a way to show the actual line-by-line change each commit made, not just a one-line summary message, letting you see exactly what existed before it was edited out.",
        "Clone the repo, then `git log -p` shows every historical change in full. Look through the diff output for an earlier version of the file with the real password.\n\nIllustrative example only -- your real value will differ:\n```\n$ git log -p\ncommit abc123...\n-README.md-\n-<the next password>\n+README.md content has been changed. Sorry!\n```",
    ],
    'bandit-29': [
        "Cloning a repository and looking at its files only shows you ONE line of development by default. Can a single git repository actually contain multiple, independent versions of its history at once?",
        "A git repository can have several branches, separate, independent lines of development, and checking out the default one only shows you that single branch's current state. Git has a documented way of listing EVERY branch that exists in the repo, not just the one you happened to check out.",
        "`git branch -a` lists every branch. `git checkout <branch-name>` each one and look through its files.\n\nIllustrative example only -- your real branch/value will differ:\n```\n$ git branch -a\n* master\n  remotes/origin/dev\n$ git checkout dev\n$ cat README.md\n<the next password>\n```",
    ],
    'bandit-30': [
        "Besides commits and branches, git has one more way of marking a specific point in a project's history, often used to flag releases. Could something be attached to one of those markers without ever being part of any branch's current, checked-out files?",
        "Git tags mark a specific point in history, independently of any branch, and can carry their own message or point at content that never made it onto any branch's current tip at all. Listing a repo's tags and inspecting what each one actually points to is a separate step from looking through branches.",
        "`git tag` lists any tags. `git show <tagname>` displays what it points at.\n\nIllustrative example only -- your real tag/value will differ:\n```\n$ git tag\nsecret\n$ git show secret\ntag secret\n<the next password>\n```",
    ],
    'bandit-31': [
        "This level isn't about finding something already hidden in the repository -- it wants you to ADD something specific and push it back. What's the first thing worth doing before trying anything, when a repo's own documentation might spell out exactly what's expected?",
        "The repository's README documents precisely what file, name, and content the level is checking for -- git won't accept just anything you push. Once you create exactly what's asked for, the normal git workflow (stage, commit, push) applies, and the push itself, if it satisfies what's required, can return or reveal the next password directly in its output.",
        "`cat README.md` for the exact filename/content required, create that file, then `git add`, `commit`, and `push origin master`.\n\nIllustrative example only -- your real required filename/value will differ:\n```\n$ cat README.md\nMake sure to place the key file with the correct name in the folder\n$ echo 'May I come in?' > key.txt\n$ git add key.txt && git commit -m add-key && git push origin master\nremote: <the next password>\n```",
    ],
    'bandit-32': [
        "Everything you type here gets transformed to uppercase before it's evaluated -- but that transformation only affects LOWERCASE letters. Is there something you could type that contains no lowercase letters at all, and would therefore pass through completely untouched?",
        "A wrapper that only uppercases lowercase letters leaves digits, symbols, and punctuation completely unaffected, so any input made up entirely of non-lowercase characters survives the filter unchanged. Separately, in a shell, a bare `$0` evaluates to the name the current shell was invoked with, and how the ENCLOSING shell was originally launched affects what that value actually is.",
        "Typing `$0` at the prompt survives the uppercase filter untouched (no lowercase letters) and, because this wrapper shell was launched via `bash -c`, evaluates to a fresh, unrestricted bash shell.\n\nIllustrative example only:\n```\n$0\nbandit33@bandit:~$ cat /etc/bandit_pass/bandit33\n<the next password>\n```",
    ],
    'bandit-33': [
        "This final shell only allows a couple of harmless-looking tools and blocks you from typing any command containing a `/` directly. But does that restriction apply to what an ALLOWED program does internally, once it's already running?",
        "This is a restricted shell (rbash) that limits your PATH and blocks commands containing `/` at the prompt, but that restriction only governs what YOU type directly. One of the few allowed tools has a documented action for launching an arbitrary program of its own choosing, and that action isn't subject to the same restriction, since it's the allowed program doing the launching, not you typing a blocked command.",
        "`find`'s `-exec` action can launch an arbitrary program: `find . -exec /bin/sh \\;` launches a real, unrestricted shell. It still inherits the old restricted PATH, so reassign it afterward.\n\nIllustrative example only:\n```\n$ find . -exec /bin/sh \\;\n$ PATH=/usr/bin:/bin\n$ export PATH\n$ cat /etc/bandit_pass/bandit33\n<the final password>\n```",
    ],
}


def _progression_note(challenge_id: str) -> str:
    """Return the common, current-instance account-transition instruction."""
    if challenge_id == "bandit-start-here":
        return (
            "\n\n**Next challenge:** After submitting this flag, begin Bandit 0 -> 1. "
            "Use the current host and port shown by the launch panel to connect as "
            "`bandit0` with password `bandit0`."
        )

    level = int(challenge_id.rsplit("-", 1)[1])
    if level == 33:
        return (
            "\n\n**Finish:** You are working as `bandit33`. Submit the recovered "
            "password here to complete the Bandit track; no further account switch is required."
        )

    return (
        f"\n\n**Account progression:** You are working as `bandit{level}`. After "
        "recovering and submitting this password, exit and reconnect to the current "
        f"host and port shown by the launch panel as `bandit{level + 1}`, using the "
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


def _validate_bandit_content() -> None:
    """Keep help guidance and account transitions aligned with this curriculum."""
    hint_text = "\n".join(content for tiers in HINTS.values() for content in tiers)
    _require("man " not in hint_text, "Bandit hints must use image-supported built-in help")

    for challenge_id, tiers in HINTS.items():
        _require(bool(tiers), f"{challenge_id} needs at least one hint tier")
        value = next(challenge["points"] for challenge in challenges_data if challenge["id"] == challenge_id)
        _require(len(tiers) == 3, f"{challenge_id} must have exactly three managed hint tiers")
        # Real invariant check on the percents managed_tiers() actually
        # produces (strictly increasing, cumulative percent-of-value, never
        # reaching 100%) -- NOT a comparison of tier_costs() against itself,
        # which can never fail regardless of what either function does.
        # These are cumulative percentages of the challenge's own point
        # value (see hint_economy.py), not additive currency amounts, so
        # they are never summed against `value`.
        costs = [cost for _, cost in managed_tiers(value, tiers)]
        _require(
            len(costs) == 3 and costs[0] < costs[1] < costs[2],
            f"{challenge_id} managed hint costs must be strictly increasing across tiers",
        )
        _require(
            costs[-1] < 100,
            f"{challenge_id} managed hint cost must leave a nonzero percentage of the challenge's value on solve",
        )

    challenge_ids = {challenge["id"] for challenge in challenges_data}
    for level in range(33):
        challenge_id = f"bandit-{level:02d}"
        _require(challenge_id in challenge_ids, f"missing {challenge_id}")
        note = _progression_note(challenge_id)
        _require(f"`bandit{level}`" in note, f"{challenge_id} omits its current account")
        _require(f"`bandit{level + 1}`" in note, f"{challenge_id} omits its next account")
        _require("launch panel" in note, f"{challenge_id} omits launch-panel access")
        rendered = _render_description(next(challenge for challenge in challenges_data if challenge["id"] == challenge_id))
        _require(rendered.count(note) == 1, f"{challenge_id} does not append progression exactly once")

    final_note = _progression_note("bandit-33")
    _require("`bandit33`" in final_note, "final level omits its current account")
    _require("no further account switch is required" in final_note, "final level omits completion guidance")
    final_rendered = _render_description(next(challenge for challenge in challenges_data if challenge["id"] == "bandit-33"))
    _require(final_rendered.count(final_note) == 1, "final progression is not appended exactly once")


_validate_bandit_content()

# Generate folder and files relative to the repo root folder dynamically
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(script_dir, "..", "challenges"))
os.makedirs(base_dir, exist_ok=True)

for i, ch in enumerate(challenges_data):
    folder_path = os.path.join(base_dir, ch["id"])
    os.makedirs(folder_path, exist_ok=True)

    full_desc = _render_description(ch)

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

    # Wallet-managed hints are intentionally absent from CTFd YAML: native
    # hint unlocks debit global score and must not be a bypass.

    file_path = os.path.join(folder_path, "challenge.yml")
    with open(file_path, "w") as f:
        f.write(yaml_content)

print(f"Successfully generated {len(challenges_data)} Bandit challenges inside '{base_dir}'!")
with open(os.path.join(base_dir, "bandit-hint-wallet.json"), "w", encoding="utf-8") as manifest:
    json.dump({"schema_version": 1, "track": "bandit", "entries": [{"name": c["name"], "tiers": [{"tier": n, "cost": cost, "content": text} for n, (text, cost) in enumerate(managed_tiers(c["points"], HINTS[c["id"]]), 1)]} for c in challenges_data if c["id"] in HINTS]}, manifest)
