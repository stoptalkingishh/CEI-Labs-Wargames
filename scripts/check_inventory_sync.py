#!/usr/bin/env python3
"""Fail CI if docs/guides/challenge-inventory.md drifts from the generated challenges.

docs/guides/challenge-inventory.md is a committed, human-audited index that answers
the event tracker's P0 inventory item. It says of itself: "regenerate by
re-running the extraction against current challenge.yml files if content
changes" -- but nothing enforced that, so a builder change (a level added,
renamed, repriced, or dropped) could silently leave the inventory describing
challenges that no longer exist, or missing new ones. This script is the
mechanical check:

  a) every generated challenge id must appear in the doc, matched with
     word-boundary-anchored regex (a substring like ``bandit-00`` inside
     ``bandit-001`` must not false-pass), and every challenge id cited as a
     table row in the doc must correspond to a generated challenge
     (bidirectional);
  b) each inventory row's Points cell must equal the generated
     ``challenge.yml`` ``value:``;
  c) each inventory row's "Hints (cost)" cell must equal the current
     schedule from scripts/hint_economy.py (``tier_costs``): wallet-managed
     challenges show ``3 (<t1>%/<t2>%/<t3>%)``, everything else shows ``0``.

Run AFTER the build_<track>.py scripts (challenges/ is generated and
gitignored). Exits 0 when in sync; exits non-zero and prints every mismatch
when drifted (2 = prerequisites missing, 1 = drift).
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hint_economy import TIER_PERCENTS

CHALLENGES_DIR = Path("challenges")
INVENTORY_DOC = Path("docs/guides/challenge-inventory.md")

# Challenges whose hints are priced by the hint-wallet plugin; the start-here
# tutorials and the AI Copilot Setup track carry no hints (cell "0").
WALLET_MANAGED_ID = re.compile(r"^(bandit|krypton|natas)-\d{2}$")

VALUE_LINE = re.compile(r"^value:\s*(\d+)\s*$", re.M)
TABLE_ROW = re.compile(r"^\s*\|(.+)\|\s*$")
CELL_ID = re.compile(r"^`([^`]+)`$")


def id_pattern(challenge_id: str) -> re.Pattern:
    """Word-boundary-anchored match: no substring false-passes (ids contain
    hyphens/digits, so treat [A-Za-z0-9-] as 'word' characters here)."""
    return re.compile(r"(?<![A-Za-z0-9-])" + re.escape(challenge_id) + r"(?![A-Za-z0-9-])")


def expected_hints_cell(challenge_id: str) -> str:
    """The Hints (cost) cell in the doc's display format, derived from the
    only cost formula the hint wallet enforces (hint_economy.tier_costs)."""
    if WALLET_MANAGED_ID.match(challenge_id):
        t1, t2, t3 = TIER_PERCENTS
        return f"3 ({t1}%/{t2}%/{t3}%)"
    return "0"


def generated_challenges() -> dict[str, int]:
    """Map every generated challenge id to its challenge.yml point value."""
    out = {}
    for p in sorted(CHALLENGES_DIR.glob("*/challenge.yml")):
        m = VALUE_LINE.search(p.read_text(encoding="utf-8"))
        if m is None:
            raise ValueError(f"{p}: no 'value:' line found")
        out[p.parent.name] = int(m.group(1))
    return out


def doc_rows(doc: str) -> dict[str, list[str]]:
    """Parse markdown table rows keyed by a backtick-quoted first cell.

    Returns {challenge_id: [stripped cells]} for every table row whose first
    cell is a backtick-quoted id (the inventory rows and the static-flag
    finding rows alike)."""
    rows = {}
    for line in doc.splitlines():
        m = TABLE_ROW.match(line)
        if not m:
            continue
        cells = [c.strip() for c in m.group(1).split("|")]
        if not cells:
            continue
        cid = CELL_ID.match(cells[0])
        if cid:
            rows[cid.group(1)] = cells
    return rows


def main() -> int:
    if not CHALLENGES_DIR.is_dir():
        print("error: challenges/ does not exist -- run the build_<track>.py scripts first")
        return 2
    try:
        generated = generated_challenges()
    except ValueError as e:
        print(f"error: {e}")
        return 2
    if not generated:
        print("error: no generated challenges found -- run the build_<track>.py scripts first")
        return 2
    if not INVENTORY_DOC.is_file():
        print(f"error: {INVENTORY_DOC} not found")
        return 2

    doc = INVENTORY_DOC.read_text(encoding="utf-8")
    rows = doc_rows(doc)

    problems = []

    # (a) Bidirectional id sync, word-boundary anchored.
    missing_from_doc = [i for i in generated if not id_pattern(i).search(doc)]
    if missing_from_doc:
        problems.append(
            "generated challenges missing from docs/guides/challenge-inventory.md: "
            + ", ".join(missing_from_doc)
        )
    only_in_doc = [i for i in rows if i not in generated]
    if only_in_doc:
        problems.append(
            "ids documented in docs/guides/challenge-inventory.md but not generated: "
            + ", ".join(sorted(only_in_doc))
        )

    # (b/c) Per-row Points and Hints (cost) checks on inventory rows
    # (7-cell rows; the 4-cell static-flag finding rows carry neither).
    for cid, value in sorted(generated.items()):
        cells = rows.get(cid)
        if cells is None or len(cells) < 6:
            continue
        try:
            doc_points = int(cells[1])
        except ValueError:
            problems.append(f"{cid}: Points cell {cells[1]!r} is not an integer")
            continue
        if doc_points != value:
            problems.append(
                f"{cid}: Points drift -- doc says {doc_points}, challenge.yml value is {value}"
            )
        expected_hints = expected_hints_cell(cid)
        if cells[5] != expected_hints:
            problems.append(
                f"{cid}: Hints (cost) drift -- doc says {cells[5]!r}, "
                f"hint_economy schedule is {expected_hints!r}"
            )

    if problems:
        print("inventory drift detected (regenerate docs/guides/challenge-inventory.md):")
        for p in problems:
            print(f"  {p}")
        return 1

    print(f"inventory in sync: {len(generated)} generated challenges all documented.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
