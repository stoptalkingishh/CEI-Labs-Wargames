# Future wargame theme reference: Leviathan (2026-07-24)

Reference material for building a future CEI Labs wargame modeled on
OverTheWire's Leviathan, supplied by the user as part of a broader
lore/theme cheat sheet covering all OverTheWire wargames. Recorded here
for later use when this wargame is actually built -- not yet
implemented in `CEI-Labs-Wargames`. Notes only, no code changed.

## Source

- Upstream game: `overthewire.org/wargames/leviathan`
- Category: Linux & entry-level labs (same category as Bandit, one
  step up in difficulty)

## Lore / theme, as supplied

"The Mythological Sea Monster" -- stepping up from a simple bandit to
face a massive, daunting binary beast without source code access. The
framing shift from Bandit's "petty thief sneaking around file
permissions" to a "sea monster" signals a jump from filesystem/
permissions puzzles to binary analysis without visible source, i.e.
players go from reading things that are just hidden to reverse-
engineering things that are opaque by nature.

## How this compares to CEI Labs' existing theme conventions

Both existing tracks (`CEI-Labs-Wargames/targets/bandit/build/generate_banners.py`
and `targets/krypton/build/generate_banners.py`) use a per-track color
identity (Bandit: warm amber->ember->dusk->maroon ramp; Krypton: cool
icy-blue->cyan->magenta) plus per-level hand-designed ASCII art tied to
that level's specific technique, with the banner text embedding the
same title string CTFd shows for the challenge. A Leviathan track would
need its own distinct palette and its own per-level art motifs (sea/
depth/monster imagery given the lore above) to fit that same pattern --
not evaluated further here since the track doesn't exist yet.

## What building this needs (not started, no code touched)

- A `targets/leviathan/` directory mirroring `targets/bandit/`'s
  structure (Dockerfile, `build/` setup scripts, `entrypoint.sh` for
  per-team flag substitution, `generate_banners.py`).
- A `scripts/build_leviathan.py` challenge-definition script mirroring
  `build_bandit.py`/`build_krypton.py`'s shape (`TITLES`, `EXTRA_INFO`,
  `HINTS`, `_render_description()`).
- A distinct color palette (not reusing Bandit's warm ramp or Krypton's
  cool ramp) and per-level ASCII art themed to "sea monster"/depth
  imagery, following the precedent set by the two existing tracks'
  `generate_banners.py` files.
- Confirming how many of upstream Leviathan's levels CEI Labs wants to
  reproduce, and whether flags/passwords follow the same per-team
  dynamic-flag chaining pattern Bandit and Krypton use.
