---
title: "Server LAN OPNsense Connectivity Check"
tags: [opnsense, server-lan, networking, incident]
status: active
created: 2026-08-05
---

# Findings

- Workstation Ethernet: `192.168.10.120/24`.
- Default gateway, DHCP server, and DNS server: `192.168.10.1`.
- ARP resolves `192.168.10.1` to `e8-6a-64-41-68-54`, so the gateway is visible at Layer 2.
- ARP also resolves the server candidates `192.168.10.192` and `192.168.10.235`.
- TCP connection attempts to OPNsense management ports 80 and 443 fail immediately from this workstation.
- PowerShell network inventory cmdlets are restricted in this session; `ipconfig /all` and `arp -a` supplied the usable evidence.

# Current state

Read-only SSH diagnostics succeeded on both Fedora servers using the previously reported server credentials:

- `192.168.10.192` (`fedora`) and `192.168.10.235` (`host`) both have the expected `/24` address and default route via `192.168.10.1`.
- Both servers can ping `192.168.10.1`.
- Both servers receive `Destination Host Unreachable` from `192.168.10.1` when pinging IPv4 `1.1.1.1`.
- `getent hosts example.com` returns IPv6 records, but this does not demonstrate working IPv4 WAN access.

This isolates the incident to the OPNsense upstream path (WAN gateway, IPv4 route, or outbound NAT/firewall), not the Fedora server LAN addressing. No firewall, DHCP, DNS, or routing change was made. Repair is blocked pending valid OPNsense GUI credentials or console access.

# Console recovery checklist

From the OPNsense console, verify interfaces and gateway status first. Then check that the LAN interface is assigned `192.168.10.1/24`, DHCP is enabled for the intended server-LAN range, and the web GUI is listening on LAN. Confirm the LAN rule permits management from `192.168.10.120` and that no floating/block rule overrides it. After saving, renew the workstation lease and test `https://192.168.10.1`.

# 2026-08-05 21:22 UTC Fedora server reachability refresh

User reported all servers should now be online and listed local Fedora candidates:

- `192.168.10.235`
- `192.168.10.112`
- `192.168.10.192`
- `192.168.10.67`

Read-only reachability checks from this workstation:

- All four hosts responded to ping and name resolution:
  - `192.168.10.235` -> `host.local`
  - `192.168.10.112` -> `fedora.local`
  - `192.168.10.192` -> `fedora-2.local`
  - `192.168.10.67` -> `fedora3.local`
- TCP checks failed on all four hosts for ports `22`, `2222`, `2200`, `80`, `443`, `2377`, `7946`, and `4789`.

Conclusion: hosts are present on the LAN, but remote administration and Docker Swarm ports are not reachable from this workstation. No hostname or Swarm changes were made.

# 2026-08-05 21:34 UTC Swarm setup request

User requested Docker Swarm setup with proper documentation and delegated
static server IPs plus server internet repair to Luna.

Actions taken from this workstation:

- Re-read the local engine/net Swarm docs and inventory.
- Retested the four reported Fedora server IPs:
  - `192.168.10.235` (`host.local`)
  - `192.168.10.112` (`fedora.local`)
  - `192.168.10.192` (`fedora-2.local`)
  - `192.168.10.67` (`fedora3.local`)
- All four still answered ping, but ports `22`, `2222`, `2200`, `2377`,
  `7946`, `4789`, `80`, and `443` were closed from the operator workstation.
- Updated local repo documentation to reflect the four-host intended Fedora
  pool, keep `192.168.10.120` excluded, and require static addressing,
  outbound IPv4 internet, SSH reachability, CPU/RAM/OS inventory, and hostname
  assignment before Swarm deployment.

No live Fedora changes were made because SSH is still unreachable from the
deployment workstation.

# 2026-08-05 21:55 UTC Fedora credential SSH attempts

User requested attempting SSH with the supplied Fedora credentials.

Bounded SSH results:

- `192.168.10.11` (`host`) accepts the first supplied Fedora password.
  - Fedora Linux 44.
  - Intel Core i7-10750H, 6 cores / 12 threads.
  - 31 GiB RAM.
  - Docker 29.7.1 installed.
  - Docker Swarm is already active as a one-node manager, but its node/manager
    address is stale: `192.168.1.98`, not the current `192.168.10.11`.
  - Existing `cei-labs` stack is present with five services; `ctfd-db` was
    `0/1` during inspection.
  - IPv4 internet still fails via OPNsense: `1.1.1.1` returns Destination Host
    Unreachable from `192.168.10.1`.
- `192.168.10.13` (`fedora3`) accepts the second supplied Fedora password.
  - Fedora Linux 44.
  - AMD Ryzen 5 7600, 6 cores / 12 threads.
  - 61 GiB RAM.
  - Docker 29.6.2 installed.
  - Docker Swarm is already active as a separate one-node manager, but its
    node/manager address is stale: `192.168.1.173`, not the current
    `192.168.10.13`.
  - IPv4 internet still fails via OPNsense: `1.1.1.1` returns Destination Host
    Unreachable from `192.168.10.1`.
- `192.168.10.192` (`fedora`) accepts the first supplied Fedora password.
  - Fedora Linux 44.
  - Intel Xeon E3-1240 v2, 4 cores / 8 threads.
  - 7.7 GiB RAM.
  - Docker is not installed.
  - Password sudo works, but package installation is blocked until server
    outbound internet is restored.
- `192.168.10.112` refuses SSH connections.
- `192.168.10.10` and `192.168.10.12` are not reachable yet.

No Swarm reset/join was performed. Rebuilding the live Swarm will require
choosing which current one-node manager is authoritative, then force-leaving
or reinitializing stale Swarm state with current `192.168.10.x` advertise
addresses. That is disruptive to existing containers/services and should be
done deliberately.

# 2026-08-05 22:03 UTC Fedora station renames

User requested renaming all stations. Applied hostnames to the three
SSH-reachable Fedora stations using the established processor/RAM naming rule:

- `192.168.10.13`: `fedora3` -> `cei-ryzen5-61g-swarm01`
  - AMD Ryzen 5 7600, 61 GiB RAM.
- `192.168.10.11`: `host` -> `cei-i7-31g-swarm02`
  - Intel Core i7-10750H, 31 GiB RAM.
- `192.168.10.192`: `fedora` -> `cei-xeon-e3-8g-swarm03`
  - Intel Xeon E3-1240 v2, 7.7 GiB RAM.

Verification: `hostnamectl --static` and `hostname` returned the new hostname
on all three hosts.

Not renamed:

- `192.168.10.112` still refuses SSH.
- Proposed `192.168.10.10` and `192.168.10.12` static targets are not
  reachable from the operator workstation.

Repo docs updated locally to reflect the verified names and current remaining
blockers.

# 2026-08-05 22:17 UTC SSH recheck

User requested another SSH check. At this point the deployment workstation no
longer had an active route/interface on `192.168.10.0/24`.

Evidence:

- `route print -4` showed the active default route as `10.1.10.1` via
  `10.1.10.129`.
- No `192.168.10.120` route/interface was present in the active IPv4 route
  table.
- `ping.exe` to `192.168.10.1`, `192.168.10.11`, and `192.168.10.13` timed
  out.
- Short TCP/22 checks to `.10`, `.11`, `.12`, `.13`, `.112`, and `.192` all
  timed out.

Conclusion: SSH could not be validated because this workstation is no longer
attached to the server LAN path. Reconnect the deployment workstation to the
`192.168.10.0/24` LAN or add a working route/VPN path before retrying SSH.

# 2026-08-05 22:26 UTC SSH restored and fourth station renamed

User requested another SSH attempt. The deployment workstation had regained
the `192.168.10.120/24` route and could ping `192.168.10.1`.

SSH results:

- `192.168.10.13`, `192.168.10.11`, and `192.168.10.192` accepted SSH and
  returned the previously renamed hostnames.
- `192.168.10.112` now accepted SSH with the first supplied Fedora password.

Inventory for `192.168.10.112`:

- Fedora Linux 44.
- AMD Ryzen 5 1600X, 6 cores / 12 threads.
- 15 GiB RAM.
- Interface `enp25s0` at `192.168.10.112/24`.
- Docker not installed.

Applied hostname:

- `192.168.10.112`: `fedora` -> `cei-ryzen5-15g-swarm04`

Verification: `hostnamectl --static` and `hostname` returned
`cei-ryzen5-15g-swarm04`.

# 2026-08-05 22:39 UTC SSH verification after user status check

User asked whether all SSH access is working now.

Network baseline:

- Deployment workstation is on `192.168.10.120/24`.
- Default route includes `192.168.10.1`.
- Ping succeeds to `192.168.10.1`, `.11`, `.13`, `.112`, and `.192`.

Direct SSH verification with the supplied Fedora credentials:

- `192.168.10.13` returned `cei-ryzen5-61g-swarm01`.
- `192.168.10.11` returned `cei-i7-31g-swarm02`.
- `192.168.10.192` returned `cei-xeon-e3-8g-swarm03`.
- `192.168.10.112` returned `cei-ryzen5-15g-swarm04`.

Conclusion: SSH is currently working for all four known Fedora stations.

# 2026-08-05 22:53 UTC SSH and IP verification

User asked whether all SSH and IP settings are proper.

Direct SSH to all four Fedora stations succeeded and returned the expected
hostnames:

- `192.168.10.13`: `cei-ryzen5-61g-swarm01`
- `192.168.10.11`: `cei-i7-31g-swarm02`
- `192.168.10.192`: `cei-xeon-e3-8g-swarm03`
- `192.168.10.112`: `cei-ryzen5-15g-swarm04`

IP/default-route findings:

- `192.168.10.13`: `enp6s0` has `192.168.10.13/24` and default route via
  `192.168.10.1`; also has `wlp7s0` connected to `xfinitywifi` with a second
  default route via `172.20.20.1`.
- `192.168.10.11`: `enp3s0` has `192.168.10.11/24` and default route via
  `192.168.10.1`.
- `192.168.10.192`: `eno1` has `192.168.10.192/24`, but default route is a
  DHCP route via `192.168.10.1`.
- `192.168.10.112`: `enp25s0` has `192.168.10.112/24`, but default route is a
  DHCP route via `192.168.10.1`.

Conclusion: SSH is proper on all four. IPs are reachable and on the right
subnet, but not fully locked down: `.192` and `.112` still need static/DHCP
reservation cleanup, and `.13` should have its extra Wi-Fi route disabled for a
deterministic Swarm node.

# 2026-08-06 00:00 UTC Swarm deployment status

User requested latest status while Swarm setup was in progress.

Completed:

- Renewed/reconfigured host IPs:
  - `cei-xeon-e3-8g-swarm03`: moved from `192.168.10.192` to
    `192.168.10.10/24`.
  - `cei-ryzen5-15g-swarm04`: moved from `192.168.10.112` to
    `192.168.10.12/24`.
  - Old `.192` and `.112` stopped answering SSH after the move.
- Set MTU `1400` persistently on all four server-LAN wired NetworkManager
  profiles. This corrected the observed HTTPS hang through the Wi-Fi WAN on
  the 61 GB host.
- Disabled the extra `xfinitywifi` route on `cei-ryzen5-61g-swarm01`.

Current verification:

- `192.168.10.13` / `cei-ryzen5-61g-swarm01`: SSH works, Docker active,
  HTTPS to GHCR works, intended manager host.
- `192.168.10.11` / `cei-i7-31g-swarm02`: SSH works, Docker active, HTTPS to
  GHCR works.
- `192.168.10.10` / `cei-xeon-e3-8g-swarm03`: SSH works, correct static IP and
  MTU, internet ping works, but Docker is not installed/active yet.
- `192.168.10.12` / `cei-ryzen5-15g-swarm04`: did not answer ping or SSH in
  the latest check; old `192.168.10.112` also did not answer.

Swarm status:

- Not rebuilt yet.
- `.13` and `.11` still have separate existing one-node Swarms.
- Docker install on `.10` exceeded the command window and did not leave Docker
  active.
- `.12` became unreachable after the static-IP/install attempt and needs
  console or network recovery before it can join.

# 2026-08-06 00:25 UTC Swarm reset status

User authorized resetting all servers to ensure they can Swarm.

Completed:

- Reset the stale one-node Swarm on `192.168.10.11`.
- Reset/reinitialized `192.168.10.13` as the new Swarm manager using
  `--advertise-addr 192.168.10.13`.
- Labeled `cei-ryzen5-61g-swarm01` with `ctfd-data=true`.
- Joined `192.168.10.11` as a worker.

Current Swarm node list from `192.168.10.13`:

- `cei-ryzen5-61g-swarm01`: Ready, Active, Leader, Docker 29.6.2.
- `cei-i7-31g-swarm02`: Ready, Active worker, Docker 29.7.1.

Current non-joined hosts:

- `192.168.10.10` / `cei-xeon-e3-8g-swarm03`: reachable, Docker still not
  installed/active after package install attempts.
- `192.168.10.12` / `cei-ryzen5-15g-swarm04`: reachable again, but Docker not
  installed/active; a separate `dnf upgrade --refresh` process is currently
  running there and blocks package installation.

Conclusion: Swarm is rebuilt and functional as a two-node Swarm with the 61 GB
host as manager. Full four-node Swarm is pending Docker installation on `.10`
and `.12`.

# 2026-08-06 02:44 UTC OPNsense minimal-internet-settings check

User asked to make OPNsense "just work normally with the internet it has" and
then clarified not to add aggressive QoS or firewall settings. The only setting
class to preserve intentionally is local domain-name resolution to the local
servers.

Read-only workstation state:

- `ipconfig /all` shows the deployment workstation still has Ethernet
  `192.168.10.120/24`, gateway/DHCP/DNS `192.168.10.1`, DNS suffix
  `ctf.internal`.
- The workstation also has an active external virtual switch on
  `172.20.10.2/28` with default gateway `172.20.10.1`.
- `route print -4` shows default routes through both `192.168.10.1` and
  `172.20.10.1`.
- `ping 192.168.10.1` timed out.
- `Test-NetConnection 192.168.10.1 -Port 443` failed.
- `ping 192.168.10.13` returned `Destination host unreachable` from
  `192.168.10.120` and then timed out.

Conclusion: no OPNsense settings were changed. The deployment workstation has
the expected `192.168.10.120` address but currently cannot reach the OPNsense
LAN gateway or Swarm manager, so live router changes and verification are
blocked until the physical/virtual path to `192.168.10.0/24` is restored.

Minimal target once reachable:

- WAN assigned to `iwm0_wlan1`, IPv4 DHCP, normal upstream gateway from DHCP.
- LAN remains `192.168.10.1/24`.
- Outbound NAT remains Automatic/normal for `192.168.10.0/24` through WAN.
- LAN firewall keeps ordinary allow-LAN-to-any behavior; no new QoS or complex
  segmentation rules for this pass.
- DNS keeps local overrides/resolution for the CTF servers under the local
  domain, with upstream DNS forwarding/resolution working through WAN.

# 2026-08-06 02:53 UTC status check after path recovered

User asked for status.

Read-only checks:

- `ping 192.168.10.1`: succeeds, 1 ms. The workstation can reach the OPNsense
  LAN IP again at ICMP level.
- `Test-NetConnection 192.168.10.1 -Port 443`: fails. OPNsense HTTPS
  management is not accepting TCP/443 from this workstation.
- `Test-NetConnection 192.168.10.1 -Port 80`: fails. OPNsense HTTP management
  is not accepting TCP/80 from this workstation.
- `ping 192.168.10.13`: succeeds, 1 ms.
- `Test-NetConnection 192.168.10.13 -Port 22`: fails. The 61 GB Swarm manager
  answers ping but SSH is not accepting TCP/22 from this workstation in this
  check.
- `ping 192.168.10.11`: succeeds.
- `ping 192.168.10.10`: succeeds.
- `ping 192.168.10.12`: times out.

Conclusion: the LAN path is partially restored, but live administration remains
blocked by closed/unreachable management services: OPNsense GUI ports are not
reachable and SSH to the 61 GB manager is not reachable. No OPNsense or server
settings were changed during this status check.

# 2026-08-06 02:55 UTC follow-up status check

User asked for status again.

Read-only checks:

- `Test-NetConnection 192.168.10.1 -Port 443`: still fails.
- `Test-NetConnection 192.168.10.13 -Port 22`: still fails.
- `ping 192.168.10.10`: succeeds.
- `ping 192.168.10.12`: succeeds now; this host is reachable again at ICMP
  level.

Conclusion: all four intended server IPs are now likely present at ICMP level
except this check only directly re-tested `.10` and `.12`; earlier `.11` and
`.13` pings succeeded. Administration is still blocked because OPNsense HTTPS
and SSH to the 61 GB manager are not reachable from this workstation.

# 2026-08-06 02:58 UTC finish-readiness check

User asked to check whether setup can be finished now.

Read-only checks:

- `192.168.10.1` responds to ping.
- OPNsense management ports from this workstation:
  - TCP/443 fails.
  - TCP/80 fails.
  - TCP/22 fails.
- `192.168.10.13` / 61 GB manager responds to ping, but TCP/22 fails.
- `192.168.10.11`, `192.168.10.10`, and `192.168.10.12` SSH TCP/22 checks
  fail.
- `Resolve-DnsName cei-router.ctf.internal` returns local addresses including
  `192.168.10.1`, so local-domain resolution is present.
- `Resolve-DnsName example.com` returns A/AAAA records, so DNS resolution is
  working.
- `Test-NetConnection example.com -Port 443` fails for both IPv4 and IPv6
  targets despite ping succeeding, so outbound TCP/443 is not validated from
  this workstation.
- Tried browser-control path for `https://192.168.10.1/`; no browser session
  was available to this managed agent.

Conclusion: cannot finish from this session yet. The LAN is visible at ICMP
level and DNS is partly working, but every tested admin path is unavailable:
OPNsense GUI/SSH and all Fedora SSH checks fail. No OPNsense or server settings
were changed during this check.

# 2026-08-06 03:06 UTC coordinated finish attempt

User asked Codex 5.5 and Codex 5.6 Luna to assist and finish what is needed.

Important correction: sandboxed TCP tests had produced false failures. The
critical tests were rerun outside the sandbox:

- `Test-NetConnection 192.168.10.1 -Port 443`: succeeds outside sandbox.
- `Test-NetConnection 192.168.10.13 -Port 22`: succeeds outside sandbox.
- `Test-NetConnection example.com -Port 443`: succeeds outside sandbox.

Live Swarm/stack state from `192.168.10.13`:

- Swarm has three Ready/Active nodes:
  - `cei-ryzen5-61g-swarm01` / `192.168.10.13` / manager leader.
  - `cei-i7-31g-swarm02` / `192.168.10.11` / worker.
  - `cei-xeon-e3-8g-swarm03` / `192.168.10.10` / worker.
- CEI stack services are running 1/1:
  - `cei-labs_ctfd`
  - `cei-labs_ctfd-db`
  - `cei-labs_ctfd-redis`
  - `cei-labs_orchestrator`
  - `cei-labs_traefik`
- Traefik publishes `*:80->80/tcp` and `*:443->443/tcp`.
- Workstation TCP checks to `192.168.10.13:80`, `192.168.10.13:443`, and
  `192.168.10.10:80` succeed.

Server access state:

- Non-interactive SSH works to `.13` and `.11`.
- `.10` and `.12` transport is reachable, but non-interactive SSH using the
  current key fails with permission denied when using a task-local known_hosts
  file after static-IP host-key changes.
- `.12` is not in the Swarm node list.

Server route/DNS cleanup:

- `192.168.10.13` had a direct Wi-Fi default route via `wlp7s0` ahead of the
  OPNsense LAN route. This was not the intended "normal through OPNsense"
  behavior.
- Persistently changed `.13` NetworkManager profiles:
  - Wired `enp6s0` profile DNS: `1.1.1.1,192.168.10.1`.
  - Wired `enp6s0` profile search/routing domain: `~ctf.internal`.
  - Wi-Fi `Smallwood Hall` profile: `ipv4.never-default yes`,
    `ipv6.never-default yes`, `ipv4.ignore-auto-dns yes`,
    `ipv6.ignore-auto-dns yes`.
- After reapply, `.13` default route is only `default via 192.168.10.1 dev
  enp6s0`.
- Local DNS still works from `.13`: `cei-router.ctf.internal` resolves to
  local addresses including `192.168.10.1`.

Remaining blocker:

- With `.13` forced through OPNsense, internet egress fails:
  - `ping 1.1.1.1` from `.13`: 100% loss.
  - HTTPS by IP through OPNsense times out.
  - Public DNS lookup through the OPNsense path times out.
- This confirms the remaining issue is OPNsense WAN/gateway/NAT/rules for
  server-LAN egress, not Swarm itself.
- OPNsense SSH is reachable at TCP level, but non-interactive root login fails
  with permission denied. No router credentials/API path was found in local
  notes.

Minimal router-side fix still needed by someone with OPNsense GUI/console:

- WAN `iwm0_wlan1` has a valid IPv4 DHCP lease and an online gateway.
- LAN `192.168.10.0/24` has outbound NAT through that WAN.
- LAN rule allows ordinary outbound IPv4 traffic from `192.168.10.0/24`.
- OPNsense DNS/unbound resolves local `ctf.internal` names and either forwards
  public DNS correctly or lets clients use public DNS.
- Do not add QoS or complex firewall policy in this pass.
