# Sentinel Lab 26 OODA Record

## 1. Observe

The Lab 26 definition promised an inventory review, but the runtime rendered
the final `Disposition: unauthorized` directly in `network-inventory.txt`
alongside the ARP, DHCP, and zone-policy observations, so the learner never had
to derive the disposition.

Evidence: `targets/sentinel/runtime.py` emitted the disposition line in the
`write("sentinel26", ...)` call at the branch baseline.

## 2. Orient

The expected answer identifies one ARP-observed MAC, the engineering zone, and
an unauthorized disposition. The engineering zone permits only registered DHCP
endpoints, and the same MAC has no DHCP lease, so the conclusion is
deterministic from committed static evidence without being printed as the
answer.

Evidence: `runtime.ANSWERS["sentinel-26"]` and the static ARP, DHCP, and
network-zone policy records.

## 3. Decide

Remove only the direct disposition label, preserve the MAC, observed zone,
missing DHCP registration, zone policy, local-only restriction, and exact
structured answer contract, and add dedicated generator and runtime tests.

Evidence: the change is limited to the Lab 26 generator entry and hint, Lab 26
runtime evidence, dedicated tests, and this lab-specific document.

## 4. Act

Added the `LAB_26_EVIDENCE` constant so the evidence is explicit and testable
without a disposition field, and updated the Lab 26 task and hints to require
ARP-to-DHCP-to-policy reasoning.

Evidence: `targets/sentinel/runtime.py` and `scripts/build_sentinel.py`.

## 5. Verify

The dedicated tests verify generated task and hint copy, the absence of a
direct disposition in the evidence, the unchanged exact answer, and
account-bound acceptance of the valid tuple with rejection of an altered
disposition.

Evidence: `python3 -m unittest test_sentinel_26 test_build_sentinel` from
`scripts` passed 5 tests, and `python3 -m unittest test_lab_26
test_runtime_contract` from `targets/sentinel` passed 18 tests.
