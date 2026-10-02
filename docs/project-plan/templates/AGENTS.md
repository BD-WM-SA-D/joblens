# Hướng dẫn cho AI agent

Áp dụng cho mọi AI agent làm việc trong repo này: Codex, Claude Code, Cursor, Copilot… Người dùng nói khác thì làm theo người dùng, nhưng phải nhắc lại quy tắc bị bỏ qua.

## Bối cảnh

JobLens VN là đồ án liên môn học kỳ 20261. Một hệ thống được chia thành 4 repo trong org `BD-WM-SA-D`:

| Repo | Vai trò |
|---|---|
| `joblens` | Dùng chung: schema Kafka, contract bảng, fixtures, glossary, phiên bản, tài liệu kế hoạch |
| `Big-Data-Storage-and-Processing-joblens` | Môn IT4931 Big Data: Kafka, Spark, Iceberg, dbt, GX, Airflow, Trino, K8s |
| `Web-mining-joblens` | Môn Web Mining: crawler, dedup, IE, ABSA, IR, RecSys, đồ thị |
| `PTTKHT-joblens` | Môn IT3120 SA&D: cổng JobLens (API + UI), UML, yêu cầu, kiểm thử chấp nhận |

Mỗi repo là bài nộp của **một** môn. Mỗi artifact chỉ có **một** môn chấm chính. Code đặt sai repo làm hỏng tính độc lập của bài nộp.

Tài liệu gốc:
- File nào lên repo nào: `joblens/docs/repo-routing.md`.
- Quy tắc làm việc: `joblens/docs/project-plan/09-quy-tac-lam-viec-chung.md`.
- Ma trận sở hữu: `joblens/docs/project-plan/07-quy-tac-phan-tach-mon.md`.

## Ngôn ngữ

- Tài liệu, comment, mô tả commit/PR, nhật ký viết bằng **tiếng Việt có dấu**.
- Tên biến, hàm, file, cột, topic viết bằng tiếng Anh (`snake_case` cho Python/SQL).

## Mỗi khi tạo hoặc sửa file (bắt buộc)

1. **Xác định repo đích** bằng `repo-routing.md`, mục A–F, và mục "Phạm vi repo này" ở cuối file này. Nếu file không thuộc repo đang mở thì **không tạo**: báo người dùng repo đúng và phần việc cần làm ở đó. Nếu bảng không có loại file này thì hỏi người dùng.
2. **Tôn trọng dòng đánh dấu.** File có dòng đầu `ĐỒNG BỘ TỪ …` hoặc `SINH TỪ …` thì **không sửa tại chỗ**. Chỉ ra bản gốc cần sửa (thường ở `joblens/docs/project-plan/templates/` hoặc `joblens/schemas/`).
3. **Thêm dòng đánh dấu** khi tạo file mục C (`ĐỒNG BỘ TỪ`), mục E (`LIÊN QUAN: <repo>/<file>`) hoặc file sinh từ schema (`SINH TỪ … @ vX.Y.Z`).
4. **Ghi `NHAT-KY.md`** của repo này trong cùng thay đổi. Mục mới đặt **trên cùng** và theo mẫu trong `repo-routing.md#nhật-ký-thay-đổi`.
   - Liệt kê mọi file tạo, sửa (mục A/C/E) và xóa.
   - Dòng **AI** ghi tên công cụ và model, phần nào do AI làm, kèm `<người kiểm tra>`. **Không tự điền tên người kiểm tra.**
   - Nếu thay đổi chạm schema, file cấu hình chung hoặc repo khác thì nhắc người dùng ghi thêm vào `joblens/NHAT-KY.md`.

## Không bao giờ làm

- **Commit những thứ cấm:**
  - Bí mật: `.env`, key, token, kubeconfig.
  - Dữ liệu crawl, HTML thô, dump Kafka, warehouse Iceberg.
  - Tập nhãn, file model (`*.pt`, `*.bin`, `*.safetensors`, `*.onnx`, `*.pkl`).
  - Dữ liệu cá nhân (tên, email, SĐT, CV).
  - Slide hay tài liệu của giảng viên.
  - Output notebook.
- **Lách bộ chặn:**
  - Không dùng `--no-verify`.
  - Không sửa `.gitignore` hay `.pre-commit-config.yaml` để cho file cấm đi qua.
- **Thao tác git và GitHub nguy hiểm:**
  - Không push thẳng `main`, không force-push, không viết lại lịch sử đã push.
  - Không merge PR thay người.
  - Không tạo hay xóa repo, không đổi cài đặt org/repo.
- **Thu thập dữ liệu sai quy tắc:**
  - Không chạy crawler thật khi chưa được yêu cầu rõ.
  - Không lách robots.txt hay chống bot, không thêm đăng nhập vào trang nguồn.
  - Không vượt 1 request/giây/domain, không chạm đường dẫn CV.
- **Tải nặng vào repo:** không tải dataset lớn hay model vào repo, không gửi dữ liệu crawl cho dịch vụ bên ngoài.
- **Ghi vào bảng hay topic của repo khác** (quy tắc 2): cần dữ liệu thì đọc, hoặc mở issue `cross-repo`.
- **Bịa thông tin:**
  - Tên thành viên, MSSV, ngày giảng viên đồng ý, mã môn.
  - Số liệu thí nghiệm, benchmark, metric.
  - Chỗ chưa biết thì giữ dạng `<...>`.
- **Lẫn báo cáo giữa các môn:** không viết nội dung báo cáo của môn khác vào repo này, không chép nguyên văn đoạn văn giữa các báo cáo (R3), không dán cùng một hình vào hai báo cáo (R5).
- **Dùng `latest`:** không dùng tag `latest` cho image hay phiên bản thư viện. Phiên bản pin nằm ở `joblens/versions.md`.

## Đổi schema hay hợp đồng dữ liệu

- Sửa ở `joblens` **trước** (SemVer: thêm trường không bắt buộc thì tăng *minor*, đổi tên hoặc xóa thì tăng *major* và tạo `.vN` mới).
- Repo môn chỉ cập nhật version sau khi `joblens` đã gắn tag.
- Thấy cần đổi schema khi đang làm ở repo môn thì dừng và báo người dùng, không sửa bản sao cục bộ.

## Git

- Làm trên nhánh `feat/…`, `fix/…` hoặc `docs/…`. Commit theo Conventional Commits, ví dụ `feat(crawler): thêm adapter ITviec`.
- PR nhỏ, một mục đích. Mô tả PR có mục **AI** (công cụ, phần nào, ai kiểm tra). Việc chạm repo khác gắn nhãn `cross-repo`.

## Trước khi báo xong

- Chạy `pre-commit run --all-files` và test của repo (xem "Phạm vi repo này"). Báo lệnh đã chạy và kết quả thật.
- Bước nào không chạy được thì nói rõ là chưa kiểm tra, không viết "đã xong".
- Tóm tắt: file đã tạo, sửa, xóa; mục nhật ký đã ghi; việc còn lại ở repo khác (nếu có).

## Hỏi người dùng thay vì đoán khi

- Không xác định được file thuộc repo nào.
- Thay đổi phá vỡ tương thích (*major*), đổi tên bảng, cột hoặc topic.
- Xóa file hay thư mục có sẵn.
- Yêu cầu mâu thuẫn với quy tắc ở trên.
