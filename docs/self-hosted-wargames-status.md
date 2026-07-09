# Self-Hosted Wargames: Status (CEI-Labs-Wargames)

**Branch:** `feature/self-hosted-wargames` @ `10e8750` (not merged to `main` @ `d306195`)
**Related:** [`cei-labs-engine` status](../../cei-labs-engine/docs/self-hosted-wargames-status.md) · [`cei-labs-net` status](../../cei-labs-net/docs/self-hosted-wargames-status.md) · full working checklist: `docs/self-hosted-wargames-blueprint.md`

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

- **No PRs opened, nothing merged to `main`.** Everything above is
  committed and pushed to the feature branch only. Merging is a deliberate
  separate decision, not bundled into this work.
