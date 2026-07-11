#!/usr/bin/env python3
"""Bandit level 33 (final): bandit33 lands in a restricted bash (`rbash`)
whose PATH points only at a directory holding `find` and `ls` -- no
`cat`/`less`/`more`/editors, so the flag file can't be read directly.
rbash blocks specifying a COMMAND name containing "/", but that
restriction never touches arguments passed to an allowed command --
`find`'s own -exec is not restricted, which is the classic, well-
documented rbash escape: `find . -exec /bin/sh \\; -quit` lets find (not
the restricted shell itself) exec a real, unrestricted /bin/sh."""
import os
import shutil
import subprocess

# Security: this flag is now a per-team secret generated at container
# START by entrypoint.sh -- a fixed-length placeholder here, substituted
# for the real value at container start (see
# docs/security-audit-status.md).
FINAL_FLAG = "BANDITPLACEHOLDER33".ljust(32, "Z")

SHELL_PATH = "/home/bandit33/rbash_wrapper.sh"
BIN_DIR = "/home/bandit33/restricted_bin"

os.makedirs(BIN_DIR, exist_ok=True)
for tool in ("find", "ls"):
    src = shutil.which(tool)
    shutil.copy2(src, f"{BIN_DIR}/{tool}")

shell_script = (
    "#!/bin/bash\n"
    "PATH=/home/bandit33/restricted_bin\n"
    "export PATH\n"
    'echo "Welcome, bandit33. This is a restricted shell -- one more escape to go."\n'
    "exec /bin/bash --restricted\n"
)
with open(SHELL_PATH, "w", newline="\n") as f:
    f.write(shell_script)
os.chmod(SHELL_PATH, 0o755)
subprocess.run(["chown", "root:root", SHELL_PATH], check=True)

with open("/etc/shells", "a") as f:
    f.write(SHELL_PATH + "\n")
subprocess.run(["usermod", "-s", SHELL_PATH, "bandit33"], check=True)

# Only reachable once a real shell is spawned (rbash's restricted PATH
# has no tool in it capable of reading a file's contents).
final_dir = "/home/bandit33/.final"
os.makedirs(final_dir, exist_ok=True)
flag_path = f"{final_dir}/flag"
with open(flag_path, "w", newline="\n") as f:
    f.write(FINAL_FLAG + "\n")
subprocess.run(["chown", "-R", "bandit33:bandit33", final_dir], check=True)
os.chmod(final_dir, 0o755)
os.chmod(flag_path, 0o644)
subprocess.run(["chown", "-R", "bandit33:bandit33", BIN_DIR], check=True)

print("Level 33 (final escape) artifacts written.")
