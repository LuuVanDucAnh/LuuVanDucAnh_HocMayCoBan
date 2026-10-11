"""
src/data.py
Module tải và làm sạch dữ liệu thô Citi Bike Trip Histories.
Tuân thủ quy tắc minh bạch của đề bài BTL:
- Lọc các chuyến đi có thời lượng không hợp lý (< 60 giây hoặc > 86400 giây / 24 giờ).
- Lọc các chuyến bị thiếu station_id, station_name hoặc tọa độ hợp lệ.
- Lọc đúng phạm vi thời gian của tháng (loại các chuyến ngoại lai khác tháng).
"""

import os
import sys
import glob
import pandas as pd
from typing import Generator, List, Optional
from tqdm import tqdm

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


RAW_DIR_202604 = r"d:\BTL_CumTramCiTiBike\202604-citibike-tripdata"
RAW_DIR_202601 = r"d:\BTL_CumTramCiTiBike\202601-citibike-tripdata"

# Định nghĩa phạm vi tọa độ New York City hợp lệ (loại bỏ trạm test tọa độ 0,0)
NYC_LAT_MIN, NYC_LAT_MAX = 40.50, 41.00
NYC_LNG_MIN, NYC_LNG_MAX = -74.25, -73.70

COLUMNS_TO_USE = [
    'ride_id', 'rideable_type', 'started_at', 'ended_at',
    'start_station_name', 'start_station_id',
    'end_station_name', 'end_station_id',
    'start_lat', 'start_lng', 'end_lat', 'end_lng',
    'member_casual'
]


def get_csv_files(raw_dir: str) -> List[str]:
    """Lấy danh sách các tệp CSV trong thư mục theo thứ tự."""
    files = sorted(glob.glob(os.path.join(raw_dir, "*.csv")))
    if not files:
        raise FileNotFoundError(f"Không tìm thấy file CSV nào trong thư mục {raw_dir}")
    return files


def clean_trip_chunk(df: pd.DataFrame, target_month: str) -> pd.DataFrame:
    """
    Làm sạch một chunk dữ liệu chuyến đi:
    1. Chuyển đổi started_at, ended_at sang datetime.
    2. Lọc thời lượng chuyến đi hợp lý: 60s <= duration <= 86400s (24 giờ).
    3. Lọc đúng target_month (ví dụ '2026-04' hoặc '2026-01').
    4. Lọc bỏ các bản ghi khuyết start_station_id hoặc start coordinates.
    5. Giới hạn tọa độ trong phạm vi New York City.
    """
    # 1. Chuyển đổi datetime
    df['started_at'] = pd.to_datetime(df['started_at'], errors='coerce')
    df['ended_at'] = pd.to_datetime(df['ended_at'], errors='coerce')
    df = df.dropna(subset=['started_at', 'ended_at'])

    # 2. Tính thời lượng chuyến đi (giây)
    duration_sec = (df['ended_at'] - df['started_at']).dt.total_seconds()
    valid_duration = (duration_sec >= 60) & (duration_sec <= 86400)
    df = df[valid_duration].copy()
    df['duration_sec'] = duration_sec[valid_duration]

    # 3. Lọc đúng tháng mục tiêu
    month_str = df['started_at'].dt.strftime('%Y-%m')
    df = df[month_str == target_month]

    # 4. Kiểm tra trường bắt buộc
    df = df.dropna(subset=['start_station_id', 'start_station_name', 'start_lat', 'start_lng'])

    # 5. Kiểm tra tọa độ NYC
    valid_coords = (
        (df['start_lat'] >= NYC_LAT_MIN) & (df['start_lat'] <= NYC_LAT_MAX) &
        (df['start_lng'] >= NYC_LNG_MIN) & (df['start_lng'] <= NYC_LNG_MAX)
    )
    df = df[valid_coords]

    # Chuẩn hóa kiểu dữ liệu
    df['start_station_id'] = df['start_station_id'].astype(str).str.strip()
    return df


def load_and_clean_data(raw_dir: str, target_month: str, chunksize: int = 250000) -> Generator[pd.DataFrame, None, None]:
    """
    Đọc và làm sạch dữ liệu theo cơ chế generator/chunking để tối ưu bộ nhớ RAM
    khi xử lý hàng triệu bản ghi.
    """
    csv_files = get_csv_files(raw_dir)
    print(f"\n[data.py] Bắt đầu đọc {len(csv_files)} files từ {raw_dir} cho tháng {target_month}...")

    for file_path in csv_files:
        print(f"  -> Đang xử lý: {os.path.basename(file_path)}")
        for chunk in pd.read_csv(file_path, usecols=COLUMNS_TO_USE, chunksize=chunksize, low_memory=False):
            cleaned = clean_trip_chunk(chunk, target_month)
            if not cleaned.empty:
                yield cleaned


if __name__ == "__main__":
    # Test thử trên 1 chunk nhỏ của tháng 4
    sample_files = get_csv_files(RAW_DIR_202604)
    print("Files 2026-04:", sample_files)
    sample_gen = load_and_clean_data(RAW_DIR_202604, "2026-04", chunksize=10000)
    first_chunk = next(sample_gen)
    print(f"Sample chunk cleaned shape: {first_chunk.shape}")
    print(first_chunk[['started_at', 'duration_sec', 'start_station_name', 'member_casual']].head())
