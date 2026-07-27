from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

APPROVED_IDS = {f"M{number}" for number in range(7)}
APPROVED_STATUSES = {"planned", "active", "blocked", "verified"}
REQUIRED_PATHS = {
    "CONTRIBUTING.md",
    "README.md",
    "data/milestones.json",
    "docs/agentic-workflow.md",
    "docs/budget-paths.md",
    "docs/build-log/README.md",
    "docs/contributions.md",
    "docs/skill-translation.md",
    "docs/evidence-contract.md",
    "docs/milestones/README.md",
    "docs/portfolio-map.md",
}
PERSONAL_PATH_PATTERNS = (
    re.compile(r"/Users/[^/\s]+/"),
    re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+\\"),
)
PUBLIC_EVIDENCE_URL_PATTERN = re.compile(
    r"^https://github\.com/yanizhang-yz/[^/?#]+/blob/"
    r"(?:main|[0-9a-fA-F]{40})/[^/?#]+(?:/[^/?#]+)*$"
)
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
MARKDOWN_HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)


def heading_anchor(heading: str) -> str:
    plain = re.sub(r"[`*_~]", "", heading).strip().lower()
    plain = re.sub(r"[^\w\s-]", "", plain)
    return re.sub(r"-+", "-", re.sub(r"\s+", "-", plain))


def heading_anchors(text: str) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for heading in MARKDOWN_HEADING.findall(text):
        anchor = heading_anchor(heading)
        count = counts.get(anchor, 0)
        counts[anchor] = count + 1
        anchors.add(anchor if count == 0 else f"{anchor}-{count}")
    return anchors


def validate_internal_links(root: Path) -> list[str]:
    errors: list[str] = []
    resolved_root = root.resolve()

    for source in sorted(root.rglob("*.md")):
        text = source.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().split(" ", 1)[0]
            if target.lower().startswith(("http://", "https://", "mailto:", "//")):
                continue

            path_text, separator, fragment = target.partition("#")
            destination = source if not path_text else source.parent / unquote(path_text)
            destination = destination.resolve()

            if not destination.is_relative_to(resolved_root):
                errors.append(
                    f"{source.relative_to(root)} links outside repository: {target}"
                )
                continue
            if not destination.is_file():
                errors.append(
                    f"{source.relative_to(root)} has missing internal link target: "
                    f"{target}"
                )
                continue
            if separator:
                anchors = heading_anchors(destination.read_text(encoding="utf-8"))
                if unquote(fragment).lower() not in anchors:
                    errors.append(
                        f"{source.relative_to(root)} has missing heading anchor: "
                        f"{target}"
                    )

    return errors


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    resolved_root = root.resolve()

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
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"milestone record at index {index} must be an object")
            continue

        milestone_id = str(record.get("id", ""))
        status = str(record.get("status", ""))
        guide_path = str(record.get("guide_path", ""))
        evidence_url = record.get("evidence_url")

        if milestone_id in seen_ids:
            errors.append(f"duplicate milestone id: {milestone_id}")
        seen_ids.add(milestone_id)

        if status not in APPROVED_STATUSES:
            errors.append(f"{milestone_id} uses unsupported status: {status}")
        guide_destination = (root / guide_path).resolve()
        try:
            guide_destination.relative_to(resolved_root)
        except ValueError:
            errors.append(
                f"{milestone_id} guide path is outside repository: {guide_path}"
            )
        else:
            if not guide_path or not guide_destination.is_file():
                errors.append(
                    f"{milestone_id} guide path does not exist: {guide_path}"
                )
        if status == "verified" and not (
            isinstance(evidence_url, str)
            and PUBLIC_EVIDENCE_URL_PATTERN.fullmatch(evidence_url)
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
        relative_path = path.relative_to(root)
        if relative_path == Path("scripts/validate_guide.py") or (
            relative_path.parts and relative_path.parts[0] == "tests"
        ):
            continue
        if path.suffix.lower() not in {".md", ".json", ".py", ".yml", ".yaml"}:
            continue
        text = path.read_text(encoding="utf-8")
        if any(pattern.search(text) for pattern in PERSONAL_PATH_PATTERNS):
            errors.append(
                f"{relative_path} contains a personal absolute path"
            )

    errors.extend(validate_internal_links(root))
    return errors


def main() -> int:
    errors = validate(Path.cwd())
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
