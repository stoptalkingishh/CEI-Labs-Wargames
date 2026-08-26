# OSINT Wargame — Storyline & Faction Design

> **Design goal:** every activity is a short **lead** the trainee can finish in
> **5–15 minutes**, but every lead is a thread that ties into one overarching
> conspiracy. The player is an OSINT analyst for the **Tiberian Order** (the
> intelligence agency that hosts every HACKTORIA contract) and works a
> discovery board that slowly unmasks a single hidden network pulling many
> different criminal actors together.

This document defines the world: the factions (some **reused verbatim** from the
existing HACKTORIA plotlines, some **new**), their individual motives, and the
**one underlying plot** they all unknowingly feed. It supersedes the earlier
"generic skill ladder" framing in `README.md` — the skill drills stay the same,
but every one now wears an in-world faction and a plot beat.

---

## 1. The world: "The Gilded Hose"

**The underlying plot (one line):** a hidden coordination node — **the Loom** —
quietly finances, equips, and launders money for a broad spectrum of otherwise-
unconnected groups (cartels, corrupt generals, corrupt politicians, hackers,
terrorist cells, and a global doomsday cult) so that, acting in parallel, they
destabilize several target economies at once to enrich a handful of the Loom's
members.

**Player framing:** You are a **Tiberian Order** OSINT analyst. Each contract is
a tip, a seized file, a flagged vessel, or a scrap of intercepted traffic that
lands on your discovery board. Your job is to resolve the lead (find the place,
the ship, the person, the code, the street) — 5–15 minutes per lead. As lead
after lead resolves, the **link graph** in your case file keeps showing the same
logistics, cash movements, and cover companies — until the pattern of *who
benefits* becomes the story.

> **Why this keeps the 5–15 min cadence:** each challenge is a real, self-
> contained puzzle (a photo to geo, a vessel to trace, a cipher to break). The
> connective tissue is **fictional framing text only** — it never adds solve
> steps. A trainee can grab any single lead and finish it in minutes; the meta-
> plot is the reward for doing many.

---

## 2. Factions

Three columns: **Status** = `existing` (already has HACKTORIA plotlines to reuse)
or `new` (we build the story), **Motive**, and **which challenges belong to it**.

### 2.1 Protagonist — the player's side

| Faction | Status | Role / motive | Motivation for the player |
|---|---|---|---|
| **Tiberian Order** | existing | Intelligence agency that fields every HACKTORIA contract | The player's employer; every lead is a filed contract |

### 2.2 Antagonist factions (the "Front")

Each group below is a real, differently-motivated actor — but all traffic with
**the Loom** (§2.3), usually unknowingly.

| Faction | Status | Concept | Motive (their own) | Challenges belonging to it |
|---|---|---|---|---|
| **Order of Hades** | existing | Shadowy anarchic criminal/mastermind org; the original recurring HACKTORIA villain | Total control through chaos; steals, kidnaps, bombs | operation-bloodhound, rogue-agent, echoes-of-retaliation, kidnapped |
| **Crimson Cartel (Los Aztecas)** | existing | Mexican / Colombian narcotics & goods-smuggling network | Money from moving narcotics and finished goods | florida-snow, the-cartel-connection, gas-attack, a-strange-file |
| **The Gilded Generals** | new | A cadre of corrupt military officers (multiple nations) who profit by selling military tech & classified equipment abroad | Personal wealth from selling hardware and blueprints the state owns | friendly-fire, naval-intrusion, cold-war-enemies, last-flight |
| **The Chancellery (Palladium Politica)** | new | Corrupt politicians & bureaucrats who use legal cover (permits, customs, diplomatic bags) to move goods, launder cash, and hollow out their own economies | Political power + a cut of every sanctioned "trade" | line-of-control, prisoner-of-war, road-to-nowhere, undercover-fleet |
| **The Wire Syndicate** | new | A transnational hacking collective that runs the digital side: crypto laundering, wiretaps, dead drops, fake funds | Money + the thrill of owning the infrastructure | on-the-wire, operation-wiretap, emergency-transmission, the-copycat-killer, the-sleeper-cell, dialogues-from-atlantis |
| **Ashfall** | new | Several small terrorist/paramilitary cells that the Loom arms and funds | Ideology + survival; they want attacks, not money | substation-bombing, saving-isabella, the-russian-blackmailer, operation-bloodhound *(dual)*, pow *(dual)* |
| **House of Krohndahkyr** | existing | The big alien/cryptid doomsday cult-network running nerve-clearing dead drops, "relic" money-laundering, and a huge true-believer funnel | Cult purity + astonishing revenues they believe are prophecy | alien-abduction, chasing-bigfoot, appalachian-aliens, klumgongyn-returns, wheres-klumgongyn, return-of-the-krohndahkyr, intergalactic-warfare, lost-in-time, message-from-hell, nightmare-fuel, the-listeners, the-latvian-connection |

### 2.3 The hidden core — the connector

| Faction | Status | Concept | Motive | Why it exists |
|---|---|---|---|---|
| **The Loom** | new | An un-nameable circle of financiers/power-brokers (a handful of politicians, generals, and corporate lords) who coordinate the Front | Single-minded: cripple rival economies so a few companies/regimes profit hugely | It is the **slow reveal**. Every lead the player solves adds a node to the link graph; "who benefits from all of this at once" is the question the capstone answers |

---

## 3. The link graph — how the plot ties together

The connective device that gives the meta-plot without adding solve time: a
fictional **case-file / link graph** in the player's OSINT workspace. Every
resolved lead writes a small "linked entity" line. After a few leads, the graph
shows the same **cutouts** recurring across otherwise-unconnected factions:

- **The cover company** — a handful of shell firms (the fabric/timber/tech
  importers) appear as the *shipper, landlord, or buyer* for several factions.
- **The dead drop** — the cult's "relic" exchange sites double as cash-and-code
  handoffs for cartels, the Syndicate, and Ashfall.
- **The port lane** — the generals' tech and the cartels' goods ride the same
  flagged shipping corridor the Chancellery brokers.
- **The wallet** — the Syndicate's laundered crypto flows are what pay everyone.

So each faction believes it is acting alone; the **recurring logistic handshake**
is the fingerprint of **the Loom**.

> This is the lever for "they all tie to one underlying plotline" — realized as
> recurring **shared logistics**, not as every faction literally plotting
> together. Individual motives stay distinct (money, ideology, power, prophecy)
> exactly as the request describes; the *main plot pushes one way* because all
> their operations flow through the Loom's shared infrastructure.

---

## 4. Challenge → faction → plot-beat map (all ~50 HACKTORIA leads)

Legend: **Keep** = reuse the existing HACKTORIA story as-is (already on-theme);
**Build** = existing puzzle, no real faction/lore yet — we attach a faction and a
plot beat; **New-plot** = new HACKTORIA events from `handler`/`ctf-events`
(available on the platform to slot in).

| Challenge | Skill (from research index) | Faction | Status | Plot beat it advances |
|---|---|---|---|---|
| florida-snow | IMINT geolocation | Crimson Cartel | keep | A cartel air-drop lane — first hint of the shared port corridor |
| the-cartel-connection | IMINT geolocation | Crimson Cartel | keep | Cartel safehouse; links to cover-company buyer |
| gas-attack | reverse-image / IMINT | Crimson Cartel | build | Cartel precursor-shipping note ties to the Loom's chemical buyer |
| a-strange-file | hex decode + geolocation + w3w | Wire Syndicate | keep | Seized hacker meeting point; the Syndicate's dead-drop tune |
| on-the-wire | DNS / packet capture | Wire Syndicate | keep | Syndicate payload exfil; first recurring cover-company URL |
| operation-wiretap | PCAP / decode | Wire Syndicate | keep | Syndicate intercept; a meeting the Chancellery brokers |
| emergency-transmission | crypto + coords | Wire Syndicate | build | Syndicate emergency beacon; code key shared across cells |
| the-copycat-killer | browser forensics | Wire Syndicate | build | Syndicate "burn" laptop; ties to the Loom's wallet |
| the-sleeper-cell | multi-decrypt + geo | Wire Syndicate (lends code) / Ashfall | build | The shared encryption the Loom hands all Front cells |
| dialogues-from-atlantis | hidden URL | Wire Syndicate | build | A Syndicate + cult joint dead-drop slip |
| friendly-fire | vehicle/IMINT ID | Gilded Generals | build | A general selling armored tech — serial ties to blueprints |
| naval-intrusion | vessel/class ID | Gilded Generals | build | General selling a PLAN frigate class; the exporters' lane |
| cold-war-enemies | air-base geolocation | Gilded Generals | build | The generals' safe airfield; same logistics as the lane |
| last-flight | aviation / aircraft lifecycle | Gilded Generals | build | A general's decommissioned aircraft used to move tech |
| line-of-control | geo + translation + temporal | Chancellery | keep | Politico vectoring a strike date — "who benefits" node |
| prisoner-of-war | NGO / AO geolocation | Chancellery (dual Ashfall) | build | An AO the Chancellery quietly refuses to intervene in |
| road-to-nowhere | stego + geo | Chancellery | build | A sanctioned smuggling route the cover-company files |
| undercover-fleet | maritime / AIS + IMINT | Chancellery | keep | The flagged port lane vessel — the centerpiece link |
| operation-bloodhound | geo + web | Order of Hades | keep | Hades low-level operative; the Order's own motive thread |
| rogue-agent | decode + geo | Order of Hades | keep | A Hades cutout in the field |
| echoes-of-retaliation | IP + street-view + w3w | Order of Hades | keep | A Hades execution/payment site |
| kidnapped | multi-cipher + w3w | Order of Hades | keep | A Hades hostage; motive is control, not money |
| substation-bombing | web + geo + tech | Ashfall | build | Ashfall's first strike, funded & cleared by the Loom |
| saving-isabella | Morse + w3w | Ashfall | build | Ashfall distress-signal dead drop on the shared network |
| the-russian-blackmailer | social footprint | Ashfall (lone-actor-financed) | keep | A freelancer the Loom blackmails into parotting |
| the-listeners | IMINT street geolocation | House of Krohndahkyr | build | Cult nerve-center; doubles as cover-company HQ |
| the-latvian-connection | reverse-image geo | House of Krohndahkyr | build | Cult "relic" laundering property |
| alien-abduction | NUFORC web research | House of Krohndahkyr | keep | Cult funnel — the "believers' wallet" |
| chasing-bigfoot | archival web research | House of Krohndahkyr | keep | Cult origin myth tying believers to the funnel |
| appalachian-aliens | audio + hex + geo | House of Krohndahkyr | build | Cult signal site; same dead-drop system |
| klumgongyn-returns | cipher translation | House of Krohndahkyr | keep | Cult cipher used for transactions |
| wheres-klumgongyn | street-view geo | House of Krohndahkyr | keep | Cult "traveling saint" — the money caravan |
| return-of-the-krohndahkyr | Latin translation | House of Krohndahkyr | keep | Cult law-text — the "tithing" ledger cipher |
| intergalactic-warfare | coords/geo | House of Krohndahkyr | build | Cult mid-east pilgrimage node feeding the wallet |
| lost-in-time | geo + font + temporal | House of Krohndahkyr | keep | Cult "prophecy site" — the founding dead-drop |
| message-from-hell | ancient-script decode | House of Krohndahkyr | keep | Cult cipher-core, reused by other Front cells |
| nightmare-fuel | EXIF / metadata | House of Krohndahkyr | build | Cult "relic" video hiding a Loom wallet key |
| lost-at-sea | maritime + simple crypto | Chancellery (dual) | keep | A decoy "legitimate" shipping manifest |
| lost-down-under | decode + geo + spatial | Wire Syndicate | build | Syndicate route-math; another recurring cover firm |
| the-road-to-rome | aerial geo + historical | Chancellery | build | Historical corroboration of the "approved trade" cover |
| the-spy-who-vanished | Wayback + social | Wire Syndicate | keep | A Syndicate handler scrubbing identity |
| peepeekun | web → w3w → archive | House of Krohndahkyr | build | Full cult→cartel money pass through jigsaw dead-drops |
| kanonniers | landmark + w3w | House of Krohndahkyr | build | A cult relic cache on the shared lane |
| far-away-outpost | satellite map | House of Krohndahkyr | build | A cult/Ashfall desert staging post |
| the-butcher | hex → audio | House of Krohndahkyr | build | The cult "butcher" who prices contracts in relics |
| the-midnight-slayer | multi-point geo + w3w | Order of Hades | keep | Hades assets; the Order's local muscle |
| the-killer-clown | park geolocation | Order of Hades | keep | Hades hit location — a silent-cutout node |
| the-spy-who-vanished | (dup name) Wayback | Wire Syndicate | build | *(dedupe with the-spy-who-vanished above)* |
| catch-me-if-you-can | geo/social (no write-up) | Order of Hades | build | A Hades escapee; pure-new plot thread to write |
| intro_to_maritime_osint | maritime/AIS (course) | Chancellery | build | The training primer for the undercover-fleet lane |
| intro_to_chinese_osint | CN platforms (course) | Chancellery / Gilded Generals | build | Training primer for the generals' exporter ties |
| friendly-fire | (see above) | Gilded Generals | build | (covered) |

---

## 5. The capstone: "Who Weaves the Loom?"

The unifying endgame challenge. The trainee has resolved enough links to see the
recurring logistics handshake. The final lead asks them to **assemble the link
graph** (which cover company, which port lane, which wallet, which dead drop
everyone shares) and issue one **sourced intelligence assessment** naming the
**Loom** as the coordinating buyer. Everything the earlier drills taught
(geolocation, maritime, crypto, footprint, corroboration, reliability scoring)
is exercised in producing that single fused product — the real "answer" is the
reliability-scored, sourced statement, exactly the capstone `osint-12` already
shapes.

---

## 6. Cadence & delivery

- **Every lead = one challenge = one flag** = 5–15 min of real solving.
- The **fiction** (which faction, which plot beat) is a framing paragraph at the
  top of each challenge description. It adds atmosphere, **no** solve steps.
- The **link graph** lives in the player's fictional case-file (and, where
  possible, a small always-visible "Case File" hint slot listing previously
  resolved linked entities) rather than as an extra puzzle.
- New-plot (non-HACKTORIA) threads — mostly the built **Gilded Generals**,
  **Chancellery**, **Wire Syndicate**, **Ashfall** factions — are written from
  scratch in `scripts/build_osint.py` using each challenge's real premise from
  the write-ups, so we "build on the plotlines that do not already have a
  story," exactly as requested.

---

## 7. Canon-checks (grounding in the real lore)

- **Tiberian Order** — confirmed in `operation-bloodhound` write-up ("Ricardo
  Alvarez... works for the Tiberian Order").
- **Order of Hades** — confirmed in `operation-bloodhound` write-up ("operative
  for the shadowy Order of Hades").
- **Cartels** — confirmed in `florida-snow` / `the-cartel-connection` (narcotics
  drops, Colombia safehouse).
- **Russian blackmailer**, **PLAN/naval**, **pandemic-cult** threads all exist
  in the source write-ups and are reused where on-theme; the **Gilded Generals /
  Chancellery / Wire Syndicate / Ashfall / the Loom** are our new connective
  tissue built on top.
