# Instructor Cheat Sheet

Fast-lookup reference for walking a room during a live session. One row
per level: what it's testing, the one-line nudge to give someone who's
stuck, and the core technique in a few words. Not a substitute for the
full writeups (`docs/writeups/`) — if a one-liner doesn't unstick
someone, jump to the matching writeup section (same level name) for the
complete explanation.

Every level's own in-platform hints (3 tiers, point-costed) are the
first thing to point a stuck participant at — this sheet is for when
you're walking the room and need the answer in your own head *faster*
than reading a hint stub, or when someone's stuck in a way the hints
don't quite address (e.g., a terminal/environment issue, not a puzzle
issue).

---

## Bandit (Unix/Linux fundamentals) — shared box, SSH

| Level | Goal | If they're stuck, point them at... | Core technique |
|---|---|---|---|
| 0→1 | Connect, read a file | "You're overthinking this — just `cat` it." | `ssh`, `cat` |
| 1→2 | Read a file named `-` | "`-` looks like a flag to `cat`. How do you tell `cat` 'this is a path, not an option'?" | `cat ./-` (not `cat -- -`, which hangs on stdin) |
| 2→3 | Filename has spaces | "Quote the whole filename." | `cat 'name with spaces'` |
| 3→4 | Find a dotfile | "`ls` won't show it by default — what flag reveals hidden files?" | `ls -la` |
| 4→5 | One real text file among decoys | "Don't read all 10 by hand — what command tells you a file's *type*?" | `file ./*` |
| 5→6 | File matching size+type+perm | "Three criteria at once — one command can filter on all three." | `find -size -type ! -executable` |
| 6→7 | Find a file anywhere by owner/group/size | "Search the whole filesystem, and silence the permission-denied noise." | `find / ... 2>/dev/null` |
| 7→8 | Value next to a marker word | "grep for the word right next to what you need." | `grep millionth` |
| 8→9 | The one non-duplicate line | "`uniq` only catches duplicates that are *next to each other* — what do you need to do first?" | `sort \| uniq -u` |
| 9→10 | Password inside binary data | "You need the readable text buried in binary noise, then narrow by a pattern you know precedes it." | `strings \| grep '^='` |
| 10→11 | Base64 | "That's Base64 — what decodes it?" | `base64 -d` |
| 11→12 | ROT13 | "It's rotated by 13 — same command undoes it as applies it." | `tr` rotation |
| 12→13 | Double-compressed hexdump | "Un-hexdump first, then `file` will tell you what compression to peel off, one layer at a time." | `xxd -r`, `file`, iterative `gunzip`/`bunzip2` |
| 13→14 | Use a private key | "Key files need tightened permissions before SSH will trust them." | `chmod 600`, `ssh -i` |
| 14→15 | Submit password to a port | "Just pipe your password into a raw connection to that port." | `nc localhost <port>` |
| 15→16 | Same, but TLS | "Same idea, but the port speaks SSL now — `nc` won't work here." | `openssl s_client -connect ... -quiet` |
| 16→17 | Find the right port in a range | "Scan the range first, then try each SSL candidate." | `nmap -p <range> -sV`, then `openssl s_client` |
| 17→18 | Diff two files | "Don't read both by eye — there's a command built for exactly this." | `diff` |
| 18→19 | Avoid a logout trap in `.bashrc` | "Don't log in interactively at all — SSH can run one command without ever opening a shell." | `ssh user@host command` |
| 19→20 | SUID binary escalation | "That binary runs as a different user no matter who calls it — what does it let you run?" | run the SUID helper with your own command string |
| 20→21 | Binary connects back to you | "You need to be listening *before* you trigger it." | `nc -lvp <port> &` then trigger the connect-back |
| 21→22 | Cron writes a password somewhere | "Cron config tells you exactly what runs and roughly where its output goes." | read `/etc/cron.d/*` |
| 22→23 | Cron script computes a filename via hash | "Read the script, then run its own filename-generating command yourself, substituting the next user." | reproduce the `md5sum` filename logic |
| 23→24 | Write your own script for cron to run | "The temp directory is world-writable and cron will run anything matching a pattern — write that yourself." | drop an executable script into the swept directory |
| 24→25 | Brute-force a 4-digit PIN | "4 digits is only 10,000 — script the whole space instead of guessing." | loop all 0000–9999, pipe to `nc` |
| 25→26 | Escape a shell that exits after paging a file | "Shrink your terminal *before* connecting so the pager doesn't finish paging in one screen." | small terminal forces `more`'s `--More--` prompt |
| 26→27 | Escape `vi` | "You're in `vi` — it can shell out." | `:set shell=/bin/bash` then `:shell` |
| 27→28 | Clone a git repo | "Just clone it like any other repo and look at what's checked in." | `git clone`, read tracked files |
| 28→29 | Password redacted in current tree | "It's gone *now* — was it always? Check history." | `git log -p` |
| 29→30 | Password on another branch | "Check what branches exist besides the one you're on." | `git branch -a`, `git checkout` |
| 30→31 | Password on a tag | "Tags can hold data too — list them." | `git tag`, `git show <tag>` |
| 31→32 | Repo demands a specific push | "Read what the repo itself is asking for, then give it exactly that." | create requested file, commit, `git push` |
| 32→33 | Shell uppercases every command | "Something that's already uppercase would pass through untouched — what variable holds the shell's own name?" | `$0` (evaluates to `bash`, unaffected by uppercasing) |
| 33→34 | Final restricted-shell escape | "`find` can launch other programs on your behalf — and that launch isn't restricted the way typing a command yourself is. Then: check what `PATH` you land in." | `find . -exec /bin/sh \;`, then reset `PATH` |

---

## Krypton (cryptography) — shared box, SSH

| Level | Goal | If they're stuck, point them at... | Core technique |
|---|---|---|---|
| 0→1 | Base64 | "Same as Bandit 10 — what decodes Base64?" | `base64 -d` |
| 1→2 | ROT13 | "Self-inverse rotation — same command decodes as encodes." | `tr` rotation |
| 2→3 | Unknown Caesar shift | "You have a tool that encrypts with the same key — feed it something predictable and see what comes out." | probe with known plaintext (`AAAA...`), derive shift, reverse it |
| 3→4 | Frequency analysis | "English letters aren't evenly distributed — count letter frequency and match against the standard order." | letter-frequency count vs. E-T-A-O-I-N... |
| 4→5 | Vigenère, known key length | "Split the ciphertext into N interleaved groups by key length — each group alone is just a Caesar shift." | column split, per-column frequency analysis |
| 5→6 | Vigenère, unknown key length | "Find repeated chunks in the ciphertext and look at the *distance* between repeats — that reveals the key length." | Kasiski examination, then level 4's technique |
| 6→7 | Stream cipher (final) | "Feed the encryptor a long run of one known character — the output directly reveals the repeating keystream." | known-plaintext keystream recovery, XOR/subtract to decrypt |

---

## Natas (web security) — shared target, attacker workstation

Every level: attacker workstation → `curl`/browser to `http://<target>:800N/`.

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

---

## Notes for facilitators

- **Point-cost hints vs. this sheet:** encourage participants to use the
  platform's own hints first — they're built to cost points on purpose
  (see `docs/wargame-building-playbook.md`). This sheet is for you, not
  for handing directly to a stuck participant.
- **Natas attacker workstation credentials:** the shared attacker box's
  SSH/VNC login is not surfaced anywhere in the launch panel UI — see
  `docs/troubleshooting-faq.md` for the current workaround (noVNC is the
  password-free path; point participants there first).
- **Shared-box tracks (Bandit, Krypton):** everyone on a track shares one
  target box. If a participant's session looks broken in a way not
  explained by the puzzle itself, a **Reboot Host** from the launch panel
  is the first thing to try before assuming it's a real bug.
