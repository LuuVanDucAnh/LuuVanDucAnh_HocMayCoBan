"""
src/features.py
Module tổng hợp đặc trưng cấp trạm (Station-Level Feature Engineering).

Chuyển đổi từ dữ liệu giao dịch chuyến đi (Trip-level, hàng triệu dòng)
sang bảng hồ sơ hành vi trạm (Station-level, ~2.000 dòng).

Đặc trưng trích xuất theo đúng yêu cầu đề tài BTL:
- 4 khung giờ: Sáng (06-10h), Trưa (10-16h), Chiều (16-20h), Đêm (20-06h).
- Tỷ lệ ngày cuối tuần (weekend_ratio).
- Tỷ lệ hội viên (member_share).
- Thời lượng trung vị chuyến đi (median_duration_min).
- Tỷ lệ chênh lệch vào/ra buổi sáng (morning_net_flow_ratio).
- Tổng số chuyến (total_trips - dùng cho baseline so sánh).
- Tọa độ (lat, lng) và tên trạm (station_name) - CHỈ DÙNG BẢN ĐỒ.
"""

import os
import sys
import numpy as np
import pandas as pd
from typing import Tuple
from collections import defaultdict

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from src.data import load_and_clean_data, RAW_DIR_202604, RAW_DIR_202601


MIN_TRIPS_THRESHOLD = 30  # Ngưỡng tối thiểu 30 chuyến/tháng để đảm bảo thống kê tin cậy


def extract_station_profiles(raw_dir: str, target_month: str) -> pd.DataFrame:
    """
    Quét qua các chunks dữ liệu và tổng hợp số liệu thống kê cho từng trạm.
    Tối ưu hóa bộ nhớ RAM bằng cách tích lũy số đếm vào từ điển.
    """
    print(f"\n[features.py] Đang tổng hợp đặc trưng cấp trạm cho tháng {target_month}...")

    # Dictionary lưu trữ các chỉ số của từng start_station_id
    stats = defaultdict(lambda: {
        'names': defaultdict(int),
        'lats': [],
        'lngs': [],
        'durations': [],
        'total_starts': 0,
        'morning_starts': 0,
        'midday_starts': 0,
        'evening_starts': 0,
        'night_starts': 0,
        'weekend_starts': 0,
        'member_starts': 0,
        'electric_starts': 0,
        'morning_ends': 0,
        'total_ends': 0
    })

    # Đọc theo chunk
    for chunk in load_and_clean_data(raw_dir, target_month, chunksize=250000):
        # Thông tin thời gian
        hours = chunk['started_at'].dt.hour
        days_of_week = chunk['started_at'].dt.dayofweek  # 5, 6 là cuối tuần
        is_weekend = days_of_week >= 5
        is_member = chunk['member_casual'] == 'member'
        is_electric = chunk['rideable_type'] == 'electric_bike'

        m_mask = (hours >= 6) & (hours < 10)
        md_mask = (hours >= 10) & (hours < 16)
        ev_mask = (hours >= 16) & (hours < 20)
        n_mask = (hours >= 20) | (hours < 6)

        # Nhóm theo trạm xuất phát
        for (sid, sname), group in chunk.groupby(['start_station_id', 'start_station_name']):
            st = stats[sid]
            st['names'][sname] += len(group)
            st['total_starts'] += len(group)

            # Lấy mẫu tọa độ và thời lượng (lấy tối đa 1000 mẫu để tiết kiệm RAM mà vẫn chính xác median)
            if len(st['lats']) < 500:
                st['lats'].extend(group['start_lat'].iloc[:50].tolist())
                st['lngs'].extend(group['start_lng'].iloc[:50].tolist())
            if len(st['durations']) < 1500:
                st['durations'].extend(group['duration_sec'].iloc[:100].tolist())

            idx = group.index
            st['morning_starts'] += m_mask.loc[idx].sum()
            st['midday_starts'] += md_mask.loc[idx].sum()
            st['evening_starts'] += ev_mask.loc[idx].sum()
            st['night_starts'] += n_mask.loc[idx].sum()
            st['weekend_starts'] += is_weekend.loc[idx].sum()
            st['member_starts'] += is_member.loc[idx].sum()
            st['electric_starts'] += is_electric.loc[idx].sum()

        # Đếm lượt kết thúc (inflow) buổi sáng và tổng kết thúc
        end_chunk = chunk.dropna(subset=['end_station_id'])
        end_hours = end_chunk['ended_at'].dt.hour
        end_m_mask = (end_hours >= 6) & (end_hours < 10)

        for end_id, end_grp in end_chunk.groupby('end_station_id'):
            sid = str(end_id).strip()
            if sid in stats:
                stats[sid]['total_ends'] += len(end_grp)
                stats[sid]['morning_ends'] += end_m_mask.loc[end_grp.index].sum()

    # Tổng hợp thành DataFrame
    rows = []
    print(f"[features.py] Đang hoàn thiện bảng đặc trưng cho {len(stats)} trạm...")

    for sid, data in stats.items():
        total_s = data['total_starts']
        if total_s < MIN_TRIPS_THRESHOLD:
            continue

        # Chọn tên trạm xuất hiện nhiều nhất
        station_name = max(data['names'].items(), key=lambda x: x[1])[0]
        mean_lat = float(np.mean(data['lats'])) if data['lats'] else 0.0
        mean_lng = float(np.mean(data['lngs'])) if data['lngs'] else 0.0
        median_dur_min = float(np.median(data['durations']) / 60.0) if data['durations'] else 0.0

        # Tính các tỷ lệ hồ sơ hành vi
        morning_ratio = data['morning_starts'] / total_s
        midday_ratio = data['midday_starts'] / total_s
        evening_ratio = data['evening_starts'] / total_s
        night_ratio = data['night_starts'] / total_s

        weekend_ratio = data['weekend_starts'] / total_s
        member_share = data['member_starts'] / total_s
        electric_share = data['electric_starts'] / total_s

        # Dòng lưu lượng sáng: (kết thúc sáng - xuất phát sáng) / (tổng chuyến sáng hoặc 1)
        morning_total_activity = data['morning_ends'] + data['morning_starts']
        morning_net_flow_ratio = (
            (data['morning_ends'] - data['morning_starts']) / morning_total_activity
            if morning_total_activity > 0 else 0.0
        )

        rows.append({
            'station_id': sid,
            'station_name': station_name,
            'month': target_month,
            'lat': round(mean_lat, 6),
            'lng': round(mean_lng, 6),
            'total_trips': total_s,
            'morning_ratio': round(morning_ratio, 4),
            'midday_ratio': round(midday_ratio, 4),
            'evening_ratio': round(evening_ratio, 4),
            'night_ratio': round(night_ratio, 4),
            'weekend_ratio': round(weekend_ratio, 4),
            'member_share': round(member_share, 4),
            'electric_share': round(electric_share, 4),
            'median_duration_min': round(median_dur_min, 2),
            'morning_net_flow_ratio': round(morning_net_flow_ratio, 4)
        })

    df_features = pd.DataFrame(rows)
    print(f"[features.py] Hoàn thành! Tạo được {len(df_features)} hồ sơ trạm hợp lệ (ngưỡng >= {MIN_TRIPS_THRESHOLD} chuyến).")
    return df_features


# Danh sách các cột đặc trưng dùng để gom cụm hành vi (KHÔNG bao gồm lat, lng, name, id, volume)
PROFILE_FEATURES = [
    'morning_ratio',
    'midday_ratio',
    'evening_ratio',
    'night_ratio',
    'weekend_ratio',
    'member_share',
    'median_duration_min',
    'morning_net_flow_ratio'
]

# Baseline feature duy nhất (chỉ dùng volume tổng chuyến)
BASELINE_FEATURES = ['total_trips']


def save_features():
    """Tạo và lưu trữ sẵn dữ liệu hồ sơ trạm cho cả 2 tháng."""
    os.makedirs(r"d:\BTL_CumTramCiTiBike\data", exist_ok=True)

    # 1. Tháng 04/2026 (Chính - Mùa xuân)
    out_04 = r"d:\BTL_CumTramCiTiBike\data\station_features_202604.csv"
    if not os.path.exists(out_04):
        df_04 = extract_station_profiles(RAW_DIR_202604, "2026-04")
        df_04.to_csv(out_04, index=False, encoding='utf-8')
        print(f"Đã lưu: {out_04}")
    else:
        print(f"Tệp {out_04} đã tồn tại.")

    # 2. Tháng 01/2026 (Đối chứng - Mùa đông)
    out_01 = r"d:\BTL_CumTramCiTiBike\data\station_features_202601.csv"
    if not os.path.exists(out_01):
        df_01 = extract_station_profiles(RAW_DIR_202601, "2026-01")
        df_01.to_csv(out_01, index=False, encoding='utf-8')
        print(f"Đã lưu: {out_01}")
    else:
        print(f"Tệp {out_01} đã tồn tại.")


if __name__ == "__main__":
    save_features()
