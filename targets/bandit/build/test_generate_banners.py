import importlib.util
import tempfile
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("banners", Path(__file__).with_name("generate_banners.py"))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

class BannerTests(unittest.TestCase):
    def test_complete_safe_rendering(self):
        self.assertEqual(set(mod.TITLES), set(range(34)))
        self.assertEqual(mod.TITLES[18], "Shell Bypass")
        self.assertEqual(mod.TITLES[32], "Shell Overrides")
        with tempfile.TemporaryDirectory() as root:
            mod.generate(root)
            self.assertEqual(len(list(Path(root).iterdir())), 34)
            for level in range(34):
                text = (Path(root) / ("bandit%d" % level)).read_text(encoding="ascii")
                self.assertIn("Misuse of this system is prohibited", text)
                self.assertIn("AI or external tools", text)
                self.assertIn("assigned challenge environment", text)
                self.assertLessEqual(max(map(len, text.splitlines())), 80)

    def test_art_covers_all_levels(self):
        self.assertEqual(set(mod.ART), set(range(34)))

    def test_every_banner_is_genuinely_distinct(self):
        # Not just "34 files exist" -- actually diff the rendered content,
        # and specifically the art portion (banner text minus the
        # level-specific title/account lines, which legitimately differ by
        # level number/title already).
        rendered = {level: mod.render(level) for level in range(34)}
        seen = {}
        for level, text in rendered.items():
            self.assertNotIn(text, seen.values(), "bandit%d duplicates another level's banner" % level)
            seen[level] = text

        art_only = {level: "\n".join(mod.ART[level]) for level in range(34)}
        seen_art = {}
        for level, art_text in art_only.items():
            self.assertNotIn(
                art_text, seen_art.values(),
                "bandit%d reuses another level's art verbatim" % level,
            )
            seen_art[level] = art_text

    def test_art_is_themed_to_title(self):
        # Judgment-call spot checks -- just confirm a few levels' art contains
        # a recognizable token tying it back to the title theme, so we don't
        # regress to one generic shape reused everywhere.
        clock_level = 21  # "Cron Jobs"
        clock_art = "\n".join(mod.ART[clock_level])
        self.assertTrue(
            "12" in clock_art and "6" in clock_art,
            "expected a clock face (12/6) for the Cron Jobs banner",
        )

        needle_level = 5  # "The Needle"
        self.assertTrue(
            any("~" in line for line in mod.ART[needle_level]),
            "expected a haystack (~~~) for The Needle banner",
        )

        matryoshka_level = 12  # "Matryoshka"
        self.assertTrue(
            any(line.count("[") >= 3 for line in mod.ART[matryoshka_level]),
            "expected nested brackets for the Matryoshka banner",
        )

        escape_level = 33  # "Final Escape"
        self.assertTrue(
            any("+--+" in line or "->" in line for line in mod.ART[escape_level]),
            "expected a door/exit motif for the Final Escape banner",
        )

    def test_color_is_well_formed_and_always_resets(self):
        # Every SGR color-open code must be closed with a reset on the same
        # line, and the reset must actually appear right after the colored
        # segment -- otherwise color could bleed into whatever the terminal
        # prints next (the next banner line, or the shell prompt).
        import re
        open_re = re.compile(r"\x1b\[(?:1;)?3[0-7]m")
        for level in range(34):
            for line in mod.render(level).splitlines():
                opens = open_re.findall(line)
                self.assertEqual(
                    len(opens), line.count(mod.RESET),
                    "bandit%d has an unmatched color code on: %r" % (level, line),
                )
                # only the most widely supported basic SGR 8-color codes
                for m in re.finditer(r"\x1b\[([0-9;]*)m", line):
                    codes = m.group(1)
                    self.assertTrue(
                        codes == "0" or re.fullmatch(r"(1;)?3[0-7]", codes),
                        "bandit%d uses a non-basic SGR code: %r" % (level, codes),
                    )
                # a color-open sequence, if present, is immediately closed
                # before the line ends -- no dangling/open-ended color run.
                if opens:
                    self.assertTrue(
                        line.rstrip("\n").endswith(mod.RESET) or mod.RESET in line,
                        "bandit%d color never resets on: %r" % (level, line),
                    )

    def test_color_is_supplementary_not_load_bearing(self):
        # Strip every ANSI escape and confirm the banners are still fully
        # readable plain text, and still just as distinct from each other as
        # they were before color was added -- color decorates the art, it
        # does not carry any of the distinguishing information.
        import re
        strip_re = re.compile(r"\x1b\[[0-9;]*m")
        plain = {level: strip_re.sub("", mod.render(level)) for level in range(34)}
        seen = {}
        for level, text in plain.items():
            self.assertNotIn(text, seen.values(), "bandit%d not distinct once color is stripped" % level)
            seen[level] = text
            self.assertTrue(all(ord(ch) <= 127 for ch in text))
            self.assertLessEqual(max(len(l) for l in text.splitlines()), 80)

    def test_palette_progresses_gradually_with_level_depth(self):
        # Color identity should shift gradually as levels get deeper, not
        # jump around at random, and should actually span a range rather
        # than being one flat color for the whole track.
        tiers = [mod.palette_for(level) for level in range(34)]
        indices = [mod._PALETTE_TIERS.index(t) for t in tiers]
        self.assertEqual(indices, sorted(indices), "palette tier must be non-decreasing with level")
        self.assertGreater(len(set(tiers)), 1, "palette must actually vary across the track")
        self.assertEqual(mod.palette_for(0), mod._PALETTE_TIERS[0])
        self.assertEqual(mod.palette_for(33), mod._PALETTE_TIERS[-1])

if __name__ == "__main__": unittest.main()
