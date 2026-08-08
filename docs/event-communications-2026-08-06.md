# Event Communications Recap — 2026-08-06 CEI Labs Wargames

Full chronological log of the `CEI-LABS` relay channel conversation that drove
the event (200 messages, 2026-08-05 through 2026-08-08). Thread root:
`f086884e…cacda`.

## Phase 1 — Server LAN Discovery & OPNsense Diagnostics (Aug 5, ~14:00–19:00 UTC)

The event began with server LAN discovery. stoptalkingishh directed Codex 5.5
to access the OPNsense router (`192.168.10.1`) and discovered four Fedora
server candidates on `192.168.10.0/24` (`.235`, `.112`, `.192`, `.67`). Codex
5.5 verified they were pingable but SSH ports were unreachable from the agent
sandbox. Fizz discovered existing stale single-node Swarms on `.13` and `.11`
advertising dead `192.168.1.x` addresses, and noted server outbound internet
through OPNsense was non-functional.

Codex 5.6 Luna was brought in to diagnose the OPNsense WAN path — `ue0` (Lenovo
USB-C Ethernet) reported `no carrier`, leaving the server LAN without internet
egress. The team investigated OPNsense Wi-Fi as an alternative WAN (iwm0
interface). Multiple rounds of OPNsense web GUI configuration were attempted
but the upstream connection was never successfully established.

- Outcome: operator asked to make OPNsense "just work normally with the internet
  it has," then to revert it toward baseline except local server DNS.
- Codex 5.5 / Luna did read-only checks but were repeatedly blocked — the
  workstation couldn't reach OPNsense GUI/SSH from inside the sandbox. Outside
  the sandbox, `.13:22`, OPNsense `:443`, and external `:443` all opened.
- Swarm was already 3-node Ready/Active and the CEI stack was healthy.
- No QoS/firewall redesign was added; only local server DNS overrides were
  preserved. The router path was effectively deferred — the platform would be
  re-homed instead.

## Phase 2 — Server Provisioning & Swarm Formation (Aug 5, ~19:00–23:30 UTC)

stoptalkingishh provided Fedora credentials (`ismaelrodriguez/Alpha4n/a`) after
noting the login was consistent across all boxes. Servers were renamed by
processor/RAM convention:

| IP | Hostname | Spec |
|----|----------|------|
| `192.168.10.13` | `cei-ryzen5-61g-swarm01` | AMD Ryzen 5, 61 GiB |
| `192.168.10.11` | `cei-i7-31g-swarm02` | Intel Core i7, 31 GiB |
| `192.168.10.192` | `cei-xeon-e3-8g-swarm03` | Intel Xeon E3, 8 GiB |
| `192.168.10.112` | `cei-ryzen5-15g-swarm04` | AMD Ryzen 5, 15 GiB |

A 2-node Swarm was formed on `.13` (manager) and `.11` (worker) per the CEI
engine spec. Nodes `.10` (swarm03) and `.12` (swarm04) needed Docker
installation. Static IPs were applied, MTU 1400 was set for Wi-Fi WAN
compatibility, and stale Wi-Fi routes were disabled.

## Phase 3 — OPNsense Wi-Fi WAN Attempts (Aug 5, ~21:00–23:00 UTC)

Codex 5.6 Luna configured OPNsense to use iwm0 as a Wi-Fi WAN client
(infrastructure/BSS mode, SSID "Smallwood Hall", WPA2-PSK). The device was
assigned as WAN but the SSID/WPA configuration fields were not present in the
OPNsense version's WAN configuration page — the wireless clone needed
credential configuration at the device level, not the interface level. The WAN
remained in `no carrier` state.

## Phase 4 — Agent-driven CTF playthrough (2026-08-06 15:37–16:09 UTC)

Operator asked to "play the CTF as 10 separate sub-agents," registering users
1–10 on one shared team, cost-effectively, sharing found keys.

Codex 5.5 found sub-agents couldn't reach the private LAN target, so it ran it
locally: created `cei-player-1`…`10` on `CEI-Agent-Team`, launched environments
via the CTFd launch API, and solved via real SSH/web/API. **24 accepted
submissions** first pass; recovered keys shared on the team.

## Phase 5 — Subnet Re-home & New Swarm (Aug 6, ~12:30–15:00 UTC)

After exhausting OPNsense fixes, the critical decision was made to **re-home the
Swarm from `192.168.10.0/24` to `192.168.1.0/24`** where upstream internet was
functional. Fizz executed the migration:

- Swarm recreated on `192.168.1.0/24`: manager `.150`, workers `.193`, `.125`
- Fixed stale advertise address — re-initialized with `--advertise-addr
  192.168.1.150`
- Redeployed CEI stack from `/home/ismaelrodriguez/deployments/engine-31a6471`,
  updated `ORCHESTRATOR_OFFLINE_HOST` to `.150`
- Recovered from CTFd DB password mismatch using a temporary MariaDB rescue
  container
- Verified all 3 nodes Ready/Active

## Phase 6 — CTFd Reset, Game Rollout & Player Support (Aug 6, ~15:00–17:20 UTC)

Fizz executed the full event reset:

- Backup taken at `/home/ismaelrodriguez/ctfd-backup-20260806-090853.sql.gz`
- Admin password reset to `CEI-Labs-Admin2026!`
- Games staged: only Bandit (35) + AI Copilot (6) set visible
- All 28 non-admin users and teams deleted, solves and submissions cleared
- Fixed hint display cache bug (409 errors from wiped
  `hint_wallet_catalog_cache`) — rebuilt from the orchestrator catalog; hints
  returned
- Krypton unlocked next (8 challenges visible), then Natas (16 visible) when
  the operator asked to "open the last game." All four games ended active.

Player support issues:
- Workhorse (team 22) Krypton instance had never been created — Docker overlay
  network race caused silent failure. Recreated via orchestrator API, re-synced
  flag secrets for challenges 36–42, verified end-to-end over SSH.
- It went down again after a relaunch — same root cause. Recreated with a clean
  non-relaunch create; verified the full Krypton flag chain.
- Bandit per-team passwords had rotated by a relaunch. Fizz set the resume
  point to `bandit19 / bandit19` on port 32002, level-20 target in place.

## Phase 7 — Documentation & Post-Mortem (Aug 6-8, 19:00–17:40 UTC)

Operator requested a comprehensive event recap PR covering all issues, the
current network state, how many played, how challenges were done, all channel
communications, what was sacrificed (network), and Claude + ChatGPT
conversations for CEI-Labs-relevant items.

Multiple agents coordinated:

- **Honey**: Opened PR #62 on CEI-Labs-Wargames with challenge playthrough,
  participation, pre-event PR history
- **Fizz**: Pulled live server resource usage + CTFd score backup from the
  Swarm, pushed missing WORK_LOGS to the event repo
- **Bumble**: Verified event docs, fixed gap where WORK_LOGS were branch-only
  (opened and merged PR #63)
- **Opencode_DeepSeek**: Opened communications recap (redirected to event repo)

Operator directive (Aug 8, 17:50 UTC): all post-event documentation goes in
**CEI-Labs-Wargames** only. All documentation merged to main on the event repo.
Single remaining gap: Claude/ChatGPT conversation recap (no export files on
disk).

## Key decisions

- Keep the router at baseline (no QoS/segmentation), only local server DNS
  preserved.
- Re-home the Swarm to `192.168.1.0/24` rather than continue fighting server
  WAN egress through OPNsense.
- Run the playthrough locally (agents can't reach the private LAN) instead of
  10 live sub-agents.
- Reset the platform to a clean start with staged unlocks, then open Krypton
  and Natas on request.
- All post-event documentation lives only in CEI-Labs-Wargames event repo.