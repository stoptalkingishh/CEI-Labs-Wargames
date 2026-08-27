# Sentinel Tooling and Scenario Research

## Decision summary

Sentinel should begin with a small, offline-capable toolchain rather than a
full SIEM or enterprise range. The core tools are already compatible with a
lightweight Linux SSH target and cover the practical evidence work that best
fits this wargame format:

| Priority | Tool | License | Why it is in scope |
| --- | --- | --- | --- |
| P0 | OpenSSH | BSD-style | Connection method plus secure access, keys, authentication, authorization, and hardening evidence. |
| P0 | OpenSSL | Apache-2.0 | Certificates, hashes, signatures, encryption, key formats, and TLS inspection. |
| P1 | tcpdump/libpcap | BSD-style | Deterministic, offline PCAP evidence analysis without privileged live capture. |
| P2 | Suricata | GPL-2.0 | Offline IDS/alert-triage and EVE JSON exercises using pinned PCAPs and rules. |

This is the recommended toolchain for the pilot and initial full track. It is
small enough to run per team, uses CLI workflows that work through SSH, and
does not require internet access, feeds, cloud accounts, or a GUI.

## Tool matrix

| Tool | Objectives best supported | Lightweight scenario | Constraints and decision |
| --- | --- | --- | --- |
| OpenSSH | 1.2, 1.4, 2.5, 3.2, 4.1, 4.6, 4.7, 4.8 | Inspect auth logs, keys, `sshd_config`, groups, ACLs, and restricted access; identify and correct a contained configuration finding. | Core. Bind only to the lab network. Disable forwarding and host-escape paths; learners have no Docker socket, host mounts, privileged capabilities, or unrestricted `sudo`. |
| OpenSSL | 1.4, 3.3, 4.1, 4.6, 4.8 | Verify a signed artifact, inspect an internal certificate chain, find unsafe private-key permissions, or validate a CSR/renewal record. | Core. Ship generated test CA material only; pin fixtures and never accept learner-supplied or production keys. |
| tcpdump/libpcap | 2.2, 2.4, 3.2, 4.4, 4.5, 4.8, 4.9 | Read a supplied PCAP to investigate scanning, DNS anomalies, SSH password spraying, or staged data transfer. | Core after the SSH/crypto foundation. Prefer `tcpdump -r` to a supplied file; do not grant capture capability or use public targets. |
| Suricata | 2.2, 2.4, 2.5, 4.4, 4.5, 4.8, 4.9 | Run a pinned rule set over a supplied PCAP, inspect EVE JSON, distinguish a true alert from noise, and propose a narrow detection improvement. | Add only after PCAP scenarios are stable. Run offline only, with no rule-feed download; retain GPL-2.0 notice and review any distribution changes. |
| osquery | 4.1, 4.2, 4.6 | Compare installed packages, processes, services, users, and listening ports to an approved inventory. | Useful optional extension. It is lightweight and cross-platform, but static inventory fixtures plus native commands are sufficient for the first release. |
| Lynis | 2.5, 4.1, 4.2 | Review a local hardening report, fix one bounded finding, and rescan. | Optional Linux-only supplement. Useful for baseline work, but should not become a blind-remediation exercise. |
| AIDE | 1.4, 4.4, 4.5, 4.9 | Compare a protected-file baseline to the current state and document an authorized versus suspicious change. | Optional low-footprint FIM lab. Secure the baseline database and use synthetic files. |
| `auditd` | 2.4, 4.4, 4.6, 4.9 | Investigate privileged-command, authentication, or sensitive-file-access evidence. | Optional Linux-only telemetry. Add only with narrowly scoped, low-noise rules. |
| `nftables` | 2.5, 3.2, 4.5 | Read a host firewall policy, identify an unsafe rule, and validate intended management-only access. | Optional. Better fit than an appliance for a single-host lab; never give learners `CAP_NET_ADMIN` on the host namespace. |
| restic | 3.4, 4.1, 5.2 | Verify encrypted backup metadata and retention, then restore a known file into a clean training location. | Optional, low-footprint resilience lab; use only local repositories and synthetic data. |
| Wazuh | 4.1, 4.3, 4.4, 4.5, 4.8, 4.9 | Central endpoint alerts, FIM, configuration assessment, and correlated incident triage. | Deferred. GPL-2.0 and broad coverage, but manager/indexer/dashboard operations are too heavy for the per-team core. Consider a shared later lab only. |
| Velociraptor | 4.8, 4.9 | Scoped endpoint collection and artifact-based incident triage. | Deferred advanced/shared lab. AGPL-3.0 and powerful collection capabilities require tight authorization and release review. |
| Greenbone Community Edition | 2.3, 4.3 | Scan, prioritize, remediate, rescan, and report against isolated targets. | Deferred. The scanner/feed/database stack is too heavy for the initial deterministic environment. |
| OpenSCAP/ComplianceAsCode | 4.1, 4.3, 5.4 | Assess a Linux profile and interpret tailored compliance findings. | Deferred Linux-only extension. It is useful but benchmark interpretation should follow foundational labs. |

## Do not use as initial dependencies

| Tool or platform | Reason |
| --- | --- |
| Nmap | Widely used for training, but its NPSL is source-available rather than OSI-approved open source. It is excluded from the strict open-source baseline. Static scan outputs can teach the required reasoning. |
| Security Onion, Elastic, Splunk Attack Range, DetectionLab | Valuable references but too resource-heavy and operationally complex for an SSH-first per-team track. DetectionLab is also no longer actively maintained. |
| Kali, Metasploitable, Metasploit, password-cracking tools | Their exploit-first framing is not the primary Security+ defensive learning path. Use controlled evidence rather than requiring offensive tooling. |
| Sysmon for Windows | High-value telemetry but proprietary/freeware, not open source. Do not bundle or redistribute it. |
| Windows containers | Require a Windows host/kernel, have compatibility constraints, lack a desktop, and are not a realistic endpoint-administration lab. |

## Static evidence is a first-class lab component

Software should not be added merely to cover an objective. The following are
best represented by versioned, synthetic, checksum-verified artifacts:

| Objective areas | Artifact types |
| --- | --- |
| 1.1-1.3 | Control-selection cards, system diagrams, change request, approval/test/rollback records, and version-control diffs. |
| 2.1, 2.3, 2.5 | Threat-actor narrative, mock CVE/advisory, affected-asset inventory, compensating-control decision, and remediation report. |
| 3.1, 3.4 | Architecture diagrams, responsibility matrix, backup/restore evidence, RTO/RPO scenario, and tabletop inject. |
| 4.2, 4.3, 4.7 | Asset records, software bill of materials, scan results, exception record, reviewed automation/runbook, and failure-handling evidence. |
| 5.1-5.6 | Policy/standard/procedure/RACI package, risk register, BIA, vendor questionnaire, agreement excerpts, audit evidence, attestation, and phishing/reporting scenario. |

Artifacts must use fictional organizations, internal addresses, synthetic
credentials, and fixed timestamps. Raw PCAP/log evidence should remain
available alongside normalized JSON or worksheets so learners investigate the
source evidence rather than only a preprocessed answer.

## Copyleft image dependency review gate

Before adding a GPL, AGPL, or other copyleft component to a distributed
Sentinel image, record an actionable release review. This is an engineering
release gate, not legal advice.

| Check | Required record before image publication |
| --- | --- |
| Dependency identity | Component name, version or immutable source revision, upstream license file, package source, and whether it is merely used, modified, or redistributed in the image. |
| Notices and source | Preserve required copyright/license notices; identify the corresponding source location and any modified source, patches, build scripts, and source-offer mechanism required by the applicable license. |
| Network obligations | For AGPL components, identify whether the deployed use exposes network interaction and route the release to license-owner review before service availability or distribution. |
| Image artifacts | Generate or update the image SBOM; place required notices and source/offer references in the image documentation or accompanying release artifact, where a recipient can obtain them. |
| Approval | A designated license owner records the review outcome, distribution scope, notice/source location, and any release conditions before publishing the image. |

Suricata, Wazuh, and Velociraptor remain subject to this gate if adopted. A
tool's inclusion in this research document is not approval to distribute it.

## Scenario patterns used by training platforms

Public material from blue-team and cyber-range platforms commonly uses
evidence-driven scenarios rather than tool tutorials. The recurring patterns
that fit Sentinel are:

- Authentication triage: failed and successful SSH/RDP/VPN logins, password
  spraying, lockouts, concurrent sessions, and anomalous access.
- Endpoint persistence: cron/systemd tasks, shell profiles, authorized keys,
  new users, or service configuration changes.
- Web and network investigation: suspicious requests, DNS/HTTP/TLS metadata,
  scanning, unusual outbound traffic, and IDS alerts.
- Vulnerability and configuration response: validate an advisory against
  system evidence, decide priority, apply or verify a narrow remediation, and
  document an exception where appropriate.
- Incident response: build a timeline, scope affected assets, preserve
  evidence, choose containment, and write a concise remediation/debrief.
- Detection validation: use a supplied benign/malicious fixture set to test a
  simple rule or query and explain false-positive tradeoffs.

Sentinel should adopt those patterns but create original scenarios, evidence,
and solutions. It must not copy content from commercial training platforms.

## Linux and Windows scope

### Initial Linux-first delivery

The core track remains per-team Linux over SSH. It can teach monitoring,
inventory, access control, FIM, vulnerability workflow, PKI, recovery,
incident handling, and governance without a Windows runtime.

### Windows evidence phase

Add sanitized, project-owned EVTX fixtures and a maintained open-source parser
such as `libevtx` for Windows log interpretation. This provides Windows
authentication, process, service, PowerShell, and persistence investigations
without a Windows VM. Preserve raw EVTX plus documented source scenario and
fixture provenance.

### Windows runtime phase

Only if demand warrants it, provide a resettable, isolated Windows evaluation
VM shared by an active cohort, not one VM per team. Use official Microsoft
evaluation media under its terms and do not redistribute an image. A Linux
hosted Wazuh or Velociraptor service may then collect a small amount of native
Windows telemetry. Keep the Windows network isolated and expose only the
intended gateway and telemetry paths.

## Adoption sequence

1. **Foundation:** OpenSSH plus static artifacts for all governance/risk/
   process objectives.
2. **Cryptography:** OpenSSL with pinned certificates, keys, hash manifests,
   ciphertext, and expected outputs.
3. **Evidence analysis:** offline PCAP/log bundles read through `tcpdump`.
4. **Detection:** offline Suricata PCAP processing with a local rule set.
5. **Optional host controls:** osquery, Lynis, AIDE, `auditd`, `nftables`, or
   restic only when a specific lab needs its unique behavior.
6. **Shared advanced services:** Wazuh, Velociraptor, Greenbone, and Windows
   runtime only after resource, isolation, and maintenance gates are met.

## Source notes

- [OpenSSH manuals](https://www.openssh.com/manual.html) and
  [license](https://github.com/openssh/openssh-portable/blob/master/LICENCE)
- [OpenSSL license](https://github.com/openssl/openssl/blob/master/LICENSE.txt)
- [tcpdump manual](https://www.tcpdump.org/manpages/tcpdump.1.html) and
  [license](https://github.com/the-tcpdump-group/tcpdump/blob/master/LICENSE)
- [Suricata documentation](https://docs.suricata.io/en/latest/) and
  [license](https://github.com/OISF/suricata/blob/main/COPYING)
- [Wazuh](https://github.com/wazuh/wazuh),
  [Velociraptor](https://github.com/Velocidex/velociraptor), and
  [osquery](https://github.com/osquery/osquery)
- [Security Onion](https://github.com/Security-Onion-Solutions/securityonion),
  [DetectionLab](https://github.com/clong/DetectionLab),
  [Sigma](https://github.com/SigmaHQ/sigma),
  [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team), and
  [OTRF Security Datasets](https://github.com/OTRF/Security-Datasets)
- [Microsoft Windows containers overview](https://learn.microsoft.com/virtualization/windowscontainers/about/)
  and [Sysinternals license terms](https://learn.microsoft.com/sysinternals/license-terms)
