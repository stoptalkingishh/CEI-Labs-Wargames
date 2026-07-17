#!/usr/bin/env python3
"""Export-reconciliation black-box test for the wargame-stages CTFd plugin,
run against a local CTFd instance (see scripts/local-ctfd/).

Run THIRD, after test_staggered_concurrency.py (Bandit, locked) and
test_staggered_smoke.py (Krypton, locked; Natas, closed). Doesn't change
stage state itself -- exports are read-only GETs, safe to call anytime.

Reconciles CTFd's live state against three independent sources of truth:

  1. This repo's own manifest (game-stages.yml's expected_challenge_count)
     against what's actually live in CTFd per category -- confirms the
     deployed content matches what Wargames declared, the same guarantee
     scripts/validate_game_stages.py checks statically but now verified
     against the running instance.
  2. The JSON and CSV exports of each stage against each other -- same
     place/score/solve_count/name per account in both formats.
  3. The ground-truth state files the two upstream scripts wrote
     (scripts/local-ctfd/.state/*.json) against the exported standings --
     the actual "reconciliation": did every solve this test run performed
     actually land in the score CTFd now reports, with no extras and no
     omissions?

Also re-verifies the formula-injection team name test_staggered_smoke.py
created is still neutralized in a freshly re-fetched Krypton CSV export
(the smoke test only checked it once, immediately after creation).
"""
import json
import os
import sys

import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
import ctfd_client as ctfd  # noqa: E402

BASE_URL = "http://localhost:8000"
ADMIN_NAME = "admin"
ADMIN_PASSWORD = "LocalTest-Passw0rd!"

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME_STAGES_YML = os.path.join(REPO_ROOT, "game-stages.yml")
STATE_DIR = os.path.join(os.path.dirname(__file__), "local-ctfd", ".state")

failures = []


def check(label, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}" + (f" -- {detail}" if detail and not condition else ""))
    if not condition:
        failures.append(label)


def load_state(name):
    path = os.path.join(STATE_DIR, f"{name}.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def csv_rows(csv_text):
    import csv
    import io
    return list(csv.DictReader(io.StringIO(csv_text)))


def main() -> int:
    admin = ctfd.bootstrap_admin(BASE_URL, ADMIN_NAME, ADMIN_PASSWORD)
    print("Logged in as admin.")

    # -- 1. manifest reconciliation: game-stages.yml vs. live CTFd content -----
    with open(GAME_STAGES_YML, encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    admin_challenges = admin.api("GET", "/api/v1/challenges?view=admin&per_page=100").json()["data"]
    live_counts_by_category = {}
    for row in admin_challenges:
        live_counts_by_category[row["category"]] = live_counts_by_category.get(row["category"], 0) + 1

    for stage in manifest["stages"]:
        expected = stage["expected_challenge_count"]
        live = live_counts_by_category.get(stage["category"], 0)
        check(
            f"{stage['slug']}: live CTFd challenge count matches game-stages.yml ({expected})",
            live == expected,
            f"live={live} expected={expected}",
        )

    check("total live challenge count is 59 (35 + 8 + 16)", len(admin_challenges) == 59, str(len(admin_challenges)))

    # -- 2. JSON vs CSV export agreement, per stage -----------------------------
    for stage in manifest["stages"]:
        slug = stage["slug"]
        json_export = ctfd.stage_export(admin, slug, "json").json()
        csv_export = ctfd.stage_export(admin, slug, "csv")
        check(f"{slug}: CSV export succeeds", csv_export.status_code == 200, str(csv_export.status_code))
        rows = csv_rows(csv_export.text)

        # CSV rows differ from JSON in two intentional ways (routes.py's
        # export()): a formula-prefixed name gets a neutralizing leading "'"
        # (safe_csv_cell) only in the CSV path, and an empty stage emits one
        # metadata-only placeholder row (`for row in rows or [{}]`) with a
        # blank name instead of zero rows. Normalize both before comparing.
        json_by_name = {row["name"]: row for row in json_export["standings"]}
        csv_by_name = {
            (name[1:] if name.startswith("'") else name): row
            for row in rows
            if (name := row["name"])
        }
        check(f"{slug}: same set of scoring accounts in JSON and CSV exports", set(json_by_name) == set(csv_by_name),
              f"json-only={set(json_by_name) - set(csv_by_name)} csv-only={set(csv_by_name) - set(json_by_name)}")

        mismatches = []
        for name, jrow in json_by_name.items():
            crow = csv_by_name.get(name)
            if crow is None:
                continue
            if str(jrow["score"]) != crow["score"] or str(jrow["place"]) != crow["place"] or str(jrow["solve_count"]) != crow["solve_count"]:
                mismatches.append(name)
        check(f"{slug}: score/place/solve_count agree between JSON and CSV for every account", not mismatches, str(mismatches))

    # -- 3. ground-truth reconciliation against upstream scripts' state --------
    concurrency_state = load_state("concurrency")
    if concurrency_state is None:
        check("concurrency.json state file exists (run test_staggered_concurrency.py first)", False)
    else:
        bandit_export = ctfd.stage_export(admin, concurrency_state["stage_slug"], "json").json()
        standings_by_name = {row["name"]: row for row in bandit_export["standings"]}

        missing = [name for name in concurrency_state["scoring_team_names"] if name not in standings_by_name]
        check("every team test_staggered_concurrency.py solved as appears in Bandit's exported standings", not missing, str(missing))

        wrong_score = [
            name for name in concurrency_state["scoring_team_names"]
            if name in standings_by_name and standings_by_name[name]["score"] != concurrency_state["challenge_value"]
        ]
        check("each of those teams' exported score matches the challenge's point value", not wrong_score, str(wrong_score))

        check(
            "the team that solved after Bandit's lock is absent from the exported standings",
            concurrency_state["excluded_team_name"] not in standings_by_name,
            concurrency_state["excluded_team_name"],
        )

        check(
            "Bandit's total exported solve count matches exactly the scoring teams recorded (no extras, no omissions)",
            len(bandit_export["standings"]) == len(concurrency_state["scoring_team_names"]),
            f"exported={len(bandit_export['standings'])} expected={len(concurrency_state['scoring_team_names'])}",
        )

    # -- CSV formula-injection: re-verify with a fresh export -------------------
    smoke_state = load_state("smoke")
    if smoke_state is None:
        check("smoke.json state file exists (run test_staggered_smoke.py first)", False)
    else:
        formula_team_name = smoke_state["formula_team_name"]
        krypton_csv = ctfd.stage_export(admin, "krypton", "csv")
        check(
            "formula-injection team name is still neutralized in a freshly re-fetched Krypton CSV export",
            f"'{formula_team_name}" in krypton_csv.text,
            krypton_csv.text[:400],
        )

    print()
    if failures:
        print(f"{len(failures)} check(s) FAILED:")
        for label in failures:
            print(f"  - {label}")
        return 1
    print("All export-reconciliation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
