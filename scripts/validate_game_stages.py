#!/usr/bin/env python3
"""Read-only consistency check for game-stages.yml and challenge builders."""
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "game-stages.yml"


def _scalar(value):
    value = value.strip()
    if value.startswith(('"', "'")):
        return ast.literal_eval(value)
    try:
        return int(value)
    except ValueError:
        return value


def load_manifest(path):
    """Parse this repository's deliberately small, flat stage manifest."""
    result = {"stages": []}
    current = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line == "stages:":
            continue
        if line.startswith("- "):
            current = {}
            result["stages"].append(current)
            line = line[2:]
        key, separator, value = line.partition(":")
        if not separator:
            raise ValueError(f"invalid manifest line: {raw_line}")
        target = current if current is not None else result
        target[key.strip()] = _scalar(value)
    return result


def load_builder_data(path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(target, ast.Name) and target.id == "challenges_data" for target in targets):
                if not isinstance(node.value, (ast.List, ast.Tuple)):
                    raise ValueError("challenges_data is not a literal list")
                rows = []
                for item in node.value.elts:
                    if not isinstance(item, ast.Dict):
                        raise ValueError("challenge entry is not a dictionary")
                    fields = {ast.literal_eval(key): value for key, value in zip(item.keys, item.values)}
                    if "id" not in fields:
                        raise ValueError("challenge entry has no id")
                    rows.append({"id": ast.literal_eval(fields["id"])})
                return rows
    raise ValueError("does not define a literal challenges_data list")


def validate(root=ROOT):
    errors = []
    manifest = load_manifest(root / "game-stages.yml")
    stages = manifest.get("stages") or []
    if manifest.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if len(stages) != 3:
        errors.append(f"manifest must contain exactly 3 stages; found {len(stages)}")

    required = {"order", "slug", "name", "category", "challenge_prefix", "start_challenge", "expected_challenge_count"}
    slugs, categories, orders = set(), set(), set()
    for stage in stages:
        missing = required - set(stage)
        if missing:
            errors.append(f"stage {stage.get('slug', '<unknown>')} missing: {', '.join(sorted(missing))}")
            continue
        slug = stage["slug"]
        for value, seen, label in ((slug, slugs, "slug"), (stage["category"], categories, "category"), (stage["order"], orders, "order")):
            if value in seen:
                errors.append(f"duplicate {label}: {value}")
            seen.add(value)

        builder = root / "scripts" / f"build_{slug}.py"
        if not builder.exists():
            errors.append(f"{slug}: missing {builder.relative_to(root)}")
            continue
        try:
            data = load_builder_data(builder)
        except (SyntaxError, ValueError) as exc:
            errors.append(f"{slug}: cannot inspect builder: {exc}")
            continue
        ids = [item.get("id") for item in data]
        if len(ids) != stage["expected_challenge_count"]:
            errors.append(f"{slug}: builder count {len(ids)} != expected {stage['expected_challenge_count']}")
        if len(ids) != len(set(ids)):
            errors.append(f"{slug}: duplicate challenge id in builder")
        if stage["start_challenge"] not in ids:
            errors.append(f"{slug}: missing start challenge {stage['start_challenge']}")
        bad_ids = [challenge_id for challenge_id in ids if not challenge_id or not challenge_id.startswith(stage["challenge_prefix"])]
        if bad_ids:
            errors.append(f"{slug}: ids outside prefix {stage['challenge_prefix']}: {bad_ids}")
        expected_category_line = f'category: "{stage["category"]}"'
        if expected_category_line not in builder.read_text(encoding="utf-8"):
            errors.append(f"{slug}: builder does not emit exact category {stage['category']!r}")

        generated = root / "challenges"
        if generated.exists():
            generated_ids = set(ids)
            existing_ids = {path.name for path in generated.iterdir() if path.is_dir() and path.name.startswith(stage["challenge_prefix"])}
            if existing_ids != generated_ids:
                errors.append(f"{slug}: generated ids differ (missing={sorted(generated_ids-existing_ids)}, extra={sorted(existing_ids-generated_ids)})")
            for challenge_id in sorted(existing_ids & generated_ids):
                challenge_file = generated / challenge_id / "challenge.yml"
                if not challenge_file.exists():
                    errors.append(f"{slug}: {challenge_id} has no challenge.yml")
                    continue
                text = challenge_file.read_text(encoding="utf-8")
                match = re.search(r'^category:\s*["\']?([^"\'\r\n]+)', text, re.MULTILINE)
                category = match.group(1).strip() if match else None
                if category != stage["category"]:
                    errors.append(f"{slug}: {challenge_id} category is {category!r}")
    return errors


def main():
    errors = validate()
    if errors:
        print("Game-stage validation FAILED:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Game-stage validation passed: Bandit 35, Krypton 8, Natas 16.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
