# Security Audit: Status (CEI-Labs-Wargames)

**Related:** [`cei-labs-net` status](https://github.com/stoptalkingishh/cei-labs-net/blob/main/docs/security-audit-status.md) · [`cei-labs-engine` status](https://github.com/stoptalkingishh/cei-labs-engine/blob/main/docs/security-audit-status.md)

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

## Open decision — resolved and DONE (all 4 phases complete)

**Static flags/passwords across every deployment** (Medium severity):
confirmed real — this platform runs competing teams in the same event
and/or reuses challenges across cohorts, so identical flags enabled both
same-event collusion and cross-event leakage. User chose the full fix
(true per-team-unique flags, not just per-event rotation).

All four phases are merged to `main` and verified end-to-end against a
live redeployed stack, with two simulated teams, covering every
mechanism across all 56 levels (flat files, byte-count-sensitive files,
transforms, TCP/TLS daemons, SUID binaries, a randomized brute-force
PIN, and all 5 git mechanisms) — see the commit history in this repo and
`cei-labs-engine` for full details per phase.

**Formerly a known remaining gap, now closed**: Bandit level 13's SSH
keypair (used to reach bandit14 without a password) used to be generated
once per image BUILD, not per TEAM, so every team on the same image
build shared the literal same private key — any team that reached level
13 could also SSH straight into every OTHER team's bandit14 with it, a
team-isolation break independent of the per-team flag work above. Fixed
by moving the `ssh-keygen` call (and the wiring that drops the private
key into bandit13's home dir and installs the public key into
bandit14's `authorized_keys`) out of `targets/bandit/build/04-setup-level-13.sh`
and into `targets/bandit/entrypoint.sh`, so it now runs fresh per
container/team at start, the same way every other per-team secret is
generated. Guarded so a Reboot of the same container doesn't rotate the
key out from under a player who already downloaded it.

**Incidental finding, fixed along the way** (not part of the original
audit, but discovered and closed during the Natas phase): several
Natas levels (6, 8, 11, 14) had their next-level password/final-flag
readable via their own `?source` view-source feature, without solving
anything — closed by moving those values into a separate runtime-written
include file the main page never dumps via `highlight_file()`.

## Not done

Content generation is fully converted. **Syncing the real 56-level
content into a live CTFd instance via `ctfcli`/`deploy.sh` still needs to
happen** — this requires generating a CTFd admin API token, a durable
credential deliberately not created without explicit user direction (see
`cei-labs-engine`'s status doc). The live stack itself is redeployed
fresh with every image rebuilt from these changes and ready for that
step.
