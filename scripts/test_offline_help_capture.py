import unittest
from unittest.mock import patch, Mock
import subprocess
from offline_help_capture import capture, docker_command, SubprocessRunner, CaptureError, MAX_STREAM_BYTES, normalize_url, group_classifications, compare_manifests, capture_entry
ENTRY={"id":"x","argv":["ssh","-h"],"runtime":"target","image":"x@sha256:"+"a"*64}
class CaptureTests(unittest.TestCase):
 def test_stderr_nonzero_and_ordered_urls(self):
  r=capture(ENTRY,lambda _: {"stdout":"https://a.test/x", "stderr":"bad https://b.test/y https://a.test/x", "exit_code":1})
  self.assertEqual(r["exit_code"],1); self.assertEqual(r["printed_urls"],["https://a.test/x","https://b.test/y"])
 def test_none_and_truncation(self):
  self.assertEqual(capture(ENTRY,lambda _:{"stdout":"cat", "stderr":"", "exit_code":0})["printed_urls"],[])
  with self.assertRaises(ValueError): capture(ENTRY,lambda _:{"stdout":"", "stderr":"", "exit_code":0,"truncated":True})
 def test_exact_isolated_command(self):
  command=docker_command(ENTRY["image"],["cat","--help"])
  self.assertEqual(command[:7],["docker","run","--rm","--network","none","--read-only","--cap-drop"])
  for token in ("ALL","no-new-privileges","65534:65534","LC_ALL=C","TERM=dumb","--entrypoint","cat"): self.assertIn(token,command)
 def test_subprocess_runner_bytes_nonzero_and_limits(self):
  with patch("offline_help_capture.subprocess.run",return_value=Mock(stdout=b"x\xff",stderr=b"err",returncode=7)):
   self.assertEqual(SubprocessRunner()(["x"]),{"stdout":"x\ufffd","stderr":"err","exit_code":7})
  with patch("offline_help_capture.subprocess.run",return_value=Mock(stdout=b"x"*(MAX_STREAM_BYTES+1),stderr=b"",returncode=0)):
   with self.assertRaises(CaptureError): SubprocessRunner()(["x"])
 def test_url_normalization(self):
  self.assertEqual(normalize_url('<HTTP://Example.TEST:80>'),"http://example.test/")
  self.assertEqual(normalize_url('https://EXAMPLE.test/a?q=1).'),"https://example.test/a?q=1")
  for value in ('https://u:p@example.test/','https://example.test/%zz','https://example.test/\n'):
   with self.assertRaises(CaptureError): normalize_url(value)
 def test_grouping_is_deterministic(self):
  rows=[{"challenge_ids":["b"],"argv":["cat","--help"],"runtime":"bandit-target","package":"coreutils"},{"challenge_ids":["a"],"argv":["cat","--help"],"runtime":"bandit-target","package":"coreutils"},{"challenge_ids":["z"],"not_applicable":"topic"}]
  commands,other=group_classifications(rows)
  self.assertEqual(commands[0]["challenge_ids"],["a","b"]); self.assertEqual(other[0]["status"],"not_applicable")
 def test_manifest_comparison(self):
  base={"schema_version":1,"entries":[{"id":"x","image":"a","stdout_sha256":"1","printed_urls":[]}]}
  self.assertEqual(compare_manifests(base,base),[])
  changed={"schema_version":1,"entries":[{"id":"x","image":"b","stdout_sha256":"2","printed_urls":["https://x/"]}]}
  self.assertEqual(compare_manifests(changed,base),[("x","image"),("x","stdout_sha256"),("x","printed_urls")])
  self.assertEqual(compare_manifests({"schema_version":1,"entries":[]},base),[("x","removed")])
 def test_capture_entry_probe_order_and_metadata(self):
  calls=[]; responses=iter([{"stdout":"/usr/bin/cat\n","stderr":"","exit_code":0},{"stdout":"9.1\n","stderr":"","exit_code":0},{"stdout":"help","stderr":"","exit_code":1}])
  def runner(command): calls.append(command); return next(responses)
  entry={"id":"x","argv":["cat","--help"],"runtime":"bandit-target","package":"coreutils"}
  result=capture_entry(entry,"x@sha256:"+"a"*64,runner)
  self.assertEqual(result["exit_code"],1); self.assertEqual((result["executable_path"],result["package_version"]),("/usr/bin/cat","9.1"))
  self.assertIn("/usr/bin/which",calls[0]); self.assertIn("/usr/bin/dpkg-query",calls[1]); self.assertIn("cat",calls[2])
 def test_capture_entry_rejects_bad_probe(self):
  entry={"argv":["cat","--help"],"runtime":"bandit-target","package":"coreutils"}; image="x@sha256:"+"a"*64
  for first in ({"stdout":"relative\n","stderr":"","exit_code":0},{"stdout":"/bin/cat\n","stderr":"","exit_code":0}):
   responses=iter([first,{"stdout":"bad version!\n","stderr":"","exit_code":0}])
   with self.assertRaises(CaptureError): capture_entry(entry,image,lambda _:next(responses))
  with patch("offline_help_capture.subprocess.run",side_effect=subprocess.TimeoutExpired(["x"],5)):
   with self.assertRaises(CaptureError): SubprocessRunner()(["x"])
if __name__=="__main__": unittest.main()
