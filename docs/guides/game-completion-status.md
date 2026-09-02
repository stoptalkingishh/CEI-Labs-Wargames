# Wargame Completion Status

This is the current repository-level status of each game source and its
release path. A generated challenge count proves that a builder emitted
metadata; it does not prove that images, mappings, external dependencies, or a
live participant session have been verified.

## Primary self-hosted tracks

| Game | Current source scope | Generated | Runtime/release status |
|---|---:|---:|---|
| Bandit | 34 levels (0–33) + Start Here | 35 challenges | Content and target build are present; staged metadata validation passes. A current digest-pinned image and live Engine/CTFd deployment still need event-time verification. |
| Krypton | 7 levels (0–6) + Start Here | 8 challenges | Content and target build are present; staged metadata validation passes. A current digest-pinned image and live Engine/CTFd deployment still need event-time verification. |
| Natas | 35 endpoints (0–34) + Start Here | 36 challenges | Not release-ready. Endpoints 15–34 are inert/pending scenario content, and the attacker/noVNC image plus live mapping/session prerequisites remain unresolved. See `natas-completion-status.md`. |

The three tracks are grouped in `game-stages.yml` as stages 1–3. The stage
validator currently expects 35, 8, and 36 generated challenges respectively.
The normal metadata CI gate does not build Docker images or perform a live
Engine/CTFd launch.

## Additional tracks

| Game | Current source scope | Generated | Runtime/release status |
|---|---:|---:|---|
| AI Copilot | 6 local verification challenges | 6 challenges | Metadata track only; hidden by default, no per-team target. Requires the external CEI Labs Agent installation and organizer release decision. |
| OSINT pilot | 3 reviewed artifact-investigation methods | 3 challenges when the external plugin is installed | Hidden by default, no container or ports. This checkout does not currently have the required `ctf_generator.families:osint_investigation` entry point installed, so generation cannot be reproduced locally until that dependency is installed. |
| Threadline | 42-lead campaign across 9 arcs | 42 challenges | Source generator and committed transcripts are present; hidden by default, non-staged, and no container is required. Release still requires organizer review and the external evidence archive where attachments are expected. |
| Sentinel | Start Here + labs 01–05 + expansion labs 22–27 | 12 challenges in separate `sentinel/` output | Hidden and non-staged. Labs 01–05 are implemented but require independent runtime/assessment verification; 06–21 remain planned; 22–27 are deferred offline expansion labs. |
| Sentinel OODA | 21-lab review workspace | N/A | Review record is complete, but it is not a released game. It documents contracts, findings, and backlog for Sentinel implementation and validation. |

## What “complete” means here

- **Source-complete:** objectives, challenge definitions, writeups, and build
  source exist for the stated scope.
- **Metadata-validated:** generators, YAML contracts, inventory, and tests pass.
- **Runtime-verified:** the target or external dependency was exercised through
  the intended participant path in an isolated environment.
- **Release-ready:** runtime verification, immutable image references,
  Engine/CTFd mapping sync, and event-owner sign-off are recorded.

At present, Bandit and Krypton are source-complete and metadata-validated;
Natas and Sentinel have explicit incomplete scopes; OSINT depends on an
external package; Threadline is generated but still an organizer-released
hidden campaign. No game should be called production-ready from CI metadata
alone.
