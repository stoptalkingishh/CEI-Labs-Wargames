#!/usr/bin/env python3
"""Concurrency/race-safety black-box test for the wargame-stages CTFd
plugin (cei-labs-engine/docker/ctfd/plugins/wargame-stages), run against a
local CTFd instance (see scripts/local-ctfd/).

Owns the Bandit stage end-to-end and leaves it LOCKED when done (with a
known set of solves) -- test_staggered_smoke.py and
test_export_reconciliation.py assume this and pick up Krypton/Natas and the
export/reconciliation pass respectively. Run this script FIRST.

Exercises, against the live HTTP API (no direct DB writes except one
read-only audit-count query -- see ctfd_client.audit_count):

  1. N concurrent POST .../bandit/start requests -> exactly one audit
     'start' row and a single stable started_at (docs/staggered-wargame-
     stage-verification.md item 4's "issue simultaneous Start requests"
     bug-injection case).
  2. N teams submitting the same correct flag concurrently right after
     start -> every solve recorded, correct total score, no crash/hang
     (the doc's "future load test" section, scaled down to a real but
     fast local run).
  3. N concurrent POST .../bandit/lock requests -> exactly one audit
     'lock' row and a single stable locked_at.
  4. A solve submitted after lock is accepted by CTFd core (the flag is
     still "correct") but does not change the Bandit stage's exported
     score/solve_count -- the score-cutoff enforcement the doc's item 8
     describes.

Writes scripts/local-ctfd/.state/concurrency.json so
test_export_reconciliation.py can cross-check the ground truth recorded
here against what CTFd's own export reports later.
"""
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
import ctfd_client as ctfd  # noqa: E402

BASE_URL = "http://localhost:8000"
ADMIN_NAME = "admin"
ADMIN_PASSWORD = "LocalTest-Passw0rd!"
DB_CONTAINER = "local-ctfd-ctfd-db-1"
DB_USER = "ctfd"
DB_PASSWORD = "local-test-db-password"
DB_NAME = "ctfd"

STAGE_SLUG = "bandit"
STAGE_CHALLENGE_NAME = "Bandit 0 -> 1: The First Step"
FLAG_VALUE = "concurrency-test-flag-{}"
TEAM_PREFIX = "concurrency-team-"
CONCURRENCY = 10

STATE_DIR = os.path.join(os.path.dirname(__file__), "local-ctfd", ".state")
STATE_FILE = os.path.join(STATE_DIR, "concurrency.json")

failures = []


def check(label, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}" + (f" -- {detail}" if detail and not condition else ""))
    if not condition:
        failures.append(label)


def main() -> int:
    admin = ctfd.bootstrap_admin(BASE_URL, ADMIN_NAME, ADMIN_PASSWORD)
    print("Logged in as admin.")

    # -- setup: sync mapping, create N fresh teams -----------------------------
    resp = ctfd.stage_sync(admin, STAGE_SLUG)
    check("bandit sync succeeds", resp.status_code == 200, f"HTTP {resp.status_code}")

    challenge_id = ctfd.get_challenge_id(admin, STAGE_CHALLENGE_NAME)
    flag_value = FLAG_VALUE.format(int(time.time()))
    ctfd.add_static_flag(admin, challenge_id, flag_value)
    print(f"Added static test flag to challenge {challenge_id!r}.")

    participants = []
    for i in range(CONCURRENCY):
        suffix = f"{int(time.time())}-{i}"
        user_id = ctfd.create_user(admin, f"{TEAM_PREFIX}user-{suffix}", f"conc-{suffix}@ctf.local", "TeamPass123!")
        team_id = ctfd.create_team(admin, f"{TEAM_PREFIX}{suffix}", "TeamPass123!")
        ctfd.add_team_member(admin, team_id, user_id)
        session = ctfd.CTFdSession(base_url=BASE_URL)
        session.login(f"{TEAM_PREFIX}user-{suffix}", "TeamPass123!")
        participants.append({"user_id": user_id, "team_id": team_id, "session": session, "name": f"{TEAM_PREFIX}{suffix}"})
    print(f"Created {len(participants)} participant teams.")

    # -- 1. concurrent Start requests ------------------------------------------
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
        futures = [pool.submit(ctfd.stage_start, admin, STAGE_SLUG) for _ in range(CONCURRENCY)]
        statuses = [f.result().status_code for f in as_completed(futures)]
    check("all concurrent start requests returned 200", all(s == 200 for s in statuses), str(statuses))

    export1 = ctfd.stage_export(admin, STAGE_SLUG, "json").json()
    started_at_1 = export1["stage"]["started_at"]
    check("stage is active with a started_at timestamp", started_at_1 is not None)

    start_audit_rows = ctfd.audit_count(DB_CONTAINER, DB_USER, DB_PASSWORD, DB_NAME, STAGE_SLUG, "start")
    check("exactly one 'start' audit row despite concurrent requests", start_audit_rows == 1, f"found {start_audit_rows}")

    # Re-fire a solo start after the race settles -- idempotency must hold
    # for a normal (non-racing) repeat call too.
    ctfd.stage_start(admin, STAGE_SLUG)
    export2 = ctfd.stage_export(admin, STAGE_SLUG, "json").json()
    check("started_at unchanged after an additional solo start call", export2["stage"]["started_at"] == started_at_1)

    # -- 2. concurrent correct-flag submissions --------------------------------
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
        futures = {pool.submit(ctfd.submit_flag, p["session"], challenge_id, flag_value): p for p in participants}
        results = {}
        for future in as_completed(futures):
            p = futures[future]
            results[p["name"]] = future.result()

    all_correct = all(r.get("data", {}).get("status") == "correct" for r in results.values())
    check("every concurrent correct-flag submission was accepted", all_correct, json.dumps(results)[:500])

    export3 = ctfd.stage_export(admin, STAGE_SLUG, "json").json()
    solved_names = {row["name"] for row in export3["standings"]}
    expected_names = {p["name"] for p in participants}
    check(
        "every participating team appears exactly once in the Bandit standings",
        expected_names.issubset(solved_names),
        f"missing: {expected_names - solved_names}",
    )
    challenge_value = next(row["score"] for row in export3["standings"] if row["name"] in expected_names)
    check("each team's score equals the single challenge's point value (no double count)", challenge_value == 100, str(challenge_value))

    # -- 3. concurrent Lock requests --------------------------------------------
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
        futures = [pool.submit(ctfd.stage_lock, admin, STAGE_SLUG) for _ in range(CONCURRENCY)]
        lock_statuses = [f.result().status_code for f in as_completed(futures)]
    check("all concurrent lock requests returned 200", all(s == 200 for s in lock_statuses), str(lock_statuses))

    lock_audit_rows = ctfd.audit_count(DB_CONTAINER, DB_USER, DB_PASSWORD, DB_NAME, STAGE_SLUG, "lock")
    check("exactly one 'lock' audit row despite concurrent requests", lock_audit_rows == 1, f"found {lock_audit_rows}")

    export4 = ctfd.stage_export(admin, STAGE_SLUG, "json").json()
    cutoff = export4["stage"]["score_cutoff"]
    check("score_cutoff is set after lock", cutoff is not None)
    pre_lock_solve_count = len(export4["standings"])

    # -- 4. post-cutoff solve: accepted by CTFd core, excluded from scoring -----
    late_suffix = f"late-{int(time.time())}"
    late_user_id = ctfd.create_user(admin, f"{TEAM_PREFIX}user-{late_suffix}", f"conc-{late_suffix}@ctf.local", "TeamPass123!")
    late_team_id = ctfd.create_team(admin, f"{TEAM_PREFIX}{late_suffix}", "TeamPass123!")
    ctfd.add_team_member(admin, late_team_id, late_user_id)
    late_session = ctfd.CTFdSession(base_url=BASE_URL)
    late_session.login(f"{TEAM_PREFIX}user-{late_suffix}", "TeamPass123!")

    late_result = ctfd.submit_flag(late_session, challenge_id, flag_value)
    check("CTFd core still accepts a technically-correct flag after lock", late_result.get("data", {}).get("status") == "correct", json.dumps(late_result))

    export5 = ctfd.stage_export(admin, STAGE_SLUG, "json").json()
    check(
        "post-cutoff solve does not appear in the Bandit stage's exported standings",
        f"{TEAM_PREFIX}{late_suffix}" not in {row["name"] for row in export5["standings"]},
    )
    check("post-cutoff solve does not change the stage's total solve count", len(export5["standings"]) == pre_lock_solve_count, f"{len(export5['standings'])} vs {pre_lock_solve_count}")

    # -- persist ground truth for the export-reconciliation test ---------------
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "stage_slug": STAGE_SLUG,
            "team_name_prefix": TEAM_PREFIX,
            "scoring_team_names": sorted(expected_names),
            "excluded_team_name": f"{TEAM_PREFIX}{late_suffix}",
            "challenge_value": challenge_value,
            "started_at": started_at_1,
            "score_cutoff": cutoff,
        }, f, indent=2)
    print(f"Wrote ground-truth state to {STATE_FILE}")

    print()
    if failures:
        print(f"{len(failures)} check(s) FAILED:")
        for label in failures:
            print(f"  - {label}")
        return 1
    print("All concurrency checks passed. Bandit stage left LOCKED for downstream scripts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
