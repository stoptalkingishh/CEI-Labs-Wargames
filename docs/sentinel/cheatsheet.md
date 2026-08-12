# Sentinel Pilot Instructor Cheatsheet

This is a non-staged pilot pending platform integration. Launch and score it
only after the Engine prerequisite in #58 and the release integration work are
complete. Levels 06-21 remain planned.

| Challenge | Account | Evidence | Expected submission |
| --- | --- | --- | --- |
| Start Here | `sentinel0` / `sentinel0` | `ENGAGEMENT-RULES.txt` | onboarding token |
| 01 Asset Census | `sentinel1` | `asset-census.txt` | census result |
| 02 Control Review | `sentinel2` | `controls.md`, `control-evidence.md` | review result |
| 03 Change Window | `sentinel3` | `change-window.txt` | recorded disposition |
| 04 Certificate Trail | `sentinel4` | `service.pem`, `certificate-ledger.txt` | verified service record |
| 05 Attack Surface | `sentinel5` | `exposure-review.conf`, `ss -lnt` | signed finding |

Each solved value becomes the next account password. The image requires all
six `LEVEL_SECRETS` keys and rejects incomplete input before starting SSH.
