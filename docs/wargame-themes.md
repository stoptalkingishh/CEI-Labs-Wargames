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
You are creating a small ASCII art image for a CTF training login banner.

Output constraints: 5-9 lines, each line <=80 characters, 7-bit ASCII only
(no Unicode/box-drawing characters), no profanity, no real-world hate
symbols, no copyrighted characters or logos.

Overall track theme: {TRACK_THEME}
This piece is for the question titled: "{LEVEL_TITLE}"

Draw only from the overall track theme's imagery/setting and the mood of
the title itself. Do NOT depict, reference, or hint at the specific
command, tool, technique, or vulnerability used to solve this question --
a player must not be able to learn anything about HOW to solve it from
the art. Output only the ASCII art, nothing else.
```
