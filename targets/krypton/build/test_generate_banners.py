import importlib.util, tempfile, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("b",Path(__file__).with_name("generate_banners.py")); b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
class TestKryptonBanners(unittest.TestCase):
 def test_catalog_and_safe_files(self):
  expected={1:"ROT13 Substitution Cipher",2:"Caesar Cipher (Unknown Shift)",3:"Frequency Analysis",4:"Vigenere Cipher (Known Key Length)",5:"Vigenere Cipher (Kasiski Test)",6:"Stream Cipher / LFSR"}
  self.assertEqual(b.TITLES,expected)
  with tempfile.TemporaryDirectory() as root:
   b.generate(root); files=list(Path(root).iterdir()); self.assertEqual(len(files),6)
   for level in expected:
    text=(Path(root)/("krypton%d"%level)).read_text("ascii")
    self.assertIn("Misuse of this system is prohibited",text); self.assertIn("AI or external tools",text); self.assertIn("assigned challenge environment",text)
    self.assertLessEqual(max(map(len,text.splitlines())),80)
   self.assertIn("no next account",(Path(root)/"krypton6").read_text("ascii"))
if __name__=="__main__": unittest.main()
