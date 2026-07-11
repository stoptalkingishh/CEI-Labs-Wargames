#!/usr/bin/env python3
"""Bandit levels 21-24: cron jobs (21-23) and the PIN spool dir (24).
Level 19-20's SUID binaries are placed directly in the Dockerfile (they
come from a separate compile stage, not this script)."""
import os
import subprocess


def placeholder(n: int) -> str:
    return f"BANDITPLACEHOLDER{n:02d}".ljust(32, "Z")


def chown(path, owner):
    subprocess.run(["chown", owner, path], check=True)


def mkdir(path, owner, mode):
    os.makedirs(path, exist_ok=True)
    chown(path, owner)
    os.chmod(path, mode)


# ---- Level 21->22: world-readable script, world-readable output -----------
mkdir("/tmp/cronjob_bandit22", "root:root", 0o777)
subprocess.run(["cp", "/opt/build/src/cronjob_bandit22.sh", "/usr/bin/cronjob_bandit22.sh"], check=True)
os.chmod("/usr/bin/cronjob_bandit22.sh", 0o755)
subprocess.run(["cp", "/opt/build/src/cronjob_bandit22.cron", "/etc/cron.d/cronjob_bandit22"], check=True)
os.chmod("/etc/cron.d/cronjob_bandit22", 0o644)

# ---- Level 22->23: script unreadable by bandit22, predictable output name -
mkdir("/tmp/cronjob_bandit23", "root:root", 0o777)
subprocess.run(["cp", "/opt/build/src/cronjob_bandit23.sh", "/usr/bin/cronjob_bandit23.sh"], check=True)
chown("/usr/bin/cronjob_bandit23.sh", "bandit23:bandit23")
os.chmod("/usr/bin/cronjob_bandit23.sh", 0o700)
subprocess.run(["cp", "/opt/build/src/cronjob_bandit23.cron", "/etc/cron.d/cronjob_bandit23"], check=True)
os.chmod("/etc/cron.d/cronjob_bandit23", 0o644)

# ---- Level 23->24: world-writable spool dir, world-readable runner script -
mkdir("/var/spool/bandit24", "root:root", 0o1777)  # sticky bit, like /tmp
subprocess.run(["cp", "/opt/build/src/cronjob_bandit24.sh", "/usr/bin/cronjob_bandit24.sh"], check=True)
os.chmod("/usr/bin/cronjob_bandit24.sh", 0o755)
subprocess.run(["cp", "/opt/build/src/cronjob_bandit24.cron", "/etc/cron.d/cronjob_bandit24"], check=True)
os.chmod("/etc/cron.d/cronjob_bandit24", 0o644)

# /etc/bandit_pass/bandit(N+1) holds bandit-N's OWN flag (which is also
# bandit(N+1)'s login password) -- the cron scripts above read from these
# directly (not from the login-password chain), matching every other
# file-based level's permission model: readable only by the level's own
# user.
#
# Security: fixed-length placeholders here -- entrypoint.sh substitutes
# the real per-team values (and sets bandit22/23/24's actual login
# passwords to match) at container start (see
# docs/security-audit-status.md). placeholder(N) always means "bandit-N's
# own flag" consistently, matching the "banditN" secret-key convention
# used everywhere else -- NOT the account number the file happens to be
# named after.
os.makedirs("/etc/bandit_pass", exist_ok=True)
level_passwords = {
    "bandit22": placeholder(21),  # bandit21's flag -> bandit22's password
    "bandit23": placeholder(22),  # bandit22's flag -> bandit23's password
    "bandit24": placeholder(23),  # bandit23's flag -> bandit24's password
}
for user, password in level_passwords.items():
    path = f"/etc/bandit_pass/{user}"
    with open(path, "w") as f:
        f.write(password + "\n")
    chown(path, f"{user}:{user}")
    os.chmod(path, 0o400)

print("Levels 21-24 cron/spool setup written.")
