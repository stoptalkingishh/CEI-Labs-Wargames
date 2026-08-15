import unittest

try:
    from build_sentinel import HINTS, challenges_data
except ModuleNotFoundError:
    from scripts.build_sentinel import HINTS, challenges_data


class Sentinel26BuilderTests(unittest.TestCase):
    def test_lab_26_requires_a_static_evidence_review_without_disclosing_the_outcome(self):
        challenge = next(item for item in challenges_data if item["id"] == "sentinel-26")
        task = challenge["task"].lower()
        hints = " ".join(HINTS["sentinel-26"]).lower()

        self.assertIn("static local file", task)
        self.assertIn("do not scan networks", task)
        self.assertIn("lacks the required dhcp registration", task)
        self.assertIn("arp-observed mac", hints)
        self.assertIn("do not scan a network", hints)
        self.assertIn("device_mac, zone, and disposition", hints)


if __name__ == "__main__":
    unittest.main()
