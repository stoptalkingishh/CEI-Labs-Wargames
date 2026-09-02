"""Offline guardrails for Natas participant and release documentation."""

import ast
import sys
import types
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


class NatasDocumentationTest(unittest.TestCase):
    def test_completion_contract_covers_release_blockers(self):
        text = (ROOT / "docs/guides/natas-completion-status.md").read_text(encoding="utf-8")
        for required in (
            "not release-ready",
            "natas-attacker:latest",
            "sha-<commit>",
            "CEI-Labs-Engine",
            "GHCR returned\n`403`",
            "event-time verification",
        ):
            self.assertIn(required, text)

    def test_participant_docs_do_not_advertise_unprovisioned_ssh(self):
        for relative_path in (
            "docs/guides/participant-quickstart.md",
            "docs/guides/instructor-cheatsheet.md",
            "docs/guides/facilitation-runbook.md",
        ):
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            self.assertTrue(
                "explicitly" in text
                or "operator has supplied and tested" in text
                or "operator explicitly provisioned and tested" in text
            )
            self.assertNotIn("SSH into the attacker\nworkstation is offered", text)


def load_generator():
    path = ROOT / "scripts" / "build_natas.py"
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    declarations = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "script_dir" for target in node.targets
        ):
            break
        declarations.append(node)
    module = types.ModuleType("build_natas_documentation")
    module.__file__ = str(path)
    exec(compile(ast.Module(body=declarations, type_ignores=[]), str(path), "exec"), module.__dict__)
    return module


class NatasDocumentationContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.natas = load_generator()
        cls.writeups = (ROOT / "docs" / "tracks" / "natas" / "writeups.md").read_text(encoding="utf-8")

    def test_free_descriptions_do_not_disclose_level_nine_through_twelve_solutions(self):
        challenges = {challenge["id"]: challenge for challenge in self.natas.challenges_data}
        descriptions = "\n".join(
            f"{challenges[challenge_id]['name']}\n{challenges[challenge_id]['goal']}\n{challenges[challenge_id]['task']}"
            for challenge_id in ("natas-09", "natas-10", "natas-11", "natas-12")
        )
        for disclosure in (
            ";cat",
            "/etc/natas_webpass/natas10",
            "/etc/natas_webpass/natas11",
            '{"showpassword":"no","bgcolor":"#ffffff"}',
            "<?php",
            "web shell",
        ):
            self.assertNotIn(disclosure, descriptions)

    def test_writeups_use_correct_routes_parameters_and_dynamic_results(self):
        self.assertIn("index.php?viewsource", self.writeups)
        self.assertNotIn("8007/index.php?source", self.writeups)
        self.assertIn("8012/uploads/<uploaded-path>", self.writeups)
        self.assertIn("8013/uploads/<uploaded-path>", self.writeups)
        self.assertNotIn("8012/upload/<uploaded-path>", self.writeups)
        self.assertNotIn("8013/upload/<uploaded-path>", self.writeups)
        self.assertIn("`#` avoids the filtered metacharacters", self.writeups)
        self.assertIn("curl -u natas0:natas0", self.writeups)
        self.assertGreaterEqual(self.writeups.count("**Result:"), 24)
        for level in list(range(1, 15)) + list(range(16, 21)):
            self.assertIn(f"<team's Natas {level} password>", self.writeups)
        self.assertIn("<team-natas-1-password>", self.writeups)
        self.assertIn("<team's final Natas flag>", self.writeups)

    def test_generated_range_ends_at_terminal_level_thirty_four(self):
        level_ids = [
            int(challenge["id"].rsplit("-", 1)[1])
            for challenge in self.natas.challenges_data
            if challenge["id"].startswith("natas-") and challenge["id"] != "natas-start-here"
        ]
        self.assertEqual(level_ids, list(range(35)))
        terminal = next(challenge for challenge in self.natas.challenges_data if challenge["id"] == "natas-34")
        self.assertEqual(terminal["flag"]["data"], "natas34final")


if __name__ == "__main__":
    unittest.main()
