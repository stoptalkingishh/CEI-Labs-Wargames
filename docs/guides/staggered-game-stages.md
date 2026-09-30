# Staggered Game-Stage Manifest

`game-stages.yml` defines how Wargames content is grouped into the three
administrator-started CEI Labs games. Challenge generators remain responsible
for names, categories, values, flags, hints, and instance metadata. The stage
manifest adds the event-level grouping contract consumed by the Engine's CTFd
stage-control plugin.

## Rules

- `slug` is a stable machine identifier and must never be reused.
- `category` must exactly match every generated challenge in that stage.
- `challenge_prefix` is a validation guard, not the primary CTFd mapping key.
- `start_challenge` identifies the participant entry point.
- `expected_challenge_count` includes the Start Here challenge and detects an
  incomplete or stale import.
- A challenge may map to one stage only.
- Stage start times and scoreboard state belong to Engine/CTFd, not this
  static content repository.

## Validation

Run:

```bash
python scripts/validate_game_stages.py
```

The validator regenerates no content and changes no files. It checks the
manifest schema against the three build scripts and, when generated
`challenges/` content is present, verifies category, prefix, Start Here, and
expected-count consistency.

After deployment, an administrator must also run Engine's CTFd mapping sync
and compare its report with this manifest before starting any stage.

## Verifying the live instance

`scripts/test_staggered_concurrency.py`, `scripts/test_staggered_smoke.py`, and
`scripts/test_export_reconciliation.py` check this manifest against a running
CTFd instance. They need a live instance and are not run in CI; the procedure,
and the static guard that stands in for them there, are documented in
[Staggered Live-CTFd Test Procedure](staggered-live-test-procedure.md).
