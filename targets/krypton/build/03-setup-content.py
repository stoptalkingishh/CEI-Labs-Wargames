#!/usr/bin/env python3
"""Krypton levels 1, 3, 4, 5: pure-text puzzles (ROT13, monoalphabetic
substitution, two Vigenere variants). Levels 2 and 6 (which need the
compiled `encrypt` binaries as the single source of truth for their
ciphertext) are handled separately, after those binaries exist -- see
the Dockerfile."""
import os
import random
import string
import subprocess

FLAG = {
    1: "ROTTEN",
    3: "BRUTE",
    4: "CLEARTEXT",
    5: "RANDOM",
}


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
    """key_alphabet: a 26-letter permutation of A-Z; key_alphabet[0] is
    what 'A' becomes, etc. Case preserved, non-letters passed through."""
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


# ---- "Krypton: Start Here" onboarding challenge (build_krypton.py) -----
# Same krypton1 account the real level 1 uses, a separate file in its
# home directory (not /krypton/krypton1, which is level 1's own puzzle
# content) -- exists purely to exercise the launch controls themselves.
write("/home/krypton1/welcome.txt", "WELCOME_TO_KRYPTON\n", "krypton1:krypton1", 0o444)

# ---- Level 1: ROT13 -----------------------------------------------------
mkdir_owned("/krypton/krypton1", "krypton1:krypton1")
write(
    "/krypton/krypton1/krypton2",
    rot13(FLAG[1]) + "\n",
    "krypton1:krypton1",
    0o440,
)
write(
    "/krypton/krypton1/README",
    "The password for krypton2 is in the file 'krypton2' in this "
    "directory, rotated by 13 places (ROT13).\n",
    "krypton1:krypton1",
    0o444,
)

# ---- Level 3: monoalphabetic substitution, frequency analysis ----------
mkdir_owned("/krypton/krypton3", "krypton3:krypton3")
random.seed(1337)
sub_key = list(string.ascii_uppercase)
random.shuffle(sub_key)
sub_key = "".join(sub_key)

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
    "advance. Keep counting, keep comparing, and remember: the password "
    "for the next level is BRUTE."
)
write(
    "/krypton/krypton3/krypton4",
    substitution_encrypt(passage3, sub_key) + "\n",
    "krypton3:krypton3",
    0o440,
)
write(
    "/krypton/krypton3/README",
    "The attached file 'krypton4' is intercepted English text encrypted "
    "with a simple substitution cipher (each letter always maps to the "
    "same other letter). Use frequency analysis (E, T, A, O, I, N are "
    "the most common letters in English) to recover the plaintext and "
    "find the password for krypton4.\n",
    "krypton3:krypton3",
    0o444,
)

# ---- Level 4: Vigenere, known key length (6) ----------------------------
mkdir_owned("/krypton/krypton4", "krypton4:krypton4")
VIGENERE_KEY_4 = "CIPHER"  # 6 letters, matches the description's hint
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
    "recombine to find the password for the next level: CLEARTEXT."
)
write(
    "/krypton/krypton4/krypton5",
    vigenere_encrypt(passage4, VIGENERE_KEY_4) + "\n",
    "krypton4:krypton4",
    0o440,
)
write(
    "/krypton/krypton4/README",
    "The attached file 'krypton5' is intercepted text encrypted with a "
    "Vigenere cipher using a key exactly 6 letters long. Split the "
    "ciphertext into 6 interleaved groups and solve each as its own "
    "Caesar shift to recover the plaintext and the password for "
    "krypton5.\n",
    "krypton4:krypton4",
    0o444,
)

# ---- Level 5: Vigenere, unknown key length (Kasiski) --------------------
mkdir_owned("/krypton/krypton5", "krypton5:krypton5")
VIGENERE_KEY_5 = "OVERTHEWI"  # 9 letters
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
    "three, six, or nine letters. When you succeed, the password for the "
    "final level of Krypton is RANDOM. Look carefully for repeated three "
    "and four letter sequences scattered through this very message, "
    "measure the gaps between them, and the key length becomes clear."
)
write(
    "/krypton/krypton5/krypton6",
    vigenere_encrypt(passage5, VIGENERE_KEY_5) + "\n",
    "krypton5:krypton5",
    0o440,
)
write(
    "/krypton/krypton5/README",
    "The attached file 'krypton6' is intercepted text encrypted with a "
    "Vigenere cipher. This time the key length is NOT given -- use the "
    "Kasiski examination (look for repeated sequences in the ciphertext "
    "and measure the distances between them) to recover it, most likely "
    "3, 6, or 9 letters, then solve column by column as usual.\n",
    "krypton5:krypton5",
    0o444,
)

print("Levels 1, 3, 4, 5 content written.")
