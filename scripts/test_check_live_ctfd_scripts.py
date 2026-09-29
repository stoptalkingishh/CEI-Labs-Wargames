"""Tests for the static guard on the three main()-driven live-CTFd scripts.

House style matches the other scripts/ tests: stdlib unittest only, no live
CTFd, no network. The scan functions are exercised against throwaway trees so
each rule is pinned independently, and ``test_the_committed_tree_is_clean`` is
the regression guard itself -- if any of the three live scripts ever drifts
back to a hardcoded challenge count, that one test goes red.
"""

from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

import check_live_ctfd_scripts as guard

ROOT = guard.ROOT

# The counts game-stages.yml declares today: per stage, the staged total, and
# the total including the unstaged AI Copilot Setup track. Written out here on
# purpose -- a copy is a tripwire. If a track gains levels, this test is
# *supposed* to fail until the number is updated, and the guard's own allowed
# set moves with the manifest.
EXPECTED_COUNTS = {8, 35, 36, 79, 85}

# A minimal script that passes every static rule, so each test can break
# exactly one thing.
CLEAN_SCRIPT = '''#!/usr/bin/env python3
"""Black-box smoke test. Sync Krypton (8/8) and Natas (36/36) before start."""
BASE_URL = "http://localhost:8000"
CONCURRENCY = 10
ADMIN = "admin"


def main() -> int:
    for i in range(CONCURRENCY):
        print(i, BASE_URL, ADMIN)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


class _Tree:
    """A throwaway repo-shaped tree: game-stages.yml plus scripts/*.py."""

    def __init__(self, base: Path) -> None:
        self.base = base
        (base / "scripts").mkdir(parents=True, exist_ok=True)
        self.write("game-stages.yml", (ROOT / "game-stages.yml").read_text(encoding="utf-8-sig"))

    def write(self, relative: str, text: str) -> Path:
        path = self.base / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def script(self, source: str, name: str = "test_staggered_smoke.py") -> Path:
        return self.write(f"scripts/{name}", source)

    def findings(self, source: str, name: str = "test_staggered_smoke.py") -> list[guard.Finding]:
        """Every static finding for one synthetic script (imports excluded)."""
        self.script(source, name)
        return guard.check_module(f"scripts/{name}", self.base)


class ChallengeCountLiteralTests(unittest.TestCase):
    """Rule 1: no hardcoded challenge count in a comparison."""

    def test_flags_the_exact_literal_from_the_issue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            found = _Tree(Path(tmp)).findings(
                CLEAN_SCRIPT.replace(
                    "    return 0",
                    "    return 0 if len(admin_challenges) == 59 else 1",
                )
            )
        self.assertEqual(len(found), 1, [str(f) for f in found])
        self.assertIn("hardcoded challenge count 59", found[0].message)
        self.assertIn("game-stages.yml", found[0].message)
        self.assertIn("len(admin_challenges)", found[0].message)

    def test_flags_a_total_written_as_a_sum_of_per_stage_literals(self) -> None:
        """``35 + 8 + 16`` is the same bug, spelled differently."""
        with tempfile.TemporaryDirectory() as tmp:
            found = _Tree(Path(tmp)).findings(
                CLEAN_SCRIPT.replace("    return 0", "    return 0 if len(live_challenges) == 35 + 8 + 16 else 1")
            )
        self.assertEqual(len(found), 1, [str(f) for f in found])
        self.assertIn("hardcoded challenge count 59", found[0].message)

    def test_accepts_every_count_the_manifest_declares(self) -> None:
        for count in sorted(EXPECTED_COUNTS):
            with tempfile.TemporaryDirectory() as tmp, self.subTest(count=count):
                found = _Tree(Path(tmp)).findings(
                    CLEAN_SCRIPT.replace("    return 0", f"    return 0 if len(admin_challenges) == {count} else 1")
                )
                self.assertEqual(found, [])

    def test_allowed_set_is_derived_from_the_manifest_not_frozen(self) -> None:
        """Move the manifest, and yesterday's correct literal becomes a failure."""
        # No count in the docstring here, so the only finding can be the one
        # this test is about.
        source = CLEAN_SCRIPT.replace("Sync Krypton (8/8) and Natas (36/36) before start.", "Sync every stage first.")
        with tempfile.TemporaryDirectory() as tmp:
            tree = _Tree(Path(tmp))
            manifest = (ROOT / "game-stages.yml").read_text(encoding="utf-8-sig")
            self.assertEqual(guard.allowed_challenge_counts(tree.base), EXPECTED_COUNTS)
            tree.write("game-stages.yml", manifest.replace("expected_challenge_count: 36", "expected_challenge_count: 40"))
            self.assertEqual(guard.allowed_challenge_counts(tree.base), {8, 35, 40, 83, 89})
            found = tree.findings(source.replace("    return 0", "    return 0 if len(admin_challenges) == 36 else 1"))
        self.assertEqual(
            [(f.path, f.message) for f in found],
            [(
                "scripts/test_staggered_smoke.py",
                "hardcoded challenge count 36 compared against len(admin_challenges); "
                "derive it from game-stages.yml (the manifest declares 8, 35, 40, 83, 89)",
            )],
        )

    def test_ignores_integers_that_are_not_challenge_counts(self) -> None:
        """The reason this is an AST scan and not a regex: every one of these
        is an integer in the source and none of them is a challenge count."""
        source = CLEAN_SCRIPT + '''
import time

resp = admin.get("/api/v1/challenges?view=admin&per_page=100")
if resp.status_code != 200:
    raise SystemExit(1)
uid = int(time.time() * 1000)
admin.checks(uid, timeout=60, interval=2)
[pool.submit(job) for _ in range(10)]
raise SystemExit(main())
'''
        with tempfile.TemporaryDirectory() as tmp:
            found = _Tree(Path(tmp)).findings(source)
        self.assertEqual(found, [])

    def test_ignores_small_counts(self) -> None:
        """"exactly one audit row" is not a challenge count."""
        with tempfile.TemporaryDirectory() as tmp:
            found = _Tree(Path(tmp)).findings(
                CLEAN_SCRIPT.replace("    return 0", "    return 0 if len(challenge_audit_rows) == 1 else 1")
            )
        self.assertEqual(found, [])

    def test_ignores_challenge_point_values(self) -> None:
        """test_staggered_concurrency.py pins CTFd's default challenge value on
        purpose: that is a point value, not a count."""
        with tempfile.TemporaryDirectory() as tmp:
            found = _Tree(Path(tmp)).findings(
                CLEAN_SCRIPT.replace("    return 0", "    return 0 if challenge_value == 100 else 1")
            )
        self.assertEqual(found, [])


class DocstringProseTests(unittest.TestCase):
    """Rule 2: an N/M count claim in a docstring must match the manifest."""

    def test_flags_the_stale_natas_prose_from_the_issue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            found = _Tree(Path(tmp)).findings(
                CLEAN_SCRIPT.replace("Natas (36/36)", "Natas (16/16)")
            )
        self.assertEqual(len(found), 1, [str(f) for f in found])
        self.assertIn("16/16", found[0].message)
        self.assertEqual(found[0].line, 2)

    def test_accepts_current_prose(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            found = _Tree(Path(tmp)).findings(
                CLEAN_SCRIPT.replace(
                    "Krypton (8/8) and Natas (36/36)",
                    "Krypton (8/8), Natas (36/36), 79 deployed across three stages",
                )
            )
        self.assertEqual(found, [])

    def test_does_not_mistake_list_numbering_paths_or_status_codes_for_counts(self) -> None:
        """1/2. is checklist numbering, 200/404 is an HTTP status pair, and
        neither is a challenge count -- even on a line that says "per stage"."""
        with tempfile.TemporaryDirectory() as tmp:
            found = _Tree(Path(tmp)).findings(CLEAN_SCRIPT.replace(
                "Black-box smoke test. Sync Krypton (8/8) and Natas (36/36) before start.",
                "Deployment checklist (items 1-10) from cei-labs-engine:\n\n"
                "  1/2. Sync docker/ctfd, then check nginx/443 routing.\n"
                "  3.   Confirm the 200/404 split per stage.\n"
                "  4.   Every stage's challenges stay visible.",
            ))
        self.assertEqual(found, [])

    def test_scans_function_docstrings_not_just_the_module(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            found = _Tree(Path(tmp)).findings(
                CLEAN_SCRIPT.replace("def main() -> int:", 'def main() -> int:\n    """Natas (12/12)."""')
            )
        self.assertEqual(len(found), 1, [str(f) for f in found])
        self.assertIn("12/12", found[0].message)


class HostTests(unittest.TestCase):
    """Rule 3: no remote host literals; these only ever run against localhost."""

    def test_accepts_loopback_forms(self) -> None:
        for base in ("http://localhost:8000", "http://127.0.0.1:8000", "https://[::1]:8000"):
            with tempfile.TemporaryDirectory() as tmp, self.subTest(base=base):
                found = _Tree(Path(tmp)).findings(
                    CLEAN_SCRIPT.replace('BASE_URL = "http://localhost:8000"', f'BASE_URL = "{base}"')
                )
                self.assertEqual(found, [])

    def test_flags_a_remote_host(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            found = _Tree(Path(tmp)).findings(
                CLEAN_SCRIPT.replace('"http://localhost:8000"', '"https://ctfd.example.com"')
            )
        self.assertEqual(len(found), 1, [str(f) for f in found])
        self.assertIn("ctfd.example.com", found[0].message)


class StructureTests(unittest.TestCase):
    """Rule 4: main() exists and the __main__ guard reaches it."""

    def test_flags_a_script_whose_main_guard_is_gone(self) -> None:
        source = CLEAN_SCRIPT.split('if __name__ == "__main__":')[0]
        with tempfile.TemporaryDirectory() as tmp:
            found = _Tree(Path(tmp)).findings(source)
        self.assertEqual([f.message for f in found], ['no `if __name__ == "__main__":` guard calling main()'])

    def test_flags_a_script_with_no_main_at_all(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            found = _Tree(Path(tmp)).findings('"""No entry point."""\nprint("hi")\n')
        self.assertEqual(len(found), 2, [str(f) for f in found])
        self.assertIn("no top-level main()", found[0].message)
        self.assertIn("guard", found[1].message)

    def test_flags_a_syntax_error_instead_of_skipping_the_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            found = _Tree(Path(tmp)).findings(CLEAN_SCRIPT + "\ndef broken(:\n")
        self.assertEqual(len(found), 1, [str(f) for f in found])
        self.assertIn("cannot be parsed", found[0].message)

    def test_accepts_a_bom_prefixed_file(self) -> None:
        """One file in scripts/ is committed with a UTF-8 BOM; reading it the
        way the import machinery does keeps that from reading as broken."""
        with tempfile.TemporaryDirectory() as tmp:
            tree = _Tree(Path(tmp))
            (tree.base / "scripts" / "test_staggered_smoke.py").write_text(CLEAN_SCRIPT, encoding="utf-8-sig")
            self.assertEqual(guard.check_module("scripts/test_staggered_smoke.py", tree.base), [])


class DeadWeightTests(unittest.TestCase):
    """Rule 6: nothing else in scripts/ may be dead weight."""

    def test_flags_an_unlisted_script_with_no_test_cases(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tree = _Tree(Path(tmp))
            tree.script("def main() -> int:\n    return 0\n", name="test_live_thing.py")
            found = guard.dead_weight_findings(tree.base)
        self.assertEqual(len(found), 1, [str(f) for f in found])
        self.assertIn("LIVE_SCRIPTS", found[0].message)

    def test_accepts_an_unlisted_script_that_has_real_test_cases(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tree = _Tree(Path(tmp))
            tree.script(
                "import unittest\n\n\nclass T(unittest.TestCase):\n    def test_x(self):\n        pass\n",
                name="test_real_thing.py",
            )
            self.assertEqual(guard.dead_weight_findings(tree.base), [])

    def test_a_listed_script_is_never_reported_as_dead_weight(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tree = _Tree(Path(tmp))
            for name in ("test_staggered_concurrency.py", "test_staggered_smoke.py",
                         "test_export_reconciliation.py"):
                tree.script("def main() -> int:\n    return 0\n", name=name)
            self.assertEqual(guard.dead_weight_findings(tree.base), [])


class ImportTests(unittest.TestCase):
    """Rule 5: the scripts must import, and from the file that was scanned."""

    def _tree_with(self, tmp: str, source: str, name: str = "test_importable.py") -> _Tree:
        tree = _Tree(Path(tmp))
        tree.script(source, name=name)
        sys.path.insert(0, str(tree.base / "scripts"))
        self.addCleanup(sys.path.remove, str(tree.base / "scripts"))
        # importlib caches by module name, not by filename, and a module that
        # raises on import is left out of sys.modules -- so pop by stem.
        self.addCleanup(sys.modules.pop, Path(name).stem, None)
        return tree

    def test_accepts_a_cleanly_importing_module(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tree = self._tree_with(tmp, "VALUE = 1\n")
            self.assertEqual(guard.import_findings(tree.base, ("scripts/test_importable.py",)), [])

    def test_reports_a_module_that_explodes_on_import(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tree = self._tree_with(tmp, "raise RuntimeError('no instance')\n")
            found = guard.import_findings(tree.base, ("scripts/test_importable.py",))
        self.assertEqual(len(found), 1, [str(f) for f in found])
        self.assertIn("does not import cleanly", found[0].message)
        self.assertIn("RuntimeError", found[0].message)

    def test_reports_a_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            found = guard.import_findings(Path(tmp), ("scripts/test_absent.py",))
        self.assertEqual([f.message for f in found], ["file is missing"])

    def test_reports_a_same_named_module_from_elsewhere_on_sys_path(self) -> None:
        """A stale sys.modules entry or a shadowing path must not pass as the
        file that was actually inspected."""
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            one = self._tree_with(first, "VALUE = 1\n", name="test_shadowed.py")
            two = _Tree(Path(second))
            two.script("VALUE = 2\n", name="test_shadowed.py")
            self.assertEqual(guard.import_findings(one.base, ("scripts/test_shadowed.py",)), [])
            found = guard.import_findings(two.base, ("scripts/test_shadowed.py",))
        self.assertEqual(len(found), 1, [str(f) for f in found])
        self.assertIn("not the file that was scanned", found[0].message)


class PrerequisiteTests(unittest.TestCase):
    def test_missing_manifest_is_a_prerequisite_error_not_a_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(FileNotFoundError, "game-stages.yml"):
                guard.check(Path(tmp))

    def test_manifest_counts_match_the_committed_file(self) -> None:
        self.assertEqual(guard.allowed_challenge_counts(ROOT), EXPECTED_COUNTS)

    def test_guarded_scripts_are_the_three_live_ctfd_ones(self) -> None:
        self.assertEqual(
            set(guard.LIVE_SCRIPTS),
            {
                "scripts/test_staggered_concurrency.py",
                "scripts/test_staggered_smoke.py",
                "scripts/test_export_reconciliation.py",
            },
        )
        for relative in guard.LIVE_SCRIPTS:
            with self.subTest(relative=relative):
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_the_guarded_scripts_really_are_dead_weight(self) -> None:
        """The premise of the guard: discovery imports these and collects
        nothing, which is why the static check has to exist."""
        for relative in guard.LIVE_SCRIPTS:
            with self.subTest(relative=relative):
                source = (ROOT / relative).read_text(encoding="utf-8-sig")
                self.assertFalse(guard.exposes_test_cases(source), relative)
                self.assertIn("def main()", source, relative)


class InjectAndFailTests(unittest.TestCase):
    """Inject-and-fail, against the real committed files.

    These take the actual test_staggered_smoke.py and
    test_export_reconciliation.py, put the bug issue #103 reports back into a
    copy, and assert the guard catches it. Nothing here needs CTFd, so this is
    the demonstration CI itself runs.
    """

    def _inject(self, relative: str, broken: str, name: str) -> list[guard.Finding]:
        real = (ROOT / relative).read_text(encoding="utf-8-sig")
        self.assertNotEqual(broken, real, f"injection into {relative} did not change the file")
        with tempfile.TemporaryDirectory() as tmp:
            tree = _Tree(Path(tmp))
            tree.script(broken, name=name)
            return guard.check_module(f"scripts/{name}", tree.base)

    def test_repinning_the_total_to_a_literal_fails(self) -> None:
        found = self._inject(
            "scripts/test_export_reconciliation.py",
            (ROOT / "scripts/test_export_reconciliation.py").read_text(encoding="utf-8-sig").replace(
                "len(admin_challenges) == expected_total",
                "len(admin_challenges) == 59",
            ),
            "test_export_reconciliation.py",
        )
        self.assertEqual(
            [f.message.split(";")[0] for f in found],
            ["hardcoded challenge count 59 compared against len(admin_challenges)"],
        )

    def test_restating_a_stale_natas_count_in_prose_fails(self) -> None:
        real = (ROOT / "scripts/test_staggered_smoke.py").read_text(encoding="utf-8-sig")
        self.assertIsNotNone(re.search(r"Natas \(\d+/\d+", real), "expected an N/M Natas count in the docstring")
        found = self._inject(
            "scripts/test_staggered_smoke.py",
            re.sub(r"Natas \(\d+/\d+", "Natas (16/16", real, count=1),
            "test_staggered_smoke.py",
        )
        self.assertEqual(
            [f.message.split(",")[0] for f in found],
            ["docstring claims a challenge count of 16/16"],
        )


class CommittedTreeTests(unittest.TestCase):
    """The regression guard itself: the committed tree must pass every rule."""

    def test_the_committed_tree_is_clean(self) -> None:
        self.assertEqual([str(f) for f in guard.check(ROOT)], [])

    def test_main_exits_zero_on_the_committed_tree(self) -> None:
        self.assertEqual(guard.main(), 0)


if __name__ == "__main__":
    unittest.main()
