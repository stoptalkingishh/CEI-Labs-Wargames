# Wargame track themes

Each self-hosted track (Bandit, Krypton, Natas) has an adopted narrative
theme used only for visual identity -- per-level login banner art (and,
for Natas, the attacker workstation's desktop wallpaper). None of this is
used for hints: see "Storyboard mechanic" below for how that's enforced
structurally, not just by convention. The AI Copilot Setup track is
explicitly excluded -- it has no theme and none of this applies to it.

The narrative each track's storyboard follows -- plus a per-level
generation prompt grounded in it -- lives in
[`wargame-story.md`](wargame-story.md).

## Storyboard mechanic

Earlier iterations tried to hand-invent a small standalone picture for
every level, tied to that level's title and (briefly) its technique. In
practice this kept producing noise -- tiny arrangements of brackets and
arrows that only made sense if you already knew what they were supposed
to mean. That approach is retired.

Instead, every banner in every track is one frame of a single continuous
journey through the whole track, built from two parts:

1. **An establishing-shot frame.** Fixed, track-wide, byte-identical
   across every level in that track on purpose (Bandit: a starlit
   compound wall; Krypton: a starfield with an incoming wave-train;
   Natas: none needed, the shaft below carries the whole picture). It's
   the recurring backdrop, not the part that changes -- taller banners
   are fine since SSH clients scroll and modern terminals aren't
   height-constrained the way the 80-column line width is.
2. **A progress strip**, using the same three-symbol grammar in every
   track: `x`/`-` = ground already covered, `o` = exactly where this
   level is right now, `.` = ground still ahead, unreached. Krypton's is
   a horizontal transmission distance from the receiving dish; Natas's
   is a vertical descent shaft (each level gets its own row, so adjacent
   levels are already visually far apart). The strip is generated
   programmatically from the level number, not hand-authored -- so
   distinctness across all 56 banners is structurally guaranteed, and
   reading the whole set in order shows one continuous story (a signal
   traveling further into space; a steady descent into the underworld).

   Bandit needed one more step: squeezing all 34 levels into a single
   38-character strip meant adjacent levels differed by only one
   character shifting one position -- imperceptible at a glance, since
   that really is almost the same amount of progress (confirmed the hard
   way: bandit16/17/18 looked identical side by side). Fixed by chunking
   the compound into 8 chapters, each with its own bracket style, so
   moving between chapters is an obvious shape change, plus a smaller
   "position within this room" strip so even two levels sharing a
   chapter (e.g. bandit17/18) are still visibly distinct from each
   other, not just from levels in other chapters.

   Those 8 chapter boundaries are hand-set in `_CHAPTER_BOUNDS` to
   follow the track's own content clusters, *not* an even numeric split
   of 34. An even split cut through related runs -- it put Cron Jobs in
   one chapter and Cron Debugging/Scripting in the next, and split the
   git levels across two -- so a chapter change landed mid-material.
   The explicit bounds keep each run whole; a unit test guards that they
   stay contiguous, non-empty, and cover every level exactly once.

Because the strip only ever encodes "how far along you are," it cannot
leak a hint about any specific technique -- there is nothing per-level to
invent, and therefore nothing per-level that could give something away.

**Provenance note:** none of these themes are official OverTheWire canon.
OverTheWire's own site and GitHub repo (`OverTheWireOrg/OverTheWire-website`)
describe Bandit, Krypton, and Natas with zero narrative/lore content --
verified directly against the live pages and the repo's
`wargames/{bandit,krypton,natas}/index.md` files, which contain only a
one- or two-sentence technical description each, no naming rationale of
any kind. These themes are CEI Labs' own adopted creative interpretation,
built on real wordplay/etymology where it exists (Natas/Satan reversal;
Krypton's Greek "kryptos" root) plus originated narrative framing where it
doesn't. Treat them as our design decision, not a documented upstream fact.

## Bandit -- The Outlaw

You are an outlaw breaking into a guarded compound: moving room to room,
picking locks, slipping past guards, and stealing what's hidden deeper
inside as you go. Bandit's corridor strip follows this figure's progress
from the outer wall (level 0), room by room, to an escape at the final
level (33).

Palette: warm/earthy 6-stop ramp (sand -> gold -> rust -> ember -> dusk ->
maroon), already implemented in `targets/bandit/build/generate_banners.py`.

## Krypton -- The Hidden Signal

Krypton is a distant, hidden world (Greek *kryptos* = "hidden"; also
Superman's home planet in fiction) transmitting encoded signals across
space. Krypton's transmission strip follows a signal traveling further
from the receiving dish with each level, growing stranger and more
alien-seeming the deeper into space it goes.

Palette: cool blue -> cyan -> magenta/violet progression, already
implemented in `targets/krypton/build/generate_banners.py`.

## Natas -- The Inverted Underworld

"Natas" is "Satan" spelled backwards. Natas is a mirrored, upside-down
digital underworld where the ordinary logic of the web gets inverted and
manipulated. This is already realized in the attacker workstation's
desktop wallpaper ([`cei-labs-engine`'s `operator/kali-novnc/wallpaper/
natas-wallpaper.svg`](https://github.com/stoptalkingishh/cei-labs-engine/blob/main/operator/kali-novnc/wallpaper/natas-wallpaper.svg):
the NATAS wordmark reflecting into SATAN below a waterline, cool navy-teal
palette, scattered inverted/rotated HTTP-header and markup fragments). Engine
owns that asset; its appearance in a live Natas workstation is an event-time
check, not a Wargames build guarantee. The per-level login banner's depth shaft extends
the same descent -- surface to depths -- reinforced by the page's own
existing cool-to-hot color progression (see "Color" below).

## Color

Bandit and Krypton color their art with ANSI SGR escape codes (basic
8-color only), each with its own progressive palette (see those tracks'
generators). Natas colors its art via CSS `<span style="color:...">`,
deliberately reusing the *exact same* per-level hue that
`build/generate_themes.py` already uses for that level's page
background/headings (a continuous cool-blue -> hot-magenta sweep from
natas0's passive recon to natas14's full exploitation) -- rather than
inventing a second, redundant palette for the same page.
