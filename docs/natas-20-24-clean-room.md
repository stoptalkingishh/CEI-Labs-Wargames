# Natas 20-24 Clean-Room Scenarios

Levels 20-24 are local, per-team training models. They replace historical
implementation details with bounded original scenarios and expose only the
next adjacent runtime secret after the intended behavior is reached.

| Levels | Learning objective | Reset behavior |
| --- | --- | --- |
| 20 | Ambiguous custom record serialization can change parsed state. | The private record is recreated at container start. |
| 21 | Separate internal routes need explicit trust boundaries. | Request-local cookie state only. |
| 22 | Redirects do not necessarily stop later response generation. | Request-local, with a no-store body. |
| 23 | Numeric compatibility coercion differs from strict comparison. | Request-local. |
| 24 | Request field shape requires validation alongside values. | Request-local bounded model. |

The local HTTP audit is `scripts/runtime_audit_natas_20_24.py`. It rejects
non-loopback targets and checks authentication, intended and negative paths,
adjacent-secret isolation, and reset-safe default state.
