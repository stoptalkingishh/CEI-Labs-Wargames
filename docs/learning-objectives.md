# Learning Objectives

A skills inventory for all three self-hosted wargame tracks (Bandit,
Krypton, Natas — 56 levels total), organized by concept rather than by
level number, so it can be referenced independent of any specific
level: to check what a participant has actually learned, to plan which
levels to assign for a given skill gap, or to compare against a course
syllabus. Each entry names the real-world skill, not just the puzzle
mechanic, and lists which level(s) teach it.

## Bandit — Linux Fundamentals (34 levels)

### File discovery and navigation (levels 0–6)
- Connect to a remote Linux host over SSH and operate a shell session.
- Read files whose names are adversarial to naive command usage: a bare
  `-` (looks like a flag), embedded spaces, and hidden dotfiles.
- Use `file` to identify content type independent of filename, to pick
  one real file out of many identically-named decoys.
- Chain multiple `find` predicates (size, type, permission) in one
  search to narrow a large candidate set to one file.
- Search the entire filesystem (not just the home directory) by owner,
  group, and size, filtering out permission-denied noise.

### Text processing and data extraction (levels 7–11)
- Use `grep` to locate a value adjacent to a known marker in a large
  file.
- Use `sort`/`uniq` to find the one non-duplicated line in a large
  dataset — understanding that `uniq` only detects *adjacent*
  duplicates.
- Use `strings` to extract readable text from a binary/mixed file.
- Recognize and reverse Base64 encoding.
- Recognize and reverse a ROT13 (self-inverse) substitution.

### Layered decoding (level 12)
- Reverse a hexdump back to raw binary with `xxd`.
- Identify file type iteratively with `file` after each decompression
  step, rather than assuming the whole compression chain in advance.
- Chain multiple compression formats (gzip, bzip2) in sequence.

### Key-based authentication (level 13)
- Authenticate via a private SSH key instead of a password, including
  handling SSH's file-permission requirements on the key itself.

### Network services and port interaction (levels 14–17)
- Use `nc` (netcat) as a raw TCP client to send/receive text manually.
- Use `openssl s_client` to perform a TLS handshake and interact with an
  SSL/TLS-wrapped service by hand.
- Use `nmap` to discover which ports in a range are actually listening
  before attempting to interact with each one.
- Use `diff` to find the one meaningful change between two large,
  near-identical files.

### Restricted execution and privilege boundaries (levels 18–20)
- Understand that `.bashrc` only executes for *interactive* shells, and
  use `ssh user@host command` to run a single remote command without
  triggering it.
- Understand and exploit a setuid binary: it runs with the *file
  owner's* privileges regardless of who invokes it.
- Set up a local listener before triggering a program that connects
  back out to it — basic reverse-connection mechanics and shell job
  control (`&`, `fg`) to run two things in one session.

### Scheduled tasks / cron (levels 21–24)
- Read `/etc/cron.d/` configuration to determine what runs, as whom,
  and how often.
- Trace a cron job to the actual script it executes and read that
  script's logic to find where it writes output.
- Recognize when a cron job executes attacker-controllable input (a
  file matching a glob pattern in a writable directory) and place a
  script for it to run with elevated privilege.
- Script a brute-force attack (a 4-digit PIN, 10,000 combinations)
  against a listening service.

### Shell escapes and restricted shells (levels 25–26, 32–33)
- Recognize a non-standard login shell and identify what program it
  actually runs.
- Escape a pager (`more`) into a real editor (`vi`), then escape the
  editor into a real shell — the general pattern of "any full-featured
  interactive program is a potential shell escape."
- Identify and exploit a narrow gap in an input-mangling shell wrapper
  (a transform limited to lowercase letters lets `$0` and bash's own
  invocation semantics through untouched).
- Recognize `rbash` (restricted bash)'s actual restriction boundary —
  it blocks command names containing `/`, not what an *allowed*
  program execs internally — and use `find -exec` as a classic escape.

### Git internals (levels 27–31)
- Clone a git repository over SSH.
- Understand that git history is cumulative: `git log -p` can reveal
  data removed in a later commit.
- Enumerate and check out every branch, not just the default.
- Find data attached to a tag rather than a commit or branch.
- Read a repository's own stated contribution requirements and satisfy
  them with a real `add`/`commit`/`push` sequence.

## Krypton — Classical Cryptography (7 levels)

### Encoding vs. encryption (level 0)
- Recognize Base64 by its character set and distinguish a reversible
  *encoding* (no key required) from an actual cipher.

### Substitution ciphers (levels 1–3)
- Reverse a ROT13 rotation (a self-inverse Caesar shift of 13).
- Perform a known-plaintext attack: feed a cipher a value with known
  plaintext to directly observe its transformation, then reverse that
  transformation against the real ciphertext.
- Perform frequency analysis: use known English letter-frequency order
  (E, T, A, O, I, N, ...) to recover a monoalphabetic substitution
  alphabet from ciphertext statistics alone.

### Polyalphabetic ciphers (levels 4–5)
- Break a Vigenère cipher with a known key length by splitting
  ciphertext into interleaved groups, each solvable as its own
  independent Caesar shift.
- Perform Kasiski examination: find repeated ciphertext substrings,
  use the distances between repeats to estimate an *unknown* key
  length, then apply the known-key-length technique.

### Stream ciphers (level 6)
- Understand a stream cipher's core weakness when its keystream
  repeats: encrypting a long run of known plaintext directly reveals
  the keystream itself, which can then decrypt anything else encrypted
  with the same repeating stream.

## Natas — Web Application Security (15 levels)

### Client-side vs. server-side trust boundaries (levels 0–2)
- Understand that anything enforced in browser JavaScript (like
  blocking right-click) has no bearing on what a non-browser client can
  retrieve — view-source and `curl` bypass browser-only restrictions
  entirely.
- Read HTML comments and other artifacts left in page source that never
  render visibly.
- Recognize when directory listing is enabled and use it to discover
  files a page never links to.

### Access control bypass via HTTP headers and cookies (levels 3–5)
- Understand `robots.txt` as a public announcement of paths an owner
  didn't want indexed, not an access control.
- Forge an HTTP `Referer` header to satisfy a same-origin-style check.
- Read and modify session cookies directly to change an application's
  view of your authorization state, when the server trusts the cookie
  value with no further verification.

### Server-side source disclosure (level 6)
- Use a "view source" feature (where the application deliberately
  exposes it) to find where a secret is actually stored server-side,
  rather than guessing at it.

### File inclusion vulnerabilities (level 7)
- Recognize and exploit Local File Inclusion (LFI): an
  attacker-controlled parameter used directly as a filesystem path,
  including reading it as an absolute path with no traversal needed.

### Custom crypto/encoding schemes (level 8)
- Reverse-engineer a multi-step encoding chain (e.g. base64 → reverse
  string → hex) by reading server-side source and applying each
  inverse operation in reverse order.

### Command injection (levels 9–10)
- Recognize unsanitized input reaching a shell command and inject shell
  metacharacters to run an arbitrary command.
- Bypass a naive metacharacter blocklist by using a target command's
  *own* argument syntax (e.g. `grep` accepting a second filename
  argument) instead of shell syntax at all.

### XOR cryptanalysis (level 11)
- Recover a repeating XOR key via a known-plaintext attack (XOR a
  known plaintext against its ciphertext to recover the key), then use
  that key to forge new encrypted data.

### File upload vulnerabilities (levels 12–13)
- Exploit an upload form with no content-type validation to upload and
  execute a server-side script ("web shell").
- Bypass a magic-byte/content-based file-type check by prepending a
  real file signature ahead of an otherwise-valid payload.

### SQL injection (level 14)
- Recognize a login query built by raw string concatenation and
  construct an injection payload (matching the target's actual quoting
  style) that produces an always-true condition and comments out the
  remainder of the query.

## Cross-track meta-skills

These aren't tied to any single level, but are reinforced throughout
all three tracks:
- Reading unfamiliar tool documentation (`man <command>`) under time
  pressure and extracting the one relevant option.
- Distinguishing "I don't know this concept" from "I know the concept
  but forgot the syntax" — and using the right kind of help for each
  (a bare reference vs. a fuller explanation).
- Methodical enumeration: checking a small, well-defined search space
  exhaustively (a byte range, a port range, a PIN space) rather than
  guessing.
- Reading source code (shell scripts, PHP, cron configs) to understand
  *why* something behaves the way it does before acting.
