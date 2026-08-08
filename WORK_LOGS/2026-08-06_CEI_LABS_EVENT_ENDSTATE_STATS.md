---
title: "2026-08-06 CEI Labs Event — Final End-State & Live Stats"
tags: [cei-labs, wargames, ctfd, swarm, event-recap, end-state]
status: active
created: 2026-08-06
---

# CEI Labs Event — Final End-State & Live Stats (for event recap PR)

Pulled live from CTFd DB (`cei-labs_ctfd-db.1.ylf9ec2ck8ek3bxnju1qe7fvv`,
MariaDB 10.11) on swarm manager 192.168.1.150 at ~19:15 UTC 2026-08-06.
Feeds the CEI-Labs-Wargames event recap PR (coordinated with Honey).

## Live player/score numbers

- **Users:** 19 registered (11 teams). 9 teams have solves; `admin` and
  `ctfguy1` are 0-score placeholders.
- **Engagement:** 199 accepted solves from 399 total submissions.
- **Challenges:** 65 total, all four tracks **active/visible**:
  Linux Basics 35, Cryptography 8, Web Security 16, AI Copilot Setup 6.

### Per-track unique challenges solved
| Track | Solved / Total |
|---|---|
| Bandit (Linux Basics) | 22 / 35 |
| Krypton (Cryptography) | 7 / 8 |
| Natas (Web Security) | 11 / 16 |
| AI Copilot Setup | 4 / 6 |

### Final scoreboard (score / solves)
| Team | Score | Solves |
|---|---|---|
| DexMix | 16,080 | 35 |
| Workhorse | 15,830 | 36 |
| Ducks | 13,370 | 26 |
| 0100 | 9,690 | 32 |
| cyberparkour | 4,980 | 20 |
| Nerd_Nuggies | 3,720 | 14 |
| west point grads | 3,130 | 15 |
| Computers are evil | 1,780 | 11 |
| TeamSloth2ElectricBoogaloo | 1,770 | 10 |

### Team membership
DexMix 2, Workhorse 4, Ducks 1, 0100 2, cyberparkour 1, Nerd_Nuggies 2,
west point grads 2, Computers are evil 1, TeamSloth2ElectricBoogaloo 1,
admin 1, ctfguy1 1.

## Network / Swarm end-state (what we ended on)

- Swarm re-homed to new subnet **192.168.1.0/24**. Manager = `.150`
  (cei-ryzen5-61g-swarm01, Leader); workers `.193` (cei-i7-31g-swarm02)
  and `.125` (cei-xeon-e3-8g-swarm03). All 3 nodes Ready/Active.
- Re-initialized with `--advertise-addr 192.168.1.150` to fix the stale
  `192.168.10.13:2377` advertise address from the old subnet.
- Stack redeployed from `engine-31a6471`; `ORCHESTRATOR_OFFLINE_HOST`
  updated `192.168.10.13` → `192.168.1.150`.
- CTFd DB password realigned to current secret via temporary rescue
  container (no data purged).
- All 5 stack services `1/1`: ctfd, ctfd-db, ctfd-redis, orchestrator,
  traefik. https://192.168.1.150 live.
- Challenge infra per-team: many `chinst-*` (bandit/krypton) and
  `chrange-*` (natas attacker/target) service tasks running.

## What was sacrificed / sacrificed to make the event happen (network)

- **Old subnet (192.168.10.0/24) + old manager advertise addr** were
  abandoned when the swarm re-homed to 192.168.1.0/24. The OPNsense
  router on the old LAN was effectively bypassed for the event — the
  platform runs directly on the 192.168.1.x switch path.
- The original **OPNsense full internet/QoS path was not relied on** for
  the event; per earlier attempts the router upstream (WAN gateway/NAT)
  could not be made to pass normal internet reliably, so servers were
  re-homed instead. Local `ctf.internal` DNS intent was retained as a
  goal but the live event did not depend on OPNsense.
- Earlier 4-host pool was consolidated to the 3 reachable/healthy swarm
  hosts; `.12`-class hosts that couldn't join were dropped from the live
  swarm (3-node end-state).

## Issues → root causes (for recap "Issues" section)

1. **Workhorse (team 22) Krypton box missing / flags failing.** Team 22's
   Krypton instance was never materialized — the orchestrator create
   failed on a Docker overlay-network race
   (`network chnet-22-group-krypton not found`) and rolled back silently,
   leaving team 22 with CTFd flag secrets but **no SSH target**. Teams
   20/21/23/26/27/29 all got boxes. Fixed by recreating the instance via
   orchestrator API + re-syncing secrets to CTFd challenges 36-42; then
   again after a relaunch re-tore the box (same race). Final fix = clean
   non-relaunch create. Full detail:
   `WORK_LOGS/2026-08-06_CTFD_RESET_ADMIN_GAMES_USERS.md`.
2. **Bandit per-team passwords changed after relaunch.** A relaunch
   regenerated per-team creds, so old logins broke. Per user request, the
   resume level (bandit19) was set to username=password on port 32002.
3. **Hints stopped showing after user reset.** The reset deleted
   `hint_wallet_catalog_cache`; rebuilt display cache from orchestrator
   catalog. Lesson: future resets must not clear that row.

## Notes
- All data read-only from DB; no config changed during this collection.
- Verified swarm/stack health via `docker node ls` / `docker stack
  services cei-labs` on the manager.
