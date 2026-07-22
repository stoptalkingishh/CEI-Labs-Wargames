import unittest, json, tempfile
from pathlib import Path
from unittest.mock import patch
from capture_offline_help import parse_images, build, main, DriftError
from offline_help_inventory import all_classifications

class CliPureTests(unittest.TestCase):
 def test_parse_images_requires_exact_roles(self):
  digest="repo/x@sha256:"+"a"*64; roles={"bandit-target","kali-attacker"}
  self.assertEqual(parse_images(["bandit-target="+digest,"kali-attacker="+digest],roles)["bandit-target"],digest)
  for values in (["bandit-target="+digest],["bandit-target="+digest,"bandit-target="+digest],["other="+digest,"kali-attacker="+digest],["bandit-target=x","kali-attacker="+digest]):
   with self.assertRaises(ValueError): parse_images(values,roles)
 def test_build_captures_only_grouped_commands_deterministically(self):
  digest="repo/x@sha256:"+"a"*64; images={row["runtime"]:digest for row in all_classifications() if "argv" in row}; calls=[]
  def fake(entry,image,runner):
   calls.append(entry["id"]); return {"runtime":entry["runtime"],"argv":entry["argv"],"package":entry["package"],"image":image,"exit_code":0,"stdout_sha256":"a","stderr_sha256":"b","printed_urls":[],"executable_path":"/x","package_version":"1"}
  with patch("capture_offline_help.capture_entry",fake): first=build(images,object()); second=build(images,object())
  command_count=len({(row["runtime"],tuple(row["argv"]),row["package"]) for row in all_classifications() if "argv" in row})
  self.assertEqual(len(calls),command_count*2); self.assertEqual(first,second); self.assertEqual(first["schema_version"],1)
  self.assertEqual(len({entry.get("id",entry.get("challenge_id")) for entry in first["entries"]}),len(first["entries"]))
 def test_cli_baseline_writes_or_preserves_output(self):
  manifest={"schema_version":1,"entries":[{"id":"x","stdout_sha256":"a"}]}; digest="repo/x@sha256:"+"a"*64
  images=["--image","bandit-target="+digest,"--image","krypton-target="+digest,"--image","kali-attacker="+digest]
  with tempfile.TemporaryDirectory() as root:
   output=root+"/out.json"; baseline=root+"/base.json"; output_path=Path(output); baseline_path=Path(baseline)
   with patch("capture_offline_help.build",return_value=manifest): main([*images,"--output",output])
   self.assertTrue(output_path.read_text(encoding="utf-8").endswith("\n"))
   baseline_path.write_text(json.dumps(manifest),encoding="utf-8")
   with patch("capture_offline_help.build",return_value=manifest): main([*images,"--output",output,"--baseline",baseline])
   original=b"keep"; output_path.write_bytes(original)
   changed={"schema_version":1,"entries":[{"id":"x","stdout_sha256":"b"}]}
   with patch("capture_offline_help.build",return_value=changed):
    with self.assertRaises(DriftError): main([*images,"--output",output,"--baseline",baseline])
   self.assertEqual(output_path.read_bytes(),original)

if __name__=="__main__": unittest.main()
