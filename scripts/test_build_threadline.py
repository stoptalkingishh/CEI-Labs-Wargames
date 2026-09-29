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

    def test_uses_the_shared_tier_helper_instead_of_a_local_copy(self):
        # #102: build_threadline.py used to define its own `managed_tiers`
        # that reimplemented hint_economy's pairing *without* its
        # "exactly three hint tiers" ValueError guard, so a tier-count typo
        # in HINTS shipped a silently short wallet.
        self.assertFalse(hasattr(builder, "managed_tiers"))
        for challenge_id, texts in builder.HINTS.items():
            with self.subTest(challenge_id=challenge_id):
                tiers = builder.ctfd_tiers(100, texts)
                self.assertEqual(len(tiers), 3)
                self.assertEqual([tier["tier"] for tier in tiers], [1, 2, 3])

    def test_hint_wallet_tiers_raise_on_malformed_authored_data(self):
        malformed = dict(builder.HINTS)
        first_id = sorted(malformed)[0]
        malformed[first_id] = malformed[first_id][:2]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "threadline"
            with patch.object(builder, "BASE_DIR", output), patch.object(
                builder, "RELEASE_STATE", "hidden"
            ), patch.object(builder, "HINTS", malformed):
                with self.assertRaises(ValueError):
                    builder.main_build()


if __name__ == "__main__":
    unittest.main()
