# OSINT Pilot

CEI-Labs exports a small, neutral OSINT pilot from the separately maintained `ctfgen-family-osint` package. CTFGenerator remains the deterministic artifact engine; this repository owns only the CTFd adapter and event release state.

## Current pilot

The initial pilot contains the plugin's three reviewed artifact dossiers:

1. image provenance/geolocation;
2. vessel or aircraft movement corroboration;
3. public-record/entity corroboration.

The adapter copies only `public/` artifacts into player-downloadable files. Canonical answers are derived from the plugin's private typed verifier specification and written once to generated CTFd metadata. No private solution, ground truth, or provenance file is copied into the player bundle.

## Evidence gate

The previous 42 proposals were placeholders: their original evidence packages are absent from this repository. They are not releaseable and are preserved only as neutral skill ideas in [`archive/legacy-idea-bank.json`](archive/legacy-idea-bank.json). A proposal may return only after its evidence, provenance/license, archived fallback, safety/privacy review, canonical verifier, and playtest timing are complete in the plugin.

No storyline or cross-project lore is part of this track.

## Build

Install the trusted host and private plugin, then run:

```bash
CEI_OSINT_RELEASE_STATE=hidden python3 scripts/build_osint.py
```

Set the state to `visible` only after organizer review. Output is written to the ignored `osint/` directory for `ctf challenge sync osint/`.
