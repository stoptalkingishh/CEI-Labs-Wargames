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

if __name__ == "__main__": unittest.main()
