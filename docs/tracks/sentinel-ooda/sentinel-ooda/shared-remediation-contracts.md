# Sentinel Shared Remediation Contracts

## Scope and status

This document defines contracts for future Sentinel lab implementations. It
does not implement a validator, create fixtures, run PR #68, or authorize
staging or release. Implementations must remain offline-only and must satisfy
the applicable lab contract in the design matrix.

## Structured evidence-answer validator

Each scored lab that releases a dynamic credential must declare an answer
contract before target implementation. The target accepts one structured
submission and releases the credential only when every required field is
valid. A flag or credential must not be discoverable solely by locating a
file, matching a string, or supplying one correct field.

Required contract fields:

| Field | Requirement |
| --- | --- |
| `schema_version` | Versioned identifier for the lab answer schema. |
| `lab_id` | Canonical Sentinel lab identifier. |
| `evidence` | Named evidence references and the learner-observed values used in the conclusion. |
| `conclusion` | The lab-specific decision or classification. |
| `rationale` | Evidence-to-conclusion explanation constrained to the lab's declared criteria. |

Each lab additionally declares its required evidence keys, permitted values or
formats, normalization rules, and the exact conclusion criteria. The validator
must reject missing, extra where disallowed, malformed, contradictory, and
evidence-inconsistent fields. Its response must not disclose expected values,
ground truth, or which individual field failed. Incorrect submissions do not
change target state or reveal the credential. Contract tests must cover one
valid submission and the applicable missing, malformed, alternate-conclusion,
and evidence-mismatch cases.

## Fixture provenance and checksum manifest

Every lab fixture set must include a machine-readable provenance manifest,
kept outside learner-visible evidence when it would expose ground truth. The
manifest uses this schema:

| Field | Requirement |
| --- | --- |
| `schema_version` | Version of this manifest schema. |
| `lab_id` | Canonical Sentinel lab identifier. |
| `fixture_set_id` | Stable fixture-set name and revision. |
| `fictional_organization` | Declared fictional organization or case identity. |
| `generated_at_utc` | Fixed ISO 8601 UTC build timestamp. |
| `artifacts` | List of artifact records. |
| `source_consistency` | Shared case identifiers and any permitted cross-artifact relationships. |

Each `artifacts` record includes `path`, `media_type`, `revision`,
`observed_at_utc` when relevant, and `sha256` for binary evidence. Text
artifacts may also be checksummed when this improves integrity verification;
their timestamps and identifiers must still be deterministic. Content-invariant
tests must verify required artifacts, declared checksums, fixed timestamps, and
the identifier relationships used by the learner path. Learner-facing evidence
contains no real data, mutable external feed, hidden label, instructor
timeline, or ground-truth answer unless the lab explicitly assesses it.

## Lab-specific hint and debrief template

Each lab supplies exactly three managed, lab-specific hints and an instructor
debrief. Hints describe the allowed investigation without supplying a required
conclusion or copying an answer value.

| Item | Required content |
| --- | --- |
| Hint 1: locate | Where and how to locate the relevant raw evidence. |
| Hint 2: interpret | The lab-specific relationship, criterion, or comparison to evaluate. |
| Hint 3: act or validate | The permitted command, structured response, or bounded action and its verification. |
| Debrief | Objective, intended evidence path, expected evidence-to-decision reasoning, safe operational takeaway, and common incorrect interpretation. |

Hints and debriefs must name the lab's actual artifacts and decision criteria.
Free lab descriptions may orient the learner but must not disclose tier-two or
tier-three reasoning. The learner-facing debrief is released only according to
the lab's completion policy; instructor material may include the ground truth.

## Mutation-helper contract

A lab uses a mutation helper only when a live action uniquely reinforces its
objective. The helper has one declared purpose and an allowlist of fixed
operations, inputs, paths, and resulting state. It accepts no arbitrary
command, shell fragment, option passthrough, or path. It runs with the least
required privilege, records an action log without secrets, and makes no network
request or host-global change.

The contract declares preconditions, exact permitted mutation, postcondition,
backout operation, reset procedure, authorized caller, and refusal behavior.
The action and backout must be idempotent. Tests must prove the normal action,
repeat action, backout, reset, shell-escape rejection, arbitrary-path rejection,
unauthorized-caller rejection, and absence of unrelated state changes.

## PR #68 runtime-verification checklist

Before any staging or platform integration of the PR #68 pilot, a reviewer
with access to its branch must record the branch/commit and execute or inspect
the following checks against the built artifact:

- Generator completes from a clean build and produces the documented target artifacts.
- Target contract, including intended users, files, permissions, and challenge progression, matches its lab documentation.
- Docker build and container startup complete without undeclared network dependencies.
- Only the intended SSH listener is reachable; no unintended service is exposed.
- Startup fails closed when required dynamic-secret inputs are absent or invalid.
- Dynamic secrets are scrubbed before SSH is available and are not exposed in process environment, logs, or unintended files.
- Restart behavior is deterministic for the declared team and does not leak or rotate credentials contrary to the contract.
- Intended credentials work only for the intended account; neighboring and unauthorized accounts are denied.
- The checks above preserve target isolation and leave no staged or released environment as a side effect.

Record commands, result, artifact or container identifier, and any exception
for every checklist item. A missing result, failed check, or unreviewed branch
keeps PR #68 non-staged; this checklist is not evidence that the checks have
already passed.
