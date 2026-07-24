#!/usr/bin/env python3
"""Builds the static file-puzzle artifacts for Bandit levels 0-12.
Run as root at image build time (needs chown to arbitrary bandit* users).

Security: levels 1-12's flags are now per-team secrets generated at
container START by entrypoint.sh (see docs/security-audit-status.md),
not identical hardcoded values baked into every build. Levels whose flag
is written PLAIN into a file (0-9) get a fixed-length 32-char PLACEHOLDER
here, substituted for the real value by entrypoint.sh at container start
-- this preserves every level's exact-byte-count/position decoy
structure (e.g. level 5's 1033-byte requirement, level 6's 33-byte file)
since the placeholder is exactly the same length the real per-team
secret will be. Levels 10 (base64), 11 (rot13), 12 (gzip+bz2+hexdump)
transform the flag before writing, so a placeholder can't just be
substituted in place -- entrypoint.sh regenerates those 3 files from
scratch with the real per-team value instead; nothing is written for
them here."""
import os
import random
import subprocess


def placeholder(n: int) -> str:
    return f"BANDITPLACEHOLDER{n:02d}".ljust(32, "Z")


FLAG_00 = placeholder(0)
FLAG_01 = placeholder(1)
FLAG_02 = placeholder(2)
FLAG_03 = placeholder(3)
FLAG_04 = placeholder(4)
FLAG_05 = placeholder(5)
FLAG_06 = placeholder(6)
FLAG_07 = placeholder(7)
FLAG_08 = placeholder(8)
FLAG_09 = placeholder(9)


def write(path, content, owner, mode):
    if isinstance(content, str):
        content = content.encode()
    with open(path, "wb") as f:
        f.write(content)
    os.chmod(path, mode)
    subprocess.run(["chown", owner, path], check=True)


def mkdir(path, owner, mode=0o755):
    os.makedirs(path, exist_ok=True)
    os.chmod(path, mode)
    subprocess.run(["chown", owner, path], check=True)


# ---- Level 0: readme in home, plain text ----------------------------------
write("/home/bandit0/readme", FLAG_00 + "\n", "bandit0:bandit0", 0o644)

# ---- "Bandit: Start Here" onboarding challenge (build_bandit.py) ----------
write("/home/bandit0/welcome.txt", "WELCOME_TO_BANDIT\n", "bandit0:bandit0", 0o644)

# ---- Level 1: file named "-" -----------------------------------------------
write("/home/bandit1/-", FLAG_01 + "\n", "bandit1:bandit1", 0o644)

# ---- Level 2: file with spaces in the name ---------------------------------
write(
    "/home/bandit2/spaces in this filename",
    FLAG_02 + "\n",
    "bandit2:bandit2",
    0o644,
)
# a decoy so `cat *` (unquoted glob) doesn't trivially solve the level --
# the player must still identify and quote the correct filename
write("/home/bandit2/notes.txt", "nothing here\n", "bandit2:bandit2", 0o644)
# Count only non-hidden entries: useradd -m always seeds the home dir with
# dotfiles (.bashrc, .profile, .bash_logout), so a raw os.listdir() count
# is >1 even with zero decoys -- that would make this assertion a no-op.
# `*` glob expansion (what a player would naively try) never matches
# dotfiles either, so this mirrors exactly what `cat *` would see.
visible_entries = [e for e in os.listdir("/home/bandit2") if not e.startswith(".")]
assert len(visible_entries) > 1, (
    "level2 home dir must contain a non-hidden decoy alongside the "
    "spaces-named file, otherwise `cat *` trivially solves the level "
    f"(found only: {visible_entries!r})"
)

# ---- Level 3: hidden file inside inhere/ -----------------------------------
mkdir("/home/bandit3/inhere", "bandit3:bandit3")
write("/home/bandit3/inhere/.hidden", FLAG_03 + "\n", "bandit3:bandit3", 0o644)
# a couple of non-hidden decoys so `ls` alone isn't enough
write("/home/bandit3/inhere/notes.txt", "nothing here\n", "bandit3:bandit3", 0o644)

# ---- Level 4: only human-readable file among -file00..-file09 -------------
mkdir("/home/bandit4/inhere", "bandit4:bandit4")
readable_index = 7
for i in range(10):
    name = f"-file0{i}"
    path = f"/home/bandit4/inhere/{name}"
    if i == readable_index:
        write(path, FLAG_04 + "\n", "bandit4:bandit4", 0o644)
    else:
        # random binary bytes -- `file` reports these as "data", not ASCII text
        write(path, bytes(random.randrange(256) for _ in range(200)), "bandit4:bandit4", 0o644)

# ---- Level 5: file that is human-readable, exactly 1033 bytes, not executable,
#      somewhere under a maze of subdirectories -----------------------------
mkdir("/home/bandit5/inhere", "bandit5:bandit5")
random.seed(5)
for d in range(1, 21):
    dname = f"maybehere{('0' + str(d)) if d < 10 else d}"
    dpath = f"/home/bandit5/inhere/{dname}"
    mkdir(dpath, "bandit5:bandit5")
    for f in range(1, 11):
        fpath = f"{dpath}/-file{f}"
        # decoys: wrong size, or (right size but) executable -- never all 3
        # criteria (readable + 1033 bytes + not executable) correct at once
        choice = random.randrange(3)
        if choice == 0:
            # deliberately excludes 1033 so this branch can never
            # coincidentally collide with the real file's size
            content = ("x" * random.randrange(100, 1033)).encode()
        elif choice == 1:
            content = ("y" * 1033).encode()
        else:
            content = bytes(random.randrange(256) for _ in range(1033))
        write(fpath, content, "bandit5:bandit5", 0o644)
        if choice == 1:
            # right size, but executable -- still fails the "not executable" test
            os.chmod(fpath, 0o755)
# place the one correct file last, guaranteed unique
correct_dir = "/home/bandit5/inhere/maybehere13"
correct_path = f"{correct_dir}/.file2"
content = (FLAG_05 + "\n").encode()
content = content + b" " * (1033 - len(content))  # pad to exactly 1033 bytes
write(correct_path, content, "bandit5:bandit5", 0o644)
assert os.path.getsize(correct_path) == 1033

# ---- Level 6: somewhere on the server, owned bandit7:bandit6, 33 bytes ----
mkdir("/var/lib/bandit-data", "root:root")
os.chmod("/var/lib/bandit-data", 0o755)
level6_path = "/var/lib/bandit-data/.sys-cache-6f2a"
content = (FLAG_06 + "\n").encode()
assert len(content) == 33, f"level6 content must be exactly 33 bytes, got {len(content)}"
with open(level6_path, "wb") as f:
    f.write(content)
subprocess.run(["chown", "bandit7:bandit6", level6_path], check=True)
os.chmod(level6_path, 0o640)

# ---- Level 7: "millionth" in a large data.txt ------------------------------
random.seed(7)
words = ["apple", "banana", "cobalt", "delta", "ember", "falcon", "granite",
         "harbor", "indigo", "jungle", "kernel", "lumen", "meadow", "nectar",
         "oracle", "photon", "quartz", "raptor", "silver", "temple"]
lines = []
insert_at = 4200
for i in range(9000):
    if i == insert_at:
        lines.append(f"millionth {FLAG_07}")
    else:
        lines.append(f"{random.choice(words)}{random.randrange(1000)}")
write("/home/bandit7/data.txt", "\n".join(lines) + "\n", "bandit7:bandit7", 0o644)

# ---- Level 8: exactly one unique line in data.txt --------------------------
random.seed(8)
lines = []
common = [f"line-{random.randrange(500)}" for _ in range(40)]
for _ in range(3000):
    lines.append(random.choice(common))
unique_pos = 1500
lines[unique_pos] = FLAG_08
random.shuffle(lines)
# after shuffling, re-verify uniqueness (flag string not equal to any common line by construction)
assert lines.count(FLAG_08) == 1
write("/home/bandit8/data.txt", "\n".join(lines) + "\n", "bandit8:bandit8", 0o644)

# ---- Level 9: flag preceded by === in a mostly-binary data.txt ------------
random.seed(9)
binary_blob = bytes(random.randrange(256) for _ in range(4000))
marker = b"==========" + FLAG_09.encode() + b"\n"
content = binary_blob[:2000] + marker + binary_blob[2000:]
write("/home/bandit9/data.txt", content, "bandit9:bandit9", 0o644)

# ---- Levels 10 (base64), 11 (rot13), 12 (compressed hexdump) ---------------
# Deliberately NOT written here -- the flag is transformed before writing,
# so a simple placeholder substitution can't work. entrypoint.sh
# regenerates these 3 files from scratch with the real per-team value.
# Directory/ownership needs nothing pre-created -- write() in
# entrypoint.sh's Python block handles chown itself, same as here.

print("Levels 0-9 artifacts written (placeholders for 1-9; levels 10-12 deferred to entrypoint.sh).")
