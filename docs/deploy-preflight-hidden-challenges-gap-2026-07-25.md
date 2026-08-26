# deploy.sh's install-vs-sync preflight breaks once wargame-stages auto-hide is live (2026-07-25)

Discovered live on `192.168.1.173` immediately after redeploying the
merged wargame-stages auto-hide fix (`cei-labs-engine#31` /
`CEI-Labs-Wargames#20`, both now on `main`). Notes only, no code
changed.

## What happened

After rebuilding and redeploying the fixed `ctfd` image and re-running
`CEI-Labs-Wargames/deploy.sh` to push content, the very first challenge
in the loop failed:

```
Syncing challenge from: challenges/bandit-00
Challenge not found on CTFd. Installing challenge as new...
Installing 'Bandit 0 -> 1: The First Step' ...
Found already existing challenge with the same name (Bandit 0 -> 1: The First Step).
Perhaps you meant sync instead of install?
Install failed for:
 - Bandit 0 -> 1: The First Step
```

This looked alarming (possible data loss) but is not: querying CTFd's
own database directly confirmed all 59 challenges are present and
intact --

```
mysql> SELECT state, COUNT(*) FROM ctfd.challenges GROUP BY state;
+--------+----------+
| state  | COUNT(*) |
+--------+----------+
| hidden |       59 |
+--------+----------+
```

Every challenge is `hidden` -- correctly, since none of this box's
wargame stages have been explicitly started by an admin yet, and
`reconcile_all_pending()` (the fix just deployed) now hides every
challenge belonging to a still-pending stage on every app boot. This is
the auto-hide feature working exactly as designed, not a bug.

## Root cause of the deploy.sh failure

`deploy.sh`'s `challenge_exists()` check (around line ~118) decides
install-vs-sync by querying `${CTFD_URL}/api/v1/challenges?per_page=100`
with an admin token and checking whether the wanted challenge's name
appears in the response:

```python
with open(sys.argv[2], encoding="utf-8") as inventory_file:
    inventory = json.load(inventory_file)
names = {row.get("name") for row in inventory.get("data", [])}
raise SystemExit(0 if wanted in names else 1)
```

Confirmed live that this endpoint, even with a valid admin API token,
returned `{"success": true, "data": []}` while all 59 challenges sat
`hidden` in the database -- i.e. `/api/v1/challenges` only returns
`visible`-state challenges here, regardless of token privilege. Before
the auto-hide fix, every synced challenge stayed `visible` by default,
so this preflight check happened to work. Now that hide-by-default is
the normal state until an admin starts a stage, the preflight considers
every hidden-but-already-installed challenge "not found" and tries to
install it fresh -- which then collides with CTFd's own name-uniqueness
constraint and fails loudly (no duplicate got created; CTFd's own
install path refused it).

## Impact

- No data loss occurred in the incident that surfaced this -- confirmed
  directly against the database.
- CTFd's own install-refusal is a safety net here, not the underlying
  fix -- it prevented a duplicate this time, but the deploy run still
  exits with a failure on the very first challenge and (depending on
  `set -e` behavior) likely never reaches the rest of the loop, meaning
  a legitimate content update (e.g. a real description or points change
  to an already-installed-but-hidden challenge) would silently not get
  synced during the window between "stages exist but none has started"
  and "an admin starts the first stage."
- This will reproduce on every venue box between initial content load
  and the first stage start, and again anytime `deploy.sh` is re-run
  while any stage is still pending (e.g. testing/rehearsal periods
  before an event, or setting up event N+1 far enough ahead that
  nothing's been started yet).

## What closing this needs

- `challenge_exists()`'s preflight query needs to see hidden challenges
  too when running with an admin token -- either a different, actually
  admin-scoped listing endpoint (if CTFd exposes one under
  `/api/v1/challenges` with a query param, or a separate admin route),
  or filtering by something other than the public visible-only listing.
  Not investigated in this pass which option CTFd 3.8.2 actually
  supports.
- Until fixed, anyone re-running `deploy.sh` against a box where stages
  are still pending should expect the first not-yet-`visible` challenge
  to fail this way, and should not assume the whole sync completed
  successfully after seeing that error -- check exit status / how many
  challenges were actually reached before treating a deploy.sh run as
  successful in this state.
- This is `CEI-Labs-Wargames/deploy.sh`'s `challenge_exists()` function.
