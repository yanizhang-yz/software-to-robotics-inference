import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_guide import validate


class ValidateGuideTests(unittest.TestCase):
    def make_root(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        return Path(temp.name)

    def write_minimal_guide(self, root: Path) -> None:
        required = [
            "README.md",
            "docs/skill-translation.md",
            "docs/evidence-contract.md",
            "docs/milestones/README.md",
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

    def test_rejects_personal_absolute_paths(self) -> None:
        root = self.make_root()
        self.write_minimal_guide(root)
        (root / "README.md").write_text(
            "# Test\n/Users/example/private/file\n", encoding="utf-8"
        )
        self.assertTrue(
            any("personal absolute path" in error for error in validate(root))
        )


if __name__ == "__main__":
    unittest.main()
