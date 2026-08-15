import os
from pathlib import Path
import unittest
from unittest.mock import patch

import answer_service
import runtime


class SentinelRuntimeContractTests(unittest.TestCase):
    def test_required_secrets_fail_closed(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SystemExit):
                runtime.load_secrets()
        with patch.dict(os.environ, {"LEVEL_SECRETS": "{}"}, clear=True):
            with self.assertRaises(SystemExit):
                runtime.load_secrets()
        with patch.dict(os.environ, {"LEVEL_SECRETS": "[]"}, clear=True):
            with self.assertRaisesRegex(SystemExit, "JSON object"):
                runtime.load_secrets()

    def test_derivation_is_stable_and_team_specific(self):
        self.assertEqual(runtime.derived("team-a", "asset"), runtime.derived("team-a", "asset"))
        self.assertNotEqual(runtime.derived("team-a", "asset"), runtime.derived("team-b", "asset"))
        self.assertNotEqual(runtime.derived("team-a", "asset"), runtime.derived("team-a", "control"))

    def test_credential_accounts_do_not_assume_sequential_lab_numbers(self):
        self.assertEqual(runtime.ACCOUNT_CREDENTIAL_KEYS["sentinel22"], "sentinel-22")
        self.assertEqual(runtime.ACCOUNT_CREDENTIAL_KEYS["sentinel27"], "sentinel-27")
        self.assertNotIn("sentinel6", runtime.ACCOUNT_CREDENTIAL_KEYS)

    def test_files_are_private_to_the_intended_account(self):
        with patch("runtime.write_atomic") as write_atomic:
            runtime.write("sentinel1", "asset-census.txt", "evidence")
        write_atomic.assert_called_once_with("/srv/sentinel-evidence/sentinel1", "asset-census.txt", "evidence", 0o444)

    def test_entrypoint_scrubs_before_sshd(self):
        with open("entrypoint.sh", encoding="utf-8") as source:
            content = source.read()
        self.assertLess(content.index("unset LEVEL_SECRETS"), content.index("exec /usr/sbin/sshd"))

    def test_valid_answer_releases_only_its_credential(self):
        submission = {"lab": "sentinel-01", "answer": runtime.ANSWERS["sentinel-01"]}
        self.assertEqual(answer_service.release(submission, "sentinel0", runtime.ANSWERS, {"sentinel-01": "team-secret"}), "team-secret")

    def test_each_submission_is_bound_to_its_progression_account(self):
        expected_users = {
            "sentinel-start-here": "sentinel0",
            "sentinel-01": "sentinel0",
            "sentinel-02": "sentinel1",
            "sentinel-03": "sentinel2",
            "sentinel-04": "sentinel3",
            "sentinel-05": "sentinel4",
            "sentinel-22": "sentinel22",
            "sentinel-23": "sentinel23",
            "sentinel-24": "sentinel24",
            "sentinel-25": "sentinel25",
            "sentinel-26": "sentinel26",
            "sentinel-27": "sentinel27",
        }
        credentials = {lab: f"{lab}-credential" for lab in runtime.ANSWERS}
        self.assertEqual(answer_service.LAB_USERS, expected_users)
        for lab, caller in expected_users.items():
            submission = {"lab": lab, "answer": runtime.ANSWERS[lab]}
            self.assertEqual(answer_service.release(submission, caller, runtime.ANSWERS, credentials), credentials[lab])
            adjacent = "sentinel0" if caller != "sentinel0" else "sentinel1"
            with self.assertRaises(SystemExit, msg=lab):
                answer_service.release(submission, adjacent, runtime.ANSWERS, credentials)

    def test_invalid_answer_releases_nothing(self):
        submission = {"lab": "sentinel-01", "answer": {"asset": "wrong"}}
        with self.assertRaises(SystemExit):
            answer_service.release(submission, "sentinel0", runtime.ANSWERS, {"sentinel-01": "team-secret"})

    def test_answer_requires_exact_json_scalar_types(self):
        submission = {"lab": "sentinel-05", "answer": {**runtime.ANSWERS["sentinel-05"], "port": 22.0}}
        with self.assertRaises(SystemExit):
            answer_service.release(submission, "sentinel4", runtime.ANSWERS, {"sentinel-05": "team-secret"})
        submission["answer"]["port"] = "22"
        with self.assertRaises(SystemExit):
            answer_service.release(submission, "sentinel4", runtime.ANSWERS, {"sentinel-05": "team-secret"})
        submission["answer"]["port"] = [22]
        with self.assertRaises(SystemExit):
            answer_service.release(submission, "sentinel4", runtime.ANSWERS, {"sentinel-05": "team-secret"})

    def test_submission_size_is_bounded(self):
        self.assertEqual(answer_service.MAX_SUBMISSION_BYTES, 65536)

    def test_learner_evidence_has_no_credential_values(self):
        with open("runtime.py", encoding="utf-8") as source:
            content = source.read()
        self.assertNotIn('" + secrets[', content)

    def test_lab04_uses_static_offline_certificate_evidence(self):
        with open("Dockerfile", encoding="utf-8") as source:
            dockerfile = source.read()
        with open("runtime.py", encoding="utf-8") as source:
            runtime_source = source.read()
        self.assertIn("COPY certs /opt/sentinel/certs", dockerfile)
        self.assertNotIn("openssl req", dockerfile)
        self.assertIn("-attime 1893456000", runtime_source)
        self.assertIn("-CRLfile training-ca.crl -crl_check", runtime_source)
        self.assertIn('write("sentinel3", "service.key", source.read(), 0o400)', runtime_source)

    def test_evidence_locations_follow_password_progression(self):
        with open("runtime.py", encoding="utf-8") as source:
            content = source.read()
        self.assertIn('write("sentinel0", "asset-census.txt"', content)
        self.assertIn('write("sentinel1", "control-evidence.md"', content)
        self.assertIn('write("sentinel2", "change-window.txt"', content)
        self.assertIn('write("sentinel3", "certificate-ledger.txt"', content)
        self.assertIn('write("sentinel4", "exposure-review.conf"', content)
        self.assertIn('write("sentinel22", "phishing-message.eml"', content)
        self.assertIn('write("sentinel23", "decision-record.txt"', content)
        self.assertIn('write("sentinel24", "endpoint-enrollment.txt"', content)
        self.assertIn('write("sentinel25", "alert-triage-summary.txt"', content)
        self.assertIn('write("sentinel26", "network-inventory.txt"', content)
        self.assertIn('write("sentinel27", "evidence-metadata.txt"', content)
        self.assertIn('write("sentinel27", "field-notes.pdf"', content)
        self.assertNotIn('"/home/{owner}/{name}"', content)

    def test_expansion_evidence_is_static_and_contains_no_credentials(self):
        with open("runtime.py", encoding="utf-8") as source:
            content = source.read()
        expansion = content[content.index('write("sentinel22"'):]
        self.assertIn("Static", expansion)
        self.assertNotIn("secrets[", expansion)
        self.assertNotIn("http://", expansion)
        self.assertNotIn("https://", expansion)
        self.assertIn("/opt/sentinel/fixtures/field-notes.pdf", expansion)

    def test_lab01_contract_does_not_require_systemctl(self):
        builder = Path(__file__).resolve().parents[2] / "scripts" / "build_sentinel.py"
        with open(builder, encoding="utf-8") as source:
            self.assertNotIn("systemctl", source.read())

    def test_image_only_exposes_ssh_and_homes_are_not_traversable(self):
        with open("Dockerfile", encoding="utf-8") as source:
            content = source.read()
        self.assertIn("EXPOSE 22", content)
        self.assertNotIn("EXPOSE 80", content)
        self.assertIn('chmod 750 "/home/sentinel${number}"', content)
        for number in range(22, 28):
            self.assertIn(str(number), content)


if __name__ == "__main__":
    unittest.main()
