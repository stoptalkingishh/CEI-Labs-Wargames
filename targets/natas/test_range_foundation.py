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
        self.assertIn("natas14final", levels)
        self.assertIn("seq 0 34", users)
        self.assertIn("seq 1 34", webpasses)
        self.assertIn("LEVELS", vhosts)
        self.assertIn("EXPOSE 8000-8034", docker)

    def test_pending_content_is_explicitly_non_secret(self):
        generator = (ROOT / "build" / "generate_pending_content.py").read_text()
        self.assertIn("SCENARIO_PENDING", generator)
        self.assertIn("not a password, flag, or secret", generator)
        self.assertNotIn("natas%d" % 35, generator)

    def test_level_fourteen_preserves_the_deployed_terminal_contract(self):
        page = (ROOT / "content" / "natas14" / "index.php").read_text()
        entrypoint = (ROOT / "entrypoint.sh").read_text()
        self.assertIn("FINAL Natas flag", page)
        self.assertIn("$final_flag", page)
        self.assertNotIn("natas15", page)
        self.assertIn('"natas14final", "final_flag"', entrypoint)

    def test_pending_content_cannot_use_reserved_or_terminal_secrets(self):
        generator = (ROOT / "build" / "generate_pending_content.py").read_text()
        for secret_name in ("natas15", "natas34", "natas14final"):
            self.assertNotIn(secret_name, generator)

    def test_batches_a_and_b_replace_only_their_pending_pages(self):
        generator = (ROOT / "build" / "generate_pending_content.py").read_text()
        self.assertIn("range(25, LAST_LEVEL + 1)", generator)
        for level in range(15, 25):
            page = (ROOT / "content" / ("natas%d" % level) / "index.php").read_text()
            self.assertNotIn("SCENARIO_PENDING", page)
        self.assertNotIn("natas15", (ROOT / "content" / "natas14" / "index.php").read_text())

    def test_batch_a_isolated_emulators_do_not_spawn_commands(self):
        pages = "\n".join(
            (ROOT / "content" / ("natas%d" % level) / "index.php").read_text()
            for level in range(15, 20)
        )
        for forbidden in ("shell_exec", "exec(", "system(", "proc_open", "passthru", "unserialize", "$_SESSION"):
            self.assertNotIn(forbidden, pages)

    def test_natas_sixteen_uses_only_a_bounded_reference_expansion(self):
        page = (ROOT / "content" / "natas16" / "index.php").read_text()
        self.assertIn("search \\{\\{ref:", page)
        self.assertIn("'handoff' => 'sealed-record'", page)
        self.assertNotIn("catalog credential", page)
        self.assertIn("highlight_file(__FILE__)", page)

    def test_batch_b_scenarios_are_bounded_and_do_not_use_framework_sessions(self):
        pages = "\n".join(
            (ROOT / "content" / ("natas%d" % level) / "index.php").read_text()
            for level in range(20, 25)
        )
        for forbidden in ("$_SESSION", "session_start", "unserialize", "shell_exec", "exec(", "system(", "proc_open", "http://", "https://"):
            self.assertNotIn(forbidden, pages)
        self.assertIn("natas-batch-b", (ROOT / "entrypoint.sh").read_text())
        self.assertIn("Cache-Control: no-store", (ROOT / "content" / "natas22" / "index.php").read_text())
        natas23 = (ROOT / "content" / "natas23" / "index.php").read_text()
        self.assertIn("$noncanonical_boundary", natas23)
        self.assertIn("strlen($token) >= 2", natas23)

    def test_batch_b_record_is_recreated_on_instance_start(self):
        entrypoint = (ROOT / "entrypoint.sh").read_text()
        self.assertIn('state_path = os.path.join(state_dir, "record-%s.txt" % team)', entrypoint)
        self.assertIn('state_file.write("id=guest|role=viewer|note=welcome")', entrypoint)
        self.assertIn('os.chmod(state_path, 0o600)', entrypoint)


if __name__ == "__main__":
    unittest.main()
