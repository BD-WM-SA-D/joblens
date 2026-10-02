"""Hợp đồng dữ liệu dùng chung của JobLens: đường dẫn tới schema và fixtures."""

from __future__ import annotations

import json
from pathlib import Path

__version__ = "0.1.0"

_PKG = Path(__file__).resolve().parent
# Khi cài bằng pip, schemas/ và fixtures/ được đóng gói vào trong package;
# khi chạy từ mã nguồn (pip install -e hoặc clone), chúng nằm ở gốc repo.
_BASE = _PKG if (_PKG / "schemas").is_dir() else _PKG.parent


def schema_path(name: str, kind: str = "kafka") -> Path:
    """Đường dẫn file schema, ví dụ schema_path("job_posting.v1")."""
    return _BASE / "schemas" / kind / f"{name}.json"


def load_schema(name: str, kind: str = "kafka") -> dict:
    return json.loads(schema_path(name, kind).read_text(encoding="utf-8"))


def fixture_path(name: str) -> Path:
    """Đường dẫn fixture mẫu của một schema, ví dụ fixture_path("job_posting.v1")."""
    return _BASE / "fixtures" / f"{name}.sample.json"
