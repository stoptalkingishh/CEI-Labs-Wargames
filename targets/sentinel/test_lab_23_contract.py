import sys
import unittest
from pathlib import Path

import runtime

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import build_sentinel


class SentinelLab23ContractTests(unittest.TestCase):
    def test_generator_scopes_validation_to_bounded_local_evidence(self):
        challenge = next(item for item in build_sentinel.challenges_data if item["id"] == "sentinel-23")

        self.assertIn("bounded committed local log corpus", challenge["goal"])
        self.assertIn("static local rule, log corpus, and decision record", challenge["task"])
        self.assertIn("Compare the fixed rule condition with each corpus record", build_sentinel.HINTS["sentinel-23"][0])
        self.assertIn("not a prompt to run a live detection service", build_sentinel.HINTS["sentinel-23"][1])

    def test_fixed_rule_matches_only_the_encoded_command_record(self):
        condition = "-EncodedCommand"
        records = runtime.LAB_23_CORPUS.splitlines()

        self.assertEqual(runtime.LAB_23_RULE, "id: NS-DET-104\ntitle: Encoded PowerShell Command\ncondition: command_line contains '-EncodedCommand'\n")
        self.assertEqual(len(records), 2)
        self.assertEqual(sum(condition in record for record in records), 1)
        self.assertIn("Corpus records: 2", runtime.LAB_23_DECISION_RECORD)
        self.assertIn("Matches: 1", runtime.LAB_23_DECISION_RECORD)
        self.assertIn("Decision: triggered", runtime.LAB_23_DECISION_RECORD)

    def test_runtime_answer_and_evidence_remain_offline_and_aligned(self):
        self.assertEqual(runtime.ANSWERS["sentinel-23"], {"rule_id": "NS-DET-104", "matches": 1, "decision": "triggered"})
        self.assertIn("No live detection service was queried", runtime.LAB_23_DECISION_RECORD)
        self.assertNotIn("http://", runtime.LAB_23_CORPUS)
        self.assertNotIn("https://", runtime.LAB_23_CORPUS)


if __name__ == "__main__":
    unittest.main()
