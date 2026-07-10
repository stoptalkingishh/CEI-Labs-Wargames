# Natas — Learning Objectives

A skills inventory for the Natas track (web application security, 15
levels), organized by concept rather than by level number, so it can be
referenced independent of any specific level: to check what a
participant has actually learned, to plan which levels to assign for a
given skill gap, or to compare against a course syllabus. Each entry
names the real-world skill, not just the puzzle mechanic, and lists
which level(s) teach it. Pairs with `writeups.md` (full solutions) and
`cheatsheet.md` (fast facilitator lookup) in this same folder.

## Client-side vs. server-side trust boundaries (levels 0–2)
- Understand that anything enforced in browser JavaScript (like
  blocking right-click) has no bearing on what a non-browser client can
  retrieve — view-source and `curl` bypass browser-only restrictions
  entirely.
- Read HTML comments and other artifacts left in page source that never
  render visibly.
- Recognize when directory listing is enabled and use it to discover
  files a page never links to.

## Access control bypass via HTTP headers and cookies (levels 3–5)
- Understand `robots.txt` as a public announcement of paths an owner
  didn't want indexed, not an access control.
- Forge an HTTP `Referer` header to satisfy a same-origin-style check.
- Read and modify session cookies directly to change an application's
  view of your authorization state, when the server trusts the cookie
  value with no further verification.

## Server-side source disclosure (level 6)
- Use a "view source" feature (where the application deliberately
  exposes it) to find where a secret is actually stored server-side,
  rather than guessing at it.

## File inclusion vulnerabilities (level 7)
- Recognize and exploit Local File Inclusion (LFI): an
  attacker-controlled parameter used directly as a filesystem path,
  including reading it as an absolute path with no traversal needed.

## Custom crypto/encoding schemes (level 8)
- Reverse-engineer a multi-step encoding chain (e.g. base64 → reverse
  string → hex) by reading server-side source and applying each
  inverse operation in reverse order.

## Command injection (levels 9–10)
- Recognize unsanitized input reaching a shell command and inject shell
  metacharacters to run an arbitrary command.
- Bypass a naive metacharacter blocklist by using a target command's
  *own* argument syntax (e.g. `grep` accepting a second filename
  argument) instead of shell syntax at all.

## XOR cryptanalysis (level 11)
- Recover a repeating XOR key via a known-plaintext attack (XOR a
  known plaintext against its ciphertext to recover the key), then use
  that key to forge new encrypted data.

## File upload vulnerabilities (levels 12–13)
- Exploit an upload form with no content-type validation to upload and
  execute a server-side script ("web shell").
- Bypass a magic-byte/content-based file-type check by prepending a
  real file signature ahead of an otherwise-valid payload.

## SQL injection (level 14)
- Recognize a login query built by raw string concatenation and
  construct an injection payload (matching the target's actual quoting
  style) that produces an always-true condition and comments out the
  remainder of the query.
