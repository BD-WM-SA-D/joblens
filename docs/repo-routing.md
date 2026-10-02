# File nào lên repo nào

Bảng tra cụ thể cho từng loại file. Nền tảng: [ma trận sở hữu](project-plan/07-quy-tac-phan-tach-mon.md#ma-trận-sở-hữu) (mỗi artifact một môn chấm chính), [cấu trúc repo](project-plan/08-to-chuc-repo-va-github.md) và [quy tắc 2, 8](project-plan/09-quy-tac-lam-viec-chung.md).

## Ký hiệu

| Ký hiệu | Repo trên GitHub | Môn |
|---|---|---|
| **CHUNG** | `BD-WM-SA-D/joblens` | Dùng chung (contracts) |
| **BD** | `BD-WM-SA-D/Big-Data-Storage-and-Processing-joblens` | IT4931 Big Data |
| **WM** | `BD-WM-SA-D/Web-mining-joblens` | Web Mining |
| **SAD** | `BD-WM-SA-D/PTTKHT-joblens` | IT3120 Phân tích thiết kế hệ thống |
| **KHÔNG** | Không repo nào – để ở `s3://joblens/…`, `.env` hoặc trình quản lý mật khẩu | – |

## Quy trình mỗi khi tạo hoặc sửa file

Áp dụng cho mọi người và mọi AI agent (Codex, Claude, Cursor…).

**Khi tạo file mới:**

1. Tra loại file trong các mục A–F bên dưới để biết file thuộc repo nào. Nếu repo đích không phải repo đang mở thì **không tạo ở đây**: chuyển sang đúng repo, hoặc mở issue ở repo đó và gắn nhãn `cross-repo`.
2. Nếu file thuộc mục **F** thì không commit. Thêm đường dẫn vào `.gitignore` nếu chưa được chặn.
3. Nếu việc cần file ở nhiều repo (mục **E**) thì tách thành nhiều file, mỗi repo giữ đúng phần của mình. Làm phần ở **CHUNG** trước (schema, contract), các repo môn làm sau.
4. Đặt file đúng thư mục theo bảng. Nếu file thuộc mục C hoặc E, hoặc được sinh ra từ hợp đồng, thì thêm dòng đánh dấu ở đầu file (xem bảng "Đánh dấu ngay trong file" bên dưới).
5. Ghi vào nhật ký (xem mục [Nhật ký thay đổi](#nhật-ký-thay-đổi)).

**Khi sửa file có sẵn:**

| File đang sửa | Phải làm |
|---|---|
| Mục **B** hoặc **D** (chỉ thuộc repo này) | Sửa bình thường qua PR |
| Mục **A** (schema, fixtures, glossary…) | PR vào **CHUNG** trước, báo nhóm và chờ 24 giờ; bản *major* chờ người phụ trách repo bị ảnh hưởng xác nhận. Repo môn chỉ cập nhật version sau khi CHUNG đã gắn tag |
| Mục **C** (file cấu hình chung) | **Không sửa trực tiếp ở repo môn.** Sửa bản gốc ở `joblens/docs/project-plan/templates/`, merge, rồi chạy `python scripts/sync_templates.py ..` (trong repo `joblens`, với 4 repo clone cạnh nhau) và mở PR `cross-repo` ở từng repo trong cùng ngày. `--check` chỉ báo file lệch |
| Mục **E** (một việc nhiều repo) | Kiểm tra phần tương ứng ở repo kia có cần đổi theo không; nếu có thì mở issue `cross-repo` và dẫn link chéo |

**Đánh dấu ngay trong file.** Những file có bản gốc ở nơi khác phải ghi một dòng đầu file. Người hay agent mở file ra thấy dòng này là biết không được sửa tại chỗ:

| File | Dòng đánh dấu (comment theo cú pháp của file) |
|---|---|
| Mục C (`.gitignore`, `.pre-commit-config.yaml`, `.env.example`, `.gitattributes`) | `# ĐỒNG BỘ TỪ joblens/docs/project-plan/templates/<tên> – sửa ở đó trước, không sửa tại đây` |
| `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/joblens.mdc` | `<!-- ĐỒNG BỘ TỪ joblens/docs/project-plan/templates/<tên> – sửa ở đó trước, không sửa tại đây -->` |
| Mục E (phần việc của repo này trong một việc nhiều repo) | `# LIÊN QUAN: <repo>/<đường dẫn> – đổi file này thì kiểm tra file kia` |
| File trong repo môn sinh ra từ hợp đồng (ví dụ model Pydantic sinh từ schema) | `# SINH TỪ joblens schemas/kafka/<tên>.json @ v<x.y.z> – không sửa tay` |

Bản gốc của các file mục C ở `joblens/docs/project-plan/templates/`:

| File trong repo | Bản gốc |
|---|---|
| `.gitignore` | `gitignore.template` |
| `.pre-commit-config.yaml` | `pre-commit-config.yaml` |
| `.env.example` | `env.example` |
| `.gitattributes` | `gitattributes.template` |
| `CONTRIBUTING.md` | `CONTRIBUTING.md` (bản chép chỉ khác đường dẫn tới quy tắc 9 và repo-routing) |
| `AGENTS.md` | `AGENTS.md` + `agents/{joblens,big-data,web-mining,pttkht}.md` |
| `CLAUDE.md` | `CLAUDE.md` |
| `.cursor/rules/joblens.mdc` | `cursor-rule.mdc` |

## Nhật ký thay đổi

Mỗi repo có một file **`NHAT-KY.md`** ở thư mục gốc. Nhật ký trả lời được câu hỏi: ai, khi nào, tạo/sửa/xóa file gì, vì sao, có dùng AI không. Nhật ký cũng là bằng chứng đóng góp theo môn (R6, R7) và là tư liệu cho phần Human-AI collaboration của môn SA&D.

**Ghi vào đâu:**

| Thay đổi | Ghi vào |
|---|---|
| Chỉ chạm file mục B/D của một repo | `NHAT-KY.md` của repo đó |
| Chạm file mục A (schema, fixtures, glossary…) | `joblens/NHAT-KY.md`; repo môn cập nhật version sau đó thì ghi thêm vào nhật ký repo môn |
| Đồng bộ file mục C | `joblens/NHAT-KY.md` (bản gốc) **và** nhật ký của từng repo được chép sang |
| Việc nhiều repo (mục E) | Nhật ký của từng repo có file thay đổi, **và** một mục tóm tắt trong `joblens/NHAT-KY.md` kèm link chéo |

**Khi nào ghi:** mỗi PR một mục, ghi trong chính PR đó. Liệt kê:
- Mọi file **tạo mới** hoặc **xóa**.
- Mọi file thuộc mục A, C, E **bị sửa**.

Sửa nhỏ trong file mục B/D chỉ cần một dòng tóm tắt. Mục mới nhất đặt **trên cùng**. Nếu hai PR cùng thêm mục và bị xung đột thì giữ cả hai.

**Mẫu một mục:**

```markdown
## 2026-10-05 · <Họ tên> · PR #<số>

- **Tạo:** `crawler/spiders/topcv.py` (B)
- **Sửa:** `.pre-commit-config.yaml` (C – đồng bộ từ joblens)
- **Xóa:** –
- **Lý do:** <một câu>
- **Ảnh hưởng repo khác:** không | <repo>#<issue/PR>
- **AI:** không | <công cụ> – <phần nào>; <người> đã kiểm tra
```

## Nguyên tắc

1. **Một file có đúng một bản gốc.** Repo khác dùng file đó bằng cách cài theo tag (`pip install git+…/joblens@vX.Y.Z`), dẫn link, ghi tag image Docker, hoặc đọc bảng dữ liệu. **Không chép file sang repo khác.**
2. Ngoại lệ duy nhất là **file cấu hình chung** (mục C). Các file này có ở cả 4 repo, nội dung giống nhau, bản gốc nằm ở `joblens/docs/project-plan/templates/`.
3. Có những thứ cần nhiều repo cùng tham gia, ví dụ producer Kafka hay job mô hình. Khi đó mỗi repo giữ **một file khác nhau** cho phần việc của mình (mục E). Không bao giờ giữ cùng một file ở hai nơi.
4. Không tìm thấy loại file trong bảng thì hỏi: *"Giảng viên môn nào sẽ chấm file này?"*. Môn đó là repo đích. Nếu không môn nào chấm mà nhiều repo cùng cần, file vào **CHUNG**.

## A. Chỉ ở repo CHUNG (`joblens`)

| File / thư mục | Ví dụ |
|---|---|
| JSON Schema message Kafka | `schemas/kafka/job_posting.v1.json`, `review.v1.json`, `user_event.v1.json` |
| Data contract bảng bronze/silver/gold | `schemas/tables/silver/job_postings.yaml`, `schemas/tables/gold/mart_salary_role_region.yaml` |
| Dữ liệu mẫu có giấy phép (< 5 MB) | `fixtures/*.sample.json` |
| Thuật ngữ, phiên bản, danh mục ADR | `glossary.md`, `versions.md`, `adr-index.md` |
| Tài liệu kế hoạch dự án, mẫu cấu hình gốc | `docs/project-plan/**`, `docs/project-plan/templates/**` |
| Script khám phá dữ liệu chung (EDA trước khi làm) | `explore/01_vietjobs_eda.py` |
| Package, script kiểm tra hợp đồng và đồng bộ file mục C | `joblens_contracts/`, `scripts/validate_fixtures.py`, `scripts/sync_templates.py` |
| Tài liệu điều phối chung | `docs/repo-routing.md` (file này) |

## B. Chỉ ở một repo môn

### BD – `Big-Data-Storage-and-Processing-joblens`

| File / thư mục | Ví dụ |
|---|---|
| Hạ tầng K8s, Helm values, cấu hình k3d (bản `*.example`) | `deploy/kafka/kafka-cluster.yaml`, `deploy/trino/values.yaml`, `deploy/k3d-cluster.example.yaml` |
| Khai báo topic Kafka (Strimzi CRD) | `deploy/kafka/topics/jobs-raw-topcv-v1.yaml` |
| Dashboard Grafana (export JSON) | `deploy/monitoring/dashboards/kafka-lag.json` |
| Bảng phiên bản các lần chạy | `deploy/compat.md` |
| Spark job: streaming bronze, backfill VietJobs, silver, compaction | `spark-jobs/bronze_stream.py`, `spark-jobs/backfill_vietjobs.py`, `spark-jobs/compaction.py` |
| dbt models + tests, `profiles.yml` dùng `env_var()` | `dbt/models/gold/mart_skill_demand_monthly.sql` |
| Great Expectations suites | `gx/expectations/silver_job_postings.json` |
| Airflow DAG | `airflow/dags/daily_pipeline.py` |
| Bộ sinh sự kiện synthetic | `event-generator/generator.py` |
| Benchmark và bảng số liệu cuối | `benchmarks/batch_vs_streaming.md`, `benchmarks/trino_p95.csv` |
| ADR nền tảng, nguồn báo cáo BD | `docs/adr/0001-lambda-vs-kappa.md`, `docs/report/` |
| Smoke test ghép hệ thống hằng tuần | `scripts/smoke_test.sh` |

### WM – `Web-mining-joblens`

| File / thư mục | Ví dụ |
|---|---|
| Spider, parser, adapter từng trang, producer ghi vào Kafka | `crawler/spiders/topcv.py`, `crawler/producer.py` |
| Thuật toán dedup và đánh giá (WM1) | `crawler/dedup/minhash.py`, `experiments/wm1_dedup_eval.ipynb` |
| Mô hình IE / ABSA / IR / RecSys / Graph | `ie/`, `absa/`, `retrieval/`, `recsys/`, `graph/` |
| Từ điển alias kỹ năng → ESCO | `ie/resources/skill_alias.csv` (do nhóm tự xây) |
| Guideline gán nhãn, thống kê κ (không có dữ liệu nhãn) | `annotation/guideline_skill.md`, `annotation/kappa.md` |
| Notebook thí nghiệm (đã xóa output), kết quả | `experiments/wm2_phobert.ipynb`, `experiments/results.md` |
| Dockerfile image mô hình | `images/skill-extractor/Dockerfile` |
| Danh mục model đã train | `models.yaml` |
| ADR mô hình, nguồn báo cáo WM | `docs/adr/`, `docs/report/` |

### SAD – `PTTKHT-joblens`

| File / thư mục | Ví dụ |
|---|---|
| Code cổng JobLens | `api/`, `web/` |
| **Toàn bộ** sơ đồ UML (gồm cả deployment diagram) | `uml/usecase.puml`, `uml/deployment.puml`, `uml/*.drawio` |
| User story, đặc tả UC, NFR | `requirements/UC001-tim-kiem.md`, `requirements/nfr.md` |
| Kịch bản kiểm thử chấp nhận | `tests/acceptance/uc001.feature` |
| Script sinh gold mẫu (DuckDB/Parquet) từ fixtures để app chạy độc lập | `scripts/make_sample_gold.py` (chỉ commit script, không commit file Parquet) |
| Nhật ký Human-AI collaboration | `docs/ai-log.md` |
| Nguồn báo cáo 7 chương, ADR ứng dụng | `docs/report/`, `docs/adr/` |

## C. Có ở cả 4 repo, nội dung giống nhau

Bản gốc ở `joblens/docs/project-plan/templates/`. Muốn đổi thì sửa bản gốc trước (PR vào **CHUNG**), sau đó chép sang 3 repo môn trong cùng ngày.

| File | Ghi chú |
|---|---|
| `.gitignore` | từ `templates/gitignore.template` |
| `.pre-commit-config.yaml` | từ `templates/pre-commit-config.yaml` |
| `CONTRIBUTING.md` | từ `templates/CONTRIBUTING.md` (chỉ khác đường dẫn tới quy tắc 9) |
| `.env.example` | cùng bộ biến `JOBLENS_*` |
| `.gitattributes` | `* text=auto eol=lf` |
| `AGENTS.md` | Quy tắc cho AI agent (Codex đọc trực tiếp). Phần chung giống nhau, cuối file có mục "Phạm vi repo này" lấy từ `templates/agents/<repo>.md` |
| `CLAUDE.md` | Claude Code – chỉ nhúng `@AGENTS.md` |
| `.cursor/rules/joblens.mdc` | Cursor – `alwaysApply`, trỏ tới `@AGENTS.md` kèm tóm tắt |

## D. Có ở cả 4 repo, nội dung riêng từng repo

Chỉ trùng tên file. Nội dung mỗi repo tự viết, không chép giữa các repo (R3: không chép nguyên văn giữa các báo cáo).

| File | Riêng ở chỗ |
|---|---|
| `README.md` | Khung "Phạm vi đánh giá", thành viên, cách chạy |
| `NHAT-KY.md` | Nhật ký thay đổi của chính repo đó (mục [Nhật ký thay đổi](#nhật-ký-thay-đổi)) |
| `docs/` (nguồn báo cáo) | Mỗi môn viết lại phần bối cảnh theo góc nhìn của mình, tối đa ~1 trang |
| `docs/adr/` | ADR của repo nào nằm ở repo đó; danh mục chung ghi ở `joblens/adr-index.md` |
| `pyproject.toml`, `uv.lock` / `requirements*.txt` | Thư viện riêng; Python 3.12 chung |
| `.github/workflows/ci.yml` | Bước lint/test riêng |
| `tests/` | Test của code trong repo đó |

## E. Ca dễ nhầm: một việc, nhiều repo, mỗi repo một file

| Việc | CHUNG | BD | WM | SAD |
|---|---|---|---|---|
| Đưa tin tuyển dụng vào Kafka | schema `schemas/kafka/job_posting.v1.json` | khai báo topic `deploy/kafka/topics/…yaml` | code producer `crawler/producer.py` | – |
| Chạy mô hình trích kỹ năng trong pipeline | contract bảng `schemas/tables/silver/job_skills.yaml` | DAG gọi image theo tag `airflow/dags/…py` | code mô hình + `images/skill-extractor/Dockerfile` + `models.yaml` | – |
| Dedup tin trùng | – | Spark job silver chỉ **gọi** thư viện/image dedup theo version | thuật toán + đánh giá P/R/F1 | – |
| Kiến trúc triển khai | – | manifest/Helm thật + sơ đồ zone/luồng dữ liệu trong `docs/` | – | deployment diagram **UML** trong `uml/` (vẽ lại theo ký pháp UML, R5) |
| Số đo hiệu năng (p95, freshness) | – | đo và phân tích `benchmarks/` | – | **chỉ trích** số + dẫn tag `report-bd-v1` trong chương 6 (R4) |
| Dữ liệu tương tác người dùng | schema `user_event.v1.json` | `event-generator/` (repo ghi topic) | đọc để làm RecSys/Query mining | dùng làm kịch bản tải NFR |
| Dữ liệu mẫu cho app chạy độc lập | `fixtures/` | nạp fixtures thay crawler | train/test trên fixtures + VietJobs | `scripts/make_sample_gold.py` sinh gold từ fixtures |
| Thuật ngữ | `glossary.md` (bản duy nhất) | dẫn link | dẫn link | dẫn link |
| Notebook | `explore/` (EDA chung trước khi làm) | – | `experiments/` (thí nghiệm mô hình) | – |

## F. KHÔNG lên repo nào

Theo [quy tắc 8](project-plan/09-quy-tac-lam-viec-chung.md#8-những-gì-không-được-đưa-lên-github). Pre-commit và `.gitignore` đã chặn sẵn phần lớn các trường hợp.

| File | Để ở đâu |
|---|---|
| `.env`, `*.pem`, `*.key`, kubeconfig, token, `values-secret*.yaml` | `.env` cục bộ, Kubernetes Secret, trình quản lý mật khẩu |
| HTML thô, JSON/Parquet crawl, dump Kafka, warehouse Iceberg, checkpoint Spark | `s3://joblens/{bronze,silver,gold}/` |
| File export tập nhãn | `s3://joblens/labels/` |
| `*.pt`, `*.bin`, `*.safetensors`, `*.onnx`, `*.pkl`, cache HF, `mlruns/` | `s3://joblens/models/` hoặc Docker image |
| Bộ VietJobs đầy đủ (`data/vietjobs/`) | tải lại bằng script, không commit |
| Dữ liệu cá nhân (tên, email, SĐT, CV) | không lưu ở đâu cả |
| Slide, sách, tài liệu của giảng viên | không đưa lên – chỉ trích dẫn tên |
| Cấu hình riêng máy (`*.local.yaml`, `values-local.yaml`, `docker-compose.override.yml`) | máy cá nhân |
| File Word/Overleaf đang soạn | dịch vụ ngoài; chỉ đồng bộ bản xuất nhỏ vào `docs/` của repo môn tại mỗi mốc |
