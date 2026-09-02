# CEI-Labs-OTW-CTF 🚩

Part of the **CEI-Labs** ecosystem.

This repository contains the infrastructure and challenge generation scripts to host a local Capture The Flag (CTF) event using **CTFd**, while leveraging the excellent educational wargames hosted by [OverTheWire](https://overthewire.org).

## 🎮 Featured Games
1. **[Bandit](docs/tracks/bandit/):** Unix/Linux Basics
2. **[Krypton](docs/tracks/krypton/):** Cryptography
3. **[Natas](docs/tracks/natas/):** Server-side Web Security
4. **AI Copilot Setup:** set up [CEI Labs Agent](https://github.com/Judgernaut777/CEI-Labs-Agent),
   a free, local AI coaching assistant for the three tracks above (see
   `scripts/build_agent.py`). Unlike the three tracks above, this one has no
   per-team Docker instance and isn't part of the staged/wave-gated rollout
   below. It ships **hidden by default** -- the organizer releases it
   manually, on their own schedule, once ready, by generating with
   `CEI_AGENT_RELEASE_STATE=visible python3 scripts/build_agent.py` (or by
   toggling visibility directly in the CTFd admin UI). See that script's
   header comment for both ways.
5. **OSINT pilot:** a neutral, artifact-only Open-Source Intelligence track —
   [docs/tracks/osint/](docs/tracks/osint/). Three reviewed dossiers are
   supplied by the separately maintained `ctfgen-family-osint` package and
   exported to CTFd by `scripts/build_osint.py`. The track has no container,
   ports, or per-team runtime, ships **hidden by default**, and is
   intentionally outside the staged rollout. Release only after organizer
   review with `CEI_OSINT_RELEASE_STATE=visible python3 scripts/build_osint.py`.
6. **Threadline:** a full-length, 42-lead OSINT wargame — a 6–7 hour discovery
   campaign for a **Tiberian Order** analyst, unravelling the hidden
   coordination node called **the Loom**. See
   [docs/tracks/threadline/](docs/tracks/threadline/). Like the pilot it has
   no container, ports, or per-team runtime, ships **hidden by default**, and
   lives outside the staged rollout. Release with
   `THREADLINE_RELEASE_STATE=visible python3 scripts/build_threadline.py`.
7. **Sentinel:** a defensive security lab track (see
   [docs/tracks/sentinel/](docs/tracks/sentinel/) and
   [docs/tracks/sentinel-ooda/](docs/tracks/sentinel-ooda/)).

Each primary game's folder holds the same core docs:
- `README.md` — track overview and how to build/release it
- `writeups.md` — complete, step-by-step solutions for every level
  (instructor answer key, not for participant distribution).
- `learning-objectives.md` — the real-world skills taught, organized by
  concept rather than level number.
- `cheatsheet.md` — a fast-lookup table for instructors walking a room
  during a live session.

## 📚 Documentation

The canonical index is **[docs/README.md](docs/README.md)** — it organizes every
document into **guides** (evergreen operator/instructor material),
**tracks** (per-wargame docs), **reference**, and **archive** (history:
event recaps, worklogs, plans, dated gap analyses, art/story proposals).

Highlights:
- [Participant quick-start](docs/guides/participant-quickstart.md) — one-pager
  for players
- [Facilitation runbook](docs/guides/facilitation-runbook.md) — how to run a
  live event, start to finish
- [Troubleshooting / known-issues FAQ](docs/guides/troubleshooting-faq.md)
- [Challenge inventory](docs/guides/challenge-inventory.md) — generated from
  the challenge definitions, audited by CI
- [Wargame completion status](docs/guides/game-completion-status.md) — current
  scope, generated counts, and release-readiness boundaries for every track
- [Required network access](docs/guides/network-access.md) — external sites
  the challenge hints link to; source of truth for `cei-labs-net`' s
  firewall allowlist
- [Self-hosted wargames status](docs/guides/self-hosted-wargames-status.md)
  and [blueprint](docs/guides/self-hosted-wargames-blueprint.md)
- [Staggered game-stage contract](docs/guides/staggered-game-stages.md) — the
  Bandit/Krypton/Natas grouping and pre-deployment validation used by Engine
- [Staged game operations](docs/guides/staged-game-operations.md) — rehearsal
  and event-day controls for independently released game stages
- [Security lab intake backlog](docs/guides/security-lab-intake.md) — proposed
  offline, safe, and testable future lab concepts
- [Presentation sources](docs/presentation/README.md) — kickoff and game-guide
  briefing sources
- [Event archive](docs/archive/events/) — recaps of past runs

## 🚀 Setup Instructions

### 1. Generate and Deploy the Challenges
You can build and deploy the entire training pipeline directly into your CTFd instance using the automated deployment script.

Ensure you pass your CTFd scoreboard details as environment variables if running in an automated CI/CD runner:

```bash
export CTFD_URL="https://your-ctfd-scoreboard.com"
export CTFD_TOKEN="your_admin_token_here"
export CTFD_SYNC_SECRET="the Engine instance-launcher sync secret"

# This builds all modules (Bandit, Krypton, Natas, AI Copilot Setup) and syncs them
chmod +x deploy.sh
./deploy.sh
```

### Natas RCE isolation audit

For an authorized synthetic-secret container audit of the intentional Natas
12/13 upload RCE lessons, see
[`docs/tracks/natas/natas-12-13-rce-isolation-audit.md`](docs/tracks/natas/natas-12-13-rce-isolation-audit.md).

Deployment generates all four tracks and runs the read-only stage validator
before uploading. It must report Bandit 35, Krypton 8, and Natas 36 (the
staged/wave-gated games); AI Copilot Setup's 6 challenges aren't part of
that staging and are validated separately by `validate_generated.py`. The
event administrator then syncs and starts each staged game independently in
Engine; loading challenge content does not start a game clock.

The deployment preflight is fail-closed: it requires authenticated CTFd
inventory access, successful challenge install/sync responses, successful
instance-launcher mapping sync, and exact totals of 85 challenges, 79 mapped
environments, and 4 visible launchers. `.ctf/config` is written mode `0600`.

## Validation and immutable releases

Run the same metadata gate used by CI:

```bash
python3 scripts/build_bandit.py
python3 scripts/build_krypton.py
python3 scripts/build_natas.py
python3 scripts/build_agent.py
python3 scripts/validate_game_stages.py
python3 scripts/validate_generated.py --output validation-manifest.json
```

Before a production release, replace generated image fields with immutable
`name@sha256:<64-hex-digest>` references and run:

```bash
python3 scripts/validate_generated.py --release --output release-manifest.json
```

Release mode rejects `latest`, development tags, and every other floating
reference. `.github/workflows/validate.yml` runs the normal generation gate
on pushes and pull requests. The manually dispatched `build-targets.yml`
workflow requires an immutable Engine base-image digest and publishes SBOM
and provenance metadata for Bandit, Krypton, and Natas target images. All
third-party GitHub Actions are pinned to commit SHAs.

### 2. Self-signed / LAN CTFd instances

If `CTFD_URL` points at a CTFd instance behind a self-signed or otherwise
untrusted TLS certificate (common for LAN-only events — this is the
default for [`cei-labs-engine`](https://github.com/stoptalkingishh/cei-labs-engine)
unless `USE_LETSENCRYPT=true` is set), also set:

```bash
export CTFD_INSECURE=true
```

This disables TLS certificate verification for the `ctfcli` calls this
script makes. It defaults to `false` (verification on) and must be set
explicitly — never enable it against an instance you don't control.

## Local Natas Runtime Audit

`scripts/runtime_audit_natas.py` is an opt-in integration audit for a local,
authorized Natas target only. It verifies the Natas 0-34 solve and HTTP auth
chains using supplied synthetic per-team secrets. It is not run by the normal
CI validation workflow and rejects non-loopback URLs.

After building the Natas target image, publish its internal ports only to the
local host and start it with synthetic `LEVEL_SECRETS`. Then run the audit
with the same JSON values:

```bash
SECRETS="$(python3 -c 'import json; print(json.dumps({**{f"natas{n}": f"local-{n}" for n in range(1, 35)}, "natas34final": "local-final"}))')"
docker build -t cei-natas-local targets/natas
docker run --rm -d --name cei-natas-audit --env "LEVEL_SECRETS=$SECRETS" $(for n in $(seq 0 34); do printf '%s ' "-p 127.0.0.1:$((18000 + n)):$((8000 + n))"; done) cei-natas-local
for i in $(seq 1 30); do curl -s -o /dev/null http://127.0.0.1:18000/ && break; sleep 1; done
python3 scripts/runtime_audit_natas.py --base-url http://127.0.0.1:18000 --secrets "$SECRETS"
docker stop cei-natas-audit
```

An image workflow can run these same commands as a post-build smoke test with
ephemeral synthetic values and localhost-only port mappings. The audit has no
public-target fallback or external service dependency.
