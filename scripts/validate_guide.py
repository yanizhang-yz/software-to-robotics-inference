from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

APPROVED_IDS = {f"M{number}" for number in range(7)}
APPROVED_STATUSES = {"planned", "active", "blocked", "verified"}
MILESTONE_FIELDS = {
    "evidence_url",
    "guide_path",
    "id",
    "status",
    "title",
}
REQUIRED_MILESTONE_SECTIONS = (
    "Why This Matters",
    "Prerequisites",
    "Learn",
    "Build",
    "Measure",
    "Present",
    "Hardware-Free Path",
    "Advanced Path",
    "Completion Gate",
    "Evidence",
)
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
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
MARKDOWN_HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
MARKDOWN_H1 = re.compile(r"^#(?!#)\s+(.+?)\s*$", re.MULTILINE)
MARKDOWN_H2 = re.compile(r"^##(?!#)\s+(.+?)\s*$", re.MULTILINE)
PAGE_STATUS = re.compile(
    r"^Status: (planned|active|blocked|verified)\s*$", re.MULTILINE
)
COMMIT_REF = re.compile(r"^[0-9a-fA-F]{40}$")


def heading_anchor(heading: str) -> str:
    plain = re.sub(r"[`*_~]", "", heading).strip().lower()
    plain = re.sub(r"[^\w\s-]", "", plain)
    return re.sub(r"-+", "-", re.sub(r"\s+", "-", plain))


def heading_anchors(text: str) -> set[str]:
    anchors: set[str] = set()
    for heading in MARKDOWN_HEADING.findall(text):
        base = heading_anchor(heading)
        anchor = base
        suffix = 1
        while anchor in anchors:
            anchor = f"{base}-{suffix}"
            suffix += 1
        anchors.add(anchor)
    return anchors


def is_public_evidence_url(value: object) -> bool:
    if not isinstance(value, str):
        return False

    try:
        parsed = urlsplit(value)
    except ValueError:
        return False

    if (
        parsed.scheme != "https"
        or parsed.netloc != "github.com"
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
    ):
        return False

    raw_segments = parsed.path.split("/")
    if raw_segments[0] != "" or any(not segment for segment in raw_segments[1:]):
        return False
    if len(raw_segments) < 6:
        return False

    decoded_segments: list[str] = []
    for raw_segment in raw_segments[1:]:
        decoded_segment = unquote(raw_segment)
        if (
            decoded_segment in {"", ".", ".."}
            or "/" in decoded_segment
            or "\\" in decoded_segment
        ):
            return False
        decoded_segments.append(decoded_segment)

    raw_owner, _, raw_blob, raw_reference, *_ = raw_segments[1:]
    _, repository, _, _, *artifact = decoded_segments
    return (
        raw_owner == "yanizhang-yz"
        and repository != ""
        and raw_blob == "blob"
        and (
            raw_reference == "main"
            or COMMIT_REF.fullmatch(raw_reference) is not None
        )
        and bool(artifact)
    )


def validate_milestone_page(
    milestone_id: str, status: str, guide_path: str, text: str
) -> list[str]:
    errors: list[str] = []
    h1_match = MARKDOWN_H1.search(text)
    h1 = h1_match.group(1) if h1_match else ""
    if not re.search(
        rf"(?<![A-Za-z0-9]){re.escape(milestone_id)}(?![A-Za-z0-9])", h1
    ):
        errors.append(
            f"{milestone_id} guide page H1 does not identify {milestone_id}"
        )

    status_match = PAGE_STATUS.search(text)
    if status_match is None:
        errors.append(f"{milestone_id} guide page is missing a valid Status line")
    elif status_match.group(1) != status:
        errors.append(
            f"{milestone_id} guide page status {status_match.group(1)} "
            f"does not match milestone data status {status}"
        )

    section_matches = list(MARKDOWN_H2.finditer(text))
    sections = {match.group(1) for match in section_matches}
    for required_section in REQUIRED_MILESTONE_SECTIONS:
        if required_section not in sections:
            errors.append(
                f"{milestone_id} guide page is missing required section: "
                f"{required_section}"
            )

    for index, match in enumerate(section_matches):
        if match.group(1) != "Completion Gate":
            continue
        content_end = (
            section_matches[index + 1].start()
            if index + 1 < len(section_matches)
            else len(text)
        )
        if not text[match.end():content_end].strip():
            errors.append(f"{milestone_id} guide page has a blank Completion Gate")
        break

    return errors


def validate_milestone_overview(
    text: str, canonical_statuses: dict[str, str]
) -> list[str]:
    status_rows: dict[str, list[str]] = {
        milestone_id: [] for milestone_id in APPROVED_IDS
    }
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or not line.endswith("|"):
            continue
        cells = [cell.strip() for cell in line[1:-1].split("|")]
        if len(cells) != 4 or cells[0] not in APPROVED_IDS:
            continue
        status_rows[cells[0]].append(cells[2])

    errors: list[str] = []
    for milestone_id in sorted(APPROVED_IDS):
        statuses = status_rows[milestone_id]
        if not statuses:
            errors.append(
                f"{milestone_id} milestone overview status row is missing"
            )
            continue
        if len(statuses) != 1:
            errors.append(
                f"{milestone_id} milestone overview has {len(statuses)} "
                "status rows; expected exactly one"
            )
            continue

        canonical_status = canonical_statuses.get(milestone_id)
        if canonical_status is not None and statuses[0] != canonical_status:
            errors.append(
                f"{milestone_id} milestone overview status {statuses[0]} "
                f"does not match milestone data status {canonical_status}"
            )

    return errors


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


def validate_versioned_release_links(root: Path) -> list[str]:
    errors: list[str] = []
    launch_directory = root / "docs/launch"

    for source in sorted(launch_directory.glob("v*.md")):
        text = source.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().split(" ", 1)[0]
            if target.lower().startswith(("http://", "https://", "mailto:", "//")):
                continue
            errors.append(
                f"{source.relative_to(root)} has context-dependent release link: "
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
    canonical_statuses: dict[str, str] = {}
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"milestone record at index {index} must be an object")
            continue

        if set(record) != MILESTONE_FIELDS:
            errors.append(
                f"milestone record at index {index} must have exactly these fields: "
                f"{', '.join(sorted(MILESTONE_FIELDS))}"
            )

        expected_types: dict[str, type | tuple[type, ...]] = {
            "id": str,
            "title": str,
            "status": str,
            "guide_path": str,
            "evidence_url": (str, type(None)),
        }
        for field, expected_type in expected_types.items():
            if field in record and not isinstance(record[field], expected_type):
                errors.append(
                    f"milestone record at index {index} field {field} "
                    "has an invalid type"
                )

        milestone_id = record.get("id") if isinstance(record.get("id"), str) else ""
        status = (
            record.get("status") if isinstance(record.get("status"), str) else ""
        )
        guide_path = (
            record.get("guide_path")
            if isinstance(record.get("guide_path"), str)
            else ""
        )
        evidence_url = record.get("evidence_url")

        if milestone_id in seen_ids:
            errors.append(f"duplicate milestone id: {milestone_id}")
        seen_ids.add(milestone_id)

        if status not in APPROVED_STATUSES:
            errors.append(f"{milestone_id} uses unsupported status: {status}")
        elif (
            milestone_id in APPROVED_IDS
            and milestone_id not in canonical_statuses
        ):
            canonical_statuses[milestone_id] = status
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
            elif milestone_id and status:
                errors.extend(
                    validate_milestone_page(
                        milestone_id,
                        status,
                        guide_path,
                        guide_destination.read_text(encoding="utf-8"),
                    )
                )
        if status == "verified" and not is_public_evidence_url(evidence_url):
            errors.append(
                f"{milestone_id} is verified without a public evidence URL"
            )

    if seen_ids != APPROVED_IDS:
        errors.append(
            "milestone ids must be exactly M0 through M6; "
            f"found {sorted(seen_ids)}"
        )

    overview_path = root / "docs/milestones/README.md"
    if overview_path.is_file():
        errors.extend(
            validate_milestone_overview(
                overview_path.read_text(encoding="utf-8"),
                canonical_statuses,
            )
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
    errors.extend(validate_versioned_release_links(root))
    return errors


def main() -> int:
    errors = validate(Path.cwd())
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
