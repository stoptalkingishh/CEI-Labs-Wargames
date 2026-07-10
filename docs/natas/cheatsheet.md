# Natas — Instructor Cheat Sheet

Fast-lookup reference for walking a room during a live session. One row
per level: what it's testing, the one-line nudge to give someone who's
stuck, and the core technique in a few words. Not a substitute for the
full writeup (`writeups.md`, same folder) — if a one-liner doesn't
unstick someone, jump to the matching writeup section (same level name)
for the complete explanation.

Every level's own in-platform hints (3 tiers, point-costed) are the
first thing to point a stuck participant at — this sheet is for when
you're walking the room and need the answer in your own head *faster*
than reading a hint stub yourself, or when someone's stuck in a way the
hints don't quite address (e.g., a terminal/environment issue, not a
puzzle issue).

Shared target, attacker workstation — every level: attacker workstation
→ `curl`/browser to `http://<target>:800N/`. The attacker box's SSH
login credential isn't surfaced anywhere in the launch panel UI — point
participants at **noVNC** first (no credential needed); see
`../troubleshooting-faq.md` before treating an "I can't SSH in" report
as a bug.

| Level | Goal | If they're stuck, point them at... | Core technique |
|---|---|---|---|
| 0→1 | View source | "The answer's often literally in a comment — view source." | HTML comment |
| 1→2 | Right-click blocked | "That block is JavaScript-only — a tool that doesn't run JS doesn't care." | `curl` / browser view-source bypasses JS block |
| 2→3 | Directory listing | "Look at the page's own image path — is there a listable folder above it?" | enabled directory index reveals a password file |
| 3→4 | robots.txt | "Check the file that tells search crawlers what *not* to index." | `curl /robots.txt` |
| 4→5 | Referer check | "The error message tells you exactly what Referer it wants." | forge `Referer` header |
| 5→6 | Cookie check | "Look at the cookie it sets you, and what value it's checking for." | forge cookie value |
| 6→7 | Include path leak | "View source with `?source` — where's it including from?" | read leaked include path directly |
| 7→8 | LFI, no traversal needed | "The parameter takes a path with zero validation — just give it an absolute path." | `?page=/etc/natas_webpass/...` |
| 8→9 | Reverse a custom encoding | "Source shows the exact functions used to encode it — apply them backwards, in reverse order." | undo `bin2hex(strrev(base64_encode()))` |
| 9→10 | Command injection, unsanitized | "The parameter goes straight into a shell command — chain another command onto it." | `;cat ...` |
| 10→11 | Command injection, sanitized | "Shell metacharacters are blocked, but `grep` itself takes more than one filename argument, no special characters needed." | `grep`'s own second-argument/comment trick |
| 11→12 | XOR cookie forgery | "You know the default plaintext and can see the ciphertext — XOR them to get the key, then re-encrypt what you want." | recover XOR key from known-plaintext, forge cookie |
| 12→13 | Upload a web shell | "Upload a PHP file, then call the URL it lands at with your own command parameter." | `<?php system($_GET[...]); ?>` upload |
| 13→14 | Upload check bypassed by header only | "The check only reads the first few bytes — a real file signature followed by your payload still executes." | prepend `GIF89a` magic bytes to a PHP payload |
| 14→15 | SQL injection | "Source shows the exact quote character the query uses — your payload has to match that, not a generic example." | quote-breakout SQLi with trailing comment |
