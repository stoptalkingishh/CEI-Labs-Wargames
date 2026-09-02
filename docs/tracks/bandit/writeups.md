# Bandit — Full Solution Writeups

Complete, step-by-step solutions for all 34 Bandit levels. This is the
instructor-facing answer key: unlike the in-platform 3-tier hints (which
deliberately hold back detail so players still have to think), every
step here is spelled out, including the literal flag values. Not for
participant distribution.

Every level connects via SSH to the host/port shown on that challenge's
launch panel (all 34 levels share one persistent box — see "Bandit:
Start Here"), logging in as the account named after the level, using the
previous level's flag as that account's password (except level 0, which
uses the fixed password `bandit0`).

---

### Bandit 0 → 1: The First Step
**Goal:** Connect and read a file.
```
ssh bandit0@<host> -p <port>      # password: bandit0
cat readme
```
**Result:** `readme` contains the flag directly:
`NH2SXQwcBdpmTEzi3bvBHRW9NXrY9B1b`

---

### Bandit 1 → 2: Dashed Hopes
**Goal:** Read a file literally named `-`.
**Why:** Most commands treat a leading `-` as the start of an option
flag, not a filename. `--` stops flag-parsing, but a bare `-` argument is
*also* a long-standing Unix convention for "read from standard input" --
even `cat -- -` still hangs waiting on stdin rather than reading the
file. A leading path avoids the ambiguity entirely.
```
ssh bandit1@<host> -p <port>
cat ./-
```
**Verified live** (2026-07-10): `cat -- -` was tried first and hung; `cat ./-` worked immediately. Don't suggest `cat -- -` as a working alternative.
**Result:** `rRGizSaX8Mk1RTb1CNQoXTcYZUR6OUZY`

---

### Bandit 2 → 3: Spaces in Places
**Goal:** Read a file with spaces in its name.
```
ssh bandit2@<host> -p <port>
cat 'spaces in this filename'
```
**Result:** `aBZ0W5EmUfAf7kHTQeOwd8bauFJ2lEWG`

---

### Bandit 3 → 4: Hidden in Plain Sight
**Goal:** Find a dotfile.
```
ssh bandit3@<host> -p <port>
ls -la inhere
cat inhere/.hidden
```
**Result:** `2EW7BBsr6aMMoJ2HjW067zg8WNkNzbpm`

---

### Bandit 4 → 5: Human Readable
**Goal:** Find the one human-readable file among 10 decoys (`-file00`
through `-file09`).
```
ssh bandit4@<host> -p <port>
cd inhere
file ./*
```
Exactly one line reports as ASCII text; the rest report as `data`.
```
cat -- ./-file07     # (whichever filename `file` flagged as text)
```
**Result:** `lrIWWI6bB37kxfiCQZqUdOIYfr6eEeqR`

---

### Bandit 5 → 6: The Needle
**Goal:** Find one file under `inhere` matching all three: human-readable,
exactly 1033 bytes, not executable.
```
ssh bandit5@<host> -p <port>
find inhere -size 1033c -type f ! -executable
```
This should return exactly one (or very few) candidates — `file` each if
more than one comes back to confirm which is genuinely text.
```
cat <the-matching-path>
```
**Result:** `P4L4vucdmLnm8I7Vl7jG1ApGSfjYKqJU`

---

### Bandit 6 → 7: Server Search
**Goal:** Find a file anywhere on the server by owner, group, and size.
```
ssh bandit6@<host> -p <port>
find / -user bandit7 -group bandit6 -size 33c 2>/dev/null
```
`2>/dev/null` discards permission-denied noise from directories you can't
read.
```
cat <path-returned>
```
**Result:** `z7WtoNQU2XfjmMtWA8u5rN4vzqu4v99S`

---

### Bandit 7 → 8: The Millionth Word
**Goal:** Extract a value next to a marker word in `data.txt`.
```
ssh bandit7@<host> -p <port>
grep millionth data.txt
```
**Result:** `TESKZC0XvTetK0S9xNwm25STk5iWrBvP`

---

### Bandit 8 → 9: The Only One
**Goal:** Find the one line in `data.txt` with no duplicate.
```
ssh bandit8@<host> -p <port>
sort data.txt | uniq -u
```
(`uniq` only detects *adjacent* duplicates, hence sorting first.)
**Result:** `EN632PlfYiZbn3PhVK3XOGSlNInNE00t`

---

### Bandit 9 → 10: Strings Attached
**Goal:** Find a password in mostly-binary `data.txt`, preceded by `=`
characters.
```
ssh bandit9@<host> -p <port>
strings data.txt | grep '^='
```
**Result:** `G7w8LIi6J3kTb8O7jPdkOYOsDhmi0n0m`

---

### Bandit 10 → 11: Base Operations
**Goal:** Decode Base64.
```
ssh bandit10@<host> -p <port>
base64 -d data.txt
```
**Result:** `6zPeziLdR2RKNdNYFNb6nVCKzphlXHpt`

---

### Bandit 11 → 12: Substitution
**Goal:** Reverse ROT13.
```
ssh bandit11@<host> -p <port>
tr 'A-Za-z' 'N-ZA-Mn-za-m' < data.txt
```
(ROT13 is self-inverse — the same transform encodes and decodes.)
**Result:** `JVNBBFSmZwKKOP0XbFXOoW8chDz5yVRv`

---

### Bandit 12 → 13: Matryoshka
**Goal:** `data.txt` is a hexdump of a file compressed twice (gzip, then
bzip2).
```
ssh bandit12@<host> -p <port>
mkdir /tmp/work && cp data.txt /tmp/work && cd /tmp/work
xxd -r data.txt > data.bin
file data.bin              # -> bzip2 compressed data
mv data.bin data.bz2 && bunzip2 data.bz2
file data                  # -> gzip compressed data
mv data data.gz && gunzip data.gz
cat data
```
**Result:** `wbWdlBxEir4c8X3x5l9m5o5Wv8n9Uj4J`

---

### Bandit 13 → 14: Private Keys
**Goal:** Use a provided private key to reach `bandit14`.
```
ssh bandit13@<host> -p <port>
chmod 600 sshkey.private
ssh -i sshkey.private bandit14@localhost
cat /etc/bandit_pass/bandit14
```
**Result:** `fGrHPx402xGC7U7rXKDaxiWFTOiF0ENq`

---

### Bandit 14 → 15: Port Submission
**Goal:** Submit the current password to port 30000 on localhost.
```
ssh bandit14@<host> -p <port>
nc localhost 30000
# type: fGrHPx402xGC7U7rXKDaxiWFTOiF0ENq  <enter>
```
**Result:** `jN2kgmIXJ6fShzhT2avhotn4Zcka6tnt`

---

### Bandit 15 → 16: SSL Encryption
**Goal:** Same, but over TLS on port 30001.
```
ssh bandit15@<host> -p <port>
openssl s_client -connect localhost:30001 -quiet
# type: jN2kgmIXJ6fShzhT2avhotn4Zcka6tnt  <enter>
```
**Result:** `JQttfApK4SeyHwDlI9SXGR50qclOAil1`

---

### Bandit 16 → 17: SSL Port Scan
**Goal:** Find the one correct SSL service in port range 31000–32000.
```
ssh bandit16@<host> -p <port>
nmap -p 31000-32000 --open -sV localhost
```
Try `openssl s_client -connect localhost:<candidate-port> -quiet` against
each SSL-speaking candidate, sending the current password.
**Result:** `VwOSWtCAcEBcCU5TOk540Rh04UvwB1O8`

---

### Bandit 17 → 18: File Comparisons
**Goal:** Diff `passwords.old` and `passwords.new`.
```
ssh bandit17@<host> -p <port>
diff passwords.old passwords.new
```
**Result:** `kfBf3eYk5BPBRzwjqutbbfE887SVc5ac`

---

### Bandit 18 → 19: Shell Bypass
**Goal:** Read `readme` without triggering `.bashrc`'s logout.
```
ssh bandit18@<host> -p <port> cat readme
```
(Running a single remote command over SSH never sources `.bashrc`, which
only runs for interactive login shells.)
**Result:** `IueksS7Ubh8G3DXwAFbnnjJ1XWeqro5r`

---

### Bandit 19 → 20: SUID Escalation
**Goal:** Use a setuid binary to read bandit20's password.
```
ssh bandit19@<host> -p <port>
./bandit20-do "cat /etc/bandit_pass/bandit20"
```
**Result:** `GbKksEFF4yrVs6il55v6gwY5aVje5f0j`

---

### Bandit 20 → 21: Port Listener Connection
**Goal:** A setuid binary connects out to a port you choose; you must be
listening.
```
ssh bandit20@<host> -p <port>
nc -lvp 4444 &
./suconnect 4444
# in the listener: type GbKksEFF4yrVs6il55v6gwY5aVje5f0j <enter>
```
**Result:** `gE269g2h3mw3pwgrj0LuIpTpNcfS1KMc`

---

### Bandit 21 → 22: Cron Jobs
**Goal:** Read a cron config to find where the password ends up.
```
ssh bandit21@<host> -p <port>
cat /etc/cron.d/*
```
The listed job writes the password to a file readable by bandit21 (check
the specific script/output path shown).
**Result:** `Yk7oeL4H2E45qp7Z9EaA8F4e8G4Z5Jj7`

---

### Bandit 22 → 23: Cron Debugging
**Goal:** Trace a cron job to the script it runs.
```
ssh bandit22@<host> -p <port>
cat /etc/cron.d/*                    # find the script path
cat /usr/bin/cronjob_bandit22.sh     # (or whatever path was shown)
```
The script computes an output filename via `echo I am user $(whoami) | md5sum | cut -d ' ' -f 1`, writing to `/tmp/<that-hash>`. Reproduce it with `bandit23` substituted for the username, then read the resulting file.
**Result:** `jc1udXDznI2mD8tE8Zq2P17ZtGv6z5M0`

---

### Bandit 23 → 24: Cron Scripting
**Goal:** A cron job executes anything matching a pattern in a
world-writable temp directory — write your own script for it to run.
```
ssh bandit23@<host> -p <port>
cat /etc/cron.d/*                    # find the script + its target dir/pattern
cat /usr/bin/cronjob_bandit23.sh     # read the matching logic
echo '#!/bin/bash' > /tmp/x.sh
echo 'cp /etc/bandit_pass/bandit24 /tmp/bandit24pass' >> /tmp/x.sh
chmod +x /tmp/x.sh
# wait up to a minute for the cron sweep
cat /tmp/bandit24pass
```
**Result:** `UoMYTrfrBFHyQXmg6R1YI7mIfUIna55J`

---

### Bandit 24 → 25: PIN Brute Force
**Goal:** Brute-force a 4-digit PIN against a daemon on port 30002.
```
ssh bandit24@<host> -p <port>
mkdir /tmp/brute && cd /tmp/brute
for pin in $(seq -w 0 9999); do echo UoMYTrfrBFHyQXmg6R1YI7mIfUIna55J $pin; done | nc -q1 localhost 30002 > results.txt
grep -v Wrong results.txt
```
**Result:** `uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG`

---

### Bandit 25 → 26: Shell Breakout
**Goal:** bandit26's shell pages a short file (`more`) and exits — you
need to interrupt that before it exits.
```
ssh bandit25@<host> -p <port>
grep bandit26 /etc/passwd    # confirms the unusual shell
```
Shrink your terminal window to a handful of rows *before* connecting,
then:
```
ssh bandit26@<host> -p <port>    # password: uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG
```
`more` pauses on `--More--` instead of exiting. Press `v` to open the
paged file in `vi` — continues in the next level.
**Result:** `5czgV9L3Xx8JPOyU3jO5B9I0A3bM9E3z`

---

### Bandit 26 → 27: Text UI Breakout
**Goal:** Escape `vi` (reached via the previous level's `v` escape) into
a real shell.
```
:set shell=/bin/bash
:shell
```
(or simply `:!/bin/bash`). From the resulting real shell:
```
find / -user bandit27 2>/dev/null    # or just look around the home directory
```
**Result:** `3ba3118a22e93127a4ed485be72ef5ea`

---

### Bandit 27 → 28: Git Clone
**Goal:** Clone a git repo and read the password from its working tree.
```
git clone ssh://bandit27-git@<host>:<port>/home/bandit27-git/repo
# password: 3ba3118a22e93127a4ed485be72ef5ea
cd repo && cat README.md
```
**Result:** `0ef186ac70e04ea33b4c1853d2526fa2`

---

### Bandit 28 → 29: Git Commits
**Goal:** Find a password redacted in the current tree but present in an
earlier commit.
```
git clone ssh://bandit28-git@<host>:<port>/home/bandit28-git/repo
cd repo && git log -p
```
Scroll through the diff output for the earlier, unredacted version.
**Result:** `bbc96594b4e001778eee9975372716b2`

---

### Bandit 29 → 30: Git Branches
**Goal:** Find a password on a non-default branch.
```
git clone ssh://bandit29-git@<host>:<port>/home/bandit29-git/repo
cd repo && git branch -a
git checkout <branch-name>
cat README.md    # (or whichever file holds it on that branch)
```
**Result:** `5b90576ed34ce8c56ad62351ab66e47c`

---

### Bandit 30 → 31: Git Tags
**Goal:** Find a password attached to a tag.
```
git clone ssh://bandit30-git@<host>:<port>/home/bandit30-git/repo
cd repo && git tag
git show <tagname>
```
**Result:** `47e603bb428404d265f59c42920d81e5`

---

### Bandit 31 → 32: Git Push
**Goal:** Satisfy the repo's own stated push requirements.
```
git clone ssh://bandit31-git@<host>:<port>/home/bandit31-git/repo
cd repo && cat README.md    # read the exact filename/content it wants
# create the exact file it asked for
git add <that-file>
git commit -m "..."
git push origin master
```
The push response (or a follow-up read) reveals the password.
**Result:** `56a9bf19c63d650ce78e6ec0354ee45e`

---

### Bandit 32 → 33: Shell Overrides
**Goal:** bandit32's shell uppercases every command before running it —
escape to a real shell.
```
ssh bandit32@<host> -p <port>    # password: 56a9bf19c63d650ce78e6ec0354ee45e
$0
```
**Why it works:** the wrapper's `tr 'a-z' 'A-Z'` only touches lowercase
letters; `$0` contains none, so it passes through untouched. This
wrapper shell was itself launched via `bash -c '...'`, and inside that
context `$0` defaults to the literal string `bash` — evaluating it
spawns a fresh, unrestricted bash shell.
```
find / -user bandit33 2>/dev/null
```
**Result:** `c9c3199ddf4121b10fb58bb24580d440`

---

### Bandit 33 → 34: Final Escape
**Goal:** bandit33 lands in `rbash` (restricted bash) with only `find`
and `ls` on its PATH — no way to read a file directly.
```
ssh bandit33@<host> -p <port>    # password: c9c3199ddf4121b10fb58bb24580d440
find . -exec /bin/sh \;
```
**Why it works:** rbash blocks *you* from naming a command containing
`/`, but that restriction doesn't apply to what an *allowed* command
(`find`) execs on your behalf via `-exec`. The result is a real `dash`
shell (`/bin/sh` on this image) with no `rbash` restrictions of its own.
It still inherits the restricted `PATH` from its parent, though — unlike
rbash, this shell actually lets you change `PATH`, so fix that first:
```
PATH=/usr/bin:/bin
export PATH
find / -name flag 2>/dev/null    # or just explore ~/.final
cat ~/.final/flag
```
**Verified live** (2026-07-10): confirmed with a real interactive PTY
session that `find . -exec /bin/sh \;` does land in a genuinely
unrestricted shell (`$-` shows no `r`, `$0` is `/bin/sh`) — but `cat`
fails with "not found" until `PATH` is reset; skipping that step makes
this escape look broken when it isn't.
**Result (final Bandit flag):** `OdqthX2eZq2fFft2q3B5mJz7eIq3Zk2d`
