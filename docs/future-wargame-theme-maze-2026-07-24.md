# Future wargame theme reference: Maze (2026-07-24)

Reference material for building a future CEI Labs wargame modeled on
OverTheWire's Maze, supplied by the user as part of a broader
lore/theme cheat sheet covering all OverTheWire wargames. Recorded here
for later use when this wargame is actually built -- not yet
implemented in `CEI-Labs-Wargames`. Notes only, no code changed.

## Source

- Upstream game: `overthewire.org/wargames/maze`
- Category: Binary exploitation & memory corruption (listed last in
  the cheat sheet's ordering for this category)

## Lore / theme, as supplied

"The Labyrinth" -- complex, non-linear exploit paths where one wrong
step breaks the payload entirely. Distinct from Narnia/Behemoth/
Utumno's "descending into depth" framing -- Maze's metaphor is about
path complexity and fragility (a single misstep invalidates the whole
attempt) rather than escalating difficulty depth, suggesting its
challenge design should emphasize precise, order-sensitive exploit
chains rather than just harder individual bugs.

## How this compares to CEI Labs' existing theme conventions

Same visual-identity pattern as the other future-track notes in this
series. Because Maze's lore is thematically distinct from the other
three binary-exploitation tracks (labyrinth/path imagery rather than
depth/descent imagery), its palette and art don't need to follow the
Narnia->Behemoth->Utumno "darker/deeper" lineage the way those three
logically would relative to each other -- not evaluated further since
the track doesn't exist yet.

## What building this needs (not started, no code touched)

- A `targets/maze/` directory mirroring `targets/bandit/`'s structure.
- A `scripts/build_maze.py` challenge-definition script.
- Given the "one wrong step breaks the payload" framing, this track's
  design should be checked for whether CEI Labs' existing per-team
  instance/relaunch model (see `docs/local-testing-deployment.md` and
  the orchestrator's relaunch behavior in `cei-labs-engine`) fits
  cleanly -- e.g. whether a broken exploit attempt should be
  recoverable via relaunch without losing progress on earlier levels,
  which wasn't checked in this pass.
- A distinct color palette and per-level art themed to labyrinth/path
  imagery, following the precedent in the existing tracks'
  `generate_banners.py` files.
