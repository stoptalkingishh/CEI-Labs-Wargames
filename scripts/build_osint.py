#!/usr/bin/env python3
"""Export reviewed OSINT plugin bundles into CTFd challenge folders.

The plugin is the canonical source for evidence, private ground truth, and answer
specifications. This adapter copies only ``public/`` artifacts into downloadable
CTFd files and embeds ``private/answer.json`` only as private typed CTFd flag
metadata. It never carries forward the legacy placeholder campaign or unrelated
project lore.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import shutil
from importlib import metadata
from pathlib import Path, PurePosixPath
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
BASE_DIR = ROOT / "osint"
ENTRY_POINT_GROUP = "ctf_generator.families"
ENTRY_POINT_NAME = "osint_investigation"
PILOT_SIZE = 3
_VALID_RELEASE_STATES = ("hidden", "visible")


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value


def canonical_answer(spec: object) -> str:
    """Return one deterministic CTFd answer from a typed verifier specification."""
    if not isinstance(spec, dict):
        raise ValueError("answer verifier must be an object")
    kind = spec.get("kind")
    if kind == "aliases":
        answers = spec.get("answers")
        if not isinstance(answers, list) or not answers:
            raise ValueError("aliases verifier requires answers")
        return _text(answers[0], "aliases.answers[0]")
    if kind == "coordinate":
        latitude = spec.get("latitude")
        longitude = spec.get("longitude")
        if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
            raise ValueError("coordinate verifier requires numeric latitude and longitude")
        return f"{latitude},{longitude}"
    if kind == "identifier":
        return _text(spec.get("value"), "identifier.value")
    if kind == "multipart":
        fields = spec.get("fields")
        if not isinstance(fields, dict) or not fields:
            raise ValueError("multipart verifier requires fields")
        canonical = {str(name): canonical_answer(field) for name, field in fields.items()}
        return json.dumps(canonical, sort_keys=True, separators=(",", ":"))
    raise ValueError(f"unsupported answer verifier kind: {kind!r}")


def _as_bytes(value: object, path: str) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    content = getattr(value, "content", None)
    if isinstance(content, bytes):
        return content
    raise TypeError(f"rendered artifact {path!r} must be str, bytes, or RenderedFile")


def _bundle_digest(rendered: dict[str, object]) -> str:
    digest = hashlib.sha256()
    for path in sorted(path for path in rendered if path.startswith("public/")):
        digest.update(path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(_as_bytes(rendered[path], path))
        digest.update(b"\0")
    return digest.hexdigest()


def _validate_public_artifacts(rendered: dict[str, object]) -> None:
    for path in rendered:
        if not path.startswith("public/"):
            continue
        artifact = PurePosixPath(path)
        if artifact.is_absolute() or ".." in artifact.parts or artifact.parts[0] != "public":
            raise ValueError(f"unsafe public artifact path: {path!r}")

    manifest_path = "public/evidence-manifest.json"
    manifest = json.loads(_as_bytes(rendered[manifest_path], manifest_path))
    if not isinstance(manifest, dict):
        raise ValueError("evidence manifest must be an object")
    evidence_paths = {
        path for path in rendered if path.startswith("public/evidence/")
    }
    if set(manifest) != evidence_paths:
        raise ValueError("evidence manifest mismatch: file list differs")
    for path in sorted(evidence_paths):
        record = manifest.get(path)
        if not isinstance(record, dict):
            raise ValueError(f"evidence manifest mismatch: malformed record for {path}")
        content = _as_bytes(rendered[path], path)
        if record.get("size") != len(content) or record.get("sha256") != hashlib.sha256(content).hexdigest():
            raise ValueError(f"evidence manifest mismatch: digest or size differs for {path}")


def _pilot_bundles(family: object, count: int = PILOT_SIZE) -> list[tuple[str, dict[str, object]]]:
    if getattr(family, "isolation_level", None) != "artifact":
        raise ValueError("OSINT family must use artifact isolation")
    if tuple(getattr(family, "required_ports", ())) != ():
        raise ValueError("OSINT artifact family must declare no ports")
    if bool(getattr(family, "requires_internet", True)):
        raise ValueError("OSINT artifact family must not require internet")

    render = getattr(family, "render", None)
    if not callable(render):
        raise TypeError("OSINT family has no renderer")
    selected: list[tuple[str, dict[str, object]]] = []
    seen: set[str] = set()
    for attempt in range(256):
        seed_text = f"cei-osint-pilot-{attempt:03d}"
        seed_int = int(hashlib.sha256(seed_text.encode("utf-8")).hexdigest()[:16], 16)
        rendered = dict(render(None, random.Random(seed_int), None))
        digest = _bundle_digest(rendered)
        if digest in seen:
            continue
        required = {
            "public/briefing.md",
            "public/worksheet.md",
            "public/evidence-manifest.json",
            "private/answer.json",
            "private/provenance.json",
        }
        missing = sorted(required - set(rendered))
        if missing:
            raise ValueError(f"reviewed bundle is missing required artifacts: {missing}")
        _validate_public_artifacts(rendered)
        provenance = json.loads(_as_bytes(rendered["private/provenance.json"], "private/provenance.json"))
        if provenance.get("safety_privacy_reviewed") is not True:
            raise ValueError("pilot bundle lacks an affirmative safety/privacy review")
        seen.add(digest)
        selected.append((seed_text, rendered))
        if len(selected) == count:
            return selected
    raise ValueError(f"plugin exposed only {len(selected)} unique reviewed bundles; need {count}")


def _yaml_scalar(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _write_challenge(
    output_dir: Path,
    index: int,
    seed: str,
    rendered: dict[str, object],
    release_state: str,
) -> dict[str, object]:
    digest = _bundle_digest(rendered)
    challenge_id = f"osint-pilot-{index:02d}-{digest[:8]}"
    challenge_dir = output_dir / challenge_id
    files_dir = challenge_dir / "files"
    files_dir.mkdir(parents=True, exist_ok=True)

    briefing = _as_bytes(rendered["public/briefing.md"], "public/briefing.md").decode("utf-8")
    title = next((line[2:].strip() for line in briefing.splitlines() if line.startswith("# ")), challenge_id)
    public_files: list[str] = []
    public_hashes: dict[str, str] = {}
    for path in sorted(path for path in rendered if path.startswith("public/")):
        relative = Path(path).relative_to("public")
        destination = files_dir / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        content = _as_bytes(rendered[path], path)
        destination.write_bytes(content)
        exported = (Path("files") / relative).as_posix()
        public_files.append(exported)
        public_hashes[exported] = hashlib.sha256(content).hexdigest()

    answer_spec = json.loads(_as_bytes(rendered["private/answer.json"], "private/answer.json"))
    canonical_answer(answer_spec)
    answer_data = json.dumps(
        answer_spec, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    description = "\n".join(f"  {line}" for line in briefing.rstrip().splitlines())
    files_yaml = "".join(f"  - {_yaml_scalar(path)}\n" for path in public_files)
    challenge_yaml = (
        f"name: {_yaml_scalar(title)}\n"
        'author: "CEI Labs (reviewed OSINT pilot)"\n'
        'category: "OSINT"\n'
        "description: |\n"
        f"{description}\n"
        "value: 150\n"
        "type: standard\n"
        "flags:\n"
        f"  - type: {_yaml_scalar('typed_answer')}\n"
        f"    content: {_yaml_scalar('ctfgenerator-answer-spec-v1')}\n"
        f"    data: {_yaml_scalar(answer_data)}\n"
        f"state: {release_state}\n"
        'version: "1.1"\n'
        "files:\n"
        f"{files_yaml}"
    )
    (challenge_dir / "challenge.yml").write_text(challenge_yaml, encoding="utf-8")
    return {
        "id": challenge_id,
        "name": title,
        "plugin_seed": seed,
        "public_bundle_sha256": digest,
        "public_files": public_hashes,
    }


def export_pilot(
    family: object,
    output_dir: Path,
    *,
    release_state: str = "hidden",
) -> dict[str, object]:
    """Export the complete unique reviewed pilot and return its public manifest."""
    release_state = release_state.strip().lower()
    if release_state not in _VALID_RELEASE_STATES:
        raise ValueError(f"release_state must be one of {_VALID_RELEASE_STATES}")
    output_dir = Path(output_dir)
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    challenges = [
        _write_challenge(output_dir, index, seed, rendered, release_state)
        for index, (seed, rendered) in enumerate(_pilot_bundles(family), start=1)
    ]
    manifest: dict[str, object] = {
        "schema_version": 3,
        "track": "osint",
        "release_state": release_state,
        "source_plugin": getattr(family, "name", ENTRY_POINT_NAME),
        "source_plugin_version": getattr(family, "version", "unknown"),
        "challenges": challenges,
    }
    (output_dir / "osint-training.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest


def load_installed_family() -> object:
    """Load the operator-installed trusted OSINT plugin entry point."""
    matches = [
        entry
        for entry in metadata.entry_points(group=ENTRY_POINT_GROUP)
        if entry.name == ENTRY_POINT_NAME
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"expected one installed {ENTRY_POINT_GROUP}:{ENTRY_POINT_NAME} entry point; "
            f"found {len(matches)}"
        )
    loaded: Any = matches[0].load()
    return loaded() if callable(loaded) else loaded


def main_build() -> None:
    release_state = os.environ.get("CEI_OSINT_RELEASE_STATE", "hidden")
    manifest = export_pilot(load_installed_family(), BASE_DIR, release_state=release_state)
    print(
        f"Generated {len(manifest['challenges'])} reviewed OSINT pilot challenges "
        f"into '{BASE_DIR}' (state={manifest['release_state']})."
    )


if __name__ == "__main__":
    main_build()
