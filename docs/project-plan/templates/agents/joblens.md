## Phạm vi repo này: `joblens` (dùng chung)

Repo này không phải bài nộp của môn nào. Mọi repo môn đều phụ thuộc vào nó, nên mọi thay đổi ở đây phải **nhắn nhóm chat** và ghi một dòng `NHAT-KY.md`. Đổi tên hoặc xóa trường/cột thì hỏi nhóm đang dùng trước. Nên qua PR để CI chạy, không cần chờ duyệt.

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

**Khi sửa bản gốc trong `templates/`:** chạy lại bước đồng bộ sang cả 4 repo và ghi một dòng `NHAT-KY.md` ở repo này.

**Lệnh kiểm tra:**

```bash
pip install -e ".[dev]"
python scripts/validate_fixtures.py
pytest -q
python scripts/sync_templates.py .. --check
ruff check .
pre-commit run --all-files
```
