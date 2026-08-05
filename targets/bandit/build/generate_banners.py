"""Build-time Bandit banners. Output is data, never shell code.

Unicode (box-drawing, block-element, and dingbat glyphs) is allowed, but
restricted to single-width BMP characters only -- no emoji, no CJK-width
characters -- so one Python character always equals one terminal column
and the existing 80-column width check stays meaningful. Banners are
streamed to the client verbatim via `cat` (see the Dockerfile's
/etc/profile.d hook), so whatever bytes are written here reach the
player's terminal unmodified; rendering then depends on THEIR client
supporting UTF-8, unlike plain ASCII which is universal."""
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

# Storyboard, not standalone scenes: rather than each level inventing its
# own isolated picture (which kept reading as noise -- see PR history),
# every banner is one frame of a single continuous journey through the
# compound. A fixed "establishing shot" frame (starlit wall) tops every
# banner, identical across the whole track on purpose -- it's the
# recurring backdrop, not the part that changes. This also means no
# level's art can ever leak a hint: nothing below is hand-invented per
# level, it only ever encodes "how far along you are."
#
# A single 34-cell strip (one cell per level) was tried first, but
# adjacent levels then differ by only one character shifting one
# position -- imperceptible at a glance, since that's genuinely almost
# the same amount of progress. Fixed by chunking the compound into 6
# visibly distinct chapters (each with its own bracket style, so
# passing between chapters is an obvious shape change), plus a smaller
# strip showing exact position *within* the current chapter -- so even
# two levels in the same chapter (e.g. bandit17/18) are still visibly
# different from each other, not just from levels in other chapters.
_FRAME_TOP = (
    "   ✦      .        ✧         .       ✦",
    "  █  █  █  █  █  █  █  █  █  █  █  █  █",
    "  ████████████████████████████████████",
)

_CHAPTER_CORNERS = (".-.", "+-+", "/-\\", "#-#", "~-~", ":-:", "*-*", ">-<")

# Chapter boundaries follow the track's own content clusters, NOT an even
# numeric split of 34. An even split cut straight through related runs --
# it put Cron Jobs in one chapter and Cron Debugging/Scripting in the
# next, and split the git levels across two chapters -- so a chapter
# change landed in the middle of the same material. These bounds are
# explicit so a boundary always falls where the material actually
# changes. See docs/wargame-story.md for the narrative each maps to.
_CHAPTER_BOUNDS = (
    (0, 5),    # Over the Wall     - first steps inside
    (5, 11),   # The Storeyard     - searching for anything useful
    (11, 17),  # The Inner Halls   - keys, hatches, doors
    (17, 21),  # The Guardroom     - borrowing authority
    (21, 24),  # The Bell Tower    - everything on a schedule
    (24, 27),  # The Locked Wing   - rooms built to hold you
    (27, 32),  # The Archive       - the record room and its history
    (32, 34),  # The Escape        - out through the far wall
)

def _chapter_bounds(total=34, chapters=len(_CHAPTER_CORNERS)):
    if _CHAPTER_BOUNDS[-1][1] != total or len(_CHAPTER_BOUNDS) != chapters:
        raise ValueError("chapter bounds must cover all %d levels in %d chapters" % (total, chapters))
    return list(_CHAPTER_BOUNDS)

def _chapter_index(level, bounds):
    """The chapter whose (start, end) actually contains this level --
    derived from the same bounds used to draw the chapter row, rather
    than a separate formula, so the two can never disagree at an edge."""
    for idx, (start, end) in enumerate(bounds):
        if start <= level < end:
            return idx
    return len(bounds) - 1

def _chapter_rows(level, total=34):
    bounds = _chapter_bounds(total)
    idx = _chapter_index(level, bounds)
    start, end = bounds[idx]
    top, mid, bot = [], [], []
    for c, (left, dash, right) in enumerate(_CHAPTER_CORNERS):
        if c < idx:
            fill = "XXXX"
        elif c == idx:
            fill = ">OO<"
        else:
            fill = "    "
        top.append(left + dash * 4 + right)
        mid.append("|" + fill + "|")
        bot.append(left + dash * 4 + right)
    within = "".join("x" if i < level - start else ("o" if i == level - start else ".") for i in range(end - start))
    return [
        "  " + " ".join(top),
        "  " + " ".join(mid),
        "  " + " ".join(bot),
        "  in this room: [" + within + "]",
    ]

# render() appends the title to the art's last line; the trailing line
# below stays short so that never risks exceeding 80 columns.
_TAIL = "  -->"

ART = {level: list(_FRAME_TOP) + _chapter_rows(level) + [_TAIL] for level in range(34)}

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

def _has_unsafe_chars(text):
    """Unicode is allowed, but control characters (C0/C1, DEL) are not --
    those could inject terminal escape sequences of their own outside the
    ANSI SGR codes this module already controls."""
    return any(ord(c) < 0x20 or 0x7F <= ord(c) <= 0x9F for c in text)

def _ansi_balanced(line):
    """Every color-open code on this line is matched by a reset, so no
    color can bleed past the line into whatever the terminal prints next."""
    return len(_ANSI_OPEN_RE.findall(line)) == line.count(RESET)

# --- Banner presentation: box frame, wordmark, info block ------------------
#
# The storyboard ART above is wrapped in a box-drawing frame with a large
# BANDIT wordmark on top and an info block under a thin divider. All frame,
# wordmark, and info lines are derived from the level number alone -- no
# per-level hand-invented content -- and color stays supplementary: strip
# the SGR codes and every line is still fully readable.
#
# The wordmark uses only single-width BMP block/box glyphs, six rows tall,
# 47 columns wide, so it fits the 74-column content area with room to spare.
_WORDMARK = (
    "██████╗  █████╗ ███╗   ██╗██████╗ ██╗████████╗",
    "██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║╚══██╔══╝",
    "██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║   ",
    "██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║   ",
    "██████╔╝██║  ██║██║ ╚████║██████╔╝██║   ██║   ",
    "╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝   ╚═╝   ",
)

# 68 visible columns total: border + 2-space padding + 62-char content
# + 2-space padding + border. The raw-width contract counts ANSI bytes,
# so the frame stays narrow enough that even a bold-colored content line
# (ESC[1;3Xm ... ESC[0m, 11 bytes of SGR overhead) keeps the raw line
# <= 80 columns. Padding is computed on the *visible* width so
# ANSI-colored content lines up with plain lines.
_CONTENT_WIDTH = 62

def _frame_line(content=""):
    pad = _CONTENT_WIDTH - len(_visible(content))
    if pad < 0:
        raise ValueError("banner content wider than the frame")
    return "║  " + content + " " * pad + "  ║"

_FRAME_TOP_LINE = "╔" + "═" * (_CONTENT_WIDTH + 4) + "╗"
_FRAME_BOT_LINE = "╚" + "═" * (_CONTENT_WIDTH + 4) + "╝"
_FRAME_DIVIDER = "╟" + "─" * (_CONTENT_WIDTH + 4) + "╢"

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
    lines = [_FRAME_TOP_LINE]
    lines += [_frame_line(colorize(row, color, bold)) for row in _WORDMARK]
    lines.append(_frame_line())
    lines += [_frame_line(line) for line in colored_art]
    lines.append(_frame_line(colored_last))
    lines.append(_FRAME_DIVIDER)
    # Info block: plain text only -- account/next-step lines are never
    # colored, so the frame carries the decoration and these stay sober.
    account = "Logged in as bandit%d" % level
    progress = "Progress: %d/34 (%d%%)" % (level, round(level * 100 / 33))
    gap = _CONTENT_WIDTH - len(account) - len(progress)
    lines.append(_frame_line(account + " " * gap + progress))
    lines.append(_frame_line("Final level: submit your result; there is no next account." if level == 33 else "Submit this level, then use CTFd launch panel for bandit%d." % (level + 1)))
    lines.append(_FRAME_BOT_LINE)
    # POLICY lines stay the last three lines, verbatim and uncolored.
    lines.extend(POLICY)
    if any(_has_unsafe_chars(_visible(line)) or len(_visible(line)) > 80 for line in lines):
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
        (root / ("bandit%d" % level)).write_text(text, encoding="utf-8")

if __name__ == "__main__":
    import sys
    generate(sys.argv[1])
