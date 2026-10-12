> [← Mục lục](README.md)

# Phân tích thiết kế hệ thống (SA&D)

Đối tượng phân tích là **cổng JobLens** (ứng dụng phục vụ người dùng), còn nền tảng dữ liệu được mô hình hóa như một **hệ thống con** mà cổng phụ thuộc vào. Cách đóng khung này giúp đề tài có nghiệp vụ rõ ràng như các ví dụ trong l00, thay vì chỉ là "một pipeline".

> **Cập nhật 2026-10-12:** phạm vi đã thu hẹp theo [Blueprint hệ thống](14-blueprint-he-thong.md) (đề xuất, chờ duyệt). Mục này là bản tóm tắt; chi tiết persona, cách tương tác, luồng, dữ liệu và API ở blueprint.

## Mô hình nghiệp vụ (chương 2 – optional nhưng nên làm)

- **Persona chính:** sinh viên năm cuối / fresher IT tìm việc đầu tiên (blueprint mục 2.1). Persona phụ (tùy chọn): dev 3–5 năm muốn đổi việc.
- **Business actor:** Người tìm việc IT. **Business worker:** Quản trị dữ liệu.
- **Business use case:** "Tìm việc hợp kỹ năng", "Biết nên học thêm gì", "Đánh giá nhà tuyển dụng trước khi nộp".
- Quy trình thu thập – làm sạch – công bố dữ liệu vẽ bằng **activity diagram/BPMN**; domain class diagram: `NguoiDung`, `HoSoKyNang`, `KyNang`, `TinTuyenDung`, `NhomTinTrung`, `CongTy`, `DanhGiaKhiaCanh`, `GoiYViecLam`, `DangKyCanhBao`, `ThongBao`, `DiaDiem`.

## Ca sử dụng (chương 3)

Giữ mã cũ để contract không lệch; UC bỏ không dùng lại mã. **P0** = demo đầu tiên, **P1** = trước khi nộp, **P2** = nếu còn thời gian.

| UC | Tên | Actor chính | Mức | Dữ liệu / dịch vụ phía sau | Liên kết môn khác |
|---|---|---|---|---|---|
| UC001 | Tìm kiếm việc làm | Người tìm việc (khách) | P0 | `silver.job_postings`, `silver.job_dedup`; API tìm kiếm (`schemas/api/search.v1.yaml`, lùi về Trino) | WM1, WM4 |
| UC011 | Xem chi tiết tin tuyển dụng | Người tìm việc (khách) | P0 | như UC001 + `silver.job_skills`, `gold.mart_company_aspect_sentiment` | WM1, WM2, WM3 |
| UC004 | Lập hồ sơ kỹ năng (dán CV → tự trích) | Thành viên | P0 | `mining-service` (`schemas/api/mining.v1.yaml`), lùi về `gold.dim_skill.aliases`; CSDL ứng dụng | WM2 |
| UC012 | Nhận gợi ý việc làm | Thành viên | P0 | `mining-service`, lùi về đếm kỹ năng trùng trên `silver.job_skills` ([ADR 0002](../adr/0002-goi-y-truc-tuyen-tu-ho-so-ky-nang.md)) | WM5 |
| UC005 | Xem đánh giá công ty theo khía cạnh | Người tìm việc (khách) | P0 | `gold.mart_company_aspect_sentiment`, `silver.review_aspects` | WM3 |
| UC010 | Đăng ký / đăng nhập | Khách → Thành viên | P0 | CSDL ứng dụng | – |
| UC002 | Xem xu hướng nhu cầu kỹ năng | Người tìm việc (khách) | P1 | `gold.mart_skill_demand_monthly` | WM2, BD gold |
| UC013 | Xem khoảng trống kỹ năng | Thành viên | P1 | `silver.job_skills` | WM2, WM5 |
| UC006 | Đăng ký và nhận cảnh báo tin mới | Thành viên | P1 | app ghi `app.alert_subscriptions.v1` → BD ghép → app đọc `alerts.job_match.v1` | BD streaming |
| UC009 | Xem tình trạng dữ liệu (chỉ đọc) | Quản trị dữ liệu | P1 | `gold.data_status` | BD, WM1 |
| UC003 | So sánh mức lương | Người tìm việc (khách) | P2 | `gold.mart_salary_role_region` | BD gold |
| UC007 | ~~Xuất báo cáo thị trường~~ | | bỏ | | |
| UC008 | ~~Quản lý nguồn thu thập~~ | | bỏ (dùng Airflow UI của BD) | | |

Actor hệ thống: **Nền tảng dữ liệu JobLens** (Trino, Kafka – BD) và **Dịch vụ khai phá** (`mining-service`, `search-service` – WM). Quan hệ include/extend giữa các UC: blueprint mục 4.2. Mỗi UC kèm user story + acceptance criteria dạng Given/When/Then (l03), đạt tiêu chí INVEST.

## Yêu cầu phi chức năng đo được (theo tiêu chí "unambiguous, measurable" của l03)

| NFR | Phát biểu đề xuất | Cách kiểm thử (chương 6) |
|---|---|---|
| Hiệu năng trang | 95% yêu cầu tới API cổng (UC001, UC002, UC005, UC011) ≤ 3 giây với 20 người dùng đồng thời | Script tải (locust/k6) |
| Hiệu năng trích kỹ năng | 95% yêu cầu trích kỹ năng (văn bản ≤ 3.000 ký tự) ≤ 3 giây trên CPU | Script tải gọi UC004 |
| Chịu lỗi | Dịch vụ khai phá/tìm kiếm lỗi thì UC001, UC004, UC012 vẫn trả kết quả bằng đường lùi trong ≤ 5 giây | Tắt dịch vụ rồi chạy kịch bản chấp nhận |
| Độ tươi | Tin mới xuất hiện trong UC001 ≤ 24 giờ sau khi crawl; cảnh báo UC006 ≤ 5 phút sau khi vào Kafka | So `crawl_ts` với thời điểm hiển thị (trích số đo BD) |
| Riêng tư | Không lưu văn bản CV; mật khẩu băm bằng argon2/bcrypt; không có cột PII ở silver/gold | Test tự động + review code |
| Khả năng dùng | Người dùng mới hoàn thành "dán CV → xem gợi ý" ≤ 3 phút không cần hướng dẫn | Thử với 5 người |
| Chạy độc lập | Cổng chạy với gold mẫu (DuckDB/Parquet từ fixtures), không cần Trino, Kafka, dịch vụ khai phá | CI chạy kịch bản chấp nhận ở chế độ local |
| Triển khai lại | Dựng lại toàn bộ môi trường từ repo ≤ 30 phút | Chạy thử trên máy sạch |

## Thiết kế (chương 4) – ánh xạ vào guideline

- **Kiến trúc logic:** layered cho cổng JobLens (Presentation → Boundary → Control → Entity → Infrastructure) + client–server (SPA ↔ API) + **event-driven** cho cảnh báo UC006 + service-based với dịch vụ khai phá (các kiểu kiến trúc có trong l05). Trình bày theo **4+1 views** – bản nháp ở blueprint mục 8–9.
- **Kiến trúc triển khai:** deployment diagram UML với node = K8s node/namespace, artifact = pod/container (vẽ lại theo ký pháp UML, không dán sơ đồ Helm).
- **Mẫu thiết kế (mục 4.2 của guideline):** *Repository* cho truy cập Trino/DuckDB/PostgreSQL; *Adapter* để đổi nguồn theo môi trường (Trino ↔ DuckDB, mining-service ↔ từ điển); *Strategy* cho thuật toán gợi ý (mô hình ↔ đếm kỹ năng trùng); *Facade* là API cổng; *Observer/pub-sub* cho cảnh báo UC006; *Circuit breaker/fallback* cho dịch vụ ngoài. (Adapter cho từng trang nguồn thuộc crawler của WM, không thuộc cổng.)
- **Thiết kế ca sử dụng:** mỗi UC một biểu đồ lớp theo **ECB** (Entity–Control–Boundary, l04) + biểu đồ trình tự; biểu đồ máy trạng thái cho vòng đời `TinTuyenDung` (mới → đang mở → đã đóng / hết hạn) và `DangKyCanhBao` (đang bật ⇄ tạm dừng → đã xóa).
- **Human-AI collaboration (l00):** ghi nhật ký những bước dùng AI hỗ trợ (ví dụ nháp user story, rà soát NFR) kèm phần người kiểm duyệt – vừa minh bạch vừa đúng định hướng môn.

## Metrics chấp nhận và chất lượng thiết kế

Mỗi metric thuộc về **đúng một môn** (quy tắc R4 trong [Quy tắc phân tách](07-quy-tac-phan-tach-mon.md)). Chỉ tiêu là đề xuất để nhóm có đích nhắm, sẽ hiệu chỉnh sau khi có số đo đầu tiên.

| Metric | Định nghĩa |
|---|---|
| Độ phủ yêu cầu | % UC có đặc tả + biểu đồ lớp/trình tự + kịch bản kiểm thử |
| Tỉ lệ đạt acceptance criteria | số kịch bản Given/When/Then đạt / tổng |
| NFR đạt | từng NFR ở mục Yêu cầu phi chức năng phía trên: đạt/không đạt, kèm bằng chứng (được phép trích số đo từ BD, không phân tích lại) |
| Truy vết | 100% UC truy vết được tới thành phần triển khai ([ma trận liên kết](06-ma-tran-lien-ket.md)) |
