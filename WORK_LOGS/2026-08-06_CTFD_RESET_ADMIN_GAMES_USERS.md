---
title: "2026-08-06 CTFd Reset — admin password, games, user accounts"
tags: [ctfd, reset, admin, wargames, cei-labs]
status: active
created: 2026-08-06
---

# 2026-08-06 CTFd Reset (admin password, games, user accounts)

## What was asked
On the re-homed swarm (CTFd at https://192.168.1.150):
1. Report the admin password status / provide the admin password.
2. Reset the games to start, unlocking **only** Bandit and AI Copilot games.
3. Reset **all** user accounts.

## Environment
- CTFd 3.8.6, user_mode = **teams**. DB container `cei-labs_ctfd-db` (MariaDB 10.11)
  runs on manager `.150`; CTFd app container runs on worker `.193`.
- Swarm manager `.150` user `ismaelrodriguez` / `Access4n/a`; worker `.193` user
  `ismaelrodriguez` / `Alpha4n/a`.

## Actions
1. **Backup first** (destructive change on live system):
   `mysqldump` of the `ctfd` DB → `/home/ismaelrodriguez/ctfd-backup-20260806-090853.sql.gz`
   (55 KB, 28 users, 65 challenges).

2. **Admin password**: the existing hash was `$bcrypt-sha256$` (unrecoverable
   plaintext). Generated a fresh hash using CTFd's own
   `CTFd.utils.crypto.hash_password` inside the running ctfd container and wrote it to
   user id 1. Verified round-trip with `CTFd.utils.crypto.verify_password` → True.
   New admin password: `CEI-Labs-Admin2026!`.

3. **Games reset / only Bandit + AI Copilot unlocked** (direct SQL, transaction):
   - Set every `wargame_stages` row to `pending`, cleared start/lock/close fields.
   - Set all challenges to `hidden`.
   - Re-`active`d only `bandit` and `ai-copilot` stages (started_at=now,
     scoreboard_visible=1) and set their mapped challenges to `visible`.
   - Krypton and Natas left `pending`/hidden.

4. **User accounts reset**:
   - Deleted every non-admin user (kept id 1 admin) and every non-admin team
     (kept team 1). Repointed admin user→team 1, team 1 captain→admin.
   - Cleared solves, submissions, tracking, unlocks, awards, tokens, comments,
     notifications, ratings, field_entries, instance_launcher_team_secrets,
     hint_wallet_catalog_cache. All counts now 0.

## Verification
- `users`: only `admin` (id 1, admin@ctf.local, team 1). `teams`: only `admin`.
- Stages: `bandit`=active, `ai-copilot`=active, `krypton`=pending, `natas`=pending.
- Challenges by category/state: Linux Basics 35 **visible**, AI Copilot Setup 6
  **visible**, Cryptography 8 **hidden**, Web Security 16 **hidden**.
- Web login as `admin` with the new password → 302 redirect to authed home,
  `window.init` shows userId 1 / userName admin / Admin Panel nav. Challenges
  admin API returns 200 with all 65.

## Notes / decisions
- CTFd login form requires a CSRF nonce (from `window.init.csrfNonce`), so the
  first naive POST returned 403 — this was CSRF, not a wrong password. Confirm
  logins with the nonce flow.
- The initial user reset intentionally kept admin's own (test) solve/submission
  rows because the WHERE clause excluded id 1; a follow-up `DELETE` cleared all
  progress to leave a fully clean slate.
- Scripts were written to the servers for execution and removed afterward; the
  DB backup file is retained on `.150`.

## Follow-up: hints stopped showing (2026-08-06T13:48)
**Cause:** the user reset deleted the CTFd-side hint-wallet display cache row
`hint_wallet_catalog_cache` (id=1). `/plugins/hint-wallet/api/tiers/<track>/<entry>`
reads that row to list a hint's tier costs before a player spends; with the row
gone it returned `409 no_active_catalog`, so hints rendered nowhere for anyone.
The authoritative catalog lives in the orchestrator's SQLite (`wallet_catalog`,
id=1, revision 9, 3 tracks) and was untouched by the reset.

**Fix:** reconstructed the stripped display bundle exactly as the plugin's
`_cache_catalog_for_browsing()` writes it (schema_version + revision + manifests
with each tier's `content` removed) from the orchestrator's `wallet_catalog`
`bundle_json`, and upserted it back into `hint_wallet_catalog_cache` (id=1,
revision 9). **No re-sync/signature needed** — the orchestrator already holds the
accepted catalog.

**Verify:** authed `GET /plugins/hint-wallet/api/tiers/<track>/<entry>` now returns
HTTP 200 with tier costs (20/50/85) for bandit, krypton, and natas entries.
Lesson: a full CTFd user/progress reset must NOT clear `hint_wallet_catalog_cache`
— the display cache is rebuilt only by a wallet sync; drop the table-wide DELETE
of it from any future reset.

## Follow-up: Krypton started (2026-08-06T14:42)
User asked to start Krypton (it was left pending/hidden by the reset).
Activated the `krypton` stage (state=active, started_at=now, started_by=admin,
scoreboard_visible=1) and set all 8 Cryptography challenges to `visible`.
Verified: public (non-admin) `/api/v1/challenges` now lists `Cryptography`
alongside `Linux Basics` and `AI Copilot Setup`. Stages: bandit/krypton/ai-copilot
active, natas still pending.

## Follow-up: Workhorse (team 22) Krypton box missing (2026-08-06T16:00)
**Symptom:** Workhorse couldn't SSH into the Krypton user accounts / flags weren't
accepted.

**Root cause:** team 22's Krypton instance (`chinst-22-group-krypton`) had **never
been created**. The orchestrator's create at 15:18 failed with a Docker overlay
network race (`network chnet-22-group-krypton not found` during service create)
and rolled back, so Workhorse had **no box to connect to** at all — teams 20/21/23/26/27/29
all had boxes, team 22 did not. Their CTFd flag secrets existed (from an earlier
launch attempt) but pointed at nothing. This is the same failure class as the earlier
"port 32009 can't login to bandit0" report — a per-team instance that silently failed
to materialize.

**Fix:**
1. Verified no `instances`/network/service existed for owner 22 `group-krypton`.
2. Recreated the instance directly via the orchestrator API
   (`POST /instances`, owner 22, key `group-krypton`, type single-target,
   image `ghcr.io/stoptalkingishh/cei-labs-wargames/krypton-target:latest`,
   secret_keys `krypton0/2/6` + alpha `krypton1/3/4/5`, relaunch=True). → HTTP 201,
   fresh per-team secrets, port **32018**.
3. Synced the fresh secrets into CTFd `instance_launcher_team_secrets` for owner 22,
   challenges 36–42 (ON DUPLICATE KEY UPDATE).
4. Verified end-to-end over SSH: `krypton0`/`krypton0` front door works on 32018;
   `encoded.txt` base64-decodes to the synced krypton0 secret; `krypton1` logs in
   with it; its ROT13 file decodes to the synced krypton1 secret. Full chain intact.

**Lesson:** a failed instance create (network race) can leave a team with CTFd secrets
but no box, silently. The tcp-gateway network is created just before the service and
wasn't visible yet — a retry with `relaunch=True` resolves it. If a user reports
"can't log in" to a per-team SSH box, first check the orchestrator `instances` table /
running services to confirm the instance actually exists.

## Follow-up: Natas started (2026-08-06T17:16)
User asked to open the last game, which is Natas (Web Security). Activated the `Natas`
stage (state=active, started_at=now, started_by=1 (admin user id), scoreboard_visible=1)
and set all 16 Web Security challenges to `visible`. Verified authed (admin) API
`/api/v1/challenges` now lists all four categories: Linux Basics 35, Web Security 16,
Cryptography 8, AI Copilot Setup 6. All stages now active.

Access notes:
- DB creds come from docker secret `cei-labs_ctfd_db_password` (mounted at
  `/run/secrets/ctfd_db_password`); DB container `cei-labs_ctfd-db` runs on manager `.150`.
- CTFd API `/api/v1/challenges` requires auth and its login nonce is session-scoped —
  you must reuse the GET session cookie (curl `-c/-b cj.txt`) when POSTing the login form.

