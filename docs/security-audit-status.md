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

## Open decision — not something I decided unilaterally

**Static flags/passwords across every deployment** (Medium severity, no
branch/fix): every flag and password in `scripts/build_bandit.py`,
`build_krypton.py`, `build_natas.py`, and the `targets/*/build/*`
scripts is hardcoded and identical across every deployment of this
platform. This is clearly an intentional, heavily-commented
reproducibility tradeoff ("must match CTFd's already-defined flags
exactly"), not an oversight — but it's real risk if this platform ever
runs concurrent teams/cohorts sharing images without per-instance flag
randomization on the CTFd side. Left entirely untouched pending an
explicit decision on whether that scenario is real for how this
platform actually gets used. If it is, this needs its own planning pass
(coordinated changes across the build scripts *and* wherever CTFd's own
flag values get set) — not a small fix to bolt on here.

## Not done

The one finding is merged to `main` and fully verified. The static
flags/passwords item above remains an open decision, not a fix — no
branch exists for it pending that decision.
