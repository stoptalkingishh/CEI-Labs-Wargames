# Sentinel Lab 25 OODA Record

## 1. Observe

The Lab 25 definition described a deterministic local summary and fixed source evidence, but the runtime emitted only `alert-triage-summary.txt`. Evidence: `scripts/build_sentinel.py` and `targets/sentinel/runtime.py` at the branch baseline.

## 2. Orient

The expected answer identifies an expired VPN certificate, so a static certificate inventory with a record identifier and expiry timestamp is sufficient to corroborate the summary without external systems or nondeterministic inputs. Evidence: `runtime.ANSWERS["sentinel-25"]` and the existing local-only lab boundary.

## 3. Decide

Add one read-only Lab 25 evidence file, require both files in the generator task and final hint, and retain the existing exact structured answer. Evidence: the change is limited to the Lab 25 generator entry and hint, Lab 25 runtime evidence, dedicated test, and this lab-specific record.

## 4. Act

Added `vpn-certificate-inventory.txt` for `sentinel25`, correlated it to alert `ALT-2048` and record `VPN-GW-01`, and made its expiry precede the fixed alert window. Evidence: `targets/sentinel/runtime.py` and `scripts/build_sentinel.py`.

## 5. Verify

The dedicated test verifies generated task copy, emitted correlated static evidence, offline boundaries, and the unchanged exact answer. Evidence: `python3 -m unittest discover -s targets/sentinel -p 'test_lab25_alert_triage.py' -v` passed 2 tests, and `python3 -m unittest scripts.test_build_sentinel -v` passed 4 tests.
