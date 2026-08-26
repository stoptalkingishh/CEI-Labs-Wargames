# Future wargame theme reference: Narnia (2026-07-24)

Reference material for building a future CEI Labs wargame modeled on
OverTheWire's Narnia, supplied by the user as part of a broader
lore/theme cheat sheet covering all OverTheWire wargames. Recorded here
for later use when this wargame is actually built -- not yet
implemented in `CEI-Labs-Wargames`. Notes only, no code changed.

## Source

- Upstream game: `overthewire.org/wargames/narnia`
- Category: Binary exploitation & memory corruption (first game in that
  category, per the cheat sheet's ordering)

## Lore / theme, as supplied

"Stepping Through the Wardrobe" -- entry into low-level memory (stack,
heap, RAM), uncovering the invisible world under the hood. The
wardrobe-as-portal framing (from C.S. Lewis's Narnia) maps directly to
the idea of a hidden world existing just behind/underneath the visible
program -- an apt metaphor for a player's first exposure to memory
layout and buffer-overflow-style bugs, as the entry point into the
binary-exploitation category the same way Bandit is the entry point for
Linux basics.

## How this compares to CEI Labs' existing theme conventions

As with the Leviathan note, existing tracks use a distinct per-track
color ramp plus per-level hand-drawn ASCII art tied to each level's
specific technique. A Narnia track's visual identity would want its own
palette (wardrobe/portal/hidden-world imagery per the lore) distinct
from Bandit's warm ramp and Krypton's cool ramp -- not evaluated
further since the track doesn't exist yet.

## What building this needs (not started, no code touched)

- A `targets/narnia/` directory mirroring `targets/bandit/`'s
  structure.
- A `scripts/build_narnia.py` challenge-definition script mirroring
  the existing scripts' shape.
- Narnia's content (stack/heap/format-string/memory-corruption
  challenges) is a different risk profile than Bandit/Krypton's
  filesystem-and-cipher puzzles -- building this will need its own
  security review pass (compiler flags, ASLR/PIE settings, whether
  binaries are deliberately vulnerable in ways that must stay
  contained to the per-team target container), not just a reskin of
  the existing generator scripts.
- A distinct color palette and per-level art themed to
  wardrobe/portal/hidden-world imagery, following the precedent in the
  two existing tracks' `generate_banners.py` files.
