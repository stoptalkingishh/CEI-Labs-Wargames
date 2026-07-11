# Security Audit: Status (CEI-Labs-Wargames)

**Related:** [`cei-labs-net` status](../../cei-labs-net/docs/security-audit-status.md) · [`cei-labs-engine` status](../../cei-labs-engine/docs/security-audit-status.md)

## What this is

A full cybersecurity audit of all three repos in this ecosystem
(`CEI-Labs-Wargames`, `cei-labs-engine`, `cei-labs-net`), run as three
parallel independent reviews. **Deliberately excludes every intentional
teaching vulnerability in Bandit/Krypton/Natas** — SUID escalation, SQL
injection, command injection, restricted-shell escapes, etc. are the
whole point of this platform and are not findings. This doc covers this
repo's one fixed finding and one open decision; see the related docs
above for the other two repos'.

## Findings and fixes (merged to `main`)

| Severity | Finding | Branch | Verification |
| :--- | :--- | :--- | :--- |
| Low | `targets/natas/build/03-generate-vhosts.py` created every level's htpasswd file with `htpasswd`'s own default mode (644, root-owned) — world-readable to every OTHER level's MPM-ITK worker (each vhost's `AssignUserID` runs as a different `natasN` user, but they share the filesystem). A player with code execution at any one level (e.g. the intended natas12/13 upload RCE) could read every other level's bcrypt hash directly, not just the next one via the intended `/etc/natas_webpass` leak chain. | `fix/natas-htpasswd-permissions` (merged) | **Fully verified**, re-run once Docker recovered. Rebuilt `targets/natas` fresh and booted it: every one of the 15 htpasswd files now shows `-rw------- 1 natasN natasN` (was `-rw-r--r-- 1 root root`). Confirmed no regression — Basic Auth against natas0 still succeeds with the real level password (`200`) and correctly rejects a wrong one (`401`). Incidental finding along the way: this repo had **no `.gitattributes` at all**, so every `.sh`/`.py`/Dockerfile was CRLF-corrupted on this Windows checkout — the same bug class already fixed in `cei-labs-engine` — which broke the build via a corrupted shebang until fixed (see the `.gitattributes` commit on `main`). |

## Open decision — resolved, now in progress

**Static flags/passwords across every deployment** (Medium severity):
confirmed real — this platform runs competing teams in the same event
and/or reuses challenges across cohorts, so identical flags enabled both
same-event collusion and cross-event leakage. User chose the full fix
(true per-team-unique flags, not just per-event rotation) over the
plan's `docs/self-hosted-wargames-blueprint.md`-style phased approach —
see the plan at the time this was scoped for the full architecture and
phase breakdown.

**Phase 1 (foundation + Krypton level 2) is done, merged, and fully
verified** against a live redeployed stack — see this repo's and
`cei-labs-engine`'s latest commits. Levels across Bandit/Krypton/Natas
are converted one phase at a time; `build/03-generate-vhosts.py` and the
rest of `build_bandit.py`/`build_krypton.py`/`build_natas.py`/
`targets/*/build/*` still hold hardcoded, identical-per-deployment
values until their phase lands.

## Not done

The natas htpasswd finding is merged to `main` and fully verified. The
static flags/passwords fix is in progress (Phase 1 of 4 done) — Natas
(all 15 levels), the rest of Krypton, and Bandit (34 levels) remain.
