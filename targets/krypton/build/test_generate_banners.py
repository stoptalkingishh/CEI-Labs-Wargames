import importlib.util, tempfile, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("b",Path(__file__).with_name("generate_banners.py")); b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
class TestKryptonBanners(unittest.TestCase):
 def test_catalog_and_safe_files(self):
  expected={1:"ROT13 Substitution Cipher",2:"Caesar Cipher (Unknown Shift)",3:"Frequency Analysis",4:"Vigenere Cipher (Known Key Length)",5:"Vigenere Cipher (Kasiski Test)",6:"Stream Cipher / LFSR"}
  self.assertEqual(b.TITLES,expected)
  self.assertEqual(set(b.ART),set(range(1,7)))
  with tempfile.TemporaryDirectory() as root:
   b.generate(root); files=list(Path(root).iterdir()); self.assertEqual(len(files),6)
   for level in expected:
    text=(Path(root)/("krypton%d"%level)).read_text("ascii")
    self.assertIn("Misuse of this system is prohibited",text); self.assertIn("AI or external tools",text); self.assertIn("assigned challenge environment",text)
    self.assertLessEqual(max(map(len,text.splitlines())),80)
    self.assertTrue(all(ord(c)<128 for c in text))
   self.assertIn("no next account",(Path(root)/"krypton6").read_text("ascii"))
 def test_art_is_distinct_per_level(self):
  arts=[tuple(b.ART[level]) for level in range(1,7)]
  self.assertEqual(len(arts),len(set(arts)),"every level's art must be visually distinct")
 def test_art_is_thematically_relevant(self):
  # spot-check a few levels for a keyword tying the art to its actual title
  self.assertTrue(any("shift" in line.lower() or "13" in line for line in b.ART[1]))
  self.assertTrue(any("shift" in line.lower() or "?" in line for line in b.ART[2]))
  self.assertTrue(any("e" in line.lower() and "t" in line.lower() for line in b.ART[3]))
  self.assertTrue(any("key" in line.lower() for line in b.ART[4]))
  self.assertTrue(any("key" in line.lower() for line in b.ART[5]))
  self.assertTrue(any("xor" in line.lower() or "1" in line or "0" in line for line in b.ART[6]))
if __name__=="__main__": unittest.main()
