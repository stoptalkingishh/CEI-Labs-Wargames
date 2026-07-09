import os

# Self-hosted image references (see docs/self-hosted-wargames-blueprint.md
# Phase 4's "Wire Natas into CTFd" task). Neither is published by a CI
# workflow yet -- until it is, build+tag locally with these exact names
# before deploying:
#   docker build -t ghcr.io/stoptalkingishh/cei-labs-wargames/natas-target:latest targets/natas
# attacker_image is cei-labs-engine's own extended kali-novnc image (per
# resolved Decision 2 -- not a new separate image), not something this
# repo builds.
NATAS_TARGET_IMAGE = "ghcr.io/stoptalkingishh/cei-labs-wargames/natas-target:latest"
NATAS_ATTACKER_IMAGE = "ghcr.io/stoptalkingishh/cei-labs-engine/ctf-kali-novnc:latest"

# All 15 challenges share ONE instance_group -- launching any of them
# creates/reuses the SAME per-team range (one shared attacker + this
# level's target, joined only to that range's private network). Only the
# final level opts into shutdown_on_solve.
INSTANCE_GROUP = "natas"

CONNECT_NOTE = (
    "Launch your Natas environment from this challenge (shared across all "
    "Natas levels -- launching any one of them starts the same range: one "
    "attacker workstation plus this level's target). Connect to your "
    "attacker via the noVNC link CTFd shows you (a full desktop in your "
    "browser). From there, the target for this level is reachable at"
)

# Define the dataset for Natas Levels 0 to 14 based on OTW specifications
challenges_data = [
    {
        "id": "natas-00",
        "name": "Natas 0 -> 1: View Source",
        "points": 200,
        "desc": f"**Goal:** Retrieve the password for the next level from the page source.\n\n{CONNECT_NOTE} `http://<target-host>:8000/`.\nUsername: `natas0`\nPassword: `natas0`\n\nInspect the underlying HTML source code to find the hidden flag.",
        "flag": "g9D9cREhslqBKtcA2uVOCe7MbL6WAocT"
    },
    {
        "id": "natas-01",
        "name": "Natas 1 -> 2: Right-Click Block",
        "points": 250,
        "desc": f"**Goal:** Find the password on a page that attempts to block right-clicking.\n\n{CONNECT_NOTE} `http://<target-host>:8001/`. Log in as `natas1` using the flag from Natas 0 as your password.\n\n*Tip: Use browser devtools/view-source, or just `curl` the page directly.*",
        "flag": "ZluruAthQk7Q2MqmDeTiUij2ZvWy2mBi"
    },
    {
        "id": "natas-02",
        "name": "Natas 2 -> 3: Directory Traversal (Files)",
        "points": 300,
        "desc": f"**Goal:** Find the hidden password file on the server.\n\n{CONNECT_NOTE} `http://<target-host>:8002/`. Log in as `natas2` using the flag from Natas 1 as your password.\n\nThere is nothing obvious in the page source except an embedded image. Investigate the directories and files on the web server to find where the password file is hidden.",
        "flag": "sJIJNW6ucpu6HPZ1ZAyN8VRdTepNnQA4"
    },
    {
        "id": "natas-03",
        "name": "Natas 3 -> 4: Web Crawlers (Robots.txt)",
        "points": 350,
        "desc": f"**Goal:** Intercept files hidden from search engine crawlers.\n\n{CONNECT_NOTE} `http://<target-host>:8003/`. Log in as `natas3` using the flag from Natas 2 as your password.\n\nThere is a hint in the source code: *\"there is nothing on this page\"*. Think about how search engines index pages and what file tells them what NOT to crawl.",
        "flag": "Z9mAndu1YccU99H73fsu6mptUz2uEAte"
    },
    {
        "id": "natas-04",
        "name": "Natas 4 -> 5: Referer Spoofing",
        "points": 400,
        "desc": f"**Goal:** Spoof your HTTP Referer header.\n\n{CONNECT_NOTE} `http://<target-host>:8004/`. Log in as `natas4` using the flag from Natas 3 as your password.\n\nThe page says access is only allowed from the NEXT level's own URL -- a page you can't naturally arrive from. Forge the `Referer` header (curl's `-e`/`--referer` flag, or an intercepting proxy) to get in.",
        "flag": "iCOgHandNo6eV127665PhSAsgS2abV0M"
    },
    {
        "id": "natas-05",
        "name": "Natas 5 -> 6: Cookie Manipulation",
        "points": 450,
        "desc": f"**Goal:** Modify your active session cookies.\n\n{CONNECT_NOTE} `http://<target-host>:8005/`. Log in as `natas5` using the flag from Natas 4 as your password.\n\nThe page says you're not logged in. Check what cookie it sets and alter it to authorize yourself.",
        "flag": "f94020Bh6bUNF6M9776QvSAsSgS2abV0"
    },
    {
        "id": "natas-06",
        "name": "Natas 6 -> 7: Hidden Inclusion Files",
        "points": 500,
        "desc": f"**Goal:** Locate and read an included secret file.\n\n{CONNECT_NOTE} `http://<target-host>:8006/`. Log in as `natas6` using the flag from Natas 5 as your password.\n\nThe page wants a secret key. Use the \"View sourcecode\" link to find where the secret is stored on the server, then fetch that file directly.",
        "flag": "7z3hDeo6i6vF9M9776QvSAsSgS2abV0M"
    },
    {
        "id": "natas-07",
        "name": "Natas 7 -> 8: Local File Inclusion (LFI)",
        "points": 550,
        "desc": f"**Goal:** Exploit a Local File Inclusion vulnerability to read system files.\n\n{CONNECT_NOTE} `http://<target-host>:8007/`. Log in as `natas7` using the flag from Natas 6 as your password.\n\nThe page navigates between \"Home\" and \"About\" via a URL parameter. Abuse this parameter to read the contents of `/etc/natas_webpass/natas8`.",
        "flag": "8Ps3hDeo6i6vF9M9776QvSAsSgS2abV0"
    },
    {
        "id": "natas-08",
        "name": "Natas 8 -> 9: Reversing Crypto Schemes",
        "points": 600,
        "desc": f"**Goal:** Reverse-engineer a server-side encoding function.\n\n{CONNECT_NOTE} `http://<target-host>:8008/`. Log in as `natas8` using the flag from Natas 7 as your password.\n\nThe page requires a secret submit key and shows only its ENCODED form. View the source to see how it's encoded (base64 -> reverse -> hex), then reverse the chain to recover the original secret.",
        "flag": "W0608Rh6bUNF6M9776QvSAsSgS2abV0M"
    },
    {
        "id": "natas-09",
        "name": "Natas 9 -> 10: Command Injection I",
        "points": 650,
        "desc": f"**Goal:** Execute arbitrary system commands through an input field.\n\n{CONNECT_NOTE} `http://<target-host>:8009/`. Log in as `natas9` using the flag from Natas 8 as your password.\n\nThe page runs a search query. View the source to see the input is passed directly to a shell command (`grep`). Inject shell metacharacters (like `;`) to read `/etc/natas_webpass/natas10`.",
        "flag": "n94020Bh6bUNF6M9776QvSAsSgS2abV0"
    },
    {
        "id": "natas-10",
        "name": "Natas 10 -> 11: Command Injection II (Sanitization Bypass)",
        "points": 700,
        "desc": f"**Goal:** Bypass basic command injection filters.\n\n{CONNECT_NOTE} `http://<target-host>:8010/`. Log in as `natas10` using the flag from Natas 9 as your password.\n\nSame `grep` pattern as the previous level, but shell metacharacters like `;` and `&` are now blocked. `grep` itself takes a second filename argument -- find a way to read `/etc/natas_webpass/natas11` without needing any blocked character.",
        "flag": "U0608Rh6bUNF6M9776QvSAsSgS2abV0M"
    },
    {
        "id": "natas-11",
        "name": "Natas 11 -> 12: XOR Encryption Bypass",
        "points": 750,
        "desc": f"**Goal:** Forge server-side encrypted data.\n\n{CONNECT_NOTE} `http://<target-host>:8011/`. Log in as `natas11` using the flag from Natas 10 as your password.\n\nThe page stores preferences in a cookie XOR-encrypted with a short repeating key. The logged-out default plaintext is knowable -- XOR it against the default ciphertext to recover the key, then forge a cookie with `showpassword` set to `yes`.",
        "flag": "ED9020Bh6bUNF6M9776QvSAsSgS2abV0"
    },
    {
        "id": "natas-12",
        "name": "Natas 12 -> 13: Arbitrary File Upload (Web Shell)",
        "points": 800,
        "desc": f"**Goal:** Upload a malicious script and execute it on the server.\n\n{CONNECT_NOTE} `http://<target-host>:8012/`. Log in as `natas12` using the flag from Natas 11 as your password.\n\nThe upload form performs no real validation at all. Upload a one-line PHP web shell and request it directly to read the next password.",
        "flag": "j0608Rh6bUNF6M9776QvSAsSgS2abV0M"
    },
    {
        "id": "natas-13",
        "name": "Natas 13 -> 14: File Upload Bypass (Magic Bytes)",
        "points": 850,
        "desc": f"**Goal:** Bypass magic-byte validation during file upload.\n\n{CONNECT_NOTE} `http://<target-host>:8013/`. Log in as `natas13` using the flag from Natas 12 as your password.\n\nSame as the previous level, but the server now checks the file's actual bytes (`exif_imagetype()`). Prepend a real image header (e.g. `GIF89a`) before your PHP payload -- PHP doesn't care what precedes `<?php` as long as it's still there.",
        "flag": "L0608Rh6bUNF6M9776QvSAsSgS2abV0M"
    },
    {
        "id": "natas-14",
        "name": "Natas 14 -> 15: SQL Injection (SQLi)",
        "points": 900,
        "desc": f"**Goal:** Bypass authentication using SQL Injection.\n\n{CONNECT_NOTE} `http://<target-host>:8014/`. Log in as `natas14` using the flag from Natas 13 as your password.\n\nThis is the FINAL Natas level. The login form builds its SQL query via raw string concatenation. Inject SQL syntax (e.g. `\" OR \"1\"=\"1`) into either field to bypass the check entirely and reveal the final flag.",
        "flag": "A0608Rh6bUNF6M9776QvSAsSgS2abV0M"
    }
]

# Generate folder and files
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(script_dir, "..", "challenges"))
os.makedirs(base_dir, exist_ok=True)

for i, ch in enumerate(challenges_data):
    folder_path = os.path.join(base_dir, ch["id"])
    os.makedirs(folder_path, exist_ok=True)

    is_final_level = (i == len(challenges_data) - 1)
    yaml_content = f"""name: "{ch['name']}"
author: "CEI Labs (self-hosted recreation of OverTheWire's Natas)"
category: "Web Security"
description: |
  {ch['desc'].replace(chr(10), chr(10) + '  ')}
value: {ch['points']}
type: standard
flags:
  - "{ch['flag']}"
state: visible
version: "0.1"
instance_type: target-attacker
target_image: {NATAS_TARGET_IMAGE}
attacker_image: {NATAS_ATTACKER_IMAGE}
instance_group: {INSTANCE_GROUP}
shutdown_on_solve: {"true" if is_final_level else "false"}
"""

    file_path = os.path.join(folder_path, "challenge.yml")
    with open(file_path, "w") as f:
        f.write(yaml_content)

print(f"Successfully generated {len(challenges_data)} Natas challenges inside the '{base_dir}' folder!")
