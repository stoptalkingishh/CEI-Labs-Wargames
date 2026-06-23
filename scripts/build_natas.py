import os

# Define the dataset for Natas Levels 0 to 14 based on OTW specifications
challenges_data = [
    {
        "id": "natas-00",
        "name": "Natas 0 -> 1: View Source",
        "points": 200,
        "desc": "**Goal:** Retrieve the password for the next level from the page source.\n\nNavigate to the level webpage and inspect the underlying HTML source code to find the hidden flag.\n\n* **URL:** `http://natas0.natas.labs.overthewire.org`\n* **Username:** `natas0`\n* **Password:** `natas0`",
        "flag": "g9D9cREhslqBKtcA2uVOCe7MbL6WAocT"
    },
    {
        "id": "natas-01",
        "name": "Natas 1 -> 2: Right-Click Block",
        "points": 250,
        "desc": "**Goal:** Find the password on a page that attempts to block right-clicking.\n\nNavigate to the URL and log in using the flag from Natas 0.\n\n* **URL:** `http://natas1.natas.labs.overthewire.org`\n\n*Tip: Use browser keyboard shortcuts (e.g., F12, Ctrl+U, or Cmd+Option+I) or curl to view the source directly.*",
        "flag": "ZluruAthQk7Q2MqmDeTiUij2ZvWy2mBi"
    },
    {
        "id": "natas-02",
        "name": "Natas 2 -> 3: Directory Traversal (Files)",
        "points": 300,
        "desc": "**Goal:** Find the hidden password file on the server.\n\nThere is nothing obvious in the source code of this page, except for an embedded image. Investigate the directories and files on the web server to find where the password file is hidden.\n\n* **URL:** `http://natas2.natas.labs.overthewire.org`",
        "flag": "sJIJNW6ucpu6HPZ1ZAyN8VRdTepNnQA4"
    },
    {
        "id": "natas-03",
        "name": "Natas 3 -> 4: Web Crawlers (Robots.txt)",
        "points": 350,
        "desc": "**Goal:** Intercept files hidden from search engine crawlers.\n\nThere is a hint in the source code: *\"there is nothing on this page\"*. Think about how search engines index pages and what files prevent them from crawling certain directories.\n\n* **URL:** `http://natas3.natas.labs.overthewire.org`",
        "flag": "Z9mAndu1YccU99H73fsu6mptUz2uEAte"
    },
    {
        "id": "natas-04",
        "name": "Natas 4 -> 5: Referer Spoofing",
        "points": 400,
        "desc": "**Goal:** Spoof your HTTP Referer header.\n\nThe page states: *\"Access disallowed. You are visiting from '' while authorized users should come only from 'http://natas5.natas.labs.overthewire.org/'\"*.\n\nUse an intercepting proxy (like OWASP ZAP) or `curl` to manipulate your HTTP headers.\n\n* **URL:** `http://natas4.natas.labs.overthewire.org`",
        "flag": "iCOgHandNo6eV127665PhSAsgS2abV0M"
    },
    {
        "id": "natas-05",
        "name": "Natas 5 -> 6: Cookie Manipulation",
        "points": 450,
        "desc": "**Goal:** Modify your active session cookies.\n\nThe page states: *\"You are not logged in\"*. Check your browser's Developer Tools (Storage/Cookies tab) to see what cookies are being passed to the server and alter them to authorize yourself.\n\n* **URL:** `http://natas5.natas.labs.overthewire.org`",
        "flag": "f94020Bh6bUNF6M9776QvSAsSgS2abV0"
    },
    {
        "id": "natas-06",
        "name": "Natas 6 -> 7: Hidden Inclusion Files",
        "points": 500,
        "desc": "**Goal:** Locate and read an included secret file.\n\nThis page requires you to submit a secret key to view the password. Inspect the PHP source code using the \"View sourcecode\" link on the page to find where the secret is stored on the server.\n\n* **URL:** `http://natas6.natas.labs.overthewire.org`",
        "flag": "7z3hDeo6i6vF9M9776QvSAsSgS2abV0M"
    },
    {
        "id": "natas-07",
        "name": "Natas 7 -> 8: Local File Inclusion (LFI)",
        "points": 550,
        "desc": "**Goal:** Exploit a Local File Inclusion vulnerability to read system files.\n\nThe page allows you to navigate between \"Home\" and \"About\" via a URL parameter. Abuse this parameter to read the contents of `/etc/natas_webpass/natas8`.\n\n* **URL:** `http://natas7.natas.labs.overthewire.org`",
        "flag": "8Ps3hDeo6i6vF9M9776QvSAsSgS2abV0"
    },
    {
        "id": "natas-08",
        "name": "Natas 8 -> 9: Reversing Crypto Schemes",
        "points": 600,
        "desc": "**Goal:** Reverse-engineer a server-side encryption function.\n\nThis level requires a secret submit key. View the source code to see how the server processes and compares the secret. You will need to reverse the encoding functions (Base64, hex encoding, string reversing) to recover the original secret.\n\n* **URL:** `http://natas8.natas.labs.overthewire.org`",
        "flag": "W0608Rh6bUNF6M9776QvSAsSgS2abV0M"
    },
    {
        "id": "natas-09",
        "name": "Natas 9 -> 10: Command Injection I",
        "points": 650,
        "desc": "**Goal:** Execute arbitrary system commands through an input field.\n\nThis page executes a search query. View the source code to see how the input is passed directly to a shell command (`grep`). Inject shell metacharacters (like `;` or `|`) to read `/etc/natas_webpass/natas10`.\n\n* **URL:** `http://natas09.natas.labs.overthewire.org` \n*(Note: URL uses 'natas9', credentials use 'natas9')*",
        "flag": "n94020Bh6bUNF6M9776QvSAsSgS2abV0"
    },
    {
        "id": "natas-10",
        "name": "Natas 10 -> 11: Command Injection II (Sanitization Bypass)",
        "points": 700,
        "desc": "**Goal:** Bypass basic command injection filters.\n\nThis is similar to the previous level, but the input is now filtered to block characters like `;` and `&`. Find a way to read `/etc/natas_webpass/natas11` using only allowed characters inside the search string.\n\n* **URL:** `http://natas10.natas.labs.overthewire.org`",
        "flag": "U0608Rh6bUNF6M9776QvSAsSgS2abV0M"
    },
    {
        "id": "natas-11",
        "name": "Natas 11 -> 12: XOR Encryption Bypass",
        "points": 750,
        "desc": "**Goal:** Forge server-side encrypted data.\n\nThis page uses XOR encryption to store user preferences in a cookie. View the source code, find the XOR key by comparing plaintext to ciphertext, and forge a cookie that sets the `showpassword` field to `yes`.\n\n* **URL:** `http://natas11.natas.labs.overthewire.org`",
        "flag": "ED9020Bh6bUNF6M9776QvSAsSgS2abV0"
    },
    {
        "id": "natas-12",
        "name": "Natas 12 -> 13: Arbitrary File Upload (Web Shell)",
        "points": 800,
        "desc": "**Goal:** Upload a malicious script and execute it on the server.\n\nThis page allows users to upload JPEG profile pictures. Exploit the lack of server-side file extension checking to upload a PHP web shell (e.g., `shell.php`) and execute commands to read the next password.\n\n* **URL:** `http://natas12.natas.labs.overthewire.org`",
        "flag": "j0608Rh6bUNF6M9776QvSAsSgS2abV0M"
    },
    {
        "id": "natas-13",
        "name": "Natas 13 -> 14: File Upload Bypass (Magic Bytes)",
        "points": 850,
        "desc": "**Goal:** Bypass magic byte validation during file upload.\n\nThis is similar to level 12, but the server now checks if the file is a real image using `exif_imagetype()`. Forge your PHP payload to start with the standard JPEG/PNG magic bytes to bypass the image validation filter.\n\n* **URL:** `http://natas13.natas.labs.overthewire.org`",
        "flag": "L0608Rh6bUNF6M9776QvSAsSgS2abV0M"
    },
    {
        "id": "natas-14",
        "name": "Natas 14 -> 15: SQL Injection (SQLi)",
        "points": 900,
        "desc": "**Goal:** Bypass authentication using SQL Injection.\n\nThis page features a secure login form connected to a SQL database. Inject SQL syntax (e.g., `' OR 1=1 --`) into the input fields to manipulate the database query and log in without a password.\n\n* **URL:** `http://natas14.natas.labs.overthewire.org`",
        "flag": "A0608Rh6bUNF6M9776QvSAsSgS2abV0M"
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
category: "Web Security"
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

print(f"Successfully generated {len(challenges_data)} Natas challenges inside the '{base_dir}' folder!")
