## Phạm vi repo này: `PTTKHT-joblens` (IT3120 Phân tích thiết kế hệ thống)

Câu hỏi môn chấm: hệ thống phục vụ *ai*, cần *đáp ứng gì*, được *thiết kế* thế nào.

**Thuộc về đây:**
- `api/`, `web/`: cổng JobLens.
- `uml/`: **toàn bộ** sơ đồ UML, gồm use case, lớp ECB, trình tự, máy trạng thái, gói, deployment. Định dạng `.puml` hoặc `.drawio`.
- `requirements/`: persona, danh sách UC, user story, đặc tả UC, NFR – theo phạm vi ở `joblens/docs/project-plan/14-blueprint-he-thong.md`.
- `tests/acceptance/`: kịch bản Given/When/Then.
- `scripts/make_sample_gold.py`: sinh gold mẫu (DuckDB/Parquet) từ fixtures. Chỉ commit script, không commit file sinh ra.
- `docs/` (nguồn báo cáo 7 chương), `docs/adr/`, `docs/ai-log.md`.

**Không thuộc về đây:**
- Code xử lý dữ liệu, Helm, dbt, DAG, benchmark → `Big-Data-Storage-and-Processing-joblens`.
- Crawler, mô hình khai phá → `Web-mining-joblens`.
- Schema bảng gold → `joblens`.

**Quy tắc riêng:**
- **Chỉ đọc lakehouse** (các bảng silver/gold có `PTTKHT-joblens` trong `readers` của contract) qua Trino, hoặc gold mẫu khi chạy local.
- Gọi dịch vụ ngoài theo hợp đồng, luôn có đường lùi: tìm kiếm `schemas/api/search.v1.yaml` (không có `JOBLENS_SEARCH_URL` thì tìm bằng Trino); khai phá `schemas/api/mining.v1.yaml` (không có `JOBLENS_MINING_URL` thì trích bằng từ điển `gold.dim_skill.aliases`, gợi ý bằng đếm kỹ năng trùng – ADR 0002). Không đưa mô hình ML vào app.
- Topic duy nhất app được ghi là `app.alert_subscriptions.v1`. App đọc `alerts.job_match.v1` để gửi cảnh báo UC006 (ADR 0001 D4b). Không ghi bảng lakehouse nào.
- **CSDL ứng dụng** (PostgreSQL, schema `app`: tài khoản, hồ sơ kỹ năng, đăng ký cảnh báo, thông báo) do repo này sở hữu và ghi. **Không lưu văn bản CV**, chỉ lưu kỹ năng người dùng đã xác nhận (ADR-app 0002).
- **Số đo hiệu năng của Big Data** chỉ được *trích* làm bằng chứng NFR, kèm tag `report-bd-v1`, không phân tích lại (R4).
- **Sơ đồ** vẽ theo ký pháp UML của môn này. Không dán sơ đồ Helm hay sơ đồ luồng dữ liệu của Big Data (R5).
- **Human-AI collaboration là một phần được chấm.** Mỗi lần AI hỗ trợ phân tích hay thiết kế (nháp user story, rà NFR, gợi ý sơ đồ…) phải ghi **thêm** vào `docs/ai-log.md`: ngày, công cụ, việc AI làm, phần người chỉnh, người kiểm tra (để `<người kiểm tra>` nếu chưa có).
- Phải chạy được một mình với gold mẫu sinh từ fixtures, không cần Trino.

**Lệnh kiểm tra:** `pre-commit run --all-files`. Khi đã có code thì thêm `pytest -q` và chạy các kịch bản trong `tests/acceptance/`.
