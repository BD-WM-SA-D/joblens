# Phiên bản công nghệ (pin)

> Trạng thái: **ĐỀ XUẤT** theo `docs/project-plan/03-nen-tang-big-data.md` (tình trạng cuối 09/2026). Nhóm chốt bản vá cụ thể (`x.y.z`) khi dựng môi trường lần đầu, rồi chỉ nâng cấp có chủ đích qua PR vào repo này.

| Thành phần | Phiên bản | Ghi chú |
|---|---|---|
| Apache Spark | 4.1.x | Chưa dùng 4.2 (ra 07/2026) vì connector chưa theo kịp |
| Apache Iceberg | 1.11.x | JDK 17; build mặc định cho Spark 4.1 |
| Apache Kafka qua Strimzi | Strimzi 1.2 (Kafka 4.2–4.3, KRaft) | Không ZooKeeper |
| dbt Core + dbt-trino | 1.x | Chưa dùng dbt v2 (Fusion) vì chưa rõ adapter Trino |
| Great Expectations (GX Core) | 1.23.x | Hỗ trợ Spark 4 từ 1.19 |
| Apache Airflow | 3.3.x | Helm chart chính thức |
| Trino | 483 | Iceberg connector |
| Lakekeeper (Iceberg REST catalog) | 0.12+ | Phương án thay thế: Apache Polaris 1.4, Nessie |
| SeaweedFS (S3) | bản ổn định mới nhất – `<chốt khi dựng>` | Thay MinIO Community (đã vào chế độ bảo trì) |
| PostgreSQL | 16 hoặc 17 – `<chốt khi dựng>` | Metadata cho Airflow, Lakekeeper |
| Python | 3.12 | Dùng chung cho cả 4 repo (docs/project-plan/09, quy tắc 9) |
| JDK | 17 | Theo Iceberg 1.11 |

## Lịch sử thay đổi

| Ngày | Thay đổi | PR |
|---|---|---|
| 2026-10-02 | Khởi tạo theo đề xuất trong tài liệu kế hoạch | – |
