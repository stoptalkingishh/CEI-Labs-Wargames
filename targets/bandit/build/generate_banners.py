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

# Small, readable, title-themed ASCII art per level. Kept to the same scale
# (2-4 short lines) as the previous generic cat-face art; the last line of
# each entry is where render() appends the "CEI Labs Bandit N: Title" text,
# so keep last lines short to stay well under the 80-char safety limit.
ART = {
    0: ["   o", "  /|\\", "  / \\"],                       # first steps, on your feet
    1: ["- - - -", "   X", "- - - -"],                      # a dashed line, hopes broken
    2: ["[ ][ ][ ]", "[ ]   [ ]", "[ ][ ][ ]"],              # a grid with spaces missing
    3: [". . . . .", ". .(o). .", ". . . . ."],              # an eye hidden among dots
    4: [" o", "/|\\ [===]", "/ \\"],                         # a person reading a book
    5: ["    |", "   /|", " ~~~~~~~"],                       # a needle in a haystack
    6: ["|=|=|=|", "|=|=|=|  ,O__", "|=|=|=|  \\_|"],        # a rack under a magnifier
    7: [" ___________", "| w w w www |", "|___________|"],   # a page full of words
    8: [". . . . .", ".  *  . .", ". . . . ."],              # one star among many dots
    9: [" \\|/", "  o", " /|\\"],                            # a puppet with strings up top
    10: ["0101 1010", " -> base ->", "  16  8  2"],           # number bases
    11: [" [A] <-> [B]", " [C] <-> [D]"],                     # letters swapped
    12: [" [ [ [ ] ] ]", "  [ [ ] ]", "   [ ]"],              # nested boxes, doll in a doll
    13: [" .--.", "( () )====", " `--'"],                     # a key
    14: ["  -=[", "      \\__[ PORT ]"],                      # a plug meeting a port
    15: ["  .--.", " /    \\", "|--[]--|"],                   # a padlock
    16: [" .-''-.", "( .  * )", " `-..-'"],                   # a radar sweep
    17: ["[ A ]   [ B ]", "  |   !=   |", "  +---------+"],   # two files diffed
    18: ["  .--.", " ( () ) ---->", "  `--'"],                # a shell, arrow slipping past
    19: ["     _|^", "   _|", " _|"],                         # stairs climbing up
    20: ["  )))", " ))))", "   |"],                           # an antenna listening
    21: ["   _12_", "  9  |  3", "   `-6-'"],                 # a clock face
    22: ["  _12_   ,_,", " 9  | 3 (o.o)", "  `-6-'  ) ("],    # a clock with a bug nearby
    23: ["  _12_  |code", " 9  |3  |code", "  `-6-' |code"],  # a clock beside a script
    24: ["[1][2][3]", "[4][5][6] *?*", "[7][8][9]"],          # a numeric keypad
    25: ["  .--.", " ( )( )  o", "  `--'  /|\\"],             # a cracked shell, figure out
    26: ["+--//--+", "|  TUI  |", "+-------+"],               # a cracked text-mode window
    27: ["  o", "  |\\--> o", "  o"],                         # a commit cloned onward
    28: [" o---o---o---o", "  c1  c2  c3"],                   # commits strung on a line
    29: ["     o--o", "    /", " o-o--o--o"],                 # a branch splitting off
    30: ["  _____", " /     \\--o", " \\_____/  v1.0"],       # a tag on a commit
    31: ["  .-~~-.", " (      )", "  `-..-'", "    ^"],       # pushing up to the cloud
    32: ["  .--.", " ( () ) overridden", "  `--' -> new"],    # a shell, swapped for another
    33: [" +--+", " |  |->", " +--+"],                        # a door, and out you go
}

def render(level):
    if set(TITLES) != set(range(34)):
        raise ValueError("Bandit banner titles must cover levels 0 through 33")
    if set(ART) != set(range(34)):
        raise ValueError("Bandit banner art must cover levels 0 through 33")
    title = TITLES[level]
    art = ART[level]
    lines = list(art[:-1]) + [art[-1] + "  CEI Labs Bandit %d: %s" % (level, title)]
    lines.append("Logged in as bandit%d" % level)
    lines.append("Final level: submit your result; there is no next account." if level == 33 else "Submit this level, then use CTFd launch panel for bandit%d." % (level + 1))
    lines.extend(POLICY)
    if any(any(ord(ch) > 127 for ch in line) or len(line) > 80 for line in lines):
        raise ValueError("unsafe banner rendering")
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
