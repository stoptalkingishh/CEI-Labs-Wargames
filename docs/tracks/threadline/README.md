# Threadline

**Threadline** is a full-length OSINT wargame for the CEI Labs event platform:
a 6–7 hour, 42-lead discovery campaign in which the player is an analyst for
the **Tiberian Order**. Each lead is a short (5–15 minute) Open-Source
Intelligence puzzle — geolocate a drop point, trace a vessel, decode a seized
file, or corroborate a public record — and every lead is a thread in a larger
conspiracy.

## Why the name

A **threadline** is a military line of advance — the path a force takes toward
an objective. On a loom, the *warp threads* run lengthwise and are woven into
the fabric. The hidden coordination node at the center of this campaign is
literally called **the Loom**: follow the threads, walk the threadline, and
unmask the Loom behind the cartels, hackers, corrupt generals, terrorist cells,
and a doomsday cult that all unknowingly feed it.

## Track shape

- **42 leads** across nine arcs (onboarding, cartel, wire syndicate, gilded
  generals, chancellery, order of hades, ashfall, house of krohndahkyr, loom).
- **Non-staged, hidden-by-default**, exactly like the AI Copilot track: no
  per-team Docker instance, no orchestrator mapping. Release manually with
  `THREADLINE_RELEASE_STATE=visible`.
- **Static flags, low collusion risk**: getting an OSINT answer *is* the work.
  All flags in `scripts/build_threadline.py` were verified against ground-truth
  sources (`hacktoria-archive/`) and are the single source of truth.
- Each lead's briefing popup ("Open Briefing") renders the source narrative
  pulled from the OCR'd evidence PDFs.

## Contents

| Doc | What it is |
|---|---|
| `storyline.md` | World, factions, the Loom meta-plot, challenge⇲beat table |
| `writeups.md` | 42-lead answer key (instructor/ organizer only) |
| `cheatsheet.md` | Fast-lookup table for instructors walking the room |
| `learning-objectives.md` | Skills inventory by concept |
| `event-runbook.md` | 7-hour run-of-show + pacing |
| `release-verification.md` | Pre-flight checklist before going visible |
| `briefing-transcripts.json` | OCR'd source-briefing narratives for the popups |
| `source-lineage.md` | Broader OSINT source and ownership context |

## Source and release boundary

Threadline is a curated campaign, not a direct import of every exercise in the
OSINT research catalog. Its lead-to-source mapping is in
`scripts/build_threadline.py`; the 39 non-capstone leads map to named packages
in the external `hacktoria-archive/` checkout, while the two Loom capstones use
the campaign's case-file structure. The broader Hacktoria, Gralhix, and
Bellingcat research is documented in the sibling OSINT track's
[`source-lineage.md`](../osint/source-lineage.md).

The generator falls back to committed briefing transcripts when the external
archive is unavailable, but missing source attachments must be recorded and
resolved before release. Generated output is always rebuilt from scratch under
`threadline/`.

## Build

```bash
THREADLINE_RELEASE_STATE=visible python3 scripts/build_threadline.py
```

Output goes to the git-ignored `threadline/` directory for `ctf challenge sync
threadline/`. Source evidence zips are read from the external
`hacktoria-archive/` checkout when present (images are attached only when it
is); the briefing text always comes from the committed transcripts.
