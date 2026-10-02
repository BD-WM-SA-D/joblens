# Fixtures

Dữ liệu mẫu rất nhỏ để kiểm thử, dùng chung cho cả 4 repo.

| File | Schema | Nguồn | Giấy phép |
|---|---|---|---|
| `job_posting.v1.sample.json` | `schemas/kafka/job_posting.v1.json` | **Tự soạn (synthetic)**: công ty, URL (`example.invalid`) và nội dung đều là giả, không lấy từ trang nào | Thuộc nhóm JobLens |

Quy tắc:

- Tên file theo dạng `<tên schema>.sample.json` (mảng JSON). `scripts/validate_fixtures.py` và CI tự kiểm tra mỗi fixture khớp schema cùng tên.
- Chỉ thêm dữ liệu có giấy phép rõ ràng (ví dụ mẫu VietJobs – trích dẫn Pham Dinh et al., LREC 2026) và ghi vào bảng trên. Tổng dung lượng thư mục dưới ~5 MB.
- Không có dữ liệu cá nhân, không có HTML thô hay dữ liệu crawl (docs/project-plan/09, quy tắc 8).
