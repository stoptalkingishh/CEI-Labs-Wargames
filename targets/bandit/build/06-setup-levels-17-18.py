#!/usr/bin/env python3
"""Bandit levels 17 (diff) and 18 (.bashrc login trap).

Security: these flags are now per-team secrets generated at container
START by entrypoint.sh -- a fixed-length placeholder here, substituted
for the real value at container start (see
docs/security-audit-status.md)."""
import os
import random
import subprocess


def placeholder(n: int) -> str:
    return f"BANDITPLACEHOLDER{n:02d}".ljust(32, "Z")


FLAG_17 = placeholder(17)
FLAG_18 = placeholder(18)


def write(path, content, owner, mode):
    if isinstance(content, str):
        content = content.encode()
    with open(path, "wb") as f:
        f.write(content)
    os.chmod(path, mode)
    subprocess.run(["chown", owner, path], check=True)


# ---- Level 17: one changed line between passwords.old and passwords.new ---
random.seed(17)
lines = [f"pw_{random.randrange(10**8):08x}" for _ in range(42)]
old_content = "\n".join(lines) + "\n"
changed_index = 19
new_lines = list(lines)
new_lines[changed_index] = FLAG_17
new_content = "\n".join(new_lines) + "\n"
write("/home/bandit17/passwords.old", old_content, "bandit17:bandit17", 0o644)
write("/home/bandit17/passwords.new", new_content, "bandit17:bandit17", 0o644)

# ---- Level 18: readme readable via non-interactive SSH only ---------------
write("/home/bandit18/readme", FLAG_18 + "\n", "bandit18:bandit18", 0o644)
# Real bandit18's actual .bashrc: an interactive-shell guard (the same
# `case $- in *i*) ;; *) return;; esac` pattern Debian's own default
# .bashrc uses) followed by an unconditional logout trap. The guard is
# the load-bearing part -- confirmed empirically in this exact
# environment that omitting it makes the trap fire for EVERY ssh exec
# request, interactive or not (this container's bash/sshd combination
# sources .bashrc for non-interactive exec sessions too, unlike the
# textbook description of bash's behavior; Debian's own default .bashrc
# already relies on this same guard for exactly that reason, which is
# why every other level's untouched default .bashrc never causes this
# problem). With the guard, `ssh bandit18@host cat readme` (non-
# interactive, command mode) skips the trap and returns before the
# echo/exit ever run, exactly matching the real level's intended
# behavior; a normal interactive `ssh bandit18@host` login still hits it.
write(
    "/home/bandit18/.bashrc",
    "case $- in\n"
    "    *i*) ;;\n"
    "      *) return;;\n"
    "esac\n\n"
    'echo "This bashrc file has been used to prevent the use of the bash shell for bandit19"\n'
    "exit 0\n",
    "bandit18:bandit18",
    0o644,
)

print("Levels 17-18 artifacts written.")
