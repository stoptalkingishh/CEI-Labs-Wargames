# Bandit 3->4: the always-visible goal text spoils its own hint tiers (2026-07-24)

Reported: the Bandit 3 -> 4 ("Hidden in Plain Sight") challenge description
gives away too much about what's actually going on. Notes only, no code
changed.

## Confirmed: current text

`CEI-Labs-Wargames/scripts/build_bandit.py:106-111` (`main` `f4d9291`):

```
"id": "bandit-03",
"name": "Bandit 3 -> 4: Hidden in Plain Sight",
"desc": "**Goal:** Find a hidden (dotfile) password.\n\nLog in as `bandit3`.
         The next password is hidden inside the `inhere` directory --
         you'll need to show hidden files to find it.",
```

This description text is **always visible for free** — it's the base
challenge description, not gated behind any hint tier or cost.

## Why this is a real problem, not just a style nitpick

This same level has a 3-tier progressive hint ladder
(`scripts/build_bandit.py:412-416`, `HINTS["bandit-03"]`):

1. `` `ls --help`. ``
2. "On Linux, any filename starting with a `.` is hidden from a plain
   directory listing by convention... `ls` has a documented flag to show
   hidden entries too."
3. `` `ls -la inhere` (the `-a` flag shows hidden entries) reveals a
   dotfile. `cat` that filename directly to read the password. ``

The always-free description already states **both** of the two things
tiers 2 and 3 exist to teach progressively: that the file is a dotfile,
and that the technique is "show hidden files." A player never has to
open (or, once the hint-wallet economy gap is fixed — see
`docs/hint-wallet-economy-gap-2026-07-24.md` — ever pay for) hint tier 2
or 3 to get that information; the free description already handed it
over. The level's actual puzzle (discovering on your own that dotfiles
exist and how to reveal them) never really happens — the name "Hidden in
Plain Sight" plus the literal parenthetical "(dotfile)" in the goal line
removes the "hidden" part entirely.

Level naming makes this worse in the same way: the title itself,
"Hidden in Plain Sight," is a fair thematic name, but combined with the
description's explicit "(dotfile)" it reads more like a second hint than
flavor text.

## Scope check: is this pattern present elsewhere?

Not audited beyond bandit-03 in this pass — flagging as worth a follow-up
sweep of the other 58 challenge descriptions for the same failure mode
(free description text quietly restating what a paid/gated hint tier is
supposed to reveal), rather than assuming this is an isolated case.

## What a fix would need

Not attempted here:

- Rewrite `desc` in `scripts/build_bandit.py`'s `bandit-03` entry to
  describe the GOAL ("find the next password somewhere in `inhere`")
  without naming the mechanism (dotfile / hidden files). The existing
  3-tier hint ladder already covers the reveal progressively and doesn't
  need to change.
- Decide whether to keep or soften the "Hidden in Plain Sight" title,
  since it's borderline once the description itself stops naming the
  mechanism.
- The follow-up sweep mentioned above, scoped as its own pass rather than
  bundled into this one finding.
