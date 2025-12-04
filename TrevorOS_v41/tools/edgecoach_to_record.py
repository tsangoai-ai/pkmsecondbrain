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


def parse_edgecoach(text: str) -> dict:
    """
    Very simple parser:
    - Splits on the fixed headings
    - Returns a dict {heading_without_colon: text_block}
    - Keeps raw spacing except leading/trailing whitespace
    """
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


def build_record(args, edgecoach_text: str) -> dict:
    edge_sections = parse_edgecoach(edgecoach_text)

    # Build a compact summary if not provided
    if args.summary:
        summary = args.summary
    else:
        # fallback: first non-empty line from Work/Decisions/Next Actions
        summary = ""
        for key in ["Work", "Decisions", "Next Actions"]:
            if key in edge_sections and edge_sections[key]:
                first_line = edge_sections[key].strip().splitlines()[0]
                if first_line:
                    summary = first_line
                    break
        if not summary:
            summary = "Edge Coach reflection"

    record_id = str(uuid.uuid4())
    created_at = now_iso()

    metadata = {
        "id": record_id,
        "type": args.record_type,
        "title": args.title,
        "status": args.status,
        "priority": args.priority,
        "tags": args.tags or [],
        "created_at": created_at,
        # updated_at intentionally omitted; can be added by later tooling
        # due_at omitted unless supplied
        # source omitted unless supplied
        "owner": args.owner,
        "relations": [],
    }

    if args.source:
        metadata["source"] = args.source
    if args.due_at:
        metadata["due_at"] = args.due_at

    content = {
        "summary": summary,
        "body": edgecoach_text.strip(),
        "acceptance_criteria": [],
        "checklist": [],
        "logs": [],
        "links": [],
        "attachments": [],
        "context": {
            "location": args.location or "",
            "timeframe": args.timeframe or "",
            "scope": args.scope or "",
            "people": args.people or [],
        },
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
        description="Convert an Edge Coach v2 block into a TrevorOS v4.1 record JSON."
    )
    parser.add_argument(
        "--edgecoach-file",
        type=str,
        default="-",
        help="Path to file containing Edge Coach text (default: stdin).",
    )
    parser.add_argument(
        "--record-type",
        type=str,
        default="reflection",
        choices=[
            "log.entry",
            "reflection",
            "action.item",
            "action.step",
            "project",
            "milestone",
            "objective",
            "key_result",
            "decision",
            "risk",
            "issue",
            "idea",
            "knowledge.note",
            "meeting.note",
            "research.source",
            "resource",
            "habit",
            "template",
            "review",
            "metric",
        ],
        help="Metadata.type value; must match schema enum.",
    )
    parser.add_argument(
        "--title",
        type=str,
        required=True,
        help="Title for the record (metadata.title).",
    )
    parser.add_argument(
        "--status",
        type=str,
        default="draft",
        choices=["draft", "active", "blocked", "done", "archived"],
        help="Metadata.status.",
    )
    parser.add_argument(
        "--priority",
        type=int,
        default=3,
        help="Metadata.priority (1–5).",
    )
    parser.add_argument(
        "--tags",
        type=str,
        nargs="*",
        default=None,
        help="Metadata.tags, space-separated list.",
    )
    parser.add_argument(
        "--summary",
        type=str,
        default=None,
        help="Override auto-generated content.summary.",
    )
    parser.add_argument(
        "--owner",
        type=str,
        default="trevor",
        help="Metadata.owner.",
    )
    parser.add_argument(
        "--source",
        type=str,
        default=None,
        help="Optional metadata.source URI.",
    )
    parser.add_argument(
        "--due-at",
        type=str,
        default=None,
        help="Optional metadata.due_at (ISO datetime).",
    )
    parser.add_argument(
        "--location",
        type=str,
        default=None,
        help="Context.location.",
    )
    parser.add_argument(
        "--timeframe",
        type=str,
        default=None,
        help="Context.timeframe.",
    )
    parser.add_argument(
        "--scope",
        type=str,
        default=None,
        help="Context.scope.",
    )
    parser.add_argument(
        "--people",
        type=str,
        nargs="*",
        default=None,
        help="Context.people, space-separated list.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="-",
        help="Output JSON file path (default: stdout).",
    )

    args = parser.parse_args()

    # Load Edge Coach text
    if args.edgecoach_file == "-" or args.edgecoach_file == "":
        edge_text = sys.stdin.read()
    else:
        p = Path(args.edgecoach_file)
        if not p.exists():
            print(f"Edge Coach file not found: {p}", file=sys.stderr)
            sys.exit(1)
        edge_text = p.read_text(encoding="utf-8")

    record = build_record(args, edge_text)

    out_str = json.dumps(record, indent=2, ensure_ascii=False)

    if args.output == "-" or args.output == "":
        sys.stdout.write(out_str + "\n")
    else:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out_str + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
