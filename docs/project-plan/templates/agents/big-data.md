## Phạm vi repo này: `Big-Data-Storage-and-Processing-joblens` (IT4931 Big Data)

Câu hỏi môn chấm: dữ liệu được *di chuyển, lưu trữ, xử lý* ở quy mô lớn thế nào, và vì sao chọn như vậy.

**Thuộc về đây:**
- `deploy/`: Helm values, manifest K8s, cấu hình k3d (chỉ bản `*.example`), khai báo topic bằng `KafkaTopic` (Strimzi CRD), dashboard Grafana export JSON, `compat.md`.
- `spark-jobs/`: streaming bronze, backfill VietJobs, silver jobs, compaction.
- `dbt/`, `gx/`, `airflow/dags/`, `event-generator/`, `benchmarks/`.
- `docs/` (nguồn báo cáo Big Data) và `docs/adr/`.

**Không thuộc về đây:**
- Spider, parser, thuật toán dedup, mô hình IE/ABSA/IR/RecSys, Dockerfile mô hình → `Web-mining-joblens`. Ở đây chỉ **gọi** image hoặc thư viện của họ theo tag cố định.
- UML, đặc tả UC, API/UI → `PTTKHT-joblens`.
- Schema message hay contract bảng → `joblens`. Thiết kế topic thuộc môn này, nhưng file schema nằm ở repo chung.

**Quy tắc riêng:**
- Topic Kafka chỉ tạo bằng `KafkaTopic` CRD trong `deploy/`, không tạo bằng lệnh CLI.
- Airflow Variables/Connections khai báo qua Helm values hoặc Secret, không nhập tay trên giao diện.
- Thứ gì sửa trực tiếp trên cluster (`kubectl edit`, giao diện web) phải được đưa ngược vào manifest.
- Mỗi lần chạy demo hay chốt số liệu thì thêm một dòng vào `deploy/compat.md`.
- `benchmarks/` chỉ giữ bảng số liệu cuối, không giữ log hay output sinh tự động. Không bịa số đo.
- Repo này ghi các topic `events.user.*`, bảng `bronze.*`, `silver.job_postings*` và gold. Không ghi `silver.job_skills` hay `silver.review_aspects` (những bảng đó do job của repo mining ghi).
- Phải chạy được một mình: nạp raw mẫu từ fixtures của `joblens` thay cho crawler, image mô hình có thể thay bằng stub.

**Lệnh kiểm tra:** `pre-commit run --all-files`. Khi đã có code thì thêm `pytest -q`, `dbt build` (với profile local) và smoke test trong `scripts/`.
