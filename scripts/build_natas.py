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

# A player's connection details (attacker host/port, live status) come
# from the "Launch Environment" control on this challenge itself --
# injected into the challenge view by cei-labs-engine's instance-launcher
# plugin, not written into these descriptions, since the port is only
# known once an instance actually exists. See the "Natas: Start Here"
# challenge for how that control works, and for an explanation of the
# two-hop model this note summarizes below.
#
# Natas is target-attacker, not single-target: everything happens FROM
# inside your attacker workstation (reachable via noVNC or SSH, both shown
# on the launch panel) -- the targets are never reachable directly. All 15
# levels share ONE attacker and ONE target box; each level is just a
# different port (8000 + level number) on that same target, matching the
# real OverTheWire Natas layout. TARGET_NOTE is repeated verbatim in every
# level below so it stands on its own even if a player skips the "Start
# Here" challenge or the injected UI fails to load for any reason.
TARGET_NOTE = (
    "Everything below happens from inside your attacker workstation, not "
    "your own machine -- open it via noVNC or SSH from this challenge's "
    "launch panel first, then reach the target from there at"
)

# Define the dataset for Natas Levels 0 to 14 based on OTW specifications
challenges_data = [
    {
        "id": "natas-start-here",
        "name": "Natas: Start Here",
        "points": 10,
        "desc": (
            "**Goal:** Learn the launch controls, then prove you used them.\n\n"
            "Natas works differently from Bandit and Krypton: launching gives you a shared "
            "**attacker workstation**, not a direct connection to a target. Every one of "
            "Natas's 15 targets is reachable only from inside that workstation -- never "
            "directly from your own machine. The launch control attached to this (and every "
            "other Natas) challenge offers:\n"
            "- **Launch Environment** -- starts your attacker workstation and this track's "
            "shared target box (all 15 levels share one target, distinguished by port). "
            "Shows both a noVNC link (a full desktop in your browser) and an SSH connection.\n"
            "- **Reboot Host** -- restarts your attacker in place if it gets stuck.\n"
            "- **Relaunch Environment** -- destroys and recreates your whole range (attacker "
            "and target) from scratch. Use this if something's broken beyond a reboot.\n"
            "- **+5 more minutes** -- shows up only once every level in this track is solved "
            "and a shutdown countdown has started.\n\n"
            "Click Launch, open the attacker workstation (noVNC or SSH, your choice), and "
            "from inside it browse to `http://<target-host>:8000/welcome.txt` (the same "
            "target host every Natas level uses, just this one extra file). Submit its "
            "contents as your flag."
        ),
        "flag": "WELCOME_TO_NATAS"
    },
    {
        "id": "natas-00",
        "name": "Natas 0 -> 1: View Source",
        "points": 200,
        "desc": f"**Goal:** Retrieve the password for the next level from the page source.\n\n{TARGET_NOTE} `http://<target-host>:8000/`. Username: `natas0`, password: `natas0`.\n\nView the page's HTML source to find the hidden flag.",
        "flag": "g9D9cREhslqBKtcA2uVOCe7MbL6WAocT"
    },
    {
        "id": "natas-01",
        "name": "Natas 1 -> 2: Right-Click Block",
        "points": 250,
        "desc": f"**Goal:** Find the password on a page that blocks right-clicking.\n\n{TARGET_NOTE} `http://<target-host>:8001/`. Log in as `natas1` using the flag from Natas 0 as your password.\n\nBlocking right-click doesn't block view-source or devtools -- or just `curl` the page directly.",
        "flag": "ZluruAthQk7Q2MqmDeTiUij2ZvWy2mBi"
    },
    {
        "id": "natas-02",
        "name": "Natas 2 -> 3: Directory Traversal (Files)",
        "points": 300,
        "desc": f"**Goal:** Find a password file the page never links to.\n\n{TARGET_NOTE} `http://<target-host>:8002/`. Log in as `natas2` using the flag from Natas 1 as your password.\n\nThe page source only reveals an embedded image path. Explore the directory that image lives in to find where the password file is hidden.",
        "flag": "sJIJNW6ucpu6HPZ1ZAyN8VRdTepNnQA4"
    },
    {
        "id": "natas-03",
        "name": "Natas 3 -> 4: Web Crawlers (Robots.txt)",
        "points": 350,
        "desc": f"**Goal:** Find a path deliberately hidden from search engines.\n\n{TARGET_NOTE} `http://<target-host>:8003/`. Log in as `natas3` using the flag from Natas 2 as your password.\n\nThe page source hints \"there is nothing on this page\" -- but a file exists specifically to tell crawlers what NOT to index. Check it.",
        "flag": "Z9mAndu1YccU99H73fsu6mptUz2uEAte"
    },
    {
        "id": "natas-04",
        "name": "Natas 4 -> 5: Referer Spoofing",
        "points": 400,
        "desc": f"**Goal:** Forge an HTTP header to satisfy an access check.\n\n{TARGET_NOTE} `http://<target-host>:8004/`. Log in as `natas4` using the flag from Natas 3 as your password.\n\nThe page only allows visitors arriving from the NEXT level's own URL -- a page you can't naturally have come from. Forge the `Referer` header (curl's `-e`/`--referer`, or an intercepting proxy) to satisfy the check.",
        "flag": "iCOgHandNo6eV127665PhSAsgS2abV0M"
    },
    {
        "id": "natas-05",
        "name": "Natas 5 -> 6: Cookie Manipulation",
        "points": 450,
        "desc": f"**Goal:** Edit a session cookie to change your authorization state.\n\n{TARGET_NOTE} `http://<target-host>:8005/`. Log in as `natas5` using the flag from Natas 4 as your password.\n\nThe page claims you're not logged in. Inspect the cookie it sets and change its value to authorize yourself.",
        "flag": "f94020Bh6bUNF6M9776QvSAsSgS2abV0"
    },
    {
        "id": "natas-06",
        "name": "Natas 6 -> 7: Hidden Inclusion Files",
        "points": 500,
        "desc": f"**Goal:** Read server-side source to find where a secret is stored, then fetch it directly.\n\n{TARGET_NOTE} `http://<target-host>:8006/`. Log in as `natas6` using the flag from Natas 5 as your password.\n\nThe page wants a secret key. Its \"View sourcecode\" link shows where that secret actually lives on the server -- fetch that file directly.",
        "flag": "7z3hDeo6i6vF9M9776QvSAsSgS2abV0M"
    },
    {
        "id": "natas-07",
        "name": "Natas 7 -> 8: Local File Inclusion (LFI)",
        "points": 550,
        "desc": f"**Goal:** Abuse a page-selection parameter to read an arbitrary file.\n\n{TARGET_NOTE} `http://<target-host>:8007/`. Log in as `natas7` using the flag from Natas 6 as your password.\n\nThe page switches between \"Home\" and \"About\" via a URL parameter naming the file to include. Point that parameter at `/etc/natas_webpass/natas8` instead.",
        "flag": "8Ps3hDeo6i6vF9M9776QvSAsSgS2abV0"
    },
    {
        "id": "natas-08",
        "name": "Natas 8 -> 9: Reversing Crypto Schemes",
        "points": 600,
        "desc": f"**Goal:** Reverse a server-side encoding chain to recover a secret.\n\n{TARGET_NOTE} `http://<target-host>:8008/`. Log in as `natas8` using the flag from Natas 7 as your password.\n\nThe page requires a secret key, shown only in encoded form. View the source to see the encoding chain (base64, then reversed, then hex), and reverse it to recover the original secret.",
        "flag": "W0608Rh6bUNF6M9776QvSAsSgS2abV0M"
    },
    {
        "id": "natas-09",
        "name": "Natas 9 -> 10: Command Injection I",
        "points": 650,
        "desc": f"**Goal:** Inject a shell command through an unsanitized input field.\n\n{TARGET_NOTE} `http://<target-host>:8009/`. Log in as `natas9` using the flag from Natas 8 as your password.\n\nThe page's search box is passed straight into a shell `grep` command (visible in the source). Inject a shell metacharacter (like `;`) to run your own command and read `/etc/natas_webpass/natas10`.",
        "flag": "n94020Bh6bUNF6M9776QvSAsSgS2abV0"
    },
    {
        "id": "natas-10",
        "name": "Natas 10 -> 11: Command Injection II (Sanitization Bypass)",
        "points": 700,
        "desc": f"**Goal:** Achieve the same result once the easy metacharacters are filtered.\n\n{TARGET_NOTE} `http://<target-host>:8010/`. Log in as `natas10` using the flag from Natas 9 as your password.\n\nSame underlying `grep` command as before, but `;` and `&` are now blocked. `grep` itself accepts a second filename argument on its own command line -- use that instead of a shell metacharacter to read `/etc/natas_webpass/natas11`.",
        "flag": "U0608Rh6bUNF6M9776QvSAsSgS2abV0M"
    },
    {
        "id": "natas-11",
        "name": "Natas 11 -> 12: XOR Encryption Bypass",
        "points": 750,
        "desc": f"**Goal:** Recover an XOR key and forge encrypted data with it.\n\n{TARGET_NOTE} `http://<target-host>:8011/`. Log in as `natas11` using the flag from Natas 10 as your password.\n\nPreferences are stored in a cookie XOR-encrypted with a short repeating key. The logged-out default plaintext is predictable -- XOR it against the default ciphertext to recover the key, then forge a cookie with `showpassword` set to `yes`.",
        "flag": "ED9020Bh6bUNF6M9776QvSAsSgS2abV0"
    },
    {
        "id": "natas-12",
        "name": "Natas 12 -> 13: Arbitrary File Upload (Web Shell)",
        "points": 800,
        "desc": f"**Goal:** Upload and execute a web shell.\n\n{TARGET_NOTE} `http://<target-host>:8012/`. Log in as `natas12` using the flag from Natas 11 as your password.\n\nThe upload form performs no real validation. Upload a one-line PHP web shell and request it directly to read the next password.",
        "flag": "j0608Rh6bUNF6M9776QvSAsSgS2abV0M"
    },
    {
        "id": "natas-13",
        "name": "Natas 13 -> 14: File Upload Bypass (Magic Bytes)",
        "points": 850,
        "desc": f"**Goal:** Get a PHP payload past a file-type check based on content, not extension.\n\n{TARGET_NOTE} `http://<target-host>:8013/`. Log in as `natas13` using the flag from Natas 12 as your password.\n\nSame upload flow as the previous level, but the server now checks the file's actual bytes (`exif_imagetype()`). Prepend a real image header (e.g. `GIF89a`) before your PHP payload -- PHP still executes everything from `<?php` onward regardless of what precedes it.",
        "flag": "L0608Rh6bUNF6M9776QvSAsSgS2abV0M"
    },
    {
        "id": "natas-14",
        "name": "Natas 14 -> 15: SQL Injection (SQLi)",
        "points": 900,
        "desc": f"**Goal:** Bypass a login form using SQL injection.\n\n{TARGET_NOTE} `http://<target-host>:8014/`. Log in as `natas14` using the flag from Natas 13 as your password.\n\nThis is the final Natas level. The login form builds its SQL query with raw string concatenation. Inject SQL syntax (e.g. `\" OR \"1\"=\"1`) into either field to bypass the check and reveal the final flag.",
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
