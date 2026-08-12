import os
import unittest
from unittest.mock import patch

import runtime


class SentinelRuntimeContractTests(unittest.TestCase):
    def test_required_secrets_fail_closed(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SystemExit):
                runtime.load_secrets()
        with patch.dict(os.environ, {"LEVEL_SECRETS": "{}"}, clear=True):
            with self.assertRaises(SystemExit):
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

    def test_image_only_exposes_ssh_and_homes_are_not_traversable(self):
        with open("Dockerfile", encoding="utf-8") as source:
            content = source.read()
        self.assertIn("EXPOSE 22", content)
        self.assertNotIn("EXPOSE 80", content)
        self.assertIn('chmod 750 "/home/sentinel${number}"', content)


if __name__ == "__main__":
    unittest.main()
