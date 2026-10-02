> [← Mục lục](README.md)

# Tổng quan, căn cứ và lựa chọn phương án

## Tóm tắt đề xuất

Nhóm đề xuất xây dựng **JobLens VN** – một hệ thống thu thập tin tuyển dụng và đánh giá công ty từ các trang việc làm Việt Nam, lưu trữ theo kiến trúc lakehouse trên Kubernetes, khai phá tri thức (kỹ năng, mức lương, quan điểm về nhà tuyển dụng, gợi ý việc làm) và phục vụ người dùng qua một cổng web.

Ý tưởng cốt lõi là **một hệ thống, ba lăng kính**. Cả ba môn cùng dùng một hệ thống và một bộ dữ liệu, nhưng mỗi môn chấm một câu hỏi khác nhau, và mỗi thành phần chỉ có **một môn là nơi chấm chính** (xem [Quy tắc phân tách giữa các môn](07-quy-tac-phan-tach-mon.md)).

| Lăng kính | Câu hỏi môn này trả lời | Phần hệ thống được chấm chính |
|---|---|---|
| **Big Data Storage & Processing** | Dữ liệu được *di chuyển, lưu trữ, xử lý* ở quy mô lớn như thế nào, và vì sao chọn như vậy? | Kafka → Spark (batch + streaming) → Iceberg bronze/silver/gold → dbt → Great Expectations → Airflow → Trino, triển khai trên Kubernetes |
| **Web Mining** | *Tri thức gì* được khai phá từ dữ liệu web, bằng kỹ thuật nào, và *tốt đến đâu*? | Crawler + tiền xử lý, trích xuất kỹ năng (IE), khai phá quan điểm (ABSA), tìm kiếm/gợi ý việc làm, đồ thị kỹ năng |
| **Phân tích thiết kế hệ thống** | Hệ thống phục vụ *ai*, cần *đáp ứng gì*, được *thiết kế* thế nào? | Mô hình nghiệp vụ, yêu cầu (UC, NFR), kiến trúc 4+1, thiết kế ca sử dụng (ECB), cổng web JobLens |

Vì sao chọn domain tuyển dụng (so với review TMĐT hay tin tức): đây là domain duy nhất trong 3 phương án mà **mỗi bài giảng Web Mining đều có chỗ áp dụng tự nhiên** (IR, Link Analysis, Opinion Mining, Information Extraction, Recommender, Query Mining), có **dataset học thuật công khai rất mới** để làm baseline (VietJobs, LREC 2026), và có **actor nghiệp vụ rõ ràng** cho SA&D (người tìm việc, nhà tuyển dụng, chuyên viên phân tích).

## Căn cứ từ tài liệu môn học

Đề xuất được đối chiếu trực tiếp với slide và tài liệu trong thư mục `HUST/IT` của nhóm (không dựa vào suy đoán).

| Môn | Tài liệu đã đọc | Điều rút ra cho đề xuất |
|---|---|---|
| Big Data Storage & Processing (IT4931) | L01–L14, đặc biệt **L14 Lakehouse pipeline – "Project ideas (course)"** | Đề tài môn gợi ý đúng một *mini lakehouse*: Kafka topic → Spark land → Iceberg → dbt marts; thêm 1 bộ Great Expectations + 1 Airflow DAG *fail-on-error*; **so sánh batch-only vs streaming bronze trên cùng một mart**; Trino query gold; Spark ML (L13) là consumer tùy chọn. Slide nhấn mạnh: *"Demonstrate integration, not every advanced feature of each tool."* |
| | L10 Spark batch | Kubernetes được nêu là cluster manager "modern default on cloud" (`--master k8s://…`). Slide **không** ghi K8s là bắt buộc cho đồ án → yêu cầu "phải dùng Kubernetes" nhóm nghe trên lớp cần xác nhận phạm vi (xem [câu hỏi cho giảng viên](11-rui-ro-va-cau-hoi.md#câu-hỏi-cần-xác-nhận-với-giảng-viên)). |
| | L04, L05, L07, L08, L09, L11, L13 | Căn cứ cho thiết kế Iceberg (ACID, time travel), NoSQL/vector search, Trino (pushdown, connector), Kafka (partition key, acks, consumer group, EOS), Lambda vs Kappa, watermark/checkpoint, Spark ML pipeline. |
| Phân tích thiết kế hệ thống (IT3120, GV Nguyễn Hữu Đức) | `group-project-guideline.docx`, l00–l05 | Báo cáo **bắt buộc 7 chương**: Đặt vấn đề · Phân tích nghiệp vụ (optional) · Phân tích yêu cầu (biểu đồ gói, biểu đồ ca sử dụng, đặc tả UC, NFR) · Thiết kế (kiến trúc logic + triển khai, mẫu thiết kế, thiết kế từng UC bằng biểu đồ lớp/trình tự/máy trạng thái) · Thực hiện & triển khai · Thử nghiệm & đánh giá · Kết luận. Group project chiếm **50%** điểm. Ví dụ đề tài trong slide là các hệ thống quản lý (thư viện, POS, courseware, healthcare…) nhưng danh sách để mở ("…"). Slide có RUP, business modeling (business actor/worker, BPMN), user story + INVEST + acceptance criteria, ECB pattern, 4+1 views, các kiến trúc layered / event-driven / microservices / space-based, và định hướng **Human-AI collaboration** trong phân tích thiết kế. |
| Web Mining | L01–L09 | Không tìm thấy file yêu cầu đồ án. Nội dung bài giảng: ML cơ bản, Data visualization, **Information Retrieval** (mô hình, đánh giá, tiền xử lý, inverted index, web search, spam), **Link Analysis** (graph ranking, community detection, graph representation), **Opinion Mining** (unsupervised/supervised sentiment, aspect-based), **Information Extraction** (NER, relation extraction, coreference), **Recommender Systems** (kNN CF, Matrix Factorization, NCF, session-based, đánh giá), **Online Ads & Query Mining**. |

> **Kỳ học.** Cả ba môn đều học trong học kỳ **20261** (tên thư mục Web mining ghi 20262 là ghi nhầm), nên toàn bộ dự án chạy theo một [lộ trình chung](10-phan-cong-va-lo-trinh.md#lộ-trình).

## Bài toán và phạm vi

**Phát biểu bài toán.** Sinh viên và người đi làm khó trả lời các câu hỏi rất thực tế: *kỹ năng nào đang được tuyển nhiều nhất ở vị trí tôi nhắm tới? mức lương thực tế theo vị trí và tỉnh/thành là bao nhiêu? công ty này được nhân viên đánh giá thế nào về lương, môi trường, quản lý? với bộ kỹ năng hiện có, tôi hợp với tin tuyển dụng nào?* Thông tin nằm rải rác trên nhiều trang, không chuẩn hóa (lương "Thỏa thuận", USD/VND, kỹ năng viết lẫn Anh–Việt), và thay đổi hằng ngày.

**Trong phạm vi**

- Thu thập định kỳ tin tuyển dụng (ưu tiên nhóm ngành CNTT, mở rộng nếu kịp) và đánh giá công ty công khai.
- Pipeline lakehouse có cả đường batch và streaming, có kiểm soát chất lượng và điều phối, chạy trên Kubernetes.
- Chuẩn hóa: lương, địa điểm (34 tỉnh/thành sau sắp xếp 2025), kỹ năng (từ điển alias Việt–Anh ánh xạ về ESCO).
- Khai phá: trích xuất kỹ năng, khai phá quan điểm theo khía cạnh, tìm kiếm + gợi ý việc làm, đồ thị kỹ năng.
- Cổng web JobLens cho người tìm việc, nhà tuyển dụng/chuyên viên phân tích, quản trị dữ liệu.

**Ngoài phạm vi**

- Không thu thập CV hay bất kỳ trang nào cần đăng nhập; không lưu thông tin cá nhân (tên, email, số điện thoại người đăng tin/người review).
- Không vận hành production, không cam kết SLA thật; không huấn luyện LLM.
- Không làm hệ thống ứng tuyển/thanh toán.

## Phương án thay thế

Hai phương án dưới đây dùng **cùng kiến trúc và cùng bộ quy tắc**; chỉ đổi nguồn dữ liệu và các bài khai phá.

| | Phương án 2 – Review & giá TMĐT | Phương án 3 – Tin tức tiếng Việt |
|---|---|---|
| Nguồn | Shopee/Tiki/Lazada (nhiều trang dùng API nội bộ, chống bot mạnh – rủi ro crawl cao) | VnExpress, Tuổi Trẻ, Dân Trí… (dễ crawl hơn, cần kiểm tra robots) |
| Dataset nền | [Shopee Vietnamese Product Reviews Sentiment (Kaggle)](https://www.kaggle.com/datasets/dduongdev/shopee-vietnamese-product-reviews-sentiment), UIT-ViSFD, [ViSpamReviews – phát hiện review rác](https://arxiv.org/html/2405.13292v2), [5CD-AI Vietnamese-Sentiment-visobert](https://huggingface.co/5CD-AI/Vietnamese-Sentiment-visobert) | [bkai NewsCategory](https://huggingface.co/datasets/bkai-foundation-models/NewsCategory), [BN_VNNews1072](https://huggingface.co/datasets/BaoNhan/BN_VNNews1072), [awesome-vietnamese-nlp](https://github.com/vndee/awsome-vietnamese-nlp) |
| Bài khai phá mạnh | Sentiment/ABSA, phát hiện review rác, gợi ý sản phẩm | Phân loại chủ đề, phát hiện tin trùng/lan truyền, NER, tóm tắt |
| Điểm yếu | SA&D dễ đơn điệu; rủi ro pháp lý/anti-bot | Ít actor nghiệp vụ; Recommender/Link analysis gượng |
