# ADR 0001 – Ranh giới xử lý giữa các repo

| | |
|---|---|
| **Trạng thái** | ĐỀ XUẤT – chờ nhóm duyệt |
| **Ngày** | 2026-10-02 |
| **Người soạn** | Hoang Le (nháp bằng Claude Code) |
| **Cần đồng ý** | Người phụ trách BD: <Họ tên> · WM: <Họ tên> · SAD: <Họ tên> |
| **Ảnh hưởng** | cả 4 repo (`cross-repo`) |
| **Bản cài đặt** | Đã làm sẵn theo phương án đề xuất trong `joblens` v0.2.0 (contract ở trạng thái `draft`): schema, contract bảng, API tìm kiếm, `job_uid()`, biến D7, sửa docs kế hoạch. Điểm nào nhóm bác thì sửa ngược lại trước khi chuyển contract sang `stable` |

## Vì sao cần ADR này

Tài liệu kế hoạch đã quy định *file nào thuộc repo nào*, nhưng chưa quy định *bước xử lý nào do repo nào làm* ở các chỗ bàn giao. Có chỗ còn tự mâu thuẫn:

```
 Web Mining                 Big Data                                   PTTKHT (SA&D)
 ┌──────────┐  Kafka   ┌────────────────────────────────────┐  Trino  ┌───────────┐
 │ crawler  │ ───────► │ bronze → silver → gold (dbt)       │ ──────► │ app (web) │
 └──────────┘    ①     │            ▲         │             │    ③    └───────────┘
 ┌──────────┐          │            │ ②       │             │
 │ mô hình  │ ─────────┼──► chạy trong pipeline (Airflow)   │
 └──────────┘          └────────────────────────────────────┘
```

Không chốt thì có hai kiểu dẫm chân: hai repo cùng làm một việc (trùng code, trùng đóng góp trong báo cáo, vi phạm R2), hoặc một việc không ai làm. ADR này chốt 7 điểm (D1–D7). Mỗi điểm có thể duyệt riêng.

---

## D1 – Ai bóc tách (parse) trang tin

**Mâu thuẫn:**
- [docs/07](../project-plan/07-quy-tac-phan-tach-mon.md#ma-trận-sở-hữu) giao "spider, **parser**" cho WM.
- [docs/03](../project-plan/03-nen-tang-big-data.md) ghi "Spark silver jobs (**parse**, MinHash dedup, NER inference)", tức là BD.
- docs/02 và docs/11 nói bronze giữ HTML thô.

| Phương án | Mô tả | Được | Mất |
|---|---|---|---|
| **A** | Crawler (WM) parse luôn, gửi các trường đã tách vào Kafka. HTML thô lưu riêng trên S3, message chỉ trỏ tới | Khớp ma trận sở hữu; message nhỏ; schema `job_posting.v1` hiện tại đã theo cách này | Đổi parser thì phải crawl lại hoặc parse lại từ HTML trên S3 (WM tự làm) |
| B | Crawler gửi HTML vào Kafka, BD parse trong silver | Parse lại dễ trong pipeline | Parser nằm ở repo BD – trái ma trận; WM mất phần được chấm; message nặng (100–300 KB) |
| C | Gửi cả trường đã tách lẫn HTML | Linh hoạt | Message nặng, hai nơi giữ cùng dữ liệu |

**Đề xuất: A.**
- WM sở hữu parser và bộ lọc PII. HTML thô (đã qua lọc PII) nằm ở `s3://joblens/raw-html/<source>/<yyyy-mm-dd>/<source_job_id>.html.gz`, lưu tối đa 30 ngày.
- Thêm trường không bắt buộc `raw_html_uri` vào `job_posting` (bản **v1.1**, tăng minor).
- `bronze.jobs_raw` (BD) lưu nguyên message Kafka. "Thô" ở đây nghĩa là chưa chuẩn hóa, không phải HTML.
- BD vẫn chặn lần hai: bộ kiểm tra GX "silver không có cột PII".

**Kéo theo:** sửa câu trong docs/03 thành "Spark silver jobs (làm sạch, chuẩn hóa, gộp kết quả dedup/NER)"; sửa docs/02 thành "HTML thô lưu ở `s3://joblens/raw-html/`, không nằm trong bronze".

---

## D2 – Ai chuẩn hóa lương, địa điểm, kinh nghiệm, cấp bậc

**Mâu thuẫn:**
- [docs/04](../project-plan/04-khai-pha-web-mining.md) WM2 trích "span kỹ năng, **lương, kinh nghiệm, cấp bậc**".
- docs/03 silver (BD) cũng có "lương min/max VND, tỉnh/thành, cấp bậc".

| Phương án | Mô tả |
|---|---|
| **A** | BD chuẩn hóa mọi **trường có sẵn** (`salary_text`, `locations`, `experience_text`, `level`) bằng quy tắc, có GX kiểm tra. WM2 chỉ trích **kỹ năng** |
| B | WM2 trích tất cả, BD chỉ lưu kết quả |
| C | Cả hai cùng làm, so sánh |

**Đề xuất: A.**

| Việc | Repo | Ghi ra |
|---|---|---|
| `salary_text` → `salary_min_vnd`, `salary_max_vnd`, `salary_is_negotiable` | BD | `silver.job_postings` |
| `locations` → mã 34 tỉnh/thành (bảng ánh xạ là dbt seed) | BD | `silver.job_postings`, `dim_location` |
| `experience_text`, `level` → danh mục chuẩn | BD | `silver.job_postings` |
| Span kỹ năng trong mô tả + chuẩn hóa về ESCO (từ điển alias) | WM | `silver.job_skills` |
| *(Tùy chọn)* Trích lương/kinh nghiệm từ **đoạn mô tả tự do** khi trường có sẵn bị trống | WM, chỉ là thí nghiệm | Không ghi vào `silver.job_postings`. Muốn đưa vào hệ thống thì mở ADR mới |

**Kéo theo:** sửa WM2 trong docs/04 thành "span kỹ năng; chuẩn hóa ESCO". Câu "VietJobs cần tính lại lương từ chuỗi `salary`" (docs/13) giao cho BD (dùng cho backfill) – trở thành một expectation GX.

---

## D3 – Mô hình của WM chạy trong pipeline thế nào

**Mâu thuẫn:**
- [docs/08](../project-plan/08-to-chuc-repo-va-github.md) nói mô hình đóng thành **image Docker**, Airflow (BD) chạy bằng KubernetesPodOperator.
- [docs/10](../project-plan/10-phan-cong-va-lo-trinh.md) giao TV4 (BD) "**tích hợp mô hình WM thành Spark job**". Nếu làm vậy thì code mô hình nằm trong repo BD.

| Phương án | Mô tả | Được | Mất |
|---|---|---|---|
| **A** | WM giao **image Docker** có tag `x.y.z-gitsha`. Image đọc bảng đầu vào, ghi bảng đầu ra theo contract. BD chỉ viết DAG gọi image | Ranh giới sạch: không code mô hình nào ở repo BD | Chạy PhoBERT bằng CPU trong 1 pod – đủ cho lượng tin mới mỗi ngày, backfill 50k tin chạy lâu hơn |
| B | WM phát hành **thư viện Python** (wheel), Spark job của BD gọi qua pandas UDF | Phân tán được trên Spark | Cần đóng gói và quản lý phụ thuộc phức tạp; dễ trượt về "BD viết code mô hình" |
| C | WM tự lên lịch chạy và tự ghi bảng | WM chủ động | Hai bộ điều phối; trái "Airflow chạy toàn bộ đồ thị" (L14) |

**Đề xuất: A.** Hợp đồng chạy cho mọi image mô hình:

```
docker run <image>:<x.y.z-gitsha> \
  --input-table silver.job_postings --input-snapshot <snapshot-id> \
  --output-table silver.job_skills --run-id <airflow-run-id>
```

- Image ghi bằng `MERGE`/overwrite theo partition. Mỗi dòng có `extractor_version`.
- Biến môi trường dùng bộ `JOBLENS_*` (D7).
- WM cung cấp kèm **image stub** (trả kết quả từ từ điển) để BD chạy độc lập.
- Ai làm gì:
  - WM: code mô hình, Dockerfile, `models.yaml`, đo metric.
  - BD: DAG, tài nguyên pod, xử lý lỗi và chạy lại, ghi dòng vào `compat.md`.

**Kéo theo:**
- docs/10: TV4 đổi thành "đưa image mô hình WM vào DAG Airflow".
- docs/03: sơ đồ đổi "NER inference" từ khối Spark sang khối "Mining jobs (image)".

---

## D4 – Phục vụ tìm kiếm (UC001) và cảnh báo tin mới (UC006)

**Lỗ hổng:**
- docs/08 nói app **chỉ đọc gold qua Trino**. Nhưng chỉ mục tìm kiếm của WM4 (BM25 + embedding) không phải bảng Trino.
- UC006 cần "≤ 5 phút sau khi vào Kafka" (NFR ở docs/05), trong khi gold chạy theo lô 1–2 giờ.

Hai chức năng này chưa ai nhận.

### D4a – Tìm kiếm

| Phương án | Mô tả |
|---|---|
| **A** | WM build chỉ mục (lưu ở `s3://joblens/indexes/`) và giao **image dịch vụ tìm kiếm** (HTTP). BD triển khai image trên K8s. App gọi theo hợp đồng API trong `joblens` |
| B | App tự tìm bằng Trino (`LIKE`/full-text đơn giản) |
| C | Embedding lưu vào bảng gold, app tự tính độ tương đồng |

**Đề xuất: A, có đường lùi B.**
- Hợp đồng API đặt ở `joblens/schemas/api/search.v1.yaml` (OpenAPI), gồm `GET /search?q=&location=&limit=` → danh sách `job_uid` + điểm.
- App (SAD) gọi API này. Khi dịch vụ không chạy (ví dụ giảng viên chạy app một mình), app lùi về tìm bằng Trino hoặc gold mẫu.
- Nếu nhóm WM chọn WM5 thay vì WM4 thì UC001 chỉ dùng phương án B, do SAD làm.
- Phương án C bị loại vì đẩy việc tính toán ML vào app.

### D4b – Cảnh báo tin mới

| Phương án | Mô tả |
|---|---|
| **A** | App ghi đăng ký cảnh báo vào topic `app.alert_subscriptions.v1`. Job streaming của BD ghép tin mới với đăng ký và ghi topic `alerts.job_match.v1`. App đọc topic đó rồi thông báo cho người dùng (Observer) |
| B | App tự hỏi Trino định kỳ để tìm tin mới khớp hồ sơ |

**Đề xuất: A.**
- Mỗi topic có đúng một repo ghi: app ghi đăng ký, BD ghi kết quả ghép.
- Đáp ứng được NFR ≤ 5 phút. Đây cũng là bài demo streaming có trạng thái tốt cho BD.
- Logic ghép chỉ là lọc theo kỹ năng, từ khóa, địa điểm – không phải mô hình.
- Nếu không kịp làm thì lùi về B và nới NFR UC006 thành "≤ độ tươi của silver".

**Kéo theo:**
- Thêm 2 schema `alert_subscription.v1`, `job_match.v1`.
- Bảng "ai ghi topic nào" ở docs/09 quy tắc 2 thêm 2 dòng.
- docs/08 sửa "app chỉ đọc gold qua Trino" thành "app đọc gold qua Trino, gọi API tìm kiếm, ghi/đọc topic cảnh báo".

---

## D5 – Khóa của một tin: `job_uid` và `dup_group_id`

**Lỗ hổng:** chưa ai định nghĩa hai khóa này. Ví dụ, cùng một việc đăng trên TopCV và ITviec thì tính là một tin hay hai tin?

| Phương án | Mô tả |
|---|---|
| **A** | `job_uid` = mỗi tin trên mỗi nguồn một mã, tính cố định từ nguồn. Tin trùng giữa các trang được gom bằng `dup_group_id` do dedup sinh ra |
| B | `job_uid` dùng chung cho các tin trùng (gộp ngay khi sinh khóa) |

**Đề xuất: A.** Phương án B làm khóa đổi mỗi lần thuật toán dedup đổi, kéo theo mọi bảng tham chiếu bị vỡ.

- `job_uid = sha1("<source>:<source_job_id>")` (hex 40 ký tự). Repo nào cũng tự tính được và kết quả giống nhau.
  - Hàm này đặt trong package `joblens_contracts` để mọi repo dùng chung một cài đặt.
- WM chạy job dedup (dạng image, theo D3) và ghi bảng mới `silver.job_dedup(job_uid, dup_group_id, dedup_version, score)`.
- BD dùng `dup_group_id` để đếm tin duy nhất trong gold. Bảng `silver.job_postings` không tự tính dedup.
- WM đánh giá dedup (P/R/F1) trên các cặp `job_uid` đã gán nhãn.

**Kéo theo:**
- Thêm `job_uid()` vào `joblens_contracts`; thêm contract `silver.job_dedup`.
- docs/09 quy tắc 2 thêm dòng "`silver.job_dedup` – mining ghi".
- docs/03 bỏ "MinHash dedup" khỏi Spark silver jobs.

---

## D6 – Giảng viên và CI phải đọc được repo `joblens`

**Lỗ hổng:**
- README của 3 repo môn hướng dẫn `pip install git+…/joblens`, nhưng `joblens` là repo private.
- Theo docs/08, giảng viên chỉ được mời vào repo môn của mình, nên lệnh cài sẽ báo lỗi không tìm thấy repo và repo môn **không chạy độc lập được** (R9).
- GitHub Actions của repo môn cũng không cài được repo private khác nếu không có token.

| Phương án | Mô tả | Được | Mất |
|---|---|---|---|
| **A** | Để `joblens` **public** | Giảng viên và CI cài thẳng được, không cần token | Kế hoạch dự án công khai – chấp nhận được vì repo không có dữ liệu crawl, bí mật hay thông tin cá nhân (có pre-commit/gitleaks chặn) |
| B | Giữ private, mời mỗi giảng viên quyền Read trên `joblens` | Kín | CI repo môn vẫn cần token; phải nhớ mời từng người |
| C | Chép schema/fixtures vào từng repo môn | Không phụ thuộc mạng | Trái nguyên tắc "một file một bản gốc" – dễ lệch |

**Đề xuất: A.** Trước khi đổi sang public, chạy lại `gitleaks` trên toàn bộ lịch sử repo.

---

## D7 – Tên biến môi trường cho thông tin đăng nhập

**Lỗ hổng:** `.env.example` mới có địa chỉ dịch vụ. Thiếu biến cho khóa S3 và user Trino, nên mỗi repo sẽ tự đặt tên khác nhau.

**Đề xuất:** thêm vào `templates/env.example` (chỉ tên biến, giá trị trống hoặc mẫu), rồi đồng bộ sang 4 repo:

| Biến | Ý nghĩa |
|---|---|
| `JOBLENS_S3_ACCESS_KEY_ID`, `JOBLENS_S3_SECRET_ACCESS_KEY` | Khóa S3 (SeaweedFS) |
| `JOBLENS_S3_REGION` | Mặc định `us-east-1` |
| `JOBLENS_CATALOG_WAREHOUSE` | Tên warehouse trong Lakekeeper |
| `JOBLENS_TRINO_USER`, `JOBLENS_TRINO_PASSWORD` | Người dùng Trino (mật khẩu có thể trống khi chạy local) |
| `JOBLENS_SEARCH_URL` | Địa chỉ dịch vụ tìm kiếm (D4a) |

---

## Tổng hợp: sau khi duyệt, việc nào ở repo nào

| Repo | Việc |
|---|---|
| `joblens` | Schema `job_posting` v1.1 (`raw_html_uri`), `alert_subscription.v1`, `job_match.v1`; contract `silver.job_postings`, `silver.job_skills`, `silver.job_dedup`, `silver.review_aspects` và các mart gold cho UC001–UC005; `schemas/api/search.v1.yaml`; hàm `job_uid()`; biến D7 trong `env.example`; sửa docs/02, 03, 04, 05, 08, 09, 10 theo phần "Kéo theo"; cập nhật `repo-routing.md` mục E; gắn tag `v0.2.0` |
| BD | Chuẩn hóa trường có sẵn (D2); DAG gọi image mô hình và dedup (D3, D5); triển khai image tìm kiếm (D4a); job streaming ghép cảnh báo (D4b) |
| WM | Parser và lọc PII, HTML lên S3 (D1); image `skill-extractor`, image dedup, kèm stub (D3, D5); chỉ mục và image dịch vụ tìm kiếm nếu làm WM4 (D4a) |
| SAD | Gọi API tìm kiếm, có đường lùi (D4a); ghi đăng ký và đọc topic cảnh báo (D4b); cập nhật UC001, UC006 và deployment diagram |

## Cách duyệt

- Mỗi người phụ trách repo trả lời trong PR hoặc nhóm chat theo từng điểm: `D1 ok`, `D3 không – vì …`.
- D1, D3, D4, D5 có thể phá vỡ tương thích, nên phải có **đủ 3 người phụ trách đồng ý**. D2, D6, D7 áp dụng quy tắc 24 giờ không ai phản đối.
- Điểm nào bị bác thì ghi phương án được chọn và lý do vào bảng dưới, rồi đổi trạng thái ADR thành **ĐÃ CHẤP NHẬN**.

| Điểm | Kết quả | Phương án | Ngày | Ghi chú |
|---|---|---|---|---|
| D1 | <chờ> | | | |
| D2 | <chờ> | | | |
| D3 | <chờ> | | | |
| D4a | <chờ> | | | |
| D4b | <chờ> | | | |
| D5 | <chờ> | | | |
| D6 | <chờ> | | | |
| D7 | <chờ> | | | |
