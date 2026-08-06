# Event Recap — 2026-08-06 CEI Labs Wargames

A post-event write-up of the 2026-08-06 wargames run: the issues hit and
fixed, the network end-state we landed on, what had to be sacrificed to make
the event happen, and how the challenges were actually played. Source of truth
for the numbers below is the `CEI-LABS` relay channel recap plus the operator
`WORK_LOGS`; live player counts were confirmed at event time by the
orchestrating agent.

## 1. Infrastructure end-state

| Component | End-state |
| :--- | :--- |
| Docker Swarm | 3 nodes Ready/Active — manager `cei-ryzen5-61g-swarm01` (**192.168.1.150**), workers `cei-i7-31g-swarm02` (192.168.1.193), `cei-xeon-e3-8g-swarm03` (192.168.1.125) |
| Manager advertise addr | `192.168.1.150:2377` |
| CEI stack | `ctfd`, `ctfd-db`, `ctfd-redis`, `orchestrator`, `traefik` — all `1/1` |
| CTFd | 3.8.6, `user_mode = teams` |
| Access | https://192.168.1.150 |

All four games active at close:

| Game | Category | Challenges |
| :--- | :--- | :--- |
| Bandit | Linux Basics | 35 |
| Krypton | Cryptography | 8 |
| Natas | Web Security | 16 |
| AI Copilot Setup | (AI) | 6 |

## 2. Issues hit and fixed

1. **Stale Swarm advertise address after subnet re-home.** The manager still
   advertised the old dead `192.168.10.13:2377`. Fixed by
   `docker swarm leave --force` + re-init with `--advertise-addr
   192.168.1.150` and rejoining both workers; the stack was redeployed and
   `ORCHESTRATOR_OFFLINE_HOST` updated from `192.168.10.13` → `192.168.1.150`.
2. **CTFd DB password mismatch.** The persistent `cei-labs_ctfd_db_data`
   volume held older passwords that no longer matched `docker/secrets/*.txt`
   → `Access denied for user 'ctfd'`. Recovered with a temporary
   `mariadb:10.11 --skip-grant-tables` rescue container, realigned users, no
   data purged.
3. **Admin password not recoverable.** Existing hash was `$bcrypt-sha256$`.
   Regenerated via CTFd's own `hash_password`, verified round-trip.
4. **User/game reset wiped the hint-wallet display cache.** After deleting
   non-admin users, the hint-wallet API returned `409 no_active_catalog` so
   no hints rendered. Rebuilt `hint_wallet_catalog_cache` from the
   orchestrator's authoritative catalog (revision 9, 3 tracks); no re-sign
   needed. **Lesson:** a full reset must not `DELETE` that cache row.
5. **Per-team Krypton instance silently missing (Workhorse, team 22).** The
   orchestrator create failed on a Docker overlay-network race
   (`network chnet-22-group-krypton not found`) and rolled back, so team 22
   had CTFd flag secrets but **no SSH box at all** while teams 20/21/23/26/27/29
   had one. Recreated via the orchestrator API (fresh per-team secrets, port
   32018) and re-synced flag secrets for challenges 36–42. Hit **twice** — a
   relaunch teardown-then-recreate on the same network name repeats it.
   **Lesson:** check the orchestrator `instances` table / running services
   before blaming credentials when a user "can't log in."
6. **Bandit per-team passwords rotated by a relaunch.** Workhorse's box had
   been relaunched, regenerating all per-team passwords. Resume point set to
   `bandit19 / bandit19` per the operator, with the level-20 target in place.

## 3. How the challenges were done

Played through the **normal CTFd player flow** — real SSH boxes, real web
endpoints, real challenge pages/API. The orchestrating pass registered
10 players (`cei-player-1`…`10`) on team `CEI-Agent-Team`, launched their
environments through the CTFd launch API, and solved levels with the intended
techniques (e.g. Bandit's password-chain SSH, Krypton's base64/ROT13/known-
plaintext chain, Natas web exploitation). Recovered keys were shared on the
team so players reused them instead of re-spending. Submissions went through
the public challenge-submit path only — **no** reading of CTFd DB, source, or
containers for flags.

| Track | Unique challenges solved (final) | Available |
| :--- | :--- | :--- |
| Bandit (Linux Basics) | 22 | 35 |
| Krypton (Cryptography) | 7 | 8 |
| Natas (Web Security) | 11 | 16 |
| AI Copilot Setup | 4 | 6 |

Earlier orchestration pass (agent-driven) contributed an initial
**24 accepted submissions** (Bandit 0→1…15→16, Krypton 0→1/1→2, Natas 0→1);
real teams carried the event to the final totals above. Submissions went through
the public challenge-submit path only — **no** reading of CTFd DB, source, or
containers for flags.

## 4. Player participation

- **30 total participants** (operator's count — source of truth for who took
  part). Of those, **19 registered users / 11 teams** appear in the CTFd DB;
  the delta is people who played but never registered or submitted on the box.
- 9 teams have solves; `admin` and `ctfguy1` are 0-score placeholders.
- **199 accepted solves** from **399 total submissions** across all 4 active
  tracks (65 challenges).
- **Agent-driven playthrough:** 10 registered players (`cei-player-1`…`10`) on
  one shared team (`CEI-Agent-Team`), launched via the CTFd launch API with
  recovered keys shared team-wide.

**Final scoreboard (score / solves):**

| Team | Score | Solves |
| :--- | :--- | :--- |
| DexMix | 16,080 | 35 |
| Workhorse | 15,830 | 36 |
| Ducks | 13,370 | 26 |
| 0100 | 9,690 | 32 |
| cyberparkour | 4,980 | 20 |
| Nerd_Nuggies | 3,720 | 14 |
| west point grads | 3,130 | 15 |
| Computers are evil | 1,780 | 11 |
| TeamSloth2ElectricBoogaloo | 1,770 | 10 |

Numbers pulled live from the CTFd DB on `192.168.1.150` at event close by the
orchestrating agent. The operator and agents were actively resolving per-team
account/flag issues throughout (see the communications recap in
`docs/event-communications-2026-08-06.md`).

## 5. What was sacrificed to make the event happen (network)

The biggest concession was **network architecture**:

- The **five-VLAN router-on-a-stick** reference design
  (`VLAN10/20/30/40/50` segmentation) was **dropped** for the live box. The
  router carries **two networks**: `em0` LAN/CTF infra on `192.168.10.0/24`
  and `ue1` Player-Wi-Fi on `10.10.32.0/22`. Stale VLAN interfaces
  (`vlan01`–`vlan05`) remain configured but unused.
- **Server outbound internet through OPNsense was never restored.** DNS
  resolved locally and pings answered, but server egress through the router
  stayed broken (WAN/NAT/rule path). Rather than keep fighting the router,
  the Swarm was **re-homed to `192.168.1.0/24`**, where it could pull images
  and operate. The CTF platform itself became the priority; the original
  "servers egress through OPNsense" goal was sacrificed to get the event live.
- No aggressive QoS/segmentation was added, per the operator's instruction to
  keep the router at baseline with only local server DNS overrides preserved.

## 6. Systems / services intentionally sacrificed

| Sacrificed | Reason |
| :--- | :--- |
| Five-VLAN segmented design | Not achievable on the live box in time; two-network layout shipped instead |
| Server WAN egress via OPNsense | Unresolved router path; re-homed Swarm to a working subnet |
| `.12` / `cei-ryzen5-15g-swarm04` | Never joined the Swarm (transport/SSH issues); event ran on 3 nodes |
| OPNsense as CTF egress control point | Served as local DNS/DHCP only for the event |

## 7. Referenced logs

- `WORK_LOGS/2026-08-05_SERVER_LAN_OPNSENSE_CHECK.md` — OPNsense path saga.
- `WORK_LOGS/2026-08-06_SWARM_NEW_SUBNET.md` — re-home to 192.168.1.0/24.
- `WORK_LOGS/2026-08-06_CTFD_RESET_ADMIN_GAMES_USERS.md` — reset, hint-cache
  fix, Workhorse Krypton/Bandit fixes.
