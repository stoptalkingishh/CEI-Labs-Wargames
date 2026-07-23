"""Generates one CSS file per Natas level (natas0.css .. natas14.css),
each containing TWO selectable states -- `.cei-locked` and `.cei-solved`
-- picked at request time by cei-natas-banner.php based on a local
"solved" marker file (see cei_natas_theme_state() in that script).

IMPORTANT -- what "solved" means here: Natas's own web app has NO
visibility into CTFd's scoring/solve state at all (they're completely
separate systems -- see docs/security-audit-status.md and the PR
description on the branch that introduced this file for the full
investigation). The signal used instead is locally observable by Natas
itself: level N is marked "solved" the moment a request successfully
clears HTTP Basic Auth on level (N+1)'s vhost, since reaching that point
is proof the player actually obtained level N's password (whether via
the intended vulnerability or not). There is deliberately no themed
"solved" state for natas14 -- there is no natas15 vhost to observe an
auth success against, so that level's background never leaves its
"locked" state under this signal. See cei-natas-banner.php.

CSS-only (no binary image assets) -- gradients/patterns keep this
diffable, avoid repo bloat, and are trivial to re-theme per level.

Palette direction: hue is NOT arbitrary per level -- it's a continuous
progression across the whole 0-14 track (see _progression_hue below),
cool cyan/blue at natas0 (passive recon: view-source, robots.txt) sliding
through amber/violet in the middle (active manipulation: cookies,
referer, LFI) to hot red/magenta by natas14 (full exploitation: SQLi,
web-shell upload). Each level keeps its own distinct CSS pattern (grid,
stripes, dots, ...) tied to its specific vuln class, but the color a
player sees should visibly "warm up" as they progress deeper into the
track -- a rough visual proxy for how far along they are, independent of
the per-level solved/locked toggle. This is deliberately a different
palette family (cool->hot hue sweep, web/security-toned) from Bandit's
and Krypton's terminal banner art, which use their own separate
ANSI-driven palettes -- see those tracks' generators, not shared here.
"""
from pathlib import Path
import colorsys

# n -> (title, pattern); color is NOT hardcoded per level -- see
# _progression_hue(), which derives each level's hue from its position
# in the 0-14 track. "pattern" stays level-specific: it's what makes
# each level's texture thematically match its own vulnerability class,
# independent of the shared color progression.
THEMES = {
    0: ("View Source", "flat"),
    1: ("Right-Click Block", "diagonal-stripes"),
    2: ("Directory Traversal (Files)", "path-grid"),
    3: ("Web Crawlers (Robots.txt)", "crawl-grid"),
    4: ("Referer Spoofing", "chevrons"),
    5: ("Cookie Manipulation", "dots"),
    6: ("Hidden Inclusion Files", "layered"),
    7: ("Local File Inclusion (LFI)", "folder-stripes"),
    8: ("Reversing Crypto Schemes", "hex-noise"),
    9: ("Command Injection I", "terminal-scan"),
    10: ("Command Injection II (Sanitization Bypass)", "diagonal-stripes"),
    11: ("XOR Encryption Bypass", "binary-stripes"),
    12: ("Arbitrary File Upload (Web Shell)", "upload-arrows"),
    13: ("File Upload Bypass (Magic Bytes)", "byte-blocks"),
    14: ("SQL Injection (SQLi)", "table-grid"),
}

# Cool recon-blue (n=0) -> hot exploitation-magenta/red (n=14), swept
# through HSL hue space (200deg down to -20deg/340deg, wrapping through
# violet rather than back through green) so the whole track reads as one
# continuous "getting hotter" gradient rather than 15 unrelated colors.
_HUE_START, _HUE_END = 200, -20


def _progression_hue(n, total=14):
    return _HUE_START + (_HUE_END - _HUE_START) * (n / total)


def _hue_to_hex(hue_deg, s=0.55, l=0.48):
    h = (hue_deg % 360) / 360.0
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))

# Each "pattern" name maps to a background-image value built from CSS
# gradients only. Reused across levels that share a visual family
# (e.g. two stripe-based levels get different hues, not different
# patterns) -- that's intentional, the hue is what makes them distinct.
def _pattern_css(pattern, hue, dim):
    """Returns a CSS background-image value. `dim` is a paler backdrop
    tone used for the locked state; the solved state uses `hue` at full
    strength."""
    if pattern == "flat":
        return f"linear-gradient(180deg, {dim}, {dim})"
    if pattern == "diagonal-stripes":
        return (f"repeating-linear-gradient(45deg, {dim} 0 18px, "
                 f"{hue}22 18px 36px)")
    if pattern == "path-grid":
        return (f"linear-gradient(90deg, {hue}33 1px, transparent 1px), "
                 f"linear-gradient(0deg, {hue}33 1px, transparent 1px), "
                 f"linear-gradient(180deg, {dim}, {dim})")
    if pattern == "crawl-grid":
        return (f"radial-gradient({hue}44 1.5px, transparent 1.5px), "
                 f"linear-gradient(180deg, {dim}, {dim})")
    if pattern == "chevrons":
        return (f"repeating-linear-gradient(135deg, {dim} 0 14px, "
                 f"{hue}33 14px 28px)")
    if pattern == "dots":
        return (f"radial-gradient({hue}55 2px, transparent 2px), "
                 f"linear-gradient(180deg, {dim}, {dim})")
    if pattern == "layered":
        return (f"linear-gradient(180deg, {hue}22 0 8px, transparent 8px 24px), "
                 f"linear-gradient(180deg, {dim}, {dim})")
    if pattern == "folder-stripes":
        return (f"repeating-linear-gradient(0deg, {dim} 0 22px, "
                 f"{hue}2a 22px 26px)")
    if pattern == "hex-noise":
        return (f"repeating-linear-gradient(60deg, {dim} 0 10px, {hue}22 10px 12px), "
                 f"repeating-linear-gradient(-60deg, transparent 0 10px, {hue}18 10px 12px)")
    if pattern == "terminal-scan":
        return (f"repeating-linear-gradient(0deg, {dim} 0 3px, {hue}26 3px 4px)")
    if pattern == "binary-stripes":
        return (f"repeating-linear-gradient(90deg, {dim} 0 6px, {hue}30 6px 8px, "
                 f"{dim} 8px 16px, {hue}30 16px 20px)")
    if pattern == "upload-arrows":
        return (f"repeating-linear-gradient(90deg, {dim} 0 24px, {hue}2a 24px 26px)")
    if pattern == "byte-blocks":
        return (f"linear-gradient(90deg, {hue}30 1px, transparent 1px) 0 0/16px 16px, "
                 f"linear-gradient(0deg, {hue}30 1px, transparent 1px) 0 0/16px 16px, "
                 f"linear-gradient(180deg, {dim}, {dim})")
    if pattern == "table-grid":
        return (f"linear-gradient(90deg, {hue}3a 1px, transparent 1px) 0 0/48px 48px, "
                 f"linear-gradient(0deg, {hue}3a 1px, transparent 1px) 0 0/48px 48px, "
                 f"linear-gradient(180deg, {dim}, {dim})")
    return f"linear-gradient(180deg, {dim}, {dim})"


CSS_TEMPLATE = """/* Generated by build/generate_themes.py -- Natas %(n)d: %(title)s
 * Locked state (default): shown until the "solved" signal below fires.
 * Solved state: shown once cei-natas-banner.php observes a successful
 * Basic Auth request against %(next_desc)s (see that file's
 * cei_natas_theme_state()). %(solved_note)s
 */
body.cei-locked {
  background-color: #14151a;
  background-image: %(locked_bg)s;
  background-attachment: fixed;
}
body.cei-solved {
  background-color: #0c0f0c;
  background-image: %(solved_bg)s;
  background-attachment: fixed;
  transition: background-color 400ms ease;
}
body.cei-solved::after {
  content: "NATAS%(n)d SOLVED";
  position: fixed;
  bottom: 10px;
  right: 14px;
  font: 11px/1 monospace;
  letter-spacing: 0.08em;
  color: %(hue)s;
  opacity: 0.65;
  pointer-events: none;
}
"""


def main(root):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    for n, (title, pattern) in THEMES.items():
        hue = _hue_to_hex(_progression_hue(n))
        locked_bg = _pattern_css(pattern, hue, "#1b1c22")
        solved_bg = _pattern_css(pattern, hue, "#10140f")
        solved_note = (
            "natas14 has no next level to observe, so it never reaches "
            "the solved state under this signal -- see module docstring."
            if n == 14 else ""
        )
        next_desc = f"natas{n + 1}" if n < 14 else "a level that doesn't exist"
        css = CSS_TEMPLATE % {
            "n": n,
            "title": title,
            "next_desc": next_desc,
            "hue": hue,
            "locked_bg": locked_bg,
            "solved_bg": solved_bg,
            "solved_note": solved_note,
        }
        (root / f"natas{n}.css").write_text(css, "ascii")


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
