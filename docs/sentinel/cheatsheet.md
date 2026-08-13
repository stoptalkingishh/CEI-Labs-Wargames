# Sentinel Pilot Instructor Cheatsheet

This is a non-staged pilot pending platform integration. Launch and score it
only after the Engine prerequisite in #58 and the release integration work are
complete. Levels 06-21 remain planned.

| Challenge | Account | Evidence | Expected submission |
| --- | --- | --- | --- |
| Start Here | `sentinel0` / `sentinel0` | `ENGAGEMENT-RULES.txt` | structured engagement-scope answer |
| 01 Asset Census | `sentinel1` | `asset-census.txt`, native `sshd` process | structured asset evidence |
| 02 Control Review | `sentinel2` | `controls.md`, `control-evidence.md` | structured classifications |
| 03 Change Window | `sentinel3` | `change-window.txt` | structured disposition evidence |
| 04 Certificate Trail | `sentinel4` | test CA, leaf, CRL, key, ledger | structured certificate evidence |
| 05 Attack Surface | `sentinel5` | `exposure-review.conf`, `ss -lnt` | structured exposure evidence |

Submit JSON to `sentinel-submit`, for example
`printf '%s\n' '{"lab":"sentinel-01","answer":{...}}' | sentinel-submit`.
Only the matching account can release its next password after an exact valid
answer; malformed or invalid input changes no state. Lab 04 uses a committed
test CA/leaf/CRL and the ledger's fixed-time offline verification command, not
system trust, current time, or network revocation. The image requires all six
`LEVEL_SECRETS` keys and rejects incomplete or wrong-shaped input before SSH.
