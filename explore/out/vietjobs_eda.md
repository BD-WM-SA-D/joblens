# VietJobs – báo cáo khám phá nhanh

Số dòng: 48,092 · Số cột: 18

## Cột và tỉ lệ thiếu

| Cột | Kiểu | % thiếu |
|---|---|---|
| `job_title` | str | 0.0% |
| `location` | str | 0.0% |
| `country` | str | 0.0% |
| `qualifications` | str | 0.8% |
| `technical_skills` | str | 13.4% |
| `soft_skills` | str | 5.5% |
| `languages_required` | str | 74.4% |
| `experience_required` | str | 0.0% |
| `salary` | str | 0.0% |
| `contract_type` | str | 0.0% |
| `working_hours` | str | 10.4% |
| `benefits` | str | 0.1% |
| `description` | str | 0.0% |
| `requirements_text` | str | 0.0% |
| `category` | str | 0.0% |
| `salary_min` | int64 | 0.0% |
| `salary_max` | int64 | 0.0% |
| `salary_avg` | str | 0.0% |

> Không có các cột: company_name, posting_date, url, deadline → không làm được phân tích theo công ty/thời gian từ VietJobs.


## Lương (tính lại từ chuỗi gốc)

| Dạng | Số tin |
|---|---|
| range | 32,131 |
| fixed | 15,961 |

Số tin mà `salary_min` khác giá trị tính lại (do làm tròn/cắt số): 404
Số tin mà `salary_avg` lệch > 0,5 triệu so với trung điểm khoảng lương: 557 → nên tự tính lại, không dùng cột này.

Mức giữa khoảng lương (triệu VND): median 13.5, p10 8.5, p90 24.0

## Địa điểm

Tin có nhiều địa điểm: 6.0%. Top 10:

- hà nội: 19,780
- hồ chí minh: 17,136
- hà đông: 1,215
- hải phòng: 1,125
- bắc ninh: 1,104
- đà nẵng: 1,094
- hưng yên: 805
- đồng nai: 682
- tây ninh: 564
- ninh bình: 522

## `category` (top 10)

- kinh_doanh_bán_hàng_chăm_sóc_khách_hàng: 8,276
- sản_xuất_lao_động_phổ_thông_cơ_khí: 6,407
- marketing_truyền_thông_quảng_cáo_nội_dung: 5,950
- tài_chính_kế_toán_ngân_hàng_bảo_hiểm: 5,530
- du_lịch_nhà_hàng_khách_sạn_dịch_vụ: 4,243
- thiết_kế_nghệ_thuật_giải_trí_truyền_hình_báo_chí: 3,465
- nhân_sự_hành_chính_pháp_chế_tư_vấn: 3,276
- xây_dựng_kiến_trúc_bất_động_sản: 2,811
- công_nghệ_thông_tin_kỹ_thuật_số: 1,906
- logistics_vận_tải_chuỗi_cung_ứng: 1,813

## `contract_type` (top 10)

- Toàn thời gian: 46,058
- Bán thời gian: 874
- Thực tập: 822
- Khác: 165
- Thời vụ: 92
- Cộng tác viên: 54
- Toàn thời gian, Bán thời gian: 16
- Toàn thời gian, Thực tập: 10
- Thời vụ, Cộng tác viên: 1

## `experience_required` (top 10)

- 1 năm: 15,372
- Không yêu cầu: 12,345
- 2 năm: 9,781
- 3 năm: 5,595
- 6 tháng: 2,258
- 5 năm: 1,934
- 4 năm: 399
- 3 tháng: 142
- 7 năm: 91
- 10 năm: 64

## Kỹ năng (nhãn do LLM trích – coi là nhãn yếu)

Tin có `technical_skills`: 86.4%
Số kỹ năng khác nhau (chưa chuẩn hóa): 30,430. Top 20:

- excel: 2,698
- autocad: 2,392
- photoshop: 2,316
- tin học văn phòng: 1,719
- kỹ năng giao tiếp: 1,544
- capcut: 1,197
- word: 1,035
- illustrator: 977
- kỹ năng đàm phán: 909
- canva: 826
- thành thạo tin học văn phòng: 814
- after effects: 778
- sketchup: 727
- adobe premiere: 706
- premiere: 674
- adobe photoshop: 646
- kỹ năng bán hàng: 641
- revit: 582
- tin học văn phòng (word, excel, powerpoint): 565
- powerpoint: 563

`description`: trung bình 134 từ, median 114, p95 293

`requirements_text`: trung bình 83 từ, median 76, p95 159

## Gần trùng (khóa thô: tiêu đề chuẩn hóa + địa điểm)

Tỉ lệ tin nằm trong nhóm trùng khóa: 71.7% – cần MinHash trên nội dung để tách tin đăng lại thật sự với tin khác nhau cùng tiêu đề.
