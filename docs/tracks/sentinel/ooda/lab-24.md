# Sentinel Lab 24 OODA Evidence

## 1. Observe

Lab 24 supplied one static local enrollment file and required endpoint ID, enrollment status, and key status. The inventory, transcript, and key lifecycle statements shared no value a learner could use to demonstrate that they described the same enrollment event.

Evidence: `targets/sentinel/runtime.py` rendered a single `endpoint-enrollment.txt` with `Endpoint inventory ID`, `Enrollment transcript`, and `Enrollment key lifecycle` lines and no shared record identifier; `scripts/build_sentinel.py` directed learners to that static local evidence only.

## 2. Orient

The lab is a non-staged, offline exercise. A fixed static enrollment record ID repeated across all three sections makes the corroboration requirement explicit without contacting an endpoint, agent, manager, or other external system.

Evidence: Lab 24 uses the existing `sentinel24` account and `{"endpoint_id": "northstar-lt-042", "enrollment_record_id": "ENR-24-042", "enrollment_status": "enrolled", "key_status": "active"}` answer contract.

## 3. Decide

Add exactly one enrollment record ID to the exact runtime answer and repeat that value in the inventory entry, enrollment transcript, and key lifecycle record. State the cross-record requirement in the generator goal, task, and first hint, and cover the contract with a dedicated Lab 24 test.

Evidence: the change is limited to the Lab 24 generator entry and hint, Lab 24 runtime answer and evidence, the dedicated Lab 24 test, and this lab-specific document.

## 4. Act

Restructured `endpoint-enrollment.txt` into named `Inventory entry`, `Enrollment transcript`, and `Key lifecycle record` sections that each carry `Enrollment record ID: ENR-24-042`, and required the endpoint ID, enrollment record ID, enrollment status, and key status tuple in the generator copy. Added `targets/sentinel/test_lab24_contract.py`.

Evidence: `runtime.ANSWERS["sentinel-24"]` requires `enrollment_record_id`, and the emitted evidence repeats the fixed value exactly three times.

## 5. Verify

`python3 -m unittest test_lab24_contract.py test_runtime_contract.py` from `targets/sentinel` passed 18 tests. `python3 -m unittest scripts.test_build_sentinel` from the repository root passed 5 tests. `git diff --check` completed with no output.

Evidence: the dedicated test proves exact-answer enforcement, the three static record correlations, and that the evidence contains no HTTP(S) endpoint.
