# Sentinel Lab 24 OODA Record

## Observe

The lab used one static local file and required endpoint ID, enrollment status,
and key status. The inventory, transcript, and key lifecycle statements did not
share a value a learner could use to demonstrate that they described the same
enrollment event.

## Orient

Lab 24 is a non-staged, offline exercise. A static enrollment record ID can
make the corroboration requirement explicit without contacting an endpoint,
agent, manager, or other external system.

## Decide

Add `enrollment_record_id` to the exact runtime answer and repeat the fixed
value in the three local evidence sections. Keep the existing endpoint ID and
status fields unchanged, and cover the contract with lab-specific tests.

## Act

Updated only the Lab 24 generator definition and hints, its runtime answer and
evidence, focused tests, and this lab-specific record. The evidence now joins
the inventory entry, accepted transcript, and active key lifecycle record with
`ENR-24-042`.

## Verify

Ran `python3 -m unittest scripts/test_build_sentinel.py` before the change and
after the change: 5 tests passed. Ran `python3 -m unittest
test_lab24_contract.py test_runtime_contract.py` from `targets/sentinel`: 18
tests passed. The lab-specific tests confirm exact-answer enforcement, all three
static record correlations, and no live endpoint URL.
