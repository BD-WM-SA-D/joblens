# Đóng góp vào JobLens

Ba nhóm làm **song song**, mỗi nhóm một repo. Chỉ cần cẩn thận ở **chỗ nối** giữa các repo. Bản đầy đủ: [quy tắc làm việc chung](../09-quy-tac-lam-viec-chung.md).

## 1. Trong repo môn của mình: làm tự do

- Push thẳng `main` hoặc dùng nhánh, tùy bạn. Không bắt buộc PR, không cần ai duyệt.
- Commit message ghi rõ thay đổi gì, ví dụ `feat(crawler): thêm adapter ITviec`, `fix(dbt): sửa đơn vị lương`.
- Việc thường ngày không cần ghi nhật ký, lịch sử git là đủ. Nhật ký làm việc không đưa lên nhánh chính.
- Nếu dùng AI cho một phần đáng kể, thêm một dòng cuối commit message: `AI: <công cụ> – <phần nào>`.

## 2. Khi đụng chỗ nối giữa các repo

Chỗ nối là **hợp đồng trong repo `joblens`** (schema Kafka, contract bảng, API – xem [danh sách](../../../schemas/README.md)) và các file cấu hình chung.

| Bạn muốn | Làm thế nào |
|---|---|
| Thêm trường hoặc cột mới (không bắt buộc) | Sửa ở `joblens`, nhắn nhóm chat một câu, ghi một dòng vào `joblens/NHAT-KY.md` |
| Đổi tên hoặc xóa trường/cột, đổi topic hay bảng | Như trên, nhưng **hỏi người đang dùng** trong chat trước. Họ trả lời "ok" thì đổi |
| Ghi vào bảng hay topic của repo khác | Không làm. Mỗi bảng, mỗi topic chỉ một repo ghi ([danh sách](../../../schemas/README.md)). Cần dữ liệu thì nhắn nhóm kia |
| Sửa `.gitignore`, pre-commit, `.env.example`, `AGENTS.md`… | Không sửa trong repo môn (dòng đầu file ghi `ĐỒNG BỘ TỪ`). Báo người giữ repo `joblens` sửa bản gốc rồi đồng bộ sang |

Thay đổi ở repo `joblens` nên đi qua PR để CI kiểm tra fixtures khớp schema, nhưng không cần chờ ai duyệt.

Không chắc file thuộc repo nào thì xem bảng tra nhanh ở đầu [repo-routing](../../repo-routing.md).

## 3. Không được commit

Pre-commit chặn sẵn phần lớn các trường hợp. Sau khi clone, chạy `pre-commit install` một lần.

- Bí mật (`.env`, key, token, kubeconfig): để trong `.env`, file này đã được gitignore.
- Dữ liệu crawl, tập nhãn, model, output notebook: để trên `s3://joblens/…`.
- Dữ liệu cá nhân: không lưu ở đâu cả.
- Slide và tài liệu của giảng viên.

Lỡ đẩy bí mật lên GitHub: đổi key ngay rồi báo nhóm.

## 4. Viết tài liệu và refactor

Chi tiết ở quy tắc 11 và 12 của [quy tắc làm việc chung](../09-quy-tac-lam-viec-chung.md).

- README và `docs/` viết như repo độc lập, tập trung method, chỉ ghi kết quả chính thức, không có tên hay mã môn, không có mã phiên bản nội bộ.
- Nhật ký thí nghiệm và nhật ký làm việc để ở máy hoặc nhánh `nhat-ky`, không để ở nhánh chính.
- Refactor từng bước nhỏ, chạy `ruff` và `pytest` trước và sau, không đổi hành vi, không xóa nhầm file.

## Môi trường

- Python 3.12; `ruff`, `pytest`, `pre-commit`.
- Biến môi trường dùng tiền tố `JOBLENS_` – xem `.env.example`.
