import importlib.util, re, tempfile, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("b",Path(__file__).with_name("generate_banners.py")); b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
ANSI_RE = re.compile("\x1b\\[[0-9;]*m")
class TestKryptonBanners(unittest.TestCase):
 def test_catalog_and_safe_files(self):
  expected={0:"Base64 Decoding",1:"ROT13 Substitution Cipher",2:"Caesar Cipher (Unknown Shift)",3:"Frequency Analysis",4:"Vigenere Cipher (Known Key Length)",5:"Vigenere Cipher (Kasiski Test)",6:"Stream Cipher / LFSR"}
  self.assertEqual(b.TITLES,expected)
  self.assertEqual(set(b.ART),set(range(0,7)))
  with tempfile.TemporaryDirectory() as root:
   b.generate(root); files=list(Path(root).iterdir()); self.assertEqual(len(files),7)
   for level in expected:
    text=(Path(root)/("krypton%d"%level)).read_text("utf-8")
    self.assertIn("Misuse of this system is prohibited",text); self.assertIn("AI or external tools",text); self.assertIn("assigned challenge environment",text)
    # Length limit is on VISIBLE columns, not raw bytes -- ANSI escape
    # codes occupy zero terminal columns, so strip them before measuring
    # (matches render()'s own _visible_len check).
    plain=ANSI_RE.sub("",text)
    self.assertLessEqual(max(map(len,plain.splitlines())),80)
    # Unicode is allowed now; only control chars (which could inject
    # escape sequences of their own) remain forbidden.
    self.assertTrue(all(ord(c)>=0x20 and not(0x7F<=ord(c)<=0x9F) for c in plain.replace("\n"," ")))
   self.assertIn("no next account",(Path(root)/"krypton6").read_text("utf-8"))
 def test_art_is_distinct_per_level(self):
  arts=[tuple(b.ART[level]) for level in range(0,7)]
  self.assertEqual(len(arts),len(set(arts)),"every level's art must be visually distinct")
 def test_art_is_a_storyboard_of_progress(self):
  # Each banner's art is a fixed "establishing shot" frame (the same
  # across the whole track on purpose) plus a transmission strip that
  # shows the signal's actual distance traveled: '-' = distance already
  # crossed, 'o' = the signal's current position (this level), '.' =
  # distance still ahead, unreached. This is what makes each banner
  # genuinely distinct -- and reading the whole set in order tells one
  # continuous story -- without ever hand-inventing (and risking a hint
  # in) a scene per level.
  for level in range(0,7):
   strip=b.ART[level][-2]
   self.assertEqual(strip.count("o"),1,"krypton%d: must show exactly one current position"%level)
   self.assertEqual(len(strip),44,"krypton%d: transmission strip length must stay constant"%level)
  positions=[b.ART[level][-2].index("o") for level in range(0,7)]
  self.assertEqual(positions,sorted(positions),"signal position must move steadily deeper with level")
  self.assertLess(positions[0],positions[-1],"signal must travel further by the final level")
  frames={tuple(b.ART[level][:3]) for level in range(0,7)}
  self.assertEqual(len(frames),1,"the establishing-shot frame must be identical across the track")
 def test_color_is_progressive_and_distinct_per_level(self):
  self.assertEqual(set(b.COLOR),set(range(0,7)))
  colors=[b.COLOR[level] for level in range(0,7)]
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
   for level in range(0,7):
    lines=(Path(root)/("krypton%d"%level)).read_text("utf-8").splitlines()
    for line in lines:
     if line.startswith("Logged in as") or line.startswith("Submit this level") or line.startswith("Final level") or line in b.POLICY:
      self.assertNotIn("\x1b[",line)
 def test_banner_stays_coherent_with_ansi_stripped(self):
  # Simulates a client that does NOT interpret ANSI (e.g. `cat -v`, a
  # dumb log viewer): once escape codes are removed, every banner must
  # still contain its full title, level number, and policy text intact.
  with tempfile.TemporaryDirectory() as root:
   b.generate(root)
   for level in range(0,7):
    raw=(Path(root)/("krypton%d"%level)).read_text("utf-8")
    plain=ANSI_RE.sub("",raw)
    self.assertIn("CEI Labs Krypton %d: %s"%(level,b.TITLES[level]),plain)
    self.assertIn("Logged in as krypton%d"%level,plain)
    for policy_line in b.POLICY:
     self.assertIn(policy_line,plain)
if __name__=="__main__": unittest.main()
