# Build plan: Behemoth (2026-07-24)

Level-by-level content plan for a future CEI Labs Behemoth track.
Source coverage for this game is the thinnest of the five in this
planning series -- flagged explicitly below. Structured to match the
conventions already established by Bandit/Krypton/Natas in
`CEI-Labs-Wargames`. Planning doc only -- no code, targets, or
challenge definitions created in this pass.

## Sources

- `dc865/writeups` (`Behemoth.md`, fetched directly): covers only
  behemoth0 and behemoth1 in any real detail.
- Search-result summaries only (not fetched in full, due to a Medium
  redirect loop that couldn't be resolved in this pass) for a
  "Levels 0-8" overview piece by Jinay/MeetCyber, which the search
  summary quoted as: level 0 uses `memfrob()`-encrypted password
  inspection via gdb; level 7 is "a classic stack overflow... stripped
  of hand-holding."
- Upstream: `overthewire.org/wargames/behemoth` confirms 9 levels
  (behemoth0-behemoth8), difficulty 3/10, general framing of "buffer
  overflows, race conditions and privilege escalation... found
  commonly out in the wild." No per-level text published there.

## Level-by-level plan (9 levels, behemoth0 -> behemoth8) -- confidence noted per row

| Level | Technique (confidence) | CEI Labs equivalent notes |
|---|---|---|
| 0->1 | GDB memory inspection to recover a password obscured with `memfrob()` (medium confidence -- sourced but not cross-verified) | Similar spirit to Bandit-12's "reverse an encoding chain" levels, but via live debugger inspection instead of static decoding tools |
| 1->2 | Unsafe `gets()` -- classic stack buffer overflow (medium confidence -- sourced but not cross-verified) | Same category as Narnia's opening levels; if both tracks get built, coordinate so Behemoth's overflow levels are a genuine difficulty step up from Narnia's, not a re-tread |
| 2->6 | Not sourced in this pass at all | No plan content -- see below |
| 7 | "Classic stack overflow... stripped of hand-holding" per one search summary, unverified | Likely the track's difficulty spike level; needs real source before any hint design |
| 8 (final) | Not sourced in this pass | No plan content |

## Structural fit against existing conventions

Same shape as the other four plans in this series: `targets/behemoth/`
mirroring `targets/bandit/`'s layout, a distinct banner palette/art
following the "primeval monster" lore in
`docs/future-wargame-theme-behemoth-2026-07-24.md`, and
`scripts/build_behemoth.py` with the same `TITLES`/`EXTRA_INFO`/
`HINTS`/`_render_description()` shape.

`docs/future-wargame-theme-behemoth-2026-07-24.md` already recommended
planning Behemoth's security review together with Narnia's, since both
are the same underlying risk category (memory-corruption binaries).
That recommendation stands and applies just as much to content
planning: with only 2 of 9 levels sourced here, Behemoth needs the most
additional research of the five tracks in this series before it's
buildable.

## What this needs before it's an actual implementation plan

- Levels 2 through 6, and level 8, have **no sourced content at all**
  in this pass -- not even topic labels. This plan should not be
  treated as covering the full game; it only covers roughly a third of
  it (2 of 9 levels with real detail, 1 more with a single unverified
  quote).
- The Medium article that appeared to be the most complete single
  source (a "Levels 0-8" walkthrough) could not be fetched due to a
  redirect loop in this pass -- retrying that fetch (or finding the
  content via a cache/archive) would likely close most of this gap in
  one pass, before resorting to piecing together individual per-level
  blog posts the way Utumno's plan had to.
- Same memory-corruption containment review needed as Narnia (see that
  plan's closing note) -- more so here, since Behemoth explicitly adds
  race conditions and privilege escalation on top of buffer overflows.
