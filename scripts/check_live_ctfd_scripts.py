#!/usr/bin/env python3
r"""Fail CI if a live-CTFd test script hardcodes a challenge count.

Three scripts in this directory are ``main()``-driven black-box tests that
need a running CTFd instance, so they expose no ``unittest.TestCase``:

  scripts/test_staggered_concurrency.py
  scripts/test_staggered_smoke.py
  scripts/test_export_reconciliation.py

``unittest discover -s scripts -t scripts`` *imports* all three (they match
the default ``test*.py`` pattern) and then collects zero tests from them, so
they run as a silent no-op in CI. That blind spot is not academic: it hid a
hardcoded total of 59 challenges in test_export_reconciliation.py while
game-stages.yml declared 35 + 8 + 36, and it hid a docstring claiming
"Natas (16/16)" through the same 0-34 expansion. The live run that would
have failed never happens in CI, so the drift is invisible until someone
brings up a CTFd instance months later.

This check is the part of those scripts that *can* run without an instance.
It statically inspects the three modules and fails on the whole class of bug
rather than the one instance:

  1. no hardcoded challenge count in a comparison. Any ``Compare`` whose
     other side mentions a challenge (and not a challenge's point value)
     must not compare against an integer literal >= 10 that the manifest
     does not currently declare;
  2. no hardcoded challenge count in prose. A ``N/M`` fraction in a
     docstring is a count claim, and every number in it must be a count
     game-stages.yml currently declares;
  3. no hardcoded host. Every ``http(s)://`` literal must point at
     loopback, because these scripts are only ever run against a local
     instance (docs/guides/staggered-live-test-procedure.md);
  4. structure is intact: a top-level ``main()`` and the
     ``if __name__ == "__main__"`` guard that makes it reachable;
  5. the modules genuinely import, so a syntax error, a bad import, or a
     module renamed out from under them cannot hide behind the no-op;
  6. no *other* scripts/test_*.py may be dead weight. A new script that
     exposes no TestCase is collected by nothing, so it must either have real
     test cases or be added to ``LIVE_SCRIPTS`` here, which keeps this guard's
     coverage claim honest instead of freezing it at three filenames.

An AST scan rather than grep: the literals that matter are the ones *in
semantic position*, not the ones that merely look numeric. ``CONCURRENCY =
10``, ``timeout=60``, ``per_page=100``, ``status_code == 200`` and
``int(time.time() * 1000)`` are all integers in these files and none of them
is a challenge count; a regex cannot tell them from ``len(admin_challenges)
== 59`` without a pile of fragile context heuristics, and a plain ``\d+`` scan
over the docstrings would also fire on prose that is not a count. Reading the
tree also gets comments, which the AST drops, for free.

Deliberately NOT checked: that a count is *correct at runtime*, that the
scripts still exercise what their docstrings claim (only a live CTFd can
answer that), and anything about challenge point values -- ``challenge_value
== 100`` in test_staggered_concurrency.py pins CTFd's default challenge value
on purpose, and pinning it is correct.

Exits 0 when the three scripts are clean; 1 with a ``file:line`` report per
problem; 2 when the tree it was asked to check is unusable.
"""

from __future__ import annotations

import ast
import importlib
import re
import sys
import tokenize
from pathlib import Path
from typing import NamedTuple

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_generated import UNSTAGED_TRACK_CHALLENGE_COUNT

ROOT = Path(__file__).resolve().parents[1]
STAGES_FILE = "game-stages.yml"

# The main()-driven, live-CTFd-only scripts. Deliberately an explicit list:
# adding a fourth such script is a deliberate act that should also make the
# author read this file and its docstring.
LIVE_SCRIPTS = (
    "scripts/test_staggered_concurrency.py",
    "scripts/test_staggered_smoke.py",
    "scripts/test_export_reconciliation.py",
)

# Below this, an integer cannot be a challenge count for a shipped track
# (the smallest is Krypton at 8, and no track is being added at 1-2 levels),
# and the threshold is what keeps "1/2." list numbering and "exactly one
# audit row" from being reported. Also the threshold the issue proposes.
MIN_HARD_CODE = 10

# An expression is read as a *count of challenges* when something in it names
# a challenge. NOT_A_COUNT then removes the expressions that are about a
# challenge's point value rather than how many there are.
COUNT_HINT = re.compile("challenge", re.IGNORECASE)
NOT_A_COUNT = re.compile(
    r"value|score|point|price|weight|percent|host|port|timeout|interval|limit",
    re.IGNORECASE,
)

# "16/16", "36/36": numerator/denominator, not part of a path, URL, or version.
FRACTION = re.compile(r"(?<![\w./-])(\d+)\s*/\s*(\d+)(?![\w./-])")

# A fraction is only read as a count claim when its line is talking about
# challenges in the first place ("Natas (16/16)"), and only when the two halves
# agree ("all 16 of 16"). Both conditions exist to stay quiet on the things that
# merely look like counts in prose: "1/2." checklist numbering and a note about
# the 200/404 status-code split. A check that fires on those is a check
# maintainers learn to skip.
COUNT_CONTEXT = re.compile(
    r"challenge|level|stage|track|deployed|count|"
    r"\b(natas|krypton|bandit|sentinel|threadline|agent|osint)\b",
    re.IGNORECASE,
)

URL_HOST = re.compile(r"https?://([^/\s\"'`<>]+)", re.IGNORECASE)
LOCAL_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "[::1]", "::1", "::"}


def url_host(authority: str) -> str:
    """The host part of a URL authority, without userinfo or port."""
    host = authority.rsplit("@", 1)[-1]
    head, _, tail = host.rpartition(":")
    return head if head and tail.isdigit() else host


class Finding(NamedTuple):
    """One problem, anchored to the file and line a reviewer must edit."""

    path: str
    line: int
    message: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {self.message}"


# -- manifest-derived challenge counts -----------------------------------------


def allowed_challenge_counts(root: Path = ROOT) -> set[int]:
    """Every challenge count game-stages.yml currently declares.

    That is each stage's ``expected_challenge_count``, the staged total, and
    the total ``validate_generated.py`` expects once the deliberately-unstaged
    AI Copilot Setup track is included (these scripts reconcile a *live CTFd
    instance*, which carries that track's challenges too). A hardcoded count is
    only allowed to be one of these, so the set moves with the manifest: when
    a track gains levels, yesterday's correct literal becomes today's failure.
    """
    # utf-8-sig, not utf-8: a BOM is legal in a committed file and yaml chokes
    # on it, which would turn a stray editor into a spurious CI failure.
    data = yaml.safe_load((root / STAGES_FILE).read_text(encoding="utf-8-sig")) or {}
    stages = data.get("stages") or []
    per_stage = {int(stage["expected_challenge_count"]) for stage in stages}
    staged_total = sum(per_stage)
    return per_stage | {staged_total, staged_total + UNSTAGED_TRACK_CHALLENGE_COUNT}


# -- AST helpers ----------------------------------------------------------------


def fold_int(node: ast.expr) -> int | None:
    """The value of an integer literal expression, or None if it is not one.

    Folds ``59`` and ``35 + 8 + 16`` alike, so writing a total as a sum of
    per-stage literals is caught as readily as writing it out flat.
    """
    if isinstance(node, ast.Constant) and isinstance(node.value, int) and not isinstance(node.value, bool):
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        operand = fold_int(node.operand)
        if operand is not None:
            return operand if isinstance(node.op, ast.UAdd) else -operand
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult)):
        left = fold_int(node.left)
        right = fold_int(node.right)
        if left is None or right is None:
            return None
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        return left * right
    return None


def identifiers(node: ast.AST) -> set[str]:
    """Every name and attribute in an expression.

    Deliberately flat: ``len(admin_challenges)`` is a challenge count even
    though the ``Call`` itself is named ``len`` and the challenge is the
    argument, not the callee.
    """
    found: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Name):
            found.add(child.id)
        elif isinstance(child, ast.Attribute):
            found.add(child.attr)
    return found


def is_challenge_count(node: ast.expr) -> bool:
    names = identifiers(node)
    if any(NOT_A_COUNT.search(name) for name in names):
        return False
    return any(COUNT_HINT.search(name) for name in names)


def describe(counts: set[int]) -> str:
    return "the manifest declares " + ", ".join(str(count) for count in sorted(counts))


# -- the checks -----------------------------------------------------------------


def compare_findings(tree: ast.Module, path: str, allowed: set[int]) -> list[Finding]:
    """Integers pinned against a challenge count must be manifest-declared."""
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Compare):
            continue
        operands = [node.left, *node.comparators]
        for left, _op, right in zip(operands, node.ops, operands[1:]):
            for literal_side, count_side in ((left, right), (right, left)):
                literal = fold_int(literal_side)
                if literal is None or literal < MIN_HARD_CODE or literal in allowed:
                    continue
                if is_challenge_count(count_side):
                    found.append(Finding(
                        path, node.lineno,
                        f"hardcoded challenge count {literal} compared against "
                        f"{ast.unparse(count_side)}; derive it from {STAGES_FILE} "
                        f"({describe(allowed)})",
                    ))
                    break
    return found


def docstring_findings(tree: ast.Module, path: str, allowed: set[int]) -> list[Finding]:
    """``N/N`` in a docstring is a count claim, so it has to match the manifest.

    Only docstrings are scanned, not every string constant: a ``check()``
    label is rendered next to a live value, whereas a docstring is a frozen
    claim about how many challenges a track has. This is the check that would
    have caught "Natas (16/16)" in test_staggered_smoke.py's module docstring.

    Known limit: a claim written with two different numbers ("36/79") is not
    read as a count, because that shape is indistinguishable from the status
    codes and list numbering COUNT_CONTEXT and the equal-halves test exist to
    ignore. The comparison rule is what catches the same drift where it is a
    number the script actually asserts on.
    """
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        docstring = ast.get_docstring(node)
        if not docstring:
            continue
        for offset, line in enumerate(docstring.splitlines()):
            if not COUNT_CONTEXT.search(line):
                continue
            for numerator, denominator in FRACTION.findall(line):
                if int(numerator) != int(denominator):
                    continue
                number = int(numerator)
                if number < MIN_HARD_CODE or number in allowed:
                    continue
                found.append(Finding(
                    path, node.body[0].lineno + offset,
                    f"docstring claims a challenge count of {numerator}/{denominator}, but "
                    f"{number} is not a current manifest count ({describe(allowed)}); "
                    f"reword it or derive the number",
                ))
    return found


def host_findings(tree: ast.Module, path: str) -> list[Finding]:
    """No remote host literals: these only ever run against localhost."""
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        for authority in URL_HOST.findall(node.value):
            host = url_host(authority)
            if host.lower() not in LOCAL_HOSTS:
                found.append(Finding(
                    path, node.lineno,
                    f"hardcoded non-local host {host!r} (in {node.value!r}); the live-CTFd "
                    f"scripts run against a local instance only",
                ))
    return found


def guard_tokens(node: ast.AST) -> set[str]:
    """Names *and* string literals in an expression.

    The ``__main__`` half of ``if __name__ == "__main__"`` is a string
    constant, so ``identifiers()`` alone can never see the whole guard.
    """
    tokens = identifiers(node)
    tokens |= {
        child.value for child in ast.walk(node)
        if isinstance(child, ast.Constant) and isinstance(child.value, str)
    }
    return tokens


def structure_findings(tree: ast.Module, path: str) -> list[Finding]:
    """A live script with no reachable main() is dead weight, not coverage."""
    found = []
    if not any(isinstance(node, ast.FunctionDef) and node.name == "main" for node in tree.body):
        found.append(Finding(path, 1, "no top-level main(); the script could never run"))
    guarded = any(
        isinstance(node, ast.If)
        and {"__name__", "__main__"} <= guard_tokens(node.test)
        and any(
            isinstance(inner, ast.Call)
            and isinstance(inner.func, ast.Name)
            and inner.func.id == "main"
            for inner in ast.walk(node)
        )
        for node in tree.body
    )
    if not guarded:
        found.append(Finding(path, 1, 'no `if __name__ == "__main__":` guard calling main()'))
    return found


def read_source(path: Path) -> str:
    """Source text the way the import machinery reads it.

    ``tokenize.open`` honours a PEP 263 coding cookie and a UTF-8 BOM (one
    file in scripts/ is committed with one); a plain ``encoding="utf-8"`` read
    would report a clean file as unparseable.
    """
    with tokenize.open(path) as handle:
        return handle.read()


def compile_findings(path: Path, relative: str) -> tuple[list[Finding], ast.Module | None]:
    try:
        tree = ast.parse(read_source(path), filename=relative)
    except (OSError, SyntaxError, ValueError) as exc:
        return [Finding(relative, 0, f"cannot be parsed: {exc}")], None
    return [], tree


def exposes_test_cases(source: str) -> bool:
    """True if the module defines something deriving from a *TestCase* base."""
    tree = ast.parse(source)
    return any(
        isinstance(node, ast.ClassDef)
        and any("TestCase" in ast.unparse(base) for base in node.bases)
        for node in ast.walk(tree)
    )


def dead_weight_findings(root: Path) -> list[Finding]:
    """No ``test_*.py`` in scripts/ may be dead weight outside this guard.

    ``unittest discover`` collects nothing from a script with no TestCase, so
    the only ways to keep a new one honest are to give it real test cases or to
    add it to ``LIVE_SCRIPTS`` and let this file police it. A script that does
    neither is the exact situation issue #103 was filed about.
    """
    guarded = {Path(relative).name for relative in LIVE_SCRIPTS}
    found = []
    for path in sorted((root / "scripts").glob("test_*.py")):
        relative = f"scripts/{path.name}"
        if path.name in guarded:
            continue
        try:
            source = read_source(path)
            collects = exposes_test_cases(source)
        except (OSError, SyntaxError, ValueError) as exc:
            found.append(Finding(relative, 0, f"cannot be parsed: {exc}"))
            continue
        if not collects:
            found.append(Finding(
                relative, 0,
                "exposes no unittest.TestCase, so `unittest discover` collects nothing "
                f"from it: either write real test cases or add it to LIVE_SCRIPTS in "
                f"check_live_ctfd_scripts.py",
            ))
    return found


def import_findings(root: Path, scripts: tuple[str, ...] = LIVE_SCRIPTS) -> list[Finding]:
    """Each script must import from the file that was scanned.

    ``unittest discover`` already imports these, so a failure here is a real
    breakage rather than a hypothetical one; the file identity assertion stops
    a same-named module elsewhere on sys.path from standing in for the one
    this check just inspected.
    """
    found = []
    for relative in scripts:
        target = root / relative
        module_name = target.stem
        if not target.is_file():
            found.append(Finding(relative, 0, "file is missing"))
            continue
        try:
            module = importlib.import_module(module_name)
        except Exception as exc:  # noqa: BLE001 - any import error is the finding
            found.append(Finding(relative, 0, f"does not import cleanly: {type(exc).__name__}: {exc}"))
            continue
        imported_from = getattr(module, "__file__", None)
        if imported_from is None or Path(imported_from).resolve() != target.resolve():
            found.append(Finding(
                relative, 0,
                f"imported {module_name!r} from {imported_from!r}, not the file that was scanned",
            ))
    return found


def check_module(relative: str, root: Path = ROOT, allowed: set[int] | None = None) -> list[Finding]:
    """Every static check for one live-CTFd script."""
    if allowed is None:
        allowed = allowed_challenge_counts(root)
    path = root / relative
    if not path.is_file():
        return [Finding(relative, 0, "file is missing")]
    syntax, tree = compile_findings(path, relative)
    if syntax or tree is None:
        return syntax
    return (
        compare_findings(tree, relative, allowed)
        + docstring_findings(tree, relative, allowed)
        + host_findings(tree, relative)
        + structure_findings(tree, relative)
    )


def check(root: Path = ROOT) -> list[Finding]:
    """The whole guard: every finding across the live-CTFd scripts."""
    if not (root / STAGES_FILE).is_file():
        raise FileNotFoundError(f"{STAGES_FILE} not found in {root}; cannot derive challenge counts")
    allowed = allowed_challenge_counts(root)
    found: list[Finding] = []
    for relative in LIVE_SCRIPTS:
        found.extend(check_module(relative, root, allowed))
    found.extend(import_findings(root))
    found.extend(dead_weight_findings(root))
    return found


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    try:
        found = check(root)
    except (FileNotFoundError, KeyError) as exc:
        print(f"error: {exc}")
        return 2

    if found:
        print(f"{len(found)} problem(s) in the live-CTFd test scripts:")
        for finding in found:
            print(f"  {finding}")
        print(
            "\nThese three scripts need a live CTFd instance and are never run by CI "
            "(docs/guides/staggered-live-test-procedure.md has the manual procedure). "
            "This check is the only automated coverage they have: challenge counts must "
            f"come from {STAGES_FILE}, not from literals."
        )
        return 1

    counts = allowed_challenge_counts(root)
    print(
        f"live-CTFd scripts OK: {len(LIVE_SCRIPTS)} scripts compile, import, and are "
        f"reached through main(); no hardcoded challenge count outside {describe(counts)}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
