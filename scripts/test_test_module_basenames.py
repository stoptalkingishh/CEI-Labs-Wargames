"""Guard against duplicate unittest module basenames across the repository.

`unittest discover` imports test modules by basename. Two test modules that
share a basename but live in different directories therefore resolve to the
same `sys.modules` entry, and whichever one discovery reaches second is
silently dropped from the run -- the suite still reports OK, it just runs
fewer tests than the tree actually contains.

That is not hypothetical here. `scripts/test_lab_22.py` and
`targets/sentinel/test_lab_22.py` once coexisted (PR #106), and the collision
went unnoticed because CI never ran discovery across both roots at once. It is
currently safe only because `targets/bandit/build/test_generate_banners.py`
and `targets/krypton/build/test_generate_banners.py` are each collected in a
separate `working-directory`, which is a separate process with a separate
`sys.path`.

The one duplicate that exists today is `test_generate_banners.py`, which is
safe because .github/workflows/validate.yml collects the bandit copy and the
krypton copy in two separate `working-directory` steps -- two processes, two
`sys.path` objects, neither able to shadow the other. Rather than pretend it
is not there, this test pins that exact baseline: adding a new collision fails
the build, and so does silently removing the known one without tidying the
entry. Unifying discovery across targets is the change that makes the
allowlist wrong, and it should have to update this file when it does.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import check_doc_links

TEST_GLOB = "test_*.py"

# Colliding basenames that are known to be collected by separate discovery
# processes, and so cannot shadow each other today. Each entry must stay
# justified by a distinct `working-directory` in .github/workflows/validate.yml.
KNOWN_SAFE_DUPLICATES = {
    "test_generate_banners.py": [
        "targets/bandit/build/test_generate_banners.py",
        "targets/krypton/build/test_generate_banners.py",
    ],
}


def test_modules(root: Path) -> list[Path]:
    """Every test module in the tree that is not gitignored build output.

    The generated trees (challenges/, sentinel/, threadline/, osint/) are
    build products, absent on a clean checkout and irrelevant to discovery,
    so they are excluded using the repository's own .gitignore rather than a
    hardcoded list -- the same rule check_doc_links already follows.
    """
    ignores = check_doc_links.Gitignore.from_file(root / ".gitignore")
    found: list[Path] = []
    for path in root.rglob(TEST_GLOB):
        if not path.is_file() or ".git" in path.relative_to(root).parts:
            continue
        if ignores.ignored(path.relative_to(root).as_posix()):
            continue
        found.append(path)
    return sorted(found)


def duplicate_basenames(root: Path) -> dict[str, list[str]]:
    """Map each colliding module basename to its repo-relative locations."""
    locations: dict[str, list[str]] = {}
    for path in test_modules(root):
        locations.setdefault(path.name, []).append(path.relative_to(root).as_posix())
    return {name: sorted(paths) for name, paths in sorted(locations.items()) if len(paths) > 1}


class TestModuleBasenameTests(unittest.TestCase):
    def test_duplicates_are_only_the_known_separately_discovered_basename(self) -> None:
        """Pin the collision baseline so a new one cannot appear unreviewed."""
        root = Path(__file__).resolve().parents[1]
        duplicates = duplicate_basenames(root)
        self.assertEqual(
            duplicates,
            KNOWN_SAFE_DUPLICATES,
            "unittest imports test modules by basename, so a repeated basename "
            "means one of these modules is never collected. Either give one of "
            "the pair a unique name, or -- if they are collected by separate "
            "`working-directory` steps in .github/workflows/validate.yml and so "
            "cannot shadow each other -- add the collision to "
            "KNOWN_SAFE_DUPLICATES with a sentence saying why it is safe.",
        )

    def test_known_safe_duplicates_are_actually_still_duplicated(self) -> None:
        """Stop the allowlist from accumulating entries for resolved problems."""
        root = Path(__file__).resolve().parents[1]
        for name, paths in KNOWN_SAFE_DUPLICATES.items():
            for path in paths:
                self.assertTrue(
                    (root / path).is_file(),
                    f"{path} is allowlisted as a duplicate of {name} but does not exist",
                )

    def test_guard_detects_a_duplicate_basename(self) -> None:
        """Negative control, so the guard cannot rot into a silent no-op.

        A guard test that only ever asserts on the real tree would still pass
        if its own scanner stopped finding anything.
        """
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
            (root / "alpha").mkdir()
            (root / "beta").mkdir()
            (root / "alpha" / "test_thing.py").write_text("", encoding="utf-8")
            (root / "beta" / "test_thing.py").write_text("", encoding="utf-8")
            (root / "alpha" / "helper.py").write_text("", encoding="utf-8")

            duplicates = duplicate_basenames(root)

        self.assertEqual(list(duplicates), ["test_thing.py"])
        self.assertEqual(
            duplicates["test_thing.py"],
            ["alpha/test_thing.py", "beta/test_thing.py"],
        )

    def test_collision_free_tree_reports_nothing(self) -> None:
        """The other half of the negative control: distinct names are fine."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
            (root / "alpha").mkdir()
            (root / "beta").mkdir()
            (root / "alpha" / "test_one.py").write_text("", encoding="utf-8")
            (root / "beta" / "test_two.py").write_text("", encoding="utf-8")

            self.assertEqual(duplicate_basenames(root), {})


if __name__ == "__main__":
    unittest.main()
