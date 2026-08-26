# Skill-Building Priority — selecting the no-theme challenges

When we *build* story onto a HACKTORIA challenge that has no existing plotline,
"square space" (solve time, difficulty, uniqueness) is limited. This document is
the **decision rule**: it scores every "build" (no-theme) challenge on how much
real, transferable OSINT skill it teaches, so the selection favours
highest learning-per-minute. It complements `storyline.md` and the research
index.

> Rule: **"keep"** challenges already carry a theme (Tiberian Order, Order of
> Hades, cartels, cult) and stay as-is. Every **"build"** challenge below needed
> a new faction + plot beat — and earns a slot **only by clearing this rubric**.

---

## 1. The rubric (5 weighted criteria, max 100)

| Criterion | Weight | What it rewards |
|---|---|---|
| **Skill transferability** | 25 | Does it teach a widely-useful OSINT technique (not a one-off trick)? Favours geolocation, AIS, reverse-image, EXIF, aviation, chronolocation — skills that recur across real investigations. |
| **Doctrine / learning objective** | 20 | Does it map to a concrete ATP 2-22.9 / FM 2-0 learning objective (geo, collection, corroboration, analysis)? The stronger the anchor, the higher. |
| **Multi-step depth** | 20 | Does it chain 2+ skills (decode→geo, AIS→verify→history, photo→reverse→corroborate)? More layers = more retained learning. |
| **Tool authenticity** | 20 | Does it use real, free, industry-standard PAI tools (Google Earth, MarineTraffic, IMO, Sentinel/FIRMS, Planespotters, EXIFTool, CyberChef, what3words)? Favours tools that transfer to a real OSINT job. |
| **Ground-truth verifiability** | 15 | Is the answer a real, verifiable place/value the player can confirm independently (not a fiction-only token)? |

Score = 0.25·transfer + 0.20·doctrine + 0.20·depth + 0.20·tools + 0.15·truth.
Doctrine uses the anchors in `osint-research-index.md` §4.1.

---

## 2. Ranked score for every "build" (no-theme) challenge

Scores are the design team's estimate from the write-ups in `hacktoria-archive/`.
Threshold: **include ≥ 70**, review 55–69, drop < 55 (unless it fills a rare
skill niche the bank otherwise lacks).

| Rank | Challenge | Team | Skill chain | Transfer (25) | Doctrine (20) | Depth (20) | Tools (20) | Truth (15) | **Score** | Keep? |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | undercover-fleet | Chancellery | IMINT coords → AIS → IMO verify → port history | 25 | 20 | 20 | 20 | 15 | **100** | keep (centerpiece) |
| 2 | friendly-fire | Gilded Generals | drone photo → AFV hull/turret ID | 25 | 20 | 15 | 20 | 15 | **96** | keep |
| 3 | naval-intrusion | Gilded Generals | UAV hull/sensor → warship class → NATO name | 25 | 20 | 18 | 20 | 15 | **98** | keep |
| 4 | emergency-transmission | Wire Syndicate | Base85 → Vigenère → spoken coords | 22 | 15 | 20 | 20 | 15 | **92** | keep |
| 5 | the-sleeper-cell | Wire Syndicate | Base64 → decimal → Vigenère → geo | 22 | 15 | 20 | 20 | 15 | **92** | keep |
| 6 | road-to-nowhere | Chancellery | steghide → extract coords → geo | 22 | 18 | 20 | 20 | 15 | **95** | keep |
| 7 | substation-bombing | Ashfall | conflict-map → satellite → infra docs | 22 | 18 | 18 | 18 | 15 | **91** | keep |
| 8 | on-the-wire | Wire Syndicate | pcap → DNS → pastebin → dead-drop | 18 | 15 | 20 | 20 | 15 | **87** | keep (OPSEC) |
| 9 | operation-wiretap | Wire Syndicate | pcap/Dropbox → decode → time/place | 18 | 15 | 18 | 20 | 15 | **85** | keep |
| 10 | last-flight | Gilded Generals | aircraft ID → airframe history → country | 20 | 15 | 18 | 20 | 15 | **89** | keep |
| 11 | cold-war-enemies | Gilded Generals | satellite → air base → hierarchy | 18 | 18 | 12 | 15 | 15 | **80** | keep |
| 12 | the-copycat-killer | Wire Syndicate | SQLite browser → cached image → flag | 18 | 15 | 18 | 18 | 15 | **84** | keep |
| 13 | appalachian-aliens | House of Krohndahkyr | spectrogram → hex → site → geo | 18 | 15 | 18 | 18 | 15 | **84** | keep |
| 14 | saving-isabella | Ashfall | Morse → phrase → what3words | 20 | 15 | 15 | 18 | 15 | **84** | keep |
| 15 | prisoner-of-war | Chancellery | AO scope → satellite → NGO DB → facility | 20 | 18 | 15 | 15 | 15 | **83** | keep |
| 16 | lost-down-under | Wire Syndicate | decode → geo 8 → spatial pattern → math | 20 | 15 | 20 | 15 | 15 | **85** | keep |
| 17 | the-midnight-slayer | Order of Hades | multi-point plot → centroid → w3w → riddle | 22 | 18 | 20 | 18 | 12 | **90** | keep |
| 18 | gas-attack | Crimson Cartel | reverse-image → city from satellite | 20 | 15 | 12 | 18 | 15 | **80** | keep |
| 19 | dialogues-from-atlantis | Wire Syndicate | hidden-URL fragment reassembly | 12 | 12 | 10 | 10 | 12 | **55** | review (niche) |
| 20 | the-listeners | Cult | street geolocation (Monaco addr) | 18 | 15 | 10 | 15 | 15 | **74** | keep |
| 21 | the-latvian-connection | Cult | reverse-image + listing corroborate | 20 | 18 | 12 | 18 | 15 | **83** | keep |
| 22 | intergalactic-warfare | Cult | coords → nested admin | 12 | 12 | 8 | 12 | 12 | **56** | low, skip |
| 23 | nightmare-fuel | Cult | EXIF → hidden password | 22 | 15 | 8 | 18 | 15 | **80** | keep (EXIF A) |
| 24 | far-away-outpost | Cult | satellite map → county/road IDs | 14 | 12 | 8 | 12 | 12 | **58** | low, skip |
| 25 | the-butcher | Cult | hex → audio → spoken password | 16 | 12 | 15 | 18 | 15 | **76** | keep (audio) |
| 26 | catch-me-if-you-can | Order of Hades | (no write-up; fugitive tracking) | 12 | 12 | 12 | 10 | 8 | **54** | skip (unverifiable) |
| 27 | kanonniers | Cult | landmark → w3w + area code | 18 | 15 | 10 | 18 | 12 | **72** | keep |
| 28 | the-road-to-rome | Chancellery | aerial geo + historical corroborate | 18 | 15 | 15 | 15 | 15 | **78** | keep |

*(Rows 1–28 cover the no-theme pool; the few remaining without a clear write-up
or scoring are omitted to keep the table actionable.)*

---

## 3. What "highest learning" means for the campaign

Applying the rubric changed the build selection this way:

- **Prioritise** the 4 geospatial "anchor" skills that recur across every real
  OSINT investigation: **IMINT/geolocation**, **maritime/AIS**, **reverse-image
  + corroboration**, and **EXIF/metadata**. These carry the highest transfer +
  doctrine scores and appear in almost every write-up.
- **Prefer multi-step chains** (decode→geo, AIS→verify→history) over flat
  single-tool wins — more steps = more retained skill, and they still fit the
  5–15 min cap because each step is quick.
- **Drop or de-prioritise** low-transfer one-offs that are near-unverifiable
  (catch-me-if-you-can: no write-up; intergalactic-warfare / far-away-outpost:
  thin, geo-only). Keep them only if we need filler for a rare niche.
- **Audio (the-butcher, appalachian-aliens, saving-isabella) and browsers
  (the-copycat-killer)** are the deliberate skill-*diversity* pick-ups — they
  stretch the trainees beyond imagery even though their transfer score is mid.

Result: the **42-lead campaign** (see `scripts/build_osint.py`) is built to
maximise these priorities — every faction arc opens with an anchor skill, and
the capstone (`osint-41-loom-assess`) forces cross-referencing all of them.