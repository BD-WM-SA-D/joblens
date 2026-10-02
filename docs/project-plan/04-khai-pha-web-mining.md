> [← Mục lục](README.md)

# Các bài toán khai phá (Web Mining)

Đề xuất chọn **3 bài lõi + 1–2 bài mở rộng**, không dàn trải cả 8 bài. Mỗi bài đều có baseline đơn giản trước, mô hình tốt hơn sau, và bộ đánh giá do nhóm tự gán nhãn.

| Mã | Bài toán | Bài giảng | Đầu vào | Baseline → Nâng cao | Dữ liệu đánh giá (nhóm tự làm) | Mức |
|---|---|---|---|---|---|---|
| WM1 | Thu thập & tiền xử lý web: crawler lịch sự, loại boilerplate, **phát hiện tin trùng giữa các trang** (shingling + MinHash LSH) | L01, L04 | HTML | So khớp tiêu đề + công ty → MinHash LSH trên nội dung | ~300 cặp tin gán nhãn trùng/không trùng | **Lõi** |
| WM2 | **Trích xuất thông tin**: span kỹ năng (BIO `SKILL`), lương, kinh nghiệm, cấp bậc; chuẩn hóa kỹ năng về ESCO/alias | L07 | Mô tả công việc | Từ điển + regex → PhoBERT-base-v2 token classification (nhãn yếu từ tag "Kỹ năng cần có" của TopCV và từ điển, sửa tay) | ~1.500 câu gán nhãn span theo guideline kiểu SkillSpan | **Lõi** |
| WM3 | **Khai phá quan điểm theo khía cạnh** trên review công ty, theo 5 khía cạnh ITviec đã chấm điểm sẵn (lương & phúc lợi, đào tạo & học hỏi, quản lý, văn hóa, văn phòng) + cân bằng công việc/OT; điểm sao theo khía cạnh làm nhãn yếu | L06 | Review ITviec | Lexicon/unsupervised (L06-01) → PhoBERT/ViSoBERT fine-tune, có thể khởi động từ dữ liệu ABSA tiếng Việt công khai | ~1.000 câu review gán nhãn aspect + polarity | **Lõi** |
| WM4 | **Tìm kiếm việc làm**: inverted index BM25 + bi-encoder, hybrid ranking | L04 | Tin tuyển dụng, truy vấn | BM25 → hybrid BM25 + embedding | 50 truy vấn × top-20, chấm độ liên quan 0–2 | Mở rộng (chọn WM4 hoặc WM5) |
| WM5 | **Gợi ý việc làm**: content-based (hồ sơ kỹ năng ↔ tin) + implicit CF (ALS) + xử lý cold-start | L08 | `silver.job_skills`, `events.user` (synthetic) | Độ phổ biến → content-based → hybrid với ALS | Chia theo thời gian trên log synthetic; kiểm chứng thêm trên CareerBuilder nếu có thời gian | Mở rộng |
| WM6 | **Đồ thị kỹ năng**: đồ thị đồng xuất hiện, PageRank (kỹ năng "trung tâm"), Louvain (cụm kỹ năng ≈ vai trò) | L05 | `mart_skill_graph_edges` | Degree → PageRank; phát hiện cộng đồng | Đánh giá định tính + modularity + độ ổn định theo tháng | Mở rộng nhẹ |
| WM7 | Query mining trên log tìm kiếm (gom cụm truy vấn, gợi ý truy vấn) | L09 | log synthetic | | | Tùy chọn |
| WM8 | Phân loại nghề 16 lớp / ước lượng lương, so với baseline VietJobs | L02 | VietJobs | Logistic/GBDT trên TF-IDF → PhoBERT | Tập test của VietJobs | Tùy chọn |

Nguyên tắc thực nghiệm: cố định **snapshot Iceberg** cho train/test; báo cáo cả baseline; ghi rõ thời gian gán nhãn và độ đồng thuận giữa người gán nhãn (Cohen's κ trên ~10% mẫu) để kết quả đáng tin.

## Metrics mô hình

Mỗi metric thuộc về **đúng một môn** (quy tắc R4 trong [Quy tắc phân tách](07-quy-tac-phan-tach-mon.md)). Chỉ tiêu là đề xuất để nhóm có đích nhắm, sẽ hiệu chỉnh sau khi có số đo đầu tiên.

| Bài | Metric chính | Metric phụ | Mốc tham chiếu |
|---|---|---|---|
| WM1 dedup | Precision/Recall/F1 trên cặp trùng | tỉ lệ tin trùng liên trang | – |
| WM2 IE | **F1 cấp thực thể (seqeval, strict)** | Precision/Recall, F1 theo loại kỹ năng; độ chính xác chuẩn hóa ESCO | baseline từ điển của nhóm |
| WM3 ABSA | **Macro-F1** phát hiện aspect và phân cực | F1 theo từng aspect, confusion matrix | VLSP 2018 ABSA ~0,70–0,80 F1 (domain khác, chỉ tham khảo) |
| WM4 IR | **nDCG@10**, MAP | P@10, MRR | BM25 |
| WM5 RecSys | **Recall@10, nDCG@10** | HitRate@10, coverage, novelty; cold-start riêng | Popularity |
| WM6 Graph | modularity | độ ổn định cụm theo tháng; top-k PageRank | – |
| WM8 | Accuracy, Macro-F1 (nghề); RMSE, R² (lương) | | VietJobs: Acc 0,47 (few-shot); RMSE 10,24 triệu VND |
