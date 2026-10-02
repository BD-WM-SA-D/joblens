> [← Mục lục](README.md)

# Tổ chức repo và GitHub

Mỗi môn cần dẫn một link repo riêng, nên dự án chia thành **4 repo** trong một GitHub Organization: 3 repo tương ứng 3 môn và 1 repo nhỏ dùng chung. Các repo chỉ nối với nhau qua **hợp đồng dữ liệu** (schema message, schema bảng), không import code của nhau.

## Cấu trúc 4 repo

```
joblens-vn/                     (GitHub Organization)
│
├── joblens-contracts           ← dùng chung, nhỏ, có version (v1.0.0, v1.1.0…)
│   ├── schemas/kafka/          # JSON Schema cho từng topic (jobs.raw.*, reviews.raw.*, events.user…)
│   ├── schemas/tables/         # data contract YAML cho bronze/silver/gold
│   ├── fixtures/               # dữ liệu mẫu nhỏ (~1k tin từ VietJobs, có ghi nguồn + giấy phép)
│   ├── glossary.md             # thuật ngữ chung (một bản duy nhất)
│   ├── versions.md             # pin phiên bản Spark/Iceberg/Kafka/Trino/…
│   └── adr-index.md            # danh mục ADR của cả 3 repo
│
├── joblens-platform            ← link nộp môn BIG DATA
│   ├── deploy/                 # Helm values, manifest K8s, cấu hình k3d – nơi DUY NHẤT ghép toàn hệ thống
│   │   └── compat.md           # bảng phiên bản: platform x mining x app x contracts
│   ├── spark-jobs/             # streaming bronze, batch backfill, silver jobs, compaction
│   ├── dbt/                    # gold marts + dbt tests
│   ├── gx/                     # Great Expectations suites
│   ├── airflow/dags/
│   ├── event-generator/        # luồng sự kiện synthetic
│   ├── benchmarks/             # batch vs streaming, Trino p95, lag…
│   └── docs/                   # nguồn báo cáo BD + ADR (Lambda/Kappa, catalog, object storage)
│
├── joblens-mining              ← link nộp môn WEB MINING
│   ├── crawler/                # spiders, parser, dedup, producer ghi vào Kafka
│   ├── ie/  absa/  retrieval/  recsys/  graph/
│   ├── annotation/             # guideline gán nhãn, chỉ số κ (không commit dữ liệu crawl thô)
│   ├── experiments/            # notebook + kết quả, ghi rõ snapshot Iceberg đã dùng
│   ├── images/                 # Dockerfile cho các job mô hình (skill-extractor, absa-scorer…)
│   └── docs/                   # nguồn báo cáo WM
│
└── joblens-app                 ← link nộp môn PHÂN TÍCH THIẾT KẾ HỆ THỐNG
    ├── api/  web/
    ├── uml/                    # PlantUML / draw.io: UC, ECB, sequence, state, package, deployment
    ├── requirements/           # user story, đặc tả UC, NFR
    ├── tests/acceptance/       # kịch bản Given/When/Then
    └── docs/                   # nguồn báo cáo 7 chương
```

Repo nào cũng có `README.md` theo [mẫu](templates/README-repo.md) (mở đầu bằng khung "Phạm vi đánh giá") và `CONTRIBUTING.md` theo [mẫu](templates/CONTRIBUTING.md).

## Các repo nối với nhau thế nào

| Chiều | Cơ chế | Hợp đồng |
|---|---|---|
| mining → platform (dữ liệu) | Crawler ghi message vào Kafka | `schemas/kafka/*.json` |
| mining → platform (mô hình) | Mô hình đóng thành Docker image có tag, ví dụ `skill-extractor:1.2.0-a1b2c3d`; Airflow bên platform chạy bằng KubernetesPodOperator | Input/output là các bảng trong `schemas/tables/` |
| platform → app | App chỉ **đọc** gold qua Trino | `schemas/tables/gold/*.yaml` |
| contracts → mọi repo | Cài theo git tag cố định: `pip install git+https://github.com/joblens-vn/joblens-contracts@v1.1.0` | SemVer |

Kết quả: repo Big Data không chứa code mô hình, repo Web Mining không chứa code hạ tầng, repo SA&D không chứa code xử lý dữ liệu – khớp [ma trận sở hữu](07-quy-tac-phan-tach-mon.md#ma-trận-sở-hữu).

Tránh dùng git submodule (dễ lỗi khi nhiều người cùng làm) và tránh tách tự động từ monorepo bằng `git subtree split` (phức tạp, dễ lệch).

## Mỗi repo phải chạy được một mình

Giảng viên clone một repo về là chạy được, không cần hai repo kia (phép thử "đọc độc lập" R9):

- `joblens-mining`: train và đánh giá trên VietJobs + `fixtures`, không cần Kafka/K8s.
- `joblens-app`: chạy với gold mẫu (DuckDB/Parquet sinh từ `fixtures`) thay cho Trino.
- `joblens-platform`: nạp raw mẫu từ `fixtures` thay cho crawler thật; image mô hình có thể thay bằng stub.

README của từng repo có mục **"Phụ thuộc"** liệt kê link hai repo kia, ghi rõ chỉ để tham khảo, không thuộc phần chấm.

## Dữ liệu và bí mật

- Dữ liệu crawl, HTML thô, tập nhãn làm từ dữ liệu crawl và file model **không commit vào git**; lưu trong object storage (`s3://joblens/{bronze|silver|gold|models|labels}/…`).
- Chỉ dữ liệu mẫu có giấy phép rõ ràng (VietJobs, ghi nguồn) được vào `fixtures`.
- Không commit mật khẩu/key: dùng `.env` (đã gitignore) và Kubernetes Secret.
- Danh sách đầy đủ những gì không được đưa lên GitHub, `.gitignore` và pre-commit mẫu: [quy tắc 8](09-quy-tac-lam-viec-chung.md#8-những-gì-không-được-đưa-lên-github).

## Tạo GitHub Organization

Bất kỳ tài khoản GitHub nào cũng tạo được organization, miễn phí:

1. Ảnh đại diện → **Settings** → **Organizations** → **New organization**.
2. Chọn gói **Free**, đặt tên (ví dụ `joblens-vn`; nếu trùng thêm hậu tố như `joblens-hust`).
3. Mời thành viên; nên có **2 owner** để không bị kẹt khi một người vắng.
4. Tạo một **template repository** (chứa README/CONTRIBUTING mẫu, `.env.example`, cấu hình pre-commit) rồi sinh cả 4 repo từ template này.

**Gói Free có:** không giới hạn repo private và người cộng tác; 2.000 phút GitHub Actions/tháng – đủ cho lint/test của 4 repo trong một học kỳ.

**Giới hạn cần biết:**

- Protected branches, bắt buộc review PR, CODEOWNERS trên **repo private** thuộc gói Team (trả phí). Với gói Free, nhóm giữ quy ước "không push thẳng `main`, luôn mở PR"; nếu cần ép bằng cài đặt thì để repo public (với điều kiện repo không chứa dữ liệu crawl).
- Dung lượng package private nhỏ, trong khi image mô hình (PhoBERT…) thường vài GB → build tại máy rồi `k3d image import`, hoặc để image public nếu trong image không có dữ liệu.
- GitHub Student Developer Pack nâng cấp tài khoản **cá nhân** lên Pro, không nâng org lên Team. Nếu thật cần gói Team, giảng viên có thể xin qua chương trình GitHub Education dành cho giáo viên; với đồ án này gói Free là đủ.

## Phân quyền

| Ai | Quyền |
|---|---|
| Base permissions của org | **No permission** (không ai tự động thấy mọi repo) |
| Team `bd`, `wm`, `sad` (theo môn đăng ký học) | Write trên repo môn tương ứng; Read trên các repo còn lại |
| Mọi thành viên | Write trên `joblens-contracts` (mọi thay đổi vẫn qua PR) |
| Giảng viên từng môn | *Outside collaborator*, quyền **Read** trên đúng repo của môn mình |

## Không gian làm việc trên máy

Thư mục `C:\Users\hoang le\joblens` (nằm ngoài OneDrive – tránh lỗi khóa file và xung đột trong `.git`) dùng làm không gian làm việc chung:

```
C:\Users\hoang le\joblens\
├── README.md            # mục lục bộ tài liệu này
├── docs\                # tài liệu dự án (có thể đưa thành repo `.github` hoặc wiki của org)
├── joblens-contracts\   # clone về sau khi tạo org
├── joblens-platform\
├── joblens-mining\
└── joblens-app\
```

Nguồn tham khảo: [Creating a new organization](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/creating-a-new-organization-from-scratch) · [GitHub's plans](https://docs.github.com/get-started/learning-about-github/githubs-products).
