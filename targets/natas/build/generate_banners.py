from pathlib import Path
from html import escape
import importlib.util as _ilu
from natas_levels import LAST_LEVEL, LEVELS, title

# Reuse the exact same cool-blue -> hot-magenta per-level hue used for the
# page's own background/heading theme (see build/generate_themes.py's
# _progression_hue/_hue_to_hex) so the banner art's color matches the
# level's already-established color identity instead of inventing a
# second, redundant palette.
_themes_spec = _ilu.spec_from_file_location("natas_themes", Path(__file__).with_name("generate_themes.py"))
_themes = _ilu.module_from_spec(_themes_spec); _themes_spec.loader.exec_module(_themes)

T = {n: title(n) for n in LEVELS}

COLOR = {n: _themes._hue_to_hex(_themes._progression_hue(n)) for n in LEVELS}

# Storyboard, not standalone scenes: rather than each level inventing its
# own isolated picture (which kept reading as noise -- see PR history),
# every banner is one frame of a single continuous descent into Natas's
# adopted track theme (see docs/wargame-themes.md): "Natas" is "Satan"
# spelled backwards -- a mirrored, upside-down digital underworld. A
# vertical shaft shows how deep the player has descended: 'x' = a level
# already passed through, 'o' = the level they're on right now (this
# level), '.' = depths still ahead, unreached. The shaft's shape is what
# makes each banner genuinely distinct -- structurally guaranteed, not
# hand-invented per level -- and reading the whole set in order shows a
# steady descent from the surface (natas0) to the depths (natas14),
# reinforced by generate_themes.py's own cool-to-hot color progression
# (COLOR above) applied to this same art via main()'s <span>. This also
# means no level's art can ever leak a hint: it only encodes "how deep
# you are," nothing about any specific vulnerability.
def _shaft(level, total=LAST_LEVEL + 1):
    rows = ["  [%s]" % ("x" if i < level else ("o" if i == level else ".")) for i in range(total)]
    return ["  surface"] + rows + ["  depths"]

ART = {n: _shaft(n) for n in LEVELS}

# --- Visual redesign (banner glow-up) ---------------------------------------
# The whole banner is framed in a box-drawing border (76 cols wide, inside
# the 80-col cap) with a large NATAS wordmark at the top, the depth shaft
# below it, a divider, and an aligned info block (title / account / progress
# / next step). The shaft art itself stays byte-for-byte identical (it is the
# pinned contract and is the only part wrapped in the per-level hue <span>),
# so the shaft region is deliberately left open-sided -- it reads as the
# shaft piercing the box's floor and ceiling on its way to the depths.
_WIDTH = 76
_INNER = _WIDTH - 2  # space between the side borders

# 5-row block-letter glyphs for the track wordmark.
_GLYPHS = {
    "N": ["N   N", "NN  N", "N N N", "N  NN", "N   N"],
    "A": [" AAA ", "A   A", "AAAAA", "A   A", "A   A"],
    "T": ["TTTTT", "  T  ", "  T  ", "  T  ", "  T  "],
    "S": [" SSS ", "S    ", " SS  ", "    S", "SSS  "],
}


def _wordmark(word):
    rows = [""] * 5
    for ch in word:
        glyph = _GLYPHS[ch]
        for i in range(5):
            rows[i] += ("" if not rows[i] else "  ") + glyph[i]
    return rows


def _boxed(line=""):
    """One content row inside the frame, with 2-space inner padding."""
    return "║" + ("  " + line).ljust(_INNER) + "║"


def _frame(wordmark, art_lines, info_lines):
    top = "╔" + "═" * _INNER + "╗"
    upper = "╠" + "═" * _INNER + "╣"
    lower = "╠" + "═" * _INNER + "╣"
    bottom = "╚" + "═" * _INNER + "╝"
    lines = [top]
    for row in wordmark:
        lines.append("║" + row.center(_INNER) + "║")
    lines.append(upper)
    # The shaft art block: emitted bare (no side borders) so the pinned
    # art text stays contiguous -- the hue <span> wraps exactly this block.
    lines.extend(art_lines)
    lines.append(lower)
    lines.extend(_boxed(info) for info in info_lines)
    lines.append(bottom)
    return lines


def _next_step(n):
    if n < LAST_LEVEL:
        return "Next step: solve natas%d to descend to natas%d" % (n, n + 1)
    return "Next step: none -- you have reached the depths"


def render(n, title):
    art_lines = ART[n]
    info_lines = [
        "CEI Labs Natas %d: %s" % (n, title),
        "Account: natas%d" % n,
        "Progress: %d/%d levels descended (%d%%)" % (n, LAST_LEVEL, n * 100 // LAST_LEVEL),
        _next_step(n),
    ]
    body = "\n".join(_frame(_wordmark("NATAS"), art_lines, info_lines)) + "\n"
    body += (
        "Authorized CEI Labs training only. Misuse of this system is prohibited.\n"
        "Do not use AI or external tools/services to cheat or obtain answers.\n"
        "Stay within your assigned challenge environment only.\n"
    )
    # Unicode is allowed; only control characters (C0/C1, DEL) are not --
    # those could inject something other than visible glyphs.
    if any(ord(ch) < 0x20 and ch != "\n" or 0x7F <= ord(ch) <= 0x9F for ch in body) or any(len(line) > 80 for line in body.splitlines()):
        raise ValueError("unsafe natas banner rendering for level %d" % n)
    return body


def main(root):
    if set(ART) != set(T):
        raise ValueError("Natas banner art must cover the same levels as T")
    root = Path(root)
    for n, title in T.items():
        text = render(n, title)
        art_block = "\n".join(ART[n])
        escaped_text = escape(text)
        escaped_art = escape(art_block)
        colored_art = '<span style="color:%s">%s</span>' % (COLOR[n], escaped_art)
        html_body = escaped_text.replace(escaped_art, colored_art, 1)
        (root / ("natas%d.html" % n)).write_text(
            '<pre class="cei-login-banner">' + html_body + "</pre>", encoding="utf-8"
        )


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
