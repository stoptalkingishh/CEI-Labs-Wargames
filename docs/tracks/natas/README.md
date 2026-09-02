# Natas

**Natas** — server-side web security, self-hosted recreation of OverTheWire's
[Natas](https://overthewire.org/wargames/natas/).

Players work through 34 levels of web vulnerabilities (path traversal, source
disclosure, injection, crypto misuse, clickjacking, upload RCE lessons) from a
`natas-start-here` on-boarding challenge. Each level is a listening web app on
its own port.

## Doc set

- `learning-objectives.md` — skills inventory by concept
- `cheatsheet.md` — fast-lookup table for instructors walking a room
- `writeups.md` — complete solutions (instructor / organizer only)
- `natas-12-13-rce-isolation-audit.md` — security audit of the intentional
  upload-RCE lesson containers

## Build & release

```bash
python3 scripts/build_natas.py            # writes challenges/ (git-ignored)
python3 scripts/validate_game_stages.py   # staged-track gate (Natas = stage 3)
python3 scripts/runtime_audit_natas.py    # opt-in local integration audit
```

Target images: `targets/natas/` (per-team) + `targets/natas-attacker/`
(participant workstation). Natas is a **staged / wave-gated** track defined in
`game-stages.yml`.