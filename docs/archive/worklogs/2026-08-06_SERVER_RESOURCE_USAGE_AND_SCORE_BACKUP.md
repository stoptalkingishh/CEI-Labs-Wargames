---
title: "2026-08-06 CEI Labs Event — Server Resource Usage & Score Backup"
tags: [cei-labs, wargames, ctfd, swarm, resource-usage, backup]
status: active
created: 2026-08-06
---

# CEI Labs Event — Server Resource Usage & Score Backup

Pulled live 2026-08-06 ~19:35 UTC on the 3-node Swarm (192.168.1.0/24).
Fed the event recap PRs (coordinated with Honey #62 / Opencode #54 / Bumble).

## Node capacity & CURRENT resource usage (post-event, idle)

`docker stats --no-stream` + `free`/`df`/`uptime` captured at event end.
These are CURRENT live values — see "Important caveat" below.

| Node | IP | Roles | Cores | RAM (used/total) | Disk (used/total) | Load avg |
|---|---|---|---|---|---|---|
| cei-ryzen5-61g-swarm01 (Leader) | .150 | ctfd-db, orchestrator, traefik | 12 | 6.9 / 61 GiB | 53 / 464 GB (12%) | 0.22 |
| cei-i7-31g-swarm02 | .193 | ctfd app | 12 | 3.8 / 31 GiB | 13 / 475 GB (3%) | 0.17 |
| cei-xeon-e3-8g-swarm03 | .125 | ctfd-redis + challenge gateways | 8 | 2.6 / 7.7 GiB | 6 / 231 GB (3%) | 0.08 |

## Key stack containers (current CPU / memory at capture)

| Container | Node | CPU | Mem (used / limit) |
|---|---|---|---|
| cei-labs_ctfd | .193 | 0.09% | 370 MiB / 1 GiB |
| cei-labs_ctfd-db | .150 | 0.00% | 105 MiB / 1 GiB |
| cei-labs_ctfd-redis | .125 | 4.00% | 5.1 MiB / 256 MiB |
| cei-labs_orchestrator | .150 | 0.01% | 41 MiB / 256 MiB |
| cei-labs_traefik | .150 | 0.00% | 25.8 MiB / 61.9 GiB |

~20 per-team challenge containers (`chinst-*` bandit/krypton, `chrange-*`
natas attacker/target, plus `*-gateway`) with 64-512 MiB limits, all idle at
capture (0.00-3.34% CPU). No per-team container at or near its limit.

## IMPORTANT caveat on "max resource usage"

There was **no monitoring/collector running during the event**, so historical
peaks (max CPU/mem/disk DURING play) are **not recoverable** — nothing logged
them. The numbers above are the post-event idle state plus node capacity.
Bumble confirmed nothing on disk either. To capture real peaks in a future
event, a `docker stats` loop or Prometheus/Node-exporter would need to run
throughout. Recommend documenting node capacity + current idle as the
authoritative resource record for this recap, not fabricated peak figures.

## Score backup (machine-readable)

Durable CTFd MariaDB dump taken on manager .150:

- Container: `cei-labs_ctfd-db.1.ylf9ec2ck8ek3bxnju1qe7fvv`
- Command: `mysqldump -uctfd -p** --single-transaction --routines --events ctfd`
- Remote: `/home/ismaelrodriguez/backups/cei-labs-ctfd-backup-2026-08-06.sql`
- Local: `.scratch/ctfd-backup/cei-labs-ctfd-backup-2026-08-06.sql`
- Size: 256,480 bytes (valid MariaDB 10.11 dump, verified)

Contains all scoring tables: `solves`, `submissions`, `solutions`, `awards`,
`challenges`, `flags`, `teams`, `users`, `hints`,
`hint_wallet_catalog_cache`, plus custom `wargame_stages`,
`wargame_stage_challenges`, `wargame_stage_audit`,
`instance_launcher_team_secrets`.

Backup restore would be: `mysql -uctfd -p ctfd < dump.sql` (or via the
ctfd-db container).
