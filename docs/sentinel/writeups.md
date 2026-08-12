# Sentinel Pilot Writeups

Instructor material for the non-staged Sentinel pilot. Real submissions are
per-team values generated at runtime; never distribute a team's result. Levels
06-21 remain planned.

## Start Here

Connect as `sentinel0` with password `sentinel0`, then read
`~/ENGAGEMENT-RULES.txt`. Submit the `onboarding-token` value.

## 01 Asset Census

Connect as `sentinel1` with the Start Here result. Read
`~/asset-census.txt`; independently compare the recorded package, service,
and ownership fields if desired. Submit `census-result`.

## 02 Control Review

Connect as `sentinel2`, read `controls.md` and `control-evidence.md`, and
classify the stated safeguards. Submit `approved-review-result`.

## 03 Change Window

Connect as `sentinel3`, read `change-window.txt`, and identify the missing
change-owner approval. The safe decision is to defer the change. Submit
`recorded-disposition`.

## 04 Certificate Trail

Connect as `sentinel4`, inspect `service.pem` and `certificate-ledger.txt`.
The ledger records the trusted identity after issuer, revocation, and key
permission review. Submit `verified-service-record`.

## 05 Attack Surface

Connect as `sentinel5`, run `ss -lnt`, and compare it with
`exposure-review.conf`. SSH is the only listener; the legacy metrics service
is disabled. Submit `signed-finding`.
