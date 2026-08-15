# Sentinel Lab 27 OODA Record

## 1. Observe

The Lab 27 fixture, answer contract, and learner metadata record each identify
`field-notes.pdf` and its SHA-256 value. The fixture is a committed static PDF
with an `/Author (Northstar Training)` metadata field.

Evidence: `sha256sum targets/sentinel/fixtures/field-notes.pdf` returned
`dc3014d5c2f708b7e4628082170c3c0385afbd6dd8d84f1aff0eca6d8abe7710`.

## 2. Orient

Lab 27 is explicitly offline and bounded. A copied checksum in the runtime
answer and evidence could drift when the committed fixture changes, leaving a
learner unable to reproduce the expected value locally.

Evidence: `runtime.py` previously contained the digest separately in both the
Lab 27 answer and the rendered metadata evidence.

## 3. Decide

Derive the Lab 27 SHA-256 from the committed local fixture at runtime, retain
the fixed author contract, and expose the local `sha256sum` verification step.
This is deterministic, requires no network access, and does not alter another
lab or a platform contract.

Evidence: the fixture is included at `/opt/sentinel/fixtures/field-notes.pdf`
by the existing Sentinel image definition.

## 4. Act

Added fixture-derived Lab 27 checksum constants and a metadata-evidence
renderer, clarified the Lab 27 hint and writeup with the local checksum command,
and added a dedicated Lab 27 contract test module.

Evidence: `targets/sentinel/test_lab_27.py` verifies fixture digest, author,
offline evidence text, accepted submission, and rejected altered digest.

## 5. Verify

Run the dedicated Lab 27 tests and the focused Sentinel builder and runtime
contract tests.

Evidence: `python3 -m unittest test_lab_27.py test_runtime_contract.py` from
`targets/sentinel` passed 19 tests. `python3 -m unittest
scripts.test_build_sentinel` from the repository root passed 4 tests.
