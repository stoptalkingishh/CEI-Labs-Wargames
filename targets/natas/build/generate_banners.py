from pathlib import Path
from html import escape
T={0:"View Source",1:"Right-Click Block",2:"Directory Traversal (Files)",3:"Web Crawlers (Robots.txt)",4:"Referer Spoofing",5:"Cookie Manipulation",6:"Hidden Inclusion Files",7:"Local File Inclusion (LFI)",8:"Reversing Crypto Schemes",9:"Command Injection I",10:"Command Injection II (Sanitization Bypass)",11:"XOR Encryption Bypass",12:"Arbitrary File Upload (Web Shell)",13:"File Upload Bypass (Magic Bytes)",14:"SQL Injection (SQLi)"}

# Small, title-themed ASCII art per level, built around Natas's adopted
# track theme (see docs/wargame-themes.md): "Natas" is "Satan" spelled
# backwards -- a mirrored, upside-down digital underworld where the
# ordinary logic of the web gets inverted and manipulated, the same
# visual language as the attacker workstation's desktop wallpaper
# (cei-labs-engine's natas-wallpaper.svg: NATAS reflecting into SATAN).
# Each piece draws ONLY on that theme plus the level's own (already
# player-visible) title, and the general shape of the vulnerability
# class involved (a layer hidden beneath the surface, a path climbing
# outside its box, two things crossed together) -- but never any actual
# instructional text/labels naming the specific payload, parameter, or
# steps to solve it. Plain ASCII only; HTML-escaped before use, same as
# the rest of the banner text.
#
# Every level's core art is reflected below a waterline -- literally
# mirroring the track's own theme (NATAS/SATAN, the reflected wallpaper)
# and giving each banner more visual height, since taller banners are
# fine here: SSH clients scroll and 1080p screens aren't height-limited
# the way the 80-col line width is.
_WATERLINE = "  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

_CORE = {
    0: ["  [ page ]", "  <!--   -->", "  .-----.", "  | text |", "  '--v--'", "   txet"],  # a layer hidden beneath the page -- a mirror, text reflecting reversed
    1: ["    [ menu ]", "       X", "      o"],                            # a hand reaching, the menu denied
    2: ["  [/][/][..]-->", "  [^][^][v]", "  door door door"],              # a path climbing up levels -- a row of doors, one upside down
    3: ["    /|\\", "   --*--  web", "    \\|/"],                          # a crawler on a mirrored web
    4: ["   o", "  /|\\  letter", "  / \\  (mirrored)"],                   # a messenger with a mirrored letter
    5: ["  ( o o )", "  ( o X )  jar", "  `-----'"],                       # a jar, one cookie cracked open
    6: ["  ~~~~~~~~", "  ~~[ ]~~  rug", "     |"],                        # a trapdoor beneath the rug
    7: ["  [box]<--[../../file]", "  [D][D][D]", "   \\  |  /", "    [ ]"],  # a path reaching outside its box -- doors folding into one another
    8: ["   .--.", "  ( () )", "   `--'", "  (mirrored)"],                # a locked box, reflecting its own key
    9: ["   o", "  /|\\  ...", "  / \\"],                                 # a puppet, an extra word slipped in
    10: ["   o", "  /|\\ -->[ ]", "  / \\"],                              # the same puppet, past a watchful guard
    11: ["  \\   /", "   \\ /", "    X", "   / \\"],                      # two mirrored beams crossing
    12: ["   o", "  /|\\  [==>", "  / \\   slot"],                        # a parcel slipped through a slot
    13: ["  [ parcel ]", "     (o)", "   false seal"],                    # the same parcel, wearing a false seal
    14: ["  [=======]", "  [=cracked=]", "  [=======]"],                  # a vault of records, cracked open
}

ART = {n: core + [_WATERLINE] + list(reversed(core)) for n, core in _CORE.items()}


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
    if any(ord(ch) > 127 for ch in body) or any(len(line) > 80 for line in body.splitlines()):
        raise ValueError("unsafe natas banner rendering for level %d" % n)
    return body


def main(root):
    if set(ART) != set(T):
        raise ValueError("Natas banner art must cover the same levels as T")
    root = Path(root)
    for n, title in T.items():
        text = render(n, title)
        (root / ("natas%d.html" % n)).write_text(
            '<pre class="cei-login-banner">' + escape(text) + "</pre>", "ascii"
        )


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
