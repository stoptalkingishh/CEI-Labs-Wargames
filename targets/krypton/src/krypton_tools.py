#!/usr/bin/env python3
"""Small, offline cryptanalysis helpers for the Krypton learning track.

The commands expose the repetitive bookkeeping while leaving the actual
cryptanalysis decisions (key length, shifts, and key) to the player.
"""

import argparse
import collections
import math
import string
import sys
from pathlib import Path

ENGLISH_FREQUENCIES = {
    "A": 8.167, "B": 1.492, "C": 2.782, "D": 4.253, "E": 12.702,
    "F": 2.228, "G": 2.015, "H": 6.094, "I": 6.966, "J": 0.153,
    "K": 0.772, "L": 4.025, "M": 2.406, "N": 6.749, "O": 7.507,
    "P": 1.929, "Q": 0.095, "R": 5.987, "S": 6.327, "T": 9.056,
    "U": 2.758, "V": 0.978, "W": 2.360, "X": 0.150, "Y": 1.974,
    "Z": 0.074,
}


def read_text(path):
    return Path(path).read_text(encoding="utf-8") if path else sys.stdin.read()


def letters(text):
    return "".join(character.upper() for character in text if character.isascii() and character.isalpha())


def frequency(args):
    text = letters("".join(read_text(path) for path in args.files) if args.files else sys.stdin.read())
    counts = collections.Counter(text)
    total = len(text)
    print("letter count percent")
    for letter, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        print(f"{letter:>6} {count:>5} {count * 100 / total:>6.2f}" if total else f"{letter:>6} {count:>5}   0.00")


def columns(args):
    text = letters(read_text(args.file))
    for index in range(args.length):
        print(f"{index + 1}: {text[index::args.length]}")


def kasiski(args):
    text = letters(read_text(args.file))
    distances = []
    for size in range(args.min_size, args.max_size + 1):
        positions = collections.defaultdict(list)
        for index in range(len(text) - size + 1):
            positions[text[index:index + size]].append(index)
        for fragment, indexes in sorted(positions.items()):
            if len(indexes) < 2:
                continue
            gaps = [right - left for left, right in zip(indexes, indexes[1:])]
            distances.extend(gaps)
            print(f"{fragment} positions={','.join(map(str, indexes))} gaps={','.join(map(str, gaps))}")
    if distances:
        print(f"gcd-of-reported-gaps={math.gcd(*distances)}")
        support = collections.Counter(
            divisor
            for distance in distances
            for divisor in range(2, min(20, distance) + 1)
            if distance % divisor == 0
        )
        ranked = sorted(support.items(), key=lambda item: (-item[1], item[0]))
        print(
            "candidate-length-support="
            + " ".join(f"{divisor}:{count}" for divisor, count in ranked[:10])
        )
    else:
        print("No repeated fragments found. Try a smaller --min-size.", file=sys.stderr)


def rotate(args):
    text = read_text(args.file)
    output = []
    for character in text:
        if character.isascii() and character.isalpha():
            alphabet = string.ascii_uppercase if character.isupper() else string.ascii_lowercase
            output.append(alphabet[(alphabet.index(character) + args.shift) % 26])
        else:
            output.append(character)
    sys.stdout.write("".join(output))


def caesar_score(ciphertext, shift):
    plaintext = [chr((ord(character) - ord("A") - shift) % 26 + ord("A")) for character in ciphertext]
    counts = collections.Counter(plaintext)
    total = len(plaintext)
    return sum(
        (counts[letter] - total * expected / 100) ** 2 / (total * expected / 100)
        for letter, expected in ENGLISH_FREQUENCIES.items()
    )


def recover_vigenere_key(text, length):
    normalized = letters(text)
    shifts = []
    for index in range(length):
        column = normalized[index::length]
        shifts.append(min(range(26), key=lambda shift: caesar_score(column, shift)))
    return "".join(chr(ord("A") + shift) for shift in shifts)


def decrypt_vigenere(text, key):
    shifts = [ord(character) - ord("A") for character in key.upper()]
    output = []
    index = 0
    for character in text:
        if character.isascii() and character.isalpha():
            alphabet = string.ascii_uppercase if character.isupper() else string.ascii_lowercase
            output.append(alphabet[(alphabet.index(character) - shifts[index % len(shifts)]) % 26])
            index += 1
        else:
            output.append(character)
    return "".join(output)


def vigenere_key(args):
    text = read_text(args.file)
    key = recover_vigenere_key(text, args.length)
    print(f"candidate-key={key}")
    print("preview:")
    print(decrypt_vigenere(text, key)[: args.preview])


def vigenere_decrypt(args):
    sys.stdout.write(decrypt_vigenere(read_text(args.file), args.key))


def substitute(args):
    if len(args.cipher_alphabet) != len(args.plain_alphabet):
        raise SystemExit("cipher and plaintext alphabets must have equal length")
    table = str.maketrans(
        args.cipher_alphabet + args.cipher_alphabet.lower(),
        args.plain_alphabet + args.plain_alphabet.lower(),
    )
    sys.stdout.write(read_text(args.file).translate(table))


def stream_decrypt(args):
    known_plain = letters(read_text(args.known_plain))
    known_cipher = letters(read_text(args.known_cipher))
    if not known_plain or len(known_plain) != len(known_cipher):
        raise SystemExit("known plaintext and ciphertext must contain the same non-zero number of letters")
    shifts = [
        (ord(cipher) - ord(plain)) % 26
        for plain, cipher in zip(known_plain, known_cipher)
    ]
    key = "".join(chr(ord("A") + shift) for shift in shifts)
    sys.stdout.write(decrypt_vigenere(read_text(args.target), key))


def build_parser():
    parser = argparse.ArgumentParser(
        prog="krypton-tools",
        description="Offline helpers for counting and arranging cipher text. Run a subcommand with --help for examples.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    command = subparsers.add_parser("freq", help="count ASCII letter frequencies")
    command.add_argument("files", nargs="*", help="files to combine; reads stdin when omitted")
    command.set_defaults(run=frequency)

    command = subparsers.add_parser("columns", help="split letters into interleaved Vigenere columns")
    command.add_argument("length", type=int, help="candidate key length")
    command.add_argument("file", help="ciphertext file")
    command.set_defaults(run=columns)

    command = subparsers.add_parser("kasiski", help="report repeated fragments and their distances")
    command.add_argument("file", help="ciphertext file")
    command.add_argument("--min-size", type=int, default=3)
    command.add_argument("--max-size", type=int, default=5)
    command.set_defaults(run=kasiski)

    command = subparsers.add_parser("rotate", help="apply a signed Caesar shift")
    command.add_argument("shift", type=int, help="positive to encrypt, negative to decrypt")
    command.add_argument("file", nargs="?", help="input file; reads stdin when omitted")
    command.set_defaults(run=rotate)

    command = subparsers.add_parser("substitute", help="apply a partial or complete substitution mapping")
    command.add_argument("cipher_alphabet", help="ciphertext letters, e.g. QXV")
    command.add_argument("plain_alphabet", help="matching plaintext guesses, e.g. ETA")
    command.add_argument("file", nargs="?", help="input file; reads stdin when omitted")
    command.set_defaults(run=substitute)

    command = subparsers.add_parser("vigenere-key", help="score Caesar columns and suggest a Vigenere key")
    command.add_argument("length", type=int, help="known or candidate key length")
    command.add_argument("file", help="ciphertext file")
    command.add_argument("--preview", type=int, default=240)
    command.set_defaults(run=vigenere_key)

    command = subparsers.add_parser("vigenere-decrypt", help="decrypt with a recovered Vigenere key")
    command.add_argument("key", help="alphabetic key")
    command.add_argument("file", nargs="?", help="input file; reads stdin when omitted")
    command.set_defaults(run=vigenere_decrypt)

    command = subparsers.add_parser(
        "stream-decrypt",
        help="recover additive shifts from a known plaintext/ciphertext pair and decrypt a target",
    )
    command.add_argument("known_plain")
    command.add_argument("known_cipher")
    command.add_argument("target")
    command.set_defaults(run=stream_decrypt)
    return parser


def main():
    args = build_parser().parse_args()
    if getattr(args, "length", 1) < 1:
        raise SystemExit("length must be positive")
    args.run(args)


if __name__ == "__main__":
    main()
