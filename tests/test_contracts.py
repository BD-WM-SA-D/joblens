"""Kiểm tra hợp đồng: schema Kafka có fixture, contract bảng đúng định dạng và tự nhất quán, API đọc được."""

import json
import re
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

from joblens_contracts import job_uid, load_table_contract

ROOT = Path(__file__).resolve().parents[1]
KAFKA = sorted((ROOT / "schemas" / "kafka").glob("*.json"))
TABLES = sorted((ROOT / "schemas" / "tables").glob("*/*.yaml"))
META = json.loads((ROOT / "schemas" / "tables" / "_contract.schema.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("schema_file", KAFKA, ids=lambda p: p.stem)
def test_kafka_schema_valid_and_has_fixture(schema_file):
    schema = json.loads(schema_file.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    assert schema["properties"]["schema_version"]["const"] == schema_file.stem
    assert re.fullmatch(r"\d+\.\d+\.\d+", schema["x-version"])
    assert (ROOT / "fixtures" / f"{schema_file.stem}.sample.json").exists(), "mỗi schema cần một fixture"


@pytest.mark.parametrize("contract_file", TABLES, ids=lambda p: f"{p.parent.name}.{p.stem}")
def test_table_contract(contract_file):
    doc = yaml.safe_load(contract_file.read_text(encoding="utf-8"))
    errors = [e.message for e in Draft202012Validator(META).iter_errors(doc)]
    assert errors == []
    assert doc["table"] == f"{contract_file.parent.name}.{contract_file.stem}", "tên bảng phải khớp đường dẫn file"

    names = [col["name"] for col in doc["columns"]]
    assert len(names) == len(set(names)), "trùng tên cột"
    assert set(doc["primary_key"]) <= set(names), "khóa chính phải là cột có thật"
    for spec in doc["partition_spec"]:
        col = re.sub(r"^[a-z_]+\((?:\d+, )?([a-z0-9_]+)\)$", r"\1", spec)
        assert col in names, f"partition '{spec}' tham chiếu cột không có"
    if doc["table"].startswith("gold.") and doc["table"].split(".")[1].startswith("mart_"):
        assert doc.get("grain"), "mart gold phải ghi grain"
    for col in doc["columns"]:
        assert not re.search(r"(email|phone|sdt|contact_name|reviewer_name)", col["name"]), "không có cột PII"


def test_load_table_contract_helper():
    assert load_table_contract("silver.job_skills")["writer_repo"] == "Web-mining-joblens"


def test_search_api_contract():
    api = yaml.safe_load((ROOT / "schemas" / "api" / "search.v1.yaml").read_text(encoding="utf-8"))
    assert api["openapi"].startswith("3.1")
    assert {"/search", "/health"} <= set(api["paths"])


def test_job_uid():
    assert job_uid("synthetic", "syn-000001") == "862e0278ea284bae21ffed05e1dafedc6baac559"
    assert job_uid("topcv", "1") != job_uid("itviec", "1")
    with pytest.raises(ValueError):
        job_uid("topcv", "")


def test_fixture_job_uids_consistent():
    """job_uid trong các fixture khác phải trỏ tới tin có trong fixture job_posting."""
    postings = json.loads((ROOT / "fixtures" / "job_posting.v1.sample.json").read_text(encoding="utf-8"))
    known = {job_uid(p["source"], p["source_job_id"]) for p in postings}
    for name in ["user_event.v1", "job_match.v1"]:
        for rec in json.loads((ROOT / "fixtures" / f"{name}.sample.json").read_text(encoding="utf-8")):
            if rec.get("job_uid"):
                assert rec["job_uid"] in known, f"{name}: job_uid {rec['job_uid']} không có trong fixture job_posting"
