> [← Mục lục](README.md)

# Khám phá dữ liệu trước khi làm

Tài liệu này ghi lại những gì đã kiểm tra thực tế ở các nguồn dữ liệu của dự án (29/09/2026), điều rút ra cho thiết kế, và cách cả nhóm tự xem lại. Danh sách nguồn đầy đủ và giấy phép: [Dữ liệu](02-du-lieu.md).

> [!NOTE]
> Trong phiên soạn tài liệu này, mạng không truy cập được Hugging Face, nên VietJobs mới được xem qua **file mẫu 5 dòng và mã nguồn trên GitHub**. Các nhận xét về VietJobs dưới đây cần được xác nhận lại trên bản đầy đủ bằng script [`explore/01_vietjobs_eda.py`](../../explore/01_vietjobs_eda.py).

## Tự xem trong 30 phút

| # | Việc | Cách làm | Để ý điều gì |
|---|---|---|---|
| 1 | Xem VietJobs trên trình duyệt | Mở [trang dataset](https://huggingface.co/datasets/dinhieufam/VietJobs), tab *Dataset Viewer* | Cột nào hay trống; cột kỹ năng trông thế nào; lương ghi dạng gì |
| 2 | Chạy thống kê VietJobs | `pip install pandas pyarrow huggingface_hub` rồi `python explore/01_vietjobs_eda.py` (tự tải về `data/vietjobs/`, đã gitignore) | Kết quả lưu ở `explore/out/vietjobs_eda.md` – so với các nhận xét bên dưới |
| 3 | Xem mã crawl của VietJobs | [GitHub VinNLP/VietJobs](https://github.com/VinNLP/VietJobs), thư mục `crawling/` | Cách họ crawl TopCV và dùng LLM để trích trường |
| 4 | Xem cấu trúc tin trên TopCV | Mở [sitemap jobs_0.xml](https://www.topcv.vn/sitemap/jobs_0.xml), bấm vài link tin | Trường nào có sẵn dạng cấu trúc, trường nào phải tự tách từ văn bản |
| 5 | Xem review công ty trên ITviec | Ví dụ [trang review NTT Data Vietnam](https://itviec.com/companies/ntt-data-vietnam/review) | Điểm theo từng khía cạnh, phần "What I liked" / "Suggestions for improvement" |
| 6 | Xem ESCO | [Trang tải CSV](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/comma-separated-values-csv), chọn tiếng Anh | Bảng skills, occupations, quan hệ occupation–skill |
| 7 | Xem một bộ sentiment tiếng Việt | [UIT-VSFC trên Hugging Face](https://huggingface.co/datasets/uitnlp/vietnamese_students_feedback) | Nhãn, cỡ dữ liệu, giấy phép |

## VietJobs

**Nguồn gốc các trường.** Mã trong `crawling/` cho thấy nhóm tác giả crawl trang TopCV bằng *crawl4ai*, rồi dùng **LLM (Azure OpenAI, temperature 0)** để trích các trường theo một prompt và một schema Pydantic. Nghĩa là `technical_skills`, `soft_skills`, `qualifications`… là **nhãn do máy trích**, không phải nhãn người gán.

| Quan sát | Hệ quả cho dự án |
|---|---|
| Các cột kỹ năng là đầu ra của LLM | Chỉ dùng làm **nhãn yếu** cho WM2; tập test phải do nhóm tự gán nhãn. Có thể dùng chính cách trích bằng LLM của họ làm một baseline để so sánh |
| Schema gốc có `company_name`, `posting_date`, `deadline`, `url`, nhưng **file mẫu không có các cột này** (18 cột) | Nếu bản đầy đủ cũng thiếu: VietJobs không dùng được cho phân tích theo công ty hay theo thời gian, và không nối được với tin nhóm tự crawl theo URL/ID → chỉ dùng làm backfill phân bố nghề/lương/kỹ năng và làm baseline |
| Các cột danh sách lưu dạng chuỗi `"['a', 'b']"` | Phải parse (`ast.literal_eval`) khi nạp vào bronze/silver |
| `salary_min`/`salary_max` là số nguyên đã cắt (9,4 → 9); `salary_avg` lệch trung điểm (khoảng 9,4–12 ghi "10 triệu") | **Tự tính lại lương từ chuỗi `salary`** (BD làm khi backfill – ADR 0001 D2); đây là một expectation tốt cho Great Expectations |
| `location` viết thường, có tin nhiều tỉnh (`"hà nội, hồ chí minh"` – 1/5 dòng mẫu); mô tả có chữ "TP HCM (cũ)" | Tách (explode) địa điểm trước khi làm `mart_salary_role_region`; chuẩn hóa về 34 tỉnh/thành sau sắp xếp 2025 |
| `category` là 16 nhãn dạng slug (`nông_nghiệp_năng_lượng_môi_trường`), trong khi TopCV có 24 nhóm ngành | Cần bảng ánh xạ nhóm ngành TopCV → 16 nhãn VietJobs nếu muốn so sánh với baseline |
| 3/5 dòng mẫu (ngành không phải IT) không có `technical_skills` | WM2 nên tập trung vào ngành IT trước |
| Ngay trong 5 dòng đã có cặp gần trùng ("Xử Lý"/"Xử Lí" Nước Thải, cùng TP.HCM) | Có cơ sở thực tế cho bài dedup WM1 |
| Mô tả ~100 từ + yêu cầu ~80 từ mỗi tin (mẫu); bài báo nêu trung bình ~321 từ/tin | Đủ dài cho trích xuất span; kiểm tra lại trên bản đầy đủ |

Giấy phép: repo ghi MIT, bài báo ghi CC BY 4.0, trang Hugging Face chưa ghi → luôn trích dẫn bài báo LREC 2026.

## TopCV

- **Sitemap:** `sitemap/jobs.xml` là sitemap index gồm **220 file** (`jobs_0.xml` … `jobs_219.xml`), mỗi file ~200 URL → khoảng **44.000 URL tin** (có thể gồm cả tin đã hết hạn – cần kiểm tra). Mỗi URL có `<lastmod>` → **crawl tăng dần**: chỉ tải lại tin có `lastmod` mới hơn lần crawl trước. Việc này vừa giảm tải cho trang nguồn, vừa là câu chuyện "Velocity" tốt cho báo cáo Big Data.
- **Mẫu URL:** `/viec-lam/{slug-tieu-de}/{id}.html` → `id` chính là `source_job_id` (khóa Kafka).
- **Trường có sẵn trên trang tin:** mức lương (nhiều dạng, ví dụ "Từ 2 triệu"), địa điểm đến cấp **phường** + địa chỉ, kinh nghiệm, hạn nộp, cấp bậc, học vấn, số lượng tuyển, hình thức làm việc, loại hợp đồng, công ty (tên, quy mô, lĩnh vực), nhóm nghề, **"Kỹ năng cần có" do nhà tuyển dụng gắn tag**, các mục mô tả/yêu cầu/quyền lợi.
- **Không thấy** thông tin liên hệ cá nhân của người tuyển dụng trên trang đã xem – vẫn giữ bộ lọc PII ở silver.

Hệ quả: tag kỹ năng do nhà tuyển dụng gắn là **nhãn yếu tốt hơn** nhãn LLM của VietJobs cho WM2 (và là nguồn đầu tiên cho từ điển alias kỹ năng). Trang không hiển thị rõ ngày đăng → dùng `first_seen` (lần đầu crawl thấy), `lastmod` và hạn nộp để dựng vòng đời tin.

## ITviec – review công ty

- **Mỗi review có:** tháng/năm, điểm tổng 1–5 sao, **điểm theo 5 khía cạnh** (*Salary & benefits*, *Training & learning*, *Management cares about me*, *Culture & fun*, *Office & workspace*), có khuyên dùng hay không, phần **"What I liked"** và **"Suggestions for improvement"**. Người review ẩn danh, không hiện chức danh.
- **Chỉ một phần review hiện khi chưa đăng nhập** (trang có lời mời đăng nhập để xem thêm) → chỉ lấy phần công khai. Số review mỗi công ty nhỏ (ví dụ 42 với NTT Data Vietnam) → tổng khối lượng phụ thuộc số công ty crawl.

Hệ quả cho WM3:

- Lấy **5 khía cạnh của ITviec làm bộ aspect chuẩn**, thêm "cân bằng công việc/OT" nếu văn bản hay nhắc tới.
- Điểm sao theo khía cạnh và việc tách sẵn phần "thích"/"cần cải thiện" là **nhãn yếu miễn phí** (distant supervision ở mức review). Đánh giá mô hình vẫn cần nhãn người gán ở mức câu (~1.000 câu).
- Review có thể lẫn tiếng Anh và tiếng Việt → cần xử lý song ngữ (ViSoBERT/PhoBERT cho tiếng Việt, hoặc mô hình đa ngữ).

## ESCO

- CSV đơn ngữ, chọn 1 trong 28 ngôn ngữ, **không có tiếng Việt** → tải bản tiếng Anh.
- Gồm: khái niệm nghề (occupations), kỹ năng/kiến thức/năng lực (skills), quan hệ nghề–kỹ năng, kỹ năng–bằng cấp, nghề–bằng cấp.
- Hệ quả: nhóm tự xây **từ điển alias Việt → ESCO**, bắt đầu từ top ~200 tag kỹ năng IT trên TopCV.

## UIT-VSFC (sentiment tiếng Việt)

16.175 câu phản hồi của sinh viên (train/val/test = 11.426 / 1.583 / 3.166), nhãn cảm xúc 3 lớp và chủ đề 4 lớp, độ đồng thuận gán nhãn > 91% cho cảm xúc. Giấy phép ghi "unknown" → chỉ dùng để tiền huấn luyện/so sánh trong nghiên cứu, trích dẫn bài báo gốc (Nguyen et al., KSE 2018). Domain khác (giáo dục) nên chỉ là điểm khởi đầu cho ABSA review công ty.

## Tổng hợp: nguồn nào dùng vào đâu

| Nguồn | Vai trò chính | Bài toán / thành phần | Việc cần làm trước |
|---|---|---|---|
| TopCV (crawl) | Nguồn tin tuyển dụng chính, có lịch sử theo ngày | Bronze/silver, mart lương & kỹ năng, WM1, WM2 (tag kỹ năng = nhãn yếu) | Crawl thử 200 URL từ `jobs_0.xml` để đo tỉ lệ có đủ trường |
| ITviec jobs (crawl) | Nguồn thứ hai cho IT; tạo tin trùng liên trang | WM1 dedup, mart kỹ năng | Kiểm tra trường nào hiện khi chưa đăng nhập (lương thường bị ẩn) |
| ITviec reviews (crawl) | Nguồn duy nhất cho ý kiến về công ty | WM3 ABSA, UC005 | Đếm số review công khai trên ~20 công ty để ước lượng khối lượng |
| VietJobs | Backfill + baseline | Đường batch (L14), so sánh WM8 | Chạy script trên bản đầy đủ; xác nhận có/không cột company/date/url |
| ESCO | Chuẩn hóa kỹ năng | `dim_skill`, WM2 | Tải CSV tiếng Anh; dựng alias từ tag TopCV |
| UIT-VSFC / ABSA công khai | Khởi động mô hình cảm xúc | WM3 | Kiểm tra giấy phép từng bộ |
| Event generator | Tương tác người dùng (synthetic) | Streaming, WM5, NFR | Thiết kế tham số hành vi |

## Số liệu từ bài báo VietJobs (LREC 2026)

Lấy từ bài báo, chưa kiểm chứng trên bản đầy đủ.

| Mục | Giá trị |
|---|---|
| Nguồn, thời gian | Chỉ TopCV; bài báo ghi 07/2025, README GitHub ghi 07–10/2025 (chưa thống nhất) |
| Quy mô | 48.092 tin, ~15,4 triệu từ, trung bình ~321 từ/tin |
| Lương | 71,5% có khoảng lương cụ thể, 28,5% thỏa thuận; median ~10–15 triệu VND/tháng, lệch phải |
| Nhóm nghề | 16 nhóm; lớn nhất là Kinh doanh/Bán hàng/CSKH (8.276); **IT chỉ 1.906 (~4%)** |
| Baseline | Phân loại 16 nhóm: tốt nhất Qwen2.5-7B few-shot, acc 0,47, macro-F1 ~0,42. Ước lượng lương: RMSE ~10–11 triệu, R² ~0,16 |
| Giấy phép | CC BY 4.0 (bài báo), MIT (repo), chưa ghi (Hugging Face) → luôn trích dẫn |

Hệ quả: tin IT quá ít cho WM2 nên cần crawl thêm; WM8 có baseline thấp để so sánh; cột kỹ năng là nhãn do LLM sinh.

## Chiến lược dữ liệu: crawl là dữ liệu chính, VietJobs phục vụ việc khác (chốt 2026-10-12)

> Thay cho bản "hybrid – VietJobs làm nền" trước đây. Lý do: VietJobs bản đầy đủ **không có** `company_name`, `posting_date`, `url`, `deadline` (EDA 2026-10-07) nên không dùng được cho dedup giữa các trang, chi tiết tin, nối tin với review công ty, xu hướng theo thời gian và cảnh báo tin mới – đúng những chức năng chính của [blueprint](14-blueprint-he-thong.md).

**Dữ liệu chính của hệ thống** = tin tự crawl từ TopCV, ITviec (ngành IT) + review công khai ITviec, crawl đều hằng ngày đến cuối kỳ.

| Việc | Nguồn | Ghi chú |
|---|---|---|
| Mọi bảng app hiển thị (UC001, UC011, UC012, UC005, UC002, UC006) | **Crawl** | Có URL, công ty, ngày; tin VietJobs không hiện trong app |
| Dedup giữa các trang (WM1) | **Crawl** TopCV + ITviec | VietJobs chỉ một nguồn |
| Tập test WM2 (~1.000 câu, người gán) | **Crawl** TopCV | Cùng loại với dữ liệu hệ thống xử lý |
| Review công ty (WM3) | ITviec | Không có nguồn thay thế |
| Thí nghiệm batch vs streaming, độ tươi, cảnh báo (BD) | **Crawl** | Dữ liệu "sống" |
| Nhãn yếu để huấn luyện WM2 | VietJobs `technical_skills` (48k tin) | Nhãn do LLM sinh – không bao giờ dùng làm test |
| Từ điển alias kỹ năng | VietJobs (đã làm: 200 kỹ năng, 442 cách viết) | Bổ sung bằng tag TopCV khi có crawl |
| Dev set / luyện guideline WM2 | VietJobs `skill_batch1`, dừng ở ~300 câu | |
| So sánh với nghiên cứu đã công bố | VietJobs (baseline LREC 2026) | |
| Đo throughput, lag, chịu tải (BD) | VietJobs replay vào Kafka, có thể nhân bản ID | Dữ liệu crawl quá nhỏ để thử tải |
| Kiểm tra chất lượng GX (BD) | VietJobs (404 tin lệch lương – lỗi thật) | |
| Dự phòng khi bị chặn crawl | Replay VietJobs | Hệ thống vẫn chạy, nhưng UC001/UC011/UC005 nghèo dữ liệu |

**Quy tắc cho BD:** VietJobs không có ngày đăng, nên `first_seen_ts` của nó là ngày nạp. Mọi mart theo thời gian (`gold.mart_skill_demand_monthly`) và bảng app hiển thị **lọc bỏ `source = 'vietjobs'`**; `gold.mart_salary_role_region` được lấy VietJobs nếu giữ cột nguồn để lọc.

**Hạn chế phải nêu trong báo cáo:** xu hướng theo tháng chỉ có khoảng 2–3 tháng dữ liệu crawl.

### Cổng quyết định sau 1–2 tuần

- [ ] `explore/01_vietjobs_eda.py` trên bản đầy đủ: có cột company/date/url không?
- [ ] Crawl thử 200 tin TopCV (1 request/giây): tỉ lệ có lương, có tag kỹ năng, có bị chặn không?
- [ ] Đếm review công khai ITviec trên ~20 công ty.

Nếu crawl hoặc review thất bại: lùi về replay VietJobs + crawler nhỏ chạy tăng dần, thu hẹp các UC cần dữ liệu crawl, và bỏ hoặc thu hẹp WM3. Nên hỏi giảng viên Big Data về yêu cầu "dữ liệu tự thu thập" (câu 8 trong [Rủi ro và câu hỏi](11-rui-ro-va-cau-hoi.md)).

## Việc tiếp theo

- [x] Chạy `explore/01_vietjobs_eda.py` trên bản VietJobs đầy đủ (2026-10-07, kết quả `explore/out/vietjobs_eda.md`).
- [ ] Crawl thử 200 tin TopCV (1 request/giây), ghi tỉ lệ có lương, có tag kỹ năng, có địa chỉ.
- [ ] Đếm review công khai của ~20 công ty IT trên ITviec.
- [ ] Lập danh sách top 200 tag kỹ năng IT trên TopCV làm bản nháp từ điển alias.
- [ ] Cập nhật ước lượng 5V trong [Dữ liệu](02-du-lieu.md) bằng số đo thật.
