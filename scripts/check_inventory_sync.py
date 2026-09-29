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
     challenges show ``3 (<t1>%/<t2>%/<t3>%)``, everything else shows ``0``;
  d) each inventory row's "Flag source" cell must match the generated
     ``flags:`` block: a structured flag's ``type`` is quoted in the cell, a
     static flag is either quoted verbatim or labelled ``static``;
  e) each inventory row's "Instance type" cell must equal the generated
     ``instance_type:`` (challenges that generate none are documented
     ``none``);
  f) each inventory row's "Reset/teardown" cell must match the generated
     ``shutdown_on_solve:`` -- ``**auto on solve**`` where it is true,
     ``idle-timeout`` where it is false, ``n/a`` where the challenge
     generates no instance at all.

(c) is the only column not sourced from ``challenge.yml``; (d)-(f) exist
because a stale ``**auto on solve**`` on natas-14 (the generated
``shutdown_on_solve: false``) shipped in this table unnoticed while only
(b) and (c) were enforced.

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
INSTANCE_TYPE_LINE = re.compile(r"^instance_type:\s*(\S+)\s*$", re.M)
SHUTDOWN_LINE = re.compile(r"^shutdown_on_solve:\s*(true|false)\s*$", re.M)
# The generators write `flags:` as a top-level key followed by an indented
# block: either a mapping entry (`- type: per_team_dynamic`) or a bare static
# string (`- "WELCOME TO NATAS"`). The block ends at the next top-level key.
FLAGS_BLOCK = re.compile(r"^flags:\s*\n((?:[ \t]+.*\n)*)", re.M)
FLAG_TYPE_LINE = re.compile(r"^\s*-\s*type:\s*(\S+)\s*$", re.M)
FLAG_STATIC_LINE = re.compile(r'^\s*-\s*"(.*)"\s*$', re.M)
TABLE_ROW = re.compile(r"^\s*\|(.+)\|\s*$")
CELL_ID = re.compile(r"^`([^`]+)`$")
# A doc cell's primary value: the first backtick-quoted token, else the leading
# word, with any trailing parenthetical note dropped. Keeps prose appended to a
# cell ("| `per_team_dynamic` (fixed no longer -- see cei-labs-event#17) |",
# "| none (player's laptop) |", "| `WELCOME TO NATAS` (static -- see finding
# above) |") from breaking a comparison against the generated value.
CELL_VALUE = re.compile(r"^(?:`([^`]+)`|(\S+))")


def cell_value(cell: str) -> str:
    """The cell's primary value, ignoring backticks and any trailing
    parenthetical explanation of it."""
    head = re.split(r"[,(]", cell.strip(), 1)[0].strip()
    m = CELL_VALUE.match(head)
    if m is None:
        return ""
    return (m.group(1) or m.group(2)).strip()


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


def parse_challenge(path: Path) -> dict:
    """The generated facts the inventory's other columns are checked against.

    Parsed by regex rather than a YAML import to keep this script dependency-
    free, exactly as the value: check above already does; the challenge.yml
    files it reads are all machine-generated, so their layout is fixed.
    Raises ValueError when a required field is absent."""
    text = path.read_text(encoding="utf-8")
    m = VALUE_LINE.search(text)
    if m is None:
        raise ValueError(f"{path}: no 'value:' line found")
    block = FLAGS_BLOCK.search(text)
    if block is None:
        raise ValueError(f"{path}: no 'flags:' block found")
    flags = block.group(1)
    flag_type = FLAG_TYPE_LINE.search(flags)
    flag_static = None if flag_type else FLAG_STATIC_LINE.search(flags)
    if flag_type is None and flag_static is None:
        raise ValueError(f"{path}: 'flags:' block has neither a type nor a static string")
    instance_type = INSTANCE_TYPE_LINE.search(text)
    shutdown = SHUTDOWN_LINE.search(text)
    return {
        "value": int(m.group(1)),
        # A structured flag documents its source as the flag type; a static
        # flag is documented either as the flag string itself or as "static".
        "flag_source": flag_type.group(1) if flag_type else flag_static.group(1),
        "flag_is_static": flag_type is None,
        # A challenge with no instance_type is one with no per-team instance
        # at all (the AI Copilot Setup track), so it also has no teardown.
        "instance_type": instance_type.group(1) if instance_type else "none",
        "shutdown_on_solve": None if shutdown is None else shutdown.group(1) == "true",
    }


def generated_challenges() -> dict[str, dict]:
    """Map every generated challenge id to its challenge.yml facts."""
    return {
        p.parent.name: parse_challenge(p)
        for p in sorted(CHALLENGES_DIR.glob("*/challenge.yml"))
    }


def expected_instance_cell(challenge: dict) -> str:
    """The Instance type cell, the generated instance_type verbatim (or "none"
    for a challenge that ships no instance)."""
    return challenge["instance_type"]


def expected_teardown_cell(challenge: dict) -> str:
    """The Reset/teardown cell. The doc's own convention (see the bandit
    section's "Dependencies" note) is that a challenge with
    ``shutdown_on_solve: false`` is reset by the orchestrator's idle-timeout
    teardown, the terminal level's teardown is triggered by the solve, and a
    challenge with no instance has no teardown at all."""
    shutdown = challenge["shutdown_on_solve"]
    if shutdown is None:
        return "n/a"
    return "auto on solve" if shutdown else "idle-timeout"


def normalize_teardown_cell(cell: str) -> str:
    """Strip the cell's markdown emphasis/backticks so "**auto on solve**"
    compares equal to the plain expected value."""
    return re.sub(r"[`*]", "", cell).strip().lower()


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

    # (b-f) Per-row Points, Flag source, Instance type, Reset/teardown and
    # Hints (cost) checks on inventory rows (7-cell rows; the 4-cell
    # static-flag finding rows carry none of these).
    for cid, challenge in sorted(generated.items()):
        cells = rows.get(cid)
        if cells is None or len(cells) < 6:
            continue
        try:
            doc_points = int(cells[1])
        except ValueError:
            problems.append(f"{cid}: Points cell {cells[1]!r} is not an integer")
            continue
        if doc_points != challenge["value"]:
            problems.append(
                f"{cid}: Points drift -- doc says {doc_points}, "
                f"challenge.yml value is {challenge['value']}"
            )
        doc_flag = cell_value(cells[2])
        if challenge["flag_is_static"]:
            # The doc quotes the flag string itself for the start-here
            # tutorials and just says "static" for the AI Copilot Setup track;
            # a static flag containing a comma or parenthesis is matched on the
            # quoted cell, since cell_value() stops at the first one.
            ok = doc_flag in {challenge["flag_source"], "static"} or (
                f"`{challenge['flag_source']}`" in cells[2]
            )
            expected_flags = sorted({challenge["flag_source"], "static"})
        else:
            ok = doc_flag == challenge["flag_source"]
            expected_flags = [challenge["flag_source"]]
        if not ok:
            problems.append(
                f"{cid}: Flag source drift -- doc says {cells[2]!r}, "
                f"challenge.yml flags are {expected_flags}"
            )
        expected_instance = expected_instance_cell(challenge)
        doc_instance = cell_value(cells[3])
        if doc_instance != expected_instance:
            problems.append(
                f"{cid}: Instance type drift -- doc says {doc_instance!r}, "
                f"challenge.yml instance_type is {expected_instance!r}"
            )
        expected_teardown = expected_teardown_cell(challenge)
        doc_teardown = normalize_teardown_cell(cells[4])
        if doc_teardown != expected_teardown:
            problems.append(
                f"{cid}: Reset/teardown drift -- doc says {doc_teardown!r}, "
                f"challenge.yml shutdown_on_solve implies {expected_teardown!r}"
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
