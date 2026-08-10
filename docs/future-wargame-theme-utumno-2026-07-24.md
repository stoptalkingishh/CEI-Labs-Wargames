# Future wargame theme reference: Utumno (2026-07-24)

Reference material for building a future CEI Labs wargame modeled on
OverTheWire's Utumno, supplied by the user as part of a broader
lore/theme cheat sheet covering all OverTheWire wargames. Recorded here
for later use when this wargame is actually built -- not yet
implemented in `CEI-Labs-Wargames`. Notes only, no code changed.

## Source

- Upstream game: `overthewire.org/wargames/utumno`
- Category: Binary exploitation & memory corruption (progression step
  up from Behemoth, per the cheat sheet's ordering)

## Lore / theme, as supplied

"Tolkien's Deep Fortress" -- named after Melkor's subterranean fortress
in Middle-earth; represents diving into the deepest, darkest depths of
advanced software exploitation. Continues the category's escalating
"depth" framing (Narnia's hidden world -> Behemoth's monster within it
-> Utumno's fortress at the very bottom), positioning this as the
category's advanced tier.

## How this compares to CEI Labs' existing theme conventions

Same visual-identity pattern as the other future-track notes in this
series. If Narnia and Behemoth get built with a shared "hidden world/
monster" visual lineage, Utumno's palette would logically go darker/
deeper still (fortress-in-the-depths imagery) to signal it's the
advanced tier of the same category -- not evaluated further since the
track doesn't exist yet.

## What building this needs (not started, no code touched)

- A `targets/utumno/` directory mirroring `targets/bandit/`'s
  structure.
- A `scripts/build_utumno.py` challenge-definition script.
- As the advanced tier of the binary-exploitation category, this
  track's actual technical content and security-review needs should
  be planned once Narnia and Behemoth exist, so difficulty and
  technique progression across all three is coherent rather than each
  being designed in isolation.
- A distinct color palette and per-level art following the "deep
  fortress" lore, following the precedent in the existing tracks'
  `generate_banners.py` files.
