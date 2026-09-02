# Threadline - Writeups (Answer Key)

**Instructor / organizer only - not for participant distribution.**

Answer key for the **42-lead "Gilded Hose" campaign** (see `storyline.md`).
Every flag below is the single source of truth in `scripts/build_threadline.py`
(`FLAGS`); if a value is re-verified against real public sources at release
time, change it there and re-run `python3 scripts/build_threadline.py` - never edit
generated files. All values below are currently **illustrative placeholders**
pending that release-time verification.

Each lead: **objective**, **method**, **flag**, **doctrine anchor**.

---

## Arc 0 - Onboarding

### threadline-00-start-here - Wargame Briefing
- Objective: confirm the legal/PAI boundary and set up the local toolset.
- Method: read the briefing; open Maps, reverse-image, EXIFTool, what3words,
  FIRMS, MarineTraffic, FlightRadar24, Wayback, CyberChef.
- Flag: `WELCOME TO THREADLINE`
- Doctrine: ATP 2-22.9 PAI / legal boundary.

## Arc 1 - Crimson Cartel (the goods lane)

### threadline-01-cartel-airdrop - Cartel Air-Drop Lane
- Objective: locate a remote coastal air-drop point from one satellite frame.
- Method (from `florida-snow`): annotate street grid/coastline/landmarks in the
  overhead still; match to public satellite imagery; narrow region → city → exact
  coastal point.
- Flag: `spain-cambados-aldea-o-facho`
- Doctrine: GEOINT/IMINT; FM IPB ground-truth.

### threadline-02-cartel-safehouse - Cartel Safehouse
- Objective: pin a downtown beach-house address from one photo.
- Method (from `the-cartel-connection`): extract street signs/district clues;
  search maps + Street View; read the house number.
- Flag: `calle-106-riomar-barranquilla-atlantico-colombia`
- Doctrine: FM IPB ground-truth.

### threadline-03-cartel-precursor - Precursor Source
- Objective: find the original public appearance of an image tied to a
  cover-company buyer.
- Method (from `gas-attack`): reverse-image the ORIGINAL file; identify first
  source; note the publishing domain/company.
- Flag: `cover-company-source`
- Doctrine: provenance/authentication; FM IPB.

### threadline-04-cartel-meet - The Strange File
- Objective: decode a seized file and geolocate its meeting point.
- Method (from `a-strange-file`, ground truth): File-to-Hex → Hex-to-Text yields
  two images; geolocate both; reduce spot to what3words `definitive.doorpost.thickness`;
  compose `libya-nalut-dirj-47-definitive-doorpost-thickness-car-wash`.
- Flag: `libya-nalut-dirj-47-definitive-doorpost-thickness-car-wash`
- Doctrine: ATP discovery/collection + geo.

## Arc 2 - Wire Syndicate (the hackers)

### threadline-05-synd-exfil - Exfil on the Wire
- Objective: recover the Syndicate's exfil URL from packet capture.
- Method (from `on-the-wire`): ID the pcap despite mangled extension; filter
  DNS/NSLOOKUP; read the pastebin/raw URL; follow to the dead-drop link.
- Flag: `https://pastebin.com/raw/U7zb8Kyh`
- Doctrine: discovery/collection; OPSEC.

### threadline-06-synd-intercept - Intercepted Meeting
- Objective: extract a meeting time/place from intercepted traffic.
- Method (from `operation-wiretap`): open pcap; find the shared link; decode the
  meeting details; format time+venue.
- Flag: `sheraton-hotel-zagreb-31-03-2023-1300`
- Doctrine: collection → analysis (FM intelligence cycle).

### threadline-07-synd-beacon - Emergency Beacon
- Objective: break a layered cipher to recover coordinates.
- Method (from `emergency-transmission`, ground truth): Base85-decode; Vigenère
  with key `KLUMKLOOV`; transcribe spoken coords → `-1.251946,-78.370167`.
- Flag: `-1.251946,-78.370167,19`
- Doctrine: capture/authenticate; processing & exploitation.

### threadline-08-synd-burn - The Burn Laptop
- Objective: reconstruct a timeline from browser artifacts.
- Method (from `the-copycat-killer`, ground truth): History → "copy"; Bookmarks
  → "cat"; cached image contrast → "kitty"; assemble `FLAG{copycatkitty}`;
  decrypt Login Data with debug.log key.
- Flag: `FLAG{copycatkitty}`
- Doctrine: discovery/collection; intelligence cycle.

### threadline-09-synd-wallet - The Wallet Ledger
- Objective: multi-stage decrypt an email to reveal a target coordinate.
- Method (from `the-sleeper-cell`, ground truth): Base64 → decimal → Vigenère key
  `Androktasiai` → `SoFi-Stadium 33.953417,-118.338863`.
- Flag: `SoFi-Stadium-33.953417,-118.338863,18`
- Doctrine: capture/authenticate.

### threadline-10-synd-deaddrop - Dead-Drop Slip
- Objective: reassemble a hidden short-link from document fragments.
- Method (from `dialogues-from-atlantis`, ground truth): find `bit.ly` +
  fragment `3Dq6rGW`; assemble case-sensitively `https://bit.ly/3Dq6rGW`.
- Flag: `https://bit.ly/3Dq6rGW`
- Doctrine: capture/authenticate; OPSEC.

## Arc 3 - Gilded Generals (military tech sales)

### threadline-11-gen-tank - The Stolen AFV
- Objective: identify an armored vehicle from a drone still.
- Method (from `friendly-fire`, ground truth): hull/turret/gun layout → Merkava
  Mk 4M.
- Flag: `israel-merkava-mk-4m`
- Doctrine: IMINT target acquisition.

### threadline-12-gen-frigate - Sold Frigate Plans
- Objective: classify an unmarked warship from a UAV image.
- Method (from `naval-intrusion`, ground truth): hull/sensor/weapon layout →
  Type 054A (Jiangkai II).
- Flag: `type-054a-jiangkai-II`
- Doctrine: IMINT target acquisition; naval recognition.

### threadline-13-gen-airfield - The Safe Airfield
- Objective: locate an air base and structure its hierarchy.
- Method (from `cold-war-enemies`, ground truth): Khmeimim Air Base →
  Syria→Latakia→Jableh.
- Flag: `syria-latakia-jableh-khmeimim-air-base`
- Doctrine: IPB ground-truth; targeting.

### threadline-14-gen-aircraft - The Decommissioned 747
- Objective: identify an aircraft, its current base, and a historical deployment.
- Method (from `last-flight`, ground truth): Jumbo Stay hotel @ Arlanda (ESSA);
  Planespotters history → operated in Canada April 1993.
- Flag: `canada-essa-sweden`
- Doctrine: IPB ground-truth; temporality.

## Arc 4 - the Chancellery (corrupt politicians)

### threadline-15-chan-strike - The Strike Window
- Objective: synthesize locations + person + timing into one answer.
- Method (from `line-of-control`, ground truth): IAF bases Jaisalmer/Amritsar/
  Naliya; translate Urdu briefing; commander Imran Hameed; next Tuesday 2000hrs.
- Flag: `jaisalmer-amritsar-naliya-tuesday-2000-imran-hameed`
- Doctrine: intelligence cycle; targeting.

### threadline-16-chan-ao - The Quiet AO
- Objective: geolocate an NGO facility inside an operational area.
- Method (from `prisoner-of-war`, ground truth): ambush coord near Kayes/Mali;
  scan RN1 corridor; match children's facility → Village d'Enfants SOS Khouloum.
- Flag: `village-d-enfants-sos-khouloum-kayes`
- Doctrine: spatial/IPB; targeting.

### threadline-17-chan-smuggle - The Sanctioned Road
- Objective: extract stego-hidden coordinates and map them.
- Method (from `road-to-nowhere`, ground truth): marker + number 1920 → steghide
  password 1920 → location.txt → `20.899370,95.118041` (Myanmar).
- Flag: `20.899370,95.118041,16`
- Doctrine: capture/authenticate; discovery.

### threadline-18-chan-fleet - The Flagged Corridor (centerpiece)
- Objective: fuse IMINT with AIS to reconstruct a vessel's port history.
- Method (from `undercover-fleet`, ground truth): coords `19.5084,-49.6377` on
  03 DEC 2025 22:47 UTC @ 16.5 kn → vessel `Guria`, IMO `9758351`; verify visuals;
  ports Abidjan→Mindelo→Las Palmas(44d)→Manzanillo→Posorja.
- Flag: `guria_9758351_abidjan.ivory.coast_mindelo.cape.verde_las.palmas.spain_manzanillo.panama_posorja.ecuador`
- Doctrine: multi-INT fusion; collection management.

### threadline-19-chan-manifest - The Decoy Manifest
- Objective: derive a password from vessel metadata and interpret telemetry.
- Method (from `lost-at-sea`, ground truth): password `Narwhal2018` (ship+year);
  beacon log last coords `44.470394,32.264429`, NNE 32°, 7 kts.
- Flag: `44.470394,32.264429`
- Doctrine: discovery/collection; maritime.

### threadline-20-chan-cover - The Approved Trade
- Objective: corroborate an aerial photo with historical clues.
- Method (from `the-road-to-rome`, ground truth): aerial → Castello di Brescia;
  cross-ref Ten Days of Brescia / Venetian Lion.
- Flag: `castello-di-brescia`
- Doctrine: corroboration; IPB.

## Arc 5 - Order of Hades

### threadline-21-hades-operative - The Gifted Jacket
- Objective: locate where a Hades defector is staying from GPS-camera photos.
- Method (from `operation-bloodhound`, ground truth): photos → Latanya Hotel,
  Ankara; listing phone `+90 312 416 88 00`.
- Flag: `latanya-hotel-ankara-+903124168800`
- Doctrine: collection management; IPB.

### threadline-22-hades-cutout - The Hades Cutout
- Objective: decode a hidden location string and verify spatially.
- Method (from `rogue-agent`, ground truth): decode `æÊ…` message →
  `serbia-rakinac-44.259654-21.057843`.
- Flag: `serbia-rakinac-44.259654-21.057843`
- Doctrine: discovery/collection; IPB.

### threadline-23-hades-payment - Payment on the Corner
- Objective: pivot IP → imagery → what3words.
- Method (from `echoes-of-retaliation`, ground truth): IP `188.214.181.38` →
  Yazd; rename `.md`→`.png`; Street View Hamane `31.8501791,53.8824913` → w3w
  `continuation.partakes.devolved`.
- Flag: `continuation.partakes.devolved`
- Doctrine: IPB ground-truth; multi-INT.

### threadline-24-hades-hostage - The Hostage Note
- Objective: break a strict-order cipher stack to a rescue location.
- Method (from `kidnapped`, ground truth): Base64 → ROT47 → hex → substitution
  table (q→d, r→e, s→f, o→b, p→c) → w3w `inched.barman.fast`.
- Flag: `inched.barman.fast`
- Doctrine: capture/authenticate.

### threadline-25-hades-hit - Dead Man's Park
- Objective: pin a park/path intersection from a photo.
- Method (from `the-killer-clown`, ground truth): Berkeley parks → Ohlone
  Greenway ∩ Cedar Rose Park.
- Flag: `cedar-rose-park-ohlone-greenway`
- Doctrine: IPB ground-truth.

### threadline-26-hades-slayer - Four Points to an Address
- Objective: multi-point plot → centroid → riddle → address.
- Method (from `the-midnight-slayer`, ground truth): geocode 4 body drops; X →
  Carroll Park Golf Course; w3w `belts.chips.mental` unlocks riddle; owl answer →
  killer address → w3w `forum.report.rent`.
- Flag: `forum.report.rent`
- Doctrine: spatial/IPB; targeting.

## Arc 6 - Ashfall

### threadline-27-ash-strike - Grid-Strike Plot
- Objective: fuse conflict-map + mapping + infra docs to ID a targeted asset.
- Method (from `substation-bombing`, ground truth): Eyes-on-Russia event UW53036
  → Antonivka, Kherson; substation Кіндійська; docs → 35/6 kV.
- Flag: `Antonivka-Khersonska-Kindijska-35-6`
- Doctrine: IPB; targeting.

### threadline-28-ash-distress - Morse on the Dead Network
- Objective: transcribe Morse distress into a what3words location.
- Method (from `saving-isabella`, ground truth): callsign `mor31`; phrase
  "omega expendable ridge" → w3w `omega.expendable.ridge`.
- Flag: `omega.expendable.ridge`
- Doctrine: discovery/collection; spatial.

### threadline-29-ash-freelancer - The Financed Freelancer
- Objective: trace a person across platforms to a physical address.
- Method (from `the-russian-blackmailer`, ground truth): Sugarmill Pub, Bourne;
  translate Russian speech ("this pie is very good… leave a review"); reviews by
  Evgenil Kuznetsova (Restaurant Guru/TripAdvisor) → Mastodon handle → declared
  house → `11 Kestrel Drive`.
- Flag: `Evgenil_Kuznetsova_11_Kestrel_Drive`
- Doctrine: multi-INT fusion; corroboration; OPSEC.

## Arc 7 - House of Krohndahkyr (cult / money funnel)

### threadline-30-cult-funnel - The Believers' Ledger
- Objective: retrieve an exact record URL from a public database.
- Method (from `alien-abduction`, ground truth): NUFORC filter Broomfield CO /
  Apr 2 2023 / 22:00 / Circle / 10 min → report id 175200 →
  `https://nuforc.org/sighting/?id=175200`.
- Flag: `https://nuforc.org/sighting/?id=175200`
- Doctrine: collection management; corroboration.

### threadline-31-cult-origin - Origin Myth
- Objective: recover one specific old article URL from sparse clues.
- Method (from `chasing-bigfoot`, ground truth): 1970s military night-road query →
  `thecryptocrew.com/2014/06/driver-has-close-sighting-of-bigfoot.html`.
- Flag: `https://www.thecryptocrew.com/2014/06/driver-has-close-sighting-of-bigfoot.html`
- Doctrine: collection management; corroboration.

### threadline-32-cult-signal - The Signal Site
- Objective: spectrogram → hex → site → facility identification.
- Method (from `appalachian-aliens`, ground truth): spectrogram warning + hex →
  `galacticfiles.org` → coords `37.455327,-79.981241` → Roanoke Cement Co,
  Catawba Rd.
- Flag: `37455327-79981241-catawba-rd`
- Doctrine: discovery/collection; multi-INT.

### threadline-33-cult-cipher - The Cult Cipher
- Objective: translate an invented script into a credential.
- Method (from `klumgongyn-returns`, ground truth): language-picture key →
  translate Klumgon characters → password unlocks flagfile.
- Flag: `klumgongyn-credential`
- Doctrine: capture/authenticate.

### threadline-34-cult-caravan - The Traveling Saint
- Objective: pin a street from a tourist photo.
- Method (from `wheres-klumgongyn`, ground truth): Maldives → Elhe Didi Magu;
  verify via Street View.
- Flag: `maldives-elhe-didi-magu`
- Doctrine: IPB ground-truth.

### threadline-35-cult-ledger - The Tithing Ledger
- Objective: identify the classical source of a translated text.
- Method (from `return-of-the-krohndahkyr`, ground truth): translate Latin →
  De Vita Caesarum (Suetonius).
- Flag: `gaius-suetonius-tranquillus-de-vita-caesarum`
- Doctrine: capture/authenticate; corroboration.

### threadline-36-cult-prophecy - The Prophecy Site
- Objective: connect location + decoded message + date across a chain.
- Method (from `lost-in-time`, ground truth): Amber Palace Jaipur; Kitisakkullian
  font decodes Gorlaer message; Sam Sing Kung Temple + year 1930.
- Flag: `amber-palace-sam-sing-kung-temple-1930`
- Doctrine: IPB ground-truth; temporality.

### threadline-37-cult-relic - Relic Video
- Objective: mine media metadata for a hidden credential.
- Method (from `nightmare-fuel`, ground truth): download video; metadata viewer
  reveals the embedded password string.
- Flag: `fh453n3fk45b384gm$&%#fjksdfmo94853ff`
- Doctrine: discovery/collection; OPSEC.

### threadline-38-cult-money - The Money Pass
- Objective: staged web → w3w → vault credential chain.
- Method (from `peepeekun`, ground truth): jigsaw → Dropbox folder → three w3w
  locations → vault password = first words `case.thrillers.jams` → final key
  `D94KF932409KGL09324`.
- Flag: `D94KF932409KGL09324`
- Doctrine: multi-INT fusion; OPSEC.

### threadline-39-cult-cache - Relic Cache
- Objective: landmark → what3words + local context.
- Method (from `kanonniers`, ground truth): old cannon in Elburg; area code
  0525; w3w `punk-runways-messed`; unlock `0525-Elburg-punk-runways-messed`.
- Flag: `0525-Elburg-punk-runways-messed`
- Doctrine: IPB ground-truth.

## Arc 8 - Corroboration & the Loom (capstone)

### threadline-40-loom-corroborate - Source Discipline
- Objective: corroborate a lead with two independent sources and score them.
- Method: two independent PAI sources agreeing; rate each on a reliability/
  credibility scale; state contradictions before committing.
- Flag: `corrob-two-sources`
- Doctrine: corroboration + reliability scale (ATP/FM).

### threadline-41-loom-assess - Who Weaves the Loom? (Capstone)
- Objective: name the coordinating network behind all factions in one sourced
  product.
- Method: correlate linked entities across the whole campaign - recurring cover
  company, port lane (`threadline-18`), wallet (`threadline-09`), dead drops (`threadline-10`,
  `threadline-38`) - score sources, then issue a cited assessment (place/date/time/
  origin).
- Flag: `the-loom-assess-product`
- Doctrine: multi-INT fusion; analytic product; reliability scoring.
