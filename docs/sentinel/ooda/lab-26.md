# Sentinel Lab 26 OODA Record

Scope: Sentinel 26 only. The review uses committed synthetic evidence and has no network, service, or external-tool dependency.

## 1. Observe

The lab evidence contained the final `Disposition: unauthorized` alongside the ARP, DHCP, and zone-policy observations. This bypassed the intended inventory-review reasoning.

Evidence: `targets/sentinel/runtime.py` rendered the disposition directly in `network-inventory.txt`.

## 2. Orient

The answer contract requires a device MAC, engineering zone, and unauthorized disposition. An ARP-observed MAC with no DHCP lease conflicts with the policy that engineering permits only registered DHCP endpoints, so the conclusion remains deterministic without being printed as an answer.

Evidence: `runtime.ANSWERS["sentinel-26"]` and the static ARP/DHCP/policy records.

## 3. Decide

Remove only the direct disposition label, preserve the MAC, zone, DHCP absence, policy, local-only restriction, and exact structured answer contract. Add lab-specific tests for the generator copy and runtime evidence.

Evidence: the change is limited to Sentinel 26 generator text, runtime evidence, dedicated tests, and this record.

## 4. Act

Updated the Lab 26 task and hints to direct the learner through ARP-to-DHCP-to-policy reasoning. Introduced `LAB_26_EVIDENCE` so the evidence is explicit and testable, without a disposition field.

Evidence: `scripts/build_sentinel.py`, `targets/sentinel/runtime.py`, `scripts/test_sentinel_26.py`, and `targets/sentinel/test_lab_26.py`.

## 5. Verify

Focused offline tests verify the generator’s local-only instructions, the absence of a direct disposition in evidence, and exact account-bound acceptance of the valid tuple with rejection of an altered disposition.

Evidence: `python3 -m unittest scripts.test_sentinel_26` and `python3 -m unittest test_lab_26.py`.
