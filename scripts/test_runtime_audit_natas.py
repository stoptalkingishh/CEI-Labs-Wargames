import importlib.util
import pathlib
import unittest

spec = importlib.util.spec_from_file_location(
    "runtime_audit_natas", pathlib.Path(__file__).with_name("runtime_audit_natas.py")
)
runtime_audit_natas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime_audit_natas)
NatasAudit = runtime_audit_natas.NatasAudit
local_base_url = runtime_audit_natas.local_base_url
parse_secrets = runtime_audit_natas.parse_secrets


def secrets():
    return {**{f"natas{level}": f"synthetic-{level}" for level in range(1, 35)}, "natas14final": "synthetic-final"}


class RuntimeAuditNatasTests(unittest.TestCase):
    def test_parse_secrets_requires_complete_synthetic_chain(self):
        parsed = parse_secrets(__import__("json").dumps(secrets()))
        self.assertEqual(parsed["natas14final"], "synthetic-final")
        with self.assertRaisesRegex(AssertionError, "natas1"):
            parse_secrets("{}")

    def test_local_base_url_rejects_remote_and_paths(self):
        self.assertEqual(local_base_url("http://127.0.0.1:18000/"), "http://127.0.0.1:18000")
        for value in ("https://127.0.0.1:18000", "http://example.com:18000", "http://127.0.0.1:18000/natas"):
            with self.assertRaises(AssertionError):
                local_base_url(value)

    def test_url_uses_one_port_per_level(self):
        audit = NatasAudit("http://localhost:18000", secrets())
        self.assertEqual(audit.url(6, "/?source"), "http://localhost:18006/?source")


if __name__ == "__main__":
    unittest.main()
