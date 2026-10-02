"""Hợp đồng dữ liệu dùng chung của JobLens: đường dẫn tới schema, contract bảng, fixtures và khóa tin."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

__version__ = "0.2.0"

_PKG = Path(__file__).resolve().parent
# Khi cài bằng pip, schemas/ và fixtures/ được đóng gói vào trong package;
# khi chạy từ mã nguồn (pip install -e hoặc clone), chúng nằm ở gốc repo.
_BASE = _PKG if (_PKG / "schemas").is_dir() else _PKG.parent


def schema_path(name: str, kind: str = "kafka") -> Path:
    """Đường dẫn file schema, ví dụ schema_path("job_posting.v1")."""
    return _BASE / "schemas" / kind / f"{name}.json"


def load_schema(name: str, kind: str = "kafka") -> dict:
    return json.loads(schema_path(name, kind).read_text(encoding="utf-8"))


def table_contract_path(table: str) -> Path:
    """Đường dẫn contract của bảng, ví dụ table_contract_path("silver.job_skills")."""
    zone, name = table.split(".", 1)
    return _BASE / "schemas" / "tables" / zone / f"{name}.yaml"


def load_table_contract(table: str) -> dict:
    import yaml  # chỉ cần khi đọc contract bảng

    return yaml.safe_load(table_contract_path(table).read_text(encoding="utf-8"))


def fixture_path(name: str) -> Path:
    """Đường dẫn fixture mẫu của một schema, ví dụ fixture_path("job_posting.v1")."""
    return _BASE / "fixtures" / f"{name}.sample.json"


def job_uid(source: str, source_job_id: str) -> str:
    """Khóa của một tin trên một nguồn (ADR 0001 D5): sha1("<source>:<source_job_id>"), hex 40 ký tự.

    Cùng một việc đăng trên hai trang là hai job_uid; tin trùng được gom bằng dup_group_id (silver.job_dedup).
    """
    if not source or not source_job_id:
        raise ValueError("source và source_job_id không được rỗng")
    return hashlib.sha1(f"{source}:{source_job_id}".encode()).hexdigest()
