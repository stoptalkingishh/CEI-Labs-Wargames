# OSINT Wargame — Handoff Report

> **Status:** Superseded by the plugin pilot (see §2). This file records the
> full history of the OSINT track so anyone picking it up understands what was
> built, what was playtested, and why the current generator is the way it is.

---

## 1. TL;DR

- **Where the track is now:** `main` runs a small, neutral **plugin-based OSINT
  pilot**. `scripts/build_osint.py` is an adapter that exports reviewed artifact
  bundles from the separately maintained `ctfgen-family-osint` package; it no
  longer generates a 42-lead campaign locally. See
  `docs/osint/README.md` and the pilot entries in `CHANGELOG.md`.
- **Why:** after an earlier 42-lead campaign was merged and locally playtested,
  the project retired those 42 placeholder proposals (their source evidence
  packages aren't in this repository) in favor of the reviewed plugin pilot.
- **Where the earlier work went:** `docs/osint/archive/` — `legacy-idea-bank.json`
  (neutral skill ideas), plus `briefing-transcripts.json`,
  `participant-quickstart.md`, and `release-verification.md` (kept as a record
  of the campaign and its validation).
- **Local tooling that still works:** `scripts/local-ctfd/upload_osint_files.py`
  (syncs any `osint/` output into a local CTFd) and
  `scripts/local-ctfd/ocr_briefings.py` (re-OCR the retired campaign's source
  briefings into the archive). Both are independent of which generator produced
  the challenge folders.

---

## 2. Timeline

1. **42-lead campaign designed & generated** (`feat/osint-wargame`, PR #86
   merged). `scripts/build_osint.py` produced 42 leads (storyline arcs, factions,
   flags) into the git-ignored `osint/`. Docs: `storyline.md`, `writeups.md`,
   `cheatsheet.md`, `event-runbook.md`, etc.
2. **Local playtest** (2026-08-27). A local CTFd stack
   (`scripts/local-ctfd/docker-compose.yml`) validated: 42 challenges listed,
   descriptions non-empty, 39 evidence images attached, and the "Open Briefing"
   popup rendered the real source-briefing narrative.
3. **PDF content recovered via OCR.** The briefing PDFs are raster scans with
   no text layer (verified: pypdf + pdfplumber extract 0 glyphs). RapidOCR
   transcribed all 39 source briefings → `briefing-transcripts.json`, and the
   popup was restyled as an on-theme intel report (Tiberian Order / OSINT
   Directorate).
4. **Project pivot (PRs #88/#89).** `main` retired the 42 placeholder proposals
   and switched `scripts/build_osint.py` to the plugin adapter exporting the
   reviewed `ctfgen-family-osint` pilot (3 vertical cases, typed answer
   verifiers, no storyline). The campaign docs were archived.
5. **Reconciliation.** This handoff merges the playtest tooling + documentation
   into `main` and archives the retired-campaign artifacts, without restoring
   the retired generator.

---

## 3. Where things live now

| Concern | Location |
|---|---|
| OSINT adapter (plugin pilot, canonical) | `scripts/build_osint.py` |
| Pilot docs & state | `docs/osint/README.md` |
| Generated CTFd import YAML (git-ignored) | `osint/*/challenge.yml` |
| Retired 42-lead skill ideas | `docs/osint/archive/legacy-idea-bank.json` |
| Retired campaign: OCR'd briefings | `docs/osint/archive/briefing-transcripts.json` |
| Retired campaign: player quickstart | `docs/osint/archive/participant-quickstart.md` |
| Retired campaign: release verification | `docs/osint/archive/release-verification.md` |
| Local CTFd stack for black-box testing | `scripts/local-ctfd/` |
| Sync files + descriptions into local CTFd | `scripts/local-ctfd/upload_osint_files.py` |
| Re-OCR retired source briefings | `scripts/local-ctfd/ocr_briefings.py` |

---

## 4. Local test instance

`scripts/local-ctfd/` provides a minimal CTFd stack (no Traefik, no Swarm) with
the wargame plugins baked into the image from `CEI_LABS_ENGINE_PATH`.

```powershell
cd scripts\local-ctfd
$env:CEI_LABS_ENGINE_PATH="C:\Users\Ismael\.buzz\REPOS\cei-labs-engine"
docker compose up -d --build
# browse http://localhost:8000 ; admin credentials per setup_local_ctfd.py
```

Sync a generated track (pilot or campaign) into the instance:

```powershell
$env:CTFD_TOKEN="ctfd_<token>"
python scripts\local-ctfd\upload_osint_files.py --remove-pdfs
```

Playtest results (retired 42-lead campaign, 2026-08-27):

- 42 challenges present via `/api/v1/challenges?view=admin`.
- 42 descriptions non-empty (after the popup embed).
- 39 evidence images attached (one per non-capstone lead).
- 39 retired PDF attachments pruned (the popup replaced them).
- Verified the popup for `Cartel Air-Drop Lane` contained the real PDF prose
  ("Greetings, Special Agent … Los Aztecas").

---

## 5. Maintainer TODOs

- Spot-check the plugin pilot's generated challenges on the live board
  (the pilot ships no storyline; confirm that's intended).
- Move `scripts/local-ctfd/ocr_briefings.py` dependencies
  (`pypdfium2`, `rapidocr_onnxruntime`) into a dev-requirements file if you
  plan to re-run it; they are not runtime dependencies.
- If `HTML_SANITIZATION` is ever enabled on the deployment, the raw-HTML
  briefing popup markup (retired campaign) would be sanitized away — that only
  affects archived artifacts, not the pilot.

---

## 6. Reference: retired campaign details

For anyone who wants to study or revive the 42-lead design (e.g. to re-read the
OCR'd briefings or the answer key), the archived files above are the record.
The generator that produced them is in `git history` (branch
`feat/osint-wargame`, up to and including commit `7c0cdec`); it is intentionally
**not** restored on `main`.