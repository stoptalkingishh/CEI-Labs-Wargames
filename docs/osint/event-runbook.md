# OSINT Wargame — Event Runbook (6–7 hour session)

Run-of-show for facilitators executing the **42-lead "Gilded Hose" campaign**.
Pairs with `cheatsheet.md` (fast lookup) and `writeups.md` (answer key).

## Event shape

- **Duration:** 6.5 h core + 30 min buffer = **7 h wall clock** (trim Arc 7 to
  run 6 h).
- **Format:** teams of 2–4 on one scoreboard; every lead is a solo-solvable
  5–15 min puzzle, so split arcs across the team and swap drivers per arc.
- **Ordering:** leads are numbered in intended play order — light→heavy, and
  each arc's first lead is its easiest anchor skill. Teams may skip ahead, but
  the capstone (`osint-41`) assumes notes from earlier arcs.
- **Release model:** track ships hidden; organizer releases manually
  (`CEI_OSINT_RELEASE_STATE=visible python3 scripts/build_osint.py`, then sync).

## Timeline (7-hour plan)

| Clock | Block | Leads | Facilitator focus |
|---|---|---|---|
| T+0:00 | Kickoff + briefing | `osint-00-start-here` | Rules, legal/PAI boundary, tool check (Maps/reverse-image/EXIF/w3w/FIRMS/MarineTraffic/Wayback/CyberChef). Everyone solves start-here. |
| T+0:15 | **Arc 1 — Cartel** | 01–04 | Warm-up geolocation. Watch for tool friction; this is where laggards get unstuck early. (~50 min) |
| T+1:05 | **Arc 2 — Wire Syndicate** | 05–10 | Digital forensics. Heaviest tooling block — have CyberChef + a pcap viewer pre-installed. (~60 min) |
| T+2:05 | Break | — | 10 min hard stop. |
| T+2:15 | **Arc 3 — Gilded Generals** | 11–14 | Military recognition IDs. Fast wins; keep energy up. (~45 min) |
| T+3:00 | **Arc 4 — Chancellery** | 15–20 | Multi-step chains incl. centerpiece `18-chan-fleet`. Mid-event slump risk — announce progress here. (~70 min) |
| T+4:10 | Lunch / break | — | 20 min. |
| T+4:30 | **Arc 5 — Order of Hades** | 21–26 | Cryptanalysis-heavy. Point stuck teams at cheatsheet nudges before hints. (~70 min) |
| T+5:40 | **Arc 6 — Ashfall** | 27–29 | Cross-platform footprint work; remind OPSEC/legal boundary. (~35 min) |
| T+6:15 | **Arc 7 — Cult** | 30–39 | Long varied tail. For a 6 h event cut to any 5 of these. (~75 min) |
| T+7:00→ | **Arc 8 — Loom capstone** | 40–41 | Corroboration then fused assessment. Score generously on sourcing quality, not just the flag string. |

**6-hour trim:** drop leads 36–39 from Arc 7 (keep 30–35) — the capstone still
works because it keys on arcs 1–6 artifacts.

## Facilitation notes

- **Hint economy:** OSINT is not wallet-managed; give verbal tiered nudges
  straight from `cheatsheet.md` ("crawl → walk → run") before revealing method.
- **The storyline is framing-only:** if a team asks how fiction relates to the
  solve, answer briefly and redirect to the premise line — no extra steps hide
  in flavor text.
- **Link-graph ritual:** after each arc, have teams write one line in their case
  file: which entity recurred (a company, a lane, a wallet, a drop). This makes
  the capstone trivial to attempt even for slower teams.
- **Legal guardrail to repeat:** public info only; never contact/message a real
  person or account surfaced during play.
- **Scoring:** flags are static (the work is the proof). Consider bonus points
  for cited reasoning on 40/41 rather than speed.

## Pre-flight checklist

- [ ] `python3 scripts/build_osint.py` (hidden default) or with
      `CEI_OSINT_RELEASE_STATE=visible`, then `ctf challenge sync osint/`.
- [ ] Answers re-verified against live sources (all flags are placeholders until
      then — see `writeups.md` header).
- [ ] Workstations have: browser + Google account, one reverse-image engine,
      EXIFTool, what3words access, CyberChef, a pcap viewer (Wireshark), audio
      spectrogram tool (Audacity), SQLite browser.
- [ ] Network allowlist updated for the external sites above (see
      `docs/network-access.md`).
- [ ] Print/share `participant-quickstart`-style one-pager + the legal boundary.