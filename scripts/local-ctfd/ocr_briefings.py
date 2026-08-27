#!/usr/bin/env python3
"""OCR each mapped OSINT briefing PDF and write per-challenge transcripts.

The source briefings are raster scans with no text layer, so this uses
RapidOCR to transcribe each page. Output: docs/osint/briefing-transcripts.json
mapping challenge-id -> list of page transcripts, keyed by the source PDF.
ASCII-safe output. Run: python scripts/local-ctfd/ocr_briefings.py
"""
import importlib.util
import io
import json
import sys
import zipfile
from pathlib import Path

import pypdfium2 as pdfium
from rapidocr_onnxruntime import RapidOCR

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("build_osint", ROOT / "scripts" / "build_osint.py")
build = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build)
ARCHIVE_DIR = ROOT.parent / "hacktoria-archive"
OUT = ROOT / "docs" / "osint" / "briefing-transcripts.json"

ocr = RapidOCR()
reverse = {}  # zip -> list of cids
for cid, zname in build.CHALLENGE_SOURCE_ZIP.items():
    reverse.setdefault(zname, []).append(cid)

transcripts = {}
for zname, cids in reverse.items():
    zip_path = ARCHIVE_DIR / zname
    with zipfile.ZipFile(zip_path) as zf:
        pdf_names = [n for n in zf.namelist() if n.lower().endswith(".pdf") and "__macosx" not in n.lower()]
        if not pdf_names:
            continue
        data = zf.read(pdf_names[0])
    pdf = pdfium.PdfDocument(data)
    pages = []
    for i in range(len(pdf)):
        bmp = pdf[i].render(scale=200 / 72).to_pil()
        png = io.BytesIO()
        bmp.save(png, format="PNG")
        png.seek(0)
        result, _ = ocr(png.getvalue())
        if result:
            pages.append("\n".join(item[1] for item in result).strip())
        else:
            pages.append("")
    print(f"OCR {zname}: {len(pages)} pages ({sum(len(p) for p in pages)} chars)")
    for cid in cids:
        transcripts[cid] = {"source": zname, "pages": pages}

OUT.write_text(json.dumps(transcripts, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(f"wrote {OUT}")