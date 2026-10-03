> [← Mục lục](README.md)

# Quy tắc làm việc chung giữa các repo

[Quy tắc phân tách giữa các môn](07-quy-tac-phan-tach-mon.md) giúp ba **báo cáo** không trùng nhau. Tài liệu này là bộ quy tắc **kỹ thuật** để bốn **repo** ghép lại vẫn chạy được. Rủi ro lớn nhất khi chia nhiều repo là mỗi người sửa phần của mình, đến lúc ghép thì không khớp.

## 1. Sửa hợp đồng trước, sửa code sau

- Hợp đồng (schema message Kafka, contract bảng, API) chỉ có **một bản** ở repo `joblens`. Cần đổi thì sửa ở đó **trước**, rồi mới sửa code ở repo môn.
- **Giai đoạn `draft`** (tới buổi ghép hệ thống đầu tiên): sửa thoải mái. Chỉ cần nhắn nhóm chat một câu và ghi một dòng vào `joblens/NHAT-KY.md`.
- **Sau khi ổn định (`stable`):**
  - Thêm trường hoặc cột không bắt buộc: cứ làm và báo nhóm (tăng *minor*).
  - Đổi tên hoặc xóa: hỏi người đang dùng trong chat, họ "ok" thì đổi (tăng *major*). Nếu bên kia chưa kịp chuyển thì tạo topic hay bảng `.vN` mới và chạy song song với bản cũ.
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

## 3. Làm song song, ghép khi cần

- **Trong repo môn của mình: làm tự do.**
  - Push thẳng `main` hay dùng nhánh đều được; không bắt buộc PR, không cần ai duyệt.
  - Mỗi repo do nhóm của môn đó tự quản.
- **Ở repo `joblens` và mọi thay đổi chạm repo khác:**
  - Nên qua PR để CI chạy.
  - Không cần chờ duyệt, nhưng phải **nhắn nhóm chat** (quy tắc 1).
- **Commit message** ghi rõ thay đổi gì, nên theo kiểu Conventional Commits: `feat(crawler): thêm adapter ITviec`, `fix(dbt): sửa đơn vị lương USD`.
- **Để máy kiểm tra thay người:** pre-commit chặn bí mật và dữ liệu trước mỗi commit; CI của `joblens` kiểm tra hợp đồng.
- **Không force-push** lên `main` của bất kỳ repo nào.

## 4. Không dùng `latest`, luôn ghi rõ phiên bản

- Mỗi repo gắn tag SemVer khi phát hành; image Docker gắn tag `version-gitsha`, ví dụ `skill-extractor:1.2.0-a1b2c3d`.
- `Big-Data-Storage-and-Processing-joblens/deploy/compat.md` là bảng phiên bản của mỗi lần chạy:

  | Ngày | platform | mining (images) | app | contracts | Ghi chú |
  |---|---|---|---|---|---|
  | 2026-10-18 | v0.3.0 | skill-extractor 0.2.0 | v0.1.0 | v1.1.0 | ghép lần 2 |

- Mọi buổi demo và mọi lần chốt số liệu đều phải dựng lại được từ một dòng của bảng này.

## 5. Ghép hệ thống theo mốc

- Ghép toàn luồng (crawler → Kafka → bronze → silver → gold → app) **ở cuối mỗi giai đoạn** của lộ trình (P1, P2, P3) và trước mỗi buổi demo. Hai nhóm cần thử chỗ nối thì có thể ghép riêng bất cứ lúc nào.
- Mỗi lần ghép, ghi một dòng vào `deploy/compat.md` (repo Big Data) và một mục vào `joblens/NHAT-KY.md`.
- Lỗi ở chỗ nối giữa các repo được ưu tiên sửa **trước** việc mới.

## 6. Theo dõi công việc

- Việc trong một repo: nhóm tự quản theo cách tiện nhất (issue, checklist, chat…).
- Việc **cần repo khác làm** thì mở issue ở repo đó, gắn nhãn `cross-repo`, để không bị quên. GitHub Projects cấp org là tùy chọn.

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

- Quyết định ảnh hưởng nhiều repo ghi thành ADR ở `joblens/docs/adr/`. Quyết định chỉ trong một repo thì ghi ADR ở repo đó nếu cần cho báo cáo. Tất cả liệt kê trong `joblens/adr-index.md`.
- Glossary chỉ có một bản duy nhất ở `joblens`.
- **Nhật ký `NHAT-KY.md`** chỉ ghi khi:
  - Đổi hợp đồng hoặc file cấu hình chung.
  - Ghép hệ thống, chốt số liệu.
  - Có quyết định đáng nhớ.

  Việc thường ngày không cần ghi.
- **Dùng AI:**
  - Ghi một dòng `AI: <công cụ> – <phần nào>` cuối commit message.
  - Riêng repo PTTKHT ghi thêm vào `docs/ai-log.md`, vì Human-AI collaboration là phần được chấm của môn Phân tích thiết kế hệ thống.
- Họp ngắn khi cần (gợi ý mỗi tuần 15–30 phút): việc xong, việc bị chặn, hợp đồng sắp đổi.

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

## Trước khi push

- [ ] Không lẫn dữ liệu, bí mật hay cấu hình riêng của máy mình (pre-commit chặn phần lớn).
- [ ] Nếu đã sửa trực tiếp trên cluster hay giao diện web: đã đưa ngược vào manifest, values hoặc file export.
- [ ] Nếu đụng hợp đồng: đã sửa ở `joblens`, đã nhắn nhóm, đã ghi một dòng `joblens/NHAT-KY.md` (đổi tên hoặc xóa thì đã có người dùng trả lời "ok").
- [ ] Nếu dùng AI đáng kể: đã ghi dòng `AI:` trong commit message.
