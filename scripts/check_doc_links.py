#!/usr/bin/env python3
"""Fail CI if a relative markdown link in README.md or docs/** points nowhere.

Relative doc links are the one piece of documentation metadata no other check
covers, and they rot silently: a doc is moved or renamed during a restructure
and every relative link inside it becomes a dead 404, with nothing in the diff
flagging it. That is exactly how docs/archive/plans/sentinel-sy0-701-plan.md
ended up citing four pre-restructure sibling paths that resolved inside
docs/archive/plans/ instead of docs/reference/ and docs/tracks/.

What this validates:

  * inline links/images ``[text](target)`` / ``![alt](target)``, including
    angle-bracketed targets (``[x](<my file.md>)``);
  * reference-style link definitions ``[id]: target``;
  * relative targets only, resolved against the *containing file's* directory
    (plus repo-root-absolute ``/docs/...`` targets, which GitHub renders as a
    repository path).

Deliberately NOT validated, because a false positive here would only train
maintainers to ignore the check:

  * external schemes -- http(s)://, mailto:, tel:, data:;
  * pure in-page anchors (``#some-heading``);
  * anything inside a fenced code block or an inline code span -- those are
    prose about paths, not navigable links (``challenges/<id>/challenge.yml``
    is written that way throughout the guides).

Generated output is also exempt. challenges/, osint/, threadline/, and
sentinel/ are gitignored build products that are absent on a clean CI
checkout, so a link into one of them is unverifiable rather than broken. The
exemption is read from the repository's own .gitignore instead of a hardcoded
list, so it tracks whatever the build scripts start emitting.

Run on a clean checkout, before or after the build_<track>.py scripts.
Exits 0 when every relative link resolves (or lands in ignored generated
output); exits 1 and prints a ``file:line`` report for each dead link; exits 2
when the tree it was asked to check is not usable.
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path
from urllib.parse import unquote

# The committed documentation surface: the top-level README plus docs/**.
# targets/ is deliberately excluded -- it is build context, and its READMEs
# are target-internal rather than part of the published doc tree.
DOC_ROOTS = ("README.md", "docs")

# Anything matching this is not a link we can (or should) resolve. Bare
# "//host/path" is a protocol-relative URL, which is external, not relative.
EXTERNAL_SCHEME = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.IGNORECASE)

# Inline link or image, bare or angle-bracketed target. Deliberately simple:
# nested parens in a target are rare here and over-matching would create
# false positives.
INLINE_LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*<?([^)<>\s]+)>?(?:\s+[\"'][^)\n]*[\"'])?\s*\)")

# Reference-style definition, e.g. ``[readme]: ../README.md``.
REF_DEFINITION = re.compile(r"^ {0,3}\[[^\]\n]+\]:\s*<?([^\s>]+)>?")

FENCE = re.compile(r"^\s*(?:```|~~~)")
INLINE_CODE = re.compile(r"`[^`\n]*`")


class Gitignore:
    """Minimal gitignore matcher, enough for this repository's patterns.

    Supports comments, blank lines, root anchoring via a leading '/',
    '**' wildcards, and trailing '/' (a directory pattern, which in git also
    covers everything beneath it). Negation ('!pattern') is honoured with
    git's last-match-wins rule, so un-ignoring a path works.
    """

    def __init__(self, patterns: list[str]) -> None:
        self._rules: list[tuple[re.Pattern[str], bool]] = []
        for raw in patterns:
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            negated = line.startswith("!")
            if negated:
                line = line[1:]
            # A directory-only pattern ('challenges/*/') is stripped to the
            # same form as a file pattern; a path match always covers the
            # matched entry and anything under it, which is what git does for
            # directories.
            stripped = line.strip("/")
            if not stripped:
                continue
            # A leading '/' anchors at the root, and so does any interior '/'
            # (git's own rule). Otherwise the pattern matches at any depth.
            anchored = line.startswith("/") or "/" in stripped
            self._rules.append((re.compile(self._translate(stripped, anchored)), negated))

    @staticmethod
    def _translate(pattern: str, anchored: bool) -> str:
        # '**/' spans zero or more directories; '**' spans anything.
        out: list[str] = []
        i = 0
        while i < len(pattern):
            if pattern.startswith("**/", i):
                out.append("(?:[^/]+/)*")
                i += 3
            elif pattern[i] == "*":
                out.append("[^/]*")
                i += 1
            elif pattern[i] == "?":
                out.append("[^/]")
                i += 1
            else:
                out.append(re.escape(pattern[i]))
                i += 1
        prefix = "" if anchored else "(?:.*/)?"
        return f"^{prefix}{''.join(out)}(?:/.*)?$"

    @classmethod
    def from_text(cls, lines: list[str]) -> "Gitignore":
        return cls(lines)

    @classmethod
    def from_file(cls, path: Path) -> "Gitignore":
        return cls.from_text(path.read_text(encoding="utf-8").splitlines())

    def ignored(self, repo_relative: str) -> bool:
        """True if the last matching rule ignores the path (git semantics)."""
        candidate = repo_relative.strip("/")
        if not candidate:
            return False
        verdict = False
        for regex, negated in self._rules:
            if regex.match(candidate):
                verdict = not negated
        return verdict


def iter_markdown(root: Path) -> list[Path]:
    """Every markdown file in the doc surface, in a stable order."""
    files: list[Path] = []
    for entry in DOC_ROOTS:
        base = root / entry
        if base.is_file() and base.suffix == ".md":
            files.append(base)
        elif base.is_dir():
            files.extend(p for p in base.rglob("*.md") if p.is_file())
    return sorted(files)


def link_targets(line: str) -> list[str]:
    """All link targets on one markdown line, inline and reference-style."""
    # Drop inline code spans so path-shaped prose is never read as a link.
    line = INLINE_CODE.sub("", line)
    targets = [m.group(1) for m in INLINE_LINK.finditer(line)]
    ref = REF_DEFINITION.match(line)
    if ref:
        targets.append(ref.group(1))
    return targets


def link_positions(files: list[Path]) -> list[tuple[Path, int, str]]:
    """(file, 1-based line number, raw target) for every link in fenced-free text."""
    found = []
    for path in files:
        inside_fence = False
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if FENCE.match(line):
                inside_fence = not inside_fence
                continue
            if inside_fence:
                continue
            for target in link_targets(line):
                found.append((path, lineno, target))
    return found


def is_relative_link(target: str) -> bool:
    """False for external URLs, in-page anchors, and pure fragments."""
    if not target or target.startswith("#"):
        return False
    return EXTERNAL_SCHEME.match(target) is None


def resolve(target: str, source: Path, root: Path) -> Path:
    """Resolve a relative link against its containing file, not the CWD.

    The result is normalized, so 'docs/guides/../../README.md' collapses to
    'README.md' before it is compared or reported.
    """
    path_part = unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not path_part:
        return source
    if path_part.startswith("/"):
        candidate = root / path_part.lstrip("/")
    else:
        candidate = source.parent / path_part
    return Path(os.path.normpath(candidate))


def _repo_relative(path: Path, root: Path) -> str | None:
    """Path relative to root, or None if it escapes the repository."""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return None


def check(root: Path) -> list[str]:
    """Return a report line per dead relative link; an empty list means clean."""
    files = iter_markdown(root)
    if not files:
        raise FileNotFoundError(f"no markdown found under {', '.join(DOC_ROOTS)} in {root}")

    ignore_file = root / ".gitignore"
    if not ignore_file.is_file():
        raise FileNotFoundError(f"{ignore_file} not found; cannot tell generated paths from real ones")
    ignores = Gitignore.from_file(ignore_file)

    problems: list[str] = []
    for source, lineno, target in link_positions(files):
        if not is_relative_link(target):
            continue
        resolved = resolve(target, source, root)
        if resolved.exists():
            continue
        repo_relative = _repo_relative(resolved, root)
        if repo_relative is not None and ignores.ignored(repo_relative):
            # Generated build output: unverifiable on a clean checkout, not broken.
            continue
        shown = repo_relative or str(resolved)
        problems.append(
            f"{_repo_relative(source, root)}:{lineno}: "
            f"dead relative link -> {target} (resolves to {shown})"
        )
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root to scan (default: the checkout containing scripts/)",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    try:
        problems = check(root)
    except FileNotFoundError as exc:
        print(f"error: {exc}")
        return 2

    if problems:
        print(f"{len(problems)} dead relative markdown link(s):")
        for problem in problems:
            print(f"  {problem}")
        return 1
    print(f"doc links OK: no dead relative links under {', '.join(DOC_ROOTS)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
