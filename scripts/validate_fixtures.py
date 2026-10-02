"""Kiểm tra mọi fixtures/<schema>.sample.json khớp schemas/kafka/<schema>.json.

Chạy: python scripts/validate_fixtures.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


def validate_all() -> list[str]:
    errors: list[str] = []
    for fixture in sorted((ROOT / "fixtures").glob("*.sample.json")):
        name = fixture.name.removesuffix(".sample.json")
        schema_file = ROOT / "schemas" / "kafka" / f"{name}.json"
        if not schema_file.exists():
            errors.append(f"{fixture.name}: không có schema {schema_file.relative_to(ROOT)}")
            continue
        schema = json.loads(schema_file.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        for i, record in enumerate(json.loads(fixture.read_text(encoding="utf-8"))):
            for err in validator.iter_errors(record):
                path = "/".join(map(str, err.absolute_path)) or "<gốc>"
                errors.append(f"{fixture.name}[{i}] {path}: {err.message}")
    return errors


if __name__ == "__main__":
    problems = validate_all()
    for p in problems:
        print(p)
    print("OK" if not problems else f"{len(problems)} lỗi")
    sys.exit(1 if problems else 0)
