# Future wargame theme reference: Behemoth (2026-07-24)

Reference material for building a future CEI Labs wargame modeled on
OverTheWire's Behemoth, supplied by the user as part of a broader
lore/theme cheat sheet covering all OverTheWire wargames. Recorded here
for later use when this wargame is actually built -- not yet
implemented in `CEI-Labs-Wargames`. Notes only, no code changed.

## Source

- Upstream game: `overthewire.org/wargames/behemoth`
- Category: Binary exploitation & memory corruption (progression step
  up from Narnia, per the cheat sheet's ordering)

## Lore / theme, as supplied

"Primeval Monster" -- wrestling with heavier memory corruption like
race conditions and complex buffer overflows. Continues the
category's "creature" naming pattern (Narnia's wardrobe leads to a
hidden world; Behemoth is a bigger, older monster within it),
signaling a difficulty step up within the same broad skill area rather
than a new category.

## How this compares to CEI Labs' existing theme conventions

Same visual-identity pattern as the other future-track notes in this
series: existing tracks each get a distinct color ramp and per-level
art tied to their own lore. If Narnia gets built first with a
"wardrobe/portal" palette, Behemoth would want a visually related but
distinct identity (e.g. a darker/heavier variant) to signal
progression within the same category the way Bandit's warm ramp
darkens tier-over-tier -- not evaluated further since the track
doesn't exist yet.

## What building this needs (not started, no code touched)

- A `targets/behemoth/` directory mirroring `targets/bandit/`'s
  structure.
- A `scripts/build_behemoth.py` challenge-definition script.
- Like Narnia, this category's challenge content (race conditions,
  more complex buffer overflows) carries a different security review
  burden than the filesystem/cipher tracks -- worth planning Narnia
  and Behemoth's security review together rather than duplicating that
  work, given they're the same underlying risk category.
- A distinct color palette and per-level art following the "bigger/
  older monster" lore, following the precedent in the existing tracks'
  `generate_banners.py` files.
