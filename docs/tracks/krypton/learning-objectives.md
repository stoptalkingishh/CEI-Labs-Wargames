# Krypton — Learning Objectives

A skills inventory for the Krypton track (classical cryptography, 7
levels), organized by concept rather than by level number, so it can be
referenced independent of any specific level: to check what a
participant has actually learned, to plan which levels to assign for a
given skill gap, or to compare against a course syllabus. Each entry
names the real-world skill, not just the puzzle mechanic, and lists
which level(s) teach it. Pairs with `writeups.md` (full solutions) and
`cheatsheet.md` (fast facilitator lookup) in this same folder.

## Encoding vs. encryption (level 0)
- Recognize Base64 by its character set and distinguish a reversible
  *encoding* (no key required) from an actual cipher.

## Substitution ciphers (levels 1–3)
- Reverse a ROT13 rotation (a self-inverse Caesar shift of 13).
- Perform a known-plaintext attack: feed a cipher a value with known
  plaintext to directly observe its transformation, then reverse that
  transformation against the real ciphertext.
- Perform frequency analysis: use known English letter-frequency order
  (E, T, A, O, I, N, ...) to recover a monoalphabetic substitution
  alphabet from ciphertext statistics alone.

## Polyalphabetic ciphers (levels 4–5)
- Break a Vigenère cipher with a known key length by splitting
  ciphertext into interleaved groups, each solvable as its own
  independent Caesar shift.
- Perform Kasiski examination: find repeated ciphertext substrings,
  use the distances between repeats to estimate an *unknown* key
  length, then apply the known-key-length technique.

## Stream ciphers (level 6)
- Understand a stream cipher's core weakness when its keystream
  repeats: encrypting a long run of known plaintext directly reveals
  the keystream itself, which can then decrypt anything else encrypted
  with the same repeating stream.
