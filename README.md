# CEI-Labs-OTW-CTF 🚩

Part of the **CEI-Labs** ecosystem.

This repository contains the infrastructure and challenge generation scripts to host a local Capture The Flag (CTF) event using **CTFd**, while leveraging the excellent educational wargames hosted by [OverTheWire](https://overthewire.org).

## 🎮 Featured Games
1. **[Bandit](docs/bandit/):** Unix/Linux Basics
2. **[Krypton](docs/krypton/):** Cryptography
3. **[Natas](docs/natas/):** Server-side Web Security
4. **AI Copilot Setup:** set up [CEI Labs Agent](https://github.com/Judgernaut777/CEI-Labs-Agent),
   a free, local AI coaching assistant for the three tracks above (see
   `scripts/build_agent.py`). Unlike the three tracks above, this one has no
   per-team Docker instance and isn't part of the staged/wave-gated rollout
   below. It ships **hidden by default** -- the organizer releases it
   manually, on their own schedule, once ready, by generating with
   `CEI_AGENT_RELEASE_STATE=visible python3 scripts/build_agent.py` (or by
   toggling visibility directly in the CTFd admin UI). See that script's
   header comment for both ways.

Each game's folder holds three docs:
- `writeups.md` — complete, step-by-step solutions for every level
  (instructor answer key, not for participant distribution).
- `learning-objectives.md` — the real-world skills taught, organized by
  concept rather than level number.
- `cheatsheet.md` — a fast-lookup table for instructors walking a room
  during a live session.

## 📚 Documentation

- [Learning objectives](docs/learning-objectives.md) — index into each
  track's skills inventory, plus cross-track meta-skills
- [Instructor cheat sheet](docs/instructor-cheatsheet.md) — index into
  each track's fast-lookup table
- [Facilitation runbook](docs/facilitation-runbook.md) — how to run a
  live event, start to finish
- [Troubleshooting / known-issues FAQ](docs/troubleshooting-faq.md)
- [Participant quick-start](docs/participant-quickstart.md) — one-pager
  for players
- [Wargame-building playbook](docs/wargame-building-playbook.md) — the
  reusable methodology behind these tracks, for building the next one
- [Required network access](docs/network-access.md) — external sites
  the challenge hints link to; source of truth for `cei-labs-net`'s
  firewall allowlist
- [Self-hosted wargames status](docs/self-hosted-wargames-status.md)
  and [blueprint](docs/self-hosted-wargames-blueprint.md)
- [Staggered game-stage contract](docs/staggered-game-stages.md) — the
  Bandit/Krypton/Natas grouping and pre-deployment validation used by Engine
- [Staged game operations](docs/staged-game-operations.md) — rehearsal and
  event-day controls for independently released game stages
- [Presentation sources](presentation/README.md) — current kickoff and
  per-track briefing source
- [Event recap — 2026-08-06](docs/event-recap-2026-08-06.md) — post-event
  write-up of the 2026-08-06 run (issues, network end-state, what was
  sacrificed, how challenges were played)

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

Deployment generates all four tracks and runs the read-only stage validator
before uploading. It must report Bandit 35, Krypton 8, and Natas 16 (the
staged/wave-gated games); AI Copilot Setup's 6 challenges aren't part of
that staging and are validated separately by `validate_generated.py`. The
event administrator then syncs and starts each staged game independently in
Engine; loading challenge content does not start a game clock.

The deployment preflight is fail-closed: it requires authenticated CTFd
inventory access, successful challenge install/sync responses, successful
instance-launcher mapping sync, and exact totals of 65 challenges, 59 mapped
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
