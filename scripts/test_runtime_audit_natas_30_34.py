import importlib.util
import json
import pathlib
import unittest

spec = importlib.util.spec_from_file_location("audit", pathlib.Path(__file__).with_name("runtime_audit_natas_30_34.py"))
audit = importlib.util.module_from_spec(spec); spec.loader.exec_module(audit)


class BatchDAuditTests(unittest.TestCase):
    def test_loopback_and_complete_secret_chain_are_required(self):
        secrets = {"natas%d" % n: "test-%d" % n for n in range(30, 35)}; secrets["natas34final"] = "terminal"
        self.assertEqual(audit.parse_secrets(json.dumps(secrets)), secrets)
        with self.assertRaises(AssertionError): audit.local_url("http://example.test:18000")
        with self.assertRaises(AssertionError): audit.parse_secrets("{}")
