# OSINT Pilot Event Runbook

## Pre-flight

- Install the trusted CTFGenerator host and reviewed OSINT plugin.
- Deploy a CEI Engine CTFd image that includes the `typed-answer-flags` plugin;
  do not sync the pilot to stock CTFd or an older Engine image.
- Run `python3 -m unittest -v test_build_osint_adapter` from `scripts/`.
- Build with `CEI_OSINT_RELEASE_STATE=hidden`.
- Review generated `osint-training.json`, evidence hashes, licensing, safety/privacy approval, and private instructor solutions.
- Sync only after organizer approval.
- Confirm all three imported flags have type `typed_answer` before testing
  submissions; a static flag indicates an obsolete export and must fail the
  release gate.

## Session

The three pilot cases are independent and may be completed in any order. Allocate 20–30 minutes per case plus a short evidence-corroboration debrief. Participants use only the supplied artifacts and legal public information described by each briefing.

## Release and rollback

Release with:

```bash
CEI_OSINT_RELEASE_STATE=visible python3 scripts/build_osint.py
ctf challenge sync osint/
```

To withdraw the pilot, regenerate it as `hidden` and sync again. The track has no runtime instance, ports, container, or orchestrator mapping.
