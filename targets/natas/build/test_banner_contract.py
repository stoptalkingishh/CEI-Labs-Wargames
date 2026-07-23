import importlib.util, tempfile, unittest, re
from pathlib import Path
ROOT=Path(__file__).parents[1]
spec=importlib.util.spec_from_file_location("b",ROOT/"build"/"generate_banners.py"); b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
class NatasBannerContract(unittest.TestCase):
 def test_outputs_are_safe_and_complete(self):
  self.assertEqual(set(b.T),set(range(15)))
  with tempfile.TemporaryDirectory() as root:
   b.main(root); files=list(Path(root).glob("*.html")); self.assertEqual(len(files),15)
   for f in files:
    text=f.read_text("ascii"); self.assertIn('<pre class="cei-login-banner">',text); self.assertNotIn("<script",text.lower()); self.assertIsNone(re.search(r"\son\w+\s*=",text,re.I)); self.assertIn("Misuse of this system is prohibited",text); self.assertIn("AI or external tools",text); self.assertIn("assigned challenge environment",text)
 def test_server_wiring_contract(self):
  php=(ROOT/"build"/"cei-natas-banner.php").read_text(); vhost=(ROOT/"build"/"03-generate-vhosts.py").read_text(); docker=(ROOT/"Dockerfile").read_text()
  for token in ("$port < 8000 || $port > 8014","/etc/cei-labs/natas-banners","Content-Disposition","text/html","preg_match","static $done") : self.assertIn(token,php)
  self.assertEqual(vhost.count("php_admin_value auto_prepend_file /opt/cei-natas-banner.php"),1); self.assertIn("range(15)",vhost)
  self.assertIn("/etc/cei-labs/natas-banners",docker); self.assertIn("/opt/cei-natas-banner.php",docker); self.assertIn("chmod 444",docker)
if __name__=="__main__": unittest.main()
