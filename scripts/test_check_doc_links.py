from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

import check_doc_links


class GitignoreTests(unittest.TestCase):
    def test_matches_this_repository_generated_output_rules(self) -> None:
        """The real .gitignore is the contract: generated build output must be
        recognised so a link into it is skipped rather than reported broken on
        a clean CI checkout."""
        root = Path(__file__).resolve().parents[1]
        ignores = check_doc_links.Gitignore.from_file(root / ".gitignore")

        for ignored in (
            "challenges/bandit-00/challenge.yml",
            "challenges/natas-34/challenge.yml",
            "challenges/sentinel-hint-wallet.json",
            "osint/osint-training.json",
            "threadline/threadline-00/challenge.yml",
            "sentinel/sentinel-00/challenge.yml",
            "scripts/local-ctfd/.state/concurrency.json",
            "validation-manifest.json",
            "scripts/__pycache__/build_natas.cpython-312.pyc",
        ):
            with self.subTest(ignored=ignored):
                self.assertTrue(ignores.ignored(ignored))

        for kept in (
            "docs/guides/challenge-inventory.md",
            "scripts/check_doc_links.py",
            "game-stages.yml",
            "README.md",
            "challenges.md",
        ):
            with self.subTest(kept=kept):
                self.assertFalse(ignores.ignored(kept))

    def test_supports_anchoring_wildcards_comments_and_negation(self) -> None:
        ignores = check_doc_links.Gitignore.from_text(
            [
                "# a comment",
                "",
                "/root-only.txt",
                "generated/",
                "deep/**/scratch/",
                "*.tmp",
                "!keep.tmp",
            ]
        )

        # Root-anchored ('/root-only.txt') and interior-slash patterns
        # ('deep/**/scratch/') match only at the repository root, per git.
        for ignored in (
            "root-only.txt",
            "generated/thing.md",
            "deep/scratch/z",
            "deep/x/y/scratch/z",
            "notes.tmp",
            "anywhere/notes.tmp",
        ):
            with self.subTest(ignored=ignored):
                self.assertTrue(ignores.ignored(ignored))

        # '!keep.tmp' un-ignores it (last matching rule wins); a leading '/'
        # or an interior '/' does not match at other depths; a slash-free
        # pattern matches at any depth, which is why notes.tmp is ignored.
        for kept in (
            "sub/root-only.txt",
            "a/b/deep/x/y/scratch/z",
            "keep.tmp",
            "docs/notes.md",
            "",
        ):
            with self.subTest(kept=kept):
                self.assertFalse(ignores.ignored(kept))


class _Repo:
    """A throwaway repo-shaped tree for check() to walk."""

    def __init__(self, base: Path) -> None:
        self.base = base
        (base / "docs" / "guides").mkdir(parents=True, exist_ok=True)
        (base / ".gitignore").write_text("challenges/*/\n/osint/\n", encoding="utf-8")

    def write(self, relative: str, text: str) -> Path:
        path = self.base / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def check(self) -> list[str]:
        return check_doc_links.check(self.base)


class CheckDocLinksTests(unittest.TestCase):
    def test_clean_repo_reports_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _Repo(Path(tmp))
            repo.write("README.md", "# Root\n\nSee [guide](docs/guides/guide.md).\n")
            repo.write("docs/README.md", "# Docs index\n")
            repo.write(
                "docs/guides/guide.md",
                "# Guide\n\nBack to [root](../../README.md).\n"
                "Up one [index](../README.md) and [sibling](other.md).\n"
                "Reference-style [ref][r].\n\n[r]: ../../README.md\n",
            )
            repo.write("docs/guides/other.md", "# Other\n")
            self.assertEqual(repo.check(), [])

    def test_flags_dead_sibling_link_with_file_and_line(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _Repo(Path(tmp))
            repo.write("README.md", "# Root\n")
            repo.write(
                "docs/guides/guide.md",
                "# Guide\n\nFine [root](../../README.md).\n\n"
                "Broken [sibling](missing.md) here.\n",
            )
            problems = repo.check()
            self.assertEqual(len(problems), 1)
            self.assertIn("docs/guides/guide.md:5", problems[0])
            self.assertIn("missing.md", problems[0])

    def test_flags_dead_reference_style_definition(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _Repo(Path(tmp))
            repo.write("README.md", "# Root\n\n[gone][missing].\n\n[missing]: docs/nope.md\n")
            problems = repo.check()
            self.assertEqual(len(problems), 1)
            self.assertIn("README.md:5", problems[0])

    def test_ignores_external_schemes_and_in_page_anchors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _Repo(Path(tmp))
            repo.write("README.md", "# Root\n")
            repo.write(
                "docs/guides/guide.md",
                "# Guide\n"
                "[web](https://example.invalid/nope.md) and [mail](mailto:a@b.invalid)\n"
                "[anchor](#some-heading) and [bare](#) and [proto](//example.invalid/x)\n"
                "[data](data:text/plain,hi) and [tel](tel:+15550100)\n",
            )
            self.assertEqual(repo.check(), [])

    def test_does_not_flag_links_into_gitignored_generated_output(self) -> None:
        """challenges/ and osint/ are gitignored build products, absent on a
        clean checkout -- a link into one is unverifiable, not broken."""
        with tempfile.TemporaryDirectory() as tmp:
            repo = _Repo(Path(tmp))
            repo.write("README.md", "# Root\n")
            repo.write(
                "docs/guides/guide.md",
                "# Guide\n"
                "[gen](../../challenges/bandit-00/challenge.yml)\n"
                "[osint](../../osint/osint-training.json)\n",
            )
            self.assertEqual(repo.check(), [])

    def test_flags_dead_link_outside_generated_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _Repo(Path(tmp))
            repo.write("README.md", "# Root\n")
            repo.write(
                "docs/guides/guide.md",
                "# Guide\n[gen](../../challenges/../nope/x.md)\n",
            )
            problems = repo.check()
            self.assertEqual(len(problems), 1)
            self.assertIn("nope/x.md", problems[0])

    def test_ignores_links_inside_fenced_code_blocks_and_inline_code(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _Repo(Path(tmp))
            repo.write("README.md", "# Root\n")
            repo.write(
                "docs/guides/guide.md",
                "# Guide\n\nInline `challenges/<id>/challenge.yml` is prose, not a link.\n\n"
                "```markdown\n[demo](not-a-real-path.md)\n```\n\n"
                "~~~\n[also](neither-is-this.md)\n~~~\n\n[real](../../README.md)\n",
            )
            self.assertEqual(repo.check(), [])

    def test_resolves_angle_bracketed_and_percent_encoded_targets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _Repo(Path(tmp))
            repo.write("README.md", "# Root\n")
            repo.write("docs/my guide.md", "# Spaced\n")
            repo.write(
                "docs/guides/guide.md",
                "# Guide\n[spaced](../my%20guide.md) and [angled](<../my guide.md>)\n",
            )
            self.assertEqual(repo.check(), [])

    def test_anchor_and_query_are_stripped_before_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _Repo(Path(tmp))
            repo.write("README.md", "# Root\n")
            repo.write(
                "docs/guides/guide.md",
                "# Guide\n[sect](guide.md#a-heading) and [q](guide.md?x=1)\n",
            )
            self.assertEqual(repo.check(), [])

    def test_repo_root_absolute_link_resolves_from_repo_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _Repo(Path(tmp))
            repo.write("README.md", "# Root\n")
            repo.write(
                "docs/guides/guide.md",
                "# Guide\n[ok](/docs/guides/guide.md) [no](/docs/nope.md)\n",
            )
            problems = repo.check()
            self.assertEqual(len(problems), 1)
            self.assertIn("docs/nope.md", problems[0])

    def test_escaping_the_repository_is_broken(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _Repo(Path(tmp))
            repo.write("README.md", "# Root\n")
            repo.write("docs/guides/guide.md", "# Guide\n[away](../../../../etc/passwd.md)\n")
            self.assertEqual(len(repo.check()), 1)

    def test_missing_gitignore_is_a_prerequisite_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "docs").mkdir()
            (base / "docs" / "a.md").write_text("# A\n", encoding="utf-8")
            with self.assertRaisesRegex(FileNotFoundError, "gitignore"):
                check_doc_links.check(base)

    def test_repo_doc_surface_is_actually_clean(self) -> None:
        """The regression guard itself: the committed tree must pass."""
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(check_doc_links.check(root), [])


class ResolverTests(unittest.TestCase):
    def test_is_relative_link_classification(self) -> None:
        for target in ("docs/a.md", "./a.md", "../a.md", "/docs/a.md", "a.md#frag", "a.md?q=1"):
            with self.subTest(target=target):
                self.assertTrue(check_doc_links.is_relative_link(target))
        for target in (
            "",
            "#frag",
            "https://x/y",
            "http://x/y",
            "mailto:a@b",
            "tel:+1",
            "//x/y",
            "data:text/plain,x",
        ):
            with self.subTest(target=target):
                self.assertFalse(check_doc_links.is_relative_link(target))

    def test_resolve_is_relative_to_containing_file_not_cwd(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "docs" / "guides" / "guide.md"
            source.parent.mkdir(parents=True)
            self.assertEqual(
                check_doc_links.resolve("../../README.md", source, root),
                root / "README.md",
            )
            self.assertEqual(
                check_doc_links.resolve("sibling.md", source, root),
                root / "docs" / "guides" / "sibling.md",
            )
            self.assertEqual(
                check_doc_links.resolve("/docs/guides/guide.md", source, root),
                source,
            )
            self.assertEqual(
                check_doc_links.resolve("guide.md#anchor", source, root),
                source,
            )

    def test_resolve_normalizes_dot_segments(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "docs" / "guides" / "g.md"
            self.assertEqual(
                check_doc_links.resolve("../../a/../README.md", source, root),
                root / "README.md",
            )
            self.assertEqual(
                check_doc_links.resolve("../guides/../x.md", source, root),
                Path(os.path.normpath(root / "docs" / "x.md")),
            )


if __name__ == "__main__":
    unittest.main()
