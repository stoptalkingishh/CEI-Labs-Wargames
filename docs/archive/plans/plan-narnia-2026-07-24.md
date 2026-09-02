# Build plan: Narnia (2026-07-24)

Level-by-level content plan for a future CEI Labs Narnia track. Source
coverage for this game is notably thinner than Leviathan's -- flagged
explicitly below rather than papered over. Structured to match the
conventions already established by Bandit/Krypton/Natas in
`CEI-Labs-Wargames`. Planning doc only -- no code, targets, or
challenge definitions created in this pass.

## Sources

- `laurentiu-raducu.medium.com/overthewire-narnia-walkthrough-...`
  (fetched directly, but only actually covers narnia0->1 in detail:
  a `scanf()`-based stack buffer overflow overwriting an adjacent
  stack variable)
- `github.com/jynxora/OverTheWire-Narnia-Series-Walkthrough` (fetched;
  its own README lists a level-by-level technique table, but the table
  content read back as generic category labels -- e.g. "Advanced
  stack-based payload construction," "Final exploitation techniques
  (specifics not detailed)" -- not concrete per-level vulnerability
  descriptions the way Leviathan's and Maze's sources gave. Treat this
  table as a rough topic outline only, not verified fact.)
- Upstream: `overthewire.org/wargames/narnia` confirms 10 levels
  (narnia0-narnia9), source code provided per level, "most common
  bugs" framing; no per-level text published there.

## Level-by-level plan (10 levels, narnia0 -> narnia9) -- confidence noted per row

| Level | Technique (confidence) | CEI Labs equivalent notes |
|---|---|---|
| 0->1 | Stack buffer overflow via unsafe `scanf()` overwriting an adjacent variable (high confidence -- directly sourced) | First stack-smashing level for CEI Labs; needs a from-scratch tier-1 hint introducing stack layout, since no existing track covers memory corruption |
| 1->2 through 8->9 | General "basic exploitation, most common bugs" per upstream framing: unsafe functions (`gets`, `strcpy`, `sprintf`), offset calculation, return-address redirection, environment-variable tricks, privilege escalation via vulnerable SUID binaries (low-to-medium confidence -- topic labels only, not verified against real level content) | Cannot be responsibly turned into specific hint text yet -- see "what this needs" below |

## Structural fit against existing conventions

Same shape as the Leviathan plan: `targets/narnia/` mirroring
`targets/bandit/`'s Dockerfile/build/entrypoint.sh layout, a new
distinct banner palette and per-level art following the "wardrobe/
hidden-world" lore already recorded in
`docs/future-wargame-theme-narnia-2026-07-24.md`, and a
`scripts/build_narnia.py` with the same `TITLES`/`EXTRA_INFO`/`HINTS`/
`_render_description()` shape as the existing three tracks.

One structural difference worth flagging: upstream Narnia gives players
the source code of each level's vulnerable binary. None of Bandit/
Krypton/Natas currently ship source code alongside a challenge (Bandit/
Krypton hand over binaries or ciphertext to analyze blind; Natas hands
over server-side PHP source via the browser, which is different from
distributing a standalone C source file). Narnia would need a new
delivery mechanism -- e.g. the source file placed in the level's home
directory, or attached to the CTFd challenge itself -- that doesn't
have a direct precedent in this codebase yet.

## What this needs before it's an actual implementation plan (not just this doc)

- **Source depth is insufficient past level 0->1.** Only one level has
  a concretely verified vulnerability description; the other 9 are
  category labels from a low-confidence source. Before writing real
  `HINTS`/`desc` text or building actual vulnerable binaries, someone
  needs to fetch and verify each individual level's real technique --
  either from `overthewire.org`'s own level pages once SSH-accessible,
  or from a more granular walkthrough series than what was found in
  this pass (e.g. `hackmethod.com`'s per-level posts, which were found
  in search results but not fetched here).
- This is the first CEI Labs track involving actual memory-corruption
  vulnerable binaries -- needs its own security/containment review
  (compiler flags, ASLR/PIE/stack-canary settings per level, whether a
  crashed/corrupted target process can affect anything outside its own
  container) before real implementation, independent of content
  planning.
