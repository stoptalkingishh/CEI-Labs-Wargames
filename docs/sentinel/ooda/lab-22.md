# Sentinel Lab 22 OODA Record

## Observe

`scripts/build_sentinel.py` defines Lab 22 as an offline task over one static
RFC-822 file. `targets/sentinel/runtime.py` supplies a visible From domain, a
different Return-Path domain, SPF pass for that envelope domain, and DMARC
failure for the visible From domain.

## Orient

The evidence and required tuple were deterministic, but the final managed hint
could be read as treating SPF pass as a sender-identity pass. DMARC alignment is
the intended learning point. The change stays within Lab 22's generator hint,
runtime evidence, dedicated tests, and lab-specific documentation.

## Decide

Clarify that SPF pass for the envelope sender does not establish alignment with
the visible From domain. Name the existing fixed message fixture so a focused
test can parse and verify the answer-evidence relationship without a network or
container dependency.

## Act

Updated only Lab 22's third hint and replaced its inline runtime message with
the deterministic `LAB_22_MESSAGE` fixture. Added generator and runtime tests
that assert the offline boundary, do not expose answer values in hints, verify
the header-derived tuple, and reject wrong-account, wrong-value, and extra-field
submissions.

## Verify

Executed `python3 scripts/test_lab_22.py` successfully: 1 test passed.
Executed `python3 targets/sentinel/test_lab_22.py` successfully: 2 tests
passed. The runtime test's three `invalid structured answer` messages are the
expected wrong-account, wrong-value, and extra-field rejection paths. Both
suites are offline and validate the fixed evidence, exact structured answer,
account binding, and generator copy without contacting a mail system.
