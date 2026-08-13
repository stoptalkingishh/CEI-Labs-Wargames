import json
import os
import tempfile
import unittest

try:
    from build_sentinel import HINTS, challenges_data, build, validate
except ModuleNotFoundError:
    from scripts.build_sentinel import HINTS, challenges_data, build, validate


class SentinelBuilderTests(unittest.TestCase):
    def test_pilot_has_only_start_here_and_five_scored_labs(self):
        self.assertEqual([challenge["id"] for challenge in challenges_data], ["sentinel-start-here", "sentinel-01", "sentinel-02", "sentinel-03", "sentinel-04", "sentinel-05"])
        self.assertNotIn("sentinel-start-here", HINTS)
        self.assertEqual(set(HINTS), {f"sentinel-{number:02d}" for number in range(1, 6)})
        self.assertTrue(validate() is None)

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
            self.assertEqual(len(wallet["entries"]), 5)
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
