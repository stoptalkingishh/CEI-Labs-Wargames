# Build plan: Leviathan (2026-07-24)

Level-by-level content plan for a future CEI Labs Leviathan track,
sourced from public walkthroughs (real OverTheWire Leviathan is
SSH-only with no public per-level goal text on overthewire.org itself,
so third-party walkthroughs are the only way to plan actual level
content ahead of building it). Structured to match the conventions
already established by Bandit/Krypton/Natas in `CEI-Labs-Wargames`.
Planning doc only -- no code, targets, or challenge definitions created
in this pass.

## Sources

- Level topic index: `https://mayadevbe.me/posts/overthewire/leviathan/overview/`
- Cross-checked against search summaries of `techyrick.com`,
  `nguendung.github.io`, and `github.com/Whimmery/CTF-Leviathan`
  (not individually fetched -- topic-level agreement only, not
  verified command-by-command the way the Bandit/Krypton/Natas
  cross-reference PRs were)
- Upstream: `overthewire.org/wargames/leviathan` (confirms 8 levels,
  leviathan0-leviathan7, no per-level text published there)

## Level-by-level plan (8 levels, leviathan0 -> leviathan7)

| Level | Technique (per sources) | CEI Labs equivalent notes |
|---|---|---|
| 0->1 | Find a password in a backup/bookmarks-style file left in a readable location | Same shape as Bandit's early hidden-file levels; reuse that hint-ladder style |
| 1->2 | SUID binary inspection -- a setuid binary leaks or can be coerced into revealing the next password | Mirrors Bandit-19's setuid pattern; can reuse similar hint framing |
| 2->3 | Path/whitespace manipulation -- crafting a filename or path argument the binary doesn't expect | New technique not present in Bandit/Krypton/Natas; needs its own hint ladder from scratch |
| 3->4 | `ltrace`/`strace` recon -- observing a binary's library calls to recover a hardcoded or derived password | New tool category for CEI Labs (no existing track uses ltrace/strace); would need a tier-1 hint introducing the tool the way Bandit's tier-1 hints introduce `find`/`grep`/etc. |
| 4->5 | Weak authentication logic -- similar `ltrace` recovery against different binary logic | Same tool, different target; natural pairing with level 3->4 in a shared hint style |
| 5->6 | Temp files / loot left behind by another process | Similar in spirit to Bandit's cron levels (21-24) reading world-writable/leftover state |
| 6->7 | Tricking a binary into reading a file the player has no direct permission to read | Conceptually close to Bandit-19/20's setuid-binary-as-proxy pattern, applied to file reads instead of privileged commands |
| 7-> (final) | Reverse engineering with `gdb` to recover the final flag | First `gdb` usage in CEI Labs; would need its own tier-1 "how to even start gdb" hint, no existing precedent in Bandit/Krypton/Natas to reuse |

## Structural fit against existing conventions

Matching `targets/bandit/` and `scripts/build_bandit.py`'s shape, a
Leviathan track would need:

- `targets/leviathan/Dockerfile`, `targets/leviathan/build/` (per-level
  setup scripts, likely one `NN-setup-*.py` per level or level-group
  the way Bandit splits `01-create-users.sh`/`02-set-passwords.sh`/etc.)
- `targets/leviathan/entrypoint.sh` for per-team flag substitution,
  following Bandit's `PLACEHOLDER`-substitution pattern for flags
  embedded in plain files/binaries
- `targets/leviathan/build/generate_banners.py` with a new, distinct
  color ramp (not reusing Bandit's warm ramp or Krypton's cool ramp)
  and level-specific ASCII art following the "sea monster" lore
  already recorded in `docs/future-wargame-theme-leviathan-2026-07-24.md`
- `scripts/build_leviathan.py` with `TITLES`, `EXTRA_INFO`, `HINTS`
  (3-tier ladder per level), and `_render_description()`, mirroring
  `build_bandit.py`'s shape exactly
- Per-team dynamic flags via the same orchestrator env-var mechanism
  Bandit/Krypton already use, chained level-to-level the same way
  (each level's flag becomes the next login's password)

## Open questions / what real implementation would need

- Levels 3->4 and 4->5 introduce `ltrace`/`strace` and level 7
  introduces `gdb` -- tools with no existing hint-ladder precedent in
  this repo. Tier-1 hints for these would need to be written from
  scratch, unlike a level that can reuse an existing tool's established
  hint style (e.g. `find`, `grep`).
- This plan's source coverage is topic-level, not command-verified --
  unlike the Bandit/Krypton/Natas cross-reference PRs (#13-#16) which
  fetched and quoted exact commands, this plan is built from search
  summaries and one overview page. Actual level content (real binaries,
  real vulnerabilities) would need deeper research or original design
  before implementation, not just copying a walkthrough's steps.
- No security review of what "vulnerable binaries with real bugs"
  means for containment has been done -- Leviathan's levels don't
  involve intentionally-exploitable memory corruption the way Narnia/
  Behemoth/Utumno/Maze would, so the containment bar is likely closer
  to Bandit's (misconfigured permissions, not memory-unsafe code), but
  this wasn't explicitly confirmed level-by-level.
