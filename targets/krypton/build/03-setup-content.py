#!/usr/bin/env python3
"""Krypton onboarding content only. Levels 1, 3, 4, 5's actual puzzle
content (ROT13, substitution, two Vigenere variants) is generated at
CONTAINER START by entrypoint.sh from per-team secrets, not baked in
here at build time -- see docs/security-audit-status.md. Levels 2 and 6
(which need the compiled `encrypt` binaries) are handled separately too,
also at container start now for level 2 (level 6 still build-time for
now)."""
import os
import subprocess


def write(path, content, owner, mode=0o440):
    with open(path, "w", newline="\n") as f:
        f.write(content)
    os.chmod(path, mode)
    subprocess.run(["chown", owner, path], check=True)


# ---- "Krypton: Start Here" onboarding challenge (build_krypton.py) -----
# Same krypton1 account the real level 1 uses, a separate file
# (welcome.txt, distinct from level 1's own puzzle content -- the
# krypton2/README pair entrypoint.sh later writes into this same home
# directory) -- exists purely to exercise the launch controls themselves.
write("/home/krypton1/welcome.txt", "WELCOME_TO_KRYPTON\n", "krypton1:krypton1", 0o444)

print("Onboarding content written; levels 1/3/4/5 content deferred to entrypoint.sh.")
