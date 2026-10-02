# Nhật ký thay đổi – joblens (dùng chung)

Quy ước ghi: [repo-routing – Nhật ký thay đổi](docs/repo-routing.md#nhật-ký-thay-đổi). Mỗi PR một mục, mục mới nhất đặt trên cùng. Liệt kê mọi file tạo/xóa và mọi file mục A/C/E bị sửa.

## 2026-10-02 · Hoang Le · chưa có PR

- **Tạo:** `docs/project-plan/templates/AGENTS.md`, `templates/agents/{joblens,big-data,web-mining,pttkht}.md`, `templates/CLAUDE.md`, `templates/cursor-rule.mdc` (A – bản gốc); `scripts/sync_templates.py` (A); `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/joblens.mdc` (C)
- **Sửa:** `docs/repo-routing.md` (A – thêm file agent vào mục C, lệnh đồng bộ); `scripts/validate_fixtures.py` (A – in UTF-8 trên Windows); `README.md` (D)
- **Xóa:** –
- **Lý do:** quy tắc làm việc cho AI agent dùng chung cho Codex, Claude Code, Cursor; script đồng bộ file mục C sang 4 repo (`--check` để phát hiện lệch)
- **Ảnh hưởng repo khác:** cả 3 repo môn nhận `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/joblens.mdc` với mục "Phạm vi repo này" riêng
- **AI:** Claude Code (Claude Opus 5.5) – soạn quy tắc và script đồng bộ; <người kiểm tra> đã kiểm tra

## 2026-10-02 · Hoang Le · không qua PR (giai đoạn khởi tạo)

- **Tạo:** `docs/repo-routing.md` (A), `NHAT-KY.md` (D), `docs/project-plan/templates/env.example`, `docs/project-plan/templates/gitattributes.template` (A – bản gốc cho file mục C)
- **Sửa:** `docs/project-plan/templates/CONTRIBUTING.md` (A – thêm bước tra repo-routing, ghi nhật ký); `README.md` (D – link repo-routing); `.gitignore`, `.pre-commit-config.yaml`, `.env.example`, `.gitattributes`, `CONTRIBUTING.md` (C – đồng bộ, thêm dòng `ĐỒNG BỘ TỪ`)
- **Xóa:** –
- **Lý do:** quy ước file nào lên repo nào, quy trình khi tạo/sửa file, nhật ký thay đổi cho từng repo
- **Ảnh hưởng repo khác:** cả 3 repo môn được đồng bộ file mục C và có `NHAT-KY.md` riêng: `Big-Data-Storage-and-Processing-joblens`, `Web-mining-joblens`, `PTTKHT-joblens`
- **AI:** Claude Code – dựng khung, soạn nội dung; <người kiểm tra> đã kiểm tra

## 2026-10-02 · Hoang Le · không qua PR (giai đoạn khởi tạo)

- **Tạo:** `schemas/kafka/job_posting.v1.json`, `fixtures/job_posting.v1.sample.json`, `glossary.md`, `versions.md`, `adr-index.md` (A); `docs/project-plan/**`, `explore/01_vietjobs_eda.py` (A – chép từ bộ tài liệu kế hoạch); `joblens_contracts/`, `scripts/validate_fixtures.py`, `tests/`, `pyproject.toml`, `.github/workflows/ci.yml`, `README.md` (D); file cấu hình chung (C)
- **Sửa:** –
- **Xóa:** –
- **Lý do:** khởi tạo repo theo docs/project-plan/08; gộp commit "Initial commit" do GitHub tự sinh, giữ README của repo
- **Ảnh hưởng repo khác:** không
- **AI:** Claude Code – dựng khung, soạn nội dung; <người kiểm tra> đã kiểm tra
