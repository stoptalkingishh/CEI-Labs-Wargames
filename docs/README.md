# Documentation Index

This folder is the repository's full documentation surface. Everything live
(the stuff you use to build, run, teach, and release) sits in **guides**,
**tracks**, and **reference**. Everything finished or one-off sits in
**archive** — history preserved, out of the way.

---

## Guides — evergreen operator / instructor / participant material

Under `docs/guides/`.

| Doc | What it is |
|---|---|
| `learning-objectives.md` | Cross-track skills index + meta-skills |
| `challenge-inventory.md` | Generated index of every challenge; audited by CI |
| `instructor-cheatsheet.md` | Index into each track's fast-lookup table |
| `facilitation-runbook.md` | How to run a live event, start to finish |
| `participant-quickstart.md` | One-pager for players |
| `troubleshooting-faq.md` | Known issues and fixes |
| `wargame-building-playbook.md` | Reusable methodology for building the next track |
| `network-access.md` | External sites hints link to; firewall-allowlist source of truth |
| `offline-dependency-audit.md` | Offline capability analysis and pinned dependency audit |
| `self-hosted-wargames-blueprint.md` | Full self-hosted architecture blueprint |
| `self-hosted-wargames-status.md` | Current status of the self-hosted build-out |
| `staggered-game-stages.md` | Bandit/Krypton/Natas grouping + pre-deploy validation contract |
| `staged-game-operations.md` | Rehearsal and event-day controls for released game stages |
| `security-audit-status.md` | Security audit state for all target images |
| `security-lab-intake.md` | Backlog of proposed offline lab concepts |
| `hint-wallet-sync-deployment.md` | Hint-wallet sync + deployment notes |
| `natas-completion-status.md` | Natas build/release status |
| `game-completion-status.md` | Current source, generated-scope, and release-readiness status for every track |

## Tracks — per-wargame documentation

Under `docs/tracks/`. The three primary self-hosted tracks share the core set
(`README.md`, `learning-objectives.md`, `cheatsheet.md`, `writeups.md`).
The additional tracks use the same pattern where applicable and retain their
own design, release, and evidence documents.

| Track | Docs | Type |
|---|---|---|
| [bandit](tracks/bandit/) | README + 3 core | Staged (Linux basics) |
| [krypton](tracks/krypton/) | README + 3 core | Staged (cryptography) |
| [natas](tracks/natas/) | README + 3 core + RCE-isolation audit | Staged (web security) |
| [sentinel](tracks/sentinel/) | README + 3 core + design matrix + tooling + `ooda/` | Hidden lab (defensive) |
| [sentinel-ooda](tracks/sentinel-ooda/) | README + ledger/findings/remediation + review-plan | Companion project |
| [osint](tracks/osint/) | README + source lineage/research index + 3-case pilot docs + archive | Hidden pilot |
| [threadline](tracks/threadline/) | README + storyline/runbook + 3-core-ish + transcripts | Hidden full campaign |

## Reference

- `reference/comptia-security-plus-sy0-701-v7-objectives.md` — COMPTIA Security+ mapping source

## Presentation

- `docs/presentation/` — kickoff-brief and game-guide-brief sources used to run
  the room

## Archive — history, preserved

Under `docs/archive/`. These are finished, historical, or one-off records.
Read them for context; don't treat them as the source of truth for anything
current.

| Folder | Contents |
|---|---|
| `events/` | Event recaps, communications, deploy logs |
| `worklogs/` | Infra/ops work logs (server, swarm, CTFd) |
| `plans/` | Superseded plans (per-track expansions, clean-room builds, future builds) |
| `future-themes/` | Future wargame theme references (Behemoth, Leviathan, Maze, Narnia, Utumno) |
| `gaps/` | Dated gap-analyses and cross-reference notes (Bandit/Krypton/Natas hints, spoilers, live links) |
| `art/` | Wargame story + banner-gallery proposals |

---

## Where the generated content lives

- `challenges/` — generated CTFd challenge folders for the three staged games
  and AI Copilot (git-ignored)
- `sentinel/` — generated CTFd challenge folders for the hidden Sentinel track
  (git-ignored; intentionally separate from the staged-game export)
- `osint/`, `threadline/` — generated output for the hidden OSINT tracks
  (git-ignored)
- `scripts/` — generators, validators, and tests (`test_*.py`)
- `targets/` — per-track Docker targets (built for Bandit/Krypton/Natas/Sentinel)
