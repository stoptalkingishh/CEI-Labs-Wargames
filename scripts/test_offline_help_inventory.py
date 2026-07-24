import unittest
from pathlib import Path
from offline_help_inventory import bandit_classifications, all_classifications, load_literal_assignment, KRYPTON_CLASSIFICATIONS, NATAS_CLASSIFICATIONS
class InventoryTests(unittest.TestCase):
 def test_bandit_ast_coverage(self):
  rows=bandit_classifications(); ids={i for row in rows for i in row["challenge_ids"]}
  self.assertEqual(ids,{"bandit-%02d"%n for n in range(34)})
  self.assertEqual(next(row["argv"] for row in rows if row["challenge_ids"]==["bandit-00"]),["ssh","-h"])
 def test_all_tracks_are_exactly_covered_without_images(self):
  rows=all_classifications(); self.assertEqual(sum(len(row["challenge_ids"]) for row in rows),56)
  self.assertFalse(any("image" in row for row in rows))
  self.assertTrue(all("package" in row for row in rows if "argv" in row))
 def test_krypton_tier_one_matches_inventory(self):
  hints=load_literal_assignment(Path(__file__).with_name("build_krypton.py"),"HINTS")
  self.assertEqual(set(hints),{"krypton-%02d"%n for n in range(7)})
  self.assertIn("base64 --help",hints["krypton-00"][0]); self.assertIn("xxd --help",hints["krypton-06"][0])
  for n in range(1,6):
   text=hints["krypton-%02d"%n][0]; self.assertNotIn("--help",text); self.assertNotIn(" -h",text); self.assertNotIn("man ",text)
  commands=[row for row in KRYPTON_CLASSIFICATIONS if "argv" in row]
  self.assertEqual([(row["challenge_ids"],row["argv"],row["runtime"]) for row in commands], [(["krypton-00"],["base64","--help"],"krypton-target"),(["krypton-06"],["xxd","--help"],"krypton-target")])
 def test_natas_tier_one_matches_inventory(self):
  hints=load_literal_assignment(Path(__file__).with_name("build_natas.py"),"HINTS")
  self.assertEqual(set(hints),{"natas-%02d"%n for n in range(15)})
  command_ids={0,1,2,4,5}
  for n in command_ids:
   text=hints["natas-%02d"%n][0]; self.assertIn("curl --help",text); self.assertIn("attacker workstation",text)
  for n in set(range(15))-command_ids:
   text=hints["natas-%02d"%n][0]; self.assertNotIn("curl --help",text); self.assertNotIn("man ",text)
  command=next(row for row in NATAS_CLASSIFICATIONS if "argv" in row)
  self.assertEqual((command["challenge_ids"],command["argv"],command["runtime"]),(["natas-00","natas-01","natas-02","natas-04","natas-05"],["curl","--help"],"kali-attacker"))
if __name__=="__main__": unittest.main()
