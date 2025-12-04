#!/usr/bin/env python3
import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

EDGE_HEADINGS = [
    "Work:",
    "Personal:",
    "Emotional State:",
    "Tasks:",
    "Decisions:",
    "Concerns:",
    "Wins:",
    "Questions for Later:",
    "Next Actions:",
]


def now_iso():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)


def find_section(lines, contains_text):
    """Return text between '## <...contains_text...>' and next '## ' heading."""
    start_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("## ") and contains_text in line:
            start_idx = i + 1
            break
    if start_idx is None:
        return ""
    end_idx = len(lines)
    for j in range(start_idx + 1, len(lines)):
        if lines[j].strip().startswith("## "):
            end_idx = j
            break
    return "\n".join(lines[start_idx:end_idx]).strip()


def parse_metadata(section_text: str) -> dict:
    meta = {}
    for line in section_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        stripped = stripped[2:]
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()

        if key == "tags":
            # expected like [tag1, tag2]
            if value.startswith("[") and value.endswith("]"):
                inner = value[1:-1]
                if inner.strip():
                    tags = [t.strip() for t in inner.split(",") if t.strip()]
                else:
                    tags = []
            else:
                tags = [v.strip() for v in value.split(",") if v.strip()]
            meta["tags"] = tags
        elif key == "priority":
            try:
                meta["priority"] = int(value)
            except ValueError:
                meta["priority"] = 3
        else:
            meta[key] = value
    return meta


def parse_context(section_text: str) -> dict:
    ctx = {
        "location": "",
        "timeframe": "",
        "scope": "",
        "people": [],
    }
    for line in section_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        stripped = stripped[2:]
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        key = key.strip().lower()
        value = value.strip()
        if key == "location":
            ctx["location"] = value
        elif key == "timeframe":
            ctx["timeframe"] = value
        elif key == "scope":
            ctx["scope"] = value
        elif key == "people":
            # comma or space separated is fine
            people = [p.strip() for p in value.replace(";", ",").split(",") if p.strip()]
            ctx["people"] = people
    return ctx


def parse_edgecoach(text: str) -> dict:
    lines = text.splitlines()
    sections = {}
    current_heading = None
    buffer = []

    def flush():
        nonlocal buffer, current_heading
        if current_heading is not None:
            key = current_heading.rstrip(":")
            sections[key] = "\n".join(buffer).strip()
        buffer = []

    for line in lines:
        stripped = line.strip()
        if stripped in EDGE_HEADINGS:
            flush()
            current_heading = stripped
        else:
            buffer.append(line)
    flush()
    return sections


def build_record_from_markdown(markdown: str) -> dict:
    lines = markdown.splitlines()

    metadata_text = find_section(lines, "Metadata")
    summary_text = find_section(lines, "Content Summary")
    context_text = find_section(lines, "Context")
    edgecoach_text = find_section(lines, "Edge Coach")
    notes_text = find_section(lines, "Additional Notes")

    meta_raw = parse_metadata(metadata_text)
    ctx = parse_context(context_text)

    edge_sections = parse_edgecoach(edgecoach_text)

    # Required metadata fields for schema
    record_id = str(uuid.uuid4())
    created_at = meta_raw.get("created_at") or now_iso()
    title = meta_raw.get("title") or "Untitled daily log"
    record_type = meta_raw.get("type") or "log.entry"
    status = meta_raw.get("status") or "draft"
    owner = meta_raw.get("owner") or "trevor"
    priority = meta_raw.get("priority", 3)
    tags = meta_raw.get("tags", [])

    metadata = {
        "id": record_id,
        "type": record_type,
        "title": title,
        "status": status,
        "priority": priority,
        "tags": tags,
        "created_at": created_at,
        "owner": owner,
        "relations": [],
    }

    if "updated_at" in meta_raw and meta_raw["updated_at"]:
        metadata["updated_at"] = meta_raw["updated_at"]
    if "due_at" in meta_raw and meta_raw["due_at"]:
        metadata["due_at"] = meta_raw["due_at"]
    if "source" in meta_raw and meta_raw["source"]:
        metadata["source"] = meta_raw["source"]

    # Summary
    summary = summary_text.strip()
    if not summary:
        # Fallback from Edge Coach sections
        for key in ["Work", "Decisions", "Next Actions"]:
            if key in edge_sections and edge_sections[key]:
                first_line = edge_sections[key].strip().splitlines()[0]
                if first_line:
                    summary = first_line
                    break
    if not summary:
        summary = "Daily log entry"

    # Body: everything except the metadata section
    # For simplicity, reuse full markdown minus metadata block
    body_lines = []
    in_metadata = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## ") and "Metadata" in stripped:
            in_metadata = True
            continue
        if in_metadata and stripped.startswith("## ") and "Metadata" not in stripped:
            in_metadata = False
        if not in_metadata:
            body_lines.append(line)
    body = "\n".join(body_lines).strip()

    content = {
        "summary": summary,
        "body": body,
        "acceptance_criteria": [],
        "checklist": [],
        "logs": [],
        "links": [],
        "attachments": [],
        "context": ctx,
        "metrics": [],
    }

    record = {
        "version": "4.1",
        "metadata": metadata,
        "content": content,
    }
    return record


def main():
    parser = argparse.ArgumentParser(
        description="Convert a TrevorOS daily_log_template.md file into a TrevorOS v4.1 JSON record."
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to filled daily log markdown file.",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="-",
        help="Output JSON file (default stdout).",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    markdown = load_text(input_path)
    record = build_record_from_markdown(markdown)

    out_str = json.dumps(record, indent=2, ensure_ascii=False)

    if args.output == "-" or args.output == "":
        sys.stdout.write(out_str + "\n")
    else:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out_str + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
