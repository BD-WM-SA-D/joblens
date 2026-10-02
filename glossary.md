# Thuật ngữ chung JobLens

Bản glossary **duy nhất** của dự án (docs/project-plan/09, quy tắc 10). Rút từ bộ tài liệu kế hoạch trong `docs/project-plan/`. Cột "Môn" cho biết thuật ngữ chủ yếu thuộc ngữ cảnh môn nào (quy tắc R5 – mỗi báo cáo dùng thuật ngữ của môn mình).

## Nghiệp vụ và dữ liệu

| Thuật ngữ | Nghĩa trong dự án | Môn |
|---|---|---|
| Tin tuyển dụng (job posting) | Một tin đăng việc làm trên trang nguồn; khóa nguồn là `source_job_id` | Chung |
| `job_uid` | Khóa của một tin trên một nguồn: `sha1("<source>:<source_job_id>")`, tính bằng `joblens_contracts.job_uid()`. Cùng việc trên hai trang là hai `job_uid` (ADR 0001 D5) | Chung |
| `dup_group_id` | Nhóm tin trùng giữa các trang, do dedup (WM1) ghi vào `silver.job_dedup`; giá trị là `job_uid` đại diện của nhóm | Chung |
| `company_key` | Khóa công ty đã gộp giữa các nguồn (`gold.dim_company`) | Chung |
| `raw_html_uri` | Đường dẫn HTML thô đã lọc PII trên `s3://joblens/raw-html/` (giữ 30 ngày, không nằm trong bronze) | Chung |
| Mã tỉnh (`location_code`) | Mã đơn vị hành chính 2 chữ số sau sắp xếp 2025, ví dụ `01` Hà Nội, `79` TP.HCM (`gold.dim_location`) | Chung |
| Review công ty | Đánh giá công khai về nhà tuyển dụng (ITviec), có điểm theo 5 khía cạnh | Chung |
| Nguồn (source) | Trang hoặc dataset sinh dữ liệu: `topcv`, `itviec`, `vietjobs`, `synthetic` | Chung |
| Snapshot tin | Trạng thái của các tin đang mở tại một ngày, phục vụ phân tích vòng đời tin và biến động lương | BD |
| `first_seen` | Lần đầu crawl thấy một tin; thay cho ngày đăng khi trang không ghi rõ | Chung |
| PII | Dữ liệu cá nhân (tên, email, SĐT người đăng tin/người review, CV); loại bỏ từ tầng silver, không lưu ở đâu cả | Chung |
| Dữ liệu synthetic | Dữ liệu giả lập (luồng `events.user`, fixtures tự soạn); kết quả trên dữ liệu này phải ghi rõ là synthetic | Chung |
| VietJobs | Dataset 48.092 tin TopCV (LREC 2026), dùng cho backfill, nhãn yếu và baseline | Chung |
| ESCO | Taxonomy kỹ năng/nghề của EU, đích chuẩn hóa kỹ năng | Chung |
| Từ điển alias kỹ năng | Bảng ánh xạ cách viết kỹ năng (Việt/Anh, viết tắt) về ESCO skill URI | WM |
| Hợp đồng dữ liệu (data contract) | Schema message Kafka, contract bảng và hợp đồng API trong `schemas/` của repo này; cơ chế duy nhất nối các repo. `draft` = còn được đổi, `stable` = đổi theo SemVer | Chung |
| Image mô hình | Image Docker có tag `x.y.z-gitsha` do repo WM giao; Airflow của BD chạy bằng KubernetesPodOperator theo hợp đồng chạy ở ADR 0001 D3 | Chung |

## Nền tảng dữ liệu (Big Data)

| Thuật ngữ | Nghĩa | Môn |
|---|---|---|
| Topic / partition / offset | Kênh message Kafka, phân vùng của topic, vị trí message trong phân vùng | BD |
| Partition key | Khóa quyết định message vào partition nào (`source_job_id`, `company_id`, `user_id`) | BD |
| Consumer group, consumer lag | Nhóm consumer chia nhau partition; độ trễ offset của group so với đầu topic | BD |
| DLQ | Dead-letter queue – topic `dlq.parse_errors.v1` chứa bản ghi lỗi parse | BD |
| Lakehouse | Kiến trúc kết hợp data lake (object storage) với tính năng kho dữ liệu (ACID, schema) qua table format | BD |
| Table format (Iceberg) | Lớp metadata trên file Parquet cho ACID, schema evolution, time travel | BD |
| Snapshot / tag Iceberg | Phiên bản bảng tại một thời điểm; tag là tên gắn cho snapshot (ví dụ `report-bd-v1`) | BD |
| Zone bronze / silver / gold | Thô (append-only) / đã làm sạch, khử trùng, làm giàu / mart phục vụ truy vấn | BD |
| Partition spec | Cách chia dữ liệu bảng Iceberg, ví dụ `days(ingest_ts)`, `bucket(16, job_uid)` | BD |
| Compaction | Gộp file nhỏ, expire snapshot cũ để giữ sức khỏe bảng | BD |
| Watermark / checkpoint | Ngưỡng event time chấp nhận dữ liệu trễ / trạng thái lưu để streaming chạy lại đúng | BD |
| Freshness | `gold_available_ts − crawl_ts` | BD |
| Lambda / Kappa | Kiến trúc hai đường batch + streaming / một đường streaming có replay | BD |
| Mart | Bảng gold phục vụ trực tiếp một nhu cầu, ví dụ `mart_salary_role_region` | BD |
| Catalog (REST) | Dịch vụ quản lý metadata bảng Iceberg (Lakekeeper) | BD |
| ADR | Architecture Decision Record – ghi lại một quyết định kỹ thuật; danh mục ở `adr-index.md` | Chung |

## Khai phá web (Web Mining)

| Thuật ngữ | Nghĩa | Môn |
|---|---|---|
| Crawl lịch sự | Tôn trọng robots.txt, ≤ 1 request/giây/domain, User-Agent ghi rõ mục đích | WM |
| Dedup, MinHash LSH, shingling | Phát hiện tin trùng/gần trùng giữa các trang (WM1) | WM |
| Corpus | Tập văn bản dùng để huấn luyện/đánh giá | WM |
| Span, BIO, `SKILL` | Đoạn văn bản được gán nhãn; lược đồ nhãn Begin-Inside-Outside; nhãn kỹ năng (WM2) | WM |
| Nhãn yếu (weak label) | Nhãn sinh tự động (tag nhà tuyển dụng, cột kỹ năng LLM của VietJobs, điểm sao) – không dùng làm tập test | WM |
| ABSA, aspect, polarity | Khai phá quan điểm theo khía cạnh; khía cạnh; phân cực cảm xúc (WM3) | WM |
| Baseline | Phương pháp đơn giản làm mốc so sánh | WM |
| Cohen's κ | Độ đồng thuận giữa người gán nhãn | WM |
| Embedding, bi-encoder | Biểu diễn vector của văn bản; mô hình mã hóa truy vấn và tài liệu riêng (WM4) | WM |
| BM25, nDCG@10, MAP | Mô hình xếp hạng từ khóa; các metric đánh giá xếp hạng | WM |
| Content-based, implicit CF, ALS | Gợi ý dựa nội dung; lọc cộng tác trên tương tác ngầm; thuật toán Alternating Least Squares (WM5) | WM |
| Cold-start | Người dùng/tin mới chưa có tương tác | WM |
| PageRank, Louvain, modularity | Xếp hạng nút; phát hiện cộng đồng; chất lượng phân cụm (WM6) | WM |

## Phân tích thiết kế hệ thống (SA&D)

| Thuật ngữ | Nghĩa | Môn |
|---|---|---|
| Tác nhân (actor) | Người tìm việc, Nhà tuyển dụng/HR, Chuyên viên phân tích, Quản trị dữ liệu; actor hệ thống: Airflow Scheduler, trang tuyển dụng bên ngoài | SA&D |
| Ca sử dụng (UC) | UC001–UC010, xem `docs/project-plan/05-phan-tich-thiet-ke-he-thong.md` | SA&D |
| User story, INVEST, acceptance criteria | Phát biểu yêu cầu theo người dùng; tiêu chí chất lượng story; tiêu chí chấp nhận dạng Given/When/Then | SA&D |
| Yêu cầu phi chức năng (NFR) | Yêu cầu đo được về hiệu năng, độ tươi, riêng tư… | SA&D |
| Lớp thực thể / điều khiển / biên (ECB) | Entity – Control – Boundary trong thiết kế ca sử dụng | SA&D |
| 4+1 views | Logical, process, development, physical + scenarios | SA&D |
| Cổng JobLens | Ứng dụng (API + UI) phục vụ người dùng; nền tảng dữ liệu là hệ thống con | SA&D |

## Quy ước dự án

| Thuật ngữ | Nghĩa |
|---|---|
| Phạm vi đánh giá | Khung mở đầu mỗi README/báo cáo, nêu phần nào đề nghị chấm cho môn đó (R10) |
| Ma trận sở hữu | Bảng quy định mỗi artifact chỉ có một môn chấm chính (docs/project-plan/07) |
| `cross-repo` | Nhãn cho issue/PR chạm tới repo khác |
| `compat.md` | Bảng phiên bản platform × mining × app × contracts của mỗi lần chạy (repo platform, `deploy/compat.md`) |
| Tag báo cáo | `report-bd-v1`, `report-wm-v1`, `report-sad-v1` – git tag + Iceberg tag cùng tên chốt số liệu (R13) |
