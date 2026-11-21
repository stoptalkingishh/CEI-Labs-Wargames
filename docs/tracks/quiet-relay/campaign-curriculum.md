# Quiet Relay campaign curriculum

Players are Meridian Desk cyber researchers investigating a fictional incident at Harbor Exchange. The campaign moves from identifying a device, to establishing an organizational relationship, to assessing impact. Each conclusion requires a primary record and independent corroboration. This is an instructor planning document with spoilers.

## Arc 1 — The Maintenance Window

**Skills.** Filter a PCAP for DNS and connection establishment. Join a source address to the DHCP lease valid at the packet timestamp. Normalize timestamps to UTC, apply a documented sensor offset and correlate proxy and application events by request ID.

**Story.** An incident summary points toward a QA workstation during approved maintenance. Researchers receive the evidence from [Case 01](case-01-design.md) and reconstruct the activity.

**Twist.** The IP address was reassigned just before the suspicious connection. The summary attached the former lease to the event. After correcting the application clock, the team can also distinguish the approved health check from a later accepted session outside the ticket's scope.

**Proof of mastery.** Submit device ID, lease record, corrected event time and request ID. The fair clues are the end-exclusive lease interval, an ordinary DHCP change, and the clock calibration note. Score device identity separately from any claim about the operator.

## Arc 2 — The Shared Address

**Skills.** Distinguish correlation in DNS, TLS certificate metadata and IP records from evidence of ownership. Resolve similar organization names using stable registry IDs and effective dates. Cross-check movement records against independent cargo and vendor records.

**Story.** A shared endpoint appears to connect Bracken Transit with Relay Office. Researchers build an evidence graph with separate edges for hosting, ownership and shipments.

**Twist.** The apparent direct link comes from shared hosting. A dated subcontractor amendment, corroborated by a cargo record, reveals the stronger relationship another way: Relay Office handled one Bracken shipment through a separate registered subsidiary. The amendment and cargo ledger share a subcontract ID, while their display names differ.

**Proof of mastery.** Submit the shared provider ID and the independently supported shipment relationship with both source IDs. Include one unsupported claim in a bounded response field so the scoring tests whether players understand what their findings justify. Provide the dated registry snapshot and amendment before the reveal.

## Arc 3 — The Missing Receipt

**Skills.** Interpret flow direction and byte counts at a documented observation point. Correlate application events, transfer job IDs and storage audit records. Recognize gaps in sensor coverage and distinguish observed activity, confirmed impact and unresolved identity. Deliver an evidence-backed incident handoff.

**Story.** Incident leadership reads the accepted session and a large flow as evidence that a manifest left the exchange. Players review a second evidence drop with per-direction counters, job receipts and a SOC shift handoff.

**Twist.** The large flow was a legitimate inbound catalog refresh, tied to its own job ID. The suspicious session did initiate a separate export job, but its matching receipt shows the job was rejected before a file was written. Earlier sensors lacked that visibility. The available records establish the attempted export and its failure on the observed service, while actor identity and activity outside sensor coverage remain open.

**Proof of mastery.** Submit the legitimate and suspicious job IDs, evidence for direction and disposition, a corrected incident timeline and the next evidence request. Accept a short unscored confidence note. Put the observation-point diagram, receipt semantics and logging coverage in the player bundle so the twist follows from evidence.

## Progression and assessment

| Arc | New work | Target time |
| --- | --- | --- |
| 1 | Use QR-01 through QR-04 as the packet and timeline foundation. | 35–50 min |
| 2 | Expand QR-05 into shared infrastructure and records corroboration. | 30–45 min |
| 3 | Expand QR-06 and QR-07 into response review and impact assessment. | 35–50 min |

Each arc starts with a guided evidence lookup, moves to a cross-source join, and ends with a conclusion that revises a plausible initial interpretation. Reveal twists through the scored evidence claims. Offer hints in order: source location, join field, then interpretation cue. Provide an evidence recap at each arc boundary so a missed solve does not block the next skill.

Build the three-exercise Case 01 prototype first. Its QR-05 exercises the basic corroboration method and its QR-07 is a short handoff rehearsal. In the full campaign the final scored handoff comes after Arc 3. Keep story connections in original fictional records and all network evidence in static synthetic files. During playtesting, give reviewers only the player bundles and verify that they can explain each twist with evidence available before the reveal. Record alternative defensible interpretations and fix ambiguous fixtures before tuning difficulty.
