#!/usr/bin/env python3
"""Validate generated CTFd challenge metadata before deploy or release."""

import argparse
import hashlib
import json
import re
from pathlib import Path

import yaml


EXPECTED_CHALLENGES = 59
EXPECTED_MAPPINGS = 58
EXPECTED_LAUNCHERS = 3
VALID_INSTANCE_TYPES = {"web-app", "single-target", "target-attacker"}
IMAGE_FIELDS = ("image", "target_image", "attacker_image")
DIGEST_REF = re.compile(r"^[^\s@]+@sha256:[0-9a-f]{64}$")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--release", action="store_true", help="require immutable digest image references")
    parser.add_argument("--output", type=Path, help="write a machine-readable validation manifest")
    args = parser.parse_args()

    root = Path("challenges")
    files = sorted(root.glob("*/challenge.yml"))
    errors: list[str] = []
    rows: list[dict] = []
    names: set[str] = set()
    mappings = 0
    launchers = 0

    if len(files) != EXPECTED_CHALLENGES:
        errors.append(f"expected {EXPECTED_CHALLENGES} challenge files, found {len(files)}")

    for path in files:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except Exception as exc:
            errors.append(f"{path}: invalid YAML: {exc}")
            continue

        name = data.get("name")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{path}: missing non-empty name")
        elif name in names:
            errors.append(f"{path}: duplicate challenge name {name!r}")
        else:
            names.add(name)

        for field in ("category", "description", "value", "type", "flags"):
            if field not in data:
                errors.append(f"{path}: missing required CTFd field {field!r}")

        instance_type = data.get("instance_type")
        if instance_type:
            mappings += 1
            if instance_type not in VALID_INSTANCE_TYPES:
                errors.append(f"{path}: invalid instance_type {instance_type!r}")
            required = {
                "web-app": ("image",),
                "single-target": ("image",),
                "target-attacker": ("target_image", "attacker_image"),
            }.get(instance_type, ())
            for field in required:
                if not data.get(field):
                    errors.append(f"{path}: {instance_type} requires {field}")

        if path.parent.name.endswith("start-here"):
            launchers += 1

        images = {field: data[field] for field in IMAGE_FIELDS if data.get(field)}
        if args.release:
            for field, image in images.items():
                if not isinstance(image, str) or not DIGEST_REF.fullmatch(image):
                    errors.append(f"{path}: release {field} must use image@sha256 digest, got {image!r}")

        raw = path.read_bytes()
        rows.append({
            "id": path.parent.name,
            "name": name,
            "instance_type": instance_type,
            "images": images,
            "sha256": hashlib.sha256(raw).hexdigest(),
        })

    if mappings != EXPECTED_MAPPINGS:
        errors.append(f"expected {EXPECTED_MAPPINGS} instance mappings, found {mappings}")
    if launchers != EXPECTED_LAUNCHERS:
        errors.append(f"expected {EXPECTED_LAUNCHERS} start-here launchers, found {launchers}")

    manifest = {
        "passed": not errors,
        "release_mode": args.release,
        "challenge_count": len(files),
        "mapping_count": mappings,
        "launcher_count": launchers,
        "challenges": rows,
        "errors": errors,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"validated {len(files)} challenges, {mappings} mappings, {launchers} launchers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
