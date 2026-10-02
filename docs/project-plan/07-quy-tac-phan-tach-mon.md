> [← Mục lục](README.md)

# Quy tắc phân tách giữa các môn

Mục tiêu: dùng chung một hệ thống để tiết kiệm công, nhưng **ba báo cáo phải là ba sản phẩm học thuật khác nhau**, mỗi báo cáo đứng độc lập và không bị xem là nộp trùng.

## Ma trận sở hữu

Ký hiệu: **A** = môn chấm chính, **R** = chỉ tham chiếu, **–** = không đưa vào.

| Thành phần / artifact | Big Data | Web Mining | SA&D |
|---|---|---|---|
| Spider, parser, lịch sự khi crawl, dedup (thuật toán + đánh giá) | R (chỉ producer → Kafka) | **A** | R (UC008) |
| Thiết kế topic Kafka, schema message, producer/consumer config | **A** | – | R (deployment) |
| Bảng Iceberg, zone bronze/silver/gold, partition spec, compaction | **A** | R (đọc dữ liệu) | R (lớp trường cửu/ERD) |
| dbt models, GX suites, Airflow DAG | **A** | – | R (UC009) |
| Thí nghiệm batch vs streaming, ADR Lambda/Kappa | **A** | – | R (chỉ trích quyết định) |
| Manifest/Helm K8s, tài nguyên, monitoring | **A** | – | R (deployment diagram) |
| Tập gán nhãn, mô hình IE/ABSA/IR/RecSys/Graph, thí nghiệm & metric mô hình | R (chỉ nói job chạy trên Spark) | **A** | R (UC tiêu thụ kết quả) |
| Mô hình nghiệp vụ, UC, user story, NFR, UML, mẫu thiết kế, 4+1 | – | – | **A** |
| Cổng JobLens (API + UI), kịch bản kiểm thử chấp nhận | – | R (demo kết quả) | **A** |
| **Repo nộp** | `joblens-platform` | `joblens-mining` | `joblens-app` |

## Các quy tắc

**R1 – Một hệ thống, ba câu hỏi.** Mỗi đoạn trong báo cáo phải trả lời câu hỏi của môn đó (xem [Tóm tắt đề xuất](01-tong-quan.md#tóm-tắt-đề-xuất)): BD – *lưu/di chuyển/xử lý thế nào và vì sao*; WM – *khai phá được gì, bằng kỹ thuật nào, tốt đến đâu*; SA&D – *phục vụ ai, cần gì, thiết kế ra sao*. Đoạn nào không trả lời câu hỏi của môn thì chuyển xuống phụ lục hoặc thay bằng một câu tham chiếu.

**R2 – Mỗi artifact chỉ có một chủ.** Theo ma trận sở hữu ở trên. Một nội dung không được trình bày như *đóng góp chính* ở hai báo cáo.

**R3 – Ngân sách trùng lặp.** Phần bối cảnh chung tối đa ~1 trang mỗi báo cáo và phải **viết lại theo góc nhìn môn**. Không sao chép nguyên văn đoạn văn giữa các báo cáo.

**R4 – Metric thuộc về môn.** Metric nền tảng → BD; metric mô hình → WM; kết quả chấp nhận/NFR → SA&D. SA&D được *trích* số đo của BD làm bằng chứng kiểm thử NFR, nhưng không phân tích lại.

**R5 – Ký pháp riêng cho từng môn.** Cùng một thành phần nhưng mỗi báo cáo vẽ bằng ký pháp của môn mình:

| | SA&D | Big Data | Web Mining |
|---|---|---|---|
| Hình | UML chuẩn (use case, class ECB, sequence, state, package, deployment) | Sơ đồ luồng dữ liệu/zone, topic–partition, bố cục bảng/partition | Pipeline mô hình, phân bố nhãn, confusion matrix, đường học |
| Thuật ngữ | ca sử dụng, tác nhân, lớp thực thể/điều khiển/biên, yêu cầu phi chức năng | topic, partition, offset, table format, snapshot, watermark, zone | corpus, gán nhãn, baseline, span, embedding, nDCG |

Không dán cùng một hình vào hai báo cáo.

**R6 – Mỗi môn một repo, mỗi việc một nhãn.** Code và tài liệu tách thành 4 repo trong GitHub Organization: `joblens-platform` (link nộp BD), `joblens-mining` (link nộp WM), `joblens-app` (link nộp SA&D) và `joblens-contracts` (dùng chung). Chi tiết cấu trúc, cách nối các repo và phân quyền: [Tổ chức repo và GitHub](08-to-chuc-repo-va-github.md). Trong từng repo:

- Mỗi issue/PR có đúng một người phụ trách; việc chạm tới repo khác gắn nhãn `cross-repo`.
- Mỗi người commit vào repo của môn mình học (R7), nên lịch sử commit của từng repo là bằng chứng đóng góp sạch cho môn đó.
- Nguồn báo cáo của môn nằm trong `docs/` của chính repo môn đó; glossary và ADR index dùng chung nằm ở `joblens-contracts`.

**R7 – Người đứng tên theo môn đăng ký học.** Nhóm lập bảng đăng ký (ai học môn nào). Chủ của một phần phải là người học môn chấm phần đó; người không học môn đó có thể hỗ trợ nhưng không đứng tên đóng góp chính trong báo cáo môn ấy.

| Thành viên | BD (20261) | SA&D (20261) | WM (20261) | Vai trò chính |
|---|---|---|---|---|
| TV1 | ☐ | ☐ | ☐ | |
| TV2 | ☐ | ☐ | ☐ | |
| TV3 | ☐ | ☐ | ☐ | |
| TV4 | ☐ | ☐ | ☐ | |
| TV5 | ☐ | ☐ | ☐ | |

**R8 – Phép thử "gỡ bỏ".** Nếu bỏ phần X khỏi báo cáo mà giảng viên môn đó không mất gì để chấm thì X không thuộc báo cáo này.

**R9 – Phép thử "đọc độc lập".** Mỗi báo cáo phải đọc hiểu được mà không cần hai báo cáo kia. Tham chiếu chéo chỉ ở dạng "chi tiết kỹ thuật xem tài liệu kèm theo, mục …".

**R10 – Minh bạch với giảng viên.** Mỗi báo cáo mở đầu bằng một khung "Phạm vi đánh giá", ví dụ:

> *Dự án JobLens dùng chung hạ tầng dữ liệu với môn [X] và [Y] (đã được giảng viên đồng ý ngày …). Báo cáo này chỉ trình bày và đề nghị đánh giá các phần: … Các phần … thuộc môn khác và chỉ được nhắc tới để làm rõ bối cảnh.*

**R11 – Demo tách kịch bản.** Ba kịch bản demo khoảng 10 phút, mỗi kịch bản nhấn đúng phần của môn: BD (replay Kafka, streaming vs batch, time travel, GX chặn dữ liệu bẩn, Grafana); WM (trích xuất kỹ năng trên tin mới, ABSA một công ty, so sánh BM25 với hybrid); SA&D (đi qua UC001–UC005 trên UI, truy vết từ UC tới deployment).

**R12 – Căn cứ tài liệu theo môn.** Mỗi báo cáo lấy bài giảng và tài liệu của chính môn đó làm căn cứ chính (xem [Tài liệu tham khảo](12-tai-lieu-tham-khao.md)).

**R13 – Số liệu tái lập được.** Mỗi báo cáo chốt số liệu bằng một git tag ở đúng repo của môn và một Iceberg tag cùng tên:

| Môn | Git tag (repo) | Ghi kèm trong release note |
|---|---|---|
| Big Data | `report-bd-v1` (`joblens-platform`) | Iceberg tag, version `joblens-contracts`, tag image mining/app đang chạy |
| Web Mining | `report-wm-v1` (`joblens-mining`) | Iceberg snapshot dùng để train/test, version model |
| SA&D | `report-sad-v1` (`joblens-app`) | Version platform + contracts dùng khi kiểm thử chấp nhận |

## Khung báo cáo gợi ý cho từng môn

| SA&D (theo `group-project-guideline.docx`) | Big Data (đề xuất, bám L14 "course wrap") | Web Mining (đề xuất) |
|---|---|---|
| 1. Đặt vấn đề | 1. Bài toán dữ liệu & 5V | 1. Bài toán & dữ liệu web |
| 2. Phân tích nghiệp vụ | 2. Kiến trúc four-layer & quyết định (ADR) | 2. Thu thập & tiền xử lý (WM1) |
| 3. Phân tích yêu cầu (UC, NFR) | 3. **Store:** object storage, Iceberg, partition, compaction | 3. Trích xuất thông tin (WM2) |
| 4. Thiết kế (4+1, mẫu thiết kế, ECB, trình tự) | 4. **Move:** Kafka topic/partition/acks/EOS | 4. Khai phá quan điểm (WM3) |
| 5. Thực hiện & triển khai (deployment UML) | 5. **Process:** Spark batch vs streaming, watermark, checkpoint | 5. IR / RecSys / Graph (WM4–6, chọn) |
| 6. Thử nghiệm & đánh giá (acceptance, NFR) | 6. **Query:** Trino, pruning, hiệu năng | 6. Thực nghiệm, metric, phân tích lỗi |
| 7. Kết luận | 7. **Integrate:** dbt + GX + Airflow; 8. Triển khai K8s & đo đạc; 9. Kết luận | 7. Kết luận & hạn chế (dữ liệu synthetic, thiên lệch nguồn) |
