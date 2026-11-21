# Quiet Relay — Network Forensics CTF

Status: proposal. Quiet Relay is a working title.

## Case premise

Players are cyber researchers reviewing a closed incident at a fictional logistics exchange. An approved maintenance window overlaps with anomalous traffic and a delayed SOC escalation. Two organizations appear to share infrastructure, but the evidence could also reflect a common service provider. Players reconstruct what happened, evaluate the defensive response, and report which connections are supported and which remain uncertain.

Use original faction roles: Harbor Exchange (affected operator), Meridian Desk (research team), Bracken Transit (logistics partner), and Relay Office (suspected broker). Threadline supplies the multi-organization discovery-board structure and the slow reveal of a possible connector. Its source lineage includes third-party material. Confirm ownership or permission before proposing any existing faction names, narratives, or assets for inclusion. The OSINT pilot supplies the evidence and scoring model. Its three dossiers are neutral and have no shared storyline.

## Source and reuse index

| Existing material | Reuse in Quiet Relay |
| --- | --- |
| [OSINT pilot](../osint/README.md) and [source lineage](../osint/source-lineage.md) | Adapt public-record/entity corroboration into a company ownership lead and movement corroboration into a shipment timing lead. Image provenance can become an optional lead. Use new fictional records by default. Any existing dossier reuse requires checking the external package, asset rights, and answer exposure. |
| [Threadline story design](../threadline/storyline.md) | Borrow the campaign structure and faction relationships as design patterns. Write new organizations, evidence and briefings. |
| [Sentinel objectives](../sentinel/learning-objectives.md) | Adapt certificate review (04), static detection validation (23), alert triage (25), network inventory (26), and evidence integrity (27) to a single shared incident with fresh answers. |
| [Natas objectives](../natas/learning-objectives.md) | Use prior web and authentication lessons to guide interpretation of fictional proxy and application logs, such as distinguishing a denied request from a confirmed session. |
| [Bandit](../bandit/README.md) and [Krypton](../krypton/README.md) | Treat shell filtering, hashing and encoding literacy as useful foundations for working with evidence. |
| [Security lab intake](../../guides/security-lab-intake.md) | Carry forward synthetic packet-capture provenance, static DNS evidence, deterministic checks and structured forensic handoff. Planned Sentinel labs are design references. |
| [Wargame building playbook](../../guides/wargame-building-playbook.md) | Use the existing track documentation and release workflow as the model for future implementation. |

## Proposed exercises

| ID | New exercise | Player evidence | Scored result |
| --- | --- | --- | --- |
| QR-01 | Evidence intake | Manifest and two capture bundles | Verified bundle ID and capture window |
| QR-02 | Attribute the source | Synthetic PCAP and time-bounded DHCP inventory | Device ID and supporting lease record |
| QR-03 | Follow the network timeline | DNS records, flow summaries and proxy logs | First corroborated connection time in UTC and evidence IDs |
| QR-04 | Separate attempts from outcomes | Proxy and application audit records with benign lookalikes | Confirmed session event and confidence rationale |
| QR-05 | Corroborate organizations | Fictional public registry and cargo movement records | Shared provider and one independently supported organization relationship |
| QR-06 | Assess the defensive response | Alert, rule decision record and change ticket | First actionable alert, supported disposition and visibility gap |
| QR-07 | Submit the forensic handoff | Complete evidence bundle with a corrected clock offset | Ordered timeline, supported relationship, unresolved attribution claim and priority evidence request |

## Build sequence

1. Write the investigator briefing, a private incident timeline, and an evidence register with stable IDs, clock offsets and intentional gaps.
2. Build a vertical slice for QR-02, QR-05 and QR-07. Use a small synthetic capture with ordinary protocol traffic, fictional logs and offline dossier snapshots. Represent suspicious actions through inert audit records. Package public artifacts separately from private answer data.
3. Validate structured answers and UTC normalization. Test accepted aliases, incorrect joins, misleading lookalikes and timezone errors. Have a second reviewer solve from the public bundle and distinguish shared infrastructure from actor attribution.
4. Expand the remaining exercises and add a facilitator guide. Prototype hidden, non-staged CTFd packaging with the Engine typed-answer plugin where compatible. Begin with offline files and local read-only analysis tools, then rehearse import and scoring before organizer release.

The first implementation milestone is one offline case with a PCAP, a corroborating OSINT dossier and a scored handoff. This PR records the proposal and reuse decisions.
