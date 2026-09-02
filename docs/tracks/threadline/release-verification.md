# Threadline - Release Verification Checklist

**Audience:** the release manager (the organizer who will move the track from
`hidden` to `visible`). All flags in `scripts/build_threadline.py` have been
**reverified against the Hacktoria ground-truth writeups extracted from
`hacktoria-archive/`** (see `skill-building-priority.md` for provenance).
Still check every row below against a **live, legal, public source**
immediately before the event — if any source has shifted, swap the flagged
string in `build_threadline.py`'s `FLAGS` dict to the new verified value, re-run:

```bash
python3 scripts/build_threadline.py
python3 scripts/build_threadline.py   # again to confirm
```

and then re-sync to CTFd (`ctf challenge sync threadline/` or the deploy pipeline).
Do not hand-edit `threadline/*/challenge.yml`.

> **Also re-check** `docs/tracks/threadline/writeups.md` and `docs/tracks/threadline/cheatsheet.md` —
> they echo every flag. The single source of truth is the builder; if a flag
> changes, those two files must be updated to match (a CI check for writeup↔
> builder flag parity exists).

## Pre-flight (one-time)

- [ ] Run `python -m compileall -q scripts/build_threadline.py` — must pass.
- [ ] Generate once in `hidden` and once with `THREADLINE_RELEASE_STATE=visible`
      and confirm all 42 `threadline/*/challenge.yml` files are valid YAML
      (`yaml.safe_load`) and category/value/flag fields are present.
- [ ] Confirm `docs/tracks/threadline/writeups.md` sections and `FLAGS` stay 1:1
      (`python C:\Users\Ismael\AppData\Local\Temp\opencode\check_flags.py`).

## Per-arc checklist

Tick each lead **only after you have personally confirmed the answer on a real
public tool** (never from a write-up copy-paste).

### Arc 0 — Onboarding

| Lead | What to verify | Public tool | Flag in builder |
|---|---|---|---|
| `threadline-00-start-here` | static phrase | — | `WELCOME TO THREADLINE` |

### Arc 1 — Crimson Cartel (4)

| Lead | What to verify | Tool/domain | Flag |
|---|---|---|---|
| `01-cartel-airdrop` | coastal drop point → coord | Google Earth, maritime drop archive | `spain-cambados-aldea-o-facho` |
| `02-cartel-safehouse` | downtown beach-house address | Maps/Street View | `calle-106-riomar-barranquilla-atlantico-colombia` |
| `03-cartel-precursor` | original image → publishing domain | Google/Yandex reverse image | `cover-company-source` |
| `04-cartel-meet` | file→hex→images→what3words triple | Hex converters, what3words | `libya-nalut-dirj-47-definitive-doorpost-thickness-car-wash` |

### Arc 2 — Wire Syndicate (6)

| Lead | What to verify | Tool | Flag |
|---|---|---|---|
| `05-synd-exfil` | DNS chain → pastebin/raw URL → dead-drop | Wireshark/NetworkMiner | `https://pastebin.com/raw/U7zb8Kyh` |
| `06-synd-intercept` | pcap → meet time+place | Wireshark, decoders | `sheraton-hotel-zagreb-31-03-2023-1300` |
| `07-synd-beacon` | Base85+Vigenère(coords) → decimal | Ascii85, Vigenère | `-1.251946,-78.370167,19` |
| `08-synd-burn` | browser artifacts → assembled flag | SQLite browser, image editor | `FLAG{copycatkitty}` |
| `09-synd-wallet` | Base64→decimal→Vigenère → target | Base64, Vigenère | `SoFi-Stadium-33.953417,-118.338863,18` |
| `10-synd-deaddrop` | document fragments → `https://…` | Text editor, case-sensitive check | `https://bit.ly/3Dq6rGW` |

### Arc 3 — Gilded Generals (4)

| Lead | What to verify | Tool | Flag |
|---|---|---|---|
| `11-gen-tank` | drone still → AFV type (Merkava Mk 4M) | Armored-vehicle guide | `israel-merkava-mk-4m` |
| `12-gen-frigate` | UAV hull→ class + NATO name (054A) | PLAN vessel catalog | `type-054a-jiangkai-II` |
| `13-gen-airfield` | satellite → Khmeimim hierarchy | Google Earth | `syria-latakia-jableh-khmeimim-air-base` |
| `14-gen-aircraft` | airframe → current base + history | Planespotters | `canada-essa-sweden` |

### Arc 4 — the Chancellery (6)

| Lead | What to verify | Tool | Flag |
|---|---|---|---|
| `15-chan-strike` | 3 IAF bases + briefing + person/time | Maps, translation | `jaisalmer-amritsar-naliya-tuesday-2000-imran-hameed` |
| `16-chan-ao` | child-photo → NGO facility | NGO registries | `village-d-enfants-sos-khouloum-kayes` |
| `17-chan-smuggle` | stego image → `20.899370,95.118041` | steghide | `20.899370,95.118041,16` |
| `18-chan-fleet` | IMINT coord → AIS → Guria/IMO + port history | MarineTraffic, IMO | `guria_9758351_abidjan.ivory.coast_mindelo.cape.verde_las.palmas.spain_manzanillo.panama_posorja.ecuador` |
| `19-chan-manifest` | Narwhal2018 log → beacon last coords | Log reader, maps | `44.470394,32.264429` |
| `20-chan-cover` | aerial → Castello di Brescia | Aerial/building compare | `castello-di-brescia` |

### Arc 5 — Order of Hades (6)

| Lead | What to verify | Tool | Flag |
|---|---|---|---|
| `21-hades-operative` | GPS-camera photos → hotel + phone | Maps | `latanya-hotel-ankara-+903124168800` |
| `22-hades-cutout` | image text → `serbia-rakinac…` | Text decoder | `serbia-rakinac-44.259654-21.057843` |
| `23-hades-payment` | IP→ `.md`→`.png` → Street View → triple | IP loc, Street View | `continuation.partakes.devolved` |
| `24-hades-hostage` | cipher stack → `inched.barman.fast` | Base64/ROT47/hex | `inched.barman.fast` |
| `25-hades-hit` | park photo → intersection | Trail maps | `cedar-rose-park-ohlone-greenway` |
| `26-hades-slayer` | 4 points → centroid → riddle → address | what3words, Maps | `forum.report.rent` |

### Arc 6 — Ashfall (3)

| Lead | What to verify | Tool | Flag |
|---|---|---|---|
| `27-ash-strike` | conflict map UW53036 → Кіндійська 35/6 | Eyes-on-Russia, infra docs | `Antonivka-Khersonska-Kindijska-35-6` |
| `28-ash-distress` | Morse(omega expendable ridge) → triple | Morse decoder | `omega.expendable.ridge` |
| `29-ash-freelancer` | Sugarmill Pub → reviews → Mastodon → address | Restaurant Guru, Maps | `Evgenil_Kuznetsova_11_Kestrel_Drive` |

### Arc 7 — House of Krohndahkyr (10)

| Lead | What to verify | Tool | Flag |
|---|---|---|---|
| `30-cult-funnel` | NUFORC filter → report id/URL | nuforc.org | `https://nuforc.org/sighting/?id=175200` |
| `31-cult-origin` | key-phrases → exact article URL | Search engine | `https://www.thecryptocrew.com/2014/06/driver-has-close-sighting-of-bigfoot.html` |
| `32-cult-signal` | spectrogram → hex → `37.455327,…` → facility | Audio analyzer | `37455327-79981241-catawba-rd` |
| `33-cult-cipher` | language-picture → credential | Cipher key | `klumgongyn-credential` |
| `34-cult-caravan` | tourist photo → Elhe Didi Magu | Street View | `maldives-elhe-didi-magu` |
| `35-cult-ledger` | Latin → De Vita Caesarum | Translator | `gaius-suetonius-tranquillus-de-vita-caesarum` |
| `36-cult-prophecy` | palace photo → font decode → 1930 | Font decoder, Maps | `amber-palace-sam-sing-kung-temple-1930` |
| `37-cult-relic` | video → EXIF/container key | EXIFTool | `fh453n3fk45b384gm$&%#fjksdfmo94853ff` |
| `38-cult-money` | jigsaw→w3w→vault → `case.thrillers.jams` | puzzel.org, w3w | `D94KF932409KGL09324` |
| `39-cult-cache` | cannon + 0525 → w3w triple | what3words | `0525-Elburg-punk-runways-messed` |

### Arc 8 — the connector (capstone) (2)

| Lead | What to verify | Tool | Flag |
|---|---|---|---|
| `40-loom-corroborate` | 2 independent sources + scored reliability | Public registries, news archives | `corrob-two-sources` |
| `41-loom-assess` | recurring logistics → sourced assessment | Case-file link graph | `the-loom-assess-product` |

## Sign-off

- Date verified: _______________
- Verifier name/handle: _______________
- Number of per-lead rows ticked: ___ / 42
- Any lead unchanged from placeholder? Y / N — if Y, block release.

Regenerate and push only when every ticked row has a checked, dated
re-verification note (even one stale placeholder is a failed gate).