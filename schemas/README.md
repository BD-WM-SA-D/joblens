# Hợp đồng dữ liệu

Bản gốc duy nhất của mọi hợp đồng giữa các repo. Repo môn không chép các file này: muốn dùng thì cài `joblens` theo tag. Đổi hợp đồng thì mở PR ở đây **trước** (docs/project-plan/09, quy tắc 1).

> Trạng thái hiện tại: **draft**, chờ [ADR 0001](../docs/adr/0001-ranh-gioi-xu-ly-giua-cac-repo.md) được nhóm duyệt. Khi ADR được chấp nhận, các contract chuyển sang `stable` và repo gắn tag `v1.0.0`.

## Đánh số phiên bản

- **Major** nằm trong tên file và tên topic: `job_posting.v1.json` dùng cho `jobs.raw.<nguồn>.v1`. Đổi major thì tạo file mới `.v2`, tạo topic mới, và chạy song song với bản cũ.
- **Minor/patch** nằm trong trường `x-version` của file schema, hoặc `version` của contract bảng. Thêm trường không bắt buộc thì tăng minor.
- Trường `schema_version` trong message chỉ ghi major (`job_posting.v1`).

## Topic Kafka – ai ghi, ai đọc

Mỗi topic có **đúng một repo ghi** (quy tắc 2).

| Topic | Schema | Key | Repo ghi | Repo đọc |
|---|---|---|---|---|
| `jobs.raw.<nguồn>.v1` | [`kafka/job_posting.v1.json`](kafka/job_posting.v1.json) | `source_job_id` | Web-mining-joblens (crawler) | Big-Data (bronze) |
| `reviews.raw.<nguồn>.v1` | [`kafka/review.v1.json`](kafka/review.v1.json) | `company_id` | Web-mining-joblens (crawler) | Big-Data (bronze) |
| `dlq.parse_errors.v1` | [`kafka/parse_error.v1.json`](kafka/parse_error.v1.json) | `source` | Web-mining-joblens (parser) | Big-Data (báo cáo tỉ lệ lỗi) |
| `events.user.v1` | [`kafka/user_event.v1.json`](kafka/user_event.v1.json) | `user_id` | Big-Data (event-generator) | Big-Data (bronze), Web-mining (RecSys) |
| `app.alert_subscriptions.v1` | [`kafka/alert_subscription.v1.json`](kafka/alert_subscription.v1.json) | `subscription_id` | PTTKHT-joblens (app) | Big-Data (job ghép cảnh báo) |
| `alerts.job_match.v1` | [`kafka/job_match.v1.json`](kafka/job_match.v1.json) | `user_id` | Big-Data (job streaming) | PTTKHT-joblens (app) |

## Bảng – ai ghi, ai đọc

Chi tiết cột nằm trong từng file. Định dạng file: [`tables/_contract.schema.json`](tables/_contract.schema.json).

| Bảng | Repo ghi | Repo đọc | Ca sử dụng / bài |
|---|---|---|---|
| `bronze.jobs_raw`, `bronze.reviews_raw`, `bronze.user_events` | Big-Data | Web-mining | WM1–3, WM5 |
| `silver.job_postings`, `silver.job_postings_snapshot` | Big-Data | Web-mining, PTTKHT | UC001, UC003, UC011, UC012 |
| `silver.job_skills` | Web-mining (image skill-extractor) | Big-Data, PTTKHT | UC002, UC004, UC011–013 |
| `silver.job_dedup` | Web-mining (image job-dedup) | Big-Data, PTTKHT | UC001–003, UC011, UC012 |
| `silver.review_aspects` | Web-mining (image absa-scorer) | Big-Data, PTTKHT | UC005, UC011 |
| `silver.reco_scores` | Web-mining (image recsys-scorer) | Big-Data | WM5 (đánh giá offline – ADR 0002) |
| `gold.dim_location`, `gold.dim_skill`, `gold.dim_company` | Big-Data (dbt) | PTTKHT, Web-mining | `dim_skill.aliases`: đường lùi trích kỹ năng UC004 |
| `gold.mart_skill_demand_monthly` | Big-Data (dbt) | PTTKHT, Web-mining | UC002 |
| `gold.mart_salary_role_region` | Big-Data (dbt) | PTTKHT, Web-mining | UC003 |
| `gold.mart_company_aspect_sentiment` | Big-Data (dbt) | PTTKHT, Web-mining | UC005, UC011 |
| `gold.mart_job_reco_candidates` | Big-Data (dbt) | Web-mining | WM5 (đánh giá offline – ADR 0002) |
| `gold.data_status` | Big-Data (dbt) | PTTKHT | UC009 |

Bảng nội bộ của một repo (ví dụ `bronze.ingest_errors` của Big-Data) không cần contract ở đây, vì không repo nào khác đọc.

**Chưa có contract:** `gold.fct_job_snapshot_daily` và `gold.mart_skill_graph_edges` (WM6 là bài mở rộng). Thêm khi bắt đầu làm.

## API

| API | File | Repo cung cấp | Repo gọi |
|---|---|---|---|
| Tìm kiếm việc làm | [`api/search.v1.yaml`](api/search.v1.yaml) (OpenAPI 3.1) | Web-mining (image search-service, Big-Data triển khai) | PTTKHT (có đường lùi về Trino) |
| Trích kỹ năng, gợi ý trực tuyến | [`api/mining.v1.yaml`](api/mining.v1.yaml) (OpenAPI 3.1) – [ADR 0002](../docs/adr/0002-goi-y-truc-tuyen-tu-ho-so-ky-nang.md) | Web-mining (image mining-service, Big-Data triển khai) | PTTKHT (có đường lùi: từ điển + đếm kỹ năng trùng) |

## Kiểm tra tự động

`pytest` (`tests/test_contracts.py`) kiểm tra:
- Mỗi schema Kafka hợp lệ và có fixture.
- Mỗi contract bảng đúng định dạng: khóa chính và partition trỏ tới cột có thật, mart có ghi `grain`, không có cột PII.
- Mọi `job_uid` trong fixture đều trỏ tới tin có thật.

`scripts/validate_fixtures.py` kiểm tra fixture khớp schema.
