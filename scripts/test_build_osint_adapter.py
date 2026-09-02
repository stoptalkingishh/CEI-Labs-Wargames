from __future__ import annotations

import hashlib
import json
import random
import tempfile
import unittest
from pathlib import Path

import build_osint


class _ReviewedFamily:
    name = "osint_investigation"
    version = "0.1.0"
    isolation_level = "artifact"
    required_ports = ()
    requires_internet = False

    _cases = (
        ("Image provenance", {"kind": "aliases", "answers": ["Harbor Light"]}),
        (
            "Movement corroboration",
            {
                "kind": "identifier",
                "value": "IMO1234567",
                "strip_prefixes": ["IMO"],
                "strip_separators": True,
            },
        ),
        (
            "Public record corroboration",
            {
                "kind": "multipart",
                "fields": {
                    "entity": {"kind": "aliases", "answers": ["Aster Research"]},
                    "registration": {
                        "kind": "identifier",
                        "value": "AR-2048",
                        "strip_separators": True,
                    },
                },
            },
        ),
    )

    def render(self, spec, rng: random.Random, cve_record=None):
        title, verifier = self._cases[rng.randrange(len(self._cases))]
        evidence = f"Reviewed evidence for {title}.\n"
        evidence_path = "public/evidence/observation.txt"
        manifest = {
            evidence_path: {
                "sha256": hashlib.sha256(evidence.encode()).hexdigest(),
                "size": len(evidence.encode()),
            }
        }
        return {
            "public/briefing.md": f"# {title}\n\nInvestigate the supplied evidence.\n",
            "public/worksheet.md": "Record observations and confidence.\n",
            "public/evidence/observation.txt": evidence,
            "public/evidence-manifest.json": json.dumps(manifest, sort_keys=True) + "\n",
            "private/answer.json": json.dumps(verifier, sort_keys=True) + "\n",
            "private/solution.md": "Private solution.\n",
            "private/ground-truth.json": "{}\n",
            "private/provenance.json": '{"safety_privacy_reviewed": true}\n',
        }


class OsintAdapterTests(unittest.TestCase):
    def test_export_is_deterministic_unique_and_public_only(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_manifest = build_osint.export_pilot(
                _ReviewedFamily(), Path(first), release_state="hidden"
            )
            second_manifest = build_osint.export_pilot(
                _ReviewedFamily(), Path(second), release_state="hidden"
            )
            self.assertEqual(first_manifest, second_manifest)
            self.assertEqual(len(first_manifest["challenges"]), 3)
            self.assertEqual(
                len({entry["public_bundle_sha256"] for entry in first_manifest["challenges"]}),
                3,
            )
            first_files = {
                path.relative_to(first).as_posix(): path.read_bytes()
                for path in sorted(Path(first).rglob("*"))
                if path.is_file()
            }
            second_files = {
                path.relative_to(second).as_posix(): path.read_bytes()
                for path in sorted(Path(second).rglob("*"))
                if path.is_file()
            }
            self.assertEqual(first_files, second_files)
            self.assertFalse(any("private" in path.split("/") for path in first_files))
            downloadable = b"\n".join(
                body for path, body in first_files.items() if "/files/" in path
            )
            for secret in (b"Harbor Light", b"IMO1234567", b"Aster Research", b"AR-2048"):
                self.assertNotIn(secret, downloadable)

    def test_export_uses_typed_answer_flags_with_full_verifier_specs(self) -> None:
        expected = {title: verifier for title, verifier in _ReviewedFamily._cases}

        with tempfile.TemporaryDirectory() as output:
            manifest = build_osint.export_pilot(_ReviewedFamily(), Path(output))

            for challenge in manifest["challenges"]:
                challenge_yaml = (
                    Path(output) / challenge["id"] / "challenge.yml"
                ).read_text(encoding="utf-8")
                lines = challenge_yaml.splitlines()
                flag_fields = {}
                for line in lines:
                    stripped = line.strip()
                    if stripped.startswith("- "):
                        stripped = stripped[2:]
                    if ": " not in stripped:
                        continue
                    key, value = stripped.split(": ", 1)
                    if key in {"type", "content", "data"}:
                        flag_fields[key] = value

                self.assertEqual(set(flag_fields), {"type", "content", "data"})
                self.assertEqual(json.loads(flag_fields["type"]), "typed_answer")
                self.assertEqual(
                    json.loads(flag_fields["content"]),
                    "ctfgenerator-answer-spec-v1",
                )
                encoded_spec = json.loads(flag_fields["data"])
                self.assertEqual(json.loads(encoded_spec), expected[challenge["name"]])
                self.assertNotIn(f'  - {json.dumps(build_osint.canonical_answer(expected[challenge["name"]]))}', lines)

    def test_typed_flag_export_bumps_manifest_and_challenge_versions(self) -> None:
        with tempfile.TemporaryDirectory() as output:
            manifest = build_osint.export_pilot(_ReviewedFamily(), Path(output))

            self.assertEqual(manifest["schema_version"], 3)
            for challenge in manifest["challenges"]:
                challenge_yaml = (
                    Path(output) / challenge["id"] / "challenge.yml"
                ).read_text(encoding="utf-8")
                self.assertIn('version: "1.1"', challenge_yaml.splitlines())

    def test_canonical_answers_come_from_verifier_specs(self) -> None:
        self.assertEqual(
            build_osint.canonical_answer({"kind": "aliases", "answers": ["Harbor Light"]}),
            "Harbor Light",
        )
        self.assertEqual(
            build_osint.canonical_answer({"kind": "identifier", "value": "IMO1234567"}),
            "IMO1234567",
        )
        self.assertEqual(
            build_osint.canonical_answer(
                {
                    "kind": "multipart",
                    "fields": {
                        "entity": {"kind": "aliases", "answers": ["Aster Research"]},
                        "registration": {"kind": "identifier", "value": "AR-2048"},
                    },
                }
            ),
            '{"entity":"Aster Research","registration":"AR-2048"}',
        )

    def test_export_rejects_unsafe_paths_and_evidence_hash_drift(self) -> None:
        class UnsafePathFamily(_ReviewedFamily):
            def render(self, spec, rng, cve_record=None):
                rendered = super().render(spec, rng, cve_record)
                rendered["public/../../escape.txt"] = "escape\n"
                return rendered

        class DriftedEvidenceFamily(_ReviewedFamily):
            def render(self, spec, rng, cve_record=None):
                rendered = super().render(spec, rng, cve_record)
                rendered["public/evidence/observation.txt"] = "tampered\n"
                return rendered

        with tempfile.TemporaryDirectory() as output:
            with self.assertRaisesRegex(ValueError, "unsafe public artifact path"):
                build_osint.export_pilot(UnsafePathFamily(), Path(output))
        with tempfile.TemporaryDirectory() as output:
            with self.assertRaisesRegex(ValueError, "evidence manifest mismatch"):
                build_osint.export_pilot(DriftedEvidenceFamily(), Path(output))

    def test_osint_pilot_has_no_loom_concept(self) -> None:
        """The neutral OSINT pilot (plugin adapter + its docs/archive) must stay
        lore-free. Named wargames such as Threadline deliberately carry the Loom
        theme and are exempt."""
        root = Path(__file__).resolve().parents[1]
        needle = ("the " + "loom").casefold()
        extensions = {".md", ".py", ".json", ".yaml", ".yml"}

        def _files(base):
            if base.is_file():
                return [base]
            return sorted(
                p for p in base.rglob("*")
                if p.is_file() and p.suffix in extensions
            )

        scopes = [
            root / "scripts" / "build_osint.py",
            root / "docs" / "tracks" / "osint",
        ]
        checked: list[Path] = []
        for base in scopes:
            for path in _files(base):
                checked.append(path)
                self.assertNotIn(
                    needle,
                    path.read_text(encoding="utf-8").casefold(),
                    path.as_posix(),
                )
        # Guard against the scope collapsing silently (e.g. a rename).
        self.assertTrue(checked, "no-lore guard scope unexpectedly empty")


if __name__ == "__main__":
    unittest.main()
