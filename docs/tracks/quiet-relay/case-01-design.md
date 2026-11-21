# Quiet Relay Case 01 — The Maintenance Window

Companion to the [track proposal](README.md). This is a maintainer design with synthetic ground truth. Future participant downloads must contain only the briefing and designated evidence files.

## Player briefing

Meridian Desk has been asked to review a late alert at Harbor Exchange. The event occurred during an approved maintenance window. Bracken Transit and Relay Office both appear in records associated with the same service endpoint. Determine which device was involved, what the service actually accepted, and how much the evidence says about who was responsible. Submit a timeline and one request for the next evidence you would collect.

## Incident timeline

Use a single fictional incident date, 2026-05-12. All rows below use UTC.

| Time | Event | Evidence |
| --- | --- | --- |
| 09:00 | An approved certificate check begins. Its scope covers health checks only. | CHG-01 |
| 09:08 | A health check receives a successful response. | FLOW-01, PROXY-01 |
| 09:12 | DHCP releases the address formerly assigned to QA-03. | LEASE-01 |
| 09:14 | The same address is assigned to WS-17. | LEASE-02 |
| 09:16:20 | WS-17 resolves the fictional relay service and opens a connection. | CAP-01, DNS-01, FLOW-02 |
| 09:17:10 | A request is denied. | PROXY-02, AUDIT-01 |
| 09:18:40 | The application records an accepted session. This documents a session, with transfer status unresolved. | PROXY-03, AUDIT-02 |
| 09:24 | The SOC correlates the session with the change scope and escalates it for review. | SOC-01 |

The application clock is 90 seconds fast. AUDIT-02 displays 09:20:10; CLOCK-01 records the measured offset. Correlate application and proxy events with a shared request ID. Define lease intervals as start-inclusive and end-exclusive. Keep the device, service account and human operator as distinct entities.

## Evidence inventory

| File | Contents and design intent |
| --- | --- |
| manifest.json | File hashes, stable evidence IDs, sensor descriptions and coverage. QR-01 can compare two labeled bundles using the published manifest. |
| harbor.pcap | CAP-01 with ordinary synthetic DNS and connection establishment, plus a benign control flow. Use reserved example addresses and domains. |
| leases.csv | LEASE-01 and LEASE-02 with explicit validity windows and a separate decoy lease. |
| dns.csv and flows.csv | Timestamped DNS and flow records for cross-checking the packet capture. Use an endpoint identifier shared with the provider registry. |
| proxy.csv and application.jsonl | Health check, denied request and accepted session. Use distinct event codes, deterministic join keys and inert event records. |
| clocks.txt | Sensor clock calibration, including sign convention and measurement time. |
| provider-registry.csv and cargo-ledger.csv | Archived fictional records show that both organizations use the same provider and that Bracken Transit handled Harbor Exchange shipment S-104. Include a similarly named organization with a distinct registry ID. |
| change-ticket.md and soc-review.json | Authorized maintenance scope and the analyst's escalation record, including the timestamp and reason. |
| evidence-coverage.md | Shows which sources cover the window and identifies unavailable endpoint sign-in and transfer records. |

Treat all registry and cargo entries as fictional snapshots. Package the source URLs or attribution metadata separately if an existing OSINT asset is later approved for reuse.

## First playable slice

| Exercise | Expected result | Scoring checks |
| --- | --- | --- |
| QR-02 / 100 pts | WS-17 and LEASE-02 | Both fields must agree. Reject QA-03, LEASE-01 and matches outside the lease interval. |
| QR-05 / 150 pts | Shared provider ID PROV-07 and the Bracken-to-Harbor shipment relationship, supported by S-104 | Accept documented aliases for entity names where needed. Require the registry and shipment identifiers. |
| QR-07 / 250 pts | Correct order and UTC time for denial, accepted session and escalation. Identify shared hosting as supported, operator identity as unresolved, and endpoint sign-in audit as the next evidence request. | Use structured fields for the scored submission. Accept equivalent timestamps with explicit offsets. Reject uncorrected application time, a claimed transfer and attribution based on shared hosting alone. |

For QR-07, add a short unscored analyst note for explaining confidence and remaining gaps. Ship the relevant files with each challenge so teams can recover from a missed earlier solve. Offer progressive hints that point to evidence locations, then join keys and clock direction.

## Playtest and implementation checklist

1. Generate the files from a fixed case definition and check that IDs, hashes, timestamps and lease windows agree across exports.
2. Play the slice offline in Wireshark and a plain text or CSV viewer. Target 35–50 minutes for a first-time learner with hints available.
3. Have two reviewers independently identify the device, reconstruct the corrected timeline, evaluate what the accepted session establishes and document remaining gaps.
4. Verify the public bundle excludes this design, verifier configuration and answer keys. Exercise scoring against alternate timestamp formats, wrong evidence references and the named false leads.
5. Confirm the Engine typed-answer plugin supports the fields needed for the slice. Start with separately scored fields if multi-field validation needs additional work. Rehearse the hidden import on a disposable CTFd instance.

After the slice, add QR-01 for intake, QR-03 for deeper DNS and flow joins, QR-04 for interpreting web evidence, and QR-06 for linking alert disposition to the change ticket. An optional OSINT image provenance exercise can introduce an independent evidence source once the main case has passed playtesting.
