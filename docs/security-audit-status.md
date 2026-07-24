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
| Critical | Two compounding Bandit bugs let the 34-level chain be mostly skipped from bandit0. (1) `targets/bandit/build/01-create-users.sh` `chmod 755`'d every `/home/banditN` home directory, and the per-level flag/password files written by `03-setup-levels-00-12.py`, `entrypoint.sh` (levels 10-12), `06-setup-levels-17-18.py`, `09-setup-levels-25-26.py`, and `11-setup-level-32.py` were all mode 0644 — both world-readable, so any level's flag could be `cat`'d directly from bandit0 with no puzzle solved. (2) `targets/bandit/src/level19_setuid.c`, installed setuid-root (`chmod 4755`) per the Dockerfile, dropped privilege to bandit20 and ran `system(argv[1])` with **no check on the caller's UID at all** — any account, including bandit0, could run it and jump straight to a bandit20 shell. | `fix/bandit-permissions` | **Fully verified**, rebuilt `targets/bandit` fresh from source and booted it with synthetic per-team `LEVEL_SECRETS`. Confirmed every home dir is now `drwxr-x---` (was `755`) and every flag file now matches the level-6 reference pattern — owned `bandit(N+1):banditN`, mode `0640` (was `0644` self-owned) — e.g. `/home/bandit0/readme` is now `-rw-r----- bandit1 bandit0`. Confirmed `su bandit0 -c 'cat /home/bandit5/.../.file2'` now fails with `Permission denied`, while each level's own user (tested bandit0, bandit5, bandit26, bandit32) still reads its own next-level flag via the group bit — progression not broken. For the SUID binary: added a `getuid() == bandit19's uid` check (looked up via `getpwnam`, not a hardcoded UID) before the privileged `system()` call; confirmed `bandit0` invoking `/home/bandit19/bandit20-do` is now rejected (`"This binary may only be run by bandit19."`, exit 1) even when tested against a copy placed at a world-executable, world-traversable path (to isolate the UID check from the now also-fixed home-directory permission), while `bandit19` running the real installed binary still correctly gets a `bandit20` shell (`uid=1020(bandit20)`). No regressions: password chain (`chpasswd`) and CTFd-style login flow unaffected. |

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
