> [← Mục lục](README.md)

# Quy tắc làm việc chung giữa các repo

[Quy tắc phân tách giữa các môn](07-quy-tac-phan-tach-mon.md) giúp ba **báo cáo** không trùng nhau. Tài liệu này là bộ quy tắc **kỹ thuật** để bốn **repo** ghép lại vẫn chạy được. Rủi ro lớn nhất khi chia nhiều repo là mỗi người sửa phần của mình, đến lúc ghép thì không khớp.

## 1. Sửa hợp đồng trước, sửa code sau

- Mọi thay đổi schema message Kafka hoặc schema bảng đều mở PR ở `joblens` **trước**, báo trước cho nhóm theo ngoại lệ ở quy tắc 3, sau đó mới sửa code ở repo khác.
- Đánh version theo SemVer: thêm trường không bắt buộc → tăng *minor*; đổi tên hoặc xóa trường → tăng *major*.
- Khi đổi *major*, tạo topic/bảng mới (ví dụ `jobs.raw.topcv.v2`) và giữ bản cũ chạy song song cho đến khi mọi repo đã chuyển xong.
- CI của `joblens` kiểm tra `fixtures` luôn khớp schema.

## 2. Mỗi bảng chỉ một repo được ghi

| Bảng / vùng | Repo được ghi | Repo chỉ đọc |
|---|---|---|
| Topic `jobs.raw.*`, `reviews.raw.*`, `dlq.parse_errors.v1` | mining (crawler) | platform |
| `events.user.v1` | platform (event-generator) | mining |
| `bronze.*`, `silver.job_postings*` | platform | mining, app |
| `silver.job_skills`, `silver.job_dedup`, `silver.review_aspects`, `silver.reco_scores` | mining (image mô hình, do Airflow của platform chạy) | platform, app |
| Topic `app.alert_subscriptions.v1` | app | platform |
| Topic `alerts.job_match.v1` | platform (job streaming) | app |
| Gold (dbt) | platform | app, mining |

Danh sách đầy đủ kèm schema/contract: `schemas/README.md` trong repo `joblens`. Cần dữ liệu thì đọc hoặc mở issue nhờ repo chủ, không tự ghi bảng của repo khác. Quy tắc này khớp với nguyên tắc mỗi phần có đúng một môn chấm chính.

## 3. Tự review, `main` luôn chạy được

- **Mặc định là tự review.** Mọi thay đổi vẫn vào `main` qua PR (để có lịch sử và để CI chạy), nhưng người mở PR tự đọc lại toàn bộ diff theo [checklist](#checklist-mở-pr) rồi tự merge khi CI pass – không chờ người khác duyệt.
- **Ngoại lệ – thay đổi có thể làm hỏng repo khác** (sửa `joblens`, đổi tên cột/bảng, đổi topic): không cần review đầy đủ, chỉ cần **báo trước** trong nhóm chat kèm link PR. Sau **24 giờ** không ai phản đối thì tự merge. Riêng thay đổi phá vỡ tương thích (tăng *major*) thì chờ người phụ trách repo bị ảnh hưởng trả lời "ok" – một dòng là đủ.
- **Để máy kiểm tra thay người:** CI chạy lint + test + kiểm tra `fixtures` khớp schema; pre-commit chạy `ruff` và gitleaks trước mỗi commit. Buổi ghép hệ thống hằng tuần (quy tắc 5) là lần kiểm tra chéo duy nhất, tập trung vào chỗ nối giữa các repo.
- Nhánh ngắn hạn `feat/…`, `fix/…`, `docs/…`; merge kiểu squash.
- Commit theo Conventional Commits, ví dụ `feat(crawler): thêm adapter ITviec`, `fix(dbt): sửa đơn vị lương USD`.
- Gói Free không ép được quy tắc này trên repo private → đây là quy ước cả nhóm tự giữ.

## 4. Không dùng `latest`, luôn ghi rõ phiên bản

- Mỗi repo gắn tag SemVer khi phát hành; image Docker gắn tag `version-gitsha`, ví dụ `skill-extractor:1.2.0-a1b2c3d`.
- `Big-Data-Storage-and-Processing-joblens/deploy/compat.md` là bảng phiên bản của mỗi lần chạy:

  | Ngày | platform | mining (images) | app | contracts | Ghi chú |
  |---|---|---|---|---|---|
  | 2026-10-18 | v0.3.0 | skill-extractor 0.2.0 | v0.1.0 | v1.1.0 | ghép lần 2 |

- Mọi buổi demo và mọi lần chốt số liệu đều phải dựng lại được từ một dòng của bảng này.

## 5. Ghép hệ thống mỗi tuần

- Mỗi tuần một buổi chạy thử toàn luồng: crawler → Kafka → bronze → silver → gold → app.
- `Big-Data-Storage-and-Processing-joblens` có một script kiểm tra nhanh (smoke test) cho việc này.
- Lỗi ở chỗ nối giữa các repo được ưu tiên sửa **trước** việc mới.

## 6. Một bảng công việc chung cho cả org

- GitHub Projects cấp org, gom issue của cả 4 repo.
- Issue liên quan repo khác dẫn link dạng `BD-WM-SA-D/Big-Data-Storage-and-Processing-joblens#12`, gắn nhãn `cross-repo`; đang chờ repo khác thì gắn `blocked`.
- Mỗi issue có đúng một người phụ trách; issue lớn tách nhỏ đến mức làm xong trong ≤ 3 ngày.

## 7. Cấu hình thống nhất, không commit bí mật

- Biến môi trường dùng chung một bộ tên:

  | Biến | Ý nghĩa |
  |---|---|
  | `JOBLENS_KAFKA_BOOTSTRAP` | địa chỉ Kafka |
  | `JOBLENS_S3_ENDPOINT`, `JOBLENS_S3_BUCKET` | object storage |
  | `JOBLENS_CATALOG_URI` | Iceberg REST catalog |
  | `JOBLENS_TRINO_URL` | Trino |
  | `JOBLENS_S3_REGION`, `JOBLENS_S3_ACCESS_KEY_ID`, `JOBLENS_S3_SECRET_ACCESS_KEY` | vùng và khóa S3 (khóa để trống trong `.env.example`) |
  | `JOBLENS_CATALOG_WAREHOUSE` | tên warehouse trong Lakekeeper |
  | `JOBLENS_TRINO_USER`, `JOBLENS_TRINO_PASSWORD` | người dùng Trino |
  | `JOBLENS_SEARCH_URL` | dịch vụ tìm kiếm; trống thì app lùi về Trino |
  | `JOBLENS_ENV` | `local` / `k8s` |

- Repo nào cũng có `.env.example`; mật khẩu/key để trong Kubernetes Secret hoặc `.env` đã gitignore (chi tiết ở quy tắc 8).

## 8. Những gì không được đưa lên GitHub

Áp dụng cho **cả 4 repo, kể cả khi repo để private** (repo private vẫn có thể bị chuyển public, bị clone, hoặc mời thêm người).

| Nhóm | Ví dụ | Vì sao | Để ở đâu thay thế |
|---|---|---|---|
| Bí mật | `.env`, `*.pem`, `*.key`, kubeconfig, file JSON service account, token GitHub/HF, `values-secret*.yaml` | Lộ là mất quyền kiểm soát hạ tầng; xóa khỏi lịch sử git cũng không cứu được | `.env` (gitignore), Kubernetes Secret; chỉ commit `.env.example` |
| Dữ liệu crawl | HTML thô, JSON/Parquet crawl về, dump Kafka, thư mục warehouse Iceberg, checkpoint Spark | Điều khoản của trang nguồn; có thể chứa dữ liệu cá nhân; nặng | `s3://joblens/{bronze,silver,gold}/…` |
| Dữ liệu cá nhân | Tên, email, SĐT người đăng tin/người review, CV | Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 | **Không lưu ở đâu cả** – loại bỏ từ tầng silver |
| Tập nhãn làm từ dữ liệu crawl | File export từ công cụ gán nhãn | Chứa nguyên văn nội dung crawl | `s3://joblens/labels/…`; git chỉ giữ guideline và thống kê |
| Model & file lớn | `*.pt`, `*.bin`, `*.safetensors`, `*.onnx`, `*.pkl`, cache Hugging Face, `mlruns/` | Vài trăm MB – vài GB, làm phình repo vĩnh viễn | `s3://joblens/models/…` hoặc Docker image |
| Output notebook | Kết quả cell in ra bảng dữ liệu | Rò dữ liệu crawl vào git | Xóa output trước khi commit (`nbstripout`) |
| Tài liệu có bản quyền | Slide bài giảng, sách, tài liệu của giảng viên | Không phải của nhóm; repo có thể thành public | Chỉ trích dẫn tên bài giảng trong báo cáo |
| Rác môi trường | `.venv/`, `__pycache__/`, `node_modules/`, `target/` (dbt), `logs/`, `.idea/`, `Thumbs.db` | Không cần, gây xung đột | Sinh lại từ lệnh cài đặt |

**Ngoại lệ được commit:** `joblens/fixtures/` (dữ liệu mẫu nhỏ, có giấy phép rõ ràng như VietJobs, dưới ~5 MB), `.env.example`, file cấu hình mẫu không chứa bí mật.

**Chặn tự động** (bắt buộc cài ở cả 4 repo):

- [`.gitignore` mẫu](templates/gitignore.template) – bỏ qua sẵn các nhóm file trên.
- [`.pre-commit-config.yaml` mẫu](templates/pre-commit-config.yaml) – chặn file > 1 MB, private key, token (gitleaks), file `.env`, file dữ liệu/model ngoài `fixtures/`, và tự xóa output notebook. Mỗi người chạy `pre-commit install` ngay sau khi clone.
- Thí nghiệm nào cũng ghi Iceberg snapshot và version model đã dùng, để không cần commit dữ liệu mà vẫn tái lập được.

**Nếu lỡ đẩy lên GitHub:**

1. **Bí mật:** thu hồi/đổi ngay key hoặc mật khẩu đó (coi như đã lộ) – bước này quan trọng hơn việc xóa file.
2. **Dữ liệu/model:** xóa khỏi toàn bộ lịch sử bằng `git filter-repo --path <file> --invert-paths`, force-push, rồi báo cả nhóm clone lại.
3. Báo trong nhóm chat để kiểm tra các bản fork/clone khác.

## 9. Công cụ giống nhau ở cả 4 repo

- Python chung một phiên bản (ví dụ 3.12), quản lý bằng `uv` hoặc `pip-tools`.
- `ruff` (lint + format), `pytest`, `pre-commit` với cùng cấu hình.
- File cấu hình chung có bản gốc ở `joblens/docs/project-plan/templates/`, đồng bộ sang 4 repo bằng `scripts/sync_templates.py` (không chép tay, không sửa tại chỗ).

## 10. Ghi lại quyết định, giữ nhịp trao đổi

- Quyết định kỹ thuật ghi thành ADR ở repo chủ (ví dụ `Big-Data-Storage-and-Processing-joblens/docs/adr/0003-lakekeeper-catalog.md`), liệt kê trong `joblens/adr-index.md`.
- Glossary chỉ có một bản duy nhất ở `joblens`.
- Với thay đổi thuộc ngoại lệ ở quy tắc 3: ai phản đối thì lên tiếng trong **24 giờ**; im lặng được coi là đồng ý.
- Họp 30 phút mỗi tuần, ngay sau buổi ghép hệ thống: việc xong, việc bị chặn, thay đổi hợp đồng sắp tới.
- Nếu dùng AI để sinh code hoặc tài liệu, ghi chú trong mô tả PR (công cụ, phần nào, ai đã kiểm tra) – vừa minh bạch, vừa là tư liệu cho phần Human-AI collaboration của môn Phân tích thiết kế hệ thống.

## Chú ý: thứ thay đổi nhưng không đưa lên GitHub

> [!IMPORTANT]
> - **File cấu hình riêng từng máy** (cổng, RAM, đường dẫn, mật khẩu): chỉ commit bản `*.example`, bản thật để trong file `*.local.*` / `.env` đã gitignore. Không dùng `git update-index --assume-unchanged` để giấu thay đổi.
> - **Thứ gì sửa trên cluster hoặc giao diện web** (topic Kafka, Airflow Connections, dashboard Grafana, `kubectl edit`): nhớ đưa ngược vào manifest/values/file export trước buổi ghép hệ thống hằng tuần.
> - **Dữ liệu, model, tập nhãn, bí mật**: không nằm trong git, nhưng git phải ghi lại *phiên bản* và *chỗ lưu* của chúng.
> - **Kiểm tra định kỳ**: xóa cluster, clone repo sang máy khác, dựng lại chỉ từ git + object storage + trình quản lý mật khẩu.

Hai bảng dưới đây là danh sách tra cứu cho từng trường hợp.

### Cấu hình riêng từng máy: commit bản mẫu, gitignore bản thật

| Thứ hay bị sửa riêng | Commit lên git | Giữ ở máy (gitignore) |
|---|---|---|
| Biến môi trường, mật khẩu | `.env.example` | `.env` |
| Helm values (RAM, số replica, cổng, đường dẫn) | `values.yaml`, `values-local.example.yaml` | `values-local.yaml` |
| Cấu hình k3d (cổng, thư mục mount trên máy) | `k3d-cluster.example.yaml` | `k3d-cluster.local.yaml` |
| dbt `profiles.yml` | bản dùng `env_var()`, không chứa mật khẩu | `~/.dbt/` nếu ai muốn profile riêng |
| Spark: bộ nhớ, số core khi chạy local | giá trị mặc định trong code/Helm | biến `JOBLENS_*` trong `.env` |
| Docker Compose chạy thử | `docker-compose.yml` | `docker-compose.override.yml` |
| Cài đặt editor | `.vscode/extensions.json`, `.vscode/settings.json` (chỉ phần chung) | phần còn lại của `.vscode/`, `.idea/` |

Không dùng `git update-index --assume-unchanged` hay `--skip-worktree` để giấu thay đổi cục bộ: các lệnh này vô hình với người khác và dễ làm mất thay đổi khi pull. Luôn tách thành file `*.local.*` hoặc `*-local.*` đã gitignore.

### Trạng thái nằm ngoài git: ghi lại ở đâu

| Thứ thay đổi | Nằm ở | Trong git chỉ lưu | Ai cập nhật |
|---|---|---|---|
| Dữ liệu, snapshot Iceberg | object storage + catalog | tag Iceberg trong `deploy/compat.md` và release note | người chốt số liệu |
| Model đã train | `s3://joblens/models/` | `mining/models.yaml`: tên, version, đường dẫn S3, metric, snapshot dữ liệu train | người train |
| Tập nhãn | công cụ gán nhãn → `s3://joblens/labels/` | guideline, thống kê, version bản export | người gán nhãn |
| Bí mật | trình quản lý mật khẩu chung của nhóm (ví dụ Bitwarden Organizations bản miễn phí) | **tên** các biến trong `.env.example`, không có giá trị | owner org |
| Topic Kafka | cluster | khai báo bằng `KafkaTopic` (Strimzi CRD) trong `deploy/` – không tạo bằng lệnh CLI | platform |
| Airflow Variables/Connections | Airflow | khai báo qua biến môi trường/Secret trong Helm values – không nhập tay trên giao diện | platform |
| Dashboard Grafana | Grafana | export JSON vào `deploy/monitoring/dashboards/` | người tạo dashboard |
| Mọi thứ sửa bằng `kubectl edit`/`kubectl apply` tay | cluster | **phải** đưa ngược vào manifest/Helm values trước buổi ghép tuần | người sửa |
| Kết quả GX Data Docs, log dbt, báo cáo benchmark sinh tự động | máy/cluster | chỉ bảng số liệu cuối cùng trong `benchmarks/` hoặc `docs/` | người chạy |
| Báo cáo soạn trên Overleaf/Word, sơ đồ trên draw.io web | dịch vụ ngoài | bản xuất (`.tex`, `.drawio`, `.png`/`.pdf` nhỏ) đồng bộ vào `docs/` ở mỗi mốc | chủ báo cáo |

Cách kiểm tra: **xóa cluster và clone lại repo trên một máy khác** – mọi thứ phải dựng lại được chỉ từ git + object storage + trình quản lý mật khẩu. Thứ gì không dựng lại được thì bổ sung vào một trong hai bảng trên. Nên làm thử một lần vào cuối giai đoạn P1.

### Ngược lại: những thứ phải push

File khóa phiên bản (`uv.lock`/`requirements*.txt`, `package-lock.json`), schema và fixtures, model dbt và test, DAG Airflow, Helm chart/manifest, nguồn UML (`.puml`, `.drawio`), ADR, `compat.md`, `models.yaml`. Thiếu một trong số này là người khác không dựng lại được hệ thống.

## Checklist mở PR

Dùng để tự review trước khi merge.

- [ ] Đã tự đọc lại toàn bộ diff trên GitHub (không chỉ trong editor).
- [ ] Không lẫn cấu hình riêng của máy mình (cổng, đường dẫn, RAM…) – những thứ đó để trong file `*.local.*`.
- [ ] Nếu đã sửa gì trực tiếp trên cluster/giao diện web: đã đưa ngược vào manifest, values hoặc file export.
- [ ] PR nhỏ, một mục đích; tiêu đề theo Conventional Commits.
- [ ] Nếu đụng schema: đã có PR ở `joblens` và đã tăng version.
- [ ] Test/lint pass; không có dữ liệu hay bí mật trong diff.
- [ ] Đã cập nhật tài liệu/ADR nếu thay đổi hành vi hoặc kiến trúc.
- [ ] Đã ghi chú nếu có dùng AI.
- [ ] Nếu ảnh hưởng repo khác: gắn nhãn `cross-repo`, đã báo nhóm và đã qua 24 giờ không ai phản đối (major thì đã có người phụ trách xác nhận).
