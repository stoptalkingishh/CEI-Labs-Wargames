#!/bin/bash
# No background daemons for Krypton (all 7 levels are pure crypto
# puzzles, nothing needs a listening service beyond sshd itself).
#
# Levels 1-5's content/passwords ARE generated here, at container START,
# from per-team secrets in $LEVEL_SECRETS (a JSON blob the orchestrator
# injects -- see cei-labs-engine's instance_types.py
# generate_track_secrets()/generate_alpha_track_secrets()). This is what
# makes them unique per team instead of an identical hardcoded value
# baked into every build (see docs/security-audit-status.md). Levels
# 1/3/4/5 use ALPHABETIC-ONLY secrets (alpha_secret_keys, not
# secret_keys) since their flag gets embedded inside a passage that's
# itself ROT13/substitution/Vigenere-encrypted -- those ciphers only
# transform letters, so a normal token's digits/-/_ would pass through
# unencrypted and visibly stand out. krypton1's password (level 0's
# flag) and level 6's content are still build-time/static for now -- see
# docs/security-audit-status.md and docs/self-hosted-wargames-status.md
# for what's converted so far. Any level missing its key in
# $LEVEL_SECRETS is simply left with no usable password/content -- a
# locked account or a build-time-placeholder-free directory is a safe
# failure mode, not a shared-credential one, so this does not refuse to
# start the whole box over it.
set -e

if [ -n "${LEVEL_SECRETS:-}" ]; then
    python3 - <<'PYEOF'
import json
import os
import string
import subprocess

secrets = json.loads(os.environ.get("LEVEL_SECRETS", "{}"))


def write(path, content, owner, mode=0o440):
    with open(path, "w", newline="\n") as f:
        f.write(content)
    os.chmod(path, mode)
    subprocess.run(["chown", owner, path], check=True)


def mkdir_owned(path, owner, mode=0o750):
    os.makedirs(path, exist_ok=True)
    os.chmod(path, mode)
    subprocess.run(["chown", owner, path], check=True)


def rot13(s):
    return s.translate(str.maketrans(
        string.ascii_lowercase + string.ascii_uppercase,
        string.ascii_lowercase[13:] + string.ascii_lowercase[:13]
        + string.ascii_uppercase[13:] + string.ascii_uppercase[:13],
    ))


def substitution_encrypt(plaintext, key_alphabet):
    upper_map = str.maketrans(string.ascii_uppercase, key_alphabet)
    lower_map = str.maketrans(string.ascii_lowercase, key_alphabet.lower())
    return plaintext.translate(upper_map).translate(lower_map)


def vigenere_encrypt(plaintext, key):
    key = key.upper()
    out = []
    ki = 0
    for ch in plaintext:
        if ch.isalpha():
            shift = ord(key[ki % len(key)]) - ord('A')
            base = 'A' if ch.isupper() else 'a'
            out.append(chr((ord(ch) - ord(base) + shift) % 26 + ord(base)))
            ki += 1
        else:
            out.append(ch)
    return "".join(out)


# ---- Level 1: ROT13 -> krypton2's password -----------------------------
flag1 = secrets.get("krypton1")
if flag1:
    subprocess.run(["chpasswd"], input=f"krypton2:{flag1}\n", text=True, check=True)
    mkdir_owned("/krypton/krypton1", "krypton1:krypton1")
    write("/krypton/krypton1/krypton2", rot13(flag1) + "\n", "krypton1:krypton1", 0o440)
    write(
        "/krypton/krypton1/README",
        "The password for krypton2 is in the file 'krypton2' in this "
        "directory, rotated by 13 places (ROT13).\n",
        "krypton1:krypton1", 0o444,
    )

# ---- Level 3: monoalphabetic substitution -> krypton4's password -------
flag3 = secrets.get("krypton3")
if flag3:
    subprocess.run(["chpasswd"], input=f"krypton4:{flag3}\n", text=True, check=True)
    mkdir_owned("/krypton/krypton3", "krypton3:krypton3")
    # Substitution key is fixed (not itself a secret -- frequency analysis
    # works the same regardless of which permutation was used; only the
    # embedded flag word needs to be per-team).
    sub_key = "QWERTYUIOPASDFGHJKLZXCVBNM"
    passage3 = (
        "In the early days of computer security research, defenders learned "
        "that the strength of a cipher rests on more than secrecy of method. "
        "A system that hides its algorithm but leaks structure in its output "
        "is not truly secure at all. Analysts studying old wartime traffic "
        "found that the shape of a language itself betrays a simple "
        "substitution: certain letters appear again and again, others almost "
        "never. In English writing, the letter E turns up far more often "
        "than any other, followed closely by T, A, O, I, and N, while "
        "letters like Q, X, and Z remain rare. A careful count of letter "
        "frequency across a long enough passage of intercepted text, "
        "compared against these known patterns, is often enough to peel back "
        "a simple substitution cipher without ever knowing the key in "
        f"advance. Keep counting, keep comparing, and remember: the password "
        f"for the next level is {flag3}."
    )
    write("/krypton/krypton3/krypton4", substitution_encrypt(passage3, sub_key) + "\n", "krypton3:krypton3", 0o440)
    write(
        "/krypton/krypton3/README",
        "The attached file 'krypton4' is intercepted English text encrypted "
        "with a simple substitution cipher (each letter always maps to the "
        "same other letter). Use frequency analysis (E, T, A, O, I, N are "
        "the most common letters in English) to recover the plaintext and "
        "find the password for krypton4.\n",
        "krypton3:krypton3", 0o444,
    )

# ---- Level 4: Vigenere, known key length (6) -> krypton5's password ----
flag4 = secrets.get("krypton4")
if flag4:
    subprocess.run(["chpasswd"], input=f"krypton5:{flag4}\n", text=True, check=True)
    mkdir_owned("/krypton/krypton4", "krypton4:krypton4")
    VIGENERE_KEY_4 = "CIPHER"
    passage4 = (
        "Blaise de Vigenere gave his name to a cipher that resisted simple "
        "frequency analysis for centuries because it uses not one shift but "
        "many, cycling through a short repeating key across the length of "
        "the message. Once the key length is known, the ciphertext can be "
        "split into that many interleaved groups, each one a plain shift "
        "cipher on its own, solvable by ordinary frequency analysis or by "
        "brute-forcing all twenty-six possible shifts per group. Here the "
        "key is exactly six letters long. Split the intercepted text into "
        "six columns, solve each column as its own Caesar shift, and "
        f"recombine to find the password for the next level: {flag4}."
    )
    write("/krypton/krypton4/krypton5", vigenere_encrypt(passage4, VIGENERE_KEY_4) + "\n", "krypton4:krypton4", 0o440)
    write(
        "/krypton/krypton4/README",
        "The attached file 'krypton5' is intercepted text encrypted with a "
        "Vigenere cipher using a key exactly 6 letters long. Split the "
        "ciphertext into 6 interleaved groups and solve each as its own "
        "Caesar shift to recover the plaintext and the password for "
        "krypton5.\n",
        "krypton4:krypton4", 0o444,
    )

# ---- Level 5: Vigenere, unknown key length (Kasiski) -> krypton6's password
flag5 = secrets.get("krypton5")
if flag5:
    subprocess.run(["chpasswd"], input=f"krypton6:{flag5}\n", text=True, check=True)
    mkdir_owned("/krypton/krypton5", "krypton5:krypton5")
    VIGENERE_KEY_5 = "OVERTHEWI"
    passage5 = (
        "Long before computers, the Kasiski examination gave cryptanalysts a "
        "way to break a Vigenere cipher without ever being told the key "
        "length in advance. The trick relies on a simple observation: in any "
        "sufficiently long passage of natural language, short sequences of "
        "letters repeat by pure chance, and whenever a repeated sequence in "
        "the plaintext happens to line up with the same position in the "
        "repeating key, it produces an identical sequence in the ciphertext "
        "as well. By finding these repeated ciphertext fragments and "
        "measuring the distance between their starting positions, an analyst "
        "can compute the greatest common divisor of those distances, which "
        "is very likely to reveal the true key length. Once the length is "
        "known, the problem reduces to exactly the same column-by-column "
        "shift analysis used for a known key length, one column at a time, "
        "letter frequency by letter frequency, until the key falls out "
        "completely. Look carefully for repeated three and four letter "
        "sequences scattered through this very message, measure the gaps "
        "between them, and you will find the key length is most likely "
        f"three, six, or nine letters. When you succeed, the password for the "
        f"final level of Krypton is {flag5}. Look carefully for repeated three "
        "and four letter sequences scattered through this very message, "
        "measure the gaps between them, and the key length becomes clear."
    )
    write("/krypton/krypton5/krypton6", vigenere_encrypt(passage5, VIGENERE_KEY_5) + "\n", "krypton5:krypton5", 0o440)
    write(
        "/krypton/krypton5/README",
        "The attached file 'krypton6' is intercepted text encrypted with a "
        "Vigenere cipher. This time the key length is NOT given -- use the "
        "Kasiski examination (look for repeated sequences in the ciphertext "
        "and measure the distances between them) to recover it, most likely "
        "3, 6, or 9 letters, then solve column by column as usual.\n",
        "krypton5:krypton5", 0o444,
    )

# ---- Level 2: Caesar cipher, unknown shift -> krypton3's password ------
flag2 = secrets.get("krypton2")
if flag2:
    subprocess.run(["chpasswd"], input=f"krypton3:{flag2}\n", text=True, check=True)

    # Random, non-zero, non-human-readable shift byte -- deliberately NOT
    # a plain ASCII digit, so `cat keyfile.dat` doesn't just hand the
    # shift over. 256 isn't evenly divisible by 26, so a single raw byte
    # would land on shift == 0 (byte % 26 == 0) about 1 in 26 draws,
    # silently turning the "encrypted" file into plaintext -- reject and
    # re-draw until we get a byte whose value mod 26 is non-zero, matching
    # the shift computed in caesar_encrypt.c.
    with open("/dev/urandom", "rb") as f:
        while True:
            shift_byte = f.read(1)
            if shift_byte[0] % 26 != 0:
                break
    with open("/krypton/krypton2/keyfile.dat", "wb") as f:
        f.write(shift_byte)

    proc = subprocess.run(
        ["./encrypt"], cwd="/krypton/krypton2", input=flag2.encode(),
        stdout=subprocess.PIPE, check=True,
    )
    with open("/krypton/krypton2/krypton3", "wb") as f:
        f.write(proc.stdout)

    write(
        "/krypton/krypton2/README",
        "The password for krypton3 is in the file 'krypton3' in this "
        "directory, encrypted with a Caesar cipher using an unknown shift.\n\n"
        "The shift is derived from 'keyfile.dat' in this directory (not "
        "human-readable -- don't just cat it). Symlink it into a scratch "
        "directory, then use the 'encrypt' binary here on a known plaintext "
        "(like a long string of 'A's) to observe the shift empirically, and "
        "reverse it to decrypt krypton3.\n",
        "krypton2:krypton2", 0o444,
    )

    subprocess.run(["chown", "-R", "krypton2:krypton2", "/krypton/krypton2"], check=True)
    os.chmod("/krypton/krypton2", 0o750)
    os.chmod("/krypton/krypton2/keyfile.dat", 0o440)
    os.chmod("/krypton/krypton2/krypton3", 0o440)
    os.chmod("/krypton/krypton2/encrypt", 0o550)

# ---- Level 6: LFSR stream cipher -> Krypton's own final flag -----------
# Unlike levels 3/4/5, this flag is the WHOLE ciphertext (not embedded in
# a longer English passage) and the taught technique (encrypt 30+ 'A's to
# read the keystream directly, independent of what it's later applied
# to) doesn't depend on the flag's own character set -- a normal
# (non-alpha-only) secret is fine here, same reasoning as level 2.
flag6 = secrets.get("krypton6")
if flag6:
    with open("/dev/urandom", "rb") as f:
        keystream_bytes = f.read(30)
    with open("/krypton/krypton6/keystream.dat", "wb") as f:
        f.write(keystream_bytes)

    proc = subprocess.run(
        ["./encrypt"], cwd="/krypton/krypton6", input=flag6.encode(),
        stdout=subprocess.PIPE, check=True,
    )
    with open("/krypton/krypton6/final", "wb") as f:
        f.write(proc.stdout)

    write(
        "/krypton/krypton6/README",
        "The final Krypton flag is in the file 'final' in this directory, "
        "encrypted with a stream cipher whose keystream repeats every 30 "
        "characters (the 'encrypt' binary here implements it).\n\n"
        "Encrypt a long run of identical letters (e.g. 30+ 'A's) with "
        "'encrypt' to read the repeating keystream directly off the "
        "output, then use it to decrypt 'final'.\n",
        "krypton6:krypton6", 0o444,
    )

    subprocess.run(["chown", "-R", "krypton6:krypton6", "/krypton/krypton6"], check=True)
    os.chmod("/krypton/krypton6", 0o750)
    os.chmod("/krypton/krypton6/keystream.dat", 0o440)
    os.chmod("/krypton/krypton6/final", 0o440)
    os.chmod("/krypton/krypton6/encrypt", 0o550)
PYEOF
else
    echo "WARNING: no LEVEL_SECRETS set -- levels 1-6 will not be playable until content is synced." >&2
fi

exec /usr/sbin/sshd -D
