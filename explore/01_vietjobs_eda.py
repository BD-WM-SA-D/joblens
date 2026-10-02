"""Khám phá nhanh dataset VietJobs (LREC 2026).

Cách chạy (trên máy có internet bình thường):
    pip install pandas pyarrow huggingface_hub
    python explore/01_vietjobs_eda.py                 # tự tải bản đầy đủ từ Hugging Face vào data/vietjobs/
    python explore/01_vietjobs_eda.py --csv đường/dẫn.csv   # hoặc chạy trên file CSV có sẵn (ví dụ VietJobs_sample.csv)

Kết quả in ra màn hình và lưu thành explore/out/vietjobs_eda.md.
Dữ liệu tải về nằm trong data/ (đã gitignore) – KHÔNG commit.
"""

from __future__ import annotations

import argparse
import ast
import re
import unicodedata
from collections import Counter
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "vietjobs"
OUT_DIR = Path(__file__).resolve().parent / "out"
LIST_COLS = ["qualifications", "technical_skills", "soft_skills", "languages_required", "benefits"]


def load(csv: str | None) -> pd.DataFrame:
    if csv:
        return pd.read_csv(csv)
    from huggingface_hub import snapshot_download

    path = snapshot_download("dinhieufam/VietJobs", repo_type="dataset", local_dir=DATA_DIR)
    files = sorted(Path(path).rglob("*.parquet")) or sorted(Path(path).rglob("*.csv"))
    if not files:
        raise SystemExit(f"Không tìm thấy file dữ liệu trong {path}")
    frames = [pd.read_parquet(f) if f.suffix == ".parquet" else pd.read_csv(f) for f in files]
    return pd.concat(frames, ignore_index=True)


def to_list(v):
    """Các cột danh sách được lưu dạng chuỗi "['a', 'b']" → list thật."""
    if isinstance(v, list):
        return v
    if not isinstance(v, str) or not v.strip():
        return []
    try:
        out = ast.literal_eval(v)
        return [str(x).strip() for x in out] if isinstance(out, (list, tuple)) else [str(out)]
    except (ValueError, SyntaxError):
        return [s.strip() for s in v.split(",") if s.strip()]


SAL_RE = re.compile(r"(\d+(?:[.,]\d+)?)")


def parse_salary(s) -> tuple[float | None, float | None, str]:
    """Tính lại lương (triệu VND) từ chuỗi gốc thay vì dùng salary_min/max/avg đã làm tròn."""
    if not isinstance(s, str):
        return None, None, "missing"
    low = s.lower()
    if "thỏa thuận" in low or "thoả thuận" in low or "cạnh tranh" in low:
        return None, None, "negotiable"
    nums = [float(x.replace(",", ".")) for x in SAL_RE.findall(low)]
    if "usd" in low:
        return None, None, "usd"  # cần tỷ giá – để riêng
    if len(nums) >= 2:
        return nums[0], nums[1], "range"
    if len(nums) == 1:
        if low.startswith("từ") or "trên" in low:
            return nums[0], None, "from"
        if low.startswith("tới") or low.startswith("đến") or "dưới" in low:
            return None, nums[0], "upto"
        return nums[0], nums[0], "fixed"
    return None, None, "unparsed"


def norm_title(t: str) -> str:
    t = unicodedata.normalize("NFC", str(t)).lower()
    t = t.replace("xử lí", "xử lý")
    return re.sub(r"[^\w]+", " ", t).strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", help="chạy trên file CSV có sẵn thay vì tải từ Hugging Face")
    args = ap.parse_args()

    df = load(args.csv)
    lines: list[str] = []
    say = lambda s="": (print(s), lines.append(s))  # noqa: E731

    say(f"# VietJobs – báo cáo khám phá nhanh\n\nSố dòng: {len(df):,} · Số cột: {df.shape[1]}\n")
    say("## Cột và tỉ lệ thiếu\n")
    say("| Cột | Kiểu | % thiếu |\n|---|---|---|")
    for c in df.columns:
        say(f"| `{c}` | {df[c].dtype} | {df[c].isna().mean():.1%} |")
    missing_expected = [c for c in ["company_name", "posting_date", "url", "deadline"] if c not in df.columns]
    if missing_expected:
        say(
            f"\n> Không có các cột: {', '.join(missing_expected)} → không làm được phân tích theo công ty/thời gian từ VietJobs.\n"
        )

    for c in LIST_COLS:
        if c in df.columns:
            df[c] = df[c].map(to_list)

    # Lương
    if "salary" in df.columns:
        parsed = df["salary"].map(parse_salary)
        df["sal_lo"], df["sal_hi"], df["sal_kind"] = zip(*parsed)
        say("\n## Lương (tính lại từ chuỗi gốc)\n")
        say("| Dạng | Số tin |\n|---|---|")
        for k, n in df["sal_kind"].value_counts().items():
            say(f"| {k} | {n:,} |")
        if "salary_min" in df.columns:
            mism = (df["sal_kind"].eq("range") & (df["sal_lo"].round(0) != df["salary_min"])).sum()
            say(f"\nSố tin mà `salary_min` khác giá trị tính lại (do làm tròn/cắt số): {mism:,}")
        if "salary_avg" in df.columns:
            avg = pd.to_numeric(
                df["salary_avg"].astype(str).str.extract(r"(\d+(?:[.,]\d+)?)")[0].str.replace(",", "."), errors="coerce"
            )
            mid = (df["sal_lo"] + df["sal_hi"]) / 2
            off = (df["sal_kind"].eq("range") & ((avg - mid).abs() > 0.5)).sum()
            say(
                f"Số tin mà `salary_avg` lệch > 0,5 triệu so với trung điểm khoảng lương: {off:,} → nên tự tính lại, không dùng cột này."
            )
        rng = df[df["sal_kind"] == "range"]
        if len(rng):
            mid = (rng["sal_lo"] + rng["sal_hi"]) / 2
            say(
                f"\nMức giữa khoảng lương (triệu VND): median {mid.median():.1f}, p10 {mid.quantile(.1):.1f}, p90 {mid.quantile(.9):.1f}"
            )

    # Địa điểm
    if "location" in df.columns:
        locs = df["location"].fillna("").str.split(r"\s*[,;]\s*").explode().str.strip().replace("", pd.NA).dropna()
        multi = (df["location"].fillna("").str.contains(",")).mean()
        say(f"\n## Địa điểm\n\nTin có nhiều địa điểm: {multi:.1%}. Top 10:\n")
        for k, n in locs.value_counts().head(10).items():
            say(f"- {k}: {n:,}")

    for c in ["category", "contract_type", "experience_required"]:
        if c in df.columns:
            say(f"\n## `{c}` (top 10)\n")
            for k, n in df[c].value_counts().head(10).items():
                say(f"- {k}: {n:,}")

    # Kỹ năng
    if "technical_skills" in df.columns:
        has = df["technical_skills"].map(len) > 0
        say(f"\n## Kỹ năng (nhãn do LLM trích – coi là nhãn yếu)\n\nTin có `technical_skills`: {has.mean():.1%}")
        cnt = Counter(s.lower() for lst in df["technical_skills"] for s in lst)
        say(f"Số kỹ năng khác nhau (chưa chuẩn hóa): {len(cnt):,}. Top 20:\n")
        for k, n in cnt.most_common(20):
            say(f"- {k}: {n:,}")

    # Độ dài văn bản
    for c in ["description", "requirements_text"]:
        if c in df.columns:
            w = df[c].fillna("").str.split().str.len()
            say(f"\n`{c}`: trung bình {w.mean():.0f} từ, median {w.median():.0f}, p95 {w.quantile(.95):.0f}")

    # Gần trùng (thô) – để hình dung bài toán dedup WM1
    if {"job_title", "location"} <= set(df.columns):
        key = df["job_title"].map(norm_title) + "|" + df["location"].fillna("").str.lower()
        dup = key.duplicated(keep=False).mean()
        say(
            f"\n## Gần trùng (khóa thô: tiêu đề chuẩn hóa + địa điểm)\n\nTỉ lệ tin nằm trong nhóm trùng khóa: {dup:.1%} – cần MinHash trên nội dung để tách tin đăng lại thật sự với tin khác nhau cùng tiêu đề."
        )

    say("\n## Một bản ghi mẫu\n")
    say("```")
    say(df.drop(columns=[c for c in ["sal_lo", "sal_hi", "sal_kind"] if c in df.columns]).iloc[0].to_string()[:2500])
    say("```")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "vietjobs_eda.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"\n→ Đã lưu {OUT_DIR / 'vietjobs_eda.md'}")


if __name__ == "__main__":
    main()
