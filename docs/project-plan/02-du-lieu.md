> [← Mục lục](README.md)

# Dữ liệu

## Nguồn thu thập trực tiếp

| Nguồn | Nội dung | robots.txt (kiểm tra 29/09/2026) | Ghi chú |
|---|---|---|---|
| [TopCV](https://www.topcv.vn/robots.txt) | Tin tuyển dụng đa ngành, có lương, kinh nghiệm, địa điểm | `User-agent: *`; chặn các đường dẫn CV (`/xem-cv/`, `/cv-ung-vien/`, `/cv-ung-tuyen/`, `/private/`…); có sitemap | Dùng sitemap để liệt kê URL tin. **Tuyệt đối không** chạm các đường dẫn CV. |
| [ITviec](https://itviec.com/robots.txt) | Tin tuyển dụng IT + **review công ty** | Cho phép `/`, chỉ chặn `/subscriptions/new`; có sitemap | Lương trên ITviec thường chỉ hiện khi đăng nhập (cần kiểm chứng) → không crawl sau đăng nhập; phân tích lương dựa chủ yếu vào TopCV + VietJobs. Review công ty là nguồn chính cho Opinion Mining. |
| VietnamWorks (tùy chọn) | Tin tuyển dụng | Chưa kiểm tra | Chỉ thêm nếu còn thời gian; kiểm tra robots/ToS trước. |

Quy tắc crawl lịch sự (áp dụng cho mọi spider): tôn trọng robots.txt; tối đa ~1 request/giây/domain, có `AUTOTHROTTLE`; User-Agent ghi rõ mục đích học tập + email nhóm; cache HTML thô để không crawl lại; chỉ lấy trường cần thiết.

## Dataset công khai (nền, backfill và benchmark)

> Kết quả xem thực tế từng nguồn (cấu trúc trường, chất lượng, hệ quả cho thiết kế): [Khám phá dữ liệu](13-kham-pha-du-lieu.md). Lưu ý quan trọng: các cột kỹ năng của VietJobs do LLM trích, chỉ dùng làm nhãn yếu.

| Dataset | Quy mô / nội dung | Giấy phép | Dùng vào đâu |
|---|---|---|---|
| **[VietJobs](https://arxiv.org/html/2603.05262v1)** (LREC 2026, VinUniversity) – [GitHub](https://github.com/VinNLP/VietJobs), tải qua `huggingface-cli download dinhieufam/VietJobs` | 48.092 tin từ TopCV (07–10/2025), 15,4 triệu từ, 34 tỉnh/thành, 16 nhóm nghề; 71,5% tin có khoảng lương. Bản trên HF có 26 cột, gồm `technical_skills`, `soft_skills`, `salary_min/max/avg`, `category`, `description`, `requirements_text` | Bài báo ghi CC BY 4.0, repo ghi MIT, trang HF chưa ghi → trích dẫn đầy đủ | (1) **Backfill** lịch sử cho đường batch; (2) cột `technical_skills`/`soft_skills` làm **nhãn yếu** cho WM2; (3) **baseline** so sánh: phân loại nghề 16 lớp (few-shot tốt nhất Acc 0,47), ước lượng lương (RMSE tốt nhất 10,24 triệu VND) |
| **[ESCO v1.2.x](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/esco-v12)** (EU) | Taxonomy kỹ năng/nghề, tải CSV | Mở (EU) | Chuẩn hóa kỹ năng: alias Việt/Anh → ESCO skill URI; tạo nhãn yếu cho NER. ESCO không có tiếng Việt → nhóm tự xây từ điển alias. |
| [SkillSpan](https://www.researchgate.net/publication/362270563_SkillSpan_Hard_and_Soft_Skill_Extraction_from_English_Job_Postings) (NAACL 2022), [Skill-Extraction-benchmark](https://github.com/jensjorisdecorte/Skill-Extraction-benchmark/) | Chuẩn gán nhãn span kỹ năng tiếng Anh | Nghiên cứu | Tham khảo **guideline gán nhãn** kỹ năng (hard/soft) cho bộ tiếng Việt của nhóm |
| [vietnamese-job-skill-ner](https://github.com/phamthaic4/vietnamese-job-skill-ner) | Dự án nhỏ: BIO `SKILL`, PhoBERT, đánh giá seqeval | Chưa ghi license | Tham khảo cấu trúc dữ liệu/huấn luyện; **không** dùng dữ liệu nếu chưa rõ license |
| [UIT-VSFC, UIT-ViSFD, VLSP 2018 ABSA](https://github.com/undertheseanlp/NLP-Vietnamese-progress/blob/master/tasks/sentiment_analysis.md) | Sentiment/ABSA tiếng Việt (16k câu feedback sinh viên; 11k bình luận smartphone; nhà hàng/khách sạn) | Theo từng bộ (thường chỉ dùng nghiên cứu) | Tiền huấn luyện/so sánh cho ABSA review công ty; mốc tham chiếu F1 |
| [CareerBuilder Job Recommendation (Kaggle 2012)](https://www.kaggle.com/competitions/job-recommendation/overview/prizes) | Log ứng tuyển thật (tiếng Anh, Mỹ) | Điều khoản Kaggle | Tùy chọn: kiểm chứng thuật toán gợi ý trên tương tác thật, vì dữ liệu tương tác của JobLens là giả lập |

## Dữ liệu giả lập (nói rõ trong mọi báo cáo)

Hệ thống không có người dùng thật, nên cần một **bộ sinh sự kiện** (`event-generator`) tạo luồng tương tác: `search`, `view`, `save`, `apply` với hành vi có tham số (người dùng có hồ sơ kỹ năng, xác suất xem tỉ lệ với độ khớp kỹ năng, có nhiễu và độ phổ biến). Bộ này phục vụ ba việc: nguồn streaming liên tục cho Kafka (BD), dữ liệu tương tác cho Recommender và log truy vấn cho Query Mining (WM), và kịch bản tải cho kiểm thử NFR (SA&D). Mọi kết quả trên dữ liệu giả lập phải được gắn nhãn "synthetic" và không được trình bày như hành vi người dùng thật.

## Ước lượng khối lượng – "5V" của đề tài (để trả lời câu hỏi "có đủ big không?")

| V | Ước lượng đề xuất | Cách đạt |
|---|---|---|
| Volume | ~50k tin backfill + ~1–3k tin mới/ngày; **snapshot hằng ngày** của tin đang mở → ~0,5–1 triệu bản ghi snapshot sau 8–10 tuần; ~vài triệu sự kiện giả lập | Không cần "giả to": giá trị nằm ở lịch sử snapshot (tin sống bao lâu, lương thay đổi) |
| Velocity | Crawl theo lô (hằng ngày) + luồng sự kiện liên tục (hàng chục–trăm event/giây, chỉnh được) | Đủ để so sánh batch vs streaming như L14 yêu cầu |
| Variety | HTML bán cấu trúc, JSON sự kiện, CSV taxonomy, văn bản tự do tiếng Việt/Anh | |
| Veracity | Tin trùng giữa các trang, lương "Thỏa thuận", kỹ năng viết tắt/sai chính tả | Là đất diễn cho Great Expectations và dedup |
| Value | Mart kỹ năng/lương/đánh giá công ty, gợi ý việc làm | |

Các con số trên là ước lượng để lập kế hoạch; nhóm đo thực tế sau 1–2 tuần crawl thử rồi cập nhật.

## Tuân thủ pháp lý và đạo đức dữ liệu

- **Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15** có hiệu lực từ 01/01/2026, cùng Nghị định hướng dẫn 356/2025/NĐ-CP ([Tilleke & Gibbins](https://www.tilleke.com/insights/vietnams-new-personal-data-protection-law-a-closer-look/)). Đề xuất xử lý: không thu thập CV/trang cần đăng nhập; loại bỏ ngay ở tầng silver mọi trường có thể là dữ liệu cá nhân (tên người liên hệ, email, SĐT, tên người review); bronze chỉ giữ HTML đã qua bộ lọc PII và có thời hạn lưu (ví dụ 30 ngày); dữ liệu chỉ dùng cho mục đích học tập, không chia sẻ lại. (Đây không phải tư vấn pháp lý – nhóm nên hỏi giảng viên nếu có quy định riêng của trường.)
- Tôn trọng robots.txt và điều khoản sử dụng từng trang; dừng crawl nếu bị yêu cầu.
- Trích dẫn và tuân thủ giấy phép của mọi dataset công khai.
