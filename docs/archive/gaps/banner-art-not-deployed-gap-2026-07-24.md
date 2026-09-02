# SSH login ASCII art request -- already built in source, not yet deployed (2026-07-24)

Requested: improve the SSH login banner ASCII art for Bandit so it matches
each level's own title/theme while staying within Bandit's overall visual
theme, and do the same for Krypton with its own distinct track theme.
Notes only, no code changed.

## This is already implemented on current `main` -- the request appears to describe a feature that exists but hasn't reached players yet

Checked `CEI-Labs-Wargames` at `main` (`f4d9291`):

- `targets/bandit/build/generate_banners.py` — per-level `TITLES` dict
  (all 34 levels, reviewed display titles like "Spaces in Places",
  "Hidden in Plain Sight", "SUID Escalation"), per-level `ART` dict (small
  hand-designed ASCII pieces themed to each level's actual technique, e.g.
  level 2's grid-with-missing-cells for "spaces in filenames", level 19's
  ascending stairs for privilege escalation), and a progressive
  warm-color `_PALETTE_TIERS` ramp (amber -> ember -> dusk -> maroon)
  applied across the level range — a consistent "warm" identity across
  the whole track while each level's art differs.
- `targets/krypton/build/generate_banners.py` — same structure: per-level
  `TITLES`/`ART` for all 6 levels, plus its own `COLOR` dict, explicitly
  commented as "deliberately NOT the warm ramp Bandit uses and NOT plain
  green... Krypton starts icy blue... cools further into cyan before
  crossing into magenta/violet" — a distinct cool-toned track identity,
  separate from Bandit's, exactly matching "krypton is a different overall
  theme" from the request.

Both generators render the level's own title directly into the banner
text (`"CEI Labs Bandit %d: %s" % (level, title)` /
`"CEI Labs Krypton %d: %s" % (level, title)`), so the banner and the
CTFd challenge title are the same string, not independently maintained
copies that could drift.

This matches the request's description closely enough that this may
already be considered done from a content standpoint — the open question
is deployment, not implementation.

## The gap: the deployable target images are stale

Checked the already-built local image
`ghcr.io/stoptalkingishh/cei-labs-wargames/bandit:offline`:

```
$ docker inspect ghcr.io/stoptalkingishh/cei-labs-wargames/bandit:offline --format '{{.Created}}'
2026-07-22T17:03:37Z

$ docker run --rm --entrypoint sh ghcr.io/stoptalkingishh/cei-labs-wargames/bandit:offline \
    -c "cat /etc/cei-labs/banners/bandit2"
cat: /etc/cei-labs/banners/bandit2: No such file or directory
```

This image predates the banner-art work (merged 2026-07-23) and doesn't
even have the per-level banner files generated at all. Since this is the
image tag (`:offline`, org `stoptalkingishh`) the venue box's
`docker/.env` is actually configured to use, whatever target image the
orchestrator is currently spawning per-team Bandit/Krypton instances from
is very likely this same stale build — meaning players connecting via SSH
right now would see old/generic banners, not the themed art already
sitting in source.

## What closing this needs

Not a content-authoring task at this point, since the content already
exists — just a rebuild-and-redeploy:

- Rebuild `targets/bandit` and `targets/krypton` target images from
  current `CEI-Labs-Wargames` `main` (both Dockerfiles run
  `generate_banners.py` at build time, per
  `targets/bandit/Dockerfile:74-76` and the Krypton equivalent).
- Push/tag them to wherever the venue box's orchestrator actually pulls
  target images from (confirm exact registry/tag convention against
  `docker/.env`'s `GITHUB_ORG`/`IMAGE_TAG` and how the orchestrator
  resolves target image references — not fully traced in this pass).
- Verify live via an actual SSH login (not just `docker run --entrypoint
  sh` inspection) that the new banner renders correctly end-to-end,
  including color codes in a real terminal.
- If this rebuild reveals the running box's target images are stale
  across the board (not just Bandit/Krypton banners), that's a broader
  finding worth its own note — this pass only checked the one image
  already sitting on this machine, not a full inventory of what's stale
  on `192.168.1.173` specifically.
