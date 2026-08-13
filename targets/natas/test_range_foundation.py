"""Static contracts for the unreleased Natas 15-34 range foundation."""
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parent


class NatasRangeFoundationTests(unittest.TestCase):
    def test_all_range_artifacts_are_configured(self):
        levels = (ROOT / "build" / "natas_levels.py").read_text()
        users = (ROOT / "build" / "01-create-users.sh").read_text()
        webpasses = (ROOT / "build" / "02-set-webpasswords.sh").read_text()
        vhosts = (ROOT / "build" / "03-generate-vhosts.py").read_text()
        docker = (ROOT / "Dockerfile").read_text()
        self.assertIn("LAST_LEVEL = 34", levels)
        self.assertIn("natas34final", levels)
        self.assertIn("seq 0 34", users)
        self.assertIn("seq 1 34", webpasses)
        self.assertIn("LEVELS", vhosts)
        self.assertIn("EXPOSE 8000-8034", docker)

    def test_pending_content_is_explicitly_non_secret(self):
        generator = (ROOT / "build" / "generate_pending_content.py").read_text()
        self.assertIn("SCENARIO_PENDING", generator)
        self.assertIn("not a password, flag, or secret", generator)
        self.assertNotIn("natas%d" % 35, generator)

    def test_level_fourteen_continues_the_webpass_chain(self):
        page = (ROOT / "content" / "natas14" / "index.php").read_text()
        self.assertIn("password for natas15", page)
        self.assertIn("$next_password", page)


if __name__ == "__main__":
    unittest.main()
