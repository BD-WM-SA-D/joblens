> [← Mục lục](README.md)

# Rủi ro và câu hỏi cho giảng viên

## Rủi ro và dự phòng

| Rủi ro | Khả năng | Ảnh hưởng | Dự phòng |
|---|---|---|---|
| Giảng viên không cho dùng chung đề tài | Trung bình | Cao | Hỏi ngay ở P0; nếu SA&D từ chối → SA&D làm đề tài quản lý riêng, BD + WM vẫn giữ JobLens |
| Trang nguồn đổi HTML/chặn bot | Cao | Trung bình | Adapter pattern; lưu HTML thô trên S3 (`s3://joblens/raw-html/`); replay VietJobs vào Kafka nếu crawl hỏng; thu hẹp phạm vi crawl; không lách chống bot (xem [chiến lược dữ liệu](13-kham-pha-du-lieu.md#chiến-lược-dữ-liệu-crawl-là-dữ-liệu-chính-vietjobs-phục-vụ-việc-khác-chốt-2026-10-12)) |
| VietJobs bản đầy đủ thiếu `company_name`/`posting_date`/`url` (**đã xác nhận** 2026-10-07) | – | Đã xảy ra | Chỉ dùng VietJobs để backfill phân bố nghề/lương và làm baseline; phân tích theo công ty/thời gian dựa vào dữ liệu tự crawl |
| Tin IT trong VietJobs quá ít (~1.900/48.000, ~4%) | Chắc chắn | Trung bình | WM2 dùng tin IT tự crawl từ TopCV (tag kỹ năng của nhà tuyển dụng làm nhãn yếu); VietJobs chỉ bổ trợ |
| Review ITviec ít hoặc bị giới hạn khi chưa đăng nhập | Trung bình | Trung bình | Chỉ lấy review công khai; đếm thử ~20 công ty trước; nếu không đủ thì thu hẹp hoặc bỏ WM3 |
| **ITviec không cho phép** (điều khoản mục 2.2 yêu cầu đồng ý bằng văn bản – kiểm tra 2026-10-12) | Trung bình | Cao | Đã gửi email xin phép: <ngày gửi>. Chưa có trả lời thì không crawl ITviec. Dự phòng: (1) trang tuyển dụng thứ hai khác cho dedup WM1 (kiểm tra robots.txt + điều khoản trước); (2) nguồn review công ty khác hoặc thu hẹp WM3; (3) hỏi giảng viên |
| Máy không đủ RAM cho K8s | Cao | Cao | Tắt bớt thành phần khi không dùng; 1 broker; Trino 1 worker; VM cloud cho demo |
| Lệch phiên bản (Spark/Iceberg/operator) | Trung bình | Trung bình | Pin trong `joblens/versions.md`; Spark 4.1 + Iceberg 1.11; submit native k8s thay vì phụ thuộc Spark Operator (Dockerfile của operator đang pin Spark 4.0) |
| Gán nhãn tốn thời gian | Cao | Trung bình | Gán nhãn yếu bằng từ điển rồi sửa tay; giới hạn cỡ tập (xem [Web Mining](04-khai-pha-web-mining.md)); đo κ trên mẫu nhỏ |
| Kết quả RecSys kém tin cậy vì dữ liệu synthetic | Chắc chắn | Trung bình | Nói rõ trong báo cáo; ưu tiên WM4 (IR) có relevance judgment thật; kiểm chứng trên CareerBuilder nếu kịp |
| MinIO không còn được bảo trì | Đã xảy ra | Thấp | Dùng SeaweedFS ngay từ đầu |
| Báo cáo bị xem là trùng lặp | Trung bình | Cao | Áp dụng R1–R13; khung "Phạm vi đánh giá"; nhãn môn trên repo |

## Câu hỏi cần xác nhận với giảng viên

**Chung (hỏi cả ba giảng viên):**

1. Nhóm có được dùng chung một hệ thống/bộ dữ liệu cho nhiều môn không, nếu mỗi báo cáo chỉ đề nghị chấm phần riêng (theo [ma trận sở hữu](07-quy-tac-phan-tach-mon.md#ma-trận-sở-hữu))?
2. Thành viên nhóm không học cùng tất cả các môn – có ràng buộc nào về thành phần nhóm không?

**Big Data Storage & Processing:**

3. Yêu cầu "phải dùng Kubernetes" áp dụng cho toàn bộ pipeline hay chỉ cần Spark chạy với `k8s://` master? Cluster local (k3d/kind) có được chấp nhận không?
4. Có bắt buộc bám đúng stack của slide L14 (Kafka – Spark – Iceberg – dbt – GE – Airflow – Trino) không, hay được thay thế tương đương (ví dụ SeaweedFS thay MinIO, Lakekeeper làm catalog)?

**Phân tích thiết kế hệ thống:**

5. Đề tài dạng "cổng phân tích thị trường tuyển dụng có hệ thống con dữ liệu" có phù hợp không, khi các ví dụ trong slide là hệ thống quản lý?
6. Chương 5 (thực hiện & triển khai) có yêu cầu mức cài đặt tối thiểu nào không?

**Web Mining:**

7. Có hướng dẫn/tiêu chí đồ án riêng không (số kỹ thuật tối thiểu, có bắt buộc tự thu thập dữ liệu)?

**Bổ sung về dữ liệu (hỏi giảng viên Big Data, và Web Mining nếu cần):**

8. Đề tài có bắt buộc dữ liệu **tự thu thập** không, hay được dùng dataset công khai (VietJobs) làm nguồn chính kèm một phần crawl nhỏ, tăng dần?
