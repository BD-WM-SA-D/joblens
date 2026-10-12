# ADR 0002 – Gợi ý việc làm trực tuyến từ hồ sơ kỹ năng

| | |
|---|---|
| **Trạng thái** | ĐỀ XUẤT – chờ nhóm duyệt |
| **Ngày** | 2026-10-12 |
| **Người soạn** | Hoang Le (nháp bằng Claude Code) |
| **Cần đồng ý** | BD: <Họ tên> · WM: <Họ tên> · SAD: <Họ tên> |
| **Ảnh hưởng** | `joblens`, `Web-mining-joblens`, `Big-Data-Storage-and-Processing-joblens`, `PTTKHT-joblens` (`cross-repo`) |
| **Nền** | [Blueprint hệ thống](../project-plan/14-blueprint-he-thong.md) mục 11.2, 13; điểm mở "hồ sơ kỹ năng UC004 đi vào RecSys thế nào" sau ADR 0001 |
| **Bản cài đặt** | `schemas/api/mining.v1.yaml` (draft), cột `aliases` của `gold.dim_skill`, `used_by` của các contract liên quan |

## Vấn đề

Blueprint chốt câu chuyện chính: người dùng **dán CV → hệ thống trích kỹ năng → hiện ngay 10 tin phù hợp**. Thiết kế hiện tại không làm được việc này:

- `gold.mart_job_reco_candidates` và `silver.reco_scores` được **tính trước theo lô** cho từng `user_id`. Người dùng vừa lập hồ sơ thì chưa có dòng nào, phải chờ tới lần chạy DAG sau (1 ngày).
- Trích kỹ năng (WM2) chỉ chạy theo lô trên tin tuyển dụng, chưa có cách chạy trên văn bản người dùng gửi lên.
- App không được tự chứa mô hình ML (ADR 0001 D4a loại phương án đẩy tính toán ML vào app).

## Quyết định đề xuất

1. **WM giao image `mining-service`** (HTTP, hợp đồng `schemas/api/mining.v1.yaml`):
   - `POST /v1/skills:extract`: chạy mô hình WM2 trên văn bản người dùng, trả `skill_id` theo `gold.dim_skill`.
   - `POST /v1/recommend`: gợi ý content-based (WM5) từ danh sách `skill_id`, trên chỉ mục dựng từ `silver.job_skills` của các tin đang mở.
   - Kèm **image stub** trả dữ liệu cố định để PTTKHT phát triển song song (như ADR 0001 D3).
2. **BD triển khai** `mining-service` trên K8s (namespace `serving`) như `search-service` (ADR 0001 D4a); cập nhật chỉ mục gợi ý sau mỗi lần DAG ghi `silver.job_skills`.
3. **Riêng tư:** dịch vụ không lưu, không ghi log nội dung văn bản; app không lưu văn bản CV, chỉ lưu danh sách kỹ năng người dùng đã xác nhận (CSDL ứng dụng của PTTKHT).
4. **Đường lùi trong app** (khi không có `JOBLENS_MINING_URL`, dịch vụ lỗi hoặc quá 3 giây):
   - Trích kỹ năng: so khớp từ điển trên `gold.dim_skill.label` và `gold.dim_skill.aliases`.
   - Gợi ý: SQL đếm số kỹ năng trùng trên `silver.job_skills` ⨝ `silver.job_postings` (tin đang mở), gộp theo `dup_group_id`.
5. **Bảng gợi ý theo lô giữ cho đánh giá offline:** `silver.reco_scores` và `gold.mart_job_reco_candidates` phục vụ đánh giá WM5 trên người dùng synthetic (Recall@10, nDCG@10) và thí nghiệm ALS của BD; **không** phục vụ người dùng thật của cổng.

## Phương án đã cân nhắc

| Phương án | Vì sao không chọn |
|---|---|
| Chờ DAG đêm tính gợi ý cho người dùng mới | Người dùng mới không thấy gì trong ngày đầu – hỏng câu chuyện demo chính |
| App tự chạy mô hình WM2/WM5 | Đưa PyTorch vào app, trộn phần chấm của WM vào repo SA&D (vi phạm R2) |
| Chỉ dùng SQL đếm kỹ năng trùng | Không có phần mô hình WM5/WM2 trực tuyến để đánh giá; vẫn giữ làm đường lùi |

## Hệ quả

| Repo | Việc |
|---|---|
| `joblens` | `schemas/api/mining.v1.yaml`; `gold.dim_skill` thêm `aliases`; `used_by` của `silver.job_skills`, `gold.dim_skill`, `gold.mart_job_reco_candidates`, `silver.reco_scores` theo UC mới (UC004, UC011, UC012, UC013) |
| WM | `mining-service` + stub; mô hình WM2 chạy trên CPU ≤ 3 giây cho văn bản ≤ 3.000 ký tự; ghi phiên bản vào `models.yaml` |
| BD | Triển khai `mining-service`; tác vụ cập nhật chỉ mục sau DAG; `dim_skill.aliases` từ từ điển alias của WM |
| PTTKHT | `MiningClient` (HTTP + từ điển), `RecommendationService` với Strategy (mô hình / đếm trùng); đặc tả UC004, UC012 |

## Cách duyệt

| Quyết định | BD | WM | SAD | Ghi chú |
|---|---|---|---|---|
| 1–5 | <chờ> | <chờ> | <chờ> | |
