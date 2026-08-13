# Sentinel Pilot Writeups

Instructor material for the non-staged Sentinel pilot. Real submissions are
per-team values generated at runtime; never distribute a team's result. Levels
06-21 remain planned.

## Start Here

Connect as `sentinel0` with password `sentinel0`, then read
`~/ENGAGEMENT-RULES.txt`. Submit the documented JSON to `sentinel-submit`.

## 01 Asset Census

Connect as `sentinel1` with the Start Here result. Read
`~/asset-census.txt`; independently compare the recorded package, service,
and ownership fields if desired. Submit the exact evidence tuple to
`sentinel-submit`; its output is the next password.

## 02 Control Review

Connect as `sentinel2`, read `controls.md` and `control-evidence.md`, and
classify the stated safeguards. Submit the exact classifications to
`sentinel-submit`.

## 03 Change Window

Connect as `sentinel3`, read `change-window.txt`, and identify the missing
change-owner approval. The safe decision is to defer the change. Submit the
disposition and missing-evidence fields to `sentinel-submit`.

## 04 Certificate Trail

Connect as `sentinel4`, inspect the committed test CA, `service.pem`,
`training-ca.crl`, `service.key`, and `certificate-ledger.txt`. Run the
ledger's fixed-time offline OpenSSL command and inspect the private-key mode.
Submit the exact evidence tuple to `sentinel-submit`.

## 05 Attack Surface

Connect as `sentinel5`, run `ss -lnt`, and compare it with
`exposure-review.conf`. SSH is the only listener; the legacy metrics service
is disabled. Submit the exact exposure tuple to `sentinel-submit`.
