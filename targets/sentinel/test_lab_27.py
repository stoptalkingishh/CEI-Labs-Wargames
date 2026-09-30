import hashlib
import unittest

import answer_service
import runtime


class SentinelLab27Tests(unittest.TestCase):
    def test_answer_digest_matches_the_committed_fixture(self):
        digest = hashlib.sha256(runtime.LAB27_FIXTURE.read_bytes()).hexdigest()
        self.assertEqual(runtime.ANSWERS["sentinel-27"]["filename"], "field-notes.pdf")
        self.assertEqual(runtime.ANSWERS["sentinel-27"]["sha256"], digest)
        self.assertEqual(runtime.ANSWERS["sentinel-27"]["extracted_author"], "Northstar Training")

    def test_metadata_evidence_supports_an_offline_checksum_review(self):
        evidence = runtime.lab27_metadata_evidence()
        self.assertIn(runtime.ANSWERS["sentinel-27"]["sha256"], evidence)
        self.assertIn("Metadata author: Northstar Training", evidence)
        self.assertIn("sha256sum field-notes.pdf", evidence)
        self.assertNotIn("http://", evidence)
        self.assertNotIn("https://", evidence)

    def test_fixture_author_and_submission_contract_are_bound(self):
        fixture = runtime.LAB27_FIXTURE.read_bytes()
        self.assertIn(b"/Author (Northstar Training)", fixture)
        credentials = {"sentinel-27": "next-lab-credential"}
        submission = {"lab": "sentinel-27", "answer": runtime.ANSWERS["sentinel-27"]}
        self.assertEqual(answer_service.release(submission, "sentinel27", runtime.ANSWERS, credentials), "next-lab-credential")
        submission["answer"] = {**submission["answer"], "sha256": "0" * 64}
        with self.assertRaises(SystemExit):
            answer_service.release(submission, "sentinel27", runtime.ANSWERS, credentials)


if __name__ == "__main__":
    unittest.main()
