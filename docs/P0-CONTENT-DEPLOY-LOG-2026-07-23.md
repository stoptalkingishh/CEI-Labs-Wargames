# P0 Content Deploy Log — 2026-07-23

Repo: `/opt/cei-labs/CEI-Labs-Wargames` (main checkout, commit `58ba1fea0166ec0f63a79ca8675fc9dcaf0b193a`)
Goal: regenerate today's content fixes (`man <cmd>` → `<cmd> --help`, explicit account-switching instructions,
per-question themed banners) and push to live CTFd. **Push was NOT executed — stopped per instructions for
human sign-off.**

## 01:05–01:08 EDT — Regeneration

Ran, as root via `sudo` (the `challenges/` tree is root-owned; ownership was restored to
`ismaelrodriguez:ismaelrodriguez` afterward so the files remain readable/diffable by this account):

```
sudo python3 scripts/build_bandit.py     # Successfully generated 35 Bandit challenges
sudo python3 scripts/build_krypton.py    # Successfully generated 8 Krypton challenges
sudo python3 scripts/build_natas.py      # Successfully generated 16 Natas challenges
python3 scripts/validate_game_stages.py  # Game-stage validation passed: Bandit 35, Krypton 8, Natas 16.
sudo python3 scripts/validate_generated.py --output deployment-manifest.json
                                          # validated 59 challenges, 58 mappings, 3 launchers
```

Backup of the pre-regeneration `challenges/` tree and old `deployment-manifest.json` saved to
`/tmp/pre-regen-backup/` on the box (not in the repo, not committed) in case a rollback reference is needed.

**Sanity checks performed:**
- All 59 `challenges/*/challenge.yml` files parse as valid YAML with non-empty `name` and `description`
  fields (scripted check, 0 problems).
- `challenges/bandit-00/challenge.yml` description confirmed updated: hint/description text now says
  `` `ssh` `` command guidance and the new `**Account progression:**` paragraph (previously absent), instead
  of the old `man ssh` phrasing.
- `challenges/bandit-hint-wallet.json`, `krypton-hint-wallet.json`, `natas-hint-wallet.json` regenerated;
  spot-checked — hint tiers now read `` `ssh -h` ``, `` `cat --help` ``, etc. across all three tracks, no
  `man <cmd>` references remain (one false-positive grep hit on the word "**Hu*man* Readable**" — not an
  actual `man` command reference).
- No repo script changes were needed — `build_bandit.py` / `build_krypton.py` / `build_natas.py` ran clean
  on the first try. **No commits were made to `fix/p0-content-deploy`** since nothing in the source needed
  fixing; only generated (gitignored) output changed.
- `targets/*/build/generate_banners.py` (the themed-banner generator) was **not** run — it renders MOTD text
  baked into the Docker target images at image-build time, not something `ctfcli`/`deploy.sh` uploads to
  CTFd. Out of scope for this content-sync task; flagging separately if the target images also need a
  rebuild/push, which is a Docker/Swarm concern explicitly out of scope per instructions.

## 01:10–01:20 EDT — Dry-run / diff against live CTFd

- Installed `ctfcli` via `pip install --user ctfcli` (was not present). No `--dry-run`/plan-only flag exists
  on `ctf challenge sync` or `ctf challenge install` (checked `--help` on both).
- Sourced `CTFD_URL` and the CTFd `API token` from `~/cei-labs-credentials.md` (values used locally on the
  box only; not written to this log, git, or any output).
- Fetched the live challenge list (`GET /api/v1/challenges`) and then full detail (`GET
  /api/v1/challenges/<id>`) for all 59 live challenges, and diffed programmatically against the regenerated
  local `challenge.yml` files.

### Diff summary (what a push would change)

- **Challenges added:** 0 — all 59 local challenge names match 59 live challenge names exactly.
- **Challenges removed:** 0.
- **`value` (points) changes:** 0.
- **`category` changes:** 0.
- **`state` (visible/hidden) changes:** 0.
- **`description` text changes: 35 of 59 challenges** — these are exactly the expected content fixes:
  `man <cmd>` phrasing replaced with `<cmd> --help`, and new `**Account progression:**` paragraphs added
  giving explicit next-account SSH instructions. Verified in detail on `Bandit 0 -> 1: The First Step`
  (live description ends after the "Helpful reading" link; local description adds the full
  `**Account progression:** You are working as \`bandit0\`. After recovering and submitting this password,
  exit and reconnect ... as \`bandit1\` ...` paragraph).
- **Hint-wallet manifests** (`challenges/*-hint-wallet.json`): all 59 challenges' worth of hint content
  regenerated with `--help`-based wording. These are **not** pushed by `ctf challenge sync` — they go via
  `deploy.sh`'s separate `sync_hint_wallet_bundle` step, gated on `HINT_WALLET_SYNC_SECRET`.

### IMPORTANT — a side effect that needs sign-off before pushing

`ctf challenge sync` (confirmed by reading ctfcli's `Challenge.sync()` source,
`~/.local/lib/python3.14/site-packages/ctfcli/core/challenge.py:886`) **unconditionally deletes each
challenge's existing hints and only recreates them if the local `challenge.yml` declares a `hints:` key**.
None of the generated `challenge.yml` files declare `hints:` (hints live only in the separate hint-wallet
JSON manifests, per repo commit `742208a "Add hint-wallet economy, signed Engine sync, and challenge banner
generation"` — a deliberate migration away from native CTFd hints).

Live CTFd currently has **native hints populated on 56 of the 59 challenges** (3-tier, e.g. tier 1 cost 5,
tier 2 cost 50, tier 3 cost 75 on `Bandit 0 -> 1`) — leftovers from before that migration.

Consequence: **running `deploy.sh` (or a raw `ctf challenge sync`) as-is would delete those 56 challenges'
native hints, and nothing would replace them**, because:

```
grep -rn 'HINT_WALLET_SYNC_SECRET' /opt/cei-labs/cei-labs-engine   # zero matches anywhere on this box
```

`HINT_WALLET_SYNC_SECRET` does not exist in `~/cei-labs-credentials.md`, in
`/opt/cei-labs/cei-labs-engine/docker/secrets/`, or anywhere else searched — so
`sync_hint_wallet_bundle()` in `deploy.sh` would print `HINT_WALLET_SYNC_SECRET not set; skipping
hint-wallet sync.` and silently no-op. Net effect for a live event: **players would lose all in-game hints**
until someone provisions that secret (`HINT_WALLET_REVISION` also required, plus the secret must be
≥32 chars) and reruns the hint-wallet sync step. This was not something I was told to expect, so I did not
proceed past this point without flagging it — I did not generate or guess a secret.

`CTFD_SYNC_SECRET` (required by `deploy.sh` for the instance-launcher mapping sync, separate from the hint
wallet) **is** available: `cei-labs-engine`'s own `offline-install.sh` documents it as
`CTFD_SYNC_SECRET=$(cat docker/secrets/plugin_shared_secret.txt)`, and that file exists and is world-readable
on this box.

## Remaining command to complete the push (NOT run)

Once a human has decided how to handle the hint-wallet gap above (either accept the native-hint loss,
provision `HINT_WALLET_SYNC_SECRET`/`HINT_WALLET_REVISION` and rerun, or add `hints:` back into the
generated `challenge.yml` files), the completing command is:

```bash
cd /opt/cei-labs/CEI-Labs-Wargames
export CTFD_URL=<from ~/cei-labs-credentials.md>
export CTFD_TOKEN=<API token from ~/cei-labs-credentials.md, WITHOUT the surrounding backticks>
export CTFD_SYNC_SECRET=$(cat /opt/cei-labs/cei-labs-engine/docker/secrets/plugin_shared_secret.txt)
# Optional, only if the hint-wallet gap is being resolved in this same run:
# export HINT_WALLET_SYNC_SECRET=<32+ char secret>
# export HINT_WALLET_REVISION=<next positive integer>
./deploy.sh
```

(Content regeneration in steps 1–2 of `deploy.sh` is idempotent and safe to let it rerun; the only
irreversible part is step 4, the actual CTFd sync loop.)

## Files touched by this session

- `challenges/*/challenge.yml` (59 files, regenerated content, not git-tracked/gitignored build output)
- `challenges/bandit-hint-wallet.json`, `challenges/krypton-hint-wallet.json`,
  `challenges/natas-hint-wallet.json` (regenerated, not git-tracked)
- `deployment-manifest.json` (regenerated, not git-tracked)
- This log file
- No changes to any tracked source file in the repo; no commits made.

## 2026-07-23 — Precondition check + staging for the final push (still NOT run)

### Wallet endpoint confirmed NOT live yet (expected)

- `sudo docker service ls` shows `cei-labs_orchestrator` running image `f491cdd86cee`.
- `sudo docker image inspect f491cdd86cee --format '{{.Created}}'` → `2026-07-22T16:58:34Z`.
- `cei-labs-engine` PR #13 ("Implement hint-wallet Engine sync/deduct/balance endpoints (P0)") merged as
  `f4749e83` at `2026-07-23T07:29:46-04:00` (= `2026-07-23T11:29:46Z`) — **after** the running image was
  built. The orchestrator container currently in the Swarm is confirmed to predate the merge; it does not
  contain the `/wallet/*` code.
- Live probe from inside the `cei-labs_ctfd` container (same overlay network,
  `cei-labs_orchestrator-internal`, orchestrator at `10.0.3.3:8080`):
  - `GET /healthz` → `200` (orchestrator itself is healthy/reachable).
  - `GET /wallet/balance/test` → `401 {"error":"unauthorized"}`.
  - `GET /wallet/nonexistent-xyz-route` and `GET /totally-bogus-route-abc123` → **also** `401
    {"error":"unauthorized"}`, identical body. Since a genuinely unauthenticated-but-real route and a
    made-up route return byte-identical responses, this is a blanket "auth required" catch-all on the old
    build, not route-specific `/wallet/*` logic — consistent with the pre-merge image and with the
    build-timestamp evidence above. No redeploy has happened; this is expected and not something to fix
    here.

### Content still current

Re-ran `scripts/build_bandit.py`, `build_krypton.py`, `build_natas.py`, `validate_game_stages.py`,
`validate_generated.py` on `fix/p0-content-deploy` (clean working tree, HEAD `cdab0c9`). Same result as the
original dry-run: 35/8/16 challenges generated, validation passed (59 challenges, 58 mappings, 3 launchers),
`git status` stayed clean throughout (all generated output is gitignored). No drift since the original
dry-run log above.

### Secrets staged (values not printed/logged/committed)

- `~/cei-labs-credentials.md` — has `CTFD_URL` (from the CTFd section header) and CTFd `API token`.
- `CTFD_SYNC_SECRET` — `cat /opt/cei-labs/cei-labs-engine/docker/secrets/plugin_shared_secret.txt` (32
  bytes, file present).
- `HINT_WALLET_SYNC_SECRET` — **now provisioned** (was missing at the time of the original dry-run above):
  `cat /opt/cei-labs/cei-labs-engine/docker/secrets/hint_wallet_sync_secret.txt` (65 bytes, satisfies
  `deploy.sh`'s `>= 32 chars` check).
- `HINT_WALLET_REVISION` — no prior catalog exists on the Engine side for this box (`wallet_catalog` table
  is fresh/unpopulated pending the redeploy — `try_accept_catalog()` in
  `cei-labs-engine/docker/orchestrator/app/store.py` accepts any positive-integer revision when no row
  exists yet), so **`1`** is the correct first value. Do not reuse `1` on any later resync — the Engine
  rejects a revision that isn't strictly higher than the last accepted one.

### Ready-to-execute command sequence

Run only after the Swarm stack has been redeployed with `cei-labs-engine` `main` (>= `f4749e83`) **and**
`GET /wallet/balance/<anything>` from inside the overlay network stops returning the blanket-401 signature
above (e.g. starts returning a distinct 404/200 for a real vs. bogus wallet id — confirms the new code is
actually running before spending the one-shot `HINT_WALLET_REVISION=1`):

```bash
cd /opt/cei-labs/CEI-Labs-Wargames
git status   # must be clean, still on fix/p0-content-deploy (or main, whichever is deploying)

export CTFD_URL=$(awk -F'— ' '/## CTFd/{print $2}' ~/cei-labs-credentials.md | tr -d '[:space:]')
export CTFD_TOKEN=$(awk '/API token:/{print $NF}' ~/cei-labs-credentials.md | tr -d '`')
export CTFD_SYNC_SECRET=$(cat /opt/cei-labs/cei-labs-engine/docker/secrets/plugin_shared_secret.txt)
export HINT_WALLET_SYNC_SECRET=$(cat /opt/cei-labs/cei-labs-engine/docker/secrets/hint_wallet_sync_secret.txt)
export HINT_WALLET_REVISION=1

./deploy.sh
```

(Sanity-check the `CTFD_URL`/`CTFD_TOKEN` extraction once against the actual file layout before relying on
the `awk` one-liners above — they're a best-effort based on the section format seen during this session;
if the file format differs, read the two values by hand instead of piping through `awk`.)

Expected outcome per the original diff (unchanged by anything done in this session): 35/59 challenge
descriptions update, 0 additions/removals/point/category/state changes, plus — new since the original
dry-run — the hint-wallet bundle now actually syncs instead of no-op'ing (all three tracks' hint-wallet
manifests uploaded, `Synced hint-wallet bundle` printed), and native CTFd hints on the 56 affected challenges
are still deleted by `ctf challenge sync` as documented above, with wallet-based hints taking over as their
replacement per the deliberate migration.

This session made no writes to live CTFd and did not run `deploy.sh`'s sync step. `git status` on
`CEI-Labs-Wargames` remained clean throughout.
