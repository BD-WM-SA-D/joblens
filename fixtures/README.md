# Fixtures

Dữ liệu mẫu rất nhỏ để kiểm thử, dùng chung cho cả 4 repo. **Toàn bộ fixture hiện tại do nhóm tự soạn (synthetic):** công ty, URL (`example.invalid`), người dùng và nội dung đều là giả, không lấy từ trang nào. Giấy phép thuộc nhóm JobLens.

| File | Schema | Ghi chú |
|---|---|---|
| `job_posting.v1.sample.json` | `schemas/kafka/job_posting.v1.json` | 3 tin; tin 3 là bản gần trùng có chủ đích để thử dedup |
| `review.v1.sample.json` | `schemas/kafka/review.v1.json` | 2 review (một tiếng Việt, một tiếng Anh) |
| `user_event.v1.sample.json` | `schemas/kafka/user_event.v1.json` | search, view, apply; `job_uid` trỏ tới tin trong `job_posting` |
| `parse_error.v1.sample.json` | `schemas/kafka/parse_error.v1.json` | 1 lỗi parser |
| `alert_subscription.v1.sample.json` | `schemas/kafka/alert_subscription.v1.json` | upsert + delete |
| `job_match.v1.sample.json` | `schemas/kafka/job_match.v1.json` | ghép `sub-001` với tin `syn-000001` |

Quy tắc:

- Tên file theo dạng `<tên schema>.sample.json` (mảng JSON). Mỗi schema phải có một fixture; `scripts/validate_fixtures.py` và `pytest` tự kiểm tra fixture khớp schema.
- `job_uid` trong fixture phải tính bằng `joblens_contracts.job_uid(source, source_job_id)` và trỏ tới tin có trong `job_posting.v1.sample.json`.
- Chỉ thêm dữ liệu có giấy phép rõ ràng (ví dụ mẫu VietJobs – trích dẫn Pham Dinh et al., LREC 2026) và ghi vào bảng trên. Tổng dung lượng thư mục dưới ~5 MB.
- Không có dữ liệu cá nhân, không có HTML thô hay dữ liệu crawl (docs/project-plan/09, quy tắc 8).
