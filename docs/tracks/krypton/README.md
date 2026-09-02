# Krypton

**Krypton** — cryptography, self-hosted recreation of OverTheWire's
[Krypton](https://overthewire.org/wargames/krypton/).

Players progress through increasingly difficult classical and modern ciphers,
working from a `krypton-start-here` on-boarding challenge through level 7.
Reinforces cipher recognition, cryptanalysis hygiene, and scripting to brute
small keyspaces.

## Doc set

- `learning-objectives.md` — skills inventory by concept
- `cheatsheet.md` — fast-lookup table for instructors walking a room
- `writeups.md` — complete solutions (instructor / organizer only)

## Build & release

```bash
python3 scripts/build_krypton.py         # writes challenges/ (git-ignored)
python3 scripts/validate_game_stages.py  # staged-track gate (Krypton = stage 2)
```

Target image: `targets/krypton/` (per-team via Docker Swarm + instance-launcher).
Krypton is a **staged / wave-gated** track defined in `game-stages.yml`.