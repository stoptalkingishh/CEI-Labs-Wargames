import json
import subprocess
import time
import unittest


IMAGE = "sentinel-pilot-security-test:local"
CONTAINER = "sentinel-pilot-security-test"
# Worst-case wait for the entrypoint to finish rendering. The entrypoint runs
# runtime.py and only then `exec`s sshd, so sshd being up is the real
# "container is ready" signal; the poll normally returns in a few seconds and
# this bound is only ever reached on genuine failure.
READY_TIMEOUT = 60.0
# asset-census.txt is only the third of the ~25 files runtime.py writes, so it
# proves far less than it looks like. Pair it with sshd so the whole of
# runtime.py has finished before any test execs into the container. Polling
# happens inside the container (one host process, not one per attempt) so the
# wait itself costs no measurable wall time.
READY_PROBE = "until test -f /srv/sentinel-evidence/sentinel0/asset-census.txt && pgrep -x sshd >/dev/null; do sleep 0.2; done"
SECRETS = {
    "sentinel-start-here": "start-secret",
    "sentinel-01": "one-secret",
    "sentinel-02": "two-secret",
    "sentinel-03": "three-secret",
    "sentinel-04": "four-secret",
    "sentinel-05": "five-secret",
    "sentinel-22": "twenty-two-secret",
    "sentinel-23": "twenty-three-secret",
    "sentinel-24": "twenty-four-secret",
    "sentinel-25": "twenty-five-secret",
    "sentinel-26": "twenty-six-secret",
    "sentinel-27": "twenty-seven-secret",
}
USERS = {
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
ANSWERS = {
    "sentinel-start-here": {"engagement_scope": "local-evidence-only"},
    "sentinel-01": {"asset": "northstar-jump-01", "package": "openssh-server", "service": "sshd", "owner": "root:root"},
    "sentinel-02": {"mfa": "technical-preventive", "badge_review": "physical-preventive", "log_review": "technical-detective"},
    "sentinel-03": {"disposition": "DEFER", "missing_evidence": "change-owner-signature"},
    "sentinel-04": {"service": "ops.northstar.training", "issuer": "Northstar Training Test CA", "revocation_status": "clear", "key_mode": "0400"},
    "sentinel-05": {"listener": "ssh", "port": 22, "legacy_metrics": "disabled"},
    "sentinel-22": {"from_domain": "northstar.training", "return_path_domain": "invoice-notice.example", "dmarc": "fail"},
    "sentinel-23": {"rule_id": "NS-DET-104", "matches": 1, "decision": "triggered"},
    "sentinel-24": {"endpoint_id": "northstar-lt-042", "enrollment_record_id": "ENR-24-042", "enrollment_status": "enrolled", "key_status": "active"},
    "sentinel-25": {"alert_id": "ALT-2048", "root_cause": "expired-vpn-certificate", "disposition": "close-benign"},
    "sentinel-26": {"device_mac": "02:00:00:00:26:01", "zone": "engineering", "disposition": "unauthorized"},
    "sentinel-27": {"filename": "field-notes.pdf", "sha256": "dc3014d5c2f708b7e4628082170c3c0385afbd6dd8d84f1aff0eca6d8abe7710", "extracted_author": "Northstar Training"},
}


class SentinelContainerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # The container name is fixed, so a container left behind by an
        # interrupted run (cancelled job, killed runner) would make `docker
        # run` exit 125 with a name conflict. Clear it up front rather than
        # trusting cleanup that a cancellation never reaches.
        cls.remove_container()
        subprocess.run(["docker", "build", "-t", IMAGE, "."], check=True)
        subprocess.run(["docker", "run", "--rm", "--name", CONTAINER, "-d", "-e", f"LEVEL_SECRETS={json.dumps(SECRETS)}", IMAGE], check=True)
        cls.wait_until_ready("initial container start")

    @classmethod
    def remove_container(cls):
        subprocess.run(["docker", "rm", "-f", CONTAINER], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

    @classmethod
    def wait_until_ready(cls, context):
        """Block until the entrypoint has finished rendering evidence.

        On timeout, raise with the container's own output attached: a bare
        "did not render evidence" gives no way to tell a slow start from a
        crashed runtime.
        """
        deadline = time.monotonic() + READY_TIMEOUT
        while True:
            probe = subprocess.run(["docker", "exec", CONTAINER, "sh", "-c", READY_PROBE], text=True, capture_output=True, check=False)
            if probe.returncode == 0:
                return
            state = cls.inspect_state()
            if not state.get("Running"):
                raise RuntimeError(f"Sentinel container exited during {context} (status {state.get('Status')}, exit code {state.get('ExitCode')}).\n{cls.container_logs()}")
            if time.monotonic() >= deadline:
                raise RuntimeError(
                    f"Sentinel container did not become ready within {READY_TIMEOUT:.0f}s during {context}. "
                    f"Waiting for: {READY_PROBE}\n"
                    f"Container state: {state}\n"
                    f"Container logs:\n{cls.container_logs()}"
                )
            time.sleep(0.2)

    @classmethod
    def inspect_state(cls):
        inspected = subprocess.run(["docker", "inspect", "-f", "{{.State.Status}} {{.State.Running}} {{.State.ExitCode}}", CONTAINER], text=True, capture_output=True, check=False)
        fields = inspected.stdout.split()
        if len(fields) != 3:
            return {"Status": "unknown", "Running": True, "ExitCode": "unknown", "inspect": inspected.stderr.strip()}
        return {"Status": fields[0], "Running": fields[1] == "true", "ExitCode": fields[2]}

    @classmethod
    def container_logs(cls):
        logs = subprocess.run(["docker", "logs", CONTAINER], text=True, capture_output=True, check=False)
        output = (logs.stdout + logs.stderr).strip()
        return output or "<container produced no output>"

    @classmethod
    def tearDownClass(cls):
        cls.remove_container()

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
            adjacent = "sentinel0" if user != "sentinel0" else "sentinel1"
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
        # `docker restart` returns as soon as the container is up, which is
        # before the entrypoint has re-rendered anything. Reading evidence here
        # without waiting races the same way setUpClass used to.
        self.wait_until_ready("container restart")
        result = self.execute("cat /tmp/sentinel-attack")
        self.assertEqual(result.stdout, "untouched")
        result = self.execute("su sentinel0 -s /bin/sh -c 'cat /home/sentinel0/evidence/asset-census.txt'")
        self.assertIn("Asset inventory: northstar-jump-01", result.stdout)

    def test_learner_evidence_is_readable(self):
        result = self.execute("su sentinel1 -s /bin/sh -c 'cat /home/sentinel1/evidence/controls.md'")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("MFA: technical preventive", result.stdout)

    def test_expansion_evidence_is_static_and_readable_by_its_account(self):
        result = self.execute("su sentinel22 -s /bin/sh -c 'cat ~/evidence/phishing-message.eml'")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("dmarc=fail", result.stdout)
        result = self.execute("su sentinel27 -s /bin/sh -c 'cat ~/evidence/evidence-metadata.txt'")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Original static local document fixture", result.stdout)
        result = self.execute("su sentinel27 -s /bin/sh -c 'test -f ~/evidence/field-notes.pdf'")
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.execute("su sentinel27 -s /bin/sh -c 'sha256sum ~/evidence/field-notes.pdf'")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.startswith(ANSWERS["sentinel-27"]["sha256"]))


if __name__ == "__main__":
    unittest.main()
