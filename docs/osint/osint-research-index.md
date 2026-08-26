# OSINT Wargame — Source & Doctrine Research Index

Working index behind the new **OSINT** wargame track. It catalogs real Open-Source
Intelligence exercises and CTFs from the four source bodies named in the project
request, records what each one teaches, which tools and methodology the solver
uses, and maps every skill back to the U.S. Army intelligence doctrine the track
uses as its learning-objective language (ATP 2-22.9 *Open-Source Intelligence*,
FM 2-0 / ADP 2-0 *Intelligence*).

This document is the *research picture*; `docs/osint/` itself (plus
`scripts/build_osint.py` and the `osint/` import output) is the wargame built
from it.

- [1. Sources](#1-sources)
- [2. OSINT skill taxonomy (recurring across all sources)](#2-osint-skill-taxonomy)
- [3. Challenge-by-challenge index](#3-challenge-by-challenge-index)
- [4. Doctrine mapping (ATP 2-22.9 / FM 2-0 / ADP 2-0)](#4-doctrine-mapping)
- [5. Toolbox / tool to skill to doctrine](#5-toolbox)
- [6. Design implications for the OSINT wargame](#6-design-implications)

---

## 1. Sources

| Source | What it is | Value to this track |
|---|---|---|
| `hacktoria-archive/` (51 zips) + `hacktoria.com/tag/ctf-events` | Narrrated, fictional OSINT "operator" contracts (a leaked-agent, cartels, naval, UFO-cult storylines). Each zip carries a briefing, starting imagery, and the platform's own `write-up-*.md` ground truth | Real task shapes & difficulty ladder: briefing -> package files -> geolocate/AIS/act-decoded datum -> final flag string. Great model for story-driven military scenario design |
| `gralhix.com/list-of-osint-exercises` (#001-#032) | Sofia Santos' free "OSINT Exercise #NN" suite, each with video walkthrough | Cleanest *single-skill pedagogy*: geolocation, chronolocation/sun-shadow, satellite thermal, EXIF, calendar conversion, aviation |
| `challenge.bellingcat.com` (105 puzzles, ~13 skill families) | Interactive OSINT training by the Bellingcat collective; themed puzzle series (Geolocation, Satellite Imagery, Historic, Munition Analysis, Audio, ...) | The **"VITA + ground-truth corroboration"** method and the "media file as a question" meta — the most transferable analyst habit |
| US doctrine | ATP 2-22.9 (2012, Chg 1 2022), FM 2-0 (2022), ADP 2-0 (2019) | The **intelligence cycle / collection-plan language** used to phrase every challenge's learning objectives (see §4). Live public PDFs are PAI-restricted (403 on armypubs), so this is grounded in established published content |

---

## 2. OSINT skill taxonomy (recurring across all sources)

Ranked roughly by how often the sources drill the skill. These map 1:1 to the
challenge set in the wargame.

| # | Skill | Description | Representative sources |
|---|---|---|---|
| 1 | **Geolocation / IMINT** | Pinning a photo/map to a coordinate or named place from visual + spatial cues | Hacktoria (Lost in Time, Midnight Slayer, Prisoner of War, "omega strand" series), Gralhix #001/#003/#019/#026/#028, Bellingcat (most Geolocation puzzles) |
| 2 | **Maritime / AIS vessel tracking** | Following a ship's AIS track, IMO registry, port history, hull/class ID | Hacktoria (Undercover Fleet, Naval Intrusion, Lost at Sea, Intro to Maritime OSINT) |
| 3 | **what3words / coordinate geocoding** | Encoding a precise spot; used as the flag/answer format | Hacktoria (The Midnight Slayer, A Strange File, Kidnapped) |
| 4 | **Reverse & similarity image search** | Find source/duplicate/provenance of an image or face | Gralhix (#001, #003, #011), Hacktoria (Lost in Time) |
| 5 | **Chronolocation / sun & shadows** | Time-of-day from sun position/shadows; cross-check with calendar | Gralhix (#009, #013), Bellingcat (Chronolocation family) |
| 6 | **Satellite / remote sensing** | Landsat/Sentinel bands, FIRMS thermal, change detection | Gralhix (#012), Bellingcat ("Kind of Blue", Satellite Imagery tag) |
| 7 | **Aviation / airport (ICAO)** | Aircraft ID, flight tracks, airport runways, tail/ICAO codes | Gralhix (#032), Bellingcat ("Lost in the Fog", "Touching Tarmac"), Hacktoria (Last Flight) |
| 8 | **EXIF / metadata forensics** | Device/GPS/date from file properties; detecting stripping | Gralhix (#028), Bellingcat (VITA technique), ATP source-verif |
| 9 | **Maritime / vessel & vehicle recognition** | hull/cl add class ID from photos; NATO reporting names | Hacktoria (Naval Intrusion), Bellingcat (Transport) |
| 10 | **Calendar / date & non-Gregorian** | Converting Bikram/Hijri/Ethiopian dates; date archaeology | Gralhix (#017) |
| 11 | **Archival / historic / Wayback** | Dead content recovery via web archives & digital newspapers | Gralhix (#020), Bellingcat (Historic Research), leading to "pattern of life" |
| 12 | **Social footprint & link analysis** | Profiling an account/person, node->node connections, staying legal | Hacktoria (social media exploit), Gralhix (#010) |
| 13 | **Deep / structured web / DB search** | Boolean/search operators, grey-literature grep | Hacktoria (Chasing Bigfoot) |
| 14 | **Cryptanalysis / stego (SIGINT-adjacent)** | Encoding chains, what3words-from-encryption | Hacktoria (Emergency, Kidnapped; echo calls it ciphers) |
| 15 | **Corroboration / reliability scoring** | Weigh independent sources, provenance, deception | All Bellingcat + cross-check the "VITA" loop; ATP's reliability |

---

## 3. Challenge-by-challenge index

> Fields per row: **skill** (taxon §2), **tools** (public), **methodology** (what the player actually does), **doctrine** (see §4 tags).

### 3.1 Hacktoria (selected)

| Challenge | Skill | Tools | Methodology (solve path) | Difficulty |
|---|---|---|---|---|
| The Midnight Slayer | Geolocation / what3words (§1,§3) | Google Maps, what3words, satellite | Plot 4 body-drop locations, read the centroid "X" (a park), get a w3w triple; decode a riddle to a landmark + w3w for the flag | L1 map -> L2 centroid/w3w -> L3 riddle-bridge |
| A Strange File | Reverse-image geolocation + w3w | hex/string decoders, what3words, Maps | Hex-decode a file to recover two photos, geolocate the meeting place, snapshot with w3w + type | L1 format -> L2 geo -> L3 w3w + category |
| Lost in Time | Archival + cultural + timeline | Google Earth, font/symbol decoders, historical refs | Decode an in-universe script; cross three unrelated provenance clues into one place, building a hyphenated answer | L3 multi-cross-timeline |
| Last Flight | Aviation / aircraft lifecycle | Planespotters, ICAO codes, Google | Recognise the airframe (Jumbo Stay), trace its life/date history to identify when and where, format flag | L1 type -> L2 airframe / L3 date-country |
| Undercover Fleet | Maritime / AIS + registry | MarineTraffic, VesselFinder, IMO, ship images | Set coordinate/time, match a 16.5-knot track, verify visuals vs registry + IMO, replay port history | L1 AIS lookup -> L2 vessel/register -> L3 port path |
| Naval Intrusion | Vessel / class recognition | PLAN vessel catalogs, naval DBs, NATO names | Classify a hull's sensors to a ship class (e.g., Type 054A), then its exact NATO/taxonomy form | L1 look -> L2 -class -> L3-fmt |
| Prisoner of War | GEOINT scoped search | Earth/Maps, NGO registers, RN1 corridor | Plot a given coordinate, sweep the AO/corridor, identify an NGO facility/building from satellite + registry | L1 region -> L2 search / L3 facility-name |
| Emergency Transmission | SIGINT-adjacent + coords | Base85/Ascii85 decoder, Vigenere (key) | Decode layers, recover coordinates, form geo-flag | L2 decode -> L3 cross-cipher+geo |
| Kidnapped | Cryptanalysis + what3words | Base64, ROT47, hex, w3w | Strict stack decode (Base64 -> ROT47 -> hex -> subs) to a w3w triple | L2 strict-order decode -> L3 |
| Chasing Bigfoot | Web/DB deep search | DuckDuckGo, site-restricted faceting | Build unique key-phrases, filter on multiple constraints, retrieve the exact canonical URL | L1 scope -> L2 facet -> L3 exact URL |

### 3.2 Gralhix (Sofia Santos) exercises

| Ex | Skill | Tools | Methodology | Difficulty (Novice/Expert) |
|---|---|---|---|---|
| #001 Kiffa, Mauritania | Geolocation from one photo | Earth/Street View, Yandex reverse | Crop the original image, inventory paving/lamp/signs, match to Sahel city, then street-view Segment pin | Medium / Easy |
| #003 Somalia-Eir and Turkey | Reverse news + venue | Rome search captions (Anadolu), Ether | Reverse-search the news photo, identify the event/venue, cross-verify with more images, pin coords | Medium / Easy |
| #009 Tirana chronolocation | Chronolocation + source ts | SunCalc, Street View, page-source Inspect | Geolocate the street; use SunCalc for the time bound; read the author's upload source for a precise timestamp | Hard / Hard-adj |
| #005 Malcom | seasonal | Sun/Camber | *(foreground context)* — tie photography to date & season | Medium |
| #012 fire map | Satellite imagery | FIRMS/NASA GIBS | Recognise the 30m thermal anomaly layer, find the coast, pin date | Easy(b)/Hard / Easy |
| #017 calendars | Non-Gregorian dates | Translator + calendar converters | Detect lang/calendar; extract the in-URL native date; convert to Gregorian | Medium / Easy |
| #028 device + hotel | EXIF + geo + amenities | EXIF tools, Google Maps "measure", Street View, hotels | Device via EXIF; geolocate the street; measure distance; identify hotel | Varied (b Hard) |
| #032 airport TV | Aviation + date-time | Departure board glyphs, FlightRadar, terminal maps | Recover a date/time from live flight data; match terminal architecture to gate | Medium / Hard |

### 3.3 Bellingcat Challenge (representative)

| Puzzle | Skill | Solve | Method |
|---|---|---|---|
| Patina Pattern (#63) | Geolocation / object ID | Google Lens, Wikidata, heritage DB | ID a public sculpture then its sculptor; cross-check coords on street-view |
| Visible fog lossed (#5) | Geolocation + ICAO | OpenStreetMap, Wiki airport list, satellite | Read runway/geometry in a foggy frame, enumerate candidate ICAO airports |
| Cold Rocking (#80) | micro-geolocation | OSM shop tags + Maps | Extract few clues, bound a neighborhood, OSM to enumerate targets |
| Shanty Province / Royal (#76) | statue->street | Wikimap reverse-address, OSM | Geoliterate the statue, then reverse-geocode the street behind the camera |
| Kind of Blue (#24) | Satellite image + SWIR | Sentinel band combos, atlases | Interpret multi-band water signature, name the topographic depression |
| Lost / Obscure production (#6) | Historic research | Accession DB, Lost Art Register, newspapers | Trace a wartime provenance, reconcile the exact date record |

---

## 4. Doctrine mapping (ATP 2-22.9 / FM 2-0 / ADP 2-0)

Concepts used as the **learning-objective language** for the OSINT track.

**ATP 2-22.9 — Open-Source Intelligence**
- OSINT = "intelligence produced from publicly available information (PAI) collected, exploited and disseminated in a timely manner to answer specific intelligence requirements (IRs)."
- Legally-available vs **legally-protected / proprietary / PII** line — a hard collection boundary (the "OSINT legal" rule).
- The OSINT process is **discovery -> collection/exploitation -> validation -> fusion**, not "googling".
- **"Eat it fresh"** — PAI is volatile; capture, timestamp, archive at observation time (Wayback discipline).
- **Social-media exploit** — turn a passing public post into drifted bytes; authenticating the source/account.

**FM 2-0 / ADP 2-0 — Intelligence**
- The **intelligence cycle**: planning & direction -> collection -> processing & exploitation -> analysis & production -> dissemination -> (feedback).
- **Collection management / collection matrix** — OSINT as a tasked asset like any other.
- **IPB** — intelligence preparation of the battlefield; terrain/ground-truth corroboration.
- **Targeting** — OSINT as the "dashboard" for target development/detection.
- **Analytical tradecraft** — multi-INT/all-source fusion, reliability & legal rating, structured reasoning.
- **INT taxonomy** — OSINT alongside HUMINT, SIGINT (COMINT/ELINT), IMINT, MASINT, GEOINT, CYBINT.

### 4.1 Skill -> doctrine table (the tag set used in the wargame)

| Skill | ATP 2-22.9 anchor | FM / ADP anchor | Learning-objective phrasing | Cleanup tags |
|---|---|---|---|---|
| Geolocation / IMINT | geo-context from GoP | spatial / IPB geospatial | triangulate an image to coordinates, cite reasoning | GEOINT, IMINT, corrosion |
| Chronolocation / sun-shadow | date-time verification of a PAI record | analytic dict | infer time-of-day/shadows + solar position | timestamp, temporal |
| Satellite thermal (FIRM/VItere) | commercial open IMINT | multi-INT corroborate | locate heat signature on a thermal map, confirm on ground | Thermal MASINT ammas |
| Reverse / similarity image | capture + provenance | unknown | use reverse-image to find the source appearance/provenance | provenance, manipulate |
| Aircraft / aircraft-vessel | open baseline PAI | IMINT corrosion + target | identify air subtype | target acq, IMINT |
| Maritime / AIS | PAI commercial AIS/VMS | mixed GEOINT/SIGINT | trace AIS track, reverse the ship/owner | AIS, trajectory |
| what3words / geo-coding | geospatial rif | decode/dis | convert a w3w triple to a map point | GEOINT, geocode |
| Social media footprint | social media exploit, PII | HUMINT-adjacent, CI-boundary | profile + unwrap a personal target account legally | HUMINT-adjoin, PII, foot |
| EXIF / metadata | capture/authentication of PAI | processing (integrity) | extract EXIF, decide whether it's truthful | foster, provenance |
| Calendar / non-Gregorian | temporal resolution | IPB | convert calendars to place an event in time | temporal |
| Archived / Internet | "eat it fresh" | social exploitation, baseline | recover several deleted state via Wayback, pattern of life | archive, PAI |
| Deep / DB web search | DO-INT discovery / collection | collection mgmt | Boolean/DB search to undisclosed grey records | discovery, RFI |
| Cryptography/stego | hidden PAI / deception | analytical | a simple cipher, flag it as indicator | IND |
| Urban ground-truth | PAI imagery->terrain | IPB | verify with street-view + maps, note a false positive | terrain, ground-truth |
| Cross-verification / anonymity | corroboration + reliability | OPSEC "A-F" scale | score each source on a credibility scale, flag contradiction | reliability, osteo |

---

## 5. Toolbox (skill → tool → doctrine)

| Tool | Skill | Notes |
|---|---|---|
| Google Earth / Maps / Street View | Imagery geolocation, urban corroboration, reverse-address | Core everywhere |
| What3Words | precise flag/coordinate format | Geography as an answer string |
| SunCalc | chronolocation | sun-highlight business |
| FIRMS (NASA) / GIBS / Sentinel Hub | fire / thermal & multi-band | IMINT/ remote footprint |
| MarineTraffic / VesselFinder / IMO | maritime AIS, registry, history | shipping / SIGINT-ish GEOINT |
| FlightRadar24 / ADSBExchange / Planespotters / ICAO | aviation / aircraft / airport | aviation |
| Yandex / Google / Bing reverse image | provenance, face nickname | source recovery |
| EXIFTool / online EXIF | metadata / tampering | "eat it max" |
| Wayback Machine / arXiv / newsDB | archive & history, "eat it fruit" | pattern of life |
| Sherlock / web landing / OSI | social-media profile, footprint, legal | basin |
| CyberChef | decoding chains (Base64, ROT47, Vigenere, etc.) | SIGINT-adjacent |
| Satellite / thermal ... (see above) | — | — |

---

## 6. Design implications for the wargame

1. **No shared target box is needed** — every skill runs against the public web and the player's own machine. The OSINT track therefore joins the AI Copilot Setup track as a **non-staged, hidden-by-default** track rather than the three staged games: no per-team Docker instance, no orchestration, flags are the *produced answer* (the "work is the proof," so a static flag is defensible).
2. **Skill ladder** reused from the sources: Tier A (single-tool direct answer) -> Tier B (one transform: decode-then-geo) -> Tier C (multi-clue cross-toolchain / a "mini case" requiring corroboration).
3. **Every challenge carries the doctrine vocabulary** from §4 in its learning-objectives doc, so a participant can trace each flag back to an ATP/FM concept (this is the OS-Schoolhouse hook).
4. **Legal boundary is a first-class objective** — at least one challenge and the player quick-start make the ATP "legally available vs legally protected / PII" line explicit, mirroring the AI track's own "do not message users" rule.
5. **Corroboration / reliability is the capstone node** — a later challenge asks the driver to produce a sourced judgement string (bodies of a "product"), closing the cycle.

The build: start with `scripts/build_osint.py` (generates the `osint/` import), tune difficulty from the writeup traces above, and release the track hidden-by-default exactly like the AI Copilot track.