# Self-Hosted Wargames: Status (CEI-Labs-Wargames)

**Status:** Merged to `main` (confirmed via `git merge-base --is-ancestor
fb30456 main`). Originally written from `feature/self-hosted-wargames` @
`fb30456` before that branch landed.
**Related:** [`cei-labs-engine` status](https://github.com/stoptalkingishh/cei-labs-engine/blob/main/docs/self-hosted-wargames-status.md) · [`cei-labs-net` status](https://github.com/stoptalkingishh/cei-labs-net/blob/main/docs/self-hosted-wargames-status.md) · full working checklist: `docs/self-hosted-wargames-blueprint.md`

## What this is

Bandit, Krypton, and Natas — previously pure CTFd metadata pointing at
OverTheWire's live, credential-rotating infrastructure — are now fully
self-hosted: real target images this repo builds, deployed on demand by
`cei-labs-engine`'s orchestrator, wired into CTFd via the `instance-launcher`
plugin. `main` still has the old OTW-pointing versions; this branch replaces
them entirely.

## What's done

| Track | Levels | Target image | Deployment model |
| :--- | :--- | :--- | :--- |
| Bandit | 34 (0-33) | `targets/bandit/` | `single-target`, one persistent SSH box, shared `instance_group: bandit` |
| Krypton | 7 (0-6) | `targets/krypton/` | `single-target`, same pattern; level 0 needs no instance at all |
| Natas | 15 (0-14) | `targets/natas/` | `target-attacker`, one range (kali-novnc attacker + LAMP target) per team, shared `instance_group: natas` |

All three are wired into CTFd via `scripts/build_{bandit,krypton,natas}.py`
(`instance_type`/`target_image`/`attacker_image`/`instance_group`/
`shutdown_on_solve` fields, synced by `deploy.sh`'s `sync_instance_mapping()`).

**Live-tested, not just written:**
- Every individual level across all three tracks was solved through its
  actual intended exploitation technique (not flag-copying) against a real
  running container, in batches, as each was authored.
- A full integration pass (real CTFd → orchestrator → hardened container
  chain) confirmed: 3 representative Bandit levels, all 6 automatable
  Krypton levels, 3 representative Natas levels; `instance_group` sharing
  (two challenges from the same group reuse one container — checked via
  `docker service ls` creation timestamps, not just "seemed to work");
  `shutdown_on_solve` timing (only the final level's solve starts the
  countdown, confirmed via the orchestrator's reaper log actually tearing
  the instance down after the delay); network isolation from CTFd/the
  orchestrator; inbound-port discipline (only the intended port reachable
  from outside, checked via direct socket probes).

## Player-experience content pass: hints and free reference material

A real playtest surfaced that the original single-hint-per-level system
(one hint, one cost) wasn't calibrated the way the user actually wanted,
and that OverTheWire's own real pages give players real, free direction
(a "Commands you may need" tool list and a "Helpful reading" links
section) on every level with no point cost at all. Both are now fixed
across all 56 real levels (not the 3 onboarding "Start Here" challenges,
whose descriptions are already full walkthroughs):

- **3-tier hints ("crawl/walk/run"), 168 total.** Tier 1 is a bare
  manpage name or a single reading link only — no explanation. Tier 2
  (~50% of the challenge's points) explains the underlying concept and
  names tier 1's tool/reference explicitly, but stops short of the exact
  command or payload. Tier 3 (~75%+ of the points, deliberately
  expensive) is a close-to-complete walkthrough of *why* and *how*,
  still without the literal flag value. `scripts/build_{bandit,krypton,
  natas}.py`'s `HINTS` dict holds these; the YAML generator emits a
  `hints:` block per challenge.
- **Free "Commands you may need to solve this level" + "Helpful
  reading"** sections, added to every level's description — Bandit's
  list was built directly from OverTheWire's own real page content
  (command lists and reading URLs provided directly by the user);
  Krypton/Natas reuse the same Wikipedia links already verified during
  hint authoring. Lives in each script's `EXTRA_INFO` dict, appended
  uniformly by the generator so the source data stays DRY.
- **Real bug found and fixed via structured testing:** three
  descriptions (written before the tier system existed) embedded the
  exact working technique for free — Krypton 1's full `tr` command,
  Natas 13's `GIF89a` magic bytes, Natas 14's SQLi payload — which made
  paying for those levels' tier-3 hints pointless. Found by actually
  self-testing as three fresh CTFd accounts (novice/intermediate/expert
  personas, zero prior solves) unlocking every tier live via the real
  API across 6 representative levels, not by reading source. Full
  findings: `cei-labs-engine/docs/hint-tier-persona-findings.md`.
- Also surfaced and fixed, unrelated to content: CTFd's DELETE-request
  CSRF check requires an explicit `Content-Type: application/json`
  header even on a bodyless request, or it silently falls through to a
  form-nonce check that a header-only client never satisfies — this was
  the real cause of several "403 on delete" incidents earlier in the
  project that had been written off as minor test noise.

**Verified live, not just written:** full YAML validation sweep across
all 59 generated `challenge.yml` files after every edit round, synced to
a running CTFd test instance, checked for zero duplicate/leftover hints
via the real admin API, and the fixed descriptions' live rendering
confirmed directly (not just diffed against source).

## Known open items

- **Content-accuracy pass not done:** the flags in `build_bandit.py`/
  `build_krypton.py`/`build_natas.py` were flagged early on as looking like
  they could be placeholder-style values. They're internally consistent
  (verified extensively — every level's exploit reveals exactly the next
  level's password, chain-checked end to end) but haven't been cross-checked
  against any external source of truth. Not blocking; independent of this
  infrastructure work.
- **Natas scope is 15 levels (0-14) by deliberate decision, not a gap** —
  confirmed with the user (2026-07-08). Real Natas's 34+ level catalog
  (including levels 25-26, PHP object injection) is explicitly out of scope
  here; extending it later is new content authoring, not a correction.
- **Level 33 (Bandit's final level) and Krypton's final LFSR mechanic are
  original designs**, not reconstructions of real OTW mechanics — noted
  where relevant in the target images' own comments, since no reliable
  public documentation of the real mechanics was found.
- Phase 6/7 hardening and full verification (see the `cei-labs-engine`
  status doc for what changed there) were run against this repo's images
  without needing any changes on this side — the target images themselves
  already ran as intended non-root users, with the orchestrator applying
  the new capability restrictions at the Swarm-service level.

## Not done at all

Nothing — this is all merged to `main` now (see the status note at the
top). No PRs were opened; merged directly.
