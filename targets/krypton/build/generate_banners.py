"""Build-time, ASCII-only Krypton banners. Output is data, never shell code."""
from pathlib import Path

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
    4: ["  C I P H E R", "  | | | | | |", "  ? ? ? ? ? ?  (key=6)"],       # a fixed-width Vigenere key grid
    5: ["  ...KEY...KEY...", "      ^-------^", "      gap -> key length"],  # Kasiski repeat-distance find
    6: ["  1 0 1 1 0 1 ->[XOR]", "        ^________|", "  (keystream repeats)"],  # LFSR feedback shift register
}


def render(level):
    if set(TITLES) != set(range(1, 7)):
        raise ValueError("Krypton coverage")
    if set(ART) != set(range(1, 7)):
        raise ValueError("Krypton banner art must cover levels 1 through 6")
    title = TITLES[level]
    art = ART[level]
    lines = list(art[:-1]) + [art[-1] + "  CEI Labs Krypton %d: %s" % (level, title)]
    lines.append("Logged in as krypton%d" % level)
    lines.append(
        "Final level: submit your result; there is no next account."
        if level == 6
        else "Submit this level, then use CTFd launch panel for krypton%d." % (level + 1)
    )
    lines.extend(POLICY)
    if any(any(ord(c) > 127 for c in line) or len(line) > 80 for line in lines):
        raise ValueError("unsafe banner")
    return "\n".join(lines) + "\n"


def generate(root):
    root = Path(root)
    for level in range(1, 7):
        (root / ("krypton%d" % level)).write_text(render(level), encoding="ascii")


if __name__ == "__main__":
    import sys
    generate(sys.argv[1])
