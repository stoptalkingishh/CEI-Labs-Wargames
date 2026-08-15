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

import answer_service
import build_sentinel


class EndpointEnrollmentEvidenceTests(unittest.TestCase):
    def test_generator_requires_the_shared_enrollment_record_id(self):
        challenge = next(item for item in build_sentinel.challenges_data if item["id"] == "sentinel-24")
        hints = build_sentinel.HINTS["sentinel-24"]

        self.assertIn("enrollment record", challenge["goal"])
        self.assertIn("enrollment record ID", challenge["task"])
        self.assertIn("enrollment record ID", hints[0])
        self.assertIn("enrollment_record_id", hints[2])

        with tempfile.TemporaryDirectory() as directory:
            build_sentinel.build(directory)
            challenge_yaml = Path(directory, "sentinel-24", "challenge.yml").read_text(encoding="utf-8")
        self.assertIn("enrollment record ID", challenge_yaml)

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
            if call.args[0] == "sentinel24"
        }
        enrollment = evidence["endpoint-enrollment.txt"]

        self.assertEqual(enrollment.count("Enrollment record ID: ENR-24-042"), 3)
        self.assertIn("Endpoint inventory ID: northstar-lt-042", enrollment)
        self.assertIn("Enrollment transcript: accepted", enrollment)
        self.assertIn("Enrollment key status: active", enrollment)
        self.assertIn("Do not contact an endpoint, agent, or manager.", enrollment)
        self.assertNotIn("http://", enrollment)
        self.assertNotIn("https://", enrollment)
        self.assertEqual(
            runtime.ANSWERS["sentinel-24"],
            {
                "endpoint_id": "northstar-lt-042",
                "enrollment_record_id": "ENR-24-042",
                "enrollment_status": "enrolled",
                "key_status": "active",
            },
        )

    def test_answer_rejects_an_omitted_enrollment_record_id(self):
        credentials = {"sentinel-24": "lab-24-credential"}
        submission = {"lab": "sentinel-24", "answer": runtime.ANSWERS["sentinel-24"]}
        self.assertEqual(
            answer_service.release(submission, "sentinel24", runtime.ANSWERS, credentials),
            "lab-24-credential",
        )

        incomplete = {
            "lab": "sentinel-24",
            "answer": {key: value for key, value in runtime.ANSWERS["sentinel-24"].items() if key != "enrollment_record_id"},
        }
        with self.assertRaises(SystemExit):
            answer_service.release(incomplete, "sentinel24", runtime.ANSWERS, credentials)


if __name__ == "__main__":
    unittest.main()
