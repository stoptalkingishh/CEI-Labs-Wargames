#!/usr/bin/env python3
"""Bandit level 32: bandit32's login shell uppercases every command
before running it. The escape is typing "$0" -- tr only touches a-z so
the literal two characters survive untouched into eval, and $0 inside
the eval's fresh parse resolves to the enclosing `bash -c '...'`
invocation's own argv[0], which bash defaults to the literal string
"bash" whenever -c is used without a following name argument (verified:
`bash -c 'echo $0'` prints "bash"). eval-ing that spawns a real,
unrestricted bash outside the uppercase loop entirely."""
import os
import subprocess

# Security: this flag is now a per-team secret generated at container
# START by entrypoint.sh -- a fixed-length placeholder here, substituted
# for the real value at container start (see
# docs/security-audit-status.md).
FLAG_32 = "BANDITPLACEHOLDER32".ljust(32, "Z")  # -> bandit33's password

SHELL_PATH = "/home/bandit32/uppershell"

# The outer script is just a thin trampoline into `bash -c '...'` --
# that -c invocation is what makes $0 default to "bash" rather than to
# this trampoline script's own path (which would just re-launch the same
# restricted loop instead of escaping it).
shell_script = (
    "#!/bin/bash\n"
    "exec bash --norc -c '\n"
    'if [ -z "${CEI_BANDIT_BANNER_SHOWN:-}" ]; then export CEI_BANDIT_BANNER_SHOWN=1; cat -- /etc/cei-labs/banners/bandit32; fi\n'
    'echo "Welcome to the CEI-Labs UPPERCASE shell (bandit32)"\n'
    'echo "Every command you enter is converted to UPPERCASE before it runs."\n'
    "export PATH=/usr/bin:/bin\n"
    'while read -r -p "$ " line; do\n'
    '    [ -z "$line" ] && continue\n'
    '    cmd=$(printf "%s" "$line" | tr "a-z" "A-Z")\n'
    '    eval "$cmd"\n'
    "done\n"
    "'\n"
)
with open(SHELL_PATH, "w", newline="\n") as f:
    f.write(shell_script)
os.chmod(SHELL_PATH, 0o755)
subprocess.run(["chown", "root:root", SHELL_PATH], check=True)

with open("/etc/shells", "a") as f:
    f.write(SHELL_PATH + "\n")
subprocess.run(["usermod", "-s", SHELL_PATH, "bandit32"], check=True)

# Only reachable from a real (escaped) shell -- the uppercase loop can
# never produce a valid lowercase command name, so `cat` typed there
# always becomes the nonexistent command CAT.
creds_dir = "/home/bandit32/.creds"
os.makedirs(creds_dir, exist_ok=True)
flag_path = f"{creds_dir}/flag"
with open(flag_path, "w", newline="\n") as f:
    f.write(FLAG_32 + "\n")
subprocess.run(["chown", "-R", "bandit32:bandit32", creds_dir], check=True)
os.chmod(creds_dir, 0o755)
os.chmod(flag_path, 0o644)

print("Level 32 uppercase-shell artifacts written.")
