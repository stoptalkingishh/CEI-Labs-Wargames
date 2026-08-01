from pathlib import Path
from html import escape
import importlib.util as _ilu

# Reuse the exact same cool-blue -> hot-magenta per-level hue used for the
# page's own background/heading theme (see build/generate_themes.py's
# _progression_hue/_hue_to_hex) so the banner art's color matches the
# level's already-established color identity instead of inventing a
# second, redundant palette.
_themes_spec = _ilu.spec_from_file_location("natas_themes", Path(__file__).with_name("generate_themes.py"))
_themes = _ilu.module_from_spec(_themes_spec); _themes_spec.loader.exec_module(_themes)

T={0:"View Source",1:"Right-Click Block",2:"Directory Traversal (Files)",3:"Web Crawlers (Robots.txt)",4:"Referer Spoofing",5:"Cookie Manipulation",6:"Hidden Inclusion Files",7:"Local File Inclusion (LFI)",8:"Reversing Crypto Schemes",9:"Command Injection I",10:"Command Injection II (Sanitization Bypass)",11:"XOR Encryption Bypass",12:"Arbitrary File Upload (Web Shell)",13:"File Upload Bypass (Magic Bytes)",14:"SQL Injection (SQLi)"}

COLOR = {n: _themes._hue_to_hex(_themes._progression_hue(n)) for n in range(15)}

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
def _shaft(level, total=15):
    rows = ["  [%s]" % ("x" if i < level else ("o" if i == level else ".")) for i in range(total)]
    return ["  surface"] + rows + ["  depths"]

ART = {n: _shaft(n) for n in range(15)}


def render(n, title):
    art_lines = ART[n]
    body = "\n".join(art_lines) + "\n" if art_lines else ""
    body += (
        "CEI Labs Natas %d: %s\n"
        "Account: natas%d\n"
        "Authorized CEI Labs training only. Misuse of this system is prohibited.\n"
        "Do not use AI or external tools/services to cheat or obtain answers.\n"
        "Stay within your assigned challenge environment only.\n"
    ) % (n, title, n)
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
