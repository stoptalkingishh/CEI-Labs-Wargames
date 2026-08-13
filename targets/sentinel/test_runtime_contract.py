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

    def test_files_are_private_to_the_intended_account(self):
        calls = []
        with patch("runtime.open", create=True) as opened, patch("runtime.subprocess.run", side_effect=lambda command, **kwargs: calls.append(command)), patch("runtime.os.chmod") as chmod:
            runtime.write("sentinel1", "asset-census.txt", "evidence")
        self.assertIn(["chown", "sentinel1:sentinel1", "/home/sentinel1/asset-census.txt"], calls)
        chmod.assert_called_once_with("/home/sentinel1/asset-census.txt", 0o400)

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
        }
        credentials = {lab: f"{lab}-credential" for lab in runtime.ANSWERS}
        self.assertEqual(answer_service.LAB_USERS, expected_users)
        for lab, caller in expected_users.items():
            submission = {"lab": lab, "answer": runtime.ANSWERS[lab]}
            self.assertEqual(answer_service.release(submission, caller, runtime.ANSWERS, credentials), credentials[lab])
            adjacent = f"sentinel{(int(caller[-1]) + 1) % 6}"
            with self.assertRaises(SystemExit, msg=lab):
                answer_service.release(submission, adjacent, runtime.ANSWERS, credentials)

    def test_invalid_answer_releases_nothing(self):
        submission = {"lab": "sentinel-01", "answer": {"asset": "wrong"}}
        with self.assertRaises(SystemExit):
            answer_service.release(submission, "sentinel0", runtime.ANSWERS, {"sentinel-01": "team-secret"})

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
        self.assertIn('os.chmod("/home/sentinel3/service.key", 0o400)', runtime_source)

    def test_evidence_locations_follow_password_progression(self):
        with open("runtime.py", encoding="utf-8") as source:
            content = source.read()
        self.assertIn('write("sentinel0", "asset-census.txt"', content)
        self.assertIn('write("sentinel1", "control-evidence.md"', content)
        self.assertIn('write("sentinel2", "change-window.txt"', content)
        self.assertIn('write("sentinel3", "certificate-ledger.txt"', content)
        self.assertIn('write("sentinel4", "exposure-review.conf"', content)

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


if __name__ == "__main__":
    unittest.main()
