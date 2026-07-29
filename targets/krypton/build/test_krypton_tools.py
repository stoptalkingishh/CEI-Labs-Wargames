import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace


TOOLS_PATH = Path(__file__).parents[1] / "src" / "krypton_tools.py"
SPEC = importlib.util.spec_from_file_location("krypton_tools", TOOLS_PATH)
TOOLS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOLS)


class KryptonToolsTests(unittest.TestCase):
    def test_columns_ignore_non_letters_like_the_cipher(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ciphertext"
            path.write_text("A B-C!D E?F", encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                TOOLS.columns(SimpleNamespace(length=3, file=str(path)))
        self.assertEqual(output.getvalue().splitlines(), ["1: AD", "2: BE", "3: CF"])

    def test_frequency_combines_files_and_normalizes_case(self):
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "one"
            second = Path(directory) / "two"
            first.write_text("Aa b!", encoding="utf-8")
            second.write_text("bC", encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                TOOLS.frequency(SimpleNamespace(files=[str(first), str(second)]))
        self.assertIn("A     2", output.getvalue())
        self.assertIn("B     2", output.getvalue())
        self.assertIn("C     1", output.getvalue())

    def test_kasiski_reports_repeat_distance_and_gcd(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ciphertext"
            path.write_text("ABCDEFGHIABC", encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                TOOLS.kasiski(SimpleNamespace(file=str(path), min_size=3, max_size=3))
        self.assertIn("ABC positions=0,9 gaps=9", output.getvalue())
        self.assertIn("gcd-of-reported-gaps=9", output.getvalue())
        self.assertIn("candidate-length-support=3:1 9:1", output.getvalue())

    def test_vigenere_key_recovery_and_decryption(self):
        plaintext = (
            "THIS IS A LONG ENGLISH PASSAGE USED TO GIVE FREQUENCY ANALYSIS "
            "ENOUGH LETTERS TO RECOVER A REPEATING CIPHER KEY. "
        ) * 20
        key = "CIPHER"
        shifts = [ord(character) - ord("A") for character in key]
        encrypted = []
        index = 0
        for character in plaintext:
            if character.isalpha():
                encrypted.append(chr((ord(character) - ord("A") + shifts[index % len(key)]) % 26 + ord("A")))
                index += 1
            else:
                encrypted.append(character)
        ciphertext = "".join(encrypted)
        self.assertEqual(TOOLS.recover_vigenere_key(ciphertext, len(key)), key)
        self.assertEqual(TOOLS.decrypt_vigenere(ciphertext, key), plaintext)

    def test_stream_decrypt_uses_known_pair(self):
        with tempfile.TemporaryDirectory() as directory:
            plain = Path(directory) / "known.txt"
            cipher = Path(directory) / "encrypted.txt"
            target = Path(directory) / "target.txt"
            plain.write_text("AAAAAA", encoding="utf-8")
            cipher.write_text("BCDBCD", encoding="utf-8")
            target.write_text("IGOMQZ", encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                TOOLS.stream_decrypt(
                    SimpleNamespace(
                        known_plain=str(plain),
                        known_cipher=str(cipher),
                        target=str(target),
                    )
                )
        self.assertEqual(output.getvalue(), "HELLOW")


if __name__ == "__main__":
    unittest.main()
