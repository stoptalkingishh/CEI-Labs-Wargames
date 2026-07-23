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

if __name__ == "__main__": unittest.main()
