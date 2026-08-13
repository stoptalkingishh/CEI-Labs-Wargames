# Sentinel OODA Ledger

Key: `K` keep, `R` refine, `D` defer. Severity is `N` none, `m` minor,
`M` major, `B` blocker. Each cell is an orchestrator decision after Observe,
Orient, Decide, and Act. Sources: local objective reference, lab design matrix,
tooling research, OODA plan, and bounded reviewer evidence. `verify PR68`
means verify the existing pilot claim against PR #68's reported target tests;
it is not a design defect by itself.

| Lab | 1 Objective | 2 Realism | 3 Evidence | 4 Path | 5 Progression | 6 Assessment | 7 Safety | 8 Operations | 9 Tool fit | 10 Readiness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | R-M: add baseline decision | K-N | R-m: one discrepancy/noise | K-N | R-m: three lab hints | R-M: validate discrepancy tuple | R-M: verify PR68 isolation | D-M: verify restart | K-N | D-M: after refinements |
| 02 | R-M: require CIA/AAA impact | K-N | R-M: prevent label leakage | K-N | R-m: staged hints | R-M: structured classification | K-N | D-M: verify PR68 YAML/flag | K-N | D-M: after assessment |
| 03 | K-N | K-N | R-M: make absence explicit | K-N | R-m: staged hints | R-M: require impact/dependency | K-N | D-M: verify PR68 artifacts | K-N | D-M: after assessment |
| 04 | K-N | K-N | R-M: explicit CRL/OCSP fixture | R-M: clock/trust independent | R-m: inspection hints | R-M: validate three findings | K-N | D-M: verify PR68 reset | K-N | D-M: after fixture contract |
| 05 | K-N | K-N | R-M: align static/live evidence | R-M: distinguish configured from exposed | R-m: staged hints | R-M: validate risk/action | D-M: verify PR68 listeners | D-M: verify reset | K-N | D-M: after terminology/tests |
| 06 | R-M: include monitoring implication | K-N | R-M: UTC/provenance corpus | R-M: one raw-log path | R-m: log-correlation hints | R-M: structured timeline answer | K-N | R-M: journal-independent reset | D-m: omit `ausearch` first | R-M: re-review 1/3/4/6/8 |
| 07 | R-M: classify vulnerability type | K-N | R-M: backport/version semantics | R-M: deterministic priority rubric | R-m: triage hints | R-M: response/validation answer | K-N | K-N | K-N | R-M: re-review 1/3/4/6 |
| 08 | R-M: choose analysis or correction | K-N | R-M: effective-access table | R-M: one learner path | R-m: ACL hints | R-M: structured finding/state | R-M: restricted-helper contract | R-M: reset/idempotence | R-m: pin ACL tools | R-M: re-review 1/3/4/6/7/8 |
| 09 | R-M: name architecture model | R-m: define zone roles | R-M: flow-consistent fixture | R-M: default/order semantics | R-m: rule-reading hints | R-M: structured flow answer | K-N | D-m: static only | K-N | R-M: re-review 1/3/4/6 |
| 10 | R-M: require type/state/geography | R-m: define policy terms | R-M: policy consistency test | R-M: scope valid controls | R-m: policy hints | R-M: per-record response | K-N | D-m: no OpenSSL initially | K-N | R-M: re-review 3/4/6 |
| 11 | R-m: distinguish validation/calculation | R-m: define workload | R-M: reconcile evidence | R-M: checksum/time restore criterion | R-m: RPO/RTO hints | R-M: structured readiness result | R-m: restrict restic path | D-m: static first | K-N | R-M: re-review 3/4/6 |
| 12 | R-m: require guardrail explanation | K-N | R-m: provenance/context | R-M: diagnose before helper | R-m: staged hints | R-M: diagnosis plus post-state | K-N | R-M: reset/idempotence | K-N | R-M: re-review 4/6/8 |
| 13 | R-m: distinguish hash/signature | K-N | R-M: evidence consistency | R-m: define comparison order | R-m: staged hints | R-M: classification/response answer | K-N | R-m: pin hashes/times | K-N | R-M: re-review 3/6 |
| 14 | K-N | K-N | R-M: inert evidence model | R-M: analysis-only or helper | R-m: staged hints | R-M: separate diagnosis/correction | D-B: resolve active-account contradiction | R-M: deterministic fixture/reset | K-N | D-B: redesign then re-review |
| 15 | K-N | K-N | R-m: provenance/noise fields | R-M: reproducible query path | R-m: query hints | R-M: rationale plus tradeoff | K-N | K-N | K-N | R-M: re-review 4/6 |
| 16 | R-m: explain guardrail/effect | K-N | R-m: approved change evidence | R-M: review before helper | R-m: staged hints | R-M: pre/post/backout answer | R-m: namespace constraint | R-M: reset/backout/action log | K-N | R-M: re-review 4/6/8 |
| 17 | K-N | K-N | R-m: correlation fields/checksum | R-M: unique containment rubric | R-M: add hints/feedback | R-M: structured timeline/scope/action | K-N | K-N | D-m: no Suricata first | R-M: re-review 4/5/6 |
| 18 | K-N | R-m: case/recipient context | R-m: provenance/signature choice | R-m: readonly/workspace split | R-M: hints/feedback | R-M: structured handoff | R-M: filesystem contract | R-m: error/restart checks | K-N | R-M: re-review 5/6/7 |
| 19 | R-M: role/responsibility field | K-N | R-M: revision manifest/checksum | K-N | R-m: hierarchy hints | R-M: structured governance answer | K-N | K-N | K-N | D-M: re-review 1/3/6 |
| 20 | K-N | R-m: business consequence/owner | R-M: input units/rounding | R-M: treatment constraints | R-m: calculation hints | R-M: intermediate-value answer | K-N | R-m: locale/format test | K-N | D-M: re-review 3/4/6 |
| 21 | R-M: remove 2.1 mapping | R-M: one unifying vendor case | R-M: evidence-decision matrix | R-M: one trigger/escalation | R-M: staged scope hints | R-B: redesign structured assessment | K-N | R-m: revision/timestamp test | K-N | D-B: redesign then re-review |

## Completion note

All 210 rows have an Observe/Orient basis in the cited source set. The compact
cell format records the final Decide/Act result. Re-review references identify
only affected loops; they do not erase this completed review record.
