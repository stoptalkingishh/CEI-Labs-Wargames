import os

# Define the dataset for Krypton Levels 0 to 6 based on OTW specifications
challenges_data = [
    {
        "id": "krypton-00",
        "name": "Krypton 0 -> 1: Base64 Decoding",
        "points": 200,
        "desc": "**Goal:** Decrypt the first password using Base64 decoding.\n\nWelcome to Krypton! The first level is easy. The following string encodes the password for level 1 using Base64:\n\n`S1JZUFRPTklTR1JFQVQ=`\n\nUse a Base64 decoder (like the `base64 -d` command) to find the flag.",
        "flag": "KRYPTONISGREAT"
    },
    {
        "id": "krypton-01",
        "name": "Krypton 1 -> 2: ROT13 Substitution Cipher",
        "points": 250,
        "desc": "**Goal:** Decrypt a classic Caesar cipher (ROT13).\n\nSSH into `krypton.labs.overthewire.org` on port `2231` (username: `krypton1`).\n\nThe password for level 2 is located in `/krypton/krypton1/krypton2`. It is encrypted with a simple ROT13 rotation cipher.\n\n*Hint: The `tr` command is very useful for translating characters (e.g., `tr \"[:alpha:]\" \"N-ZA-Mn-za-m\"`).*",
        "flag": "ROTTEN"
    },
    {
        "id": "krypton-02",
        "name": "Krypton 2 -> 3: Caesar Cipher (Unknown Shift)",
        "points": 300,
        "desc": "**Goal:** Determine the shift of a Caesar Cipher by encrypting known plaintext.\n\nSSH into `krypton.labs.overthewire.org` on port `2231` (username: `krypton2`).\n\nCreate a temp directory, symlink the `keyfile.dat`, and use the provided `encrypt` binary to encrypt a string of 'A's. Compare the output to figure out the key shift, then reverse it to read the next password.",
        "flag": "CAESARISEASY"
    },
    {
        "id": "krypton-03",
        "name": "Krypton 3 -> 4: Frequency Analysis",
        "points": 350,
        "desc": "**Goal:** Crack a substitution cipher using frequency analysis.\n\nSSH into `krypton.labs.overthewire.org` on port `2231` (username: `krypton3`).\n\nYou are given intercepted texts in English. Count the frequency of the letters to determine the substitution alphabet. \n\n*Hint: E, T, A, O, I, N are the most common letters in the English language.*",
        "flag": "BRUTE"
    },
    {
        "id": "krypton-04",
        "name": "Krypton 4 -> 5: Vigenère Cipher (Known Key Length)",
        "points": 400,
        "desc": "**Goal:** Decrypt a Vigenère cipher when you know the key length.\n\nSSH into `krypton.labs.overthewire.org` on port `2231` (username: `krypton4`).\n\nThe README tells you the key length is 6. You can brute-force common 6-letter words or use a Vigenère solver on the intercepted text to find the key, then use it to decode the password.",
        "flag": "CLEARTEXT"
    },
    {
        "id": "krypton-05",
        "name": "Krypton 5 -> 6: Vigenère Cipher (Kasiski Test)",
        "points": 450,
        "desc": "**Goal:** Decrypt a Vigenère cipher without knowing the key length.\n\nSSH into `krypton.labs.overthewire.org` on port `2231` (username: `krypton5`).\n\nUse the Kasiski examination method to find repeating patterns in the ciphertext. This will help you guess the key length (likely 3, 6, or 9). Once the length is known, apply frequency analysis to recover the key.",
        "flag": "RANDOM"
    },
    {
        "id": "krypton-06",
        "name": "Krypton 6 -> 7: Stream Cipher / LFSR",
        "points": 500,
        "desc": "**Goal:** Reverse a Linear-Feedback Shift Register (LFSR) stream cipher.\n\nSSH into `krypton.labs.overthewire.org` on port `2231` (username: `krypton6`).\n\nEncrypt long strings of identical characters (e.g., all 'A's) using the provided binary to find the repeating keystream pattern (it repeats every 30 characters). Map the integer differences and subtract them from the encrypted password to retrieve the final flag.",
        "flag": "LFSRISNOTRANDOM"
    }
]

# Generate folder and files relative to the repo root folder dynamically
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(script_dir, "..", "challenges"))

os.makedirs(base_dir, exist_ok=True)

for ch in challenges_data:
    folder_path = os.path.join(base_dir, ch["id"])
    os.makedirs(folder_path, exist_ok=True)
    
    escaped_desc = ch['desc'].replace('\n', '\n  ')
    yaml_content = f"""name: "{ch['name']}"
author: "OverTheWire"
category: "Cryptography"
description: |
  {escaped_desc}
value: {ch['points']}
type: standard
flags:
  - "{ch['flag']}"
state: visible
version: "0.1"
"""
    
    file_path = os.path.join(folder_path, "challenge.yml")
    with open(file_path, "w") as f:
        f.write(yaml_content)

print(f"Successfully generated {len(challenges_data)} Krypton challenges inside '{base_dir}'!")
