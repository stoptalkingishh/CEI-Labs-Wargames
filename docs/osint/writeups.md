# OSINT — Writeups (Answer Key)

**Instructor / organizer only — not for participant distribution.** Every answer
below is an **illustrative placeholder** chosen to make the challenge definition
self-consistent; before a production release, swap each for values *verified
against real legal public sources* at release time (single source of truth: the
`FLAGS` dict in `scripts/build_osint.py`; the generator re-emits these into
`osint/*`).

Each level: **objective**, **method (what the participant does)**, **flag**.

---

## osint-start-here — Onboarding
- Objective: confirm the track uses only legal public information (PAI), set up the local practice workspace.
- Method: read the track intro; verify the participant can reach public OSINT tools in their browser.
- Flag: `WELCOME TO OSINT`

## osint-01-geolocation
- Objective: name/coordinate a place from a single image.
- Method: open the photo; inventory architecture, signage, road layout, climate; narrow to a candidate city; match block-by-block on Street View; record the place.
- Flag: `place` (placeholder: `eiffel-tower-paris`)

## osint-02-reverse-image
- Objective: find the source/provenance of a media file.
- Method: reverse-image search the **original** file; find first/oldest appearance; identify the source/creator.
- Flag: `creative-work-placeholder` (placeholder: `starry-night-van-gogh`)

## osint-03-chronolocation
- Objective: estimate the time of day from solar clues.
- Method: measure shadow length/direction; use SunCalc for the location+date to bound a time.
- Flag: `time-of-day-placeholder` (placeholder: `afternoon-4pm`)

## osint-04-satellite-fire
- Objective: locate a thermal event on satellite imagery.
- Method: recognize the 30 m fire/anomaly layer; open FIRMS; find the fire/cluster; map to the named location.
- Flag: `location-placeholder` (placeholder: `california-wildfire-2023`)

## osint-05-exif
- Objective: extract and judge device/date metadata.
- Method: run the file through an EXIF reader; read camera model + capture date; note trust/alteration.
- Flag: `device-date-placeholder` (placeholder: `canon-r5-2026-09-14`)

## osint-06-calendar
- Objective: convert a non-Gregorian to a Gregorian date.
- Method: recognize the calendar (Hijri/Solar Hijri/Bikram/Ethiopian) from the source; convert; cross-check the event.
- Flag: `gregorian-date-placeholder` (placeholder: `2024-01-12`)

## osint-07-aviation-icao
- Objective: identify an airport from a photo/comb of aircraft.
- Method: read the tail/Registration + runway geometry; query an aircraft/airport DB; output the ICAO code.
- Flag: `icao-placeholder` (placeholder: `egll`)

## osint-08-maritime-ais
- Objective: identify a vessel and trace a track.
- Method: query the coordinate/time on AIS data (MarineTraffic/WesselFinder); get IMO/name; replay the port history.
- Flag: `ship-placeholder` (placeholder: `imo-9758351`)

## osint-09-what3words
- Objective: convert a precise pin to a 3-word address.
- Method: read the plan background, geocode the spot, then w3w it.
- Flag: `triple-placeholder` (placeholder: `index.focus.fresh`)

## osint-10-web-archive
- Objective: recover a changed/delated web state.
- Method: find the URL’s Wayback snapshots; pick the dated capture nearest the incident; read the old state.
- Flag: `snapshot-placeholder` (placeholder: `snapshot-2005-03-11`)

## osint-11-social-footprint
- Objective: legally map a public footprint and link profiles.
- Method: only public posts/accounts; gather handle -> platform; build a link map; note impersonators/PII limits.
- Flag: `profile-placeholder` (placeholder: `verified-profile-2022`)

## osint-12-corroborate (capstone)
- Objective: corroborate a lead with 2+ independent sources, score it, issue a short sourced "product".
- Method: take the lead, find two independent sources and one contradiction-check; score reliability; produce a one-paragraph CIDST-style product string.
- Flag: the corroborated product (placeholder: `corrob-two-sources`)