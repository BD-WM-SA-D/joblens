# Danh mục ADR

ADR nằm ở repo chủ (`docs/adr/NNNN-ten-ngan.md`); bảng này chỉ là danh mục chung cho cả 3 repo (docs/project-plan/09, quy tắc 10).

| Repo | Số | Tiêu đề | Trạng thái | Ngày |
|---|---|---|---|---|
| joblens | [0001](docs/adr/0001-ranh-gioi-xu-ly-giua-cac-repo.md) | Ranh giới xử lý giữa các repo (parse, chuẩn hóa, mô hình, tìm kiếm/cảnh báo, khóa tin, quyền đọc joblens, biến môi trường) | Đề xuất | 2026-10-02 |
| joblens | [0002](docs/adr/0002-goi-y-truc-tuyen-tu-ho-so-ky-nang.md) | Gợi ý việc làm trực tuyến từ hồ sơ kỹ năng (mining-service, đường lùi) | Đề xuất | 2026-10-12 |
| PTTKHT-joblens | [0001](https://github.com/BD-WM-SA-D/PTTKHT-joblens/blob/main/docs/adr/0001-cong-nghe-cong.md) | Công nghệ cổng: FastAPI + React/Vite + PostgreSQL | Đề xuất | 2026-10-12 |
| PTTKHT-joblens | [0002](https://github.com/BD-WM-SA-D/PTTKHT-joblens/blob/main/docs/adr/0002-khong-luu-van-ban-cv.md) | Không lưu văn bản CV, chỉ lưu kỹ năng đã xác nhận | Đề xuất | 2026-10-12 |

Gợi ý các ADR đầu tiên (từ tài liệu kế hoạch): Lambda hay Kappa (platform, sau thí nghiệm batch vs streaming), chọn catalog Lakekeeper, chọn SeaweedFS thay MinIO.
