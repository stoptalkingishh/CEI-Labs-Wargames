import json
import os
import tempfile
import unittest

try:
    from build_sentinel import HINTS, challenges_data, build, validate
except ModuleNotFoundError:
    from scripts.build_sentinel import HINTS, challenges_data, build, validate


class SentinelBuilderTests(unittest.TestCase):
    def test_pilot_and_deferred_expansion_have_expected_labs(self):
        self.assertEqual([challenge["id"] for challenge in challenges_data], ["sentinel-start-here", "sentinel-01", "sentinel-02", "sentinel-03", "sentinel-04", "sentinel-05", "sentinel-22", "sentinel-23", "sentinel-24", "sentinel-25", "sentinel-26", "sentinel-27"])
        self.assertNotIn("sentinel-start-here", HINTS)
        self.assertEqual(set(HINTS), {f"sentinel-{number:02d}" for number in range(1, 6)} | {f"sentinel-{number}" for number in range(22, 28)})
        self.assertTrue(validate() is None)

    def test_expansion_labs_are_explicitly_deferred_and_offline(self):
        self.assertEqual(
            [challenge["name"] for challenge in challenges_data[-6:]],
            [
                "Sentinel 22: Phishing Header Analysis",
                "Sentinel 23: Detection Rule Validation",
                "Sentinel 24: Endpoint Enrollment Evidence",
                "Sentinel 25: Alert Triage Summary",
                "Sentinel 26: Network Inventory Review",
                "Sentinel 27: Evidence Metadata Review",
            ],
        )
        for challenge in challenges_data[-6:]:
            self.assertIn("non-staged, offline Sentinel expansion", challenge["task"])
            self.assertIn("Labs 06-21 remain planned", challenge["task"])
            self.assertIn("local", challenge["task"])
        for lab in (f"sentinel-{number}" for number in range(22, 28)):
            self.assertNotIn("network scan", " ".join(HINTS[lab]).lower())
        self.assertIn("external ai", HINTS["sentinel-25"][1].lower())
        self.assertIn("do not scan", HINTS["sentinel-26"][1].lower())

    def test_structured_submission_copy_replaces_obsolete_result_fields(self):
        for lab in ("sentinel-02", "sentinel-03", "sentinel-05"):
            self.assertIn("sentinel-submit", HINTS[lab][2])
        self.assertNotIn("approved-review-result", HINTS["sentinel-02"][2])
        self.assertNotIn("recorded disposition", HINTS["sentinel-03"][2])
        self.assertNotIn("signed finding", HINTS["sentinel-05"][2])

    def test_generated_yaml_and_wallet_keep_the_runtime_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            build(directory)
            with open(os.path.join(directory, "sentinel-hint-wallet.json"), encoding="utf-8") as source:
                wallet = json.load(source)
            self.assertEqual(wallet["track"], "sentinel")
            self.assertEqual(len(wallet["entries"]), 11)
            for entry in wallet["entries"]:
                self.assertEqual([tier["cost"] for tier in entry["tiers"]], [20, 50, 85])
            for challenge in challenges_data:
                with open(os.path.join(directory, challenge["id"], "challenge.yml"), encoding="utf-8") as source:
                    content = source.read()
                self.assertIn("instance_type: single-target", content)
                self.assertIn("instance_group: sentinel", content)
                self.assertIn(f'data: "{challenge["flag"]["data"]}"', content)
                self.assertIn("state: hidden", content)
                self.assertNotIn("hints:", content)


if __name__ == "__main__":
    unittest.main()
