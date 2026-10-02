> [← Mục lục](README.md)

# Phân tích thiết kế hệ thống (SA&D)

Đối tượng phân tích là **cổng JobLens** (ứng dụng phục vụ người dùng), còn nền tảng dữ liệu được mô hình hóa như một **hệ thống con** mà cổng phụ thuộc vào. Cách đóng khung này giúp đề tài có nghiệp vụ rõ ràng như các ví dụ trong l00, thay vì chỉ là "một pipeline".

## Mô hình nghiệp vụ (chương 2 – optional nhưng nên làm)

- **Business actor:** Người tìm việc (sinh viên, người đi làm), Nhà tuyển dụng/HR.
- **Business worker:** Chuyên viên phân tích thị trường lao động, Quản trị dữ liệu.
- **Business use case:** "Tìm việc phù hợp năng lực", "Nắm mặt bằng lương", "Đánh giá nhà tuyển dụng", "Theo dõi xu hướng kỹ năng".
- Quy trình thu thập – làm sạch – công bố dữ liệu vẽ bằng **activity diagram/BPMN**; domain class diagram: `TinTuyenDung`, `CongTy`, `KyNang`, `DanhGia`, `HoSoKyNang`, `DiaDiem`.

## Ca sử dụng đề xuất (chương 3)

| UC | Tên | Actor chính | Dữ liệu phía sau | Liên kết môn khác |
|---|---|---|---|---|
| UC001 | Tìm kiếm việc làm theo từ khóa/bộ lọc | Người tìm việc | `silver.job_postings`, chỉ mục tìm kiếm | WM4 |
| UC002 | Xem xu hướng nhu cầu kỹ năng | Người tìm việc, Chuyên viên | `mart_skill_demand_monthly` | WM2, BD gold |
| UC003 | So sánh mức lương theo vị trí/tỉnh | Người tìm việc, HR | `mart_salary_role_region` | BD gold |
| UC004 | Khai báo hồ sơ kỹ năng và nhận gợi ý việc làm | Người tìm việc | `mart_job_reco_candidates` | WM5 |
| UC005 | Xem đánh giá công ty theo khía cạnh | Người tìm việc | `mart_company_aspect_sentiment` | WM3 |
| UC006 | Đăng ký cảnh báo tin mới khớp hồ sơ | Người tìm việc | luồng streaming | BD streaming |
| UC007 | Xuất báo cáo thị trường (CSV/PDF) | HR, Chuyên viên | các mart | – |
| UC008 | Quản lý nguồn thu thập (bật/tắt, lịch) | Quản trị dữ liệu | cấu hình spider, Airflow | WM1, BD |
| UC009 | Giám sát chất lượng dữ liệu | Quản trị dữ liệu | kết quả GX, dbt tests | BD |
| UC010 | Đăng nhập/phân quyền | Mọi actor | – | – |

Actor hệ thống: **Airflow Scheduler** (kích hoạt UC008/009 theo lịch), **Trang tuyển dụng bên ngoài**. Mỗi UC kèm user story + acceptance criteria dạng Given/When/Then (l03), đạt tiêu chí INVEST.

## Yêu cầu phi chức năng đo được (theo tiêu chí "unambiguous, measurable" của l03)

| NFR | Phát biểu đề xuất | Cách kiểm thử (chương 6) |
|---|---|---|
| Hiệu năng | 95% truy vấn dashboard (UC002/003) trả về ≤ 3 giây trên gold | Script tải 20 người dùng đồng thời; số liệu Trino |
| Độ tươi | Tin mới xuất hiện trong UC001 ≤ 24 giờ sau khi đăng; cảnh báo UC006 ≤ 5 phút sau khi vào Kafka | So `crawl_ts` với thời điểm hiển thị |
| Tin cậy dữ liệu | 100% bản ghi gold vượt bộ kiểm tra GX/dbt; bản ghi lỗi vào DLQ | Báo cáo GX |
| Riêng tư | Không lưu trường PII ở silver/gold | Test tự động quét cột |
| Lịch sự khi crawl | ≤ 1 request/giây/domain, tôn trọng robots.txt | Log spider |
| Khả năng mở rộng nguồn | Thêm một trang tuyển dụng mới chỉ cần thêm một adapter, không sửa lõi | Review thiết kế (Adapter pattern) |
| Triển khai lại | Dựng lại toàn bộ môi trường từ repo ≤ 30 phút | Chạy thử trên máy sạch |

## Thiết kế (chương 4) – ánh xạ vào guideline

- **Kiến trúc logic:** layered cho cổng JobLens (Presentation → Application Service → Domain → Data Access qua Trino) + **event-driven** cho nền tảng dữ liệu (các kiểu kiến trúc có trong l05). Trình bày theo **4+1 views**.
- **Kiến trúc triển khai:** deployment diagram UML với node = K8s node/namespace, artifact = pod/container (vẽ lại theo ký pháp UML, không dán sơ đồ Helm).
- **Mẫu thiết kế (mục 4.2 của guideline):** *Adapter* cho mỗi trang nguồn; *Repository* cho các lớp trường cửu truy cập Trino; *Facade/Gateway* cho webservice; *Strategy* cho các thuật toán gợi ý/xếp hạng; *Observer/pub-sub* cho cảnh báo UC006.
- **Thiết kế ca sử dụng:** mỗi UC một biểu đồ lớp theo **ECB** (Entity–Control–Boundary, l04) + biểu đồ trình tự; biểu đồ máy trạng thái cho vòng đời `TinTuyenDung` (mới → đang mở → đã đóng → hết hạn).
- **Human-AI collaboration (l00):** ghi nhật ký những bước dùng AI hỗ trợ (ví dụ nháp user story, rà soát NFR) kèm phần người kiểm duyệt – vừa minh bạch vừa đúng định hướng môn.

## Metrics chấp nhận và chất lượng thiết kế

Mỗi metric thuộc về **đúng một môn** (quy tắc R4 trong [Quy tắc phân tách](07-quy-tac-phan-tach-mon.md)). Chỉ tiêu là đề xuất để nhóm có đích nhắm, sẽ hiệu chỉnh sau khi có số đo đầu tiên.

| Metric | Định nghĩa |
|---|---|
| Độ phủ yêu cầu | % UC có đặc tả + biểu đồ lớp/trình tự + kịch bản kiểm thử |
| Tỉ lệ đạt acceptance criteria | số kịch bản Given/When/Then đạt / tổng |
| NFR đạt | từng NFR ở mục Yêu cầu phi chức năng phía trên: đạt/không đạt, kèm bằng chứng (được phép trích số đo từ BD, không phân tích lại) |
| Truy vết | 100% UC truy vết được tới thành phần triển khai ([ma trận liên kết](06-ma-tran-lien-ket.md)) |
