import unittest

import answer_service
import runtime


class SentinelLab24ContractTests(unittest.TestCase):
    def test_answer_requires_the_shared_enrollment_record_id(self):
        expected = {
            "endpoint_id": "northstar-lt-042",
            "enrollment_record_id": "ENR-24-042",
            "enrollment_status": "enrolled",
            "key_status": "active",
        }
        credentials = {"sentinel-24": "lab-24-credential"}
        submission = {"lab": "sentinel-24", "answer": expected}
        self.assertEqual(
            answer_service.release(submission, "sentinel24", {"sentinel-24": expected}, credentials),
            "lab-24-credential",
        )

        incomplete = {"lab": "sentinel-24", "answer": {key: value for key, value in expected.items() if key != "enrollment_record_id"}}
        with self.assertRaises(SystemExit):
            answer_service.release(incomplete, "sentinel24", {"sentinel-24": expected}, credentials)

    def test_evidence_correlates_all_three_records_without_live_endpoints(self):
        with open("runtime.py", encoding="utf-8") as source:
            runtime_source = source.read()
        evidence = runtime_source[runtime_source.index('write("sentinel24"'):runtime_source.index('write("sentinel25"')]
        self.assertEqual(evidence.count("Enrollment record ID: ENR-24-042"), 3)
        self.assertIn("Inventory entry", evidence)
        self.assertIn("Enrollment transcript", evidence)
        self.assertIn("Key lifecycle record", evidence)
        self.assertIn("Do not contact an endpoint, agent, or manager.", evidence)
        self.assertNotIn("http://", evidence)
        self.assertNotIn("https://", evidence)


if __name__ == "__main__":
    unittest.main()
