# OSINT Source Lineage and Scope

This document explains how the original OSINT research request became the
current pilot and Threadline tracks. It is the maintainer-facing source and
scope record; it does not reproduce third-party challenge content.

## Original source set

The research phase considered four source bodies:

| Source | Role in the research | Current repository use |
|---|---|---|
| [Hacktoria CTF events](https://hacktoria.com/tag/ctf-events) and the supplied `hacktoria-archive/` package | Story-driven OSINT contracts, evidence packaging, geolocation, maritime, aviation, decoding, and public-record investigations | Primary inspiration and evidence lineage for the separate 42-lead Threadline campaign. The archive is an external checkout, not a tracked repository directory. |
| [Gralhix OSINT exercises](https://gralhix.com/list-of-osint-exercises) | Single-skill progression: geolocation, chronolocation, satellite imagery, EXIF, calendars, and aviation | Curriculum and tool-selection reference; not directly imported as CTF content. |
| [Bellingcat Challenge](https://challenge.bellingcat.com) | Image provenance, geolocation, satellite, historic research, audio, and corroboration practice | Curriculum and analytical-tradecraft reference; not directly imported as CTF content. |
| [Supplied archive download](https://filedn.eu/lUjfgD4ARTG5FVP7w924bsy/hacktoria-archive) | Initial source-delivery mechanism for the Hacktoria archive | Historical input. Use the local archive checkout and its provenance records rather than assuming the URL remains available. |

The detailed research table, selected examples, tool taxonomy, and doctrine
mapping are in [`osint-research-index.md`](osint-research-index.md).

## Why there are two OSINT tracks

The original 42-lead campaign was technically playtested, but its source
evidence packages were not reliably present in this repository. Its answers,
attachments, licensing, and provenance could therefore not be treated as a
production release. The campaign was retained as Threadline, hidden by default,
with its source archive and release checks made explicit.

The canonical OSINT pilot was narrowed to three reviewed artifact cases supplied
by the external `ctfgen-family-osint` package. That package owns the evidence,
private ground truth, and typed verifier specifications. This repository owns
the CTFd adapter and release-state control only.

| Track | Source of truth | Scope | Release boundary |
|---|---|---|---|
| OSINT pilot | External `ctfgen-family-osint` package + `scripts/build_osint.py` adapter | Three reviewed artifact-investigation methods | Hidden by default; requires the external plugin, typed-answer-flags support, organizer review, and evidence-gate completion |
| Threadline | `scripts/build_threadline.py`, committed transcripts, and optional external `hacktoria-archive/` checkout | 42 fictionalized leads across 9 arcs | Hidden by default; requires source re-verification, organizer review, and an available evidence archive |

## Evidence and attribution rules

- Do not copy generated CTFd files back into source documentation.
- Do not treat a representative research example as a released challenge.
- Preserve public/private boundaries: participant bundles may contain public
  artifacts only; private answer specifications remain verifier metadata.
- Record source URL, retrieval date, license/provenance, archived fallback, and
  safety/privacy review before adding a pilot case.
- Re-check volatile public answers immediately before releasing Threadline or
  any future research-derived case.

## Maintainer references

- [`pr-handoff.md`](pr-handoff.md) — complete history of the 42-lead campaign,
  playtest, OCR work, and plugin pivot
- [`skill-building-priority.md`](skill-building-priority.md) — evidence gate
  for pilot selection
- [`../threadline/release-verification.md`](../threadline/release-verification.md)
  — Threadline release checklist
- [`../../guides/game-completion-status.md`](../../guides/game-completion-status.md)
  — current completion and release-readiness status for all games
