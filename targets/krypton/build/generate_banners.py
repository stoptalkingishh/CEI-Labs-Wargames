"""Build-time Krypton banners. Output is data, never shell code.

Unicode (box-drawing, block-element, and dingbat glyphs) is allowed, but
restricted to single-width BMP characters only -- no emoji, no CJK-width
characters -- so one Python character always equals one terminal column
and the 80-column width check below stays meaningful. Rendering then
depends on the connecting client's terminal supporting UTF-8, unlike
plain ASCII which is universal.

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

# Storyboard, not standalone scenes: rather than each level inventing its
# own isolated picture (which kept reading as noise -- see PR history),
# every banner is one frame of a single continuous signal traveling
# further from the receiving dish. A fixed "establishing shot" frame (a
# starfield with an incoming wave-train) tops every banner, identical
# across the whole track on purpose -- it's the recurring backdrop, not
# the part that changes. Underneath it, a transmission strip shows how
# far the signal has traveled: '-' = distance already crossed, 'o' = the
# signal's current position (this level), '.' = distance still ahead,
# unreached. The strip's shape is what makes each banner genuinely
# distinct -- structurally guaranteed, not hand-invented per level -- and
# reading the whole set in order shows the signal traveling steadily
# deeper into unknown space from level 0 to level 6. This also means no
# level's art can ever leak a hint: it only encodes "how far along you
# are," nothing about any specific cipher/technique.
_FRAME_TOP = (
    "     ★        .          ☆          .        ★",
    "  .     ★          .          ☆          .",
    "  ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈",
)

def _transmission(level, total_levels=7, width=40):
    pos = round(level * (width - 1) / (total_levels - 1))
    return "  [" + "".join("-" if i < pos else ("o" if i == pos else ".") for i in range(width)) + "]"

# The transmission strip is deliberately NOT the art's last line --
# render() appends the title to the last line, and the strip (44 chars)
# plus the longest title would exceed 80 columns. This short trailing
# line carries the title instead, and doubles as "the signal continues".
_TAIL = "  ~>"

ART = {level: list(_FRAME_TOP) + [_transmission(level), _TAIL] for level in range(7)}

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


def _has_unsafe_chars(text):
    """Unicode is allowed, but control characters (C0/C1, DEL) are not --
    those could inject terminal escape sequences of their own outside the
    ANSI SGR codes this module already controls."""
    return any(ord(c) < 0x20 or 0x7F <= ord(c) <= 0x9F for c in text)


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
    if any(_has_unsafe_chars(_ANSI_RE.sub("", line)) or _visible_len(line) > 80 for line in lines):
        raise ValueError("unsafe banner")
    return "\n".join(lines) + "\n"


def generate(root):
    root = Path(root)
    for level in range(0, 7):
        (root / ("krypton%d" % level)).write_text(render(level), encoding="utf-8")


if __name__ == "__main__":
    import sys
    generate(sys.argv[1])
