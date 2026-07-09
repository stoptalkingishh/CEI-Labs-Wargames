#!/usr/bin/env python3
"""Bandit levels 25 (discover bandit26's unusual login shell) and 26
(actually break out of it and find the next flag)."""
import os
import subprocess

FLAG_25 = "5czgV9L3Xx8JPOyU3jO5B9I0A3bM9E3z"
FLAG_26 = "3ba3118a22e93127a4ed485be72ef5ea"


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
write("/home/bandit25/readme", FLAG_25 + "\n", "bandit25:bandit25", 0o644)

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
write(f"{mkdir_path}/flag_26", FLAG_26 + "\n", "bandit26:bandit26", 0o644)

print("Levels 25-26 artifacts written.")
