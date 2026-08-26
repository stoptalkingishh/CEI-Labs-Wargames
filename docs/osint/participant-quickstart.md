# OSINT — Participant Quick-Start (one page)

Everything you need for the OSINT track, in one page. No prior OSINT
experience is assumed. Print or keep this tab open alongside CTFd.

## 1. What OSINT is — and is not

OSINT = intelligence from **publicly available information (PAI)**, used legally.
You will only use what **anyone** can lawfully see on the open web: maps,
satellite imagery, public databases, archived pages, and free tools. You will
**never**:

- Phish, crack, or guess credentials.
- Pay for or harvest protected personal data (PII).
- Message, follow, or social-engineer a real person or account.

If a lead asks for a person, use only what that person has clearly made
public. Treat the legal line as part of the puzzle — it is what keeps OSINT
OSINT and not something else.

## 2. Start at the briefing

Open **OSINT: Wargame Briefing (Start Here)** first (10 points), even if you
have done OSINT before. It states the rules, the tool set, and the storyline's
case file. Every later lead assumes you have read it.

## 3. There is no Launch panel

Unlike Bandit/Krypton/Natas, this track has **no per-team Docker box to launch**.
Every puzzle runs against the **public web and your own workstation** — the same
tools a real analyst uses. If a challenge page shows no connection info, that is
intentional.

## 4. The story is framing, not steps

You are an analyst for the **Tiberian Order**, working a 6–7 hour discovery
board. Each challenge is one short lead (5–15 min). The fiction — which faction
(crimson cartel, wire syndicate, gilded generals, chancellery, order of hades,
ashfall, or the house of krohndahkyr) — tells you *whose* lead it is. It never
adds hidden solve steps. If fiction mentions a place or person, the *real* clue
is always stated plainly in the premise that follows.

The connective tissue is the **link graph** you build yourself: after each arc,
write which recurring cover company, port lane, wallet, or dead drop the
factions shared. That graph is what the capstone (`41-loom-assess`) asks you to
use.

## 5. Tools you actually need (free, no account required for most)

Have these ready before the timer starts — the exam room's network is allowlisted
for them (see your facilitator's `network-access.md`):

- **Maps / geolocation:** Google Maps / Earth / Street View
- **Reverse-image / provenance:** Google Images, Yandex, TinEye, Bing Visual
- **Coordinates:** what3words
- **Satellite / thermal:** FIRMS (NASA), GIBS / Sentinel Hub
- **Maritime:** MarineTraffic / VesselFinder, IMO registry
- **Aviation:** FlightRadar24 / ADS-B Exchange, Planespotters, ICAO codes
- **Metadata:** EXIFTool (or an online EXIF viewer)
- **Decoding:** CyberChef (Base64, hex, ROT47, Vigenere, etc.)
- **Capture / browser:** Wireshark/NetworkMiner, a SQLite browser, a packet/Morse decoder, an audio spectrogram tool (Audacity)
- **Web history:** Wayback Machine, public image / wiki databases

Most challenges name their toolset in an always-visible free hint. You never need
a subscription.

## 6. How to read and solve a lead

1. Read the **Premise** (what was seized / leaked / flagged).
2. Skim the **Method** (which tool class solves it) and the free tool list.
3. Produce the **exact answer string** the prompt asks for — a place name,
   coordinate, w3w triple, URL, device, ICAO code, or a short assessment. Use the
   format stated (all-lowercase, hyphens, no trailing slash, include `https://`
   only when asked).
4. Submit it as the flag in CTFd. Case and punctuation matter; copy the format
   exactly.

## 7. Hints and scoring

Every lead keeps the repo's **3-tier hint ladder**, even though OSINT is not
point-gated the same way Bandit is:

- **Tier 1 (crawl):** a bare tool/manpage name or a single reference link.
- **Tier 2 (walk):** what the concept means, still leaving the command to you.
- **Tier 3 (run):** full method — you still run it yourself and read output.

Hints cost points (the percentages shown on each challenge are the only pricing
rule). They never block solving normally — just a points trade-off. Verbal nudges
from an instructor are free; use `cheatsheet.md` nudges before burning points.

## 8. Submitting the flag and pacing

- Flags go in the **challenge's submission box** on CTFd exactly as shown.
  They are static strings — the proof of work was finding them.
- Average pace is **~10 min per lead**; 42 leads = ~6–7 hours. Do not stall on
  one lead — skip ahead and return later. The easiest lead in each faction arc
  is always its first puzzle.
- After each arc, pause 60 seconds and update your case-file link graph. That
  graph is the answer to the final lead.

## Where to get help

- Stuck on the *puzzle*? Try the next hint tier first.
- Stuck on *tooling* (a site won't load, a tool won't run)? Ask a facilitator.
- Something looks *actually broken* (totally blank page, mangled download)?
  Ask — do not assume it's part of the puzzle. Most "isn't working" in OSINT
  *is* the puzzle (e.g., a stripped EXIF is supposed to be stripped).
