"""Đồng bộ file mục C (repo-routing) từ docs/project-plan/templates/ sang các repo JobLens.

Mỗi file đích có dòng đầu "ĐỒNG BỘ TỪ …". AGENTS.md = phần chung + mục "Phạm vi repo này"
lấy từ templates/agents/<repo>.md.

Chạy từ repo joblens, với thư mục chứa các repo đã clone cạnh nhau:
    python scripts/sync_templates.py ..            # ghi file
    python scripts/sync_templates.py .. --check    # chỉ báo file lệch, exit 1 nếu có
Sau khi chạy: ghi NHAT-KY.md ở từng repo được đồng bộ và ở joblens.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "docs" / "project-plan" / "templates"
TPL_PREFIX = "joblens/docs/project-plan/templates"
BLOB = "https://github.com/BD-WM-SA-D/joblens/blob/main"

# Tên repo trên GitHub (kể cả tên cũ) → file phạm vi trong templates/agents/
SCOPES = {
    "joblens": "joblens",
    "Big-Data-Storage-and-Processing-joblens": "big-data",
    "-Big-Data-Storage-and-Processing-Joblens": "big-data",
    "Web-mining-joblens": "web-mining",
    "PTTKHT-joblens": "pttkht",
}

# File trong repo → (bản gốc trong templates/, kiểu comment)
SIMPLE = {
    ".gitignore": ("gitignore.template", "#"),
    ".pre-commit-config.yaml": ("pre-commit-config.yaml", "#"),
    ".env.example": ("env.example", "#"),
    ".gitattributes": ("gitattributes.template", "#"),
    "CONTRIBUTING.md": ("CONTRIBUTING.md", "html"),
    "CLAUDE.md": ("CLAUDE.md", "html"),
}


def marker(src: str, style: str) -> str:
    text = f"ĐỒNG BỘ TỪ {TPL_PREFIX}/{src} – sửa ở đó trước, không sửa tại đây"
    return f"<!-- {text} -->\n" if style == "html" else f"# {text}\n"


def repo_name(path: Path) -> str:
    try:
        url = subprocess.run(
            ["git", "-C", str(path), "remote", "get-url", "origin"], capture_output=True, text=True, check=True
        ).stdout.strip()
        return url.rstrip("/").removesuffix(".git").rsplit("/", 1)[-1]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return path.name


def read(name: str) -> str:
    return (T / name).read_text(encoding="utf-8")


def render(repo: str) -> dict[str, str]:
    shared = repo == "joblens"
    out: dict[str, str] = {}
    for dst, (src, style) in SIMPLE.items():
        body = read(src)
        if dst == "CONTRIBUTING.md":
            plan = "docs/project-plan" if shared else f"{BLOB}/docs/project-plan"
            routing = "docs/repo-routing.md" if shared else f"{BLOB}/docs/repo-routing.md"
            body = body.replace("](../09-quy-tac-lam-viec-chung.md", f"]({plan}/09-quy-tac-lam-viec-chung.md")
            body = body.replace("](../../repo-routing.md", f"]({routing}")
        out[dst] = marker(src, style) + body
    scope = f"agents/{SCOPES[repo]}.md"
    out["AGENTS.md"] = (
        f"<!-- ĐỒNG BỘ TỪ {TPL_PREFIX}/AGENTS.md + {scope} – sửa ở đó trước, không sửa tại đây -->\n"
        + read("AGENTS.md").rstrip()
        + "\n\n"
        + read(scope)
    )
    front, body = read("cursor-rule.mdc").split("---\n", 2)[1:]
    out[".cursor/rules/joblens.mdc"] = f"---\n{front}---\n" + marker("cursor-rule.mdc", "html") + body
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252
    ap = argparse.ArgumentParser()
    ap.add_argument("repos_dir", type=Path, help="thư mục chứa các repo JobLens cạnh nhau")
    ap.add_argument("--check", action="store_true", help="chỉ kiểm tra, không ghi")
    args = ap.parse_args()

    drift = 0
    for path in sorted(p for p in args.repos_dir.resolve().iterdir() if (p / ".git").exists()):
        repo = repo_name(path)
        if repo not in SCOPES:
            print(f"bỏ qua {path.name} (không phải repo JobLens)")
            continue
        for dst, content in render(repo).items():
            target = path / dst
            current = target.read_text(encoding="utf-8") if target.exists() else None
            if current == content:
                continue
            drift += 1
            print(f"{'lệch' if args.check else 'ghi'}: {repo}/{dst}")
            if not args.check:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8", newline="\n")
    print("OK – không có file lệch" if drift == 0 else f"{drift} file {'lệch' if args.check else 'đã ghi'}")
    return 1 if args.check and drift else 0


if __name__ == "__main__":
    sys.exit(main())
