# Build plan: Utumno (2026-07-24)

Level-by-level content plan for a future CEI Labs Utumno track,
assembled from several individual per-level blog posts rather than one
comprehensive walkthrough (no single-source overview was found for
this game, unlike Leviathan's mayadevbe.me overview or Maze's l3o
post). Structured to match the conventions already established by
Bandit/Krypton/Natas in `CEI-Labs-Wargames`. Planning doc only -- no
code, targets, or challenge definitions created in this pass.

## Sources

- `nicolagatta.blogspot.com`'s individual Utumno level posts (levels
  0, 1, 2, 3, 4, 7 -- found via search, summarized from search results,
  not individually fetched and read in full in this pass)
- `r4stl1n.github.io`'s Utumno0 post (found in search, not fetched)
- Upstream: `overthewire.org/wargames/utumno` confirms 10 levels
  (utumno0-utumno9), difficulty 4/10, framed as "harder than Leviathan,
  a bit harder than Behemoth." No per-level text published there.
- Multiple GitHub walkthrough-collection repos found in search
  explicitly mark their own Utumno sections "Coming Soon" / not
  started -- worth noting that comprehensive public coverage of this
  specific game appears genuinely thin, not just under-searched here.

## Level-by-level plan (10 levels, utumno0 -> utumno9) -- confidence noted per row

| Level | Technique (confidence) | CEI Labs equivalent notes |
|---|---|---|
| 0 | `ptrace`-based tracing of the binary's own syscalls to recover behavior/password (low-medium confidence -- search-summarized, not fetched) | New tool category (`ptrace`), no existing precedent in this repo's hint ladders |
| 1 | Binary scans a directory for filenames via `strncmp` -- likely a filename/path trick similar in spirit to Leviathan's 2->3 (low-medium confidence) | Could share hint-design lessons with the Leviathan plan's level 2->3 once both are built |
| 2 | `strcpy` vulnerability involving environment variables (low-medium confidence) | Same category as Narnia/Behemoth's unsafe-function levels, but via env-var injection specifically |
| 3 | Buffer overflow, shellcode placed in an `EGG` environment variable with NOP padding, redirecting execution flow (low-medium confidence) | First "classic NOP-sled shellcode injection" level referenced across all five plans in this series -- if built, this is likely the best level to establish that technique's hint-ladder pattern for reuse in Behemoth/Maze |
| 4 | Binary copies a second argument onto the stack, sized by the first argument -- sounds like an attacker-controlled-length stack write (low-medium confidence) | Not enough detail to design hints yet |
| 5-6 | Not sourced in this pass at all | No plan content |
| 7 | Buffer overflow exploitation involving stack addresses (low confidence -- one-line search summary only) | Not enough detail to design hints yet |
| 8-9 | Not sourced in this pass at all | No plan content |

## Structural fit against existing conventions

Same shape as the other plans: `targets/utumno/` mirroring
`targets/bandit/`'s layout, a distinct banner palette/art following the
"deep fortress" lore in `docs/future-wargame-theme-utumno-2026-07-24.md`,
and `scripts/build_utumno.py` with the same `TITLES`/`EXTRA_INFO`/
`HINTS`/`_render_description()` shape.

`docs/future-wargame-theme-utumno-2026-07-24.md` already recommended
planning Utumno's actual technical content once Narnia and Behemoth
exist, so difficulty/technique progression across the category is
coherent. This plan doesn't have enough source depth to confirm or
challenge that sequencing decision either way.

## What this needs before it's an actual implementation plan

- Levels 5, 6, 8, and 9 have **no sourced content at all** -- 4 of 10
  levels are completely unresearched in this pass, and the remaining 6
  are individually sourced from search-result summaries rather than
  fetched and read directly (unlike the Bandit/Krypton/Natas
  cross-references, which quoted exact fetched text).
- Given public walkthrough coverage for this specific game appears
  thin across the board (several dedicated OverTheWire-walkthrough
  repos explicitly mark it "Coming Soon"), closing the remaining gaps
  may take more effort than the other four games in this series, or
  may need to lean more on original design/testing against upstream
  Utumno directly rather than secondary sources.
- Same memory-corruption containment review needed as Narnia/Behemoth.
