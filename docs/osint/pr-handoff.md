# OSINT Wargame — PR Handoff Report

> Status: **MERGED** (PR #86, `feat/osint-wargame` → `main`).
> This file summarizes the follow-up work done after the initial merge:
> local playtest validation, source-briefing recovery via OCR, and the
> on-theme "intel report" briefing popup. It is the single entry point for
> anyone picking up this track.

---

## 1. Where things live

| Concern | Location |
|---|---|
| Campaign generator (single source of truth for flags) | `scripts/build_osint.py` |
| Generated CTFd import YAML (git-ignored, not committed) | `osint/*/challenge.yml` |
| Per-lead metadata / skill / doctrine mapping | `scripts/build_osint.py` (`META`, `HINTS`) |
| Storyline & factions ("Gilded Hose", Tiberian Order, the Loom) | `docs/osint/storyline.md` |
| OCR'd source-briefing narratives (one entry per challenge) | `docs/osint/briefing-transcripts.json` |
| Instructor answer key | `docs/osint/writeups.md` |
| Release / pre-flight verification | `docs/osint/release-verification.md` |
| Local CTFd stack for black-box testing | `scripts/local-ctfd/` |
| Sync challenge files + descriptions into local CTFd | `scripts/local-ctfd/upload_osint_files.py` |
| OCR the source briefing PDFs → transcripts JSON | `scripts/local-ctfd/ocr_briefings.py` |

---

## 2. What changed in this handoff

### 2.1 Functional games-term changes

- **Source files attached to each non-capstone challenge** so every lead is
  playable without the original `hacktoria-archive/` zips. The generator picks
  the best evidence image (`starting-image-*`, `image-*`) and writes it under
  `osint/<id>/files/`, then `challenge.yml` lists it in `files:`.
- **The raw PDFs are NOT attached as downloads.** The source briefings are
  raster scans with **no text layer** (verified with pypdf + pdfplumber: 0
  glyphs on all 51 PDFs). So the generator instead:
  1. **OCR's each briefing** (via `scripts/local-ctfd/ocr_briefings.py` using
     RapidOCR) into `docs/osint/briefing-transcripts.json` (39 challenges,
     per-page text);
  2. renders that narrative inside a **"Source briefing (seized document)"**
     block.
- **"Open Briefing" popup** — a clean, on-theme intelligence report styled for
  the Tiberian Order / OSINT Directorate (off-white paper, slate + gold, a
  `FIELD TRACE` / `ORDERS` / `RECON` header tag, a `CEI-RESTRICTED // FOR
  TIBERIAN ORDER PERSONNEL` classification, structured summary, and
  "Exhibit N" transcribed pages). Implemented as a dependency-free fixed
  overlay toggled with inline vanilla JS — CTFd embeds the description as raw
  HTML (`CMARK_OPT_UNSAFE`), and a nested Bootstrap modal would silently fail
  to open inside CTFd's own modal, so we deliberately avoid Bootstrap here.

### 2.2 ASCII / encoding hardening

- `scripts/build_osint.py` generates ASCII-safe YAML end-to-end (Windows
  CP1252-safe). One ground-truth flag that contained Cyrillic was transliterated
  to keep generated YAML loadable by `ctfcli` on Windows:
  - `Антонівка-Херсонськаобласть-Кіндійська-35/6` → `Antonivka-Khersonska-Kindijska-35-6`
  - Mirrored in `docs/osint/writeups.md` and `docs/osint/release-verification.md`.

---

## 3. Local black-box playtest instance

`scripts/local-ctfd/` provides a minimal CTFd stack (no Traefik, no Swarm) with
the wargame plugins baked into the image from `CEI_LABS_ENGINE_PATH`.

```powershell
cd scripts\local-ctfd
$env:CEI_LABS_ENGINE_PATH="C:\Users\Ismael\.buzz\REPOS\cei-labs-engine"
docker compose up -d --build
# browse http://localhost:8000  (admin/CTFd once-setup, see setup_local_ctfd.py)
```

Playtest results (local instance, 2026-08-27):

- All **42 OSINT challenges** listed via `/api/v1/challenges?view=admin`.
- **All 42 descriptions** verified non-empty after the popup embed.
- **39 evidence images** attached (one per non-capstone lead); the 2 capstones
  and the start-here briefing intentionally have no image.
- **39 PDF attachments removed** from the instance (the popup replaced them).
- Verified the live popup for `Cartel Air-Drop Lane` contains the real PDF
  prose ("Greetings, Special Agent … Los Aztecas").

Re-sync a rebuilt track into a fresh local CTFd:

```powershell
$env:CTFD_TOKEN="ctfd_<token>"
python scripts\local-ctfd\upload_osint_files.py --remove-pdfs
```

> The admin token in `.ctf/config` is git-ignored and stays local.

---

## 4. Regenerating the track

```bash
CEI_OSINT_RELEASE_STATE=visible python3 scripts/build_osint.py
```

Re-OCR (only if you want to re-run transcription — output already committed):

```bash
python3 scripts/local-ctfd/ocr_briefings.py
```

CI already runs `python3 scripts/build_osint.py` in `validate.yml` (generation
must stay idempotent and ASCII-safe).

---

## 5. TODO / next steps for maintainers

- Verify OCR transcripts read naturally on the live events board (RapidOCR
  transcription of stylized covers can be noisy — spot-check a few Exhibits).
- Confirm the `hacktoria-archive/` location is documented/reachable for anyone
  who wants to re-OCR from source. The archive itself is not committed.
- Confirm the deployed CTFd has `HTML_SANITIZATION` disabled (it is by default
  here) so raw-HTML descriptions render; if that setting is ever enabled, the
  popup markup + inline script would be sanitized away and you'd need a real
  plugin.