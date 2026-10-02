## Phạm vi repo này: `PTTKHT-joblens` (IT3120 Phân tích thiết kế hệ thống)

Câu hỏi môn chấm: hệ thống phục vụ *ai*, cần *đáp ứng gì*, được *thiết kế* thế nào.

**Thuộc về đây:**
- `api/`, `web/`: cổng JobLens.
- `uml/`: **toàn bộ** sơ đồ UML, gồm use case, lớp ECB, trình tự, máy trạng thái, gói, deployment. Định dạng `.puml` hoặc `.drawio`.
- `requirements/`: user story, đặc tả UC001–UC010, NFR.
- `tests/acceptance/`: kịch bản Given/When/Then.
- `scripts/make_sample_gold.py`: sinh gold mẫu (DuckDB/Parquet) từ fixtures. Chỉ commit script, không commit file sinh ra.
- `docs/` (nguồn báo cáo 7 chương), `docs/adr/`, `docs/ai-log.md`.

**Không thuộc về đây:**
- Code xử lý dữ liệu, Helm, dbt, DAG, benchmark → `Big-Data-Storage-and-Processing-joblens`.
- Crawler, mô hình khai phá → `Web-mining-joblens`.
- Schema bảng gold → `joblens`.

**Quy tắc riêng:**
- **Chỉ đọc gold** qua Trino, hoặc qua gold mẫu khi chạy local. Không ghi bảng hay topic nào.
- **Số đo hiệu năng của Big Data** chỉ được *trích* làm bằng chứng NFR, kèm tag `report-bd-v1`, không phân tích lại (R4).
- **Sơ đồ** vẽ theo ký pháp UML của môn này. Không dán sơ đồ Helm hay sơ đồ luồng dữ liệu của Big Data (R5).
- **Human-AI collaboration là một phần được chấm.** Mỗi lần AI hỗ trợ phân tích hay thiết kế (nháp user story, rà NFR, gợi ý sơ đồ…) phải ghi **thêm** vào `docs/ai-log.md`: ngày, công cụ, việc AI làm, phần người chỉnh, người kiểm tra (để `<người kiểm tra>` nếu chưa có).
- Phải chạy được một mình với gold mẫu sinh từ fixtures, không cần Trino.

**Lệnh kiểm tra:** `pre-commit run --all-files`. Khi đã có code thì thêm `pytest -q` và chạy các kịch bản trong `tests/acceptance/`.
