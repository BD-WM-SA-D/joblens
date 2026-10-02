## Phạm vi repo này: `Web-mining-joblens` (Web Mining)

Câu hỏi môn chấm: *tri thức gì* được khai phá từ dữ liệu web, bằng kỹ thuật nào, và *tốt đến đâu*.

**Thuộc về đây:**
- `crawler/`: spider, parser, adapter từng trang, producer ghi vào Kafka, thuật toán dedup (WM1).
- `ie/`, `absa/`, `retrieval/`, `recsys/`, `graph/`: mô hình WM2–WM6, từ điển alias kỹ năng.
- `annotation/`: guideline gán nhãn và thống kê κ (không có dữ liệu nhãn).
- `experiments/`: notebook đã xóa output, cùng bảng kết quả.
- `images/`: Dockerfile cho job mô hình. `models.yaml`: danh mục model.
- `docs/` (nguồn báo cáo Web Mining) và `docs/adr/`.

**Không thuộc về đây:**
- Helm, manifest K8s, khai báo topic, dbt, GX, DAG Airflow → `Big-Data-Storage-and-Processing-joblens`.
- UML, đặc tả UC, API/UI → `PTTKHT-joblens`.
- Schema message hay contract bảng (kể cả `silver.job_skills`) → `joblens`.

**Quy tắc riêng:**
- **Crawl lịch sự:** tôn trọng robots.txt, ≤ 1 request/giây/domain, User-Agent ghi rõ mục đích học tập. Không crawl trang cần đăng nhập, không chạm đường dẫn CV của TopCV, không lách chống bot. Không chạy crawler thật nếu người dùng chưa yêu cầu rõ; khi thử thì dùng fixtures hoặc HTML mẫu tự soạn.
- **PII:** không lưu tên, email, SĐT người đăng tin hay người review; lọc ngay trong parser.
- **Không commit:** HTML thô, dữ liệu crawl, file export nhãn, file model, cache Hugging Face. Những thứ này nằm ở `s3://joblens/…`.
- **Train xong:** cập nhật `models.yaml` (version, đường dẫn S3, metric, snapshot dữ liệu train). Image gắn tag `version-gitsha`, không dùng `latest`.
- **Ghi nguồn số liệu:** mỗi thí nghiệm ghi snapshot hay tag Iceberg đã dùng và báo cáo cả baseline. Nhãn yếu (tag nhà tuyển dụng, cột kỹ năng LLM của VietJobs) không được dùng làm tập test.
- Repo này ghi topic `jobs.raw.*`, `reviews.raw.*`, `dlq.parse_errors.v1` và bảng `silver.job_skills`, `silver.job_dedup`, `silver.review_aspects`, `silver.reco_scores` (qua image do Airflow của repo Big Data chạy). Không ghi bảng khác.
- Mỗi mô hình giao dưới dạng image theo hợp đồng chạy trong ADR 0001 D3 (`--input-table … --output-table … --run-id …`), kèm image stub. Dịch vụ tìm kiếm (nếu làm WM4) theo `schemas/api/search.v1.yaml`.
- Không chuẩn hóa lương/địa điểm/cấp bậc cho silver (việc của Big Data – D2); `job_uid` luôn tính bằng `joblens_contracts.job_uid()`.
- Phải chạy được một mình: train và đánh giá trên VietJobs + fixtures, không cần Kafka hay K8s.

**Lệnh kiểm tra:** `pre-commit run --all-files`. Khi đã có code thì thêm `pytest -q`.
