import os

# Define the dataset for Krypton Levels 0 to 6 based on OTW specifications
challenges_data = [
    {
        "id": "krypton-00",
        "name": "Krypton 0 -> 1: Base64 Decoding",
        "points": 200,
        "desc": "**Goal:** Decrypt the first password using Base64 decoding.\n\nWelcome to Krypton! The first level is easy. The following string encodes the password for level 1 using Base64:\n\n```text\nS1JZUFRPTklTR1JFQVQ=\n```\n\nDecode this string to find the password, then log in to the next level.\n\n**Connection Information:**\n* **Host:** `krypton.labs.overthewire.org`\n* **Port:** `2231`\n* **Username:** `krypton1`\n* **Password:** (The decoded string)",
        "flag": "KRYPTONISGREAT"
    },
    {
        "id": "krypton-01",
        "name": "Krypton 1 -> 2: Caesar Rotations",
        "points": 300,
        "desc": "SSH into `krypton.labs.overthewire.org` on port `2231` using username `krypton1`.\n\nThe password for level 2 is in the file **'krypton2'** inside the home directory. It is encrypted using a simple rotation cipher (ROT). \n\nNote that the ciphertext preserves plaintext word boundaries to help you analyze the shift. Decrypt the file contents to get the next flag.",
        "flag": "ROTTEN"
    },
    {
        "id": "krypton-02",
        "name": "Krypton 2 -> 3: Caesar's Shift Program",
        "points": 400,
        "desc": "SSH into `krypton.labs.overthewire.org` on port `2231` using username `krypton2`.\n\nThe password for level 3 is in the file **krypton3**. It is in a 5-letter group ciphertext format, encrypted with a Caesar Cipher.\n\nYou do not have direct access to the key, but you have access to a program called `encrypt` in `/krypton/krypton2/` that will encrypt anything you pass to it using the same key. \n\n**Hint:**\nThe `encrypt` binary looks for `keyfile.dat` in your current working directory. Create a temporary directory in `/tmp`, link to the keyfile, grant permissions, and run the tool:\n```bash\nmktemp -d\ncd /tmp/tmp.XXXXXX\nln -s /krypton/krypton2/keyfile.dat\nchmod 777 .\n/krypton/krypton2/encrypt /etc/issue\n```",
        "flag": "CAESARISEASY"
    },
    {
        "id": "krypton-03",
        "name": "Krypton 3 -> 4: Frequency Analysis",
        "points": 500,
        "desc": "SSH into `krypton.labs.overthewire.org` on port `2231` using username `krypton3`.\n\nYou have intercepted several encrypted messages (`found1`, `found2`, `found3`) encrypted with the same key. The password to the next level is in the file **krypton4**.\n\nUse **Frequency Analysis** to map the ciphertext letters back to English. Plaintexts are in American English. Analyze the letter distributions to crack the monoalphabetic substitution cipher.",
        "flag": "BRUTE"
    },
    {
        "id": "krypton-04",
        "name": "Krypton 4 -> 5: Vigenère Cipher (Known Length)",
        "points": 600,
        "desc": "SSH into `krypton.labs.overthewire.org` on port `2231` using username `krypton4`.\n\nThis level introduces polyalphabetic substitution via a **Vigenère Cipher**.\n\nYou have intercepted two longer English messages. Crucially, you know that the **key length is 6**.\n\nThe password to level 5 is in the usual place, encrypted with this 6-letter repeating key. Determine the key and decode the password.",
        "flag": "CLEARTEXT"
    },
    {
        "id": "krypton-05",
        "name": "Krypton 5 -> 6: Vigenère Cipher (Unknown Length)",
        "points": 700,
        "desc": "SSH into `krypton.labs.overthewire.org` on port `2231` using username `krypton5`.\n\nThis is another polyalphabetic Vigenère Cipher challenge, but this time **the key length is unknown**.\n\nUse index of coincidence or Kasiski examination to find the key length, then perform frequency analysis on each sliced subset of the ciphertext to retrieve the password from the **krypton6** file.",
        "flag": "KEYLENGTH"
    },
    {
        "id": "krypton-06",
        "name": "Krypton 6 -> 7: Stream Ciphers & Randomness",
        "points": 800,
        "desc": "SSH into `krypton.labs.overthewire.org` on port `2231` using username `krypton6`.\n\nModern ciphers attempt to create an on-the-fly 'random' keystream to encrypt incoming plaintext one byte at a time (Stream Ciphers). Typically, the key byte is XOR'd with the plaintext.\n\nThe binary `encrypt6` in your directory will read the keyfile (which you cannot read) and encrypt any message you desire using the key AND a pseudo-random number generator (PRNG).\n\nPerform a **known-ciphertext attack** by introducing plaintext of your choice. The challenge is not simple, but the PRNG is mathematically weak. Crack the PRNG to decrypt the password for level 7.",
        "flag": "RANDOM"
    }
]

# Generate folder and files
base_dir = "../challenges"
os.makedirs(base_dir, exist_ok=True)

for ch in challenges_data:
    folder_path = os.path.join(base_dir, ch["id"])
    os.makedirs(folder_path, exist_ok=True)
    
    yaml_content = f"""name: "{ch['name']}"
author: "OverTheWire"
category: "Cryptography"
description: |
  {ch['desc'].replace(chr(10), chr(10) + '  ')}
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

print(f"Successfully generated {len(challenges_data)} Krypton challenges inside the '{base_dir}' folder!")
