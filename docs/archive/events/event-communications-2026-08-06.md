# Event Communications Recap — 2026-08-06 CEI Labs Wargames

Condensed log of the `CEI-LABS` relay channel conversation that drove the
event, distilled to the decisions and actions that mattered. Thread root:
`f086884e…cacda`.

## Phase 1 — OPNsense / internet fix (2026-08-06 02:41–03:13 UTC)

- Operator asked to make OPNsense "just work normally with the internet it
  has," then to revert it toward baseline except local server DNS.
- **Codex 5.5 / Luna** did read-only checks. Repeatedly blocked: workstation
  couldn't reach OPNsense GUI/SSH and server admin services from inside the
  sandbox. Outside the sandbox, `.13:22`, OPNsense `:443`, and external
  `:443` all opened.
- Swarm was already 3-node Ready/Active and the CEI stack was healthy. `.13`
  was forced through OPNsense; **server internet egress stayed broken**.
- Outcome: no QoS/firewall redesign was added; only local server DNS
  overrides were preserved. The router path was effectively deferred — the
  platform would be re-homed instead (Phase 3).

## Phase 2 — Agent-driven CTF playthrough (2026-08-06 15:37–16:09 UTC)

- Operator asked to "play the CTF as 10 separate sub-agents," registering
  users 1–10 on one shared team, cost-effectively, sharing found keys.
- **Codex 5.5** found sub-agents couldn't reach the private LAN target, so it
  ran it locally: created `cei-player-1`…`10` on `CEI-Agent-Team`, launched
  environments via the CTFd launch API, and solved via real SSH/web/API.
  **24 accepted submissions** first pass; recovered keys shared on the team.

## Phase 3 — Swarm re-home to new subnet (2026-08-06 19:32 UTC)

- Operator: "set up the swarm with the new IP addresses of the servers, main
  `192.168.1.150`, others `.193`, `.125`."
- **Fizz** fixed the stale advertise address, redeployed the stack, updated
  `ORCHESTRATOR_OFFLINE_HOST` to `.150`, and recovered the CTFd DB password
  mismatch via a rescue container. Verified all 3 nodes Ready/Active.

## Phase 4 — Reset, then staged game unlocks

- **Fizz** reset the admin password (`CEI-Labs-Admin2026!`), reset all games
  to start with only **Bandit + AI Copilot** visible, and reset **all user
  accounts** (non-admin users/teams deleted, all solves/submissions/unlocks/
  tokens/team-secrets cleared). DB backup taken first.
- Hints stopped showing — root cause was the reset deleting the hint-wallet
  display cache. Fizz rebuilt it from the orchestrator catalog; hints
  returned.
- **Krypton** unlocked next (8 challenges visible), then **Natas** (16
  visible) when the operator asked to "open the last game." All four games
  ended active.

## Phase 5 — Workhorse (team 22) account/flag issues

- Operator reported Workhorse couldn't use Krypton flags or user logins.
- **Fizz** found team 22's Krypton box had **never been created** (orchestrator
  create failed on a Docker overlay-network race and rolled back). Recreated
  it via the orchestrator API, re-synced flag secrets for challenges 36–42,
  verified end-to-end over SSH.
- It went down again after a relaunch — same root cause. Recreated with a
  clean non-relaunch create; verified the full Krypton flag chain.
- Bandit per-team passwords had rotated from an earlier relaunch. Fizz set
  the resume point to `bandit19 / bandit19` on port 32002, level-20 target in
  place.

## Phase 6 — Event documentation request

- Operator: produce a highly-summarized PR to the event repo covering all
  issues, the current network state, how many played, how challenges were
  done, document all channel communications, connect to the servers/end
  states, note what was sacrificed (network), and pull the last 9 Claude +
  ChatGPT conversations for CEI-Labs-relevant items.
- **Fizz, Opencode_DeepSeek, Bumble, Honey** split the work: Honey (PR body +
  recap), Fizz (live verification + numbers), Opencode_DeepSeek/Bumble
  (Claude/ChatGPT convo recap).

## Key decisions

- Keep the router at baseline (no QoS/segmentation), only local server DNS
  preserved.
- Re-home the Swarm to `192.168.1.0/24` rather than continue fighting server
  WAN egress through OPNsense.
- Run the playthrough locally (agents can't reach the private LAN) instead of
  10 live sub-agents.
- Reset the platform to a clean start with staged unlocks, then open Krypton
  and Natas on request.
