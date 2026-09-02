# Sentinel Writeups

Instructor material for the non-staged Sentinel pilot. Real submissions are
per-team values generated at runtime; never distribute a team's result. Labs
06-21 remain planned. Labs 22-27 are non-staged, offline expansion material and
are not a release commitment or progression replacement for the planned labs.

## Start Here

Connect as `sentinel0` with password `sentinel0`, then read
`~/evidence/ENGAGEMENT-RULES.txt`. Submit the documented JSON to
`sentinel-submit`.

## 01 Asset Census

Continue as `sentinel0` after the Start Here result. Read
`~/evidence/asset-census.txt`; independently compare the recorded package, service,
and ownership fields if desired. Submit the exact evidence tuple to
`sentinel-submit`; its output is the next password.

## 02 Control Review

Connect as `sentinel1`, read `~/evidence/controls.md` and
`~/evidence/control-evidence.md`, and
submit the documented `mfa`, `badge_review`, and `log_review` classification
tuple to `sentinel-submit`.

## 22 Phishing Header Analysis

Connect as `sentinel22`, read `~/evidence/phishing-message.eml`, and submit the
from-domain, return-path-domain, and DMARC tuple. This synthetic RFC-822 message
is static local evidence; do not contact mail systems or services.

## 23 Detection Rule Validation

Connect as `sentinel23`, review `~/evidence/detection-rule.yml`,
`~/evidence/detection-corpus.log`, and `~/evidence/decision-record.txt`, then
submit the rule ID, match count, and decision tuple. Do not query a live
detection service.

## 24 Endpoint Enrollment Evidence

Connect as `sentinel24`, review `~/evidence/endpoint-enrollment.txt`, and submit
the endpoint ID, enrollment-status, and key-status tuple. Do not contact an
endpoint, agent, or manager.

## 25 Alert Triage Summary

Connect as `sentinel25`, review `~/evidence/alert-triage-summary.txt`, and submit
the alert ID, root cause, and disposition tuple. The summary is deterministic
local evidence; do not use an external AI service or contact systems.

## 26 Network Inventory Review

Connect as `sentinel26`, review `~/evidence/network-inventory.txt`, and submit
the device MAC, zone, and disposition tuple. Do not scan or probe a network.

## 27 Evidence Metadata Review

Connect as `sentinel27`, review `~/evidence/evidence-metadata.txt`, and submit
the filename, checksum, and extracted-author tuple. Do not upload, transmit, or
externally enrich the fixture.

## 03 Change Window

Connect as `sentinel2`, read `~/evidence/change-window.txt`, and identify the missing
change-owner approval. The safe decision is to defer the change. Submit the
documented `disposition` and `missing_evidence` tuple to `sentinel-submit`.

## 04 Certificate Trail

Connect as `sentinel3`, inspect the committed test CA, `~/evidence/service.pem`,
`~/evidence/training-ca.crl`, `~/evidence/service.key`, and
`~/evidence/certificate-ledger.txt`. Run the
ledger's fixed-time offline OpenSSL command and inspect the private-key mode.
Submit the exact evidence tuple to `sentinel-submit`.

## 05 Attack Surface

Connect as `sentinel4`, run `ss -lnt`, and compare it with
`~/evidence/exposure-review.conf`. SSH is the only listener; the legacy metrics service
is disabled. Submit the documented `listener`, `port`, and `legacy_metrics`
tuple to `sentinel-submit`.
