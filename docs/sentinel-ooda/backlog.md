# Sentinel OODA Implementation Backlog

## Shared first

- Implement a reusable structured-answer validator that gates a dynamic
  credential on evidence fields, not a hidden string location.
- Define fixture provenance/checksum schema and content-invariant test helper.
- Define lab-specific three-hint/debrief template and mutation-helper contract.
- Re-run PR #68 runtime validation before any stage integration.

## Batch 1

- Lab 06: accepted contract specifies a UTC/provenance manifest, the sole
  `/var/lib/sentinel/lab06/raw/auth.log` workflow, monitoring implication, and
  account/source/window structured validator; omit `ausearch` initially.
- Lab 07: accepted contract specifies vulnerability classification,
  epoch/version/release and backport semantics, deterministic risk rubric, and
  finding/priority/response/validation structured validator.
- Lab 08: accepted analysis-only contract specifies an effective-access table,
  sole evidence path, structured finding/correction-state assessment, and no
  `sudo`, root, cross-account access, or mutation helper.

## Batch 2

- Lab 09: architecture/zone model, ordered policy fixture, and structured
  unsafe-flow/safer-path validator; remain static.
- Lab 10: policy-versioned records with scoped valid controls and per-record
  response validator; keep OpenSSL out initially.
- Lab 11: consistent BIA/manifest/drill set and readiness validator; add
  restic only after static review is solid.

## Batch 3

- Lab 12: provenance/context manifest, diagnose-before-helper assessment gate,
  and restricted-helper idempotence/reset/escape tests.
- Lab 13: integrity-evidence provenance, explicit hash-to-owner-to-change-record
  comparison order, classification/response assessment, and pinned hash and
  evidence timestamps.
- Labs 15-16: implement provenance, reproducible paths, structured assessment,
  and helper lifecycle tests listed in the ledger.
- Lab 14: complete blocker redesign before any target implementation.

## Batches 4-5

- Labs 17-18: define containment/handoff decision schemas, raw-evidence
  boundaries, and immutable-corpus tests.
- Labs 19-20: implement revision/input manifests and structured governance/
  risk decisions.
- Lab 21: complete blocker redesign, remove 2.1 mapping, and use a single
  vendor-centered evidence-to-decision model.

## Superseding design decisions

- Lab 14's blocker redesign is defined: author inert tombstoned offboarding
  evidence and a structured documentary-gap/follow-up assessment. Target
  implementation must prove that no residual usable account, credential,
  private key, or authorized-key entry exists.
- Lab 21's blocker redesign is defined: author one vendor-assurance renewal
  case with citations and decisions for retained 5.3-5.6 criteria, followed by
  one renewal decision. Do not restore 2.1 or the phishing scenario, and do
  not add a challenge.
