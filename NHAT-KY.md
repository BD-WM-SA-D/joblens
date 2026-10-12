# Nhật ký thay đổi – joblens (dùng chung)

Chỉ ghi sự kiện đáng nhớ: đổi hợp đồng hoặc file cấu hình chung, ghép hệ thống, chốt số liệu, quyết định quan trọng. Việc thường ngày đã có lịch sử git. Mục mới đặt trên cùng, vài dòng là đủ – xem [repo-routing](docs/repo-routing.md), mục Nhật ký.

## 2026-10-12 · Hoang Le

- Thêm [Blueprint hệ thống](docs/project-plan/14-blueprint-he-thong.md) (đề xuất): persona, cách tương tác, UC thu hẹp, kiến trúc 4+1, dữ liệu, API. Sửa docs/05, docs/06, docs/07 (UC008 → UC009), mục lục.
- Thêm [ADR 0002](docs/adr/0002-goi-y-truc-tuyen-tu-ho-so-ky-nang.md) và hợp đồng `schemas/api/mining.v1.yaml` (draft): gợi ý trực tuyến qua `mining-service`.
- Contract (draft): `gold.dim_skill` 0.2.0 thêm `aliases`; `silver.review_aspects` 0.2.0 thêm `sentence_text`; mới `gold.data_status`; `gold.mart_job_reco_candidates` 0.2.0 chỉ còn cho đánh giá offline WM5 (reader: Web-mining); cập nhật `used_by` (UC011–UC013) ở `job_skills`, `job_postings`, `job_dedup`, `mart_company_aspect_sentiment`, `reco_scores`.
- `templates/agents/pttkht.md`: CSDL ứng dụng, `mining.v1`; đồng bộ `AGENTS.md` sang PTTKHT.
- Ảnh hưởng: WM (làm `mining-service` + stub, ghi `sentence_text`, cung cấp alias kỹ năng), BD (triển khai `mining-service`, `dim_skill.aliases`, `data_status`), PTTKHT (đã cập nhật tài liệu) – đã nhắn nhóm: <chưa>.
- **Chốt chiến lược dữ liệu:** tin crawl (TopCV, ITviec) là dữ liệu chính; VietJobs chỉ cho nhãn yếu/từ điển WM2, baseline, đo tải + GX + replay của BD, dự phòng. Sửa docs/02, 11, 13, 14, mục lục; note lọc `source = vietjobs` trong `silver.job_postings` 0.1.2, `gold.mart_skill_demand_monthly` 0.1.1, `gold.mart_salary_role_region` 0.1.1. Ảnh hưởng BD – đã nhắn nhóm: <chưa>.
- AI: Claude Code (Claude Opus 5.5) – soạn blueprint, ADR, contract; <người kiểm tra> đã kiểm tra

## 2026-10-07 · Hoang Le

- `job_posting.v1` lên 1.2.0: `url` không bắt buộc khi `source = vietjobs` (dataset VietJobs không có URL). Nguồn khác vẫn bắt buộc như cũ. Ảnh hưởng: Big Data (replay VietJobs vào bronze) – đã nhắn nhóm: <chưa>.
- Thêm `explore/out/vietjobs_eda.md`: số liệu EDA VietJobs đầy đủ (48.092 tin), chỉ có thống kê, không có bản ghi gốc.
- AI: Claude Code (Claude Opus 5.5) – sửa schema, chạy EDA; <người kiểm tra> đã kiểm tra

## 2026-10-03 · Hoang Le

- Đơn giản hóa quy trình: trong repo môn làm tự do (push thẳng `main` được, không bắt buộc PR, không ghi nhật ký việc thường ngày); chỉ chỗ nối (hợp đồng ở `joblens`, file cấu hình chung) mới cần nhắn nhóm + ghi một dòng nhật ký; đổi tên/xóa trường thì hỏi người đang dùng; ghép hệ thống theo mốc thay vì hằng tuần; bỏ chờ 24 giờ.
- Sửa: `docs/project-plan/09` (quy tắc 1, 3, 5, 6, 10, checklist), `docs/repo-routing.md` (thêm bảng Tra nhanh), `templates/CONTRIBUTING.md`, `templates/AGENTS.md`, `templates/agents/joblens.md`, `templates/cursor-rule.mdc`, ADR 0001 (cách duyệt), `README.md`; đồng bộ `CONTRIBUTING.md`, `AGENTS.md`, `.cursor/rules/joblens.mdc` sang 4 repo; sửa phần đầu `NHAT-KY.md` ở 4 repo.
- AI: Claude Code (Claude Opus 5.5) – soạn quy trình mới theo yêu cầu; <người kiểm tra> đã kiểm tra

## 2026-10-02 · Hoang Le · chưa có PR

- **Tạo:** `schemas/kafka/{review,user_event,parse_error,alert_subscription,job_match}.v1.json` (A); 16 contract `schemas/tables/{bronze,silver,gold}/*.yaml` + `schemas/tables/_contract.schema.json` (A); `schemas/api/search.v1.yaml` (A); `schemas/README.md` (A); 5 fixture mới `fixtures/*.v1.sample.json` (A); `tests/test_contracts.py` (D)
- **Sửa:** `schemas/kafka/job_posting.v1.json` (A – 1.1.0, thêm `raw_html_uri`); `fixtures/job_posting.v1.sample.json`, `fixtures/README.md` (A); `joblens_contracts/__init__.py` (A – `job_uid()`, `load_table_contract()`, v0.2.0); `pyproject.toml` (D – thêm pyyaml, pin ruff 0.8.0 cho CI); `docs/project-plan/02, 03, 04, 05, 07, 08, 09, 10, 11, 13, README.md, templates/README-repo.md` (A – tên repo/org thật, các điểm "Kéo theo" của ADR 0001, bỏ "template repository"); `templates/env.example`, `templates/gitignore.template`, `templates/pre-commit-config.yaml`, `templates/agents/*.md` (A – bản gốc mục C); `.env.example`, `.gitignore`, `.pre-commit-config.yaml`, `AGENTS.md` (C – đồng bộ); `docs/repo-routing.md`, `glossary.md`, `docs/adr/0001-…` (A); `README.md` (D)
- **Xóa:** `schemas/tables/{bronze,silver,gold}/.gitkeep`
- **Lý do:** cài đặt sẵn các phương án đề xuất của ADR 0001 (D1–D7) để các repo có hợp đồng làm việc song song; contract ở trạng thái `draft` cho tới khi nhóm duyệt ADR
- **Ảnh hưởng repo khác:** cả 3 repo môn – `.env.example` thêm biến đăng nhập (D7), `AGENTS.md` cập nhật phạm vi theo ADR; khi ADR được duyệt, mỗi repo làm phần việc ở bảng "Tổng hợp" của ADR
- **AI:** Claude Code (Claude Opus 5.5) – soạn schema, contract, script, sửa docs theo phương án đề xuất của ADR 0001; <người kiểm tra> đã kiểm tra

## 2026-10-02 · Hoang Le · chưa có PR

- **Tạo:** `docs/adr/0001-ranh-gioi-xu-ly-giua-cac-repo.md` (A)
- **Sửa:** `adr-index.md` (A)
- **Xóa:** –
- **Lý do:** chốt các điểm dễ dẫm chân giữa repo: ai parse, ai chuẩn hóa lương/địa điểm, mô hình giao dưới dạng image, phục vụ tìm kiếm và cảnh báo, khóa `job_uid`/`dup_group_id`, quyền đọc `joblens`, biến môi trường đăng nhập
- **Ảnh hưởng repo khác:** cả 3 repo môn sau khi ADR được duyệt (bảng "Tổng hợp" trong ADR); cần 3 người phụ trách đồng ý D1, D3, D4, D5
- **AI:** Claude Code (Claude Opus 5.5) – soạn nháp ADR và phương án đề xuất; <người kiểm tra> đã kiểm tra

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
