import importlib.util
import json
import pathlib
import unittest

spec = importlib.util.spec_from_file_location("audit", pathlib.Path(__file__).with_name("runtime_audit_natas_25_29.py"))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class BatchCAuditTests(unittest.TestCase):
    def test_local_target_and_adjacent_secrets_are_required(self):
        secrets = {"natas%d" % n: "test-%d" % n for n in range(25, 31)}
        self.assertEqual(audit.parse_secrets(json.dumps(secrets)), secrets)
        self.assertEqual(audit.local_url("http://127.0.0.1:18000/"), "http://127.0.0.1:18000")
        with self.assertRaises(AssertionError): audit.local_url("http://example.test:18000")
        with self.assertRaises(AssertionError): audit.parse_secrets("{}")
