# Changelog

Format loosely follows [Keep a Changelog](https://keepachangelog.com/).
This repo predates this file (71 commits as of 2026-07-15) — entries below
start from where this file was introduced plus a milestone summary of what
came before it, not a commit-by-commit history. See `git log` for the full
record.

## [Unreleased]

### Added
- Human-playability support for Krypton: an offline `krypton-tools`
  command for frequency counts, Caesar rotation, Vigenere column
  splitting, and Kasiski evidence; the missing level-3 `found1`-`found3`
  samples; and an in-login pointer to the toolkit.
- A Natas attacker workstation image with the tools players need for the
  middle and late levels, including `xxd`, `rev`, `jq`, Python requests,
  `file`, and `natas-help`.
- Progressive Natas hint rendering with clear Step 1/2/3 headings,
  an HTTP Basic Auth reminder on every tier, and authenticated,
  copy-pasteable `curl` examples.
- `docs/challenge-inventory.md`: the full 59-level structured inventory
  (ID, points, flag source, instance type, reset method, dependencies,
  hints, expected solve path) the production-readiness tracker's §3 P0
  item calls for, generated directly from every `challenges/*/challenge.yml`.
  Surfaced a real finding along the way: `krypton-00` (a real 200-point
  scored challenge, not a tutorial) uses a static, non-per-team flag,
  because it has no per-team instance to scope a dynamic flag to — see
  that doc for the full explanation and a recommended accepted-risk
  write-up.

### Fixed
- Krypton Vigenere guidance now groups letters exactly as the cipher does;
  spaces and punctuation no longer shift the suggested columns.
- Krypton level-2 and later hints now match the deployed command-line
  behavior and point players at local analysis helpers.
- Natas level 7 restores the intended page-source hint for the local file
  inclusion path.
- Natas level 8 now gives a valid hex decode/reverse/base64 pipeline using
  tools installed in the attacker image.
- Natas level 11 now uses the exact JSON plaintext for the XOR cookie and
  includes a complete offline forging helper.
- Krypton instructor writeups now use the deployed `/home/kryptonN`
  paths instead of nonexistent `/krypton/kryptonN` paths.

### Deployment notes
- The Natas generator now references
  `ghcr.io/stoptalkingishh/cei-labs-wargames/natas-attacker:latest`.
  Publish that attacker image to GHCR before relying on the generated
  deployment manifests outside the local Docker test environment.

## Milestones before this file existed

- Bandit (35 levels), Krypton (8 levels), and Natas (16 levels) converted
  from pointing at OverTheWire's live infrastructure to fully
  self-hosted target images, deployed on demand by `cei-labs-engine`'s
  orchestrator.
- Per-team dynamic flags rolled out across every mechanism used by the
  56 non-tutorial/non-self-contained levels: flat files, byte-count-
  sensitive files, transforms, TCP/TLS daemons, SUID binaries, a
  randomized brute-force PIN, and all 5 git-history-hiding mechanisms —
  verified end-to-end against a live redeployed stack with two simulated
  teams.
- Security audit: fixed world-readable Natas htpasswd files (0600 now,
  were 0644 root-owned — exploitable via any level's intended RCE to read
  every other level's password hash) and four levels (Natas 6/8/11/14)
  that leaked their own next-level secret through their `?source`
  view-source feature.
- Staggered-game content (independent per-game starts/scoreboards for
  Bandit/Krypton/Natas): `game-stages.yml` + validator, merged to `main`.

Full detail lives in `docs/self-hosted-wargames-status.md` and
`docs/security-audit-status.md`.
