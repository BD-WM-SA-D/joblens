> [← Mục lục](README.md)

# Ma trận liên kết (traceability)

Bảng này là "sợi chỉ đỏ" nối dữ liệu – kỹ thuật – ca sử dụng – bài giảng – metric. Nó được dùng trong cả ba báo cáo nhưng mỗi báo cáo đọc theo một cột khác nhau.

| Ca sử dụng (SA&D) | Gold / bảng phục vụ (BD) | Bài khai phá (WM) | Nguồn dữ liệu | Bài giảng căn cứ | Metric chính |
|---|---|---|---|---|---|
| UC001 Tìm kiếm | `silver.job_postings` + chỉ mục | WM1, WM4 | TopCV, ITviec, VietJobs | BD L07 · WM L04 · SAD l03–l04 | nDCG@10 (WM) · p95 truy vấn (BD) · acceptance (SAD) |
| UC002 Xu hướng kỹ năng | `mart_skill_demand_monthly` | WM2, WM6 | tin tuyển dụng + ESCO | BD L14 · WM L05, L07 | F1 IE (WM) · freshness (BD) |
| UC003 So sánh lương | `mart_salary_role_region` | (WM8) | TopCV, VietJobs | BD L10, L14 | GX pass rate (BD) · RMSE (WM8) |
| UC004 Gợi ý việc làm | `mart_job_reco_candidates` | WM5 | job_skills + events synthetic | BD L13 · WM L08 | Recall@10 (WM) |
| UC005 Đánh giá công ty | `mart_company_aspect_sentiment` | WM3 | ITviec reviews | WM L06 | Macro-F1 (WM) |
| UC006 Cảnh báo tin mới | luồng Kafka → streaming | – | Kafka | BD L08, L11 | streaming freshness (BD) · NFR ≤ 5 phút (SAD) |
| UC008 Quản lý nguồn | cấu hình spider + Airflow DAG | WM1 | – | BD L14 · SAD l05 (Adapter) | – |
| UC009 Giám sát chất lượng | kết quả GX, dbt tests | – | – | BD L14 | GX pass rate (BD) |
