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

# Small, readable, title-themed ASCII art per level -- same 2-4 short line
# scale as the previous shared lock-icon art. The last line of each entry
# is where render() appends the "CEI Labs Krypton N: Title" text, so keep
# last lines short to stay well under the 80-char safety limit.
ART = {
    1: ["  A B C D ...", "  | | | |  (shift 13)", "  N O P Q ..."],       # letter->letter rotation map
    2: ["   .--?--.", "  <  shift  >>--", "   `--?--'"],                  # a dial with the shift unknown
    3: ["  #", "  # #   #", "  # # # # #", "  E T A O I N ."],            # a letter-frequency histogram
    4: ["  C I P H E R", "  | | | | | |", "  ? ? ? ? ? ?  (key=6)"],      # a fixed-width Vigenere key grid
    5: ["  ...KEY...KEY...", "      ^-------^", "      gap -> key length"],  # Kasiski repeat-distance find
    6: ["  1 0 1 1 0 1 ->[XOR]", "        ^________|", "  (keystream repeats)"],  # LFSR feedback register
}

# Progressive cool-to-deep palette, basic 8-color SGR only. Deliberately
# NOT the warm (red/orange/yellow) ramp Bandit uses and NOT plain green
# (the generic "hacker terminal" default Natas would reach for first) --
# Krypton starts icy blue (a fresh, still-legible cipher) and cools
# further into cyan before crossing into magenta/violet by the final
# LFSR level, reading as "the cipher gets colder and stranger" the
# deeper you go, distinct from either sibling track at a glance.
_RESET = "\x1b[0m"
COLOR = {
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
    if set(TITLES) != set(range(1, 7)):
        raise ValueError("Krypton coverage")
    if set(ART) != set(range(1, 7)):
        raise ValueError("Krypton banner art must cover levels 1 through 6")
    if set(COLOR) != set(range(1, 7)):
        raise ValueError("Krypton banner color must cover levels 1 through 6")
    title = TITLES[level]
    art = ART[level]
    color = COLOR[level]
    # Only the art block is colorized -- title/login/policy lines stay
    # plain so the informational content never depends on color at all.
    colored_art = [color + line + _RESET for line in art[:-1]]
    colored_art.append(color + art[-1] + _RESET + "  CEI Labs Krypton %d: %s" % (level, title))
    lines = colored_art
    lines.append("Logged in as krypton%d" % level)
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
    for level in range(1, 7):
        (root / ("krypton%d" % level)).write_text(render(level), encoding="ascii")


if __name__ == "__main__":
    import sys
    generate(sys.argv[1])
