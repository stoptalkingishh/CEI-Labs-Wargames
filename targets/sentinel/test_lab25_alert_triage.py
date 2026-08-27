import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import runtime

SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_sentinel


class AlertTriageSummaryTests(unittest.TestCase):
    def test_generator_requires_bounded_corroboration_evidence(self):
        challenge = next(item for item in build_sentinel.challenges_data if item["id"] == "sentinel-25")
        hints = build_sentinel.HINTS["sentinel-25"]

        self.assertIn("alert-triage-summary.txt", challenge["task"])
        self.assertIn("vpn-certificate-inventory.txt", challenge["task"])
        self.assertIn("external AI", challenge["task"])
        self.assertIn("vpn-certificate-inventory.txt", hints[2])

        with tempfile.TemporaryDirectory() as directory:
            build_sentinel.build(directory)
            challenge_yaml = Path(directory, "sentinel-25", "challenge.yml").read_text(encoding="utf-8")
        self.assertIn("vpn-certificate-inventory.txt", challenge_yaml)

    def test_runtime_emits_correlated_static_evidence_and_exact_answer(self):
        with (
            patch.object(runtime, "load_secrets", return_value={key: "test-secret" for key in runtime.KEYS}),
            patch.object(runtime.subprocess, "run"),
            patch.object(runtime, "write_root"),
            patch.object(runtime, "write") as write,
            patch("builtins.open", side_effect=lambda *args, **kwargs: io.StringIO("fixture")),
        ):
            runtime.main()

        evidence = {
            call.args[1]: call.args[2]
            for call in write.call_args_list
            if call.args[0] == "sentinel25"
        }
        summary = evidence["alert-triage-summary.txt"]
        inventory = evidence["vpn-certificate-inventory.txt"]

        self.assertIn("Alert ID: ALT-2048", summary)
        self.assertIn("VPN-GW-01", summary)
        self.assertIn("Certificate status: expired", inventory)
        self.assertIn("2026-08-14T08:55:00Z", inventory)
        self.assertIn("2026-08-14T09:00:00Z", summary)
        self.assertNotIn("http://", summary + inventory)
        self.assertNotIn("https://", summary + inventory)
        self.assertEqual(
            runtime.ANSWERS["sentinel-25"],
            {"alert_id": "ALT-2048", "root_cause": "expired-vpn-certificate", "disposition": "close-benign"},
        )
