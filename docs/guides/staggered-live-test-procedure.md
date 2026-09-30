# Staggered Live-CTFd Test Procedure

`scripts/test_staggered_concurrency.py`, `scripts/test_staggered_smoke.py`,
and `scripts/test_export_reconciliation.py` are black-box tests of the Engine's
`wargame-stages` CTFd plugin. They drive a **live CTFd instance over HTTP** and
they change it: they create users and teams, add static flags to real
challenges, and start, lock, and close real stages.

**They are not run by CI, by design.** All three are `main()`-driven scripts
with no `unittest.TestCase`, so `python -m unittest discover -s scripts -t
scripts` imports them and collects zero tests from them. What CI *does* enforce
is `scripts/check_live_ctfd_scripts.py`, a static guard over the same three
files: no challenge count may be hardcoded, no remote host may be baked in, and
each script must compile, import, and keep a reachable `main()`. This page is
the manual procedure for the part CI cannot do.

## What you need

- Docker with `docker compose` v2, and permission to run `docker exec`.
- A sibling checkout of `cei-labs-engine`. The CTFd image bakes in the
  `wargame-stages` and `instance-launcher` plugins from there, and there is no
  CTFd image in this repository. The default path is `../../../cei-labs-engine`
  relative to `scripts/local-ctfd/`; override it with `CEI_LABS_ENGINE_PATH`.
- Python 3.12 (the version CI pins). Install the dependencies with
  `pip install -r requirements.txt` — that is the same file the Validate
  workflow installs, so the two stay in sync. (`requirements.txt` is resolved
  relative to the repository root, not this directory.)
- `ctfcli` if you use `deploy.sh` to load challenges:
  `pip install -r requirements-deploy.txt`. It is deliberately kept out of
  `requirements.txt` because CI never contacts a CTFd instance.

Never point this at production, or at any instance holding real participants.
The scripts add flags to real challenges and start stages on schedule.

## 1. Bring the instance up

```bash
cd scripts/local-ctfd
CEI_LABS_ENGINE_PATH=/path/to/cei-labs-engine docker compose up -d --build
```

CTFd is then on <http://localhost:8000> with no TLS, no proxy, and no
orchestrator. Run compose **from this directory**: the scripts address the
containers by the compose-derived names `local-ctfd-ctfd-1` and
`local-ctfd-ctfd-db-1`, so the project name has to stay `local-ctfd`.

Tear down with `docker compose down -v` when you are finished. The `-v` also
drops the database volume, which is what makes the next run a clean slate.

## 2. Bootstrap the admin account (once per volume)

```bash
python scripts/local-ctfd/setup_local_ctfd.py
```

This runs the `/setup` wizard in **teams** mode, logs in, mints an API token,
and prints `CTFD_URL=` and `CTFD_TOKEN=` lines meant to be `eval`ed. The three
test scripts do not use the token: they log in over the session API with
`admin` / `LocalTest-Passw0rd!`, the same credentials the wizard sets. If you
change either, the scripts no longer match and every check fails at login.

The token is for step 3.

## 3. Load the challenges

The scripts reconcile CTFd's live contents against `game-stages.yml`, so the
instance needs the generated challenges before they are useful. `deploy.sh`
generates and uploads them in one step:

```bash
eval "$(python scripts/local-ctfd/setup_local_ctfd.py 2>/dev/null | grep '^CTFD_')"
CTFD_SYNC_SECRET=local-test-sync-secret ./deploy.sh
```

`CTFD_SYNC_SECRET` must match `PLUGIN_SHARED_SECRET` in
`scripts/local-ctfd/docker-compose.yml` (`local-test-sync-secret`), or the
instance-launcher mapping sync is rejected. `deploy.sh` also refuses to run
against 65 challenges -- a count that is itself stale; see the open item at the
bottom of this page.

`deploy.sh` additionally offers to push the hint-wallet bundles and hard-fails
if the generated manifests contain entries while `HINT_WALLET_SYNC_SECRET` is
unset. The local stack has no hint-wallet plugin, so the supported options are
either to drop the hint manifests for the run, or to generate and install the
challenges without `deploy.sh`:

```bash
python scripts/build_bandit.py
python scripts/build_krypton.py
python scripts/build_natas.py
python scripts/build_agent.py
for dir in challenges/*/; do ctf challenge install "${dir%/}"; done
```

Either way, verify the counts before continuing -- all three scripts assert
them:

```bash
python scripts/validate_generated.py     # 85 challenge files, 79 staged + 6 unstaged
```

## 4. Run the three scripts, in this order

The order is load-bearing, not stylistic. Each script leaves stage state that
the next one reads.

```bash
python scripts/test_staggered_concurrency.py   # 1st: owns Bandit, leaves it LOCKED
python scripts/test_staggered_smoke.py         # 2nd: owns Krypton + Natas
python scripts/test_export_reconciliation.py   # 3rd: read-only, reconciles the exports
```

- **1st, concurrency** (`scripts/test_staggered_concurrency.py`): 10 teams hit
  Start, Lock, and the same flag simultaneously, proving the plugin records one
  audit row and one timestamp per transition. Leaves Bandit `locked` and writes
  `scripts/local-ctfd/.state/concurrency.json`.
- **2nd, smoke** (`scripts/test_staggered_smoke.py`): the deployment checklist
  end to end for Krypton and Natas, including a `docker restart` of the CTFd
  container. Leaves Krypton `locked`, Natas `closed`, and writes
  `scripts/local-ctfd/.state/smoke.json`.
- **3rd, export reconciliation** (`scripts/test_export_reconciliation.py`):
  checks the live counts against `game-stages.yml`, the JSON and CSV exports
  against each other, and the two state files above against what CTFd actually
  reports. Read-only: safe to re-run at any time, and the one to re-run after
  any content change.

Each script prints a `[PASS]`/`[FAIL]` line per check, lists the failures at
the end, and exits non-zero if any failed. The third script is the one that
reports a missing `concurrency.json` or `smoke.json` -- that means a step was
skipped or the earlier run was against a different instance, not that the
plugin regressed.

The state files are gitignored scratch, regenerated every run. Delete
`scripts/local-ctfd/.state/` when you want a from-scratch run.

## 5. Expected failures in a partial deployment

- **Instance-launcher mappings** are best-effort against this stack: there is
  no orchestrator, so no per-team dynamic flags exist. That is expected, and
  it is why the scripts add their own static flags
  (`scripts/lib/ctfd_client.py`'s `add_static_flag`) rather than depending on
  deployed flags.
- **OSINT tooling is separate.** `scripts/local-ctfd/upload_osint_files.py` and
  `ocr_briefings.py` are local conveniences for the OSINT track and are not
  part of these three scripts or of `game-stages.yml`.
- **Challenge point values** are whatever CTFd defaults to. The concurrency
  script pins `challenge_value == 100`, so a non-default `value:` in
  `challenges/*/challenge.yml` is a real finding, not an environment artifact.
- **Counts are the one thing that is never expected to fail.** They come from
  `game-stages.yml`, and `scripts/check_live_ctfd_scripts.py` refuses to let
  any of the three scripts hardcode one.

## When a check fails for real

1. Re-run the third script first: it is read-only and tells you whether the
   *content* drifted (a count mismatch) or the *state* did (a stage left in the
   wrong state by an interrupted earlier run).
2. If state is the problem, `docker compose down -v` in `scripts/local-ctfd/`
   and start again from step 2. A half-finished run leaves stages in states the
   scripts assume they control.
3. If a count is the problem, that is a real content regression -- do not
   "fix" it by editing the number in the script. `scripts/validate_generated.py`
   and `game-stages.yml` decide what the right number is, and the guard exists
   precisely so nobody hardcodes a third answer.

## Known open items

- `deploy.sh` still hard-fails unless exactly 65 challenges are present. The
  generators now emit 85 (79 staged + 6 AI Copilot Setup), so `deploy.sh` needs
  the same treatment `scripts/test_export_reconciliation.py` just got: derive
  the number instead of pinning it. Until then, expect `deploy.sh` to abort at
  its final count assertion on a current tree.
- No scheduled CI job runs these three scripts. It needs the CTFd harness to be
  buildable in CI, which is a much larger change than the static guard and
  should not block it.

## Related

- [Staggered Game-Stage Manifest](staggered-game-stages.md) -- what
  `game-stages.yml` means and what its static validator checks.
- [Staged Game Operations](staged-game-operations.md) -- the event-day
  controls, once an instance is really deployed.
- [`scripts/check_live_ctfd_scripts.py`](../../scripts/check_live_ctfd_scripts.py)
  -- the static guard CI runs instead of these scripts.
