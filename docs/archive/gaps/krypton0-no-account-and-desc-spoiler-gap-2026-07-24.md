# Krypton 0->1: no dedicated user account/home folder, and the goal text spoils the solve command (2026-07-24)

Two issues reported together for Krypton level 0 -> 1:

1. Unlike every Bandit level (each of which logs in as a distinct user
   with its own home folder, e.g. `bandit0` -> `bandit1` -> ...),
   Krypton 0 -> 1 has no dedicated account or home directory at all.
   Requested: give it the same per-level-account/home-folder treatment
   Bandit uses.
2. The challenge's own goal text names the exact command needed to
   solve it, which shouldn't be there.

Notes only, no code changed.

## Finding 1: krypton0 having no account is a recorded, deliberate scope decision -- not an oversight

Confirmed in `CEI-Labs-Wargames/targets/krypton/build/01-create-users.sh`:

```bash
# Creates krypton1-krypton6 (no krypton0 -- level 0 needs no SSH login at
# all, it's just a Base64 string given directly in the challenge
# description, matching build_krypton.py's own level-0 text).
for i in $(seq 1 6); do
    useradd -m -s /bin/bash --no-log-init "krypton${i}"
    ...
```

And `targets/krypton/build/02-set-passwords.sh`, which is even more
explicit that this was decided deliberately:

```bash
# Only krypton1 is set here. krypton1's password is level 0's flag, which
# is embedded directly in the CTFd challenge description text (a Base64
# puzzle) rather than anything this container serves -- CTFd descriptions
# don't vary per team, so there's no mechanism to make this per-team
# unique, and it gates no privileged access of its own (level 0 itself
# needs no target instance at all). This is a deliberate scope decision,
# not an oversight -- see docs/guides/security-audit-status.md.
```

So: krypton1-krypton6 already get real accounts with home directories,
exactly like Bandit. krypton0 specifically was scoped out on purpose,
with a stated reason (no per-team-unique flag mechanism for text
embedded in a CTFd description, and no privileged access to gate). This
doc doesn't take a position on whether that reasoning still holds --
just that it's a recorded decision in the codebase's own comments and
`docs/guides/security-audit-status.md`, not a bug. Implementing what's
requested (a real `krypton0` account + home folder + target instance
for a plain Base64 string) would be a scope/design change to that
existing decision, not a fix to broken behavior.

## Finding 2: the goal text for krypton-00 does spoil the solve command

From `CEI-Labs-Wargames/scripts/build_krypton.py`:

```python
"id": "krypton-00",
"name": "Krypton 0 -> 1: Base64 Decoding",
"desc": "**Goal:** Decode a Base64-encoded password.\n\nThis level needs no environment at all -- the following string encodes the password for level 1 in Base64:\n\n`S1JZUFRPTklTR1JFQVQ=`\n\nDecode it (e.g. with the `base64 -d` command) to find the flag.",
```

The free description literally says "e.g. with the `base64 -d`
command" -- the exact command needed to solve the level is stated in
the always-visible goal text, not gated behind any hint tier. This is
the same category of issue as the already-documented
`bandit3-desc-spoiler-gap-2026-07-24.md` (free description giving away
what the hint ladder is meant to teach), just for Krypton's level 0
instead.

None of the other Krypton levels' descriptions checked in this pass
(`krypton-01` through `krypton-06`) name a specific solve command in
their free description text -- this appears isolated to `krypton-00`.

## What closing this needs

- Finding 1 needs a product decision, not a code fix: either leave
  krypton0 as text-only (current, documented, intentional) or decide to
  give it a real account/home folder/target instance like Bandit,
  which would also require resolving the per-team-flag-uniqueness gap
  `02-set-passwords.sh` cites as the reason it wasn't done. This is
  `CEI-Labs-Wargames`'s `targets/krypton/build/01-create-users.sh` and
  `02-set-passwords.sh`, plus likely `entrypoint.sh` for per-team flag
  wiring, plus `scripts/build_krypton.py` for the challenge/env change.
- Finding 2 needs `HINTS`/`desc` editing in `scripts/build_krypton.py`:
  drop "e.g. with the `base64 -d` command" from `krypton-00`'s `desc`,
  moving that detail into the hint ladder instead (there's currently no
  `HINTS["krypton-00"]` tier that would need adjusting beyond what
  already exists, since tier 1 already says "Run `base64 --help`" --
  removing the desc spoiler would make the hint ladder the only place
  the actual command is confirmed).
- `challenge.yml` files are generated from `build_krypton.py`; do not
  hand-edit them directly.
