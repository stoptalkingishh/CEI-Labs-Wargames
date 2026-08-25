#!/usr/bin/env python3
"""Generate the OSINT wargame track (12 drills + a Start Here).

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

IMPORTANT / LEGAL: the landing/answer strings below marked PLACEHOLDER are
illustrative, self-consistent values for building the challenge definitions.
Before any production release, re-verify every answer against real, legal,
publicly-available sources and swap them here (single source of truth) -- never
by hand-editing generated files. The Doctrine anchor per challenge is recorded in
the `doctrine` field and in docs/osint/learning-objectives.md.

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

# id -> (skill, tier, doctrine-anchor) used for the diagnostics manifest only.
META = {
    "osint-start-here": ("onboarding", "A", "PAI / legal boundary"),
    "osint-01-geolocation": ("geolocation", "A", "GEOINT/IMINT, IPB ground-truth"),
    "osint-02-reverse-image": ("reverse-image", "A", "provenance / authentication"),
    "osint-03-chronolocation": ("chronolocation", "B", "temporality, ADP timeline"),
    "osint-04-satellite-fire": ("satellite/thermal", "B", "remote-sensing, IMINT"),
    "osint-05-exif": ("metadata forensics", "A", "processing / source integrity"),
    "osint-06-calendar": ("non-Gregorian date", "B", "temporality, IPB"),
    "osint-07-aviation-icao": ("aviation/ICAO", "B", "open baseline, target acq"),
    "osint-08-maritime-ais": ("maritime/AIS", "C", "vessel/registry, multi-MINT"),
    "osint-09-what3words": ("what3words geocoding", "A", "precise geospatial"),
    "osint-10-web-archive": ("web archive", "B", "eat it fresh / Wayback"),
    "osint-11-social-footprint": ("social footprint", "C", "social-media exploit, PII"),
    "osint-12-corroborate": ("corroboration (capstone)", "C", "reliability / product"),
}

# id -> 3 hint-tiers (crawl / walk / run). Prices are derived by
# scripts/hint_economy.py (tier_costs) the same way bandit/krypton/natas do;
# OSINT is not wallet-managed (the wallet regex only matches
# ^(bandit|krypton|natas)-NN), but the texts are authored here so a future
# wallet adoption has content to price.
HINTS = {
    "osint-01-geolocation": [
        "Understand consider the architecture, signage and climate; narrow to a country first.",
        "Blocks match on Street View: same lamp posts, materials and street width pin the exact road.",
        "A single block is enough. Ground-truth it then cite the coordinate.",
    ],
    "osint-03-chronolocation": [
        "Think about the direction and length of shadows in the photo.",
        "Get the location and date, then use a sun-position calculator to bound local time.",
        "Cross the sun azimuth with the street orientation to pick morning vs afternoon.",
    ],
    "osint-04-satellite-fire": [
        "Those red dots are a 30 m thermal/fire anomaly layer.",
        "That layer is served by FIRMS / NASA GIBS.",
        "Open FIRMS, find the coast, read the date and place.",
    ],
    "osint-05-exif": [
        "Check whether the file still carries EXIF metadata.",
        "EXIFTool will list the device model and the capture date if they weren't stripped.",
        "Read device + date + GPS, and state whether the metadata looks authentic.",
    ],
    "osint-06-calendar": [
        "That year may follow a different official calendar, not the Gregorian one.",
        "Convert with a calendar converter once you identify the calendar system.",
        "Cross the converted Gregorian date against the news event to confirm.",
    ],
    "osint-07-aviation-icao": [
        "Look at the airside layout not the crowd; runways and tails are the clue.",
        "Match the runway/geography to a known airport using an ICAO reference.",
        "Read the aircraft registration, look it up, and confirm the ICAO of the base airport.",
    ],
    "osint-08-maritime-ais": [
        "That track and its speed are open AIS: query the coordinates/time.",
        "A tool like MarineTraffic or VesselFinder plus the IMO registry IDs the ship.",
        "Verify the hull visuals against photos, then replay the port history.",
    ],
    "osint-09-what3words": [
        "Once you pin the exact spot you can encode it to a 3-word address.",
        "What3Words maps any coordinate to three unique words.",
        "See the input place the marker precisely, then read the triple.",
    ],
    "osint-10-web-archive": [
        "The current page proves nothing about an older state of that page.",
        "A web archive keeps frozen snapshots of past versions.",
        "Open the Wayback URL, pick the snapshot nearest the incident, and read the saved content.",
    ],
    "osint-11-social-footprint": [
        "This is the legal boundary: only publicly-visible posts and accounts, nothing paywalled or harvested.",
        "Search each handle across platforms to build the profile network.",
        "Always respect PII limits; never tamaliagate the subject.",
    ],
    "osint-12-corroborate": [
        "One hit is not proof. Look for two independent sources that agree.",
        "Score each source on a standard reliability/credibility scale.",
        "Write a short sourced product string that cites origin, date and time.",
    ],
}

# id -> (name, points, desc) . Flags live entirely in FLAGS below so a release
# re-verification only touches one place.
CHALLENGES = [
    {
        "id": "osint-start-here",
        "name": "OSINT: Start Here",
        "points": 10,
        "desc": (
            "Welcome the Open-Source Intelligence track.\n"
            "OSINT means intelligence produced legally from publicly available "
            "information (PAI). Its only boundaries are the law and ethics: no "
            "phishing, no credential hacking, no harvesting protected PII, and "
            "never messaging/social-engineering a real target.\n"
            "This track has no server box. Your target is the public web and "
            "your own local tools.\n"
            "Tools + method (free): open a browser with Google Maps / Earth, a "
            "reverse-image engine, EXIFTool, what3words, FIRMS, MarineTraffic, "
            "ICAA/FlightRadar, the Wayback Machine, and CyberChef.\n"
            "Prove you read this by entering the phrase below."
        ),
    },
    {
        "id": "osint-01-geolocation",
        "name": "OSINT 1: Place, People, Circumstances",
        "points": 150,
        "desc": (
            "A single ground-level photograph of an unfamiliar street and you "
            "must name and locate the place (a village/town square).\n"
            "Read architecture, street layout, signage, climate and road surface; "
            "narrow to a country/city, then match block-by-block on Street View. "
            "Record the place and the coordinate.\n"
            "PLACEHOLDER ANSWER — swap to a verified real target at release."
        ),
    },
    {
        "id": "osint-02-reverse-image",
        "name": "OSINT 2: Provenance, Not the Screenshot",
        "points": 200,
        "desc": (
            "Reverse-search the source appearance of a media file. Work from the "
            "original file, never a re-saved screenshot or a platform-re-encoded "
            "thumbnail; find the earliest on-the-source appearance and name the "
            "original source/creator, plus the intended show/context.\n"
            "PLACEHOLDER ANSWER."
        ),
    },
    {
        "id": "osint-03-chronolocation",
        "name": "OSINT 3: What Time Was It?",
        "points": 250,
        "desc": (
            "A video shows an outdoor plaza and the sun sits low. Determine the "
            "approximate local time of recording (morning, midday or afternoon) "
            "and justify it.\n"
            "Use the shadows' direction and length, the street's orientation, and "
            "a sun-position calculator (e.g., SunCalc) for the known place and "
            "date.\n"
            "PLACEHOLDER ANSWER."
        ),
    },
    {
        "id": "osint-04-satellite-fire",
        "name": "OSINT 4: Satellite Fire Finder",
        "points": 300,
        "desc": (
            "An annotated satellite screenshot shows hundreds of red pixels "
            "along a coast. Identify (a) which public tool produced it and (b) "
            "the exact date of the fire/anomaly cluster.\n"
            "The 30 m thermal/anomaly layer is the signature of FIRMS / NASA "
            "GIBS; open it, scan the coastal region, and read the retained "
            "per-date record.\n"
            "PLACEHOLDER ANSWER."
        ),
    },
    {
        "id": "osint-05-exif",
        "name": "OSINT 5: Metadata Is Evidence",
        "points": 350,
        "desc": (
            "A media file's EXIF is your first source. Say which device captured "
            "it, the GPS date, and whether the metadata looks 'eat it fresh' "
            "(unedited) or suspiciously stripped.\n"
            "Run an EXIF reader (e.g., EXIFTool) and read the output.\n"
            "PLACEHOLDER ANSWER."
        ),
    },
    {
        "id": "osint-06-calendar",
        "name": "OSINT 6: Which Year Is It?",
        "points": 400,
        "desc": (
            "Three foreign-news clips carry dates in non-Gregorian calendars. "
            "Convert each official publication date into the modern Gregorian date.\n"
            "Identify the calendar (Solar Hijri, Bikram, Ethiopian), extract the "
            "native date, convert, and sanity-check against the event.\n"
            "PLACEHOLDER ANSWER."
        ),
    },
    {
        "id": "osint-07-aviation-icao",
        "name": "OSINT 7: Airport Without a Name Tag",
        "points": 450,
        "desc": (
            "An airside photo shows a runway and parked aircraft. Identify the "
            "airport and report its ICAO code.\n"
            "Read runway geometry and aircraft registrations, and the ICAO "
            "registry/history databases.\n"
            "PLACEHOLDER ANSWER."
        ),
    },
    {
        "id": "osint-08-maritime-ais",
        "name": "OSINT 8: Kelly's Long Underway",
        "points": 500,
        "desc": (
            "Given a coordinate + timestamp, recover the ship sailing there, its "
            "IMO, and its last-call port history.\n"
            "Pull AIS/VMS track data (MarineTraffic / VesselFinder), verify the "
            "visual vs the IMO registry, and replay the port sequence.\n"
            "PLACEHOLDER ANSWER."
        ),
    },
    {
        "id": "osint-09-what3words",
        "name": "OSINT 9: Three Words for a Pin",
        "points": 550,
        "desc": (
            "Pin an exact spot from a description, then reduce it to a three-word "
            "address.\n"
            "Getting the marker precise enough is the whole point; geocode it "
            "then read the three-word address.\n"
            "PLACEHOLDER ANSWER."
        ),
    },
    {
        "id": "osint-10-web-archive",
        "name": "OSINT 10: The Page That Was",
        "points": 600,
        "desc": (
            "A webpage has been rewritten, but an older version was public once. "
            "Recover what the page said at an earlier date.\n"
            "Query the Wayback Machine (and a news date claw) for snapshots near "
            "the incident date and read the saved content.\n"
            "PLACEHOLDER ANSWER."
        ),
    },
    {
        "id": "osint-11-social-footprint",
        "name": "OSINT 11: The Public Footprint",
        "points": 650,
        "desc": (
            "Profile a target across public platforms -- only *public* accounts "
            "and posts; build handles, and link them into one web.\n"
            "Respect the legal/PAI boundary: no paywalled/agg-game data, never "
            "message the subject.\n"
            "PLACEHOLDER ANSWER."
        ),
    },
    {
        "id": "osint-12-corroborate",
        "name": "OSINT 12: Final Corroborated Assessment (Capstone)",
        "points": 700,
        "desc": (
            "The capstone: take a lead, corroborate it with **two independent, "
            "legal PAI sources**, score each on a credibility scale, flag any "
            "contradiction, and issue a one-paragraph, sourced assessment "
            "(cite place, date, time, origin).\n"
            "PLACEHOLDER ANSWER."
        ),
    },
]

# id -> flag. The single source of truth used by both the generator and the
# writeups.md. Placeholders below are illustrative; verify before release.
FLAGS = {
    "osint-start-here": "WELCOME TO OSINT",
    "osint-01-geolocation": "kiffa-mauritania",
    "osint-02-reverse-image": "starry-night-van-gogh",
    "osint-03-chronolocation": "afternoon-4pm",
    "osint-04-satellite-fire": "firms-california-2023",
    "osint-05-exif": "canon-eos-r5-2026-09-14",
    "osint-06-calendar": "2024-01-12",
    "osint-07-aviation-icao": "egll",
    "osint-08-maritime-ais": "imo-9758351",
    "osint-09-what3words": "index.focus.fresh",
    "osint-10-web-archive": "snap-2009-03-11",
    "osint-11-social-footprint": "verified-profile-2022",
    "osint-12-corroborate": "corrob-two-sources",
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
        "meta": {c["id"]: {"skill": META[c["id"]][0], "tier": META[c["id"]][1], "doctrine": META[c["id"]][2]} for c in CHALLENGES},
    }
    if RELEASE_STATE == "hidden" and os.environ.get("OSINT_SKIP_MANIFEST") is None:
        pass
    (BASE_DIR / "osint-training.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if wallet:
        (BASE_DIR / "osint-hint-wallet.json").write_text(json.dumps({"schema_version": 1, "track": "osint", "entries": wallet}, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"Generated {len(CHALLENGES)} OSINT challenges into '{BASE_DIR}' (state={RELEASE_STATE}).")
    print("Release with:   OSINT_RELEASE_STATE=visible python3 scripts/build_osint.py")


if __name__ == "__main__":
    main_build()