import unittest

import answer_service
import runtime


class Sentinel26RuntimeTests(unittest.TestCase):
    def test_static_inventory_supports_the_answer_without_stating_the_disposition(self):
        evidence = runtime.LAB_26_EVIDENCE

        self.assertIn("02:00:00:00:26:01", evidence)
        self.assertIn("no lease for 02:00:00:00:26:01", evidence)
        self.assertIn("engineering permits only registered DHCP endpoints", evidence)
        self.assertIn("Observed zone: engineering", evidence)
        self.assertNotIn("Disposition:", evidence)
        self.assertIn("Do not scan or probe a network", evidence)

    def test_exact_lab_26_answer_is_bound_to_its_account(self):
        answer = {"device_mac": "02:00:00:00:26:01", "zone": "engineering", "disposition": "unauthorized"}
        credentials = {"sentinel-26": "lab-26-credential"}
        submission = {"lab": "sentinel-26", "answer": answer}

        self.assertEqual(runtime.ANSWERS["sentinel-26"], answer)
        self.assertEqual(answer_service.release(submission, "sentinel26", runtime.ANSWERS, credentials), "lab-26-credential")
        with self.assertRaises(SystemExit):
            answer_service.release({"lab": "sentinel-26", "answer": {**answer, "disposition": "authorized"}}, "sentinel26", runtime.ANSWERS, credentials)


if __name__ == "__main__":
    unittest.main()
