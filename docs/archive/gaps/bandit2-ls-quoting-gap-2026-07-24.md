# Bandit 2->3: `ls` displays the spaces-filename pre-quoted (2026-07-24)

Reported: on Bandit level 2 (`bandit2` -> `bandit3`), the file containing
the next password shows up with surrounding `'quotes'` when the player
runs `ls`, i.e. `ls` shows `'spaces in this filename'` instead of
`spaces in this filename`. Since the whole point of this level is teaching
a player to notice a space-containing filename and figure out how to quote
it themselves, `ls` handing them the already-quoted, copy-pasteable syntax
defeats the challenge. Notes only, no code changed.

## Confirmed: the file itself is correct, this is a display artifact

Checked `CEI-Labs-Wargames` at current `main` (`f4d9291`):

- `targets/bandit/build/03-setup-levels-00-12.py:66-73` creates the file
  with the literal path
  `"/home/bandit2/spaces in this filename"` via plain Python `open()` —
  **no quote characters in the actual filename on disk.**
- `targets/bandit/entrypoint.sh:54` references the same literal path when
  substituting the real per-team flag into the file's contents at
  container start — again, no quote characters in the path itself.
- `scripts/build_bandit.py:102`'s challenge description says "a file
  called `spaces in this filename`" — backticks there are markdown code
  formatting, not literal quote marks, and render as a code font in CTFd,
  not as quote characters.

So nothing in this repo's own code puts quote characters into the
filename. What the player sees comes from `ls` itself.

## Root cause: GNU coreutils' default quoting style

`targets/bandit/Dockerfile:18,25` bases the image on `debian:12-slim`
(bookworm), which ships a GNU coreutils version whose `ls` defaults to
`QUOTING_STYLE=shell-escape` (or an equivalent shell-quoting default) when
output goes to a terminal — this is the coreutils default any time a
filename contains characters (like a space) that would need quoting/
escaping to be re-typed safely in a shell. It's not something this repo's
Dockerfile, entrypoint.sh, or build scripts configure; it's inherited
straight from the base image's coreutils. Checked
`targets/bandit/Dockerfile` and `targets/bandit/entrypoint.sh` for any
existing `QUOTING_STYLE` override or `ls` alias — there is none.

Practical effect: a player SSHed into `bandit2` running a bare `ls` over
an interactive terminal sees the filename pre-wrapped in single quotes,
which is *also* valid, ready-to-paste shell syntax for referencing that
file — the exact thing the level is supposed to make them work out for
themselves. The real OverTheWire Bandit (and presumably whatever
environment this level's description was originally written against) most
likely runs on an older coreutils/distro where `ls`'s default quoting
style doesn't do this, or the level was authored before this coreutils
default changed upstream.

## What a fix would need to decide

Not attempted here, but the mechanism is well understood enough to scope:

- **Force literal (unquoted) `ls` output** for the bandit2 account (or
  globally across all bandit accounts, for consistency) — e.g. set
  `QUOTING_STYLE=literal` in `bandit2`'s (or every bandit account's)
  shell environment (`.bashrc`/`.bash_profile`, or a
  `/etc/profile.d/*.sh` drop-in in `targets/bandit/Dockerfile`), or alias
  `ls` to always pass `--quoting-style=literal`.
- **Scope decision**: apply only to `bandit2` (minimal, targeted at this
  one level) or to every bandit account (consistent behavior across the
  whole track, avoids the same class of issue resurfacing on a different
  level that also relies on players noticing an awkward filename).
- Whichever is chosen should be re-verified against a live `ls` in the
  actual built image (not just read from source) before considering this
  closed, since quoting-style defaults can also depend on locale/env vars
  set elsewhere in the image that weren't audited as part of this pass.
