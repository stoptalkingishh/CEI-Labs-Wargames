# Bandit — Learning Objectives

A skills inventory for the Bandit track (Linux fundamentals, 34 levels),
organized by concept rather than by level number, so it can be
referenced independent of any specific level: to check what a
participant has actually learned, to plan which levels to assign for a
given skill gap, or to compare against a course syllabus. Each entry
names the real-world skill, not just the puzzle mechanic, and lists
which level(s) teach it. Pairs with `writeups.md` (full solutions) and
`cheatsheet.md` (fast facilitator lookup) in this same folder.

## File discovery and navigation (levels 0–6)
- Connect to a remote Linux host over SSH and operate a shell session.
- Read files whose names are adversarial to naive command usage: a bare
  `-` (looks like a flag), embedded spaces, and hidden dotfiles.
- Use `file` to identify content type independent of filename, to pick
  one real file out of many identically-named decoys.
- Chain multiple `find` predicates (size, type, permission) in one
  search to narrow a large candidate set to one file.
- Search the entire filesystem (not just the home directory) by owner,
  group, and size, filtering out permission-denied noise.

## Text processing and data extraction (levels 7–11)
- Use `grep` to locate a value adjacent to a known marker in a large
  file.
- Use `sort`/`uniq` to find the one non-duplicated line in a large
  dataset — understanding that `uniq` only detects *adjacent*
  duplicates.
- Use `strings` to extract readable text from a binary/mixed file.
- Recognize and reverse Base64 encoding.
- Recognize and reverse a ROT13 (self-inverse) substitution.

## Layered decoding (level 12)
- Reverse a hexdump back to raw binary with `xxd`.
- Identify file type iteratively with `file` after each decompression
  step, rather than assuming the whole compression chain in advance.
- Chain multiple compression formats (gzip, bzip2) in sequence.

## Key-based authentication (level 13)
- Authenticate via a private SSH key instead of a password, including
  handling SSH's file-permission requirements on the key itself.

## Network services and port interaction (levels 14–17)
- Use `nc` (netcat) as a raw TCP client to send/receive text manually.
- Use `openssl s_client` to perform a TLS handshake and interact with an
  SSL/TLS-wrapped service by hand.
- Use `nmap` to discover which ports in a range are actually listening
  before attempting to interact with each one.
- Use `diff` to find the one meaningful change between two large,
  near-identical files.

## Restricted execution and privilege boundaries (levels 18–20)
- Understand that `.bashrc` only executes for *interactive* shells, and
  use `ssh user@host command` to run a single remote command without
  triggering it.
- Understand and exploit a setuid binary: it runs with the *file
  owner's* privileges regardless of who invokes it.
- Set up a local listener before triggering a program that connects
  back out to it — basic reverse-connection mechanics and shell job
  control (`&`, `fg`) to run two things in one session.

## Scheduled tasks / cron (levels 21–24)
- Read `/etc/cron.d/` configuration to determine what runs, as whom,
  and how often.
- Trace a cron job to the actual script it executes and read that
  script's logic to find where it writes output.
- Recognize when a cron job executes attacker-controllable input (a
  file matching a glob pattern in a writable directory) and place a
  script for it to run with elevated privilege.
- Script a brute-force attack (a 4-digit PIN, 10,000 combinations)
  against a listening service.

## Shell escapes and restricted shells (levels 25–26, 32–33)
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

## Git internals (levels 27–31)
- Clone a git repository over SSH.
- Understand that git history is cumulative: `git log -p` can reveal
  data removed in a later commit.
- Enumerate and check out every branch, not just the default.
- Find data attached to a tag rather than a commit or branch.
- Read a repository's own stated contribution requirements and satisfy
  them with a real `add`/`commit`/`push` sequence.
