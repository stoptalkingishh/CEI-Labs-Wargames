import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

try:
    import build_threadline as builder
except ModuleNotFoundError:
    from scripts import build_threadline as builder


class ThreadlineBuilderTests(unittest.TestCase):
    def test_campaign_shape_and_source_contract(self):
        ids = [challenge["id"] for challenge in builder.CHALLENGES]
        self.assertEqual(len(ids), 42)
        self.assertEqual(len(set(ids)), 42)
        self.assertEqual(set(ids), set(builder.FLAGS))
        self.assertEqual(set(ids), set(builder.META))
        self.assertEqual(len(builder.CHALLENGE_SOURCE_ZIP), 39)
        self.assertTrue(set(builder.CHALLENGE_SOURCE_ZIP) <= set(ids))
        self.assertEqual(
            [
                sum(1 for challenge in builder.CHALLENGES if challenge["arc"].split("-", 1)[0] == str(arc))
                for arc in range(9)
            ],
            [1, 4, 6, 4, 6, 6, 3, 10, 2],
        )

    def test_build_is_clean_deterministic_shape_and_hidden_by_default(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "threadline"
            with patch.object(builder, "BASE_DIR", output), patch.object(builder, "RELEASE_STATE", "hidden"):
                builder.main_build()
                self.assertEqual(len(list(output.glob("*/challenge.yml"))), 42)
                manifest = json.loads((output / "threadline-training.json").read_text(encoding="utf-8"))
                self.assertEqual(manifest["track"], "threadline")
                self.assertEqual(manifest["release_state"], "hidden")
                self.assertEqual(len(manifest["challenges"]), 42)
                self.assertTrue(all("state: hidden" in p.read_text(encoding="utf-8") for p in output.glob("*/challenge.yml")))

                stale = output / "stale" / "challenge.yml"
                stale.parent.mkdir()
                stale.write_text("stale", encoding="utf-8")
                builder.main_build()
                self.assertFalse(stale.exists())
                self.assertEqual(len(list(output.glob("*/challenge.yml"))), 42)

    def test_invalid_release_state_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(builder, "BASE_DIR", Path(directory) / "threadline"), patch.object(
                builder, "RELEASE_STATE", "published"
            ):
                with self.assertRaises(SystemExit):
                    builder.main_build()


if __name__ == "__main__":
    unittest.main()
