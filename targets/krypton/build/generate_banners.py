"""Build-time, ASCII-only Krypton banners. Output is data, never shell code.

Color is a supplement only, never load-bearing: every banner is written so
the plain-text art/title/policy content is fully readable with zero ANSI
support (a client that doesn't interpret escape codes just shows a few
extra control-character bytes inline; no information is color-only). Only
the widely-supported basic SGR 8-color codes are used (\\x1b[3Xm / bold
\\x1b[3X;1m, reset \\x1b[0m) -- no 256-color/truecolor, no background
fills, nothing terminal-specific.
"""
from pathlib import Path
import re

TITLES = {
    0: "Base64 Decoding",
    1: "ROT13 Substitution Cipher",
    2: "Caesar Cipher (Unknown Shift)",
    3: "Frequency Analysis",
    4: "Vigenere Cipher (Known Key Length)",
    5: "Vigenere Cipher (Kasiski Test)",
    6: "Stream Cipher / LFSR",
}
POLICY = (
    "Authorized CEI Labs training only. Misuse of this system is prohibited.",
    "Do not use AI or external tools/services to cheat or obtain answers.",
    "Stay within your assigned challenge environment only.",
)

# Small, title-themed ASCII art per level, built around Krypton's adopted
# track theme (see docs/wargame-themes.md): a distant, hidden world
# transmitting encoded signals across space, growing stranger and more
# alien the deeper you go. Each piece draws on that theme, the level's
# own (already player-visible) title, and the general shape of what kind
# of cipher/technique is involved (a dial rotating, a repeating pattern,
# a feedback loop) -- but never any actual instructional text/labels
# naming the specific technique, key, or steps to solve it; a player may
# recognize "this is some kind of rotation/repetition/feedback thing"
# from the shapes, never read an answer off the banner. The last line of
# each entry is where render() appends the "CEI Labs Krypton N: Title"
# text, so keep last lines short to stay well under the 80-char limit.
#
# A fixed, track-wide frame (a starfield with an incoming wave-train) is
# prepended to every level's core art below -- taller banners are fine
# since SSH clients scroll, and 1080p terminals aren't width/height
# constrained the way the 80-col line limit is. The frame is only added
# at the TOP, never the bottom, so it never risks pushing the title line
# (appended to the core art's last line) past 80 characters.
_FRAME_TOP = (
    "     *        .          *          .        *",
    "  .     *          .          *          .",
    "  - - - - - - - - - - - - - - - - - - - - - -",
)

_CORE = {
    0: ["  [ %#&@ ]  -->  [ ==== ]", "         << signal"],             # scrambled block resolving -- an encode/decode swap
    1: ["   \\ | /", "   -- O --  spinning", "   / | \\"],               # a dial turning under the stars -- a rotation
    2: ["   \\ | /", "   -- ? --  half-turned", "   / | \\"],            # the same dial, shadowed, offset unknown -- rotation by an unknown amount
    3: ["   |     ##", "   |  #  ## #", "   | ## ## ##", "   +-----------  spectrum"],  # bars of uneven height -- a frequency spectrum
    4: ["  [AA][AA][AA][AA]", "  (( (( (( ))", "   ((  core  ))", "  (( (( (( ))"],  # a short repeating tile -- a fixed-length repeating pattern
    5: ["  [xxx]......[xxx]", "   |<-- gap -->|", "  ((( deeper ((((", "  (( (((( (("],  # two matching marks with a measured gap -- a repeat-distance search
    6: ["  [1][0][1][1]<-.", "   ^____________|", "   *", "    \\_/\\_/\\_", "   endless loop"],  # a register chain feeding back into itself
}

ART = {level: list(_FRAME_TOP) + list(core) for level, core in _CORE.items()}

# Progressive cool-to-deep palette, basic 8-color SGR only. Deliberately
# NOT the warm (red/orange/yellow) ramp Bandit uses and NOT plain green
# (the generic "hacker terminal" default Natas would reach for first) --
# Krypton starts icy blue (a fresh, still-legible cipher) and cools
# further into cyan before crossing into magenta/violet by the final
# LFSR level, reading as "the cipher gets colder and stranger" the
# deeper you go, distinct from either sibling track at a glance. Level 0
# sits one step before the ramp even starts -- plain white, since Base64
# isn't really a cipher at all (no key/shift/secret), just an encoding.
_RESET = "\x1b[0m"
COLOR = {
    0: "\x1b[37m",     # plain white
    1: "\x1b[34m",     # blue
    2: "\x1b[36m",     # cyan
    3: "\x1b[36;1m",   # bright cyan
    4: "\x1b[34;1m",   # bright blue
    5: "\x1b[35m",     # magenta
    6: "\x1b[35;1m",   # bright magenta
}

_ANSI_RE = re.compile("\x1b\\[[0-9;]*m")


def _visible_len(line):
    return len(_ANSI_RE.sub("", line))


def render(level):
    if set(TITLES) != set(range(0, 7)):
        raise ValueError("Krypton coverage")
    if set(ART) != set(range(0, 7)):
        raise ValueError("Krypton banner art must cover levels 0 through 6")
    if set(COLOR) != set(range(0, 7)):
        raise ValueError("Krypton banner color must cover levels 0 through 6")
    title = TITLES[level]
    art = ART[level]
    color = COLOR[level]
    # Only the art block is colorized -- title/login/policy lines stay
    # plain so the informational content never depends on color at all.
    colored_art = [color + line + _RESET for line in art[:-1]]
    colored_art.append(color + art[-1] + _RESET + "  CEI Labs Krypton %d: %s" % (level, title))
    lines = colored_art
    lines.append("Logged in as krypton%d" % level)
    lines.append("Player tools: krypton-tools --help")
    lines.append(
        "Final level: submit your result; there is no next account."
        if level == 6
        else "Submit this level, then use CTFd launch panel for krypton%d." % (level + 1)
    )
    lines.extend(POLICY)
    if any(any(ord(c) > 127 for c in line) or _visible_len(line) > 80 for line in lines):
        raise ValueError("unsafe banner")
    return "\n".join(lines) + "\n"


def generate(root):
    root = Path(root)
    for level in range(0, 7):
        (root / ("krypton%d" % level)).write_text(render(level), encoding="ascii")


if __name__ == "__main__":
    import sys
    generate(sys.argv[1])
