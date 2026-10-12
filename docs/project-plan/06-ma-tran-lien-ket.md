> [← Mục lục](README.md)

# Ma trận liên kết (traceability)

Theo phạm vi đã thu hẹp ở [Blueprint hệ thống](14-blueprint-he-thong.md) (UC007, UC008 đã bỏ). Bảng này là "sợi chỉ đỏ" nối dữ liệu – kỹ thuật – ca sử dụng – bài giảng – metric. Nó được dùng trong cả ba báo cáo nhưng mỗi báo cáo đọc theo một cột khác nhau.

| Ca sử dụng (SA&D) | Gold / bảng phục vụ (BD) | Bài khai phá (WM) | Nguồn dữ liệu | Bài giảng căn cứ | Metric chính |
|---|---|---|---|---|---|
| UC001 Tìm kiếm | `silver.job_postings`, `silver.job_dedup` + chỉ mục | WM1, WM4 | TopCV, ITviec, VietJobs | BD L07 · WM L04 · SAD l03–l04 | P/R/F1 dedup, nDCG@10 (WM) · p95 truy vấn (BD) · acceptance (SAD) |
| UC011 Chi tiết tin | như UC001 + `silver.job_skills`, `mart_company_aspect_sentiment` | WM1, WM2, WM3 | như UC001 | WM L05, L06 · SAD l04 | acceptance (SAD) |
| UC004 Hồ sơ kỹ năng (dán CV) | `mining-service` (`mining.v1`), lùi `dim_skill.aliases` | WM2 | văn bản người dùng (không lưu) | WM L07 (IE) · SAD l03 | F1 thực thể (WM) · NFR ≤ 3 giây (SAD) |
| UC012 Gợi ý việc làm | `mining-service`, lùi `silver.job_skills` (ADR 0002) | WM5 | job_skills (+ events synthetic cho đánh giá offline) | BD L13 · WM L08 | Recall@10, nDCG@10 offline (WM) · acceptance (SAD) |
| UC013 Khoảng trống kỹ năng | `silver.job_skills` | WM2, WM5 | job_skills | WM L08 | acceptance (SAD) |
| UC005 Đánh giá công ty | `mart_company_aspect_sentiment`, `silver.review_aspects` | WM3 | ITviec reviews | WM L06 | Macro-F1 (WM) |
| UC002 Xu hướng kỹ năng | `mart_skill_demand_monthly` | WM2, WM6 | tin tuyển dụng + ESCO | BD L14 · WM L05, L07 | F1 IE (WM) · freshness (BD) |
| UC006 Cảnh báo tin mới | luồng Kafka → streaming | – | Kafka | BD L08, L11 | streaming freshness (BD) · NFR ≤ 5 phút (SAD) |
| UC009 Tình trạng dữ liệu | `gold.data_status` (GX, DLQ, độ tươi) | WM1 (lỗi parse) | – | BD L14 | GX pass rate (BD) |
| UC010 Đăng nhập | CSDL ứng dụng (PTTKHT) | – | – | SAD l03 | acceptance (SAD) |
| UC003 So sánh lương (P2) | `mart_salary_role_region` | (WM8) | TopCV, VietJobs | BD L10, L14 | GX pass rate (BD) · RMSE (WM8) |
