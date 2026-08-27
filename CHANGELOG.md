# Changelog

Format loosely follows [Keep a Changelog](https://keepachangelog.com/).
This repo predates this file (71 commits as of 2026-07-15) — entries below
start from where this file was introduced plus a milestone summary of what
came before it, not a commit-by-commit history. See `git log` for the full
record.

## [Unreleased]

### Added
  - `docs/osint/storyline.md` — overarching faction/plot design for the OSINT
    track: the "Gilded Hose" meta-narrative, a Tiberian Order analyst framing,
    a faction map (reusing real HACKTORIA lore — Tiberian Order, Order of Hades,
    cartels — plus new Gilded Generals / Chancellery / Wire Syndicate / Ashfall /
    the Loom), and a challenge→faction→plot-beat table for all ~50 leads, all
    constrained to 5–15 minute solves.
  - `docs/osint/pr-handoff.md` — handoff report for the OSINT track: where
    things live, the local playtest instance & commands, regeneration steps,
    and maintainer TODOs.
  - `docs/osint/briefing-transcripts.json` — OCR'd source-briefing narratives
    for all 39 source-backed OSINT leads (the briefing PDFs are raster scans
    with no text layer, so the generator renders their text through this file).
  - `scripts/local-ctfd/ocr_briefings.py` — OCRs each Hacktoria briefing PDF
    (RapidOCR) and writes `docs/osint/briefing-transcripts.json`.
  - `scripts/local-ctfd/upload_osint_files.py` — syncs generated OSINT challenge
    files + descriptions into a local CTFd (supports `--remove-pdfs` to prune
    retired PDF attachments).
  - `scripts/build_osint.py` now attaches the best evidence image per
    non-capstone lead and embeds an **"Open Briefing"** intel-report popup
    (Tiberian Order / OSINT Directorate styling, classification mark, "Exhibit"
    pages pulled from the OCR transcripts) in each description instead of
    shipping raw PDFs. Popup is a dependency-free fixed overlay (avoids
    Bootstrap nested-modal failure inside CTFd's own modal).

### Changed
  - `docs/osint/writeups.md`, `docs/osint/release-verification.md`: transliterated
    the `ash-strike` ground-truth flag to keep generated YAML ASCII-safe on
    Windows (`Антонівка-…` → `Antonivka-Khersonska-Kindijska-35-6`).

### Validated
  - Local CTFd black-box run: 42 challenges present, 42 descriptions non-empty,
    39 evidence images attached, 39 retired PDFs pruned, and the live popup
    confirmed to contain the real PDF narrative (e.g. `Cartel Air-Drop Lane`).
  - `python -m compileall` passes for the changed scripts.

- `docs/event-recap-2026-08-06.md`: post-event recap of the 2026-08-06
    track: the "Gilded Hose" meta-narrative, a Tiberian Order analyst framing,
    a faction map (reusing real HACKTORIA lore — Tiberian Order, Order of Hades,
    cartels — plus new Gilded Generals / Chancellery / Wire Syndicate / Ashfall /
    the Loom), and a challenge→faction→plot-beat table for all ~50 leads, all
    constrained to 5–15 minute solves.
  - `docs/osint/` — design + research index (`docs/osint/osint-research-index.md`)
    cataloging real OSINT exercises and CTFs across Hacktoria, Gralhix, and the
    Bellingcat Challenge, including a skill->tool->method->doctrine table mapped
    to ATP 2-22.9 / FM 2-0 / ADP 2-0; plus `learning-objectives.md`,
    `cheatsheet.md`, `writeups.md` for the 13-challenge track.
  - `scripts/build_osint.py` — generator writing the track's CTFd import output
    to the git-ignored `osint/` (single source of truth for flags; release via
    `CEI_OSINT_RELEASE_STATE=visible`, mirroring the AI Copilot track). Track
    stays out of `game-stages.yml` and `challenges/` so all existing stage
    validators are untouched. Expanded to a full **42-lead campaign** organized
    by storyline arc (cartel / syndicate / generals / chancellery / hades /
    ashfall / cult / loom), each a 5–15 min solve wearing faction + plot-beat
    framing.
  - `docs/osint/skill-building-priority.md` — the scoring rubric (skill
    transferability, doctrine anchor, multi-step depth, tool authenticity,
    ground-truth verifiability) used to pick which no-theme challenges earn a
    slot, with the ranked table that drove the 42-lead selection.
  - `docs/osint/writeups.md`, `docs/osint/cheatsheet.md` rewritten for all
    42 leads (answer key verified against the generator's `FLAGS` dict), plus
    `docs/osint/event-runbook.md` — a 7-hour run-of-show with per-arc pacing,
    a 6-hour trim, facilitation notes, and a pre-flight checklist.
  - Verified all 42 OSINT flags against the extracted Hacktoria ground-truth
    writeups in `hacktoria-archive/`; updated `scripts/build_osint.py` `FLAGS`,
    `docs/osint/writeups.md`, and `docs/osint/release-verification.md` to
    ground-truth values (e.g., `https://nuforc.org/sighting/?id=175200`,
    `spain-cambados-aldea-o-facho`, Guria full port chain, Cyrillic substation
    identifier). Wired `deploy.sh` to generate/sync the hidden `osint/` track
    and `validate.yml` to build it in CI.
- `docs/event-recap-2026-08-06.md`: post-event recap of the 2026-08-06
  wargames run — issues hit and fixed, infrastructure end-state, what was
  sacrificed (network + systems), how challenges were played, and player
  participation.
- `docs/event-communications-2026-08-06.md`: condensed recap of the
  `CEI-LABS` channel conversation that drove the event.
- `docs/wargame-story-art.md`: per-level art drawn against each prompt
  in `wargame-story.md` -- 56 pieces, one per level. Explicitly a
  proposal: nothing in it is wired into any Dockerfile or banner
  generator, and the shipped banners remain the programmatic
  storyboard. All pieces are purely pictorial (no written labels), stay
  within 80 columns, and name no command, tool, payload, or step.
- `docs/wargame-story.md`: a simple on-theme story for each track
  ("The Vault at Dryrock" for Bandit, "Signal from the Dark" for
  Krypton, "Into the Mirror" for Natas), broken into the same beats the
  storyboard mechanic already visualizes, plus a per-level generation
  prompt grounded in that beat and the level's public title. Every one
  of the 56 levels has its own distinct beat. Shared prompt constraints
  are stated once rather than repeated per level, and level titles and
  chapter bounds are pulled from the generators so they can't drift.
  Chapter/beat names are internal design vocabulary -- deliberately not
  printed in the banners players see.
- Test guarding that Bandit's now hand-maintained `_CHAPTER_BOUNDS`
  stay contiguous, non-empty, and cover every level exactly once.

### Fixed
- Bandit's chapter boundaries came from an even 34/6 split, which cut
  through related level runs -- Cron Jobs landed in a different chapter
  than Cron Debugging/Scripting, and the git levels straddled two. Now
  8 explicit chapters aligned to the track's actual content clusters,
  so a chapter change always lands where the material changes.
- Bandit's storyboard corridor (34 levels in one 38-char strip) made
  adjacent levels differ by only one character shifting one position --
  imperceptible at a glance (confirmed directly: bandit16/17/18 looked
  identical side by side). Chunked into 6 visibly distinct chapters
  (each with its own bracket style), plus a within-chapter position
  strip, so every level -- including same-chapter neighbors -- is now
  visibly distinct and the art is bigger besides.

### Changed
- Login banner art redesigned around a storyboard mechanic instead of a
  standalone per-level scene: each banner is now a fixed track-wide
  establishing-shot frame plus a programmatically generated progress
  strip (`x`/`-` = ground covered, `o` = this level's position, `.` =
  ground ahead) -- Bandit's is a corridor of rooms, Krypton's is a
  transmission distance from the dish, Natas's is a depth shaft.
  Distinctness across all 56 banners is now structurally guaranteed
  (the strip's shape always differs) instead of hand-invented per level,
  which had repeatedly produced unreadable symbol combinations. See
  `docs/wargame-themes.md`'s "Storyboard mechanic" section.
- Login banners now allow Unicode (box-drawing/block-element/dingbat
  glyphs, restricted to single-width BMP characters so the 80-column
  width check stays meaningful) instead of 7-bit-ASCII-only; frames and
  several core pieces across all three tracks updated to use it. This is
  a deliberate compatibility tradeoff -- rendering now depends on the
  connecting player's terminal supporting UTF-8, unlike plain ASCII.
- Natas banner art is now colored via CSS, reusing the exact per-level
  hue `build/generate_themes.py` already uses for that level's page
  background/headings (cool blue at natas0 -> hot magenta at natas14)
  instead of leaving it plain or inventing a second palette.
- Login banner art policy loosened: art may now visually depict the
  general *kind* of technique/vulnerability involved in a level (a
  rotation dial, a frequency histogram, a directory-traversal arrow, a
  branching commit graph) in addition to the track theme and title --
  still never any actual instructional text/labels naming the specific
  command, payload, key, or steps to solve it. Updated the shared
  generation prompt in `docs/wargame-themes.md` and re-derived several
  Bandit/Krypton/Natas pieces accordingly.
- Bandit and Krypton banners now prepend a fixed, track-wide decorative
  frame (a starlit compound wall; a starfield with an incoming
  wave-train) to every level's art purely for added height. Natas
  banners now mirror each level's art below a waterline, doubling their
  height in a way that fits its own "inverted underworld" theme. No hard
  line-count cap exists anymore -- only the existing 80-char line-width
  limit -- since SSH clients scroll and modern terminals aren't
  height-constrained.

### Added
- `docs/wargame-themes.md`: documents each track's adopted narrative theme
  (Bandit: an outlaw breaking into a guarded compound; Krypton: a hidden
  world transmitting encoded signals; Natas: "Satan" spelled backwards, a
  mirrored/inverted digital underworld) and the reusable prompt used to
  generate all per-level ASCII art from it. Explicitly notes these are
  CEI Labs' own adopted themes, not documented OverTheWire canon.
- Natas login banners now include ASCII art (all 15 levels) -- previously
  plain title/policy text only. Wired into the existing
  `<pre class="cei-login-banner">` HTML block via `cei-natas-banner.php`.

### Changed
- Bandit (34 levels) and Krypton (7 levels) login banner ASCII art
  reworked to draw only on the track's overall theme and the level's
  title, never the level's actual technique/command/vulnerability --
  the previous art (e.g. a literal base64 string for Krypton's Base64
  Decoding, a literal ROT13 shift-map for its substitution cipher level)
  doubled as a mechanical hint. All three tracks' art now follows one
  reusable generation prompt (see `docs/wargame-themes.md`).

- Human-playability support for Krypton: an offline `krypton-tools`
  command for frequency counts, Caesar rotation, Vigenere column
  splitting, and Kasiski evidence; the missing level-3 `found1`-`found3`
  samples; and an in-login pointer to the toolkit.
- A Natas attacker workstation image with the tools players need for the
  middle and late levels, including `xxd`, `rev`, `jq`, Python requests,
  `file`, and `natas-help`.
- Progressive Natas hint rendering with clear Step 1/2/3 headings,
  an HTTP Basic Auth reminder on every tier, and authenticated,
  copy-pasteable `curl` examples.
- `docs/challenge-inventory.md`: the full 59-level structured inventory
  (ID, points, flag source, instance type, reset method, dependencies,
  hints, expected solve path) the production-readiness tracker's §3 P0
  item calls for, generated directly from every `challenges/*/challenge.yml`.
  Surfaced a real finding along the way: `krypton-00` (a real 200-point
  scored challenge, not a tutorial) uses a static, non-per-team flag,
  because it has no per-team instance to scope a dynamic flag to — see
  that doc for the full explanation and a recommended accepted-risk
  write-up.

### Fixed
- Krypton Vigenere guidance now groups letters exactly as the cipher does;
  spaces and punctuation no longer shift the suggested columns.
- Krypton level-2 and later hints now match the deployed command-line
  behavior and point players at local analysis helpers.
- Natas level 7 restores the intended page-source hint for the local file
  inclusion path.
- Natas level 8 now gives a valid hex decode/reverse/base64 pipeline using
  tools installed in the attacker image.
- Natas level 11 now uses the exact JSON plaintext for the XOR cookie and
  includes a complete offline forging helper.
- Krypton instructor writeups now use the deployed `/home/kryptonN`
  paths instead of nonexistent `/krypton/kryptonN` paths.
- Krypton levels 2 and 6 (`entrypoint.sh`) no longer draw their Caesar
  shift / LFSR keystream from `/dev/urandom` on every container start.
  A reboot, health-check-triggered recreate, or hung-container recovery
  regenerated fresh key material each time even though the per-team
  flag in `LEVEL_SECRETS` never changed, so `keyfile.dat`/`keystream.dat`
  and the encrypted `krypton3`/`final` files silently stopped matching
  whatever a player had already pulled off the box, breaking in-progress
  solves. Both are now derived deterministically from the stable
  per-team secret (SHA-256 counter mode), so they're stable across
  restarts and still unique per team.
- Bandit level 13's SSH keypair (the one used to log into bandit14) no
  longer gets regenerated on every reboot. It was `ssh-keygen`'d from
  `/dev/urandom` and guarded by an `os.path.exists()` check on the
  false assumption that a reboot restarts the same container without
  wiping its filesystem -- `cei-labs-engine`'s reboot is actually a
  Swarm task replacement with a fresh filesystem every time, so the
  guard never held in production and every reboot silently minted a
  new keypair, orphaning any `sshkey.private` a player had already
  downloaded. Confirmed via a real container recreate before and after
  the fix (identical key material after; a pre-recreate downloaded key
  still authenticated afterward once fixed). Derived deterministically
  from bandit13's own per-team secret instead (SHA-256 seed into
  `cryptography`'s Ed25519 key generation), same pattern as the Krypton
  fix below. Also corrected a matching but lower-severity comment on
  the levels-27-31 git-repo setup that made the same false assumption
  -- the actual flag values there were never affected since they're
  re-derived from `LEVEL_SECRETS` on every run regardless.
- Audited Natas for the same class of bug (any per-boot randomness not
  derived from `LEVEL_SECRETS`); found none -- every Natas secret
  already comes straight from the stable per-team blob.

### Deployment notes
- The Natas generator now references
  `ghcr.io/stoptalkingishh/cei-labs-wargames/natas-attacker:latest`.
  Publish that attacker image to GHCR before relying on the generated
  deployment manifests outside the local Docker test environment.

## Milestones before this file existed

- Bandit (35 levels), Krypton (8 levels), and Natas (16 levels) converted
  from pointing at OverTheWire's live infrastructure to fully
  self-hosted target images, deployed on demand by `cei-labs-engine`'s
  orchestrator.
- Per-team dynamic flags rolled out across every mechanism used by the
  56 non-tutorial/non-self-contained levels: flat files, byte-count-
  sensitive files, transforms, TCP/TLS daemons, SUID binaries, a
  randomized brute-force PIN, and all 5 git-history-hiding mechanisms —
  verified end-to-end against a live redeployed stack with two simulated
  teams.
- Security audit: fixed world-readable Natas htpasswd files (0600 now,
  were 0644 root-owned — exploitable via any level's intended RCE to read
  every other level's password hash) and four levels (Natas 6/8/11/14)
  that leaked their own next-level secret through their `?source`
  view-source feature.
- Staggered-game content (independent per-game starts/scoreboards for
  Bandit/Krypton/Natas): `game-stages.yml` + validator, merged to `main`.

Full detail lives in `docs/self-hosted-wargames-status.md` and
`docs/security-audit-status.md`.
