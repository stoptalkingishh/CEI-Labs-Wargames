"""Build-time, ASCII-only Bandit banners. Output is data, never shell code."""
from pathlib import Path
import re

# Reviewed display titles; kept separate from runtime flags/password material.
TITLES = {
0:"The First Step",1:"Dashed Hopes",2:"Spaces in Places",3:"Hidden in Plain Sight",4:"Human Readable",5:"The Needle",6:"Server Search",7:"The Millionth Word",8:"The Only One",9:"Strings Attached",10:"Base Operations",11:"Substitution",12:"Matryoshka",13:"Private Keys",14:"Port Submission",15:"SSL Encryption",16:"SSL Port Scan",17:"File Comparisons",18:"Shell Bypass",19:"SUID Escalation",20:"Port Listener Connection",21:"Cron Jobs",22:"Cron Debugging",23:"Cron Scripting",24:"PIN Brute Force",25:"Shell Breakout",26:"Text UI Breakout",27:"Git Clone",28:"Git Commits",29:"Git Branches",30:"Git Tags",31:"Git Push",32:"Shell Overrides",33:"Final Escape"}
POLICY = (
    "Authorized CEI Labs training only. Misuse of this system is prohibited.",
    "Do not use AI or external tools/services to cheat or obtain answers.",
    "Stay within your assigned challenge environment only.",
)

# Small, title-themed ASCII art per level, built around Bandit's adopted
# track theme (see docs/wargame-themes.md): you're an outlaw breaking into
# a guarded compound, moving room to room, picking locks, slipping past
# guards, stealing what's hidden deeper inside as you go -- ending in an
# escape at the final level. Each piece draws ONLY on that theme plus the
# level's own (already player-visible) title -- deliberately NOT on the
# level's actual technique/command/vulnerability, so the art itself never
# hints at how to solve anything. The last line of each entry is where
# render() appends the "CEI Labs Bandit N: Title" text, so keep last
# lines short to stay well under the 80-char safety limit.
ART = {
    0: ["   .---.", "   | o | -->", "   '---'"],                    # stepping through the outer gate
    1: ["   .-------.", "   |   X   |", "   '-------'"],            # a dead end, hopes dashed
    2: ["  |  |     |  |", "  |  | o   |  |", "  |  |     |  |"],   # slipping through a narrow gap
    3: ["  [#][#][#]", "  [#][o][#]", "  [#][#][#]"],               # blending among the crates
    4: ["   ,-------.", "   | note   |", "   |  o     |", "   `-------'"],  # reading by torchlight
    5: ["  ~~~~~~~~~~", "  ~~~ | ~~~~", "  ~~~~~~~~~~"],            # searching the haystack
    6: ["  [=][=][=]", "  [=][=][=]  o", "  [=][=][=]"],            # combing a row of cabinets
    7: ["  wwwwwwwwwwwww", "  ww[W]wwwwwwww", "  wwwwwwwwwwwww"],   # one word among countless
    8: ["  ooooooooo", "  oo[*]oooo", "  ooooooooo"],               # a single glint among many
    9: ["    \\|/", "     o", "    /|\\"],                          # tangled up, working free
    10: ["   ####", "   #  # o", "   ####"],                        # a carved tablet, studied closely
    11: ["  [A]<->[B]", "      o", "   swapped"],                   # switching one thing for another
    12: ["  [ [ [ o ] ] ]", "   [ [ ] ]", "    [ ]"],                # a chest inside a chest
    13: ["   .--.", "  ( () )==o", "   `--'"],                      # an ornate key, held up
    14: ["   o -->", "   [ ]  <-hatch"],                            # a note passed through a hatch
    15: ["    .--.", "   /    \\", "  |--[]--| o"],                 # a sealed vault door
    16: ["  [ ][ ][ ]", "   o  scan-->"],                           # sweeping past a row of doors
    17: ["   [A]  [B]", "     o  <->"],                             # weighing two things side by side
    18: ["  |||||", "  ||| o -->", "  |||||"],                      # slipping past the bars
    19: ["    ^", "   /|", "  o |"],                                # climbing to a higher ledge
    20: ["  )))", "  ))) o", "   |"],                                # a whisper through the wall
    21: ["   _12_", "  9  o  3", "   `-6-'"],                       # watching the bell tower
    22: ["   _12_   ,_,", "  9  o 3 (o.o)", "   `-6-'"],            # the bell tower, something's off
    23: ["   _12_  |~~~", "  9  o 3 |~~~", "   `-6-' |~~~"],        # leaving a note on the gears
    24: ["  [1][2][3]", "  [4][5][6] o", "  [7][8][9]"],            # working through a locked dial
    25: ["  |||||", "  ||X|| o-->", "  |||||"],                     # breaking through the cell door
    26: ["  +--//--+", "  | o  //|", "  +-------+"],                # out through a cracked window
    27: ["   o", "   |\\--> o", "   o"],                            # a path copied and followed onward
    28: ["  o---o---o", "   stack  o"],                             # stones stacked one on the last
    29: ["      o--o", "     /", "  o-o--o--o"],                    # the path splits in two
    30: ["   _____", "  /     \\--o", "  \\_____/"],                # a marker tied to a stone
    31: ["   .-~~-.", "  (  o   )", "   `-..-'", "     ^"],         # sending a loaded cart onward
    32: ["  [cloak A]", "      o", "  [cloak B]"],                  # one disguise traded for another
    33: ["  +--+", "  |o |->", "  +--+"],                           # out through the wall, free
}

# --- Progressive color, layered on top of the art above -------------------
#
# Color is a *supplement*, never load-bearing: it only wraps the ASCII art
# lines, using the most widely supported basic SGR 8-color codes
# (ESC[3Xm ... ESC[0m). Every plain-text line (title/account/reconnect/
# POLICY) stays completely uncolored, and the art itself is byte-for-byte
# identical whether or not the terminal honors ANSI escapes -- strip the
# escapes and every level is still fully readable and still distinct from
# every other level, exactly as before this file gained color support.
#
# The palette is a warm/earthy 6-stop ramp (sand -> gold -> rust -> ember ->
# dusk -> maroon) that shifts gradually as the participant goes deeper into
# the track, giving Bandit its own identifiable, desert/canyon-toned
# progression distinct from the other tracks' palettes.
ESC = "\x1b["
RESET = ESC + "0m"
_PALETTE_TIERS = (
    (33, False),  # sand    - level 0 area
    (33, True),   # gold
    (31, False),  # rust
    (31, True),   # ember
    (35, False),  # dusk
    (35, True),   # maroon  - level 33 area
)

def palette_for(level):
    """Return the (SGR color, bold) pair for a level's tier on the ramp."""
    idx = min(level * len(_PALETTE_TIERS) // 34, len(_PALETTE_TIERS) - 1)
    return _PALETTE_TIERS[idx]

def colorize(text, color, bold):
    if not text:
        return text
    prefix = ESC + ("1;%dm" % color if bold else "%dm" % color)
    return prefix + text + RESET

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
_ANSI_OPEN_RE = re.compile(r"\x1b\[(?:1;)?3[0-7]m")

def _visible(line):
    """Line content a viewer actually sees once ANSI codes are stripped."""
    return _ANSI_RE.sub("", line)

def _ansi_balanced(line):
    """Every color-open code on this line is matched by a reset, so no
    color can bleed past the line into whatever the terminal prints next."""
    return len(_ANSI_OPEN_RE.findall(line)) == line.count(RESET)

def render(level):
    if set(TITLES) != set(range(34)):
        raise ValueError("Bandit banner titles must cover levels 0 through 33")
    if set(ART) != set(range(34)):
        raise ValueError("Bandit banner art must cover levels 0 through 33")
    title = TITLES[level]
    art = ART[level]
    color, bold = palette_for(level)
    colored_art = [colorize(line, color, bold) for line in art[:-1]]
    colored_last = colorize(art[-1], color, bold) + "  CEI Labs Bandit %d: %s" % (level, title)
    lines = colored_art + [colored_last]
    lines.append("Logged in as bandit%d" % level)
    lines.append("Final level: submit your result; there is no next account." if level == 33 else "Submit this level, then use CTFd launch panel for bandit%d." % (level + 1))
    lines.extend(POLICY)
    if any(any(ord(ch) > 127 for ch in _visible(line)) or len(_visible(line)) > 80 for line in lines):
        raise ValueError("unsafe banner rendering")
    if any(not _ansi_balanced(line) for line in lines):
        raise ValueError("unsafe banner rendering: unbalanced ANSI codes")
    return "\n".join(lines) + "\n"

def generate(root):
    root = Path(root)
    for level in range(34):
        text = render(level)
        if re.search(r"BANDITPLACEHOLDER|password|flag\{", text, re.I):
            raise ValueError("banner secret scan failed")
        (root / ("bandit%d" % level)).write_text(text, encoding="ascii")

if __name__ == "__main__":
    import sys
    generate(sys.argv[1])
