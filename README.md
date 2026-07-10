# CEI-Labs-OTW-CTF 🚩

Part of the **CEI-Labs** ecosystem.

This repository contains the infrastructure and challenge generation scripts to host a local Capture The Flag (CTF) event using **CTFd**, while leveraging the excellent educational wargames hosted by [OverTheWire](https://overthewire.org).

## 🎮 Featured Games
1. **[Bandit](docs/bandit/):** Unix/Linux Basics
2. **[Krypton](docs/krypton/):** Cryptography
3. **[Natas](docs/natas/):** Server-side Web Security

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
- [Self-hosted wargames status](docs/self-hosted-wargames-status.md)
  and [blueprint](docs/self-hosted-wargames-blueprint.md)

## 🚀 Setup Instructions

### 1. Generate and Deploy the Challenges
You can build and deploy the entire training pipeline directly into your CTFd instance using the automated deployment script.

Ensure you pass your CTFd scoreboard details as environment variables if running in an automated CI/CD runner:

```bash
export CTFD_URL="https://your-ctfd-scoreboard.com"
export CTFD_TOKEN="your_admin_token_here"

# This builds all modules (Bandit, Krypton, Natas) and syncs them
chmod +x deploy.sh
./deploy.sh
```

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
