#!/usr/bin/env python3
"""Black-box deployment smoke test for the wargame-stages CTFd plugin,
automating cei-labs-engine/docs/staggered-wargame-stage-verification.md's
"Deployment smoke test" checklist (items 1-10) against a local CTFd
instance (see scripts/local-ctfd/).

Run SECOND, after test_staggered_concurrency.py (which owns Bandit and
leaves it LOCKED). This script owns Krypton and Natas end-to-end:

  1/2. Sync Krypton (8/8) and Natas (16/16) -- start() 409s on a count
       mismatch, so a successful start below is itself proof the count
       matched exactly.
  3.   Confirm Krypton/Natas are hidden from a participant while pending.
  4.   Start Krypton; a second Start call must be a no-op (same
       started_at, no extra audit row).
  5.   Two participant teams solve Krypton challenges at different times
       with different point totals; confirm scoreboard order is score
       desc, then elapsed time, then name. One team's name is a
       spreadsheet-formula string, feeding test_export_reconciliation.py's
       CSV-injection check.
  6.   Start Natas while Krypton is still active (not locked) -- two
       stages simultaneously active, each scoreboard containing only its
       own category's solves.
  7.   Hide then show Krypton's scoreboard; confirm participants get 404
       while hidden, admins still see it, and no score data changes.
  8.   Lock Krypton, then submit a further Krypton solve -- CTFd core
       still accepts it, but the stage's exported score is unaffected.
  9.   Close Natas while active; its close time must equal its score
       cutoff, and its started_at must be independent of Krypton's.
  10.  Restart the CTFd container; confirm all persisted state (stage
       state/timestamps/mappings/scoreboard visibility/audit rows, for
       Bandit too) survives the restart.
"""
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
import ctfd_client as ctfd  # noqa: E402

BASE_URL = "http://localhost:8000"
ADMIN_NAME = "admin"
ADMIN_PASSWORD = "LocalTest-Passw0rd!"
CTFD_CONTAINER = "local-ctfd-ctfd-1"

KRYPTON_SLUG = "krypton"
NATAS_SLUG = "natas"
BANDIT_SLUG = "bandit"

KRYPTON_CH_A = "Krypton 0 -> 1: Base64 Decoding"
KRYPTON_CH_B = "Krypton 1 -> 2: ROT13 Substitution Cipher"

STATE_DIR = os.path.join(os.path.dirname(__file__), "local-ctfd", ".state")
STATE_FILE = os.path.join(STATE_DIR, "smoke.json")

failures = []


def check(label, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}" + (f" -- {detail}" if detail and not condition else ""))
    if not condition:
        failures.append(label)


def new_participant(admin, tag):
    suffix = f"{tag}-{int(time.time()*1000)}"
    user_id = ctfd.create_user(admin, f"user-{suffix}", f"{suffix}@ctf.local", "TeamPass123!")
    # Leading "=" is what triggers safe_csv_cell()'s neutralization -- the
    # rest just needs to be unique per run so re-runs don't collide on
    # CTFd's unique team-name constraint.
    team_name = f"=1+1+{suffix}" if tag == "formula" else f"smoke-team-{suffix}"
    team_id = ctfd.create_team(admin, team_name, "TeamPass123!")
    ctfd.add_team_member(admin, team_id, user_id)
    session = ctfd.CTFdSession(base_url=BASE_URL)
    session.login(f"user-{suffix}", "TeamPass123!")
    return {"user_id": user_id, "team_id": team_id, "team_name": team_name, "session": session}


def visible_categories(session):
    resp = session.get("/api/v1/challenges")
    resp.raise_for_status()
    return {row["category"] for row in resp.json()["data"]}


def main() -> int:
    admin = ctfd.bootstrap_admin(BASE_URL, ADMIN_NAME, ADMIN_PASSWORD)
    print("Logged in as admin.")

    bystander = new_participant(admin, "bystander")

    # -- items 1/2/3: sync + pending-hidden ------------------------------------
    for slug in (KRYPTON_SLUG, NATAS_SLUG):
        resp = ctfd.stage_sync(admin, slug)
        check(f"{slug} sync succeeds", resp.status_code == 200, f"HTTP {resp.status_code}")

    for slug in (KRYPTON_SLUG, NATAS_SLUG):
        pre = ctfd.stage_export(admin, slug, "json").json()
        check(f"{slug} is still pending before start", pre["stage"]["state"] == "pending", pre["stage"]["state"])
        resp = ctfd.scoreboard_page(bystander["session"], slug)
        check(f"{slug} scoreboard is hidden (404) from a participant while pending", resp.status_code == 404, str(resp.status_code))

    # -- item 4: start Krypton + idempotent re-start ---------------------------
    ctfd.stage_start(admin, KRYPTON_SLUG)
    export_a = ctfd.stage_export(admin, KRYPTON_SLUG, "json").json()
    started_at_1 = export_a["stage"]["started_at"]
    check("Krypton has a started_at after start", started_at_1 is not None)

    ctfd.stage_start(admin, KRYPTON_SLUG)  # deliberate repeat
    export_b = ctfd.stage_export(admin, KRYPTON_SLUG, "json").json()
    check("repeat start does not change Krypton's started_at", export_b["stage"]["started_at"] == started_at_1)

    check("only Bandit + Krypton categories are visible to participants (Natas still pending)",
          visible_categories(bystander["session"]) == {"Linux Basics", "Cryptography"},
          str(visible_categories(bystander["session"])))

    # -- item 5: two participants solve at different times, ordering ----------
    fast_team = new_participant(admin, "fast")
    slow_team = new_participant(admin, "formula")  # formula-injection team name

    chal_a = ctfd.get_challenge_id(admin, KRYPTON_CH_A)
    chal_b = ctfd.get_challenge_id(admin, KRYPTON_CH_B)
    flag_a = f"smoke-flag-a-{int(time.time())}"
    flag_b = f"smoke-flag-b-{int(time.time())}"
    ctfd.add_static_flag(admin, chal_a, flag_a)
    ctfd.add_static_flag(admin, chal_b, flag_b)

    # fast_team solves both quickly (higher score); slow_team solves one,
    # deliberately delayed so its elapsed-time tiebreak loses on ties and its
    # lower score loses outright.
    r1 = ctfd.submit_flag(fast_team["session"], chal_a, flag_a)
    r2 = ctfd.submit_flag(fast_team["session"], chal_b, flag_b)
    check("fast_team's two solves were both accepted", all(r.get("data", {}).get("status") == "correct" for r in (r1, r2)), json.dumps([r1, r2]))
    time.sleep(2)
    r3 = ctfd.submit_flag(slow_team["session"], chal_a, flag_a)
    check("slow_team's solve was accepted", r3.get("data", {}).get("status") == "correct", json.dumps(r3))

    export_c = ctfd.stage_export(admin, KRYPTON_SLUG, "json").json()
    standings = export_c["standings"]
    fast_row = next(row for row in standings if row["name"] == fast_team["team_name"])
    slow_row = next(row for row in standings if row["name"] == slow_team["team_name"])
    check("fast_team outscores slow_team (2 challenges vs 1)", fast_row["score"] > slow_row["score"], f"{fast_row['score']} vs {slow_row['score']}")
    check("scoreboard is ordered score-descending", standings.index(fast_row) < standings.index(slow_row))
    check("place numbers reflect score order", fast_row["place"] < slow_row["place"])

    # -- CSV export: formula-injection neutralization --------------------------
    csv_resp = ctfd.stage_export(admin, KRYPTON_SLUG, "csv")
    check("Krypton CSV export succeeds", csv_resp.status_code == 200, str(csv_resp.status_code))
    csv_text = csv_resp.text
    check(
        "the formula-injection team name is neutralized in the CSV export (leading ' prefix)",
        f"'{slow_team['team_name']}" in csv_text,
        csv_text[:400],
    )

    # -- item 6: start Natas while Krypton is still active ----------------------
    krypton_state = ctfd.stage_export(admin, KRYPTON_SLUG, "json").json()["stage"]["state"]
    check("Krypton is still active (not locked) before Natas starts", krypton_state == "active", krypton_state)

    ctfd.stage_start(admin, NATAS_SLUG)
    natas_export_1 = ctfd.stage_export(admin, NATAS_SLUG, "json").json()
    check("Natas is now active", natas_export_1["stage"]["state"] == "active")
    check("both Krypton and Natas categories are now visible", visible_categories(bystander["session"]) == {"Linux Basics", "Cryptography", "Web Security"})
    check("Krypton's own standings contain no Natas solves (per-stage isolation)",
          {row["name"] for row in export_c["standings"]}.issubset({fast_team["team_name"], slow_team["team_name"]}))

    # -- item 7: hide/show Krypton's scoreboard, no score mutation -------------
    before_hide = ctfd.stage_export(admin, KRYPTON_SLUG, "json").json()
    ctfd.stage_visibility(admin, KRYPTON_SLUG, False)
    resp = ctfd.scoreboard_page(bystander["session"], KRYPTON_SLUG)
    check("hidden Krypton scoreboard 404s for a participant", resp.status_code == 404, str(resp.status_code))
    resp_admin = ctfd.scoreboard_page(admin, KRYPTON_SLUG)
    check("hidden Krypton scoreboard is still visible to an admin", resp_admin.status_code == 200, str(resp_admin.status_code))
    ctfd.stage_visibility(admin, KRYPTON_SLUG, True)
    resp2 = ctfd.scoreboard_page(bystander["session"], KRYPTON_SLUG)
    check("Krypton scoreboard is visible again after show", resp2.status_code == 200, str(resp2.status_code))
    after_show = ctfd.stage_export(admin, KRYPTON_SLUG, "json").json()
    check("hide/show cycle did not change Krypton's standings", before_hide["standings"] == after_show["standings"])

    # -- item 8: lock Krypton, post-cutoff solve excluded -----------------------
    ctfd.stage_lock(admin, KRYPTON_SLUG)
    locked_export = ctfd.stage_export(admin, KRYPTON_SLUG, "json").json()
    check("Krypton has a score_cutoff after lock", locked_export["stage"]["score_cutoff"] is not None)
    pre_lock_count = len(locked_export["standings"])

    late_team = new_participant(admin, "krypton-late")
    late_result = ctfd.submit_flag(late_team["session"], chal_a, flag_a)
    check("CTFd core still accepts a correct flag after Krypton locks", late_result.get("data", {}).get("status") == "correct", json.dumps(late_result))
    post_lock_export = ctfd.stage_export(admin, KRYPTON_SLUG, "json").json()
    check("post-lock solve does not appear in Krypton's standings", late_team["team_name"] not in {row["name"] for row in post_lock_export["standings"]})
    check("post-lock solve count is unchanged", len(post_lock_export["standings"]) == pre_lock_count)

    # -- item 9: close Natas, cutoff == close time, independent clock ----------
    before_close = time.strftime("%Y-%m-%dT%H:%M:%S")
    ctfd.stage_close(admin, NATAS_SLUG)
    natas_export_2 = ctfd.stage_export(admin, NATAS_SLUG, "json").json()
    check("Natas is closed", natas_export_2["stage"]["state"] == "closed")
    check("Natas's score_cutoff was set at close time (never separately locked, so cutoff == close)",
          natas_export_2["stage"]["score_cutoff"] is not None and natas_export_2["stage"]["score_cutoff"] >= before_close,
          f"cutoff={natas_export_2['stage']['score_cutoff']} before_close={before_close}")
    check("Natas started_at differs from Krypton's (independent per-stage clocks)",
          natas_export_2["stage"]["started_at"] != export_a["stage"]["started_at"])

    # -- item 10: restart CTFd, confirm persistence ----------------------------
    pre_restart = {
        slug: ctfd.stage_export(admin, slug, "json").json()["stage"]
        for slug in (BANDIT_SLUG, KRYPTON_SLUG, NATAS_SLUG)
    }
    print("Restarting the CTFd container...")
    subprocess.run(["docker", "restart", CTFD_CONTAINER], check=True, capture_output=True)

    def ctfd_back_up():
        try:
            import requests
            return requests.get(f"{BASE_URL}/setup", timeout=3).status_code in (200, 302)
        except Exception:
            return False

    up = ctfd.wait_until(ctfd_back_up, timeout=60, interval=2)
    check("CTFd came back up after restart", up)

    admin2 = ctfd.bootstrap_admin(BASE_URL, ADMIN_NAME, ADMIN_PASSWORD)
    for slug in (BANDIT_SLUG, KRYPTON_SLUG, NATAS_SLUG):
        post = ctfd.stage_export(admin2, slug, "json").json()["stage"]
        before = pre_restart[slug]
        check(f"{slug} state/timestamps persisted across a CTFd restart",
              (post["state"], post["started_at"], post["score_cutoff"]) == (before["state"], before["started_at"], before["score_cutoff"]),
              f"before={before} after={post}")

    os.makedirs(STATE_DIR, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "formula_team_name": slow_team["team_name"],
            "krypton_scoring_team_names": [fast_team["team_name"], slow_team["team_name"]],
        }, f, indent=2)
    print(f"Wrote state to {STATE_FILE}")

    print()
    if failures:
        print(f"{len(failures)} check(s) FAILED:")
        for label in failures:
            print(f"  - {label}")
        return 1
    print("All smoke checks passed. Krypton LOCKED, Natas CLOSED for downstream scripts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
