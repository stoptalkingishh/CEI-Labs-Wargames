# Sentinel Lab 23 OODA Evidence

## 1. Observe

Lab 23 supplied one matching PowerShell record and a decision record reporting one match. The corpus had no non-matching control record, so the documented result did not demonstrate evaluation across a bounded corpus.

Evidence: `targets/sentinel/runtime.py` defined one Lab 23 corpus line containing `-EncodedCommand`; `scripts/build_sentinel.py` directed learners to the static local evidence only.

## 2. Orient

The lab is a non-staged, offline exercise. The safest scoped improvement is evidence-only: retain the rule ID, submission tuple, and account contract while adding a deterministic non-match that permits direct comparison of the fixed condition to both records.

Evidence: Lab 23 uses the existing `sentinel23` account and `{"rule_id": "NS-DET-104", "matches": 1, "decision": "triggered"}` answer contract.

## 3. Decide

Add exactly one benign PowerShell command to the committed corpus, state both the corpus size and match/non-match result in the decision record, and add a dedicated unit test that verifies the rule, corpus count, match count, answer, and offline boundary.

Evidence: the change is limited to Lab 23 generator copy, Lab 23 runtime evidence, a dedicated Lab 23 test, and this lab-specific document.

## 4. Act

Defined named deterministic Lab 23 evidence constants, added the `-NoProfile -Command Get-Date` non-match, recorded `Corpus records: 2`, and updated the first hint to require comparison against each corpus record. Added `targets/sentinel/test_lab_23_contract.py`.

Evidence: `LAB_23_RULE`, `LAB_23_CORPUS`, and `LAB_23_DECISION_RECORD` are rendered only into `sentinel23`'s local evidence directory.

## 5. Verify

`python3 -m unittest test_lab_23_contract.py` from `targets/sentinel` passed 3 tests. `python3 -m unittest scripts.test_build_sentinel` from the repository root passed 4 tests. `python3 -m unittest test_runtime_contract.py` from `targets/sentinel` passed 16 tests. `git diff --check` completed with no output.

Evidence: the dedicated test proves two corpus records produce exactly one fixed-condition match, the decision record reports that result, and the evidence contains no HTTP(S) endpoint.
