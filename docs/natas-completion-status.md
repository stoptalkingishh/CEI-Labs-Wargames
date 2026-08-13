# Natas Completion Status

**Current status: not release-ready.** This repository contains the Natas
target and attacker Dockerfile sources, but this audit did not verify a
launchable Natas range. Do not treat historical playtest statements as a
current deployment attestation.

## Scope

The approved eventual Natas scope is level endpoints 0-34. The range
foundation is complete: endpoints, identities, authentication, runtime secret
validation, and inert pending pages exist through level 34. Scenario content
for levels 15-34 remains pending and is deliberately not a release of 36
challenges. Deployment totals, `game-stages.yml`, and current deployment
behavior remain unchanged. See plan PR #69 for the deferred scenario work.

## What This Repository Owns

- `targets/natas/` is the Natas target build context.
- `targets/natas-attacker/` is the Natas-specific attacker extension. It
  adds Natas tools to an Engine-provided Kali/noVNC base image.
- `.github/workflows/build-targets.yml` includes both `natas` and
  `natas-attacker` contexts. It publishes `sha-<commit>` tags only when a
  maintainer manually dispatches it with an immutable base-image digest.
- Generated challenge metadata defaults to
  `ghcr.io/stoptalkingishh/cei-labs-wargames/natas-attacker:latest`, while
  the build workflow publishes `sha-<commit>` tags. That default is not a
  release reference and must be overridden with a verified immutable
  digest for an event.

## External Prerequisite

The base workstation, including noVNC, SSH, and the Natas wallpaper, is
owned by [CEI-Labs-Engine](https://github.com/stoptalkingishh/cei-labs-engine)
at `operator/kali-novnc/`. The Natas attacker image cannot be built until an
authorized Engine base image is available by immutable digest.

For an event, the operator must provide all of the following before exposing
Natas to participants:

1. A published, pullable Wargames `natas-attacker` image built from this
   repository's context and pinned by digest.
2. Its Engine `ctf-kali-novnc` base image pinned by digest.
3. Natas target and attacker digest references in the deployed challenge
   mappings.
4. An Engine deployment whose instance-launcher mapping has been synced.

The audit could fetch Engine's public `ctf-kali-novnc:latest` manifest but
could not fetch Wargames `natas-attacker:latest` anonymously (GHCR returned
`403`). This is evidence of an unresolved publication or access prerequisite,
not evidence that the image does not exist.

## Supported Participant Path

Once the prerequisite is met and the event operator has verified the live
range, participants use the noVNC link supplied by the launch panel. Natas
targets are reached only from that workstation. SSH is not participant-facing
by default: use it only when the event operator explicitly provides a tested
endpoint and credential. Source review of Engine shows SSH support in the
base image, but this audit did not run an SSH or noVNC session against a Natas
deployment.

The Natas Start Here challenge depends on Engine's checked-in wallpaper for
its `WELCOME TO NATAS` value. That source asset exists in Engine, but its
appearance in a launched workstation remains an event-time verification.

## Ownership And Verification Contract

| Item | Owner | Required evidence before release |
|---|---|---|
| Natas target and attacker extension | CEI-Labs-Wargames | Successful digest-pinned build and published, pullable digest |
| Kali/noVNC base, SSH behavior, wallpaper | CEI-Labs-Engine | Referenced base digest plus source-owner build evidence |
| Challenge mapping and launch panel | CEI-Labs-Engine deployment operator | Mapping sync and a live launch for a test team |
| Participant noVNC path and Start Here wallpaper | Event operator | Open the launch-panel link and visually confirm the desktop/value |
| SSH path, if offered | Event operator | Test the supplied endpoint and credential; otherwise do not advertise it |

Record image digests, Engine revision, mapping-sync result, and the live
noVNC/Start Here check in the event record. A source review, generated YAML,
or successful image build alone does not satisfy the live-range checks.
