> [← Mục lục](README.md)

# Phân công và lộ trình

## Phân công 4–5 người

Phân công theo **môn chủ** để khớp quy tắc R7 ([Quy tắc phân tách](07-quy-tac-phan-tach-mon.md)); mỗi người có thêm một vai trò phụ để hiểu toàn hệ thống.

| Vai trò | Nhiệm vụ chính | Môn chủ | Vai trò phụ |
|---|---|---|---|
| **TV1 – Data acquisition & IE** | Spider TopCV/ITviec, parser, dedup (WM1), bộ gán nhãn + mô hình trích xuất kỹ năng (WM2) | WM | Viết producer Kafka cùng TV3 |
| **TV2 – Opinion & Retrieval** | ABSA review công ty (WM3), tìm kiếm hoặc gợi ý (WM4/WM5), đồ thị kỹ năng (WM6) | WM | Event-generator |
| **TV3 – Platform & Streaming** | k3d, Strimzi/Kafka, SeaweedFS, Lakekeeper, Trino, monitoring; đường streaming bronze; thí nghiệm batch vs streaming | BD | Deployment diagram cho TV5 |
| **TV4 – Processing & Quality** | Spark jobs silver, dbt gold, GX suites, Airflow DAG, compaction; đo hiệu năng | BD | Đưa image mô hình WM vào DAG Airflow (ADR 0001 D3) |
| **TV5 – Analyst/Architect & PM** | Mô hình nghiệp vụ, UC, NFR, UML, ADR phía ứng dụng; cổng JobLens (API + UI); kiểm thử chấp nhận; điều phối nhóm | SA&D | Glossary, ma trận truy vết |

**Nếu nhóm 4 người:** gộp TV1 + TV2 thành một người phụ trách WM1–WM3 và bỏ WM4–WM6 (chỉ giữ 3 bài lõi); hoặc TV3 kiêm luôn Airflow/GX nếu TV4 cần hỗ trợ phần WM. Luôn giữ **một người chuyên trách SA&D**, vì 7 chương cùng toàn bộ UML là khối lượng lớn nhất về tài liệu.

**Nhịp làm việc gợi ý:** họp 30 phút/tuần, board Kanban lọc theo nhãn môn, demo nội bộ cuối mỗi giai đoạn.

## Lộ trình

Cả ba môn học song song trong kỳ 20261. Lịch tính từ tuần 05/10/2026, giả định còn khoảng 12 tuần; cần khớp lại với deadline chính thức của từng môn (ba môn có thể có mốc nộp khác nhau – lấy mốc sớm nhất làm hạn chốt số liệu).

| Giai đoạn | Tuần | Big Data | Web Mining | SA&D | Mốc |
|---|---|---|---|---|---|
| P0 Chốt | T0 (29/09–04/10) | Hỏi GV phạm vi K8s | – | Hỏi GV về dùng chung đề tài | Bảng đăng ký, repo, glossary |
| P1 Khung chạy được | T1–T2 | k3d + Strimzi + SeaweedFS + Lakekeeper + Trino; 1 spider → Kafka → bronze streaming | Spider TopCV + ITviec, crawl lịch sự; backfill VietJobs | Chương 1, business model, danh sách UC | "Walking skeleton" end-to-end |
| P2 Dữ liệu sạch | T3–T5 | Silver + dbt gold + GX + Airflow DAG | Guideline gán nhãn, tập IE, baseline từ điển; dedup MinHash | Đặc tả UC, NFR (chương 3), kiến trúc logic | Mart đầu tiên truy vấn được qua Trino |
| P3 Khai phá & ứng dụng | T6–T8 | Thí nghiệm batch vs streaming, compaction, monitoring | PhoBERT IE, ABSA, WM4/WM5 | Thiết kế UC (ECB, trình tự), cổng JobLens UC001–005 | Demo nội bộ |
| P4 Đo & kiểm thử | T9–T10 | Benchmark, tối ưu, tag `report-bd-v1` | Đánh giá, phân tích lỗi, tag `report-wm-v1` | Chương 5–6, acceptance tests, tag `report-sad-v1` | Chốt số liệu |
| P5 Hoàn thiện | T11–T12 | Báo cáo + demo BD | Báo cáo + demo WM | Báo cáo + slide SA&D | Nộp bài |

Vì ba môn chạy song song, phần Web Mining không thể chờ nền tảng hoàn chỉnh mới bắt đầu: từ T1 nhóm WM làm việc trực tiếp trên VietJobs và dữ liệu crawl thô (file Parquet) để gán nhãn và làm baseline, đến P2 mới chuyển sang đọc từ bảng silver. Crawler chạy liên tục từ T1 để đến cuối kỳ có khoảng 10 tuần dữ liệu snapshot cho phân tích xu hướng.
