# joblens (joblens-contracts)

Hợp đồng dữ liệu dùng chung của dự án JobLens VN: JSON Schema cho topic Kafka, data contract cho bảng bronze/silver/gold, fixtures, glossary, bảng phiên bản và bộ tài liệu kế hoạch dự án.

> **Phạm vi đánh giá – repo dùng chung, không phải repo nộp của môn nào**
>
> Dự án JobLens dùng chung một hệ thống cho ba môn học kỳ 20261: IT4931 Big Data Storage and Processing, Web Mining (<mã môn>) và IT3120 Phân tích thiết kế hệ thống (đã được giảng viên đồng ý ngày <dd/mm/yyyy>). Repo này chỉ chứa hợp đồng dữ liệu và tài liệu chung, mọi repo môn đều tham chiếu tới nó. Nội dung ở đây **không** được đề nghị chấm như đóng góp chính của môn nào. Thiết kế topic và schema message thuộc môn Big Data theo ma trận sở hữu, file schema chỉ được đặt ở đây để các repo cùng dùng.

> Tên repo trên GitHub là `joblens`, giữ vai trò `joblens-contracts` trong tài liệu kế hoạch. Bảng đối chiếu tên nằm ở mục [Repo trong org](#repo-trong-org).

## Thành viên phụ trách

| Thành viên | MSSV | Vai trò trong repo này |
|---|---|---|
| <Họ tên> | <MSSV> | <…> |

Theo docs/project-plan/08, mọi thành viên đều có quyền Write trên repo này và mọi thay đổi vẫn phải đi qua PR.

## Chạy nhanh

```bash
# Cài vào repo khác theo tag cố định
pip install git+https://github.com/BD-WM-SA-D/joblens@v<x.y.z>

# Phát triển trong repo này
pip install -e ".[dev]"
python scripts/validate_fixtures.py   # fixtures khớp schema
pytest -q
```

```python
from joblens_contracts import load_schema, load_table_contract, fixture_path, job_uid
schema = load_schema("job_posting.v1")
contract = load_table_contract("silver.job_skills")
uid = job_uid("topcv", "123456")
```

## Cấu trúc thư mục

```
schemas/README.md       bảng tra: topic/bảng/API nào, repo nào ghi, repo nào đọc
schemas/kafka/          JSON Schema cho 6 topic (job_posting, review, user_event, parse_error, alert_subscription, job_match)
schemas/tables/         contract YAML cho bảng bronze/ silver/ gold/ (định dạng: _contract.schema.json)
schemas/api/            hợp đồng API (search.v1.yaml – OpenAPI 3.1)
fixtures/               dữ liệu mẫu rất nhỏ, có ghi nguồn và giấy phép
joblens_contracts/      package Python nhỏ trả đường dẫn tới schema/fixtures
scripts/                validate_fixtures.py (CI), sync_templates.py (đồng bộ file cấu hình chung sang 4 repo)
tests/                  pytest
docs/adr/               ADR chung giữa các repo (0001: ranh giới xử lý)
docs/project-plan/      bộ tài liệu kế hoạch dự án (01–13) và bản gốc file cấu hình chung (templates/)
explore/                script khám phá dữ liệu (VietJobs EDA)
AGENTS.md, CLAUDE.md    quy tắc cho AI agent (Codex, Claude Code, Cursor)
NHAT-KY.md              nhật ký thay đổi
glossary.md             thuật ngữ chung (bản duy nhất)
versions.md             pin phiên bản Spark/Iceberg/Kafka/Trino/…
adr-index.md            danh mục ADR của cả 3 repo
```

## Đổi schema

Hợp đồng sửa ở đây **trước**, code ở repo khác sửa sau (docs/project-plan/09, quy tắc 1):

- Giai đoạn `draft` (tới buổi ghép đầu tiên): sửa thoải mái, chỉ cần nhắn nhóm chat một câu và ghi một dòng `NHAT-KY.md`.
- Sau khi `stable`:
  - Thêm trường không bắt buộc: tăng *minor* và báo nhóm.
  - Đổi tên hoặc xóa: hỏi người đang dùng, họ "ok" thì đổi. Tăng *major* và tạo `.vN` mới nếu cần chạy song song.
- Nên qua PR để CI chạy, không cần chờ duyệt. Mỗi lần phát hành gắn git tag SemVer.

## Tài liệu

- Mục lục kế hoạch dự án: [`docs/project-plan/README.md`](docs/project-plan/README.md)
- **File nào lên repo nào, quy trình khi tạo/sửa file:** [`docs/repo-routing.md`](docs/repo-routing.md)
- Thuật ngữ: [`glossary.md`](glossary.md) · Phiên bản: [`versions.md`](versions.md) · ADR: [`adr-index.md`](adr-index.md)

## Repo trong org

Tên trong tài liệu kế hoạch được đối chiếu với tên thật trên GitHub như sau:

| Vai trò (docs/project-plan/08) | Repo trên GitHub | Môn |
|---|---|---|
| `joblens-contracts` | [`BD-WM-SA-D/joblens`](https://github.com/BD-WM-SA-D/joblens) | Dùng chung |
| `joblens-platform` | [`BD-WM-SA-D/Big-Data-Storage-and-Processing-joblens`](https://github.com/BD-WM-SA-D/Big-Data-Storage-and-Processing-joblens) | IT4931 Big Data |
| `joblens-mining` | [`BD-WM-SA-D/Web-mining-joblens`](https://github.com/BD-WM-SA-D/Web-mining-joblens) | Web Mining |
| `joblens-app` | [`BD-WM-SA-D/PTTKHT-joblens`](https://github.com/BD-WM-SA-D/PTTKHT-joblens) | IT3120 SA&D |

## Dữ liệu và giấy phép

Repo không chứa dữ liệu crawl. Fixture hiện tại do nhóm tự soạn (synthetic), chi tiết xem [`fixtures/README.md`](fixtures/README.md). Nếu sau này thêm mẫu từ VietJobs (Pham Dinh et al., LREC 2026) thì phải trích dẫn theo giấy phép của dataset.
