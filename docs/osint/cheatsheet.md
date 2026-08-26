# OSINT — Instructor Cheat Sheet

Fast-lookup reference for walking the room during the **42-lead "Gilded Hose"
campaign** (see `storyline.md`). One row per lead: what it tests, the one-line
nudge to give someone who's stuck, and the core technique in a few words. Not a
substitute for the full answer key (`writeups.md`, same folder).

Answers below are **illustrative placeholders** — swap them at release time (the
single source of truth is the `FLAGS` dict in `scripts/build_osint.py`), and
re-verify against real, legal public sources before releasing.

| Lead | Faction | Goal | If they're stuck, point them at... | Core technique |
|---|---|---|---|---|
| 00 start-here | Tiberian Order | Learn rules + tools | "OSINT = legal public info only. No phishing, no PII harvesting." | PAI / legal boundary |
| 01 cartel-airdrop | Cartel | Locate coastal drop lane from satellite still | "Read coastline shape + street grid, not colors." | IMINT geolocation |
| 02 cartel-safehouse | Cartel | Pin downtown address from one photo | "Smallest clue wins: signs, district, house number." | Street-view geolocation |
| 03 cartel-precursor | Cartel | Find original image source | "Reverse-search the ORIGINAL file, never the screenshot." | Reverse image / provenance |
| 04 cartel-meet | Cartel | Decode seized file to meeting spot | "It's not text — hex round-trip it; two images hide inside." | Hex decode → geo → what3words |
| 05 synd-exfil | Syndicate | Recover exfil URL from capture | "Look at DNS lookups — a pastebin/raw URL hides there." | PCAP/DNS analysis |
| 06 synd-intercept | Syndicate | Extract meet time/place from intercept | "Find the shared link inside the pcap, then decode." | PCAP + decoding |
| 07 synd-beacon | Syndicate | Break layered cipher for coordinates | "Base85 first, then Vigenère with the recovered key." | Base85 → Vigenère |
| 08 synd-burn | Syndicate | Rebuild timeline from browser artifacts | "History + bookmarks each hold a word fragment." | Browser forensics (SQLite) |
| 09 synd-wallet | Syndicate | Multi-stage decrypt email to target coord | "Strict order: Base64 → decimal → Vigenère." | Layered decryption |
| 10 synd-deaddrop | Syndicate | Reassemble hidden short-link | "Scan for URL fragments; case matters." | Hidden-URL reassembly |
| 11 gen-tank | Generals | ID armored vehicle from drone still | "Hull, turret, gun layout — match a recognition guide." | AFV identification |
| 12 gen-frigate | Generals | Classify unmarked warship | "Sensor + weapon layout maps to a class + NATO name." | Naval vessel ID |
| 13 gen-airfield | Generals | Locate air base, structure hierarchy | "Hangars/runways on satellite; then country→region→base." | Air-base geolocation |
| 14 gen-aircraft | Generals | ID airframe, current base + history | "Planespotters gives current AND past deployments." | Aviation registry history |
| 15 chan-strike | Chancellery | Synthesize bases+person+time | "Translate first; the day/time is stated in the briefing." | Geo + translation + temporal |
| 16 chan-ao | Chancellery | Geolocate NGO facility in an AO | "Constrain to corridor, match facility type to NGO registries." | AO-scoped facility search |
| 17 chan-smuggle | Chancellery | Stego-extract coordinates | "The marker number IS the stego password." | Steganography → geo |
| 18 chan-fleet ★ | Chancellery | Vessel ID + port history from IMINT | "Query coord/time on AIS; verify IMO visuals; replay ports." | IMINT ↔ AIS fusion |
| 19 chan-manifest | Chancellery | Derive password from vessel metadata | "Ship name + build year unlocks the beacon log." | Metadata inference + telemetry |
| 20 chan-cover | Chancellery | Corroborate aerial photo with history | "Match building silhouette, cross-check historical event clues." | Aerial geo + historic corroboration |
| 21 hades-operative | Hades | Locate defector's hotel from photos | "Hotel name → city → listing phone on Maps." | Photo geo + enrichment |
| 22 hades-cutout | Hades | Decode hidden location string | "The message rides INSIDE the aerial image's text layer." | Encoding decode + verify |
| 23 hades-payment | Hades | IP → imagery → what3words pivot | "IP geolocates the city; fix the extension to see the photo." | IP pivot + street view + w3w |
| 24 hades-hostage | Hades | Strict cipher stack to w3w location | "Order matters: Base64 → ROT47 → hex → substitution table." | Multi-layer cryptanalysis |
| 25 hades-hit | Hades | Pin park/path intersection | "City parks first, then trail intersections." | Park geolocation |
| 26 hades-slayer | Hades | Four points → centroid → riddle → address | "Plot all four; the X marks the spot; solve the riddle next." | Centroid analysis + w3w |
| 27 ash-strike | Ashfall | Fuse conflict-map + infra docs | "Conflict map event → substation name → rating docs." | Conflict-map fusion |
| 28 ash-distress | Ashfall | Morse distress → what3words | "Transcribe callsign first; the phrase IS the triple." | Morse decoding |
| 29 ash-freelancer | Ashfall | Trace person across platforms to address | "Pub → translate speech → reviews by name → social handle → address." | Cross-platform footprint |
| 30 cult-funnel | Cult | Exact record URL from sparse IDs | "Filter by date/place/shape in the reporting DB." | Public-DB research |
| 31 cult-origin | Cult | Recover one old article URL | "Distinct key-phrases + site-scoped search." | Archival web search |
| 32 cult-signal | Cult | Spectrogram → hex → site → facility | "Open audio in a spectrogram; the hex decodes to a site." | Audio forensics chain |
| 33 cult-cipher | Cult | Translate invented script to credential | "Use their language-picture key literally." | Cipher translation |
| 34 cult-caravan | Cult | Street from tourist photo | "Landmarks/signs → candidate city → Street View verify." | Street-view verification |
| 35 cult-ledger | Cult | Identify classical source of text | "Translate; the phrasing betrays the ancient author." | Translation/provenance |
| 36 cult-prophecy | Cult | Location + decoded script + year chain | "Palace photo → font decoder → parse place + year clues." | Font decoding + temporal |
| 37 cult-relic | Cult | Mine metadata for credential | "EXIF/container metadata holds the embedded string." | EXIF forensics |
| 38 cult-money | Cult | Staged jigsaw → w3w → vault pass | "Each stage hands you the next; vault takes the first words." | Staged chain resolution |
| 39 cult-cache | Cult | Landmark → w3w + area code | "Identify the landmark; local dialing code + triple = unlock." | Landmark + w3w |
| 40 loom-corroborate | Loom | Corroborate with 2 independent sources | "One hit isn't proof — find a second and score both." | Reliability scoring |
| 41 loom-assess ★ | Loom | Name the coordinating network, sourced | "Recurring cover company + port lane + wallet + dead drops." | Fused assessment (capstone) |

★ = centerpiece/capstone leads.

## Pacing guide

- Arcs 1–2 (cartel/syndicate): warm-up tier, ~8–10 min per lead.
- Arcs 3–4 (generals/chancellery): mid-tier multi-step chains, ~10–15 min.
- Arcs 5–6 (hades/ashfall): harder chains incl. cryptanalysis, ~10–15 min.
- Arc 7 (cult): long tail of varied skills, ~8–15 min.
- Arc 8 (loom): capstone pair, ~15 min combined if teams kept notes.
