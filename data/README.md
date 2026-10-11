# HỒ SƠ DỮ LIỆU (DATA DOCUMENTATION & DATA DICTIONARY)

**Dự án:** Project 23 — Phân nhóm trạm Citi Bike theo hồ sơ sử dụng  
**Học phần:** Học máy cơ bản (PGS.TS. Nguyễn Văn Hậu)  
**Tập dữ liệu:** Citi Bike Trip Histories (New York City)  

---

## 1. Nguồn Dữ Liệu & Giấy Phép Sử Dụng (Data License)

- **Trang dữ liệu chính thức:** [https://citibikenyc.com/system-data](https://citibikenyc.com/system-data)
- **Chính sách sử dụng dữ liệu (Data Sharing Policy):** [https://ride.citibikenyc.com/data-sharing-policy](https://ride.citibikenyc.com/data-sharing-policy)
- **Đơn vị vận hành:** NYCBS LLC (Bicycle Share Systems, New York City).
- **Phạm vi cấp phép:** Dữ liệu mở phục vụ nghiên cứu học thuật, giáo dục và phi thương mại.
- **Tuân thủ đạo đức & quyền riêng tư (Responsible AI):**
  - Không suy luận hành trình cá nhân của người sử dụng xe đạp.
  - Tuyệt đối không lưu trữ hoặc hiển thị trường định danh `ride_id` trên ứng dụng web giao diện.
  - Toàn bộ dữ liệu phân tích đều được tổng hợp ở cấp độ trạm (`station_id`).

---

## 2. Các Tập Dữ Liệu Sử Dụng Trong Dự Án

Dự án chọn **2 tháng hoàn chỉnh đối chứng mùa** (Mùa xuân vs Mùa đông) theo khuyến nghị của đề bài:

| Tập dữ liệu | Thư mục lưu trữ | Số tệp thô | Kích thước | Tổng số chuyến đi thô | Số trạm hợp lệ (>= 30 chuyến) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Tháng 04/2026 (Mùa Xuân)** | `202604-citibike-tripdata/` | 4 CSVs | ~719 MB | 3.860.371 | **2.229 trạm** |
| **Tháng 01/2026 (Mùa Đông)** | `202601-citibike-tripdata/` | 2 CSVs | ~354 MB | 1.816.391 | **2.143 trạm** |

---

## 3. Data Dictionary (Từ Điển Dữ Liệu)

### A. Dữ liệu thô cấp chuyến đi (Trip-level raw data)
| Tên cột | Kiểu dữ liệu | Vai trò | Đơn vị | Mô tả |
| :--- | :--- | :--- | :--- | :--- |
| `ride_id` | String | Identifier | Mã chuyến | Mã chuyến duy nhất (chỉ dùng nội bộ, cấm public) |
| `rideable_type` | String | Feature | Phân loại | Loại xe: `classic_bike` (cơ) hoặc `electric_bike` (điện) |
| `started_at` | Datetime | Feature | YYYY-MM-DD HH:MM:SS | Thời điểm mở khóa xe xuất phát |
| `ended_at` | Datetime | Feature | YYYY-MM-DD HH:MM:SS | Thời điểm trả khóa xe vào trạm kết thúc |
| `start_station_name`| String | Metadata | Text | Tên địa danh của trạm xuất phát |
| `start_station_id` | String | Station ID | Mã trạm | Mã định danh trạm xuất phát |
| `end_station_name` | String | Metadata | Text | Tên địa danh của trạm kết thúc |
| `end_station_id` | String | Station ID | Mã trạm | Mã định danh trạm kết thúc |
| `start_lat`, `start_lng`| Float | Geo Coordinates | Độ thập phân | Tọa độ địa lý trạm (CHỈ dùng vẽ bản đồ) |
| `member_casual` | String | Feature | Phân loại | Loại người dùng: `member` (hội viên) hoặc `casual` (vãng lai) |

### B. Dữ liệu tổng hợp cấp trạm (Station-level Aggregated Features - Lưu tại `data/station_features_*.csv`)
Đơn vị quan sát của bài toán học máy là: **Một trạm trong một tháng**.

| Tên biến | Kiểu | Vai trò | Miền giá trị | Mô tả nghiệp vụ |
| :--- | :---: | :---: | :---: | :--- |
| `station_id` | String | ID | Text | Khóa chính của trạm |
| `station_name` | String | Metadata | Text | Tên địa danh trạm (không đưa vào K-Means) |
| `lat`, `lng` | Float | Metadata | [40.50, 41.00], [-74.25, -73.70] | Tọa độ trạm (CHỈ dùng vẽ bản đồ) |
| `total_trips` | Integer | Baseline | >= 30 | Tổng số chuyến xuất phát (dùng cho Baseline Volume) |
| `morning_ratio` | Float | Feature | [0.0, 1.0] | Tỷ lệ xuất phát giờ cao điểm sáng (06:00 - 10:00) |
| `midday_ratio` | Float | Feature | [0.0, 1.0] | Tỷ lệ xuất phát khung giờ trưa (10:00 - 16:00) |
| `evening_ratio` | Float | Feature | [0.0, 1.0] | Tỷ lệ xuất phát giờ cao điểm chiều/tan sở (16:00 - 20:00) |
| `night_ratio` | Float | Feature | [0.0, 1.0] | Tỷ lệ xuất phát khung giờ đêm (20:00 - 06:00) |
| `weekend_ratio` | Float | Feature | [0.0, 1.0] | Tỷ lệ chuyến vào Thứ 7 & Chủ Nhật |
| `member_share` | Float | Feature | [0.0, 1.0] | Tỷ lệ người dùng là hội viên năm (`member`) |
| `electric_share` | Float | Feature | [0.0, 1.0] | Tỷ lệ người dùng xe đạp điện |
| `median_duration_min` | Float | Feature | [1.0, 120.0] | Thời lượng trung vị chuyến đi (phút) |
| `morning_net_flow_ratio`| Float | Feature | [-1.0, 1.0] | Chênh lệch (Chuyến đến - Chuyến đi) sáng / Tổng hoạt động |
| `cluster` | Integer | Target Output| {0, 1, 2} | Nhãn cụm K-Means dự đoán |

---

## 4. Báo Cáo Chất Lượng Dữ Liệu & Quy Tắc Tiền Xử Lý Minh Bạch

Để đảm bảo tính trung thực học thuật và chất lượng dữ liệu:
1. **Lọc thời lượng không hợp lý:**
   - Loại các chuyến đi `< 60 giây` (thường do người dùng đổi xe lỗi hoặc bấm nhầm mở khóa).
   - Loại các chuyến đi `> 86.400 giây` (24 giờ - thường do quên trả xe hoặc lỗi chốt khóa trạm).
2. **Lọc ngoại lệ tọa độ & Trạm bảo trì:**
   - Chỉ giữ tọa độ trong khung NYC: Vĩ độ `[40.50, 41.00]`, Kinh độ `[-74.25, -73.70]`.
   - Loại các chuyến bị khuyết `start_station_id` (chỉ chiếm ~0.05% tổng số dòng).
3. **Lọc ngày ngoại lai ngoài tháng:**
   - Tháng 1/2026 có 266 chuyến rơi vào ngày 30-31/12/2025 do lệch múi giờ UTC, đã được lọc sạch.
4. **Ngưỡng kích thước mẫu tối thiểu:**
   - Chỉ giữ các trạm có `total_trips >= 30 chuyến/tháng` (ít nhất 1 chuyến/ngày) để các tỷ lệ xác suất thống kê ổn định và đáng tin cậy.

---

## 5. Hướng Dẫn Tái Tạo Dữ Liệu (Script Execution)

Theo quy định rubric, các file CSV lớn (>100MB) không đưa lên Git. Để tái tạo lại toàn bộ file hồ sơ đặc trưng:
```bash
# Kích hoạt môi trường
.venv\Scripts\activate

# Chạy tạo đặc trưng cấp trạm từ dữ liệu thô
python -m src.features
```
Kết quả được xuất ra tự động tại `data/station_features_202604.csv` và `data/station_features_202601.csv`.
