#!/usr/bin/env python3
"""Bandit levels 25 (discover bandit26's unusual login shell) and 26
(actually break out of it and find the next flag).

Security: these flags are now per-team secrets generated at container
START by entrypoint.sh -- fixed-length placeholders here, substituted
for the real value at container start (see
docs/security-audit-status.md)."""
import os
import subprocess


def placeholder(n: int) -> str:
    return f"BANDITPLACEHOLDER{n:02d}".ljust(32, "Z")


FLAG_25 = placeholder(25)
FLAG_26 = placeholder(26)


def write(path, content, owner, mode):
    if isinstance(content, str):
        content = content.encode()
    with open(path, "wb") as f:
        f.write(content)
    os.chmod(path, mode)
    subprocess.run(["chown", owner, path], check=True)


# ---- Level 25: plain readable flag; the real "lesson" here is reading
# /etc/passwd (already world-readable by default) and noticing bandit26's
# shell field isn't /bin/bash -- that's prep for level 26, not something
# this level's own flag-discovery depends on. ----------------------------
write("/home/bandit25/readme", FLAG_25 + "\n", "bandit26:bandit25", 0o640)

# ---- Level 26: bandit26's login shell pages this file, then exits.
# Short enough that a normal-size terminal shows it all without pausing
# -- the player has to deliberately shrink their terminal to force
# `more` to pause, which is the actual lesson. -----------------------------
text_content = "\n".join([f"line {i}: nothing interesting here" for i in range(1, 8)]) + "\n"
write("/home/bandit26/text.txt", text_content, "bandit26:bandit26", 0o644)

subprocess.run(["cp", "/opt/build/src/showtext.sh", "/home/bandit26/showtext"], check=True)
subprocess.run(["chown", "bandit26:bandit26", "/home/bandit26/showtext"], check=True)
os.chmod("/home/bandit26/showtext", 0o755)

# bandit26's actual login shell -- must be a valid entry in /etc/shells
# or some sshd/PAM configs will refuse the login entirely.
with open("/etc/shells", "a") as f:
    f.write("/home/bandit26/showtext\n")
subprocess.run(
    ["usermod", "-s", "/home/bandit26/showtext", "bandit26"], check=True
)

# Level 26's own flag -- discoverable via "directory layout" exploration
# once a real shell is actually achieved (not reachable through the
# restricted showtext shell at all, matching "query the directory
# layout to locate the flag").
mkdir_path = "/home/bandit26/.hidden_dir"
os.makedirs(mkdir_path, exist_ok=True)
subprocess.run(["chown", "bandit26:bandit26", mkdir_path], check=True)
os.chmod(mkdir_path, 0o755)
# Owned bandit27:bandit26, mode 0640 -- same next-level-owner/current-level-
# group pattern as every other flag file (mirrors level 6's bandit7:bandit6).
write(f"{mkdir_path}/flag_26", FLAG_26 + "\n", "bandit27:bandit26", 0o640)

print("Levels 25-26 artifacts written.")
