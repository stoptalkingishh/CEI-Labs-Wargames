#!/usr/bin/env python3
"""Fail CI if docs/challenge-inventory.md drifts from the generated challenges.

docs/challenge-inventory.md is a committed, human-audited index that answers
the event tracker's P0 inventory item. It says of itself: "regenerate by
re-running the extraction against current challenge.yml files if content
changes" -- but nothing enforced that, so a builder change (a level added,
renamed, or dropped) could silently leave the inventory describing
challenges that no longer exist, or missing new ones. This script is the
mechanical check: every generated challenge directory's id must appear in
the inventory doc.

Run AFTER the build_<track>.py scripts (challenges/ is generated and
gitignored). Exits non-zero and prints the mismatch.
"""

import sys
from pathlib import Path

CHALLENGES_DIR = Path("challenges")
INVENTORY_DOC = Path("docs/challenge-inventory.md")


def generated_ids() -> list[str]:
    """Return the id (parent directory name) of every generated challenge."""
    return sorted(p.parent.name for p in CHALLENGES_DIR.glob("*/challenge.yml"))


def main() -> int:
    if not CHALLENGES_DIR.is_dir():
        print("error: challenges/ does not exist -- run the build_<track>.py scripts first")
        return 2
    ids = generated_ids()
    if not ids:
        print("error: no generated challenges found -- run the build_<track>.py scripts first")
        return 2
    if not INVENTORY_DOC.is_file():
        print(f"error: {INVENTORY_DOC} not found")
        return 2

    doc = INVENTORY_DOC.read_text(encoding="utf-8")

    # NOTE: the check is deliberately id-based only. The inventory doc cites
    # each challenge by its directory id (`bandit-00`) but does not quote the
    # display names, so a name-text check would false-positive on every row.
    missing_from_doc = [i for i in ids if i not in doc]
    if missing_from_doc:
        print("inventory drift detected (regenerate docs/challenge-inventory.md):")
        print(
            "  generated challenges missing from docs/challenge-inventory.md: "
            + ", ".join(missing_from_doc)
        )
        return 1

    print(f"inventory in sync: {len(ids)} generated challenges all documented.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
