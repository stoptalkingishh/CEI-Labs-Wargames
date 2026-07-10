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
        "desc": (
            "**Goal:** Exploit a Local File Inclusion (LFI) vulnerability to read a file the application was "
            "never meant to serve.\n\n"
            f"{TARGET_NOTE} `http://<target-host>:8007/`. Log in as `natas7` using the flag from Natas 6 as your password."
        ),
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
        "desc": f"**Goal:** Get a PHP payload past a file-type check based on content, not extension.\n\n{TARGET_NOTE} `http://<target-host>:8013/`. Log in as `natas13` using the flag from Natas 12 as your password.\n\nSame upload flow as the previous level, but the server now checks the file's actual bytes (`exif_imagetype()`) rather than its name or extension.",
        "flag": "L0608Rh6bUNF6M9776QvSAsSgS2abV0M"
    },
    {
        "id": "natas-14",
        "name": "Natas 14 -> 15: SQL Injection (SQLi)",
        "points": 900,
        "desc": f"**Goal:** Bypass a login form using SQL injection.\n\n{TARGET_NOTE} `http://<target-host>:8014/`. Log in as `natas14` using the flag from Natas 13 as your password.\n\nThis is the final Natas level. The login form builds its SQL query with raw string concatenation from your username and password fields.",
        "flag": "A0608Rh6bUNF6M9776QvSAsSgS2abV0M"
    }
]

# "Commands you may need" + "Helpful reading" shown directly in the
# description, free -- matching OverTheWire's own real page structure
# (see build_bandit.py's EXTRA_INFO comment for the full rationale).
EXTRA_INFO = {
    "natas-00": (["curl", "browser view-source"], []),
    "natas-01": (["curl", "browser view-source"], []),
    "natas-02": (["curl"], []),
    "natas-03": (["curl"], [("Robots exclusion standard on Wikipedia", "https://en.wikipedia.org/wiki/Robots.txt")]),
    "natas-04": (["curl"], []),
    "natas-05": (["curl", "browser devtools"], []),
    "natas-06": (["browser view-source", "curl"], []),
    "natas-07": (["curl", "browser view-source"], [("File inclusion vulnerability on Wikipedia", "https://en.wikipedia.org/wiki/File_inclusion_vulnerability")]),
    "natas-08": (["browser view-source", "base64", "xxd"], []),
    "natas-09": (["browser view-source", "curl"], []),
    "natas-10": (["browser view-source", "curl"], []),
    "natas-11": (["browser devtools", "base64", "xxd"], [("XOR cipher on Wikipedia", "https://en.wikipedia.org/wiki/XOR_cipher")]),
    "natas-12": (["browser view-source", "curl"], []),
    "natas-13": (["browser view-source", "curl"], []),
    "natas-14": (["browser view-source"], [("SQL injection on Wikipedia", "https://en.wikipedia.org/wiki/SQL_injection")]),
}

# One real, technique-specific hint per level (not natas-start-here --
# its description is already a full walkthrough). See build_bandit.py's
# HINTS comment for the quoting constraint (no literal double-quotes --
# note this rules out double-quote-style SQLi/JSON payloads in hint text,
# use single-quote syntax instead).
HINTS = {
    "natas-00": [
        ("`man curl`.", 15),
        ("Web pages sometimes leave notes for developers directly in the HTML that never show up in the rendered page -- these are HTML comments, marked with `<!--` and `-->`, invisible in a normal browser view but fully readable in the raw source. Both a browser's view-source and `curl` show you the raw HTML.", 100),
        ("`curl http://<target-host>:8000/` (or Ctrl+U in a browser) prints the raw HTML -- look for an HTML comment (`<!-- ... -->`) in it. The password is written directly inside one.", 150),
    ],
    "natas-01": [
        ("`man curl`.", 15),
        ("Right-click/context-menu blocking is implemented in JavaScript that runs inside YOUR browser -- it can only interfere with browser UI, never with how the underlying page content is actually retrieved. A browser's view-source mode, or a command-line HTTP client, both bypass browser-level UI restrictions entirely.", 175),
        ("Bypass the block entirely by not using the browser's right-click menu at all: view-source (`view-source:http://<target-host>:8001/` in the address bar, or Ctrl+U) or a plain `curl http://<target-host>:8001/` both retrieve the exact same HTML the JavaScript is trying to protect -- the password is in an HTML comment, same pattern as the level before.", 187),
    ],
    "natas-02": [
        ("`man curl`.", 20),
        ("The page references an image file living in some subdirectory -- and many simple web servers, if not explicitly configured otherwise, will list the CONTENTS of a directory when no specific file is requested from it. Requesting the directory path itself, rather than a file inside it, is worth trying.", 225),
        ("View the page source to find the image's path (something like `files/pixel.png`), then request the directory itself rather than a specific file inside it, e.g. `curl http://<target-host>:8002/files/` -- if directory listing is enabled, this shows every file in there, including one holding the password.", 337),
    ],
    "natas-03": [
        ("[Robots exclusion standard on Wikipedia](https://en.wikipedia.org/wiki/Robots.txt).", 25),
        ("Search engines respect a specific, standard filename at the root of a website to know which paths NOT to crawl or index -- site owners sometimes misuse this file to 'hide' sensitive paths, not realizing that listing a path there is itself a public announcement of where it is.", 262),
        ("`curl http://<target-host>:8003/robots.txt` fetches the standard crawler-exclusion file -- it lists a path the owner didn't want indexed. Request that listed path directly to find the password.", 337),
    ],
    "natas-04": [
        ("`man curl`.", 25),
        ("The page checks the `Referer` header (which browsers normally set automatically to whatever page you clicked a link FROM) against a value it expects but a real visitor could never naturally arrive with. Helpfully, sending the WRONG referer first will show you, in the page's own error message, the exact value it actually wanted -- `curl` has a documented flag for setting a custom Referer header on your next request.", 262),
        ("Send any request first (`curl http://<target-host>:8004/`) and read the error text -- it states the exact Referer value it expects (in this deployment, it's computed from your own request: the same host, one port number higher than the port you're already using). Resend with that: `curl -e '<the-exact-value-shown>' http://<target-host>:8004/` to be granted access and see the password.", 337),
    ],
    "natas-05": [
        ("`man curl`.", 30),
        ("The page decides whether you're 'logged in' purely by reading a cookie value it already trusts completely, with no other verification. Viewing the response headers on your first request (curl's verbose mode shows every header, including any `Set-Cookie`) reveals what cookie it's setting; curl also has a flag for sending back a specific cookie value of your own choosing.", 300),
        ("`curl -v http://<target-host>:8005/` (the `-v` shows response headers, including `Set-Cookie`) reveals a cookie that looks boolean-ish (e.g. `loggedin=0`). Resend the request with that value flipped: `curl -b 'loggedin=1' http://<target-host>:8005/` to be treated as logged in and see the password.", 450),
    ],
    "natas-06": [
        ("Click 'View sourcecode'.", 30),
        ("The form on the page checks a 'secret' value against something the PHP code includes from another file. If you can read that included file's actual source rather than guessing its content, the page's own 'View sourcecode' link tells you exactly where to look.", 300),
        ("The 'View sourcecode' link shows the PHP, which `include`s a secret from a specific relative file path (e.g. `includes/secret.inc`). Request that exact path directly as a URL (`http://<target-host>:8006/includes/secret.inc`) to read the real secret value in plain text, then submit it in the form to reveal the password.", 450),
    ],
    "natas-07": [
        ("[File inclusion vulnerability on Wikipedia](https://en.wikipedia.org/wiki/File_inclusion_vulnerability).", 27),
        ("View the page source -- the site uses a URL parameter to choose which page to show ('Home' vs 'About'). If that parameter is used directly as a filename with no validation, you control which file on the server gets read, including files well outside the page's intended folder.", 275),
        ("The page uses a query parameter (commonly named `page`) to decide which file to include, e.g. `?page=home.php`. Because the application does no validation, replacing that value with an ABSOLUTE path to any file readable by the web server works directly -- try `?page=/etc/natas_webpass/natas8` (no `../` traversal needed at all, since it's already an absolute path, not a relative one).", 412),
    ],
    "natas-08": [
        ("Click 'View sourcecode'.", 35),
        ("The page shows an ENCODED secret and checks your input by re-running it through the same encoding function. If you can read the exact sequence of encoding steps in the source, you can apply each step BACKWARDS, in REVERSE order, against the encoded value to recover the original secret.", 350),
        ("The source shows the encoding as base64-encode, then reverse the string, then hex-encode (`bin2hex(strrev(base64_encode($secret)))`). To undo it, apply the inverse steps in reverse order: hex-decode the shown value first, then reverse that resulting string, then base64-decode what's left -- e.g. in a shell, `echo <encoded> | xxd -r -p | rev | base64 -d`. Submit the result as the secret.", 525),
    ],
    "natas-09": [
        ("Click 'View sourcecode'.", 40),
        ("The source shows your search input is passed straight into a shell command with no sanitization at all -- meaning any shell metacharacter you include (like a semicolon, which separates commands) gets interpreted by the underlying shell, not just treated as search text.", 400),
        ("Since the input reaches a real shell unsanitized, a needle like `;cat /etc/natas_webpass/natas10` closes off the intended `grep` command with `;` and runs your own `cat` command right after it, in the query string: `?needle=;cat+/etc/natas_webpass/natas10` (URL-encode the semicolon as `%3B` if your client won't send it raw).", 585),
    ],
    "natas-10": [
        ("Click 'View sourcecode'.", 40),
        ("The same underlying `grep` command exists as the previous level, but the app now blocks the obvious shell metacharacters. `grep` itself, though, accepts a SECOND filename as a plain command-line argument, searched in addition to the intended file -- worth checking whether that's usable without needing any blocked character at all.", 400),
        ("A needle of `. /etc/natas_webpass/natas11 #` needs no blocked character at all: the lone `.` is a regex matching every line (so the intended dictionary file's content doesn't matter), the second word is treated by `grep` as an ADDITIONAL file to search (not a shell command), and the trailing ` #` is a shell comment that drops the rest of the real command line (including the app's own hardcoded filename) once it reaches the shell.", 585),
    ],
    "natas-11": [
        ("[XOR cipher on Wikipedia](https://en.wikipedia.org/wiki/XOR_cipher).", 45),
        ("The cookie holds your preferences, XOR-encrypted with a short key that REPEATS if the data is longer than the key. You don't know the key directly, but you DO know what the default preferences look like when logged out (a fixed JSON structure) -- and XOR has a useful property: if you already know both the plaintext and the resulting ciphertext, XOR-ing them together recovers the key that was used, which you can then reuse to encrypt something new.", 450),
        ("Base64-decode the default (logged-out) cookie to get the raw XOR-encrypted bytes, then XOR those bytes against the KNOWN default plaintext JSON (the fixed preferences structure the source reveals) to recover the repeating XOR key. Build a new plaintext JSON with `showpassword` changed to `yes`, XOR-encrypt it with that same recovered key, base64-encode the result, and set it as your cookie -- the page will now show you the password.", 675),
    ],
    "natas-12": [
        ("Click 'View sourcecode'.", 45),
        ("The upload form accepts any file with no real validation of its content or type -- meaning you're not limited to uploading an actual image. A file containing server-side code, once uploaded, sits in a location the web server may execute if you simply request it by its URL afterward.", 450),
        ("Create a tiny PHP file containing `<?php system($_GET['c']); ?>` (a minimal 'web shell' that runs whatever shell command you pass it), upload it through the form, then note the path it was saved to. Request that uploaded file's URL with a `c` parameter, e.g. `?c=cat+/etc/natas_webpass/natas13`, and the server executes your command and returns the password.", 675),
    ],
    "natas-13": [
        ("Click 'View sourcecode'.", 50),
        ("The server now inspects the file's actual BYTES (not the filename/extension) to decide if it's really an image, using a function that only looks at the first few bytes for a known 'magic number' signature. Nothing stops a file's very first bytes from being a real image signature while the rest of the file remains valid server-side code.", 500),
        ("Prepend the literal bytes `GIF89a` (a real GIF file signature) to the very beginning of your PHP web shell from the previous level, before the `<?php` tag. The magic-byte check reads only those first bytes and is satisfied it's a GIF; PHP itself doesn't care what comes before `<?php` in the file, so your shell still executes normally once uploaded and requested with `?c=cat+/etc/natas_webpass/natas14`.", 750),
    ],
    "natas-14": [
        ("[SQL injection on Wikipedia](https://en.wikipedia.org/wiki/SQL_injection).", 50),
        ("Click 'View sourcecode' too -- the login query is built by directly gluing your username and password INTO a SQL string with no escaping at all, meaning a quote character you type doesn't stay 'just data.' It can close the string the developer intended and let you add your own SQL logic that the database will actually execute as part of the query. Pay close attention to which quote character the source itself uses to wrap each field.", 500),
        ("Since the query wraps each field in DOUBLE quotes and concatenates them directly, entering a username like `\\\" OR \\\"1\\\"=\\\"1\\\" -- ` (matching that same double-quote style -- note the trailing space after the double-dash, which comments out whatever the original query intended to add after your input) closes the intended string early, adds an always-true condition, and comments out the rest -- bypassing the password check entirely and logging you in, revealing the final flag.", 750),
    ],
}

# Generate folder and files
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(script_dir, "..", "challenges"))
os.makedirs(base_dir, exist_ok=True)

for i, ch in enumerate(challenges_data):
    folder_path = os.path.join(base_dir, ch["id"])
    os.makedirs(folder_path, exist_ok=True)

    is_final_level = (i == len(challenges_data) - 1)

    full_desc = ch["desc"]
    extra_info = EXTRA_INFO.get(ch["id"])
    if extra_info:
        cmds, reading = extra_info
        if cmds:
            cmd_list = ", ".join(f"`{c}`" for c in cmds)
            full_desc += f"\n\n**Commands you may need to solve this level:** {cmd_list}"
        if reading:
            links = "\n".join(f"- [{title}]({url})" for title, url in reading)
            full_desc += f"\n\n**Helpful reading:**\n{links}"

    yaml_content = f"""name: "{ch['name']}"
author: "CEI Labs (self-hosted recreation of OverTheWire's Natas)"
category: "Web Security"
description: |
  {full_desc.replace(chr(10), chr(10) + '  ')}
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
show_launcher: {"true" if ch["id"] == "natas-start-here" else "false"}
"""

    hint = HINTS.get(ch["id"])
    if hint:
        tiers = hint if isinstance(hint, list) else [hint]
        yaml_content += "hints:\n"
        for hint_content, hint_cost in tiers:
            yaml_content += f'  - content: "{hint_content}"\n    cost: {hint_cost}\n'

    file_path = os.path.join(folder_path, "challenge.yml")
    with open(file_path, "w") as f:
        f.write(yaml_content)

print(f"Successfully generated {len(challenges_data)} Natas challenges inside the '{base_dir}' folder!")
