# Security Policy

## Scope in one sentence

This repository publishes **intentionally vulnerable CTF and wargame content**.
A large fraction of it is offensive-security challenge material — insecure web
apps, vulnerable containers, capture-the-flag keys, and exploit walkthroughs.
**The vulnerabilities in the challenge content are the product, not defects.**

## What is in scope

A valid report is one where a bug in the *tooling or platform* lets someone do
something the authors did not intend:

- **Execution or data exposure outside a challenge sandbox.** For example, the
  Bandit/Krypton/Natas/Sentinel/Agent target images or the `natas-attacker`
  image allowing escape, host mount access, network pivot, or reading files
  outside the intended challenge filesystem.
- **Real secrets.** Committed CTFd API tokens, GHCR credentials, cloud keys,
  registry passwords, or a `.ctf/` config leaking a live token.
- **Leaking ground truth.** A published hint, `challenge.yml` flag value,
  solution doc, or test that hands a competitor the answer the challenge is
  meant to gate behind solving it.
- **The deploy or export path.** `deploy.sh`, `scripts/validate_generated.py`,
  or the CI workflows overwriting or destroying operator state, or shipping
  unpublished/un-audited content to a live CTFd instance.
- **CI/supply chain.** A workflow that runs untrusted PR code with elevated
  permissions, leaks `GITHUB_TOKEN`, or lets a PR write to the repository.

## What is NOT in scope (do not file these)

These are working as designed and reports will be closed as `won't fix`:

- **Any vulnerability in challenge content itself** — the Natas web app, the
  Bandit/Krypton crypto puzzles, Threadline's planted evidence, Sentinel's
  synthetic alerts and headers, or any Dockerfile `USER`/permission weakness
  that exists to make a challenge solvable.
- **Intended insecure configuration**, weak/default credentials, or
  deliberately reachable services inside `targets/`.
- **Exploitability of the published material.** Anyone can read the walkthroughs
  in `docs/`; that is intentional.
- **Findings requiring you to already control a target container** with the
  credentials the challenge hands out.
- **Missing hardening on a `localhost`-bound dev service**, or anything behind
  a documented network-access/QoS restriction.

## Reporting a vulnerability in the challenge content

If you believe a challenge is **broken** rather than intentionally vulnerable —
a flag is unreachable, a solution no longer works, a lab is unsolvable, or the
material teaches something factually wrong — that is a **content bug**, not a
security report. Open a normal public issue describing the challenge ID and the
symptom. Please do **not** include working flags or a complete exploit chain in
a public issue; describe the failure mode instead and let the maintainer
confirm the fix privately.

## Reporting a real security issue

1. **Preferred:** use GitHub's private advisory form —
   <https://github.com/stoptalkingishh/CEI-Labs-Wargames/security/advisories/new>
   (Report a vulnerability → Report a new vulnerability). If that form is
   unavailable, private vulnerability reporting may be disabled for this
   repository; in that case open a
   [private security advisory](https://github.com/stoptalkingishh/CEI-Labs-Wargames/security/advisories/new)
   from your own account, or contact the maintainer **stoptalkingishh** via
   their GitHub profile.
2. **Do not** open a public issue for anything in scope.

Please include: affected path, reproduction steps, impact, and any suggested
remediation. Give the maintainer a reasonable window to ship a fix before
disclosure. We aim to acknowledge within **3 business days** and to ship or
triage a fix within **14 days**.

## Supported Versions

This repository has no tagged releases or versioned distribution. Validation
runs against the **`main` branch at its current commit**, and that is the only
supported target.

| Version | Supported |
| ------- | --------- |
| `main` (current HEAD) | Yes |
| Any older commit, PR branch, or fork | No — upgrade to `main` |

Fixes land on `main` only. If you are running a pinned older commit, treat it
as unsupported and re-sync before reporting anything that `main` already fixes.
