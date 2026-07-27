from __future__ import annotations

import json
import re
import sys
from pathlib import Path

APPROVED_IDS = {f"M{number}" for number in range(7)}
APPROVED_STATUSES = {"planned", "active", "blocked", "verified"}
REQUIRED_PATHS = {
    "README.md",
    "data/milestones.json",
    "docs/skill-translation.md",
    "docs/evidence-contract.md",
    "docs/milestones/README.md",
}
PERSONAL_PATH_PATTERNS = (
    re.compile(r"/Users/[^/\s]+/"),
    re.compile(r"[A-Za-z]:\\\\Users\\\\[^\\\\\s]+\\\\"),
)


def validate(root: Path) -> list[str]:
    errors: list[str] = []

    for relative in sorted(REQUIRED_PATHS):
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    milestone_path = root / "data/milestones.json"
    records: list[dict[str, object]] = []
    if milestone_path.is_file():
        try:
            loaded = json.loads(milestone_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid milestone JSON: {exc.msg}")
        else:
            if isinstance(loaded, list):
                records = loaded
            else:
                errors.append("data/milestones.json must contain a list")

    seen_ids: set[str] = set()
    for record in records:
        milestone_id = str(record.get("id", ""))
        status = str(record.get("status", ""))
        guide_path = str(record.get("guide_path", ""))
        evidence_url = record.get("evidence_url")

        if milestone_id in seen_ids:
            errors.append(f"duplicate milestone id: {milestone_id}")
        seen_ids.add(milestone_id)

        if status not in APPROVED_STATUSES:
            errors.append(f"{milestone_id} uses unsupported status: {status}")
        if not guide_path or not (root / guide_path).is_file():
            errors.append(f"{milestone_id} guide path does not exist: {guide_path}")
        if status == "verified" and not (
            isinstance(evidence_url, str)
            and evidence_url.startswith("https://github.com/yanizhang-yz/")
        ):
            errors.append(
                f"{milestone_id} is verified without a public evidence URL"
            )

    if seen_ids != APPROVED_IDS:
        errors.append(
            "milestone ids must be exactly M0 through M6; "
            f"found {sorted(seen_ids)}"
        )

    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in {".md", ".json", ".py", ".yml", ".yaml"}:
            continue
        text = path.read_text(encoding="utf-8")
        if any(pattern.search(text) for pattern in PERSONAL_PATH_PATTERNS):
            errors.append(
                f"{path.relative_to(root)} contains a personal absolute path"
            )

    return errors


def main() -> int:
    errors = validate(Path.cwd())
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
