import unittest

try:
    from build_sentinel import HINTS, challenges_data
except ModuleNotFoundError:
    from scripts.build_sentinel import HINTS, challenges_data


class Lab22GeneratorTests(unittest.TestCase):
    def test_lab_22_description_and_hints_preserve_the_offline_boundary(self):
        challenge = next(item for item in challenges_data if item["id"] == "sentinel-22")
        hints = HINTS["sentinel-22"]

        self.assertEqual(challenge["name"], "Sentinel 22: Phishing Header Analysis")
        self.assertIn("static local file", challenge["task"])
        self.assertIn("do not contact mail systems or services", challenge["task"])
        self.assertIn("non-staged, offline Sentinel expansion", challenge["task"])
        self.assertIn("SPF pass for the envelope sender", hints[2])
        self.assertIn("from_domain, return_path_domain, and dmarc", hints[2])
        self.assertNotIn("northstar.training", " ".join(hints))
        self.assertNotIn("invoice-notice.example", " ".join(hints))


if __name__ == "__main__":
    unittest.main()
