#!/usr/bin/env python3
"""Focused safety tests for Natas's runtime secret materialization."""

import importlib.util
import json
import pathlib
import tempfile
import unittest


TARGET_DIR = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "natas_runtime_secrets", TARGET_DIR / "runtime_secrets.py"
)
RUNTIME_SECRETS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNTIME_SECRETS)


def valid_secrets():
    return {
        key: f"secret-{key}"
        for key in sorted(RUNTIME_SECRETS.REQUIRED_KEYS)
    }


class RuntimeSecretsTests(unittest.TestCase):
    def test_accepts_exact_required_keys_and_adversarial_values(self):
        secrets = valid_secrets()
        adversarial = "quote'\\backslash$dollar<em>&</em>\""
        secrets["natas5"] = adversarial
        secrets["natas6"] = adversarial

        self.assertEqual(
            RUNTIME_SECRETS.load_required_secrets(json.dumps(secrets)), secrets
        )

    def test_rejects_missing_malformed_partial_and_wrong_shaped_values(self):
        partial = valid_secrets()
        del partial["natas34final"]
        wrong_key_set = valid_secrets()
        wrong_key_set["unexpected"] = "secret"
        wrong_shape = valid_secrets()
        wrong_shape["natas1"] = ["secret"]
        empty = valid_secrets()
        empty["natas2"] = ""

        for raw in (
            None,
            "not json",
            json.dumps(partial),
            json.dumps(wrong_key_set),
            json.dumps(["not", "an", "object"]),
            json.dumps(wrong_shape),
            json.dumps(empty),
        ):
            with self.assertRaises(ValueError):
                RUNTIME_SECRETS.load_required_secrets(raw)

    def test_runtime_php_file_base64_serializes_special_characters(self):
        value = "quote'\\backslash$dollar<em>&</em>\""
        with tempfile.TemporaryDirectory() as temporary_directory:
            destination = pathlib.Path(temporary_directory) / "secret.php"
            RUNTIME_SECRETS.write_php_secret(destination, "natas5_secret", value)
            content = destination.read_text(encoding="utf-8")
            self.assertNotIn(value, content)
            self.assertIn("base64_decode", content)

    def test_natas_4_and_5_escape_runtime_values_for_html(self):
        for level, variable in ((4, "natas5_secret"), (5, "natas6_secret")):
            content = (TARGET_DIR / "content" / f"natas{level}" / "index.php").read_text()
            self.assertIn(f"require '/etc/cei-labs/natas-runtime/natas{level}.php'", content)
            self.assertIn(f"htmlspecialchars(${variable}, ENT_QUOTES, 'UTF-8')", content)


if __name__ == "__main__":
    unittest.main()
