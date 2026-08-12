# Sentinel: Security+ SY0-701-Aligned Wargame Plan

## Status and purpose

This is a planning specification, not a playable track. It proposes
**Sentinel**, a progressive, SSH-based security-operations wargame whose
hands-on labs reinforce the public CompTIA Security+ SY0-701 V7 objective
areas. It is not affiliated with CompTIA, does not reproduce exam questions,
and does not claim that completing it prepares a participant to pass an exam.

The source used for the alignment is the local `CompTIA Security+ SY0-701
Exam Objectives (7.0).pdf`, dated 2023. Objective wording is summarized here
rather than copied. Sentinel complements the existing Linux, cryptography,
and web-security tracks with defensive system administration and incident
response work.

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

| Lab | Scenario and observable work | SY0-701 alignment |
| --- | --- | --- |
| Start Here | Connect using SSH, read the engagement rules, retrieve the onboarding token. | Safe lab conduct; SSH as a secure access method. |
| 01 Asset Census | Reconcile a supplied asset inventory with installed packages, active services, and ownership metadata. | 4.2 asset management; 4.1 secure baselines. |
| 02 Control Review | Classify a set of implemented safeguards by category and purpose using evidence on the host. | 1.1 controls; 1.2 CIA and AAA. |
| 03 Change Window | Review a change request, identify missing approval, rollback, or test evidence, and select the safe action. | 1.3 change management. |
| 04 Certificate Trail | Inspect a certificate chain, key permissions, and revocation evidence to identify the trustworthy service identity. | 1.4 PKI, certificates, hashing, and signatures. |
| 05 Attack Surface | Enumerate listening services and configuration artifacts, then identify the exposed default service. | 2.2 attack surface; 2.5 hardening. |
| 06 Suspicious Access | Correlate authentication logs for password spraying, impossible travel, and concurrent-session indicators. | 2.4 indicators of malicious activity; 4.9 log sources. |
| 07 Vulnerability Triage | Validate a scanner finding against package and configuration evidence, distinguish false positive from true finding, and prioritize remediation. | 2.3 vulnerabilities; 4.3 vulnerability management. |
| 08 Least Privilege | Audit Unix users, groups, ACLs, and sudo policy to correct an over-broad delegated permission. | 2.5 access control and least privilege; 4.6 IAM. |
| 09 Segmented Services | Read a constrained host firewall and network-zone diagram to identify the allowed management path and an unsafe rule. | 3.1 architecture models; 3.2 infrastructure security. |
| 10 Data Handling | Classify sample data and choose the required protection for data at rest, in transit, and in use. | 3.3 data protection. |
| 11 Recovery Evidence | Validate encrypted backup metadata, recovery-point evidence, and a restoration drill record. | 3.4 resilience and recovery. |
| 12 Baseline Drift | Compare a secure baseline with the current system, identify unauthorized service or configuration drift, and restore the approved state. | 4.1 secure baselines and hardening; 4.7 automation guard rails. |
| 13 Integrity Alert | Verify a file-integrity alert with hashes and package ownership, then identify the affected asset. | 1.4 hashing; 4.4 monitoring; 4.5 file integrity monitoring. |
| 14 Identity Lifecycle | Process a simulated offboarding request and verify deprovisioning, group removal, and credential invalidation evidence. | 4.6 provisioning and deprovisioning; least privilege. |
| 15 Alert Tuning | Analyze SIEM-like normalized events, separate a false positive from a true alert, and document the tuning rationale. | 4.4 alerting and monitoring. |
| 16 Secure Service Change | Apply a narrow, reversible secure-protocol and firewall configuration change through the supplied automation interface. | 4.5 secure protocols and firewall rules; 4.7 automation. |
| 17 Incident Containment | Build a timeline from endpoint, application, and firewall records, then choose the containment action that preserves evidence. | 4.8 incident response; 4.9 investigation sources. |
| 18 Forensic Handoff | Validate an evidence manifest and chain-of-custody record without modifying the evidence set. | 4.8 digital forensics, preservation, and reporting. |
| 19 Policy to Practice | Match system evidence to policy, standard, procedure, and ownership requirements; identify a governance gap. | 5.1 governance. |
| 20 Risk Register | Calculate and prioritize a small risk register using likelihood, impact, exposure factor, SLE, ARO, ALE, RTO, and RPO. | 5.2 risk management and business impact analysis. |
| 21 Assurance Review | Assess a vendor evidence pack and a reported phishing message, then select the required escalation and compliance record. | 5.3 third-party risk; 5.4 compliance; 5.5 assessments; 5.6 awareness. |

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
| Engine coordination | Extend Engine hint-wallet track validation and verify the stage-manifest ingestion, admin controls, mapping reconciliation, and Swarm hardening for a fourth staged track. |

## Delivery sequence and gates

1. **Platform contract PRs:** generalize staged-track validation and deploy
   assumptions in this repository; make the coordinated Engine change for a
   fourth managed hint wallet and stage. No Sentinel content is released at
   this point.
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
- Approve the coordinated Engine work as a prerequisite; the current wallet
  allowlist and stage assumptions cannot support a fourth managed track.
- Confirm the event's offline policy for any future reading links. Sentinel
  should prefer original, local explanations and must not require external
  websites.
