#!/usr/bin/env python3
"""OCR the retired 42-lead campaign's source briefing PDFs to transcripts.

Kept as historical/local tooling for the superseded 42-lead OSINT campaign.
The source briefings are raster scans (no text layer), so this uses RapidOCR
to transcribe each page. Output:
    docs/tracks/osint/archive/briefing-transcripts.json
mapping challenge-id -> {source, pages}. ASCII-safe output.

The challenge->zip mapping below is frozen from the retired campaign. It is
independent of scripts/build_osint.py (which became a plugin adapter and no
longer carries this table), so this tool still runs against a checkout of
hacktoria-archive/.

Run: python scripts/local-ctfd/ocr_briefings.py
"""
import io
import json
import zipfile
from pathlib import Path

import pypdfium2 as pdfium
from rapidocr_onnxruntime import RapidOCR

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE_DIR = ROOT.parent / "hacktoria-archive"
OUT = ROOT / "docs" / "tracks" / "osint" / "archive" / "briefing-transcripts.json"

# Frozen from the retired 42-lead campaign (scripts/build_osint.py
# CHALLENGE_SOURCE_ZIP at commit 7c0cdec).
CHALLENGE_SOURCE_ZIP = {
    "osint-01-cartel-airdrop": "florida-snow.zip",
    "osint-02-cartel-safehouse": "the-cartel-connection.zip",
    "osint-03-cartel-precursor": "gas-attack.zip",
    "osint-04-cartel-meet": "a-strange-file.zip",
    "osint-05-synd-exfil": "on-the-wire.zip",
    "osint-06-synd-intercept": "operation-wiretap.zip",
    "osint-07-synd-beacon": "emergency-transmission.zip",
    "osint-08-synd-burn": "the-copycat-killer.zip",
    "osint-09-synd-wallet": "the-sleeper-cell.zip",
    "osint-10-synd-deaddrop": "dialogues-from-atlantis.zip",
    "osint-11-gen-tank": "friendly-fire.zip",
    "osint-12-gen-frigate": "naval-intrusion.zip",
    "osint-13-gen-airfield": "cold-war-enemies.zip",
    "osint-14-gen-aircraft": "last-flight.zip",
    "osint-15-chan-strike": "line-of-control.zip",
    "osint-16-chan-ao": "prisoner-of-war.zip",
    "osint-17-chan-smuggle": "road-to-nowhere.zip",
    "osint-18-chan-fleet": "undercover_fleet.zip",
    "osint-19-chan-manifest": "lost-at-sea.zip",
    "osint-20-chan-cover": "the-road-to-rome.zip",
    "osint-21-hades-operative": "operation-bloodhound.zip",
    "osint-22-hades-cutout": "rogue-agent.zip",
    "osint-23-hades-payment": "echoes-of-retaliation.zip",
    "osint-24-hades-hostage": "kidnapped.zip",
    "osint-25-hades-hit": "the-killer-clown.zip",
    "osint-26-hades-slayer": "the-midnight-slayer.zip",
    "osint-27-ash-strike": "substation-bombing.zip",
    "osint-28-ash-distress": "saving-isabella.zip",
    "osint-29-ash-freelancer": "the-russian-blackmailer.zip",
    "osint-30-cult-funnel": "alien-abduction.zip",
    "osint-31-cult-origin": "chasing-bigfoot.zip",
    "osint-32-cult-signal": "appalachian-aliens.zip",
    "osint-33-cult-cipher": "klumgongyn-returns.zip",
    "osint-34-cult-caravan": "wheres-klumgongyn.zip",
    "osint-35-cult-ledger": "return-of-the-krohndahkyr.zip",
    "osint-36-cult-prophecy": "lost-in-time.zip",
    "osint-37-cult-relic": "nightmare-fuel.zip",
    "osint-38-cult-money": "peepeekun.zip",
    "osint-39-cult-cache": "kanonniers.zip",
}


def main():
    if not ARCHIVE_DIR.is_dir():
        print(f"skip: source archive not found at {ARCHIVE_DIR}", file=sys.stderr)
        return

    ocr = RapidOCR()
    reverse = {}  # zip -> list of cids
    for cid, zname in CHALLENGE_SOURCE_ZIP.items():
        reverse.setdefault(zname, []).append(cid)

    transcripts = {}
    for zname, cids in reverse.items():
        zip_path = ARCHIVE_DIR / zname
        if not zip_path.is_file():
            print(f"skip: {zname} missing", file=sys.stderr)
            continue
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

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(transcripts, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    import sys
    main()