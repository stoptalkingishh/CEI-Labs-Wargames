import importlib.util, re, tempfile, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("b",Path(__file__).with_name("generate_banners.py")); b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
ANSI_RE = re.compile("\x1b\\[[0-9;]*m")
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
    # Length limit is on VISIBLE columns, not raw bytes -- ANSI escape
    # codes occupy zero terminal columns, so strip them before measuring
    # (matches render()'s own _visible_len check).
    plain=ANSI_RE.sub("",text)
    self.assertLessEqual(max(map(len,plain.splitlines())),80)
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
 def test_color_is_progressive_and_distinct_per_level(self):
  self.assertEqual(set(b.COLOR),set(range(1,7)))
  colors=[b.COLOR[level] for level in range(1,7)]
  self.assertEqual(len(colors),len(set(colors)),"every level's color must be distinct")
  # Basic SGR 8-color codes only (30-37, optionally ";1" bold) -- no
  # 256-color/truecolor, nothing terminal-specific.
  for code in colors:
   self.assertRegex(code,r"^\x1b\[3[0-7](;1)?m$")
 def test_color_never_touches_policy_or_login_lines(self):
  # Color must be a supplement, never load-bearing: the login/submission
  # instructions and the acceptable-use policy must render identically
  # whether or not the client interprets ANSI, so they must carry no
  # escape codes of their own (only the art block above them does).
  with tempfile.TemporaryDirectory() as root:
   b.generate(root)
   for level in range(1,7):
    lines=(Path(root)/("krypton%d"%level)).read_text("ascii").splitlines()
    for line in lines:
     if line.startswith("Logged in as") or line.startswith("Submit this level") or line.startswith("Final level") or line in b.POLICY:
      self.assertNotIn("\x1b[",line)
 def test_banner_stays_coherent_with_ansi_stripped(self):
  # Simulates a client that does NOT interpret ANSI (e.g. `cat -v`, a
  # dumb log viewer): once escape codes are removed, every banner must
  # still contain its full title, level number, and policy text intact.
  with tempfile.TemporaryDirectory() as root:
   b.generate(root)
   for level in range(1,7):
    raw=(Path(root)/("krypton%d"%level)).read_text("ascii")
    plain=ANSI_RE.sub("",raw)
    self.assertIn("CEI Labs Krypton %d: %s"%(level,b.TITLES[level]),plain)
    self.assertIn("Logged in as krypton%d"%level,plain)
    for policy_line in b.POLICY:
     self.assertIn(policy_line,plain)
if __name__=="__main__": unittest.main()
