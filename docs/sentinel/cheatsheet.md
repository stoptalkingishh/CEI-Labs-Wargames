# Sentinel Instructor Cheatsheet

This is a non-staged pilot pending platform integration. Launch and score it
only after the Engine prerequisite in #58 and the release integration work are
complete. Levels 06-21 remain planned. Labs 22-27 are non-staged, offline
expansion labs and do not make the planned levels available.

| Challenge | Account | Evidence | Expected submission |
| --- | --- | --- | --- |
| Start Here | `sentinel0` / `sentinel0` | `~/evidence/ENGAGEMENT-RULES.txt` | structured engagement-scope answer |
| 01 Asset Census | `sentinel0` | `~/evidence/asset-census.txt`, native `sshd` process | structured asset evidence |
| 02 Control Review | `sentinel1` | `~/evidence/controls.md`, `control-evidence.md` | structured MFA, badge-review, and log-review tuple |
| 03 Change Window | `sentinel2` | `~/evidence/change-window.txt` | structured disposition and missing-evidence tuple |
| 04 Certificate Trail | `sentinel3` | `~/evidence/` test CA, leaf, CRL, key, ledger | structured certificate evidence |
| 05 Attack Surface | `sentinel4` | `~/evidence/exposure-review.conf`, `ss -lnt` | structured listener, port, and legacy-metrics tuple |
| 22 Phishing Header Analysis | `sentinel22` | `~/evidence/phishing-message.eml` | structured from-domain, return-path-domain, and DMARC tuple |
| 23 Detection Rule Validation | `sentinel23` | `~/evidence/detection-rule.yml`, `detection-corpus.log`, `decision-record.txt` | structured rule-ID, match-count, and decision tuple |
| 24 Endpoint Enrollment Evidence | `sentinel24` | `~/evidence/endpoint-enrollment.txt` | structured endpoint-ID, enrollment-status, and key-status tuple |
| 25 Alert Triage Summary | `sentinel25` | `~/evidence/alert-triage-summary.txt` | structured alert-ID, root-cause, and disposition tuple |
| 26 Network Inventory Review | `sentinel26` | `~/evidence/network-inventory.txt` | structured device-MAC, zone, and disposition tuple |
| 27 Evidence Metadata Review | `sentinel27` | `~/evidence/evidence-metadata.txt` | structured filename, checksum, and extracted-author tuple |

Submit JSON to `sentinel-submit`, for example
`printf '%s\n' '{"lab":"sentinel-01","answer":{...}}' | sentinel-submit`.
Only the matching account can release its next password after an exact valid
answer; malformed or invalid input changes no state. Lab 04 uses a committed
test CA/leaf/CRL and the ledger's fixed-time offline verification command, not
system trust, current time, or network revocation. The image requires all 12
`LEVEL_SECRETS` keys and rejects incomplete or wrong-shaped input before SSH.
The expansion evidence is original static local training content only: it includes
no credential values and requires no network scan, live service, external AI, or
external-system interaction.
