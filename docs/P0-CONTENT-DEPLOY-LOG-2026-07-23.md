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
