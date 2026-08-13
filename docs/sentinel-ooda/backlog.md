# Sentinel OODA Implementation Backlog

## Shared first

- Implement a reusable structured-answer validator that gates a dynamic
  credential on evidence fields, not a hidden string location.
- Define fixture provenance/checksum schema and content-invariant test helper.
- Define lab-specific three-hint/debrief template and mutation-helper contract.
- Re-run PR #68 runtime validation before any stage integration.

## Batch 1

- Lab 06: UTC log corpus, one raw-log workflow, monitoring implication, and
  account/source/window validator; omit `ausearch` initially.
- Lab 07: version/backport semantics, risk rubric, vulnerability type, and
  finding/priority/response/validation validator.
- Lab 08: choose analysis-only or restricted correction before account/ACL
  fixture, helper, reset, and cross-account tests are authored.

## Batch 2

- Lab 09: architecture/zone model, ordered policy fixture, and structured
  unsafe-flow/safer-path validator; remain static.
- Lab 10: policy-versioned records with scoped valid controls and per-record
  response validator; keep OpenSSL out initially.
- Lab 11: consistent BIA/manifest/drill set and readiness validator; add
  restic only after static review is solid.

## Batch 3

- Labs 12, 13, 15, 16: implement provenance, reproducible paths, structured
  assessment, and helper lifecycle tests listed in the ledger.
- Lab 14: complete blocker redesign before any target implementation.

## Batches 4-5

- Labs 17-18: define containment/handoff decision schemas, raw-evidence
  boundaries, and immutable-corpus tests.
- Labs 19-20: implement revision/input manifests and structured governance/
  risk decisions.
- Lab 21: complete blocker redesign, remove 2.1 mapping, and use a single
  vendor-centered evidence-to-decision model.
