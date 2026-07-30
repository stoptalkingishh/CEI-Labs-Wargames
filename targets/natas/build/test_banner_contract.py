import importlib.util, tempfile, unittest, re
from pathlib import Path
ROOT=Path(__file__).parents[1]
spec=importlib.util.spec_from_file_location("b",ROOT/"build"/"generate_banners.py"); b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
class NatasBannerContract(unittest.TestCase):
 def test_outputs_are_safe_and_complete(self):
  self.assertEqual(set(b.T),set(range(15)))
  self.assertEqual(set(b.ART),set(range(15)))
  with tempfile.TemporaryDirectory() as root:
   b.main(root); files=list(Path(root).glob("*.html")); self.assertEqual(len(files),15)
   for f in files:
    text=f.read_text("ascii"); self.assertIn('<pre class="cei-login-banner">',text); self.assertNotIn("<script",text.lower()); self.assertIsNone(re.search(r"\son\w+\s*=",text,re.I)); self.assertIn("Misuse of this system is prohibited",text); self.assertIn("AI or external tools",text); self.assertIn("assigned challenge environment",text)
 def test_art_is_distinct_and_safe(self):
  arts=[tuple(b.ART[n]) for n in range(15)]
  self.assertEqual(len(arts),len(set(arts)),"every level's art must be visually distinct")
  for n,lines in b.ART.items():
   for line in lines:
    self.assertTrue(all(ord(c)<128 for c in line))
    self.assertLessEqual(len(line),80)
 def test_art_precedes_title_in_rendered_banner(self):
  # The art must actually be wired into the rendered banner (not just
  # defined and unused), and appear before the title/policy text.
  for n,title in b.T.items():
   rendered=b.render(n,title)
   art_text="\n".join(b.ART[n])
   self.assertIn(art_text,rendered)
   self.assertLess(rendered.index(art_text),rendered.index("CEI Labs Natas"))
 def test_server_wiring_contract(self):
  php=(ROOT/"build"/"cei-natas-banner.php").read_text(); vhost=(ROOT/"build"/"03-generate-vhosts.py").read_text(); docker=(ROOT/"Dockerfile").read_text()
  for token in ("$port < 8000 || $port > 8014","/etc/cei-labs/natas-banners","Content-Disposition","text/html","preg_match","static $done") : self.assertIn(token,php)
  self.assertEqual(vhost.count("php_admin_value auto_prepend_file /opt/cei-natas-banner.php"),1); self.assertIn("range(15)",vhost)
  self.assertIn("/etc/cei-labs/natas-banners",docker); self.assertIn("/opt/cei-natas-banner.php",docker); self.assertIn("chmod 444",docker)
if __name__=="__main__": unittest.main()
