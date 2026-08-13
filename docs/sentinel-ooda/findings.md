# Sentinel OODA Findings

## Accepted cross-lab rules

1. Every scored lab requires a structured, evidence-backed conclusion before
   its dynamic flag/next credential is released. A discoverable file location
   or one string search is never sufficient assessment.
2. Every fixture set has a provenance manifest: fictional organization,
   artifact revision, fixed UTC timestamps, checksums for binary evidence, and
   internally consistent identifiers across sources.
3. Static artifact labs remain static unless a live action uniquely reinforces
   the objective. Governance, risk, data handling, and vendor assurance do
   not gain value from adding a service.
4. Any mutation helper has one fixed purpose, accepts no arbitrary command or
   path, logs work, is idempotent/reversible, and has reset, escape, and
   unauthorized-state tests.
5. Evidence labs use raw evidence first. Normalized JSON, instructor timeline,
   labels, and ground truth are not visible to learners unless intentionally
   introduced after investigation.
6. Hints are lab-specific: locate evidence, interpret it, then execute or
   validate the allowed action. Free descriptions must not disclose tier-two
   or tier-three reasoning.
7. Offline-only is retained: no mutable feeds, public scanning, live capture,
   external DNS, external reputation checks, cloud storage, or live email.

## Design blockers

- **Lab 14:** a deliberately active residual offboarding account conflicts
  with target isolation. Redesign as inert evidence-only, or define a tightly
  restricted correction flow that cannot create unscoped access.
- **Lab 21:** one escalation cannot validly assess threat actors plus all of
  5.3-5.6. Remove 2.1 from the lab and split its structured evidence-to-
  decision assessment across the retained objectives, without increasing the
  stage challenge count.

## Verification gates, not design blockers

The reviewers could not inspect the PR #68 branch locally. Before staging the
built pilot, independently execute its reported generator, target contract,
Docker, listener, fail-closed, secret-scrub, restart, and cross-account tests.
