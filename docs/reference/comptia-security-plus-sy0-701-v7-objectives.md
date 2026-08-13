# CompTIA Security+ SY0-701 V7 Coverage Map

## Source record

| Field | Record |
| --- | --- |
| Official source | [CompTIA exam objectives](https://www.comptia.org/training/resources/exam-objectives) |
| Document | CompTIA Security+ SY0-701 Exam Objectives |
| Document version | 7.0 |
| Published copyright year | 2023 |
| Repository retrieval date | Not recorded. Record the UTC access date and the official PDF URL before relying on a newly retrieved copy. |
| File checksum | Not recorded. Do not invent one; calculate it for the exact retained PDF with `sha256sum <file>` and record the filename, SHA-256 value, and retrieval date together. |

This project-owned coverage map is a high-level planning aid, not a copy or
substitute for CompTIA's exam objectives. It does not reproduce objective text,
exam questions, or official weighting. Consult the official source for the
authoritative document. Sentinel is not affiliated with or endorsed by CompTIA.

## High-level domain coverage

| Domain | Sentinel coverage themes |
| --- | --- |
| 1.0 General Security Concepts | Security controls, foundational principles, controlled change, and cryptographic evidence. |
| 2.0 Threats, Vulnerabilities, and Mitigations | Attack-surface reasoning, malicious-activity evidence, vulnerability triage, and mitigations. |
| 3.0 Security Architecture | Segmentation, infrastructure design, data protection, resilience, and recovery evidence. |
| 4.0 Security Operations | Baselines, asset and vulnerability workflows, monitoring, secure changes, identity lifecycle, automation, incident response, and investigation data. |
| 5.0 Security Program Management and Oversight | Governance artifacts, risk decisions, third-party assurance, compliance, assessment, and awareness scenarios. |

## Sentinel alignment boundaries

- Objective identifiers in Sentinel documents are internal alignment labels, not
  a claim of complete coverage or exam preparation.
- Labs use original fictional evidence and scenarios. They do not reproduce
  official objective wording or commercial training content.
- Detailed coverage claims stay at the summary level and are limited to the
  learner action and evidence defined in the lab design matrix.

## 4.7 Automation and orchestration coverage for Lab 16

Lab 16 uses automation only as a bounded secure-change workflow. It covers
reviewing an approved change, applying one restricted and idempotent action,
recording the result, validating the expected post-state, and using a defined
backout path.

| Area | Lab 16 coverage |
| --- | --- |
| Use cases | Controlled service configuration, access-control, or firewall changes in a static fixture or isolated private namespace. |
| Benefits | Repeatability, reduced manual error, consistent evidence, and faster validation of an approved change. |
| Limits | Automation does not replace authorization, review, testing, monitoring, or rollback judgment. The helper accepts no arbitrary commands or paths and cannot alter host state. |
