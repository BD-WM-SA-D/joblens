## Phạm vi repo này: `joblens` (dùng chung)

Repo này không phải bài nộp của môn nào. Mọi repo môn đều phụ thuộc vào nó, nên **mọi thay đổi ở đây đều là thay đổi `cross-repo`**: phải báo nhóm và chờ 24 giờ; bản *major* phải chờ người phụ trách repo bị ảnh hưởng xác nhận.

**Thuộc về đây:**
- `schemas/kafka/*.json` (JSON Schema draft 2020-12), `schemas/tables/{bronze,silver,gold}/*.yaml` (theo `_contract.schema.json`), `schemas/api/*.yaml` (OpenAPI); bảng ai ghi/ai đọc ở `schemas/README.md` phải cập nhật cùng lúc.
- `docs/adr/` (ADR chung giữa các repo).
- `fixtures/*.sample.json`: chỉ dữ liệu tự soạn hoặc có giấy phép rõ ràng, tổng < 5 MB, không có PII. Mỗi fixture được ghi vào bảng trong `fixtures/README.md`.
- `glossary.md` (bản duy nhất), `versions.md`, `adr-index.md`.
- `docs/project-plan/**` (kế hoạch, bản gốc các file cấu hình chung trong `templates/`), `docs/repo-routing.md`.
- `explore/` (EDA chung trước khi làm), package `joblens_contracts/`, `scripts/validate_fixtures.py`.

**Không thuộc về đây:**
- Code xử lý dữ liệu, Helm, dbt, DAG → `Big-Data-Storage-and-Processing-joblens`.
- Crawler, mô hình, notebook thí nghiệm → `Web-mining-joblens`.
- UML, API/UI, đặc tả UC → `PTTKHT-joblens`.

**Khi sửa bản gốc trong `templates/`:** chạy lại bước đồng bộ sang cả 4 repo. Ghi vào `NHAT-KY.md` của repo này và nhắc người dùng ghi nhật ký ở từng repo được đồng bộ.

**Lệnh kiểm tra:**

```bash
pip install -e ".[dev]"
python scripts/validate_fixtures.py
pytest -q
python scripts/sync_templates.py .. --check
ruff check .
pre-commit run --all-files
```
