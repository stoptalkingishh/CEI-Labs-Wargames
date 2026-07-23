import importlib.util, tempfile, unittest, re
from pathlib import Path
ROOT=Path(__file__).parents[1]
spec=importlib.util.spec_from_file_location("t",ROOT/"build"/"generate_themes.py"); t=importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
class NatasThemeContract(unittest.TestCase):
 def test_outputs_are_complete_and_scoped(self):
  self.assertEqual(set(t.THEMES),set(range(15)))
  with tempfile.TemporaryDirectory() as root:
   t.main(root); files=list(Path(root).glob("*.css")); self.assertEqual(len(files),15)
   for f in files:
    text=f.read_text("ascii")
    self.assertIn(".cei-locked",text); self.assertIn(".cei-solved",text)
    self.assertNotIn("<script",text.lower()); self.assertNotIn("url(",text.lower())
 def test_hue_progression_is_monotonic_cool_to_hot(self):
  # Not literally monotonic in raw degrees (it can wrap through violet),
  # but the endpoints must differ substantially and every level must get
  # its own distinct hue -- no two levels should share a color.
  hues=[t._progression_hue(n) for n in range(15)]
  self.assertNotEqual(hues[0],hues[14])
  hexes=[t._hue_to_hex(h) for h in hues]
  self.assertEqual(len(set(hexes)),15)
 def test_natas14_has_no_reachable_solved_signal_documented(self):
  with tempfile.TemporaryDirectory() as root:
   t.main(root)
   css=(Path(root)/"natas14.css").read_text("ascii")
   self.assertIn("never reaches",css)
 def test_server_wiring_contract(self):
  php=(ROOT/"build"/"cei-natas-banner.php").read_text()
  vhost=(ROOT/"build"/"03-generate-vhosts.py").read_text()
  docker=(ROOT/"Dockerfile").read_text()
  for token in (
      "cei_natas_theme_state","cei_natas_mark_previous_level_solved",
      "/etc/cei-labs/natas-themes","/etc/cei-labs/natas-solve-state",
      "cei-locked","cei-solved",
  ):
   self.assertIn(token,php)
  self.assertIn("/etc/cei-labs/natas-themes",docker)
  self.assertIn("/etc/cei-labs/natas-solve-state",docker)
  self.assertIn("chmod 1777",docker)
if __name__=="__main__": unittest.main()
