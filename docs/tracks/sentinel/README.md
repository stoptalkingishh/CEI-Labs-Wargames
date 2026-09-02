# Sentinel

**Sentinel** — a defensive security lab track built for offline, safe,
observability-focused practice (SOC analyst / security-operations training).

The current generated pilot contains Start Here, labs 01–05, and six deferred
expansion labs (22–27). Labs 06–21 remain planned. All generated challenges are
hidden and non-staged until the target, evidence contracts, and runtime checks
are independently validated.

## Doc set

- `learning-objectives.md` — skills inventory by concept
- `cheatsheet.md` — fast-lookup table for instructors walking a room
- `writeups.md` — lab solutions (instructor / organizer only)
- `sentinel-lab-design-matrix.md` — lab inventory and design rationale
- `sentinel-tooling-research.md` — tooling research for the track
- `ooda/` — OODA-loop lab writeups (see sibling project
  `docs/tracks/sentinel-ooda/` for the review plan, findings, and ledger)

## Build & release

```bash
python3 scripts/build_sentinel.py   # writes sentinel/ (git-ignored)
```

Target image: `targets/sentinel/` (per-team via Docker Swarm + instance-launcher).
Sentinel ships **hidden by default** and lives outside the staged rollout.
