import json
import subprocess
import time
import unittest


IMAGE = "sentinel-pilot-security-test:local"
CONTAINER = "sentinel-pilot-security-test"
SECRETS = {
    "sentinel-start-here": "start-secret",
    "sentinel-01": "one-secret",
    "sentinel-02": "two-secret",
    "sentinel-03": "three-secret",
    "sentinel-04": "four-secret",
    "sentinel-05": "five-secret",
}
USERS = {
    "sentinel-start-here": "sentinel0",
    "sentinel-01": "sentinel0",
    "sentinel-02": "sentinel1",
    "sentinel-03": "sentinel2",
    "sentinel-04": "sentinel3",
    "sentinel-05": "sentinel4",
}
ANSWERS = {
    "sentinel-start-here": {"engagement_scope": "local-evidence-only"},
    "sentinel-01": {"asset": "northstar-jump-01", "package": "openssh-server", "service": "sshd", "owner": "root:root"},
    "sentinel-02": {"mfa": "technical-preventive", "badge_review": "physical-preventive", "log_review": "technical-detective"},
    "sentinel-03": {"disposition": "DEFER", "missing_evidence": "change-owner-signature"},
    "sentinel-04": {"service": "ops.northstar.training", "issuer": "Northstar Training Test CA", "revocation_status": "clear", "key_mode": "0400"},
    "sentinel-05": {"listener": "ssh", "port": 22, "legacy_metrics": "disabled"},
}


class SentinelContainerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(["docker", "build", "-t", IMAGE, "."], check=True)
        subprocess.run(["docker", "run", "--rm", "--name", CONTAINER, "-d", "-e", f"LEVEL_SECRETS={json.dumps(SECRETS)}", IMAGE], check=True)
        for _ in range(20):
            if subprocess.run(["docker", "exec", CONTAINER, "test", "-f", "/srv/sentinel-evidence/sentinel0/asset-census.txt"]).returncode == 0:
                return
            time.sleep(0.1)
        raise RuntimeError("Sentinel runtime did not render evidence")

    @classmethod
    def tearDownClass(cls):
        subprocess.run(["docker", "rm", "-f", CONTAINER], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def execute(self, command, **kwargs):
        return subprocess.run(["docker", "exec", CONTAINER, "sh", "-c", command], text=True, capture_output=True, **kwargs)

    def submit(self, user, payload):
        encoded = json.dumps(payload).replace("'", "'\\''")
        return self.execute(f"printf '%s\\n' '{encoded}' | su {user} -s /bin/sh -c sentinel-submit")

    def test_suid_owner_and_private_material(self):
        result = self.execute("stat -c '%a %U:%G' /usr/local/bin/sentinel-submit /opt/sentinel/certs/service.key")
        self.assertEqual(result.stdout.splitlines(), ["4755 root:root", "600 root:root"])
        result = self.execute("su sentinel3 -s /bin/sh -c 'cat /opt/sentinel/certs/service.key'", check=False)
        self.assertNotEqual(result.returncode, 0)
        result = self.execute("su sentinel3 -s /bin/sh -c 'cat ~/evidence/service.key'", check=False)
        self.assertNotEqual(result.returncode, 0)
        result = self.execute("su sentinel0 -s /bin/sh -c 'cat /var/lib/sentinel/credentials.json'", check=False)
        self.assertNotEqual(result.returncode, 0)

    def test_valid_submission_only_releases_its_credential_and_rejects_adjacent(self):
        for lab, answer in ANSWERS.items():
            user = USERS[lab]
            result = self.submit(user, {"lab": lab, "answer": answer})
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), SECRETS[lab])
            adjacent = f"sentinel{(int(user[-1]) + 1) % 6}"
            rejected = self.submit(adjacent, {"lab": lab, "answer": answer})
            self.assertNotEqual(rejected.returncode, 0, lab)
            self.assertEqual(rejected.stdout, "")

    def test_sanitized_execution_and_bad_input(self):
        payload = {"lab": "sentinel-01", "answer": ANSWERS["sentinel-01"]}
        encoded = json.dumps(payload).replace("'", "'\\''")
        result = self.execute(f"printf '%s\\n' '{encoded}' | su sentinel0 -s /bin/sh -c 'env -i PATH=/tmp /usr/local/bin/sentinel-submit'")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), SECRETS["sentinel-01"])
        result = self.submit("sentinel4", {"lab": "sentinel-05", "answer": {**ANSWERS["sentinel-05"], "port": 22.0}})
        self.assertNotEqual(result.returncode, 0)
        result = self.execute("yes x | head -c 65537 | su sentinel0 -s /bin/sh -c sentinel-submit", check=False)
        self.assertNotEqual(result.returncode, 0)

    def test_restart_does_not_follow_learner_home_symlink(self):
        result = self.execute("su sentinel0 -s /bin/sh -c 'printf untouched > /tmp/sentinel-attack; ln -sf /tmp/sentinel-attack /home/sentinel0/asset-census.txt'", check=True)
        self.assertEqual(result.returncode, 0)
        subprocess.run(["docker", "restart", CONTAINER], check=True, stdout=subprocess.DEVNULL)
        result = self.execute("cat /tmp/sentinel-attack")
        self.assertEqual(result.stdout, "untouched")
        result = self.execute("su sentinel0 -s /bin/sh -c 'cat /home/sentinel0/evidence/asset-census.txt'")
        self.assertIn("Asset inventory: northstar-jump-01", result.stdout)

    def test_learner_evidence_is_readable(self):
        result = self.execute("su sentinel1 -s /bin/sh -c 'cat /home/sentinel1/evidence/controls.md'")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("MFA: technical preventive", result.stdout)


if __name__ == "__main__":
    unittest.main()
