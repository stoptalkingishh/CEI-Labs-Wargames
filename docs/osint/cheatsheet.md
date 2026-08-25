# OSINT — Instructor Cheat Sheet

Fast-lookup for walking the room during a session. One row per challenge: what it
tests, the one-line nudge, and the core tool/technique. Full solutions live in
`writeups.md`. In-platform 3-tier hints are the first pointer for a stuck player;
this sheet is for when you need the answer in your own head faster than reading a
hint.

Answers below are **illustrative placeholders** — swap them at release time (see
`docs/osint/README`); they are stored once in `scripts/build_osint.py` and must be
re-verified against real, legal public sources before releasing.

| Level | Skill & objective | If they're stuck, point them at... | Core tool / method |
|---|---|---|---|
| start-here | truth of the legal-PAO boundary; set up the local workspace | "OSINT only uses legal, publicly-available info — no phishing, no guessing databases." | Read the track intro; confirm their workspace |
| 01-geolocation | identify a place from one image | "Read the buildings, signage, and climate — then match block-by-block on Street View." | Google Earth / Street View |
| 02-reverse-image | provenance of a photo | "Reverse-search the *original* file, not the re-saved screenshot." | Google / Yandex reverse image |
| 03-chronolocation | time of day from shadows | "Use the sun's azimuth and shadow ratio, then SunCalc it." | SunCalc |
| 04-satellite-fire | locate a fire / thermal | "That's a 30 m thermal-anomaly layer — open FIRMS." | FIRMS / NASA GIBS |
| 05-exif | metadata & date/device | "Open the file's metadata — it'll tell you the device and the date." | EXIFTool / EXIF viewer |
| 06-calendar | non-Gregorian date | "That 'year' isn't a Gregorian one — what's the local official calendar?" | calendar converters, translator |
| 07-aviation-icao | ICAO code from the airport | "Runway + tail number, then check the ICAO registry/history." | FlightRadar / Planespotters / ICAO |
| 08-maritime-ais | identify and trace a vessel | "That's a ship track — pull the IMO and its port history." | MarineTraffic / VesselFinder / IMO |
| 09-what3words | precise spot as a triple | "Encode the pin to a 3-word address." | what3words |
| 10-web-archive | recover "old" web state | "The current page is new — capture must still be public." | Wayback Machine / newsDB |
| 11-social-footprint | legal profile + linkage | "Only *public* posts and accounts — no paywalled/harvested PII." | profile + search, network map |
| 12-corroborate | corroborate + reliability | "Don't stop at the first hit — 2+ independent sources & score it." | cross-check + a reliability scale |