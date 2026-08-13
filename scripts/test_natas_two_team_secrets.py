"""Verify two independently generated Natas secret sets cannot overlap."""
import unittest

from runtime_audit_natas import parse_secrets


class TwoTeamSecretTests(unittest.TestCase):
    def test_two_team_materials_are_unique(self):
        first = {"natas%d" % level: "alpha-%d" % level for level in range(1, 35)}
        second = {"natas%d" % level: "bravo-%d" % level for level in range(1, 35)}
        first["natas34final"] = "alpha-terminal"
        second["natas34final"] = "bravo-terminal"
        import json
        first, second = parse_secrets(json.dumps(first)), parse_secrets(json.dumps(second))
        self.assertTrue(set(first.values()).isdisjoint(second.values()))
