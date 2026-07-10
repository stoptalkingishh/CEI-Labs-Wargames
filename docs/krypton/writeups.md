# Krypton — Full Solution Writeups

Complete, step-by-step solutions for all 7 Krypton levels. Instructor
answer key — not for participant distribution.

Levels 1–6 connect via SSH to the host/port shown on that challenge's
launch panel (all 6 share one persistent box — see "Krypton: Start
Here"), logging in as the account named after the level, using the
previous level's flag as that account's password. Level 0 needs no
connection at all.

---

### Krypton 0 → 1: Base64 Decoding
**Goal:** Decode a Base64 string given directly in the description --
`S1JZUFRPTklTR1JFQVQ=`.
```
echo 'S1JZUFRPTklTR1JFQVQ=' | base64 -d
```
**Result:** `KRYPTONISGREAT`

---

### Krypton 1 → 2: ROT13 Substitution Cipher
**Goal:** Reverse a ROT13 rotation.
```
ssh krypton1@<host> -p <port>    # password: KRYPTONISGREAT
tr '[:alpha:]' 'N-ZA-Mn-za-m' < /krypton/krypton1/krypton2
```
**Result:** `ROTTEN`

---

### Krypton 2 → 3: Caesar Cipher (Unknown Shift)
**Goal:** `/krypton/krypton2/krypton3` is Caesar-shifted by an amount
derived from a keyfile you can't read directly, but an `encrypt` binary
next to it uses that key.
```
ssh krypton2@<host> -p <port>    # password: ROTTEN
mktemp -d
cd <the-temp-dir>
ln -s /krypton/krypton2/keyfile.dat
python3 -c "print('A'*40)" > plain.txt
/krypton/krypton2/encrypt < plain.txt
```
The output shows what a run of `A`s becomes — that letter's position in
the alphabet (relative to A) is the shift. Reverse that shift against
`krypton3`:
```
tr 'A-Za-z' 'N-ZA-Mn-za-m' < /krypton/krypton2/krypton3    # example for shift 13; adjust rotation to match what was actually observed
```
**Result:** `CAESARISEASY`

---

### Krypton 3 → 4: Frequency Analysis
**Goal:** `/krypton/krypton3/krypton4` is a monoalphabetic substitution
cipher. Three extra intercepted files (`found1`–`found3`) use the same
key.
```
ssh krypton3@<host> -p <port>    # password: CAESARISEASY
cat /krypton/krypton3/found1 /krypton/krypton3/found2 /krypton/krypton3/found3 /krypton/krypton3/krypton4 \
  | tr -cd 'A-Za-z' | tr 'a-z' 'A-Z' | fold -w1 | sort | uniq -c | sort -rn
```
Map the most frequent output letter to `E`, next to `T`, and so on down
the standard English frequency order (E T A O I N S H R D L U ...).
Apply the resulting substitution with `tr` against `krypton4`. Some
letters typically need manual correction once partial words appear.
**Result:** `BRUTE`

---

### Krypton 4 → 5: Vigenère Cipher (Known Key Length)
**Goal:** `/krypton/krypton4/krypton5` is Vigenère-encrypted with a
known 6-letter key.
```
ssh krypton4@<host> -p <port>    # password: BRUTE
cat /krypton/krypton4/krypton5
```
Split the ciphertext into 6 interleaved groups (characters at positions
0, 6, 12, ... form group 1; 1, 7, 13, ... form group 2; etc. — do this
with a short script, e.g. Python:
```python
ct = open('/krypton/krypton4/krypton5').read().strip()
groups = [''.join(ct[i::6]) for i in range(6)]
```
Solve each group independently as its own Caesar shift (same frequency-
analysis approach as level 3), then reassemble the recovered plaintext
back into original character order.
**Result:** `CLEARTEXT`

---

### Krypton 5 → 6: Vigenère Cipher (Kasiski Test)
**Goal:** Same as level 4, but the key length is unknown.
```
ssh krypton5@<host> -p <port>    # password: CLEARTEXT
cat /krypton/krypton5/krypton6
```
Find repeated 3+ character substrings in the ciphertext and record the
distance between each repeat. The greatest common factor across those
distances is the likely key length (this deployment's answer: 9). Once
known, apply level 4's technique with that key length.
**Result:** `RANDOM`

---

### Krypton 6 → 7: Stream Cipher / LFSR
**Goal:** `/krypton/krypton6/final` is stream-cipher encrypted; the
keystream repeats every 30 characters.
```
ssh krypton6@<host> -p <port>    # password: RANDOM
python3 -c "print('A'*60)" > plain.txt
/krypton/krypton6/encrypt < plain.txt > out.bin
xxd out.bin | head
```
Since every input byte is the same known value (`A`), the corresponding
output bytes directly reveal the 30-byte repeating keystream (compare
each output byte against the known plaintext byte, using whichever
operation — XOR or subtraction — the cipher implements). Apply that same
operation between the recovered keystream (cycling every 30 bytes) and
`/krypton/krypton6/final` to recover the final plaintext.
**Result (final Krypton flag):** `LFSRISNOTRANDOM`
