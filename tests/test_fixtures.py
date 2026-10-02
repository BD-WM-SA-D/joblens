import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from validate_fixtures import validate_all  # noqa: E402

from joblens_contracts import fixture_path, load_schema  # noqa: E402


def test_fixtures_match_schemas():
    assert validate_all() == []


def test_package_helpers():
    assert load_schema("job_posting.v1")["title"] == "job_posting v1"
    assert fixture_path("job_posting.v1").exists()
