# Wargame-Building Playbook

The reusable methodology behind Bandit/Krypton/Natas, written so the
same approach can be used to build another track later without
re-deriving all of this from scratch.

## Track architecture choices

Two instance patterns cover everything built so far:

- **`single-target`** (Bandit, Krypton): one persistent SSH box shared
  across every level in the track. Levels are just different user
  accounts on the same box, each password-gated by the previous level's
  flag. Use this when the whole track is about interacting with one
  environment progressively (privilege escalation, cryptanalysis against
  a shared toolset, etc.) — it avoids spinning up N separate containers
  for N levels, and it's how OverTheWire's own real Bandit/Krypton work,
  which made mapping content over straightforward.
- **`target-attacker`** (Natas): a shared target box plus a **separate**
  attacker workstation (noVNC + SSH), because the puzzles are entirely
  HTTP-based and there's no reason to give a participant a shell on the
  target itself — that would leak the answer. Use this pattern whenever
  the track's puzzles live behind a network service the participant
  should interact with externally, not from a shell on the box hosting
  it.

Both patterns share one `instance_group` per track (all levels in a
track resolve to the same underlying environment), configured via the
`instance-launcher` CTFd plugin's admin mappings — this is what lets 34
Bandit levels reuse one box instead of needing 34 separate ones.

**Track release-gating** (letting an admin release Bandit/Krypton/Natas
independently, at their own pace, based on participant progress) was
scoped for this project but deferred — the user is researching/planning
it separately. Worth recording here for whoever builds it: a direct
source check of CTFd's own API (`CTFd/api/v1/challenges.py`) found no
built-in bulk-by-category visibility toggle — every challenge route
operates on a single `challenge_id`. `Brackets` is a skill-division
concept, unrelated. `ChallengeRequirements` (prerequisite challenges) is
real but player-solve-driven, not admin-action-driven. A future track
gating feature will likely need a small custom admin control (e.g., a
category-to-challenges bulk `state` toggle), not a rediscovery of an
existing CTFd mechanism.

## The "Start Here" onboarding pattern

Every track gets one challenge literally named "**\<Track\>: Start
Here**" whose job is purely to explain that track's specific connection
method and prove the participant used it (usually by fetching one
trivial, guaranteed-reachable file/value). This exists because the three
tracks genuinely connect differently (direct SSH vs. an attacker
workstation with noVNC/SSH options), and burying that explanation inside
level 1's own puzzle content would conflate "learning the tooling" with
"solving the first real puzzle." Keep this pattern for any new track
whose connection method isn't identical to an existing one.

## The 3-tier hint model

Every level (except an already-fully-explanatory Start Here) gets up to
3 hints, cheapest first:

1. **Tier 1 ("crawl")** — near-free (roughly 5–10% of the challenge's
   points). *Only* a bare tool/manpage name or a single reading link —
   no explanation of what it does or how it applies. For someone who
   already knows the concept but is rusty on the exact syntax.
2. **Tier 2 ("walk")** — about half the challenge's points. A real
   explanation of the underlying concept that names tier 1's tool/
   reference, but stops short of the literal command line or payload —
   the player still has to connect it to the problem themselves.
3. **Tier 3 ("run")** — most of the challenge's points (deliberately —
   using it should leave almost nothing to "win" by solving after). A
   near-complete walkthrough of the method: why it works and how to
   execute it, still requiring the player to actually run commands and
   read output rather than being handed the flag.

Alongside hints, every description gets a **free, always-visible**
"Commands you may need" + "Helpful reading" section — matching
OverTheWire's own real page structure, sourced from their actual public
pages where the track maps directly to OTW content. This is deliberately
*not* gated behind points; it's a pointer list, not a solution.

**Failure mode found and fixed, worth designing around next time:** a
description that goes even slightly beyond a bare pointer — e.g.,
naming the exact command *and* showing an example, or stating a literal
value that's supposed to be a discovery (a magic-byte signature, an
exact injection payload) — silently undercuts its own tier-1/tier-3
hints' cost, since the answer is now free. Caught during persona-based
review (see below) in 3 places (Krypton 1, Natas 13, Natas 14) after the
fact. When writing a new track's descriptions, treat "would this appear
in tier 1, or is it already tier-3 material?" as a checklist question,
not something to catch only in a later review pass.

## Build-script architecture

Each track has one `scripts/build_<track>.py` with three data
structures, kept deliberately separate to stay DRY and avoid duplicating
logic per level:

- `challenges_data`: the list of levels — id, name, points, description,
  flag.
- `HINTS`: `id -> list of exactly 3 hint-text strings`, cheapest/least-
  revealing first. There is no authored cost field here — every tier's
  price comes exclusively from `tier_costs(value)`
  (`scripts/hint_economy.py`), applied by `managed_tiers()` at build time,
  so a hand-typed cost would never actually be read.
- `EXTRA_INFO`: `id -> (commands_list, reading_list)`, appended by the
  generator to every description as the free Commands/Reading sections.

The generator loop composes these into `challenge.yml` per level via
plain Python f-string interpolation — **not PyYAML**. This is a
deliberate choice, not an oversight: it keeps content authoring as plain
Python data (easy to review, diff, and regenerate) without a library
round-trip. The cost is a real discipline requirement: **no literal `"`
character anywhere in description/hint content**, since it would break
the hand-built double-quoted YAML scalar. Use single quotes/backticks
instead. The one legitimate exception found so far (Natas 14's real
double-quote SQLi payload) used a proper YAML `\"` escape, written
carefully in the Python source as a double-backslash-plus-quote sequence
to produce the right 2-character escape in the generated file. Any new
track's content should follow the same rule; if PyYAML is ever adopted
instead, this whole class of gotcha goes away, but so does the ability
to trivially eyeball-diff the generator's own logic against plain data.

## Verification discipline

The single most valuable habit from this project: **verify against the
real deployed target, not against what "should" be true.** Concretely:

- **Live command execution over assumed correctness.** Two real,
  previously-undetected bugs (Bandit 1's `cat -- -` hang; Bandit 33's
  missing PATH-reset step after the rbash escape) were only caught by
  actually running the documented commands over a real PTY session
  against the live target image — both looked completely plausible on
  paper. Read-only review would not have caught either.
- **YAML validation sweeps** after every content regeneration — load
  every generated `challenge.yml` with a real YAML parser before
  syncing, not just eyeballing the source.
- **Persona-based review**: walk the same content as 3 distinct skill-
  level personas (novice/intermediate/expert), unlocking hints live via
  the real API rather than just reading source. This is what surfaced
  the description-leak failure mode above — a static read-through of
  the source didn't make the "this is too much free information" issue
  obvious the way replaying it as a first-time player did.
- **Checking claims against this repo's own target images**, not generic
  upstream writeups — even when a technique is well-documented elsewhere
  (e.g., the classic rbash `find -exec` escape), this project's specific
  image can have its own wrinkle (the PATH-inheritance detail) that a
  generic writeup won't mention.
- When a live test contradicts committed content, **fix both** the
  generator source and any already-synced live content, and **record
  the correction** (a "Verified live (\<date\>)" note in the writeup, a
  status-doc entry) rather than silently patching it — this is what
  makes the next person's verification pass faster instead of starting
  from zero trust again.

## Known platform limitations worth designing around next time

Full detail in `cei-labs-engine/docs/self-hosted-wargames-status.md` —
not duplicated here, but worth flagging up front for whoever plans the
next track:

- The orchestrator's in-memory state isn't shared across its 2 worker
  processes — expect real status/launch races under concurrent load
  until this gets a real architectural fix (shared/Redis-backed state,
  or a single-worker-plus-concurrency-elsewhere redesign).
- No reconciliation between the orchestrator's in-memory state and real
  Docker/Swarm state — a restart or manual Docker change can leave it
  reporting stale information.
- `relaunch` has a known, non-deterministic Swarm network-recreation
  race (retry-on-failure works around it; not fixed at the source).

None of these blocked shipping this project's content, but a future
track with heavier concurrent launch load (e.g., a much larger cohort)
would hit them more often — worth prioritizing a fix before scaling up
usage, not just content.
