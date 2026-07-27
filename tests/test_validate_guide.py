import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_guide import validate


class ValidateGuideTests(unittest.TestCase):
    def test_repository_contract_passes(self) -> None:
        repository_root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate(repository_root), [])

    def make_root(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        return Path(temp.name)

    def write_minimal_guide(self, root: Path) -> None:
        required = [
            "CONTRIBUTING.md",
            "README.md",
            "docs/agentic-workflow.md",
            "docs/budget-paths.md",
            "docs/build-log/README.md",
            "docs/contributions.md",
            "docs/skill-translation.md",
            "docs/evidence-contract.md",
            "docs/milestones/README.md",
            "docs/portfolio-map.md",
        ]
        for relative in required:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# Test\n", encoding="utf-8")

        milestone_dir = root / "docs/milestones"
        records = []
        for number in range(7):
            milestone_id = f"M{number}"
            guide_path = f"docs/milestones/m{number}.md"
            (root / guide_path).write_text(f"# {milestone_id}\n", encoding="utf-8")
            records.append(
                {
                    "id": milestone_id,
                    "title": f"Milestone {number}",
                    "status": "planned",
                    "guide_path": guide_path,
                    "evidence_url": None,
                }
            )
        data = root / "data/milestones.json"
        data.parent.mkdir(parents=True, exist_ok=True)
        data.write_text(json.dumps(records), encoding="utf-8")

    def test_minimal_guide_is_valid(self) -> None:
        root = self.make_root()
        self.write_minimal_guide(root)
        self.assertEqual(validate(root), [])

    def test_rejects_missing_internal_file(self) -> None:
        root = self.make_root()
        self.write_minimal_guide(root)
        (root / "README.md").write_text(
            "# Test\n[missing](docs/missing.md)\n", encoding="utf-8"
        )
        self.assertTrue(
            any("missing internal link target" in error for error in validate(root))
        )

    def test_accepts_existing_heading_anchor(self) -> None:
        root = self.make_root()
        self.write_minimal_guide(root)
        target = root / "docs/target.md"
        target.write_text("# Target\n\n## Expected Heading\n", encoding="utf-8")
        (root / "README.md").write_text(
            "# Test\n[target](docs/target.md#expected-heading)\n",
            encoding="utf-8",
        )
        self.assertEqual(validate(root), [])

    def test_ignores_case_insensitive_external_link_schemes(self) -> None:
        root = self.make_root()
        self.write_minimal_guide(root)
        (root / "README.md").write_text(
            "# Test\n"
            "[http](HTTP://example.com/path)\n"
            "[https](HTTPS://example.com/path)\n"
            "[email](MAILTO:hello@example.com)\n",
            encoding="utf-8",
        )
        self.assertEqual(validate(root), [])

    def test_ignores_protocol_relative_external_links(self) -> None:
        root = self.make_root()
        self.write_minimal_guide(root)
        (root / "README.md").write_text(
            "# Test\n[external](//cdn.example.com/guide.md)\n", encoding="utf-8"
        )
        self.assertEqual(validate(root), [])

    def test_accepts_duplicate_heading_anchor_suffixes(self) -> None:
        root = self.make_root()
        self.write_minimal_guide(root)
        target = root / "docs/target.md"
        target.write_text(
            "# Target\n\n## Overview\n\n## Overview\n\n## Overview\n",
            encoding="utf-8",
        )
        (root / "README.md").write_text(
            "# Test\n"
            "[first](docs/target.md#overview)\n"
            "[second](docs/target.md#overview-1)\n"
            "[third](docs/target.md#overview-2)\n",
            encoding="utf-8",
        )
        self.assertEqual(validate(root), [])

    def test_decodes_percent_encoded_internal_link_paths(self) -> None:
        root = self.make_root()
        self.write_minimal_guide(root)
        target = root / "docs/space name.md"
        target.write_text("# Target\n", encoding="utf-8")
        (root / "README.md").write_text(
            "# Test\n[target](docs/space%20name.md)\n", encoding="utf-8"
        )
        self.assertEqual(validate(root), [])

    def test_rejects_internal_links_outside_repository(self) -> None:
        root = self.make_root()
        self.write_minimal_guide(root)
        (root / "README.md").write_text(
            "# Test\n[outside](../outside.md)\n", encoding="utf-8"
        )
        self.assertIn(
            "README.md links outside repository: ../outside.md", validate(root)
        )

    def test_reports_internal_link_errors_in_source_path_order(self) -> None:
        root = self.make_root()
        self.write_minimal_guide(root)
        for relative in ("docs/z-source.md", "docs/a-source.md"):
            (root / relative).write_text(
                "# Test\n[missing](missing.md)\n", encoding="utf-8"
            )

        self.assertEqual(
            validate(root),
            [
                "docs/a-source.md has missing internal link target: missing.md",
                "docs/z-source.md has missing internal link target: missing.md",
            ],
        )

    def test_rejects_unknown_status(self) -> None:
        root = self.make_root()
        self.write_minimal_guide(root)
        path = root / "data/milestones.json"
        records = json.loads(path.read_text(encoding="utf-8"))
        records[0]["status"] = "done"
        path.write_text(json.dumps(records), encoding="utf-8")
        self.assertIn("M0 uses unsupported status: done", validate(root))

    def test_verified_requires_public_evidence(self) -> None:
        root = self.make_root()
        self.write_minimal_guide(root)
        path = root / "data/milestones.json"
        records = json.loads(path.read_text(encoding="utf-8"))
        records[0]["status"] = "verified"
        path.write_text(json.dumps(records), encoding="utf-8")
        self.assertIn("M0 is verified without a public evidence URL", validate(root))

    def test_verified_accepts_public_github_blob_evidence(self) -> None:
        root = self.make_root()
        self.write_minimal_guide(root)
        path = root / "data/milestones.json"
        records = json.loads(path.read_text(encoding="utf-8"))
        records[0]["status"] = "verified"

        for evidence_url in (
            "https://github.com/yanizhang-yz/project/blob/main/evidence/result.md",
            "https://github.com/yanizhang-yz/project/blob/"
            "0123456789abcdef0123456789abcdef01234567/evidence/result.md",
        ):
            with self.subTest(evidence_url=evidence_url):
                records[0]["evidence_url"] = evidence_url
                path.write_text(json.dumps(records), encoding="utf-8")
                self.assertNotIn(
                    "M0 is verified without a public evidence URL", validate(root)
                )

    def test_verified_rejects_non_artifact_evidence_urls(self) -> None:
        root = self.make_root()
        self.write_minimal_guide(root)
        path = root / "data/milestones.json"
        records = json.loads(path.read_text(encoding="utf-8"))
        records[0]["status"] = "verified"

        invalid_urls = (
            "https://github.com/yanizhang-yz",
            "https://github.com/yanizhang-yz/project",
            "https://github.com/yanizhang-yz/project/tree/main/evidence",
            "https://github.com/yanizhang-yz/project/blob/main/",
            "https://github.com/yanizhang-yz/project/blob/main//",
            "https://github.com/yanizhang-yz/project/blob/main?file=evidence.md",
            "https://github.com/yanizhang-yz/project/blob/main#evidence.md",
            "https://github.com/other-owner/project/blob/main/evidence.md",
            "https://example.com/yanizhang-yz/project/blob/main/evidence.md",
        )
        for evidence_url in invalid_urls:
            with self.subTest(evidence_url=evidence_url):
                records[0]["evidence_url"] = evidence_url
                path.write_text(json.dumps(records), encoding="utf-8")
                self.assertIn(
                    "M0 is verified without a public evidence URL", validate(root)
                )

    def test_rejects_non_object_milestone_records(self) -> None:
        root = self.make_root()
        self.write_minimal_guide(root)
        path = root / "data/milestones.json"
        records = json.loads(path.read_text(encoding="utf-8"))
        records[0] = "M0"
        path.write_text(json.dumps(records), encoding="utf-8")
        self.assertIn(
            "milestone record at index 0 must be an object", validate(root)
        )

    def test_rejects_guide_paths_outside_the_repository(self) -> None:
        root = self.make_root()
        self.write_minimal_guide(root)
        path = root / "data/milestones.json"
        records = json.loads(path.read_text(encoding="utf-8"))

        for guide_path in ("../outside.md", "/etc/passwd"):
            with self.subTest(guide_path=guide_path):
                records[0]["guide_path"] = guide_path
                path.write_text(json.dumps(records), encoding="utf-8")
                self.assertIn(
                    f"M0 guide path is outside repository: {guide_path}",
                    validate(root),
                )

    def test_rejects_personal_absolute_paths(self) -> None:
        root = self.make_root()
        self.write_minimal_guide(root)
        (root / "README.md").write_text(
            "# Test\n/Users/example/private/file\n", encoding="utf-8"
        )
        self.assertTrue(
            any("personal absolute path" in error for error in validate(root))
        )

    def test_rejects_windows_personal_absolute_paths(self) -> None:
        root = self.make_root()
        self.write_minimal_guide(root)
        (root / "README.md").write_text(
            r"# Test\nC:\Users\alice\private\file\n", encoding="utf-8"
        )
        self.assertTrue(
            any("personal absolute path" in error for error in validate(root))
        )

    def test_ignores_personal_path_literals_in_validator_and_tests(self) -> None:
        root = self.make_root()
        self.write_minimal_guide(root)
        validator = root / "scripts/validate_guide.py"
        validator.parent.mkdir(parents=True, exist_ok=True)
        validator.write_text("PATH = '/Users/example/private/file'\n", encoding="utf-8")
        test_control = root / "tests/test_control.py"
        test_control.parent.mkdir(parents=True, exist_ok=True)
        test_control.write_text(
            "PATH = '/Users/example/private/file'\n", encoding="utf-8"
        )

        self.assertEqual(validate(root), [])

    def test_rejects_personal_paths_in_other_python_files(self) -> None:
        root = self.make_root()
        self.write_minimal_guide(root)
        helper = root / "scripts/helper.py"
        helper.parent.mkdir(parents=True, exist_ok=True)
        helper.write_text("PATH = '/Users/example/private/file'\n", encoding="utf-8")

        self.assertIn(
            "scripts/helper.py contains a personal absolute path", validate(root)
        )


if __name__ == "__main__":
    unittest.main()
