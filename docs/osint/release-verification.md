# OSINT — Release Verification Checklist

**Audience:** the release manager (the organizer who will move the track from
`hidden` to `visible`). Every flag currently in `scripts/build_osint.py` is an
**illustrative placeholder** until this checklist is cleared. Check every row
below against a **live, legal, public source** immediately before the event,
swap the flagged string in `build_osint.py`'s `FLAGS` dict to the verified
value, re-run:

```bash
python3 scripts/build_osint.py
python3 scripts/build_osint.py   # again to confirm
```

and then re-sync to CTFd (`ctf challenge sync osint/` or the deploy pipeline).
Do not hand-edit `osint/*/challenge.yml`.

> **Also re-check** `docs/osint/writeups.md` and `docs/osint/cheatsheet.md` —
> they echo every flag. The single source of truth is the builder; if a flag
> changes, those two files must be updated to match (a CI check for writeup↔
> builder flag parity exists).

## Pre-flight (one-time)

- [ ] Run `python -m compileall -q scripts/build_osint.py` — must pass.
- [ ] Generate once in `hidden` and once with `CEI_OSINT_RELEASE_STATE=visible`
      and confirm all 42 `osint/*/challenge.yml` files are valid YAML
      (`yaml.safe_load`) and category/value/flag fields are present.
- [ ] Confirm `docs/osint/writeups.md` sections and `FLAGS` stay 1:1
      (`python C:\Users\Ismael\AppData\Local\Temp\opencode\check_flags.py`).

## Per-arc checklist

Tick each lead **only after you have personally confirmed the answer on a real
public tool** (never from a write-up copy-paste).

### Arc 0 — Onboarding

| Lead | What to verify | Public tool | Flag in builder |
|---|---|---|---|
| `osint-00-start-here` | static phrase | — | `WELCOME TO OSINT` |

### Arc 1 — Crimson Cartel (4)

| Lead | What to verify | Tool/domain | Flag |
|---|---|---|---|
| `01-cartel-airdrop` | coastal drop point → coord | Google Earth, maritime drop archive | `cartel-drop-lane` |
| `02-cartel-safehouse` | downtown beach-house address | Maps/Street View | `cartel-safehouse-street` |
| `03-cartel-precursor` | original image → publishing domain | Google/Yandex reverse image | `cover-company-source` |
| `04-cartel-meet` | file→hex→images→what3words triple | Hex converters, what3words | `definitive.doorpost.thickness` |

### Arc 2 — Wire Syndicate (6)

| Lead | What to verify | Tool | Flag |
|---|---|---|---|
| `05-synd-exfil` | DNS chain → pastebin/raw URL → dead-drop | Wireshark/NetworkMiner | `exfil-pastebin-url` |
| `06-synd-intercept` | pcap → meet time+place | Wireshark, decoders | `meet-time-place` |
| `07-synd-beacon` | Base85+Vigenère(coords) → decimal | Ascii85, Vigenère | `-1.251946,-78.370167` |
| `08-synd-burn` | browser artifacts → assembled flag | SQLite browser, image editor | `flag-copycatkitty` |
| `09-synd-wallet` | Base64→decimal→Vigenère → target | Base64, Vigenère | `sofi-stadium-33.953417` |
| `10-synd-deaddrop` | document fragments → `https://…` | Text editor, case-sensitive check | `dead-drop-link` |

### Arc 3 — Gilded Generals (4)

| Lead | What to verify | Tool | Flag |
|---|---|---|---|
| `11-gen-tank` | drone still → AFV type (Merkava Mk 4M) | Armored-vehicle guide | `merkava-mk-4m` |
| `12-gen-frigate` | UAV hull→ class + NATO name (054A) | PLAN vessel catalog | `type-054a-jiangkai-II` |
| `13-gen-airfield` | satellite → Khmeimim hierarchy | Google Earth | `syria-latakia-jableh` |
| `14-gen-aircraft` | airframe → current base + history | Planespotters | `canada-essa-sweden` |

### Arc 4 — the Chancellery (6)

| Lead | What to verify | Tool | Flag |
|---|---|---|---|
| `15-chan-strike` | 3 IAF bases + briefing + person/time | Maps, translation | `jaisalmer-amritsar-naliya` |
| `16-chan-ao` | child-photo → NGO facility | NGO registries | `sos-childrens-village` |
| `17-chan-smuggle` | stego image → `20.899370,95.118041` | steghide | `20.899370,95.118041` |
| `18-chan-fleet` | IMINT coord → AIS → Guria/IMO + port history | MarineTraffic, IMO | `guria-imo-9758351` |
| `19-chan-manifest` | Narwhal2018 log → beacon last coords | Log reader, maps | `narwhal-log-recovered` |
| `20-chan-cover` | aerial → Castello di Brescia | Aerial/building compare | `castello-di-brescia` |

### Arc 5 — Order of Hades (6)

| Lead | What to verify | Tool | Flag |
|---|---|---|---|
| `21-hades-operative` | GPS-camera photos → hotel + phone | Maps | `latanya-hotel-ankara` |
| `22-hades-cutout` | image text → `serbia-rakinac…` | Text decoder | `serbia-rakinac-44.259654` |
| `23-hades-payment` | IP→ `.md`→`.png` → Street View → triple | IP loc, Street View | `continuation.partakes.devolved` |
| `24-hades-hostage` | cipher stack → `inched.barman.fast` | Base64/ROT47/hex | `inched.barman.fast` |
| `25-hades-hit` | park photo → intersection | Trail maps | `cedar-rose-park` |
| `26-hades-slayer` | 4 points → centroid → riddle → address | what3words, Maps | `forum.report.rent` |

### Arc 6 — Ashfall (3)

| Lead | What to verify | Tool | Flag |
|---|---|---|---|
| `27-ash-strike` | conflict map UW53036 → Кіндійська 35/6 | Eyes-on-Russia, infra docs | `kindijska-35-6kv` |
| `28-ash-distress` | Morse(omega expendable ridge) → triple | Morse decoder | `omega.expendable.ridge` |
| `29-ash-freelancer` | Sugarmill Pub → reviews → Mastodon → address | Restaurant Guru, Maps | `evgenil-kuznetsova-11-kestrel` |

### Arc 7 — House of Krohndahkyr (10)

| Lead | What to verify | Tool | Flag |
|---|---|---|---|
| `30-cult-funnel` | NUFORC filter → report id/URL | nuforc.org | `nuforc-sighting-id` |
| `31-cult-origin` | key-phrases → exact article URL | Search engine | `bigfoot-article-url` |
| `32-cult-signal` | spectrogram → hex → `37.455327,…` → facility | Audio analyzer | `37.455327,-79.981241` |
| `33-cult-cipher` | language-picture → credential | Cipher key | `klumgongyn-credential` |
| `34-cult-caravan` | tourist photo → Elhe Didi Magu | Street View | `maldives-elhe-didi-magu` |
| `35-cult-ledger` | Latin → De Vita Caesarum | Translator | `gaius-suetonius-de-vita-caesarum` |
| `36-cult-prophecy` | palace photo → font decode → 1930 | Font decoder, Maps | `amber-sam-sing-1930` |
| `37-cult-relic` | video → EXIF/container key | EXIFTool | `relic-video-key` |
| `38-cult-money` | jigsaw→w3w→vault → `case.thrillers.jams` | puzzel.org, w3w | `case.thrillers.jams` |
| `39-cult-cache` | cannon + 0525 → w3w triple | what3words | `0525-elburg-punk-runways-messed` |

### Arc 8 — the Loom (capstone) (2)

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
