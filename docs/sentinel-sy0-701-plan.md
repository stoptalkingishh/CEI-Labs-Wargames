# Sentinel: Security+ SY0-701-Aligned Wargame Plan

## Status and purpose

This is a planning specification, not a playable track. It proposes
**Sentinel**, a progressive, SSH-based security-operations wargame whose
hands-on labs reinforce the public CompTIA Security+ SY0-701 V7 objective
areas. It is not affiliated with CompTIA, does not reproduce exam questions,
and does not claim that completing it prepares a participant to pass an exam.

The alignment source is CompTIA's official exam-objectives page, recorded with
version and retrieval/checksum instructions in the project-owned
[`reference/comptia-security-plus-sy0-701-v7-objectives.md`](reference/comptia-security-plus-sy0-701-v7-objectives.md)
coverage map. The map does not reproduce objective wording. Sentinel
complements the existing Linux, cryptography, and web-security tracks with
defensive system administration and incident response work.

Tooling and lab-platform research, including the recommended lightweight
open-source toolchain and Windows scope, is recorded in
[`sentinel-tooling-research.md`](sentinel-tooling-research.md).

The per-lab learning, evidence, validation, software, and build contracts are
maintained in [`sentinel-lab-design-matrix.md`](sentinel-lab-design-matrix.md).

The quality-review operating model for the 210-loop, orchestrator-led OODA
review is in [`sentinel-ooda-review-plan.md`](sentinel-ooda-review-plan.md).

## Player experience

Sentinel uses the existing `single-target` pattern: each team receives one
persistent SSH target with a sequence of least-privileged `sentinelN`
accounts. Solving one lab reveals the next account credential or, for the
final lab, a per-team dynamic CTF flag. Players inspect and improve a
deliberately realistic but contained enterprise host; they do not attack
other teams, CTFd, the orchestration service, or internet systems.

The target is a fictional `Northstar` operations jump host. The progression
is defensive: inventory the host, assess evidence, apply or verify a safe
control, and record the result. Labs must have one intended, reproducible
solution path and must not require host root or generic privilege escalation.

## Curriculum scope

The initial release contains one Start Here challenge plus 21 scored labs.
This is broad objective-area alignment, not a one-lab-per-bullet transcription
of the exam outline. Each lab needs an authored scenario, a measurable output,
three progressive hints, a complete instructor writeup, and a live runtime
test before it can ship.

| Lab | Status / batch | Scenario and primary evidence | SY0-701 coverage |
| --- | --- | --- | --- |
| Start Here | Built, PR #68 / 0 | SSH connection, engagement rules, onboarding token. | Secure access context. |
| 01 Asset Census | Implemented, non-staged; assessment/runtime verification pending | Asset inventory, installed packages, active services, ownership metadata. | 4.1, 4.2 |
| 02 Control Review | Implemented, non-staged; assessment/runtime verification pending | Host safeguards classified by category and purpose. | 1.1, 1.2 |
| 03 Change Window | Implemented, non-staged; assessment/runtime verification pending | Change record with approval, test, rollback, and maintenance evidence. | 1.3 |
| 04 Certificate Trail | Implemented, non-staged; assessment/runtime verification pending | Certificate chain, key permissions, and revocation evidence. | 1.4 |
| 05 Attack Surface | Implemented, non-staged; assessment/runtime verification pending | Listening services and configuration artifacts exposing a default service. | 2.2, 2.5 |
| 06 Suspicious Access | Planned / 1 | Deterministic SSH/auth/audit logs for spraying, impossible travel, and concurrent sessions. | 2.4, 4.4, 4.9 |
| 07 Vulnerability Triage | Planned / 1 | Mock scanner/advisory plus package and configuration evidence. | 2.3, 4.3 |
| 08 Least Privilege | Planned / 1 | Unix users, groups, ACLs, and `sudo` policy. | 2.5, 4.6 |
| 09 Segmented Services | Planned / 2 | Firewall policy and network-zone diagram. | 3.1, 3.2 |
| 10 Data Handling | Planned / 2 | Data classification and state-of-data protection decision record. | 3.3 |
| 11 Recovery Evidence | Planned / 2 | Encrypted backup metadata, RPO/RTO, and restoration-drill record. | 3.4, 5.2 |
| 12 Baseline Drift | Planned / 3 | Secure baseline versus unauthorized service/configuration drift. | 4.1, 4.7 |
| 13 Integrity Alert | Planned / 3 | FIM alert, hashes, and package ownership. | 1.4, 4.4, 4.5 |
| 14 Identity Lifecycle | Planned / 3 | Inert offboarding ticket, identity snapshots, revoked-key register, and attestation for an identity absent from the target. | 4.6 |
| 15 Alert Tuning | Planned / 3 | Normalized SIEM-like events and false-positive rationale. | 4.4 |
| 16 Secure Service Change | Planned / 3 | Reversible secure-protocol/firewall automation change. | 4.5, 4.7 |
| 17 Incident Containment | Planned / 4 | Endpoint, application, firewall, and network timeline. | 2.4, 4.8, 4.9 |
| 18 Forensic Handoff | Planned / 4 | Evidence manifest and chain-of-custody record. | 4.8 |
| 19 Policy to Practice | Planned / 5 | Policy, standard, procedure, ownership, and system-evidence package. | 5.1 |
| 20 Risk Register | Planned / 5 | Risk register and BIA using SLE, ARO, ALE, RTO, and RPO. | 5.2 |
| 21 Assurance Review | Planned / 5 | One vendor's due diligence, agreement, attestation, audit finding, remediation response, and renewal-decision record. | 5.3-5.6 |

## Architecture contract

- **Slug and category:** `sentinel` and `Security Operations`. The final
  display name is `Sentinel - Security Operations` until a product owner
  approves a different theme.
- **Instances:** a per-team `single-target` SSH image, one stable
  `instance_group` for every Sentinel challenge, and exactly one public
  launcher on Start Here. SSH is the only published target port.
- **Flags and credentials:** every scored lab uses an existing per-team
  dynamic flag type and a stable `data` key. The entrypoint derives account
  credentials, flags, and puzzle values deterministically from `LEVEL_SECRETS`.
  It must fail closed if a required secret is absent.
- **State:** puzzle state must survive a restart by deterministic derivation;
  runtime entropy, shared flags, and static scored flags are prohibited.
- **Isolation:** build-time artifacts contain no team secrets. The entrypoint
  must remove `LEVEL_SECRETS` before any vulnerable service or child process
  begins. Homes, evidence, credentials, and helpers are readable only by the
  intended account or group. No lab may provide a path to another team,
  container runtime, host, CTFd, Engine, or unrestricted outbound network.
- **Content:** generated challenge YAML comes only from
  `scripts/build_sentinel.py`; generated files are never hand-edited. Every
  non-onboarding lab has exactly three `managed_tiers()` hints. Descriptions
  state the goal but do not disclose a hint-tier solution.

## Repository and platform work

Sentinel cannot be added by only creating a Dockerfile. The implementation
must update these contracts together:

| Area | Required work |
| --- | --- |
| Generator | Add `scripts/build_sentinel.py`, content invariants, dynamic flag keys, `sentinel-hint-wallet.json`, and generation tests. |
| Target | Add `targets/sentinel/` with an immutable-base Dockerfile, account/artifact setup, deterministic entrypoint, SSH hardening, and target contract tests. |
| Stage contract | Add Sentinel to `game-stages.yml`; generalize `scripts/validate_game_stages.py` and every three-track/count assumption. |
| Deploy and validation | Build Sentinel in `deploy.sh`, include its hint wallet, update exact totals only after generated counts are known, and update generated-YAML, inventory, smoke, concurrency, and reconciliation tests. |
| CI and release | Build/test the target in `.github/workflows/build-targets.yml` and `validate.yml`; use immutable image digests for release validation. |
| Documentation | Add `docs/sentinel/{writeups,learning-objectives,cheatsheet}.md` and update the README, curriculum index, facilitator material, participant quick-start, and inventory. |
| Engine coordination | Extend Engine hint-wallet track validation, the duplicated category-to-track mappings, and its independent default-stage registry. Engine does not ingest `game-stages.yml`; the two repositories must carry matching Sentinel slug, category, order, and expected-count contracts. |

## Delivery sequence and gates

1. **Platform contract PRs:** generalize staged-track validation and deploy
   assumptions in this repository; make the coordinated Engine change for a
   fourth managed hint wallet, category mapping, and independently seeded
   stage. No Sentinel content is released at this point.
2. **Target foundation PR:** add the minimal SSH image, account model,
   secret plumbing, one onboarding path, and isolation/restart tests. The
   image must demonstrate no secret leakage before curriculum work begins.
3. **Curriculum PRs:** implement small objective-grouped batches: foundations
   and exposure (01-05), evidence and architecture (06-11), operations and
   response (12-18), then governance and assurance (19-21). Each batch must
   include generators, target artifacts, hints, writeups, and live solve
   tests.
4. **Integration PR:** add the stage manifest, deploy/import support, image
   workflow, inventory, and local CTFd tests after the Engine contract is
   available.
5. **Release-readiness PR:** publish immutable images and execute an
   authorized multi-team test: intended solve paths, wrong-user denial,
   restart determinism, secret-leak probes, final-only teardown, mapping
   reconciliation, and concurrent launch/relaunch behavior.

## Curriculum implementation pipeline

Each curriculum batch is one reviewable PR after its predecessor has passed
its target and generator tests. A batch may add an existing tool only when the
lab cannot be expressed faithfully with the current deterministic artifacts;
the tooling decision record is the authority for that choice.

| Batch | Labs | Objectives | Primary evidence and tools | Completion gate |
| --- | --- | --- | --- | --- |
| 0: Foundation | Start Here, 01-05 | 1.1-1.4, 2.2, 2.5, 4.1, 4.2 | OpenSSH, OpenSSL, synthetic inventory/control/change records. | Implemented, non-staged; assessment/runtime verification remains pending until the PR #68 validation checklist is independently recorded. |
| 1: Authentication and evidence | 06-08 | 2.4, 2.5, 4.4, 4.6, 4.9 | Deterministic SSH/auth/audit logs, account/group/ACL fixtures, `journalctl`, `last`, `ausearch` where justified. | Intended login path and neighboring-account denial pass; learner derives a timeline and least-privilege conclusion from raw logs. |
| 2: Architecture and resilience | 09-11 | 3.1-3.4, 5.2 | Static topology/data-classification/backup artifacts; optional `nftables`, OpenSSL, and restic only for bounded verification. | Every scenario is solvable with no host network capability and has an explicit RTO/RPO, data-state, or access-path answer. |
| 3: Operations and detection | 12-16 | 2.3, 4.1, 4.3-4.7 | Baseline/drift fixtures, mock advisory and scan evidence, FIM data; then offline PCAP via `tcpdump -r` and pinned Suricata rules/EVE JSON. | PCAPs, logs, rules, package versions, and expected output are pinned/checksummed; no feeds, live capture, or internet access. |
| 4: Incident response | 17-18 | 2.4, 4.8, 4.9 | Combined authentication, process, file, application/firewall, and PCAP evidence; chain-of-custody and timeline artifacts. | A full raw-evidence timeline, scope, containment decision, and evidence-preservation test pass without modifying the evidence corpus. |
| 5: Governance and assurance | 19-21 | 5.1-5.6 | Original policy/standard/procedure/RACI, risk register/BIA, and one vendor's due diligence, agreement, attestation, audit finding, and remediation artifacts. | Answers cite evidence and distinguish policy, standard, procedure, control owner, risk treatment, and a vendor-assurance renewal decision. |
| 6: Windows evidence extension | Optional additional scenarios, not required for initial 22 challenges | Windows-relevant 2.4, 4.1, 4.4-4.6, 4.8-4.9 | Project-owned, sanitized EVTX plus raw/normalized evidence and an open-source parser such as `libevtx`. | Fixture provenance, source scenario, audit-policy assumptions, checksum, and expected timeline are documented. No Windows runtime is required. |
| 7: Shared advanced environment | Optional, post-release | Selected 4.3-4.5 and 4.8-4.9 | Shared Wazuh, Velociraptor, Greenbone, or isolated Windows evaluation VM. | Separate capacity, licensing, isolation, retention, reset, and maintenance review. These services never become a hidden requirement for the core SSH track. |

### Dependency rules

- Batches 1-5 may be authored and tested against the Sentinel image after
  Batch 0, but cannot be deployed until the Engine fourth-track support and
  Wargames platform integration are merged and released.
- Batch 3 may not introduce Suricata until Batch 3's PCAP corpus and its
  `tcpdump -r` workflows are already reproducible. Suricata processes local
  PCAPs with a committed rule set only.
- Batches 2 and 5 prefer documents and deterministic records over services;
  installing a product is not evidence of learning a governance or risk
  objective.
- Batch 6 must not bundle proprietary Windows software or a Microsoft image.
  Native Windows administration is a separate shared-lab decision, not a
  per-team container feature.
- A batch may not change the stage's expected challenge count without an
  explicit plan amendment and matching Engine-stage contract change.

### Required evidence for every batch

- Mapping from every new lab to at least one objective in the project
  objective reference.
- Original scenario artifacts with fictional data, deterministic timestamps,
  checksums for binary evidence, and no production credentials or captures.
- A target test for intended solve, wrong-user denial, restart determinism,
  and secret/environment leakage where the lab uses dynamic secrets.
- Generated-YAML and hint-wallet coverage: exactly three progressive hints for
  each scored lab; no hint-tier solution text in its free description.
- Instructor writeup, learner objective, cheat-sheet entry, and concise
  post-lab debrief covering decisive evidence, false-positive consideration,
  mitigation, and appropriate ATT&CK mapping where relevant.

## Completion criteria

Sentinel is ready only when all 21 labs map to this document, their intended
commands work through a real SSH PTY against a built image, generated YAML
parses and passes release validation, every lab has three costed hints and an
instructor writeup, and an authorized multi-team runtime audit demonstrates
isolation and deterministic restarts. A successful source review or Docker
build alone is not sufficient.

## Decisions required before implementation

- Confirm `Sentinel` as the permanent slug and `Security Operations` as the
  category.
- Confirm the 21-lab initial scope versus a smaller pilot (Start Here plus
  labs 01-05) before content implementation.
- Approve the coordinated Engine work as a prerequisite; its current wallet
  allowlist accepts exactly three tracks and its stage configuration is not
  sourced from this repository's manifest.
- Confirm the event's offline policy for any future reading links. Sentinel
  should prefer original, local explanations and must not require external
  websites.
