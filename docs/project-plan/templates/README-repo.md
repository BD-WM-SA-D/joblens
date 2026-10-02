<!-- Mẫu README cho joblens-platform / joblens-mining / joblens-app. Thay các chỗ <...>. -->

# <joblens-platform | joblens-mining | joblens-app>

<Một câu mô tả repo, ví dụ: "Nền tảng lakehouse của dự án JobLens VN: Kafka → Spark → Iceberg → dbt → Trino trên Kubernetes.">

> **Phạm vi đánh giá – môn <Big Data Storage and Processing | Web Mining | Phân tích thiết kế hệ thống> (<mã môn>, học kỳ 20261)**
>
> Dự án JobLens dùng chung hạ tầng dữ liệu với môn <X> và <Y> (đã được giảng viên đồng ý ngày <dd/mm/yyyy>). Repo này chỉ chứa và đề nghị đánh giá các phần: <liệt kê theo ma trận sở hữu>. Các phần <…> thuộc môn khác, nằm ở repo riêng và chỉ được nhắc tới để làm rõ bối cảnh.

## Thành viên phụ trách

| Thành viên | MSSV | Vai trò trong repo này |
|---|---|---|
| <Họ tên> | <MSSV> | <…> |

## Chạy nhanh (không cần các repo khác)

```bash
# 1. Cài hợp đồng dữ liệu (pin version)
pip install git+https://github.com/<org>/joblens-contracts@v<x.y.z>

# 2. Cấu hình
cp .env.example .env

# 3. Chạy với dữ liệu mẫu (fixtures)
<lệnh chạy>
```

## Cấu trúc thư mục

```
<cây thư mục chính và một dòng mô tả mỗi thư mục>
```

## Tài liệu

- Báo cáo môn: [`docs/`](docs/)
- Quyết định kiến trúc: [`docs/adr/`](docs/adr/)
- Thuật ngữ: `joblens-contracts/glossary.md`

## Phụ thuộc (chỉ để tham khảo, không thuộc phần chấm)

| Repo | Vai trò | Version đang dùng |
|---|---|---|
| `joblens-contracts` | Schema message/bảng, fixtures, glossary | v<x.y.z> |
| `<repo khác>` | <…> | v<x.y.z> |

## Chốt số liệu cho báo cáo

| Tag | Ngày | Iceberg tag / snapshot | Ghi chú |
|---|---|---|---|
| `report-<bd|wm|sad>-v1` | <dd/mm/yyyy> | <…> | <…> |

## Dữ liệu và giấy phép

Repo không chứa dữ liệu crawl. Dữ liệu mẫu trong `joblens-contracts/fixtures` lấy từ VietJobs (Pham Dinh et al., LREC 2026) – trích dẫn theo giấy phép của dataset.
