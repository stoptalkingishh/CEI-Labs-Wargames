# Sentinel Lab 22 OODA Record

## 1. Observe

`scripts/build_sentinel.py` defined Lab 22 as an offline task over one static RFC-822 file. `targets/sentinel/runtime.py` supplied a visible From domain, a different Return-Path domain, SPF pass for that envelope domain, and DMARC failure for the visible From domain.

Evidence: the Lab 22 third hint read `Read phishing-message.eml, then submit the from_domain, return_path_domain, and dmarc tuple through sentinel-submit.`

## 2. Orient

The evidence and required tuple were deterministic, but the final managed hint could be read as treating an SPF pass as a sender-identity pass. DMARC alignment is the intended learning point, and the lab is a non-staged, offline exercise. The change stays within Lab 22 generator copy, Lab 22 runtime evidence, dedicated tests, and this lab-specific document.

Evidence: the message reported `spf=pass smtp.mailfrom=invoice-notice.example` and `dmarc=fail header.from=northstar.training`, and the answer contract is `{"from_domain", "return_path_domain", "dmarc"}` bound to the `sentinel22` account.

## 3. Decide

Clarify that an SPF pass for the envelope sender does not establish alignment with the visible From domain, and name the existing fixed message fixture so a focused test can parse the headers and verify the answer-evidence relationship without a network or container dependency.

Evidence: the change is limited to the Lab 22 hint tier, the `LAB_22_MESSAGE` runtime constant, a dedicated Lab 22 generator test, a dedicated Lab 22 runtime test, and this document.

## 4. Act

Rewrote the third hint to state that an SPF pass for the envelope sender does not establish alignment with the visible From domain, and replaced the inline runtime message with the named `LAB_22_MESSAGE` constant. Added `scripts/test_build_sentinel_lab22.py` and `targets/sentinel/test_lab_22.py`.

Evidence: `LAB_22_MESSAGE` is written only into `sentinel22`'s local `phishing-message.eml` evidence file and is asserted byte-for-byte against the rendered evidence by the runtime test.

## 5. Verify

`python3 -m unittest test_build_sentinel_lab22` from `scripts` passed 1 test, and `python3 -m unittest test_build_sentinel` from `scripts` passed 4 tests. `python3 -m unittest test_lab_22 test_lab_27 test_runtime_contract test_lab23_contract test_lab25_alert_triage` from `targets/sentinel` passed 26 tests. `python3 -m unittest discover -s scripts -t scripts` passed 45 tests, and `git diff --check` completed with no output.

Evidence: the generator test asserts the offline boundary and that no answer value leaks into the hints, while the runtime test parses the RFC-822 fixture, confirms each answer field is derived from the headers, and rejects wrong-account, wrong-value, and extra-field submissions. No suite contacts a mail system.
