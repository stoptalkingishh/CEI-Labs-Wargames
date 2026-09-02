# Threadline - Learning Objectives

A skills inventory for the OSINT track (12 drills + a Start Here), organized by
concept rather than level number, so it can be referenced by skill gap. Every
skill is paired with the U.S. Army intelligence doctrine it teaches (see
`threadline-research-index.md` §4 for the doctrine vocabulary). Pairs with
`writeups.md` (answer key) and `cheatsheet.md` (fast lookup) in this folder.

## Geolocation / imagery analysis (drill 1, 4, 9)
- Identify a place from a single photograph using architecture, signage,
  terrain, climate and road layout (plain visual geolocation).
- Confirm a coordinate/spot against ground truth (Street View, maps,
  satellite) and record the reasoning chain.
- Convert between a precise spot, a what3words triple, and latitude/longitude.
- Use satellite/thermal layers (FIRMS-style 30 m fire anomalies) to locate an
  event and correlate it with a map.
- Doctrine: GEOINT/IMINT capture; FM 2-0 IPB geospatial interrogation.

## Reverse & similarity imaging (drill 2)
- Use reverse image search on the *original* media file, not a screenshot.
- Find the earliest/source appearance and infer provenance/date.
- Detect a re-encoded or manipulated image.
- Doctrine: source provenance / authentication (ATP 2-22.9), IMINT.

## Temporal & chronolocation (drill 3, 6)
- Bound time-of-day using sun position and shadow length (SunCalc).
- Convert between calendars (Gregorian <-> Solar Hijri / Bikram Sambat /
  Ethiopian) to date an event.
- Reconstruct a date/time from embedded or environmental clues.
- Doctrine: IPB temporality / treatment planning (ADP 2-0 cycle).

## Metadata / EXIF (drill 5)
- Read EXIF from media (device, date, GPS) and judge whether it's usable or
  honestly stripped.
- Understand "eat it fresh": public content volatishly captured and
  timestamped at observation time.
- Doctrine: processing & exploitation, source integrity (FM 2-0).

## Aviation & maritime (drill 7, 8)
- Use registry/tail/ADS-B/FlightRadar to identify an aircraft and its airport
  (ICAO), and a carpet/aircraft subtype.
- Use AIS (MarineTraffic / VesselFinder), IMO registry, and port records to
  trace a vessel's track, flag and history.
- Doctrine: multi-M INT corroboration + target development, VMS/AIS trajectory.

## Foundation file format web (drill 10)
- Use the internet archive / Wayback and newspaper databases to recover
  deleted, older, or "known-but-changed" content.
- Reconstruct a prior state / "pattern of life" from proxies.
- Doctrine: archive "eat it fresh" (ATP 2-22.9).

## Social footprint (drill 11)
- Legally enumerate a target's public footprint and build a node-link picture,
  respecting the PAI / legally-protected / PII boundary.
- Recognize risk of fabrication, sock puppets and impersonators.
- Doctrine: social-media exploit (ATP 2-22.9), HUMINT-adjacent baseline within
  CI limits (FM 2-0), OPSEC.

## Cross-verification & reliability (drill 12, capstone)
- Score independent sources on reliability & credibility and flag
  contradictions before committing to an assessment.
- Produce a short CIVST / sourced "product" that cites date, time, origin.
- Tie all the earlier drills into one corroborated judgement.
- Doctrine: corroboration and all-source fusion; the OPSEC reliability scale
  (FM 2-0 / ATP).

## Start-Here
- Explain that OSINT uses legal public (Priadically Available Information) only,
  state which tools open the browser, and confirm the participant set up the
  (git-ignored) `osint/` environment or their own practice workspace.