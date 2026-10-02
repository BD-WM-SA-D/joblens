# JobLens VN – Tài liệu dự án liên môn

**Nền tảng thu thập, lưu trữ và khai phá dữ liệu thị trường tuyển dụng Việt Nam**

Một hệ thống dùng chung cho ba môn học kỳ **20261** của nhóm 4–5 sinh viên:

| Môn | Câu hỏi môn này chấm | Repo nộp |
|---|---|---|
| IT4931 Big Data Storage and Processing | Dữ liệu được di chuyển, lưu trữ, xử lý ở quy mô lớn thế nào, vì sao chọn như vậy? | `Big-Data-Storage-and-Processing-joblens` |
| Web Mining | Tri thức gì được khai phá từ dữ liệu web, bằng kỹ thuật nào, tốt đến đâu? | `Web-mining-joblens` |
| IT3120 Phân tích thiết kế hệ thống | Hệ thống phục vụ ai, cần đáp ứng gì, được thiết kế thế nào? | `PTTKHT-joblens` |

> **Cập nhật 02/10/2026:** tên repo/org theo GitHub thật (`BD-WM-SA-D`); ranh giới xử lý giữa các repo theo [ADR 0001](../adr/0001-ranh-gioi-xu-ly-giua-cac-repo.md) (đang chờ nhóm duyệt); hợp đồng dữ liệu ở [`schemas/`](../../schemas/README.md).
>
> **Trạng thái: ĐỀ XUẤT – v1 (29/09/2026).** Lựa chọn công nghệ, chỉ tiêu và lịch là đề xuất, cần nhóm thống nhất và giảng viên xác nhận (xem [câu hỏi cho giảng viên](11-rui-ro-va-cau-hoi.md#câu-hỏi-cần-xác-nhận-với-giảng-viên)). Bộ tài liệu này thay cho file đơn `de-xuat-du-an-lien-mon-JobLens.md` trước đó.

## Mục lục

| # | Tài liệu | Nội dung |
|---|---|---|
| 01 | [Tổng quan, căn cứ và lựa chọn phương án](01-tong-quan.md) | Tóm tắt, căn cứ từ slide/guideline của 3 môn, bài toán & phạm vi, 2 phương án thay thế |
| 02 | [Dữ liệu](02-du-lieu.md) | Nguồn crawl + robots.txt, dataset công khai (VietJobs, ESCO…), dữ liệu synthetic, 5V, pháp lý |
| 03 | [Nền tảng dữ liệu (Big Data)](03-nen-tang-big-data.md) | Kiến trúc, Kafka, Iceberg, batch vs streaming, Kubernetes, tech stack, metrics nền tảng |
| 04 | [Các bài toán khai phá (Web Mining)](04-khai-pha-web-mining.md) | WM1–WM8, baseline → nâng cao, dữ liệu đánh giá, metrics mô hình |
| 05 | [Phân tích thiết kế hệ thống](05-phan-tich-thiet-ke-he-thong.md) | Mô hình nghiệp vụ, UC001–UC010, NFR, thiết kế theo guideline 7 chương, metrics chấp nhận |
| 06 | [Ma trận liên kết](06-ma-tran-lien-ket.md) | Ca sử dụng ↔ bảng gold ↔ bài khai phá ↔ bài giảng ↔ metric |
| 07 | [Quy tắc phân tách giữa các môn](07-quy-tac-phan-tach-mon.md) | Ma trận sở hữu, quy tắc R1–R13, khung báo cáo cho từng môn |
| 08 | [Tổ chức repo và GitHub](08-to-chuc-repo-va-github.md) | 4 repo, cách nối qua hợp đồng dữ liệu, tạo org, phân quyền |
| 09 | [Quy tắc làm việc chung giữa các repo](09-quy-tac-lam-viec-chung.md) | 10 quy tắc kỹ thuật (gồm những gì không được đưa lên GitHub), mục chú ý về thứ thay đổi nằm ngoài git, checklist PR |
| 10 | [Phân công và lộ trình](10-phan-cong-va-lo-trinh.md) | Vai trò 4–5 người, lịch 12 tuần |
| 11 | [Rủi ro và câu hỏi cho giảng viên](11-rui-ro-va-cau-hoi.md) | Rủi ro + dự phòng, câu hỏi cần xác nhận |
| 12 | [Tài liệu tham khảo](12-tai-lieu-tham-khao.md) | Bài giảng, bài báo, tài liệu công nghệ, dataset, pháp lý |
| 13 | [Khám phá dữ liệu trước khi làm](13-kham-pha-du-lieu.md) | Kết quả xem thực tế VietJobs, TopCV, ITviec, ESCO, UIT-VSFC; cách tự xem; script `explore/01_vietjobs_eda.py` |
| – | [Mẫu README repo](templates/README-repo.md) · [Mẫu CONTRIBUTING](templates/CONTRIBUTING.md) · [`.gitignore` mẫu](templates/gitignore.template) · [pre-commit mẫu](templates/pre-commit-config.yaml) | Bản gốc file cấu hình chung – đồng bộ sang 4 repo bằng `scripts/sync_templates.py` |

## Đọc theo vai trò

- **Cả nhóm (bắt buộc):** 01 → 07 → 09 → 10.
- **Phụ trách Big Data:** 02 → 03 → 06, rồi 08.
- **Phụ trách Web Mining:** 02 → 04 → 06.
- **Phụ trách Phân tích thiết kế hệ thống:** 05 → 06 → 07 (khung 7 chương).
- **Trước khi gặp giảng viên:** 11.

## Các quyết định chính (đề xuất)

- **Domain:** thị trường tuyển dụng, dữ liệu **hybrid**: VietJobs làm nền (pipeline, WM8, baseline) + crawl nhỏ tăng dần TopCV ngành IT (streaming, WM2) + review ITviec (WM3); replay VietJobs vào Kafka nếu crawl thất bại ([chi tiết](13-kham-pha-du-lieu.md#chiến-lược-dữ-liệu-hybrid-đề-xuất)).
- **Nền tảng:** Kafka (Strimzi) → Spark 4.1 (batch + Structured Streaming) → Iceberg 1.11 trên SeaweedFS, catalog Lakekeeper → dbt → Great Expectations → Airflow 3 → Trino; chạy trên k3d; bám slide L14 "Project ideas".
- **Khai phá lõi:** thu thập + dedup, trích xuất kỹ năng (PhoBERT), ABSA review công ty; mở rộng: tìm kiếm/gợi ý, đồ thị kỹ năng.
- **SA&D:** cổng JobLens (actor: người tìm việc, HR/chuyên viên, quản trị dữ liệu) với nền tảng dữ liệu là hệ thống con.
- **Tách môn:** mỗi thành phần đúng một môn chấm chính; mỗi môn một repo; mỗi báo cáo có khung "Phạm vi đánh giá".

## Việc cần làm ngay (tuần T0)

- [ ] Điền bảng đăng ký môn của từng thành viên ([R7](07-quy-tac-phan-tach-mon.md)).
- [ ] Gửi câu hỏi cho ba giảng viên, nhất là việc dùng chung đề tài và phạm vi Kubernetes ([11](11-rui-ro-va-cau-hoi.md#câu-hỏi-cần-xác-nhận-với-giảng-viên)).
- [x] Tạo GitHub Organization `BD-WM-SA-D` và 4 repo ([08](08-to-chuc-repo-va-github.md)); file cấu hình chung đồng bộ bằng `scripts/sync_templates.py` thay cho template repository.
- [ ] Chốt `versions.md` và bộ biến môi trường `JOBLENS_*` ([09](09-quy-tac-lam-viec-chung.md)).
- [ ] Crawl thử 1–2 tuần để đo khối lượng thật, cập nhật ước lượng 5V ([02](02-du-lieu.md)).
