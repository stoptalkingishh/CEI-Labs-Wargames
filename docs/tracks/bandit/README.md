# Bandit

**Bandit** — Unix/Linux basics, self-hosted recreation of OverTheWire's
[Bandit](https://overthewire.org/wargames/bandit/).

Players log in over SSH and progress through 34 levels of escalating Linux
shell command-line skill (navigation, permissions, file processing,
pipelining, cron, scripting). A `bandit-start-here` on-boarding challenge
teaches the workflow.

## Doc set

- `learning-objectives.md` — skills inventory by concept
- `cheatsheet.md` — fast-lookup table for instructors walking a room
- `writeups.md` — complete solutions (instructor / organizer only)

## Build & release

```bash
python3 scripts/build_bandit.py          # writes challenges/ (git-ignored)
python3 scripts/validate_game_stages.py  # staged-track gate (Bandit = stage 1)
```

Target image: `targets/bandit/` (per-team via Docker Swarm + instance-launcher).
Bandit is a **staged / wave-gated** track defined in `game-stages.yml`.