# Sentinel OODA Content Review Plan

## Purpose

This plan defines a 210-loop quality review of Sentinel's 21 scored labs:
10 OODA loops per lab. It is a content and learning-design review, not a
license to change the target, generator, stage contract, or platform while
review is underway. Start Here is excluded because it is onboarding rather
than a scored learning-objective lab.

The review's goal is not to make labs harder or add tools. It is to ensure
each lab is an original, safe, deterministic product that reinforces its
stated SY0-701 objectives through observable work.

## Non-negotiable boundaries

- **Orchestrator authority:** the primary agent is the sole decision-maker.
  Subagents provide bounded research or critique only. No subagent may edit
  Sentinel content, alter a plan decision, open a PR, add dependencies, or
  run privileged/network-destructive commands.
- **Scope:** review only the 21 labs recorded in
  `sentinel-lab-design-matrix.md`. Do not add objectives, grow the 22-challenge
  stage contract, or create a Windows-runtime requirement.
- **Safety:** do not introduce public scanning, live malware, credential
  attacks, offensive exploitation, production data, external targets,
  unrestricted outbound networking, host privileges, or generic privilege
  escalation.
- **Licensing:** prioritize existing core tools and original artifacts. Any
  new tool must be fully open source, offline-capable, lightweight, necessary
  for a specific outcome, and approved by the orchestrator after license and
  maintenance review.
- **Determinism:** artifacts use fictional data, fixed timestamps, pinned
  versions, and checksums where appropriate. A learner's result must not
  depend on a mutable feed, public service, time of day, or runtime entropy.
- **Truthfulness:** planned mechanisms remain marked `Planned`; only verified
  PR #68 behavior is marked `Built`.

## Agent roles and limits

Each loop uses at most two free research subagents in parallel. The
orchestrator assigns the lab and loop focus, reads the result, and records the
decision before the next loop begins.

| Role | Allowed work | Explicit limits |
| --- | --- | --- |
| Objective analyst | Compare the lab outcome against the local objective reference; identify missing/overclaimed coverage. | No new curriculum scope; no copying exam or commercial training content. |
| Scenario reviewer | Check realism, learner workflow, ambiguity, prerequisites, and novice/intermediate usability. | No difficulty inflation, exploit paths, or solution writing beyond a high-level critique. |
| Evidence/tool researcher | Verify an original artifact pattern or an open-source tool's license, maintenance, resource use, and offline fit. | No software installation, no web scraping of paid labs, no recommendation without primary-source evidence. |
| Safety/test reviewer | Evaluate isolation, secret handling, mutation boundaries, determinism, and testability. | No target changes and no attempts against real or external systems. |

An agent result must cite the reviewed lab, its assigned focus, evidence,
rewrites, and recommendations outside the assignment are discarded.

## OODA loop protocol

Every loop writes one completed-record cell in the compact 21x10 matrix. The
same structure applies to every lab.

1. **Observe:** record current lab contract, objective IDs, status, evidence,
   learner actions, validation, software, and prior-loop decision.
2. **Orient:** assess the loop's rubric dimension against the objective
   reference, tooling research, lab matrix, and any bounded external research.
3. **Decide:** the orchestrator chooses `keep`, `refine`, `defer`, or `remove`.
   A `refine` decision must state the smallest concrete change and its owner.
4. **Act:** document either a planned documentation/content/test task or a
   verified no-change rationale. No implementation is performed in this review
   phase.

## Ten-loop rubric for every scored lab

| Loop | Review focus | Exit question |
| --- | --- | --- |
| 1 | Objective fidelity | Does the required learner action directly demonstrate the stated objective, without overclaiming coverage? |
| 2 | Scenario realism | Is the fictional organizational context plausible and proportionate for an entry-level security practitioner? |
| 3 | Evidence quality | Is the decisive evidence authentic in form, sufficient, noise-balanced, synthetic, and internally consistent? |
| 4 | Intended path | Is there one reproducible intended path that requires analysis rather than guessing or tool trivia? |
| 5 | Learning progression | Do description, hints, prerequisites, and feedback preserve discovery for novice, intermediate, and expert learners? |
| 6 | Assessment validity | Does the flag or required result prove the learning outcome instead of a coincidental string search? |
| 7 | Safety and isolation | Does the scenario preserve team, host, secret, network, and mutation boundaries? |
| 8 | Determinism and operations | Does it reset/restart reliably, work offline, stay lightweight, and have a supportable instructor workflow? |
| 9 | Tool and artifact fit | Is the selected tool/artifact minimal, licensed, maintained, accessible over SSH, and necessary? |
| 10 | Integrated readiness | Are prior decisions coherent, all critical gaps resolved or explicitly blocked, and the lab ready for its implementation batch? |

## Decision severity and release gate

| Severity | Meaning | Required outcome |
| --- | --- | --- |
| Blocker | Unsafe, nondeterministic, legally unclear, objective-invalid, or impossible to validate. | Lab cannot enter an implementation PR until resolved and re-reviewed. |
| Major | A learner could solve without demonstrating the objective, or the intended path is ambiguous/unreliable. | Create a concrete refinement task and repeat affected loops after design update. |
| Minor | Clarity, artifact naming, documentation, or hint phrasing improvement. | Add to the batch backlog; verify during implementation review. |
| None | Evidence supports the current contract. | Record the rationale and move forward. |

A lab is `ready for implementation` only after all ten loops have an
orchestrator decision, no unresolved blocker/major finding remains, its
objective mapping is still within the approved 21-lab scope, and its proposed
software remains within the tooling decision record.

## Review order and checkpoints

The 210 loops run in implementation-batch order so shared design problems are
found before later labs depend on them.

| Checkpoint | Labs | Loops | Review output |
| --- | --- | --- | --- |
| A | 01-05, built pilot | 50 | Pilot remediation backlog; confirm existing claims against PR #68 tests. |
| B | 06-08, authentication and evidence | 30 | Batch 1 ready/not-ready decision. |
| C | 09-11, architecture and resilience | 30 | Batch 2 ready/not-ready decision. |
| D | 12-16, operations and detection | 50 | Batch 3 ready/not-ready decision; PCAP/Suricata gate decision. |
| E | 17-18, incident response | 20 | Batch 4 ready/not-ready decision. |
| F | 19-21, governance and assurance | 30 | Batch 5 ready/not-ready decision. |
| Total | 21 scored labs | 210 | Versioned review ledger and prioritized implementation backlog. |

At each checkpoint, the orchestrator consolidates repeated findings into one
shared rule rather than creating conflicting per-lab solutions. Examples are
the fixed artifact provenance format, a common false-positive rule, a common
hint review rule, and mutation-helper constraints.

## Ledger and workspace

The review workspace is version-controlled under `docs/sentinel-ooda/`:

- `README.md`: method, status, fixed terminology, and completed-loop count.
- `ledger.md`: the authoritative compact 21x10 completed record. A cell's row
  label and column heading identify its lab and loop; its decision/severity/
  action text records the final result and cites shared source conventions.
- `findings.md`: de-duplicated cross-lab findings, accepted design rules, and
  deferred decisions.
- `backlog.md`: implementation-ready work grouped by curriculum batch, with
  acceptance tests and dependencies.

Every review update is committed separately or in a small checkpoint commit.
The ledger never silently overwrites a prior decision: corrections append a
superseding entry that links to the original row.

## Research rules

- Research is just-in-time: only investigate a topic when a specific loop
  needs evidence to choose between options.
- Prefer official project documentation, licenses, and public documentation
  from training platforms. Use platform material for scenario patterns only;
  never copy challenge content, solutions, datasets, or proprietary training
  flows.
- The local SY0-701 objective reference is the curriculum authority. External
  material cannot expand objective claims.
- Record source URLs and an access date in the relevant ledger row or finding.

## First action after approval

Create the review workspace and pre-populate the 21x10 matrix with lab rows
and loop columns. Then execute checkpoint A, one loop at a time, with an
orchestrator decision recorded in each cell after each subagent result.

## Completed review

The completed review workspace is in [`sentinel-ooda/README.md`](sentinel-ooda/README.md),
with the compact 210-decision ledger, consolidated findings, and implementation
backlog. The ledger uses one cell per lab/loop to keep the complete record
reviewable without duplicating the full protocol in every row.
