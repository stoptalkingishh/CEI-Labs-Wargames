"""Offline guardrails for Natas participant and release documentation."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent.parent


class NatasDocumentationTest(unittest.TestCase):
    def test_completion_contract_covers_release_blockers(self):
        text = (ROOT / "docs/natas-completion-status.md").read_text(encoding="utf-8")
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
            "docs/participant-quickstart.md",
            "docs/instructor-cheatsheet.md",
            "docs/facilitation-runbook.md",
        ):
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            self.assertTrue(
                "explicitly" in text or "operator has supplied and tested" in text
            )
            self.assertNotIn("SSH into the attacker\nworkstation is offered", text)


if __name__ == "__main__":
    unittest.main()
