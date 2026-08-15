# Security Lab Intake Backlog

This backlog records 21 proposed labs for future CEI Labs tracks. It is an
intake and prioritization artifact, not approval to build, deploy, or operate
any named tool. A proposal enters implementation only after its owner supplies
an original scenario, deterministic fixtures, a reset contract, three hints,
an instructor writeup, and tests.

## Non-Negotiable Boundaries

- Use only isolated, per-team targets and synthetic artifacts. No venue,
  internet, public repository, production account, wireless spectrum, or other
  participant system may be scanned, modified, or contacted.
- Never collect real credentials, deploy a rogue access point, establish a
  persistent C2 channel, execute arbitrary server-side code, or expose a real
  secret. Model these concepts with inert fixtures and bounded validators.
- Flags must be generated or validated per team. Manual-review exercises need a
  separate, auditable submission workflow before they can become scored.
- Tool availability, license, offline installability, and image provenance are
  verification gates. Tool names in the source handoff are leads, not approved
  dependencies or verified Kali package names.
- New tracks remain non-staged until Engine supports their mappings, release
  controls, and scoreboard contracts. Do not add a wave merely to label a
  difficulty tier.

## Recommended Delivery Order

Start with artifact-only and deterministic labs. They support offline delivery,
repeatable grading, and the existing Sentinel direction without adding an
unreviewed attack surface.

| Priority | Proposal | Safe CEI Labs form | Gate before build |
| --- | --- | --- | --- |
| P0 | Phishing email dissection | Static synthetic RFC-822 message and header-analysis validator. | Original sample, offline parser, no live mail. |
| P0 | Traffic anomaly detection | Fixed synthetic PCAP with one documented anomaly. | PCAP provenance, deterministic answer test. |
| P0 | Metadata forensics | Original image/PDF fixture with non-sensitive metadata. | License, fixture checksum, offline extractor. |
| P0 | DNS exfiltration detector | Static DNS-query corpus with an encoded training token. | No live DNS; bounded decoder test. |
| P0 | Detection-as-code pipeline | Local fixture runner that evaluates a rule against fixed logs. | No CI service or SIEM dependency; deterministic job record. |
| P0 | GRC assessment | Structured synthetic organization evidence and rubric, not manual scoring. | Machine-checkable report schema and unique outcome. |
| P1 | FIM investigation | Synthetic before/after file manifest and event record. | No endpoint agent or dashboard required. |
| P1 | Rogue-device discovery | Fixed ARP/DHCP inventory with one unauthorized synthetic device. | No network scan or discovery traffic. |
| P1 | OSINT secret scanner | Local intentionally fake credential corpus and scanner output. | No public-repository access; nonfunctional values only. |
| P1 | Automated reconnaissance | Static HTML snapshot corpus; identify a mock administration surface. | No Selenium crawl or live URLs. |
| P1 | Least-privilege IAM design | Policy document evaluated by a local authorization simulator. | No cloud account or IAM API. |
| P1 | IR tabletop | Structured incident timeline and machine-validated response playbook. | Rubric and evidence schema; no manual flag. |
| P2 | Wazuh onboarding | Simulated manager enrollment transcript and agent-key lifecycle. | Verify license, image, and offline fixture strategy. |
| P2 | AI alert triage | Deterministic local summarizer fixture with disclosed limitations. | No external LLM, Grafana, or opaque answer. |
| P2 | Wordlist generation | Static fictional company site corpus and frequency calculation. | No crawler or public web target. |
| P2 | Prompt injection | Local toy assistant with a bounded mock system context. | No production model or hidden real secret. |
| P2 | WAF/XSS concept | Local inert rendering model that reports a marker, never browser script execution. | No bypass payload or production WAF. |
| Deferred | Captive portal | Training-only UI mock showing a fabricated credential event. | Explicit ethics review; no AP, deauth, or credential capture. |
| Deferred | C2 persistence | Event-log/evidence analysis of a simulated agent lifecycle. | No implant, persistence, beacon, or remote control. |
| Deferred | SSTI/RCE | Parser/emulator exercise with fixed virtual artifacts. | No interpreter, filesystem read, or command execution. |
| Deferred | AI exploitation/CVE task | Offline vulnerability-triage record with fictional CVE-style identifier. | No exploit execution, live vulnerability, or real disclosure. |

## Track Mapping

The proposed concepts fit the existing and planned curriculum better than a
separate offensive track:

| Track | Candidate labs | Delivery state |
| --- | --- | --- |
| Sentinel | Email, PCAP, DNS, FIM, detection-as-code, GRC, IAM, tabletop. | Intake candidates; align with the approved Sentinel design before implementation. |
| Natas | Prompt-injection and inert web-parser concepts only. | Requires a dedicated clean-room design review; do not extend the freshly merged 0-34 range ad hoc. |
| Future analysis track | Metadata, static web corpus, fake-secret scanning, word frequency. | Needs a track charter, target model, and Engine integration contract. |
| Deferred simulations | Captive portal, C2, SSTI/RCE, exploit/CVE concepts. | Safety/design review required before backlog promotion. |

## Required Implementation Packet

Every promoted row must add:

1. Original scenario description and learning objective.
2. Team-scoped flag contract with no real credential or secret.
3. Offline fixture manifest, provenance, checksum, and reset behavior.
4. Positive solve, negative isolation, and deterministic grading tests.
5. Participant description and hints, plus instructor `writeups.md`,
   `learning-objectives.md`, and `cheatsheet.md` material.
6. Exact generated metadata accepted by `validate_generated.py`; immutable image
   references for release builds.
7. Engine mapping and stage decision. Wave labels are optional event pacing, not
   a replacement for a tested stage-control contract.

## Decisions Needed

- Select the first P0 lab to prototype: phishing headers, PCAP analysis,
  metadata forensics, DNS analysis, or detection-as-code.
- Confirm whether Sentinel owns the P0/P1 defensive and GRC set, or whether a
  new analysis track is preferred.
- Approve a machine-validated format for GRC and tabletop submissions before
  claiming they are scoreable.
- Verify any future dependency against its official source, package license,
  offline installation path, and immutable image digest before it is named in
  a build plan.
