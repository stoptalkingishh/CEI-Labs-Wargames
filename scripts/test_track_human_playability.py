import importlib.util
import ast
import sys
import types
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def load(name, path):
    """Load generator declarations without running its file-writing tail."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    declarations = []
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "script_dir" for target in node.targets)
        ):
            break
        declarations.append(node)
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(ast.Module(body=declarations, type_ignores=[]), str(path), "exec"), module.__dict__)
    return module


class HumanPlayabilityContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.natas = load("build_natas_playability", ROOT / "scripts" / "build_natas.py")

    def test_every_natas_hint_is_progressive_and_explains_curl_auth(self):
        for challenge_id, tiers in self.natas.HINTS.items():
            rendered = [
                self.natas._render_hint(challenge_id, index, content)
                for index, content in enumerate(tiers, 1)
            ]
            for index, hint in enumerate(rendered):
                self.assertIn(self.natas.HINT_TITLES[index], hint)
                self.assertIn("Authenticate every curl request", hint)
                self.assertIn(f"natas{int(challenge_id[-2:])}:", hint)

    def test_shell_curl_examples_include_basic_auth(self):
        for challenge_id, tiers in self.natas.HINTS.items():
            for index, content in enumerate(tiers, 1):
                rendered = self.natas._render_hint(challenge_id, index, content)
                command_lines = [
                    line for line in rendered.splitlines() if line.startswith("$ curl ")
                ]
                for line in command_lines:
                    self.assertIn(" -u ", line, (challenge_id, line))

    def test_krypton_level_three_samples_are_generated(self):
        entrypoint = (ROOT / "targets" / "krypton" / "entrypoint.sh").read_text(encoding="utf-8")
        for filename in ("found1", "found2", "found3"):
            self.assertIn(filename, entrypoint)

    def test_krypton_toolkit_is_installed_and_advertised(self):
        dockerfile = (ROOT / "targets" / "krypton" / "Dockerfile").read_text(encoding="utf-8")
        banners = (ROOT / "targets" / "krypton" / "build" / "generate_banners.py").read_text(encoding="utf-8")
        self.assertIn("/usr/local/bin/krypton-tools", dockerfile)
        self.assertIn("krypton-tools --help", banners)

    def test_natas_seven_source_contains_the_missing_lfi_path_hint(self):
        page = (ROOT / "targets" / "natas" / "content" / "natas7" / "index.php").read_text(encoding="utf-8")
        self.assertIn("<!-- hint:", page)
        self.assertIn("/etc/natas_webpass/natas8", page)

    def test_natas_attacker_supplies_late_level_tools(self):
        dockerfile = (ROOT / "targets" / "natas-attacker" / "Dockerfile").read_text(encoding="utf-8")
        for package in ("xxd", "bsdextrautils", "jq", "python3-requests", "file"):
            self.assertIn(package, dockerfile)
        self.assertIn("natas-help", dockerfile)

    def test_natas_hex_hint_uses_valid_hex_and_installed_commands(self):
        hint = self.natas.HINTS["natas-08"][2]
        command = next(line for line in hint.splitlines() if line.startswith("$ echo "))
        encoded = command.split()[2]
        self.assertRegex(encoded, r"^[0-9a-fA-F]+$")
        self.assertEqual(len(encoded) % 2, 0)
        self.assertIn("xxd -r -p | rev | base64 -d", command)

    def test_natas_xor_cookie_hint_uses_exact_json_and_full_helper(self):
        hint = self.natas.HINTS["natas-11"][2]
        self.assertIn('{"showpassword":"no","bgcolor":"#ffffff"}', hint)
        self.assertIn('{"showpassword":"yes","bgcolor":"#ffffff"}', hint)
        self.assertIn("urllib.parse.unquote", hint)
        self.assertIn("urllib.parse.quote", hint)
        self.assertIn("period = next(", hint)
        self.assertNotIn("{ showpassword=no, bgcolor=#ffffff }", hint)


if __name__ == "__main__":
    unittest.main()
