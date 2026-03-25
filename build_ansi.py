#!/usr/bin/env python3
"""Build ansi.json by concatenating rules from all singles/*.json files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def strip_jsonc(text: str) -> str:
    """Remove // and /* */ comments while preserving string contents."""
    out: list[str] = []
    i = 0
    n = len(text)
    in_string = False
    escaped = False

    while i < n:
        ch = text[i]

        if in_string:
            out.append(ch)
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            i += 1
            continue

        if ch == '"':
            in_string = True
            out.append(ch)
            i += 1
            continue

        if ch == "/" and i + 1 < n:
            nxt = text[i + 1]
            if nxt == "/":
                i += 2
                while i < n and text[i] != "\n":
                    i += 1
                continue
            if nxt == "*":
                i += 2
                while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                    i += 1
                i += 2
                continue

        out.append(ch)
        i += 1

    return "".join(out)


def read_jsonc(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    return json.loads(strip_jsonc(raw))


def get_title(existing_output: Path, default_title: str) -> str:
    if existing_output.exists():
        try:
            data = read_jsonc(existing_output)
            title = data.get("title")
            if isinstance(title, str) and title:
                return title
        except Exception:
            pass
    return default_title


def build(input_dir: Path, output_file: Path, default_title: str) -> None:
    files = sorted(input_dir.glob("*.json"))
    if not files:
        raise FileNotFoundError(f"No JSON files found in {input_dir}")

    merged_manipulators = []
    for path in files:
        data = read_jsonc(path)
        rules = data.get("rules")
        if not isinstance(rules, list):
            raise ValueError(f"Missing or invalid 'rules' in {path}")

        for rule in rules:
            manipulators = rule.get("manipulators") if isinstance(rule, dict) else None
            if not isinstance(manipulators, list):
                raise ValueError(f"Missing or invalid 'manipulators' in a rule from {path}")
            merged_manipulators.extend(manipulators)

    result = {
        "title": get_title(output_file, default_title),
        "rules": [
            {
                "description": "ANSI merged",
                "manipulators": merged_manipulators,
            }
        ],
    }

    output_file.write_text(
        json.dumps(result, indent=4, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create ansi.json from concatenating singles/*.json rule sets."
    )
    parser.add_argument(
        "--input-dir",
        default="singles",
        help="Directory containing per-rule JSON files (default: singles)",
    )
    parser.add_argument(
        "--output",
        default="ansi.json",
        help="Output JSON file path (default: ansi.json)",
    )
    parser.add_argument(
        "--default-title",
        default="ANSI-US MacOS Deutsch",
        help="Fallback title when output file does not already define one",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_file = Path(args.output)
    build(input_dir, output_file, args.default_title)


if __name__ == "__main__":
    main()
