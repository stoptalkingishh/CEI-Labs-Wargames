# OSINT Wargame — Track Design

A new **Open-Source Intelligence** wargame for the CEI-Labs CTF deployment,
built from real-world OSINT training bodies (Hacktoria, Gralhix's OSINT
exercises, and the Bellingcat Challenge — indexed in
[`osint-research-index.md`](osint-research-index.md)). It is the first track in
this repository whose "target" is **the public web and the participant's own
workstation**, not a shared per-team Docker box.

## Why it is a non-staged, hidden track

This track deliberately follows the AI Copilot Setup precedent:

- **No per-team Docker instance.** Every skill (geolocation, reverse image
  search, satellite/FIRMS, EXIF, marine/AIS, aviation/ICAO, web-archives,
  calendar, decoding) runs against legal, publicly-available information (PAI)
  and free web tools. There is no instance mapping and no orchestrator to
  launch — so it contributes **0 instance mappings**, exactly like the AI track.
- **Flags are the *produced answer*** (a place, an ICAO code, a note-text
  double, a what3words triple, a sourced judgement). Because getting the answer
  *is* the work, a static flag does not create the collusion risk that a
  "type this exact string" answer would — the same rationale the AI track uses.
- **Hidden by default, released manually** by the organizer, like
  `build_agent.py`'s `CEI_AGENT_RELEASE_STATE=visible` flow.

This keeps `game-stages.yml` and all three stage-count validators unchanged:
OSINT is **not** a fourth "staged" boss.

## Naming

- Challenges live under the `osint-` id prefix and the player-facing name is
  "OSINT" (category: `OSINT`).
- The track defines 13 challenges: `osint-start-here` plus 12 skill drills.
- Import output is written to the git-ignored `osint/` directory by
  `scripts/build_osint.py`, ready for `ctf challenge sync osint/` when the
  organizer chooses to release it.

## Skill ladder (from the source research)

| Tier | Character | Example node | Est. effort |
|---|---|---|---|
| A (crawl) | Single-tool direct answer | a landmark photo -> name/coords | 5–10 min |
| B (walk) | One transform, then a geo | decode/EXIF/capture -> geo | 15–30 min |
| C (run) | Multi-clue, cross-toolchain, corroborate | a "mini case": bind 2+ independent sources to a judgement | 30–60+ min |

## The twelve drills (id, skill, doctrine anchor)

1. `osint-01-geolocation` — IMINT / GEOINT, IPB ground-truth (Tier A)
2. `osint-02-reverse-image` — provenance / source recovery (Tier A->B)
3. `osint-03-chronolocation` — sun/solar temporality (Tier B)
4. `osint-04-satellite-fire` — remote-sensing / thermal (Tier B)
5. `osint-05-exif` — metadata forensics, "eat it fresh" (Tier A)
6. `osint-06-calendar` — non-Gregorian / temporal (Tier B)
7. `osint-07-aviation-icao` — aviation / aircraft ID (Tier B)
8. `osint-08-maritime-ais` — AIS / vessel / registry (Tier B->C)
9. `osint-09-what3words` — precise coordinate encoding (Tier A)
10. `osint-10-web-archive` — archive / "eat it fresh" / Wayback (Tier B)
11. `osint-11-social-footprint` — social-media PAI, legal boundary (Tier C)
12. `osint-12-corroborate` — cross-verification & reliability (capstone, Tier C)

Every challenge's description carries a free "Tools + Method" pointer list and
the full doctrine vocabulary is recorded per-challenge in
[`learning-objectives.md`](learning-objectives.md).

## Authoring & verification

The `build_osint.py` generator holds each answer/flag in one place so the flag
in `osint/*/challenge.yml` stays in lock-step with `writeups.md` and the
instructor `cheatsheet.md`. Before a production release, each listed *answer* —
the coordinates, ICAO codes, dates, w3w triples — must be re-verified against
real public sources exactly as the wargame-building playbook requires for live
targets; until then the answers in this tree are **illustrative placeholders**
to be confirmed at release time (they are swapped in `build_osint.py`, not by
hand-editing generated files).

## Deliverables in this folder

- [`osint-research-index.md`](osint-research-index.md) — the source/doctrine index
- [`learning-objectives.md`](learning-objectives.md) — per-concept skills + doctrine
- [`cheatsheet.md`](cheatsheet.md) — instructor walk-the-room fast lookup
- [`writeups.md`](writeups.md) — step-by-step answer key (instructor only)