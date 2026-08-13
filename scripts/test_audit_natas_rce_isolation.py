import importlib.util
import pathlib
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("audit", pathlib.Path(__file__).with_name("audit_natas_rce_isolation.py"))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class RceIsolationPortTests(unittest.TestCase):
    def test_discovers_only_the_two_explicitly_published_ports(self):
        ports = {"%d/tcp" % port: None for port in range(8000, 8035)}
        ports["8012/tcp"] = [{"HostPort": "40112"}]
        ports["8013/tcp"] = [{"HostPort": "40113"}]
        with patch.object(audit, "run", return_value=type("Result", (), {"stdout": __import__("json").dumps(ports)})()):
            self.assertEqual(audit.published_ports(), {12: 40112, 13: 40113})

    def test_rejects_a_missing_required_published_port(self):
        with patch.object(audit, "run", return_value=type("Result", (), {"stdout": "{}"})()):
            with self.assertRaisesRegex(RuntimeError, "level 12"):
                audit.published_ports()
