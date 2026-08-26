#!/usr/bin/env python3
"""Generate the OSINT wargame track (a full 6-7 hour campaign).

OSINT is a deliberate **non-staged, hidden-by-default** track, exactly like the
AI Copilot Setup track (`build_agent.py`): its "target" is the public web and
the participant's own workstation, so there is no per-team Docker instance, no
orchestrator mapping, and it contributes 0 instance mappings. It is therefore
NOT a fourth stage in game-stages.yml and is never validated by
validate_game_stages.py / validate_generated.py (which only read `challenges/`;
this generator writes to the git-ignored `osint/` directory instead).

Because getting an OSINT answer *is* the work (the player must geolocate,
decode, and corroborate), the flags here are static but low-risk for collusion --
the same rationale the AI Copilot track already documents. The track stays
hidden until the organizer releases it manually (mirroring
`CEI_AGENT_RELEASE_STATE=visible`).

STORYLINE
---------
Every lead belongs to one faction in the "Gilded Hose" meta-plot (see
docs/osint/storyline.md). The player is a Tiberian Order analyst resolving one
short lead at a time (5-15 min each) across a discovery board. The factions:

  CARTEL   = Crimson Cartel / Los Aztecas (narcotics & goods)
  SYND     = Wire Syndicate (hackers, crypto laundering)
  GEN      = Gilded Generals (corrupt military selling tech)
  CHAN     = the Chancellery (corrupt politicians brokering trade)
  HADES    = Order of Hades (original master-villain org)
  ASH      = Ashfall (terrorist cells)
  CULT     = House of Krohndahkyr (doomsday cult + money funnel)
  LOOM     = the hidden connector (capstone arc)

Each challenge's description carries (1) a short fictional framing paragraph,
(2) the real OSINT premise, (3) the method/tools, and (4) a placeholder-note.
The fiction is framing-only and never adds solve steps, so every lead stays a
5-15 minute solve.

IMPORTANT / LEGAL: the landing/answer strings below marked PLACEHOLDER are
illustrative, self-consistent values for building the challenge definitions.
Before any production release, re-verify every answer against real, legal,
publicly-available sources and swap them here (single source of truth) -- never
by hand-editing generated files.

Usage:
    python3 scripts/build_osint.py
"""
import json
import os
import sys

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
BASE_DIR = ROOT / "osint"

RELEASE_STATE = os.environ.get("CEI_OSINT_RELEASE_STATE", "hidden")

# ---------------------------------------------------------------------------
# Challenge authoring helper
# ---------------------------------------------------------------------------


def mk(arc, faction, skill, tier, doctrine, cid, name, points, framing,
       premise, method, tools):
    """Build one lead's full description from parts (DRY)."""
    desc = "\n".join([
        framing.strip(),
        "",
        "**Premise.** " + premise.strip(),
        "",
        "**Method.** " + method.strip(),
        "",
        "**Tools you may need (free):** " + tools.strip(),
        "",
        "FICTION FRAMING ONLY -- the answer is a real, verifiable place/value.",
        "PLACEHOLDER ANSWER (verify against a real source at release).",
    ])
    return {
        "id": cid,
        "name": name,
        "points": points,
        "desc": desc,
        "arc": arc,
        "faction": faction,
        "skill": skill,
        "tier": tier,
        "doctrine": doctrine,
    }


# ---------------------------------------------------------------------------
# The campaign: ~45 leads across the storyline arcs
# ---------------------------------------------------------------------------

F = []  # the ordered lead list

# ---- ARC 0 : Onboarding ---------------------------------------------------
F.append({
    "id": "osint-00-start-here",
    "name": "Wargame Briefing (Start Here)",
    "points": 10,
    "desc": (
        "Welcome, analyst. You are joining the **Tiberian Order** -- the "
        "intelligence service that fields every lead on this board.\n"
        "OSINT means intelligence produced legally from publicly available "
        "information (PAI). Its only boundaries are law and ethics: no phishing, "
        "no credential hacking, no harvesting protected PII, and never "
        "messaging or social-engineering a real target.\n"
        "This track has no server box. Your target is the public web and your "
        "own local tools.\n"
        "Tools + method (free): Google Maps / Earth, reverse-image engines, "
        "EXIFTool, what3words, FIRMS/NASA GIBS, MarineTraffic/VesselFinder, "
        "FlightRadar24/ICAO, the Wayback Machine, and CyberChef.\n"
        "Prove you read this by entering the phrase below."
    ),
    "arc": "0-onboarding",
    "faction": "tiberian-order",
    "skill": "onboarding",
    "tier": "A",
    "doctrine": "PAI / legal boundary",
})

# ---- ARC 1 : Crimson Cartel (the goods lane) ------------------------------
F.append(mk(
    "1-cartel", "cartel", "IMINT geolocation (air-drop lane)", "A",
    "GEOINT/IMINT, IPB ground-truth",
    "osint-01-cartel-airdrop", "Cartel Air-Drop Lane", 100,
    "A DEA-confiscated satellite still shows a remote coastal drop point used "
    "by the Crimson Cartel's air corridor.",
    "Single satellite frame of an unmarked cocaine air-drop lane; identify the "
    "country/region and the exact coastal point.",
    "Read street grid, coastline shape and landmarks in the overhead view; match "
    "against public satellite imagery; narrow to the exact coastal drop point.",
    "Google Earth / Google Maps satellite.",
))
F.append(mk(
    "1-cartel", "cartel", "IMINT geolocation (safehouse)", "A",
    "FM IPB/ground-truth",
    "osint-02-cartel-safehouse", "Cartel Safehouse", 100,
    "A distress photo from inside a cartel safehouse leak reveals a downtown "
    "beach-house address.",
    "Downtown photo of the safehouse; identify the street address (beach house, "
    "street signs, district).",
    "Extract the smallest street/district clues from the photo; search maps and "
    "street view; pin the house number.",
    "Google Maps / Street View.",
))
F.append(mk(
    "1-cartel", "cartel", "Reverse image + geolocation", "A",
    "ATP provenance, FM IPB",
    "osint-03-cartel-precursor", "Precursor Source", 100,
    "The cartel's precursor-shipping note names a cover-company buyer; verify "
    "the original image that seeded the note.",
    "Reverse-search a shared image to find its original public appearance and "
    "the cover-company that hosted it.",
    "Reverse-image the original file (never the screenshot); find the first "
    "source; note the company/domain that published it.",
    "Google / Yandex reverse image.",
))
F.append(mk(
    "1-cartel", "cartel", "Hex decode + what3words + geolocation", "C",
    "ATP discovery/collection, ATP geo",
    "osint-04-cartel-meet", "The Strange File", 100,
    "A police raid in Muscat, Oman recovered a file the authorities could not "
    "read; the Tiberian Order is asked to decode and geolocate the meeting point.",
    "Seized file encodes two meeting-place images; decode, geolocate, and "
    "reduce the spot to a what3words address.",
    "File-to-Hex then Hex-to-Text to recover two images; geolocate each; pin the "
    "exact meeting spot; convert to a what3words triple plus business type.",
    "Hex converters, what3words, Google Maps.",
))

# ---- ARC 2 : Wire Syndicate (the hackers) ---------------------------------
F.append(mk(
    "2-synd", "synd", "DNS / packet capture", "C",
    "ATP discovery/collection, OPSEC",
    "osint-05-synd-exfil", "Exfil on the Wire", 120,
    "The Wire Syndicate runs a payload exfil channel; a capture shows DNS "
    "lookups pointing to their covert store.",
    "Identify a PCAP's true nature despite a mangled extension, then follow the "
    "hidden DNS/NSLOOKUP chain to the exfil URL.",
    "Open the capture in a packet tool; filter DNS; read the hidden pastebin/raw "
    "URL; follow it to the dead-drop link.",
    "Wireshark / NetworkMiner / tcpdump.",
))
F.append(mk(
    "2-synd", "synd", "PCAP analysis + decoding", "C",
    "ATP discovery/collection, FM intelligence-cycle",
    "osint-06-synd-intercept", "Intercepted Meeting", 120,
    "A wiretap capture logs a Syndicate call arranging a meet; decode the "
    "details of time and place.",
    "From an intercepted packet capture, extract a shared dropbox/meeting link "
    "and decode the meeting time and venue.",
    "Open the pcap; find the shared link; decode the meeting details; format the "
    "time/location.",
    "Wireshark, decoders.",
))
F.append(mk(
    "2-synd", "synd", "Base85 + Vigenere + geolocation", "C",
    "ATP capture/authenticate, ATP discovery",
    "osint-07-synd-beacon", "Emergency Beacon", 120,
    "The Syndicate's emergency beacon broadcasts a layered cipher; break it to "
    "recover the coordinates.",
    "Decode an intercepted transmission (Base85 then Vigenere) that carries "
    "spoken-military coordinates.",
    "Base85-decode; Vigenere-decrypt with the recovered key; transcribe spoken "
    "coordinates; convert to decimal.",
    "Acii85/Base85 decoder, Vigenere decoder.",
))
F.append(mk(
    "2-synd", "synd", "Browser forensics", "C",
    "ATP discovery/collection, FM intelligence-cycle",
    "osint-08-synd-burn", "The Burn Laptop", 130,
    "The Syndicate 'burn' laptop holds browser artifacts that assemble into a "
    "flag and a timeline.",
    "Extract browser history/bookmarks/cache from a ZIP to reconstruct an "
    "incident timeline and assemble a hidden flag.",
    "Unpack browser data; read history/bookmarks; inspect a cached image; combine "
    "the word fragments; build the timeline.",
    "SQLite browser, image editor, text editor.",
))
F.append(mk(
    "2-synd", "synd", "Multi-stage decryption + geolocation", "C",
    "ATP capture/authenticate",
    "osint-09-synd-wallet", "The Wallet Ledger", 130,
    "The Syndicate's laundered-crypto ledger hides a target coordinate in a "
    "multi-stage cipher.",
    "Decode an email (Base64 -> decimal -> Vigenere) to reveal a target "
    "coordinate and place name.",
    "Base64-decode; convert to decimal; Vigenere with the recovered key; read the "
    "coordinates and name the venue.",
    "Base64/ROT47/hex decoders, Vigenere decoder.",
))
F.append(mk(
    "2-synd", "synd", "Hidden URL / OPSEC", "A",
    "ATP capture/authenticate, OPSEC",
    "osint-10-synd-deaddrop", "Dead-Drop Slip", 100,
    "A Syndicate + cult joint slip hides a short URL; a dead-drop code-fragment "
    "chain must be reassembled.",
    "Scan a document for hidden URL fragments and reassemble a working link.",
    "Look for short-link fragments embedded in the text; concatenate into a URL; "
    "open it (case-sensitive).",
    "Text editor / search.",
))

# ---- ARC 3 : Gilded Generals (military tech sales) ------------------------
F.append(mk(
    "3-gen", "gen", "Vehicle / IMINT identification", "B",
    "FM target-acq, IMINT",
    "osint-11-gen-tank", "The Stolen AFV", 140,
    "A corrupt general is selling armored-vehicle tech abroad; identify the "
    "platform from a drone still.",
    "Recognize an armored fighting vehicle from hull/turret/gun layout in a "
    "drone photo and report its type.",
    "Analyze the design characteristics (hull, turret, gun, sensors); match "
    "against military vehicle references.",
    "Armored-vehicle / tank recognition databases.",
))
F.append(mk(
    "3-gen", "gen", "Vessel / class identification", "B",
    "FM target-acq, maritime/AIS",
    "osint-12-gen-frigate", "Sold Frigate Plans", 140,
    "The same general is selling a foreign frigate class; a UAV still IDs the "
    "vessel despite having no markings.",
    "Classify a warship's hull/superstructure/weapons from a UAV image and give "
    "the class + NATO reporting name.",
    "Identify hull/sensor/weapon layout; match against naval vessel catalogs; "
    "report class and NATO form.",
    "PLAN / naval vessel catalogs, NATO reporting-name references.",
))
F.append(mk(
    "3-gen", "gen", "Air-base geolocation", "B",
    "FM IPB/ground-truth, FM target-acq",
    "osint-13-gen-airfield", "The Safe Airfield", 140,
    "Intel points to an air base the generals use to move tech; locate it from "
    "satellite hints.",
    "Identify an air base from satellite imagery and give its hierarchical "
    "location (country -> region -> base).",
    "Read hangars/runways on satellite imagery; cross-reference ground context; "
    "structure the country/region/base.",
    "Google Earth / satellite imagery.",
))
F.append(mk(
    "3-gen", "gen", "Aviation / aircraft lifecycle", "C",
    "FM IPB/ground-truth, temporality",
    "osint-14-gen-aircraft", "The Decommissioned 747", 150,
    "A general uses a decommissioned 747 to move tech; identify the airframe, "
    "its current base, and its history.",
    "Identify a retired aircraft from a photo, locate its current stationary "
    "base, then trace its historical deployment.",
    "Recognize the airframe; look it up in an aviation database; find its current "
    "location; trace a key date in its history.",
    "Planespotters, ICAO airport codes, image search.",
))

# ---- ARC 4 : the Chancellery (corrupt politicians) ------------------------
F.append(mk(
    "4-chan", "chan", "Geo + translation + temporal", "C",
    "FM intelligence-cycle, FM target-acq",
    "osint-15-chan-strike", "The Strike Window", 150,
    "The Chancellery is vectoring a military strike; translate the intercept and "
    "assemble location + timing.",
    "Combine three air bases, a translated briefing, a named commander, and a "
    "day/time into the coordination answer.",
    "Geolocate the bases; translate the foreign briefing; extract the person + "
    "the next-day/time; assemble the answer.",
    "Google Maps, translation tools.",
))
F.append(mk(
    "4-chan", "chan", "AO / NGO facility geolocation", "C",
    "FM spatial/IPB, FM target-acq",
    "osint-16-chan-ao", "The Quiet AO", 150,
    "The Chancellery quietly refuses to act in a humanitarian AO â€” prove it by "
    "geolocating the facility from a child's photo.",
    "Locate an NGO children's facility from a photograph within a known "
    "operational area.",
    "Constrain to the country/AO; scan the corridor on satellite imagery; match "
    "the facility type to NGO records.",
    "Google Maps/Earth, satellite imagery, NGO facility databases.",
))
F.append(mk(
    "4-chan", "chan", "Steganography + geolocation", "C",
    "ATP capture/authenticate, ATP discovery",
    "osint-17-chan-smuggle", "The Sanctioned Road", 150,
    "A 'sanctioned' smuggling route hides coordinates inside an image; extract "
    "them.",
    "Extract hidden coordinates from an image via steganography and geolocate "
    "the route.",
    "Run the image steganography tool with the recovered marker/password; read "
    "the extracted location file; map the coordinates.",
    "steghide, image analysis tools.",
))
F.append(mk(
    "4-chan", "chan", "Maritime / AIS + IMINT", "C",
    "multi-INT fusion, FM collection-mgmt, maritime/AIS",
    "osint-18-chan-fleet", "The Flagged Corridor", 180,
    "The Chancellery brokers a flagged shipping lane; an IMINT report spots a "
    "suspicious vessel â€” trace it.",
    "Fuse an IMINT coordinate/time with historical AIS to identify a vessel, "
    "verify it, and reconstruct its port history (the centerpiece link).",
    "Query the coordinate/time on AIS data; identify the vessel; verify against "
    "the IMO registry + photos; replay the port sequence.",
    "MarineTraffic / VesselFinder, IMO registry, Global Fishing Watch.",
))
F.append(mk(
    "4-chan", "chan", "Maritime + simple crypto", "B",
    "ATP discovery/collection, maritime/AIS",
    "osint-19-chan-manifest", "The Decoy Manifest", 130,
    "A 'decoy' shipping manifest hides the real cargo route using a naive "
    "password on a beacon log.",
    "Derive a password from vessel metadata, unlock a beacon log, and interpret "
    "the telemetry (position/heading/speed).",
    "Infer the archive password from ship name+year; unlock; read the last "
    "coordinates; interpret the event sequence.",
    "Archive extractor, coordinate mapper.",
))
F.append(mk(
    "4-chan", "chan", "Aerial geolocation + historical corroboration", "C",
    "reliability/corroboration, FM IPB",
    "osint-20-chan-cover", "The Approved Trade", 150,
    "The Chancellery's 'approved trade' cover needs historical corroboration; "
    "correlate an aerial photo against historical clues.",
    "Geolocate an aerial photo and confirm it by cross-referencing a historical "
    "geographic riddle.",
    "Identify the aerial subject; correlate with historical event clues; confirm "
    "the fortress/landmark.",
    "Google Maps aerial / building comparison, historical reference.",
))

# ---- ARC 5 : Order of Hades (original villain) -----------------------------
F.append(mk(
    "5-hades", "hades", "Geolocation + web enrichment", "B",
    "FM collection-mgmt, FM IPB",
    "osint-21-hades-operative", "The Gifted Jacket", 140,
    "A Hades defector (Maksim) escaped, but the Order planted a GPS camera on "
    "his jacket that uploads photos; locate where he is staying.",
    "From uploaded GPS-camera photos, identify the hotel and enrich it with "
    "public listing data (phone).",
    "Analyze the photos; identify the hotel; look up the listing phone on maps.",
    "Google Maps / Street View.",
))
F.append(mk(
    "5-hades", "hades", "Decode + geolocation", "C",
    "ATP discovery/collection, FM IPB",
    "osint-22-hades-cutout", "The Hades Cutout", 150,
    "A Hades cutout encoded a hidden location string; decode it and verify "
    "spatially.",
    "Decode a hidden text/encoding inside an aerial image and resolve it to a "
    "place/coordinate.",
    "Inspect the image and hidden text; decode the message; format the location "
    "string; verify on a map.",
    "Text decoder, satellite map.",
))
F.append(mk(
    "5-hades", "hades", "IP + Street View + what3words", "C",
    "FM IPB/ground-truth, multi-INT",
    "osint-23-hades-payment", "Payment on the Corner", 150,
    "A Hades payment/exfiltration site was imaged; pivot from an IP to imagery "
    "to a what3words coordinate.",
    "Geolocate an IP, correct a file's extension to recover an image, match a "
    "street-view corner, and encode the spot as a triple.",
    "IP-geolocate the address; fix the file extension to reveal the image; match "
    "on Street View; read the what3words triple.",
    "IP geolocation, Google Street View, what3words.",
))
F.append(mk(
    "5-hades", "hades", "Multi-cipher + what3words", "C",
    "ATP capture/authenticate",
    "osint-24-hades-hostage", "The Hostage Note", 160,
    "A Hades hostage note is layered encryption; break it to the rescue location.",
    "Decode a multi-layer encoded message (Base64 -> ROT47 -> hex -> "
    "substitution) down to a what3words location.",
    "Apply the decode stack in strict order; apply the character substitution "
    "table; resolve the what3words triple.",
    "Base64/ROT47/hex decoders, substitution table, what3words.",
))
F.append(mk(
    "5-hades", "hades", "Park/route geolocation", "B",
    "FM IPB/ground-truth",
    "osint-25-hades-hit", "Dead Man's Park", 140,
    "A Hades hit was carried out at a park; pin the intersection from a photo.",
    "Geolocate a park/path intersection from a photograph.",
    "Constrain to the city's parks; match trail/intersection features on maps "
    "and street view.",
    "Google Maps / Street View / trail maps.",
))
F.append(mk(
    "5-hades", "hades", "Multi-point geo + what3words + riddle", "C",
    "FM spatial/IPB, FM target-acq",
    "osint-26-hades-slayer", "Four Points to an Address", 180,
    "Four body-drop locations mark the corners of a Hades asset's kill-zone; "
    "find the center and the asset's address.",
    "Plot four points, read the centroid, convert to what3words, decode a riddle "
    "to the asset's address.",
    "Geocode the four points; plot the cross/centroid; get the what3words; solve "
    "the riddle to the address; encode it as a triple.",
    "Google Maps, what3words, satellite.",
))

# ---- ARC 6 : Ashfall (terrorists) ------------------------------------------
F.append(mk(
    "6-ash", "ash", "Web + geolocation + technical", "C",
    "FM IPB/ground-truth, FM target-acq",
    "osint-27-ash-strike", "Grid-Strike Plot", 160,
    "Ashfall is funded to hit a power substation; cross a conflict map with "
    "mapping data to identify the target asset.",
    "Fuse a conflict-map event, mapping data, and infrastructure documentation "
    "to identify a targeted substation.",
    "Search the conflict map event; geolocate the substation; read the "
    "infrastructure docs for its rating; assemble the identifier.",
    "Conflict map, Google Maps, energy-infrastructure sites.",
))
F.append(mk(
    "6-ash", "ash", "Morse + what3words", "B",
    "FM discovery/collection, FM spatial/IPB",
    "osint-28-ash-distress", "Morse on the Dead Network", 140,
    "Ashfall's distress channel uses Morse on a dead-drop; transcribe it to the "
    "location.",
    "Transcribe a Morse distress signal and reduce the message to a what3words "
    "location.",
    "Decode the Morse; confirm the callsign; parse the phrase; convert to a "
    "what3words triple.",
    "Morse decoder, what3words.",
))
F.append(mk(
    "6-ash", "ash", "Social footprint + translation", "C",
    "multi-INT fusion, reliability/corroboration, OPSEC",
    "osint-29-ash-freelancer", "The Financed Freelancer", 160,
    "A lone-actor the Loom backs slipped his identity in a video; trace his "
    "online footprint to an address.",
    "From a video, identify a pub, translate speech, find the reviewer's online "
    "accounts, and geolocate their declared house.",
    "Identify the pub; translate the speech; find reviews by name; follow the "
    "social handle; geolocate the declared address.",
    "Translation tools, review sites (TripAdvisor/Google), Mastodon, Maps.",
))

# ---- ARC 7 : House of Krohndahkyr (the cult / money funnel) ----------------
F.append(mk(
    "7-cult", "cult", "Public-database web research", "B",
    "FM collection-mgmt, reliability/corroboration",
    "osint-30-cult-funnel", "The Believers' Ledger", 140,
    "The doomsday cult runs a 'believers' database' that also launders the money "
    "funnel; retrieve a specific record from sparse IDs.",
    "Navigate a public sighting-report database and return the exact record URL "
    "from a handful of identifiers.",
    "Recognize the report format; filter by the location/date/time; match the "
    "record ID; build the exact URL.",
    "Public reporting database (e.g., NUFORC), browser search.",
))
F.append(mk(
    "7-cult", "cult", "Archival web research", "B",
    "FM collection-mgmt, reliability/corroboration",
    "osint-31-cult-origin", "Origin Myth", 140,
    "The cult's origin story is a 'classic sighting' from decades ago; recover "
    "that exact article.",
    "Use targeted web/search operators to recover a specific old article URL "
    "from minimal narrative clues.",
    "Build a distinctive key-phrase set; search specialized archives/sites; "
    "narrow by multiple constraints to the exact URL.",
    "Search engines, cryptozoology/archive sites.",
))
F.append(mk(
    "7-cult", "cult", "Audio spectrogram + hex + geolocation", "C",
    "ATP discovery/collection, multi-INT",
    "osint-32-cult-signal", "The Signal Site", 150,
    "A cult 'signal' clip hides a spectrogram message and a hex string pointing "
    "to a staging site.",
    "Pull a hidden message from audio, decode hex to a website, and geolocate a "
    "facility from revealed coordinates.",
    "Open the clip in a spectrogram; read the warning + hex; decode hex to a "
    "site; read the coordinates; identify the facility.",
    "Audio/spectrogram analyzer, hex decoder, Google Maps.",
))
F.append(mk(
    "7-cult", "cult", "Cipher / translation", "B",
    "ATP capture/authenticate",
    "osint-33-cult-cipher", "The Cult Cipher", 140,
    "The cult transacts in an invented script; translate it to the credential.",
    "Use a provided alphabet/cipher to translate an in-universe script into a "
    "password/credential.",
    "Study the language-picture key; map the script characters; translate to the "
    "credential.",
    "Cipher/translation key, decoder.",
))
F.append(mk(
    "7-cult", "cult", "Street-view geolocation", "B",
    "FM IPB/ground-truth",
    "osint-34-cult-caravan", "The Traveling Saint", 140,
    "The cult's money caravan 'traveling saint' photographed a street; pin it.",
    "Pin a street from a tourist photo via street-view verification.",
    "Analyze the photo's landmarks/signage; search candidate cities; verify on "
    "Street View; read the street.",
    "Google Street View / Google Maps.",
))
F.append(mk(
    "7-cult", "cult", "Translation / provenance", "B",
    "ATP capture/authenticate, reliability",
    "osint-35-cult-ledger", "The Tithing Ledger", 140,
    "The cult's 'tithing' law-text is a translated classical work; identify its "
    "source.",
    "Translate a text and identify the classical source/author it draws from.",
    "Translate the text; recognize the classical source (author/work); build the "
    "credential from it.",
    "Translation tools, classical-literature reference.",
))
F.append(mk(
    "7-cult", "cult", "Font decoding + geolocation + temporal", "C",
    "FM IPB/ground-truth, temporality",
    "osint-36-cult-prophecy", "The Prophecy Site", 150,
    "The cult's founding 'prophecy site' ties a palace photo, a decoded alien "
    "script, and a year together.",
    "Connect a location, a decoded message, and a date across a riddle chain.",
    "Identify the palace from the photo; decode the script/message with the font "
    "key; parse the date and place clues; assemble.",
    "Historical image DB, font decoder, Google Maps.",
))
F.append(mk(
    "7-cult", "cult", "EXIF / metadata", "A",
    "ATP discovery/collection, OPSEC",
    "osint-37-cult-relic", "Relic Video", 100,
    "A cult 'relic' video hides a wallet key in its metadata.",
    "Mine media file metadata to obtain a hidden credential.",
    "Download the media; inspect metadata (EXIF/container); extract the hidden "
    "key.",
    "EXIFTool / media metadata viewer.",
))
F.append(mk(
    "7-cult", "cult", "Web -> what3words -> archive", "C",
    "multi-INT fusion, OPSEC",
    "osint-38-cult-money", "The Money Pass", 150,
    "The cult-to-cartel money pass runs through jigsaw dead-drops and a vault; "
    "follow the staged chain.",
    "Solve an online jigsaw, follow a shared-folder lead, read what3words "
    "locations, and unlock the vault credential.",
    "Solve the web jigsaw; open the shared folder; read the three what3words; "
    "form the vault password; recover the final key.",
    "puzzel.org, Dropbox, what3words, archive/vault.",
))
F.append(mk(
    "7-cult", "cult", "Landmark + what3words", "B",
    "FM IPB/ground-truth",
    "osint-39-cult-cache", "Relic Cache", 130,
    "A cult relic cache hides in a town landmark on the shared lane; encode its "
    "location.",
    "Identify a town landmark from clues and express its location as a "
    "what3words address plus local context.",
    "Recognize the landmark (e.g., an old cannon); note the local area code; "
    "convert to a what3words triple; assemble the unlock format.",
    "what3words, zip/archive extractor, map.",
))

# ---- ARC 8 : Corroboration & the Loom (capstone) ---------------------------
F.append(mk(
    "8-loom", "loom", "Cross-verification / reliability", "C",
    "reliability/corroboration, OPSEC",
    "osint-40-loom-corroborate", "Source Discipline", 190,
    "Before naming the network, prove you can vet sources: corroborate a lead "
    "with two independent legal sources.",
    "Take a supplied lead, corroborate with two independent PAI sources, score "
    "each on a credibility scale, flag any contradiction.",
    "Find two independent corroborating sources; rate each source/info on a "
    "reliability scale; note a contradiction; state the assessment.",
    "Public-registry search, news archives, reliability scale.",
))
F.append(mk(
    "8-loom", "loom", "Fused assessment (capstone)", "C",
    "multi-INT fusion, reliability/product",
    "osint-41-loom-assess", "Who Weaves the Loom?", 250,
    "You have resolved dozens of leads. Every faction's operation flowed through "
    "the same cover company, port lane, wallet, and dead drop. Assess the "
    "coordinator.",
    "Assemble the recurring shared logistics (cover company, port lane, wallet, "
    "dead drop) into a sourced one-paragraph intelligence assessment naming the "
    "hidden coordinating buyer.",
    "Correlate the linked entities across the case file; identify the shared "
    "logistics; score sources; issue a cited product (place, date, time, "
    "origin).",
    "Everything learned in the campaign, plus a reliability scale.",
))

# ---------------------------------------------------------------------------
# name/points/desc idempotence â€” build CHALLENGES + metadata from F
# ---------------------------------------------------------------------------
CHALLENGES = []
META = {}
for _l in F:
    CHALLENGES.append({"id": _l["id"], "name": _l["name"], "points": _l["points"], "desc": _l["desc"]})
    META[_l["id"]] = (
        _l["skill"],
        _l["tier"],
        _l["doctrine"],
        _l["arc"],
        _l["faction"],
    )

# --- flags (single source of truth; placeholders to verify at release) ------
FLAGS = {
    "osint-00-start-here": "WELCOME TO OSINT",
    "osint-01-cartel-airdrop": "cartel-drop-lane",
    "osint-02-cartel-safehouse": "cartel-safehouse-street",
    "osint-03-cartel-precursor": "cover-company-source",
    "osint-04-cartel-meet": "definitive.doorpost.thickness",
    "osint-05-synd-exfil": "exfil-pastebin-url",
    "osint-06-synd-intercept": "meet-time-place",
    "osint-07-synd-beacon": "-1.251946,-78.370167",
    "osint-08-synd-burn": "flag-copycatkitty",
    "osint-09-synd-wallet": "sofi-stadium-33.953417",
    "osint-10-synd-deaddrop": "dead-drop-link",
    "osint-11-gen-tank": "merkava-mk-4m",
    "osint-12-gen-frigate": "type-054a-jiangkai-II",
    "osint-13-gen-airfield": "syria-latakia-jableh",
    "osint-14-gen-aircraft": "canada-essa-sweden",
    "osint-15-chan-strike": "jaisalmer-amritsar-naliya",
    "osint-16-chan-ao": "sos-childrens-village",
    "osint-17-chan-smuggle": "20.899370,95.118041",
    "osint-18-chan-fleet": "guria-imo-9758351",
    "osint-19-chan-manifest": "narwhal-log-recovered",
    "osint-20-chan-cover": "castello-di-brescia",
    "osint-21-hades-operative": "latanya-hotel-ankara",
    "osint-22-hades-cutout": "serbia-rakinac-44.259654",
    "osint-23-hades-payment": "continuation.partakes.devolved",
    "osint-24-hades-hostage": "inched.barman.fast",
    "osint-25-hades-hit": "cedar-rose-park",
    "osint-26-hades-slayer": "forum.report.rent",
    "osint-27-ash-strike": "kindijska-35-6kv",
    "osint-28-ash-distress": "omega.expendable.ridge",
    "osint-29-ash-freelancer": "evgenil-kuznetsova-11-kestrel",
    "osint-30-cult-funnel": "nuforc-sighting-id",
    "osint-31-cult-origin": "bigfoot-article-url",
    "osint-32-cult-signal": "37.455327,-79.981241",
    "osint-33-cult-cipher": "klumgongyn-credential",
    "osint-34-cult-caravan": "maldives-elhe-didi-magu",
    "osint-35-cult-ledger": "gaius-suetonius-de-vita-caesarum",
    "osint-36-cult-prophecy": "amber-sam-sing-1930",
    "osint-37-cult-relic": "relic-video-key",
    "osint-38-cult-money": "case.thrillers.jams",
    "osint-39-cult-cache": "0525-elburg-punk-runways-messed",
    "osint-40-loom-corroborate": "corrob-two-sources",
    "osint-41-loom-assess": "the-loom-assess-product",
}

# --- hints (subset; OSINT is not wallet-managed, but author for future) ------
HINTS = {
    "osint-01-cartel-airdrop": [
        "Read the coastline and street grid, not the color.",
        "Match the region against public satellite atlas.",
        "Pin the exact coastal point and cite the coordinate.",
    ],
    "osint-04-cartel-meet": [
        "That file isn't text â€” try converting to hex then back.",
        "Two images hide inside; geolocate each.",
        "Reduce the exact spot to a what3words triple.",
    ],
    "osint-05-synd-exfil": [
        "Look at DNS lookups in the capture.",
        "A pastebin/raw URL is hiding in the queries.",
        "Follow it to the dead-drop link.",
    ],
    "osint-07-synd-beacon": [
        "The transmission is layered encoding.",
        "Start with a touch by the payload header (Base85).",
        "Then Vigenere with the key, transcribe spoken coords.",
    ],
    "osint-14-gen-aircraft": [
        "Recognize the airframe type first.",
        "Planespotters tells you its current and past bases.",
        "Match the key date to a country.",
    ],
    "osint-18-chan-fleet": [
        "Query the coordinate/time on AIS data.",
        "Match the track speed to one vessel.",
        "Verify with the IMO registry, then replay ports.",
    ],
    "osint-24-hades-hostage": [
        "Strict order matters: Base64 -> ROT47 -> hex.",
        "Then apply the substitution table.",
        "Resolve the final what3words triple.",
    ],
    "osint-40-loom-corroborate": [
        "One hit isn't proof â€” find a second source.",
        "Score each source on a reliability scale.",
        "Flag the contradiction before you commit.",
    ],
    "osint-41-loom-assess": [
        "The factions recycle the same logistics.",
        "Name the cover company, port lane, wallet, dead drop.",
        "Emit one cited product with place/date/time/origin.",
    ],
}


def managed_tiers(value, texts):
    """Mirror the staged tracks' tier generation (prices via hint_economy)."""
    sys.path.insert(0, str(SCRIPT_DIR))
    from hint_economy import tier_costs  # noqa: PLC0415 (late import)

    costs = tier_costs(value)
    tiers = []
    for n, (text, cost) in enumerate(zip(texts, costs), 1):
        tiers.append({"tier": n, "cost": cost, "content": text})
    return tiers


def main_build():
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    wallet = []
    for ch in CHALLENGES:
        cid = ch["id"]
        folder = BASE_DIR / cid
        folder.mkdir(parents=True, exist_ok=True)

        full_desc = ch["desc"].replace(chr(10), chr(10) + "  ")
        yaml = f"""name: "{ch['name']}"
author: "CEI Labs (OSINT wargame track)"
category: "OSINT"
description: |
  {full_desc}
value: {ch["points"]}
type: standard
flags:
  - "{FLAGS[cid]}"
state: {RELEASE_STATE}
version: "1.0"
"""
        if cid in HINTS:
            wallet.append({
                "name": ch["name"],
                "tiers": managed_tiers(ch["points"], HINTS[cid]),
            })
        (folder / "challenge.yml").write_text(yaml, encoding="utf-8")

    manifest = {
        "schema_version": 1,
        "track": "osint",
        "release_state": RELEASE_STATE,
        "challenges": [{"id": c["id"], "points": c["points"]} for c in CHALLENGES],
        "meta": {
            c["id"]: {
                "skill": META[c["id"]][0],
                "tier": META[c["id"]][1],
                "doctrine": META[c["id"]][2],
                "arc": META[c["id"]][3],
                "faction": META[c["id"]][4],
            }
            for c in CHALLENGES
        },
    }
    (BASE_DIR / "osint-training.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if wallet:
        (BASE_DIR / "osint-hint-wallet.json").write_text(json.dumps({"schema_version": 1, "track": "osint", "entries": wallet}, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"Generated {len(CHALLENGES)} OSINT challenges into '{BASE_DIR}' (state={RELEASE_STATE}).")
    print("Release with:   OSINT_RELEASE_STATE=visible python3 scripts/build_osint.py")


if __name__ == "__main__":
    main_build()

