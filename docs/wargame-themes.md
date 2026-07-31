# Wargame track themes

Each self-hosted track (Bandit, Krypton, Natas) has an adopted narrative
theme used only for visual identity -- per-level login banner ASCII art
(and, for Natas, the attacker workstation's desktop wallpaper). None of
this is used for hints: the art draws only on the *overall track theme*
and the *level's public title* (already shown in the banner regardless),
never on a level's actual technique, command, or vulnerability class.
The AI Copilot Setup track is explicitly excluded -- it has no theme and
none of this applies to it.

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
inside as you go. Bandit's per-level art follows this figure's progress
from the outer wall (level 0) through increasingly deep rooms of the
compound to an escape at the final level (33).

Palette: warm/earthy 6-stop ramp (sand -> gold -> rust -> ember -> dusk ->
maroon), already implemented in `targets/bandit/build/generate_banners.py`.

## Krypton -- The Hidden Signal

Krypton is a distant, hidden world (Greek *kryptos* = "hidden"; also
Superman's home planet in fiction) transmitting encoded signals across
space. Each level is a signal that must be decoded, growing stranger and
more alien-seeming the deeper you go.

Palette: cool blue -> cyan -> magenta/violet progression, already
implemented in `targets/krypton/build/generate_banners.py`.

## Natas -- The Inverted Underworld

"Natas" is "Satan" spelled backwards. Natas is a mirrored, upside-down
digital underworld where the ordinary logic of the web gets inverted and
manipulated. This is already realized in the attacker workstation's
desktop wallpaper (`cei-labs-engine`'s `operator/kali-novnc/wallpaper/
natas-wallpaper.svg`: the NATAS wordmark reflecting into SATAN below a
waterline, cool navy-teal palette, scattered inverted/rotated HTTP-header
and markup fragments). The per-level login banner art extends the same
mirrored/inverted visual language to each level's title.

Natas's per-level banner previously had no ASCII art at all (plain
title/policy text only) -- this is the first pass adding it.

## The generation prompt

Every piece of art in all three tracks is built from one reusable prompt,
filled in with the track's theme (above) and the level's title only:

```
You are creating a small ASCII/Unicode art image for a CTF training login
banner.

Output constraints: each line <=80 single-width characters. Unicode is
allowed -- box-drawing, block-element, and dingbat glyphs -- but restrict
to single-width BMP characters only (no emoji, no CJK-width characters),
so one character always equals one terminal column and the 80-column
width check stays meaningful. No profanity, no real-world hate symbols,
no copyrighted characters or logos. There is no hard line-count cap --
SSH clients scroll and modern (1080p+) terminals aren't height-constrained
the way the 80-column line width is, so banners can run taller than a
single screenful. Each track additionally prepends/wraps a fixed,
track-wide frame around every level's per-title core art purely to add
height (Bandit: a starlit wall skyline; Krypton: a starfield with an
incoming wave-train; Natas: a mirrored reflection below a waterline,
fitting its own theme) -- these frames carry no hint content, only
overall-theme imagery.

Note on compatibility: unlike 7-bit ASCII (which is universal), Unicode
rendering depends on the connecting player's own terminal/client
supporting UTF-8. This is an accepted tradeoff, not an oversight.

Overall track theme: {TRACK_THEME}
This piece is for the question titled: "{LEVEL_TITLE}"

Draw from the overall track theme's imagery/setting, the mood of the
title, and the general *nature* of the question (e.g. a rotation cipher,
a repeated-pattern search, a filter being bypassed, a record being
exposed) -- visual depictions of what kind of thing is going on are fine.
What is NOT fine: any actual instructional text -- no words, phrases, or
labels that explain, name, or spell out the specific command, tool,
payload, or step needed to solve it. A player may recognize "oh, this is
about X kind of thing" from the shapes, but must never be able to read an
answer or a how-to off the banner. Output only the art, nothing else.
```

## Color

Bandit and Krypton color their art with ANSI SGR escape codes (basic
8-color only), each with its own progressive palette (see those tracks'
generators). Natas colors its art via CSS `<span style="color:...">`,
deliberately reusing the *exact same* per-level hue that
`build/generate_themes.py` already uses for that level's page
background/headings (a continuous cool-blue -> hot-magenta sweep from
natas0's passive recon to natas14's full exploitation) -- rather than
inventing a second, redundant palette for the same page.
