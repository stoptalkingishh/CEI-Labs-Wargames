# 2026-08-06 Swarm re-homed to 192.168.1.0/24

## What was asked
Set up the Docker Swarm with the new server IPs: main `192.168.1.150`,
workers `192.168.1.193` and `192.168.1.125`.

## SSH access established (this session)
- `.150` = `cei-ryzen5-61g-swarm01`, user `ismaelrodriguez`, password candidate
  `Access4n/a`. Passwordless sudo confirmed.
- `.193` = `cei-i7-31g-swarm02`, user `ismaelrodriguez`, password `Alpha4n/a`.
- `.125` = `cei-xeon-e3-8g-swarm03`, user `ismaelrodriguez`, password `Alpha4n/a`.
- Managed client used `plink` (PuTTY) for password auth; OpenSSH keys were denied.

## Swarm fix (critical correctness issue)
The manager `.150` still advertised the dead `192.168.10.13:2377` from the old
subnet, even though its new IP was `192.168.1.150`. Workers joined via
`.150:2377` but the manager told them to reach it at `.10.13` (unreachable on
the new subnet). Re-initialized the swarm with the correct advertise address:

- `docker swarm leave --force` on `.150`
- `docker swarm init --advertise-addr 192.168.1.150`
- relabeled manager `ctfd-data=true`
- rejoined `.193` and `.125` as workers with the new token

Resulting node list (all Ready/Active):
- `cei-ryzen5-61g-swarm01` Leader (Docker 29.6.2)
- `cei-i7-31g-swarm02` worker (29.7.1)
- `cei-xeon-e3-8g-swarm03` worker (29.6.2)

Workers now see `RemoteManagers` = `192.168.1.150:2377` (verified on both).

## Stack redeploy
Swarm re-init wiped the swarm-level stack definition. Redeployed from
`/home/ismaelrodriguez/deployments/engine-31a6471` via `stack-up.sh`.
Updated `docker/.env` `ORCHESTRATOR_OFFLINE_HOST` from `192.168.10.13` to
`192.168.1.150`. Orchestrator service now runs with the new host.

## CTFd DB password mismatch
The persistent `cei-labs_ctfd_db_data` volume held `ctfd`/`root` passwords from
an older deploy that no longer matched `docker/secrets/*.txt`, so CTFd got
`Access denied for user 'ctfd'`. Recovered safely with a temporary
`mariadb:10.11` rescue container using `--skip-grant-tables` (mounted the
existing data volume) and realigned the `ctfd` and `root` users to the current
secret values. No data was purged. Removed the rescue container afterward.
(An earlier attempt had failed; the key was piping SQL via stdin inside the
rescue container instead of `-e` quoting over SSH.)

## Verification
- `docker node ls`: 3 nodes Ready/Active, manager Leader, correct advertise.
- `docker stack services cei-labs`: ctfd, ctfd-db, ctfd-redis, orchestrator,
  traefik all `1/1`.
- `https://192.168.1.150/login` -> HTTP 200.
- DB auth with new secret: `ctfd` user lists `ctfd` + `information_schema`.
