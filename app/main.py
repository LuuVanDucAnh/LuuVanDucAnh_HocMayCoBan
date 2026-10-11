"""
app/main.py
FastAPI Web Server phục vụ API và Giao diện Ứng dụng Phân nhóm Trạm Citi Bike.

Tuân thủ yêu cầu đề tài BTL:
- Tách train offline khỏi serving: Chỉ nạp model và dữ liệu đã tiền xử lý, không train lại khi request.
- Các API bắt buộc:
  + GET /api/stations: Danh sách trạm kèm cụm, hỗ trợ lọc theo tháng và theo cụm.
  + GET /api/station/{id}: Chi tiết hồ sơ trạm theo ID và tháng.
  + GET /api/metrics: Báo cáo kết quả đánh giá 4 thí nghiệm và chỉ số học máy.
  + GET /api/model-card: Model card tài liệu hóa mô hình, giới hạn và đạo đức dữ liệu.
- Xử lý mã lỗi chuẩn (404, 422, 500) và Schema validation Pydantic.
"""

import os
import sys
import pandas as pd
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from app.schemas import (
    StationSummary,
    StationDetail,
    ClusterMedianProfile,
    MetricsResponse,
    ModelCardResponse
)

app = FastAPI(
    title="Citi Bike Station Clustering API",
    description="Hệ thống phân nhóm trạm xe đạp chia sẻ Citi Bike theo hồ sơ sử dụng - Đề tài Project 23",
    version="1.0.0"
)

# Kích hoạt CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_DIR = r"d:\BTL_CumTramCiTiBike\models"
STATIC_DIR = r"d:\BTL_CumTramCiTiBike\app\static"

# Tên nhãn nghiệp vụ diễn giải theo kết quả Thí nghiệm 4
CLUSTER_LABELS = {
    0: "Điểm đến Đi làm / Thương mại (Commercial Destination)",
    1: "Khu Dân cư Đi làm (Residential Commuter Origin)",
    2: "Trạm Hỗn hợp & Vui chơi Đêm (Mixed & Leisure/Nightlife)"
}

CLUSTER_COLORS = {
    0: "#2563EB",  # Xanh dương đậm (Commercial/Office)
    1: "#059669",  # Xanh ngọc lục bảo (Residential/Morning commute)
    2: "#D97706"   # Cam/Hổ phách (Leisure/Nightlife)
}

# Nạp dữ liệu offline vào bộ nhớ khi khởi động server
DATA_STORE = {}


@app.on_event("startup")
def load_cached_data():
    """Nạp sẵn dữ liệu hồ sơ trạm của cả 2 tháng."""
    file_04 = os.path.join(MODEL_DIR, "station_profiles_202604.csv")
    file_01 = os.path.join(MODEL_DIR, "station_profiles_202601.csv")

    if os.path.exists(file_04):
        DATA_STORE["2026-04"] = pd.read_csv(file_04)
        DATA_STORE["202604"] = DATA_STORE["2026-04"]
        print(f"[API] Đã nạp dữ liệu Tháng 04/2026: {len(DATA_STORE['2026-04'])} trạm.")
    else:
        print("[CẢNH BÁO] Chưa tìm thấy file station_profiles_202604.csv!")

    if os.path.exists(file_01):
        DATA_STORE["2026-01"] = pd.read_csv(file_01)
        DATA_STORE["202601"] = DATA_STORE["2026-01"]
        print(f"[API] Đã nạp dữ liệu Tháng 01/2026: {len(DATA_STORE['2026-01'])} trạm.")


def get_df_by_month(month: str) -> pd.DataFrame:
    """Chuẩn hóa và lấy DataFrame theo tháng."""
    clean_month = month.strip()
    if clean_month in ["202604", "04", "4"]:
        clean_month = "2026-04"
    elif clean_month in ["202601", "01", "1"]:
        clean_month = "2026-01"

    if clean_month not in DATA_STORE:
        raise HTTPException(
            status_code=404,
            detail=f"Không tìm thấy dữ liệu cho tháng '{month}'. Chỉ hỗ trợ: '2026-04' (hoặc 202604) và '2026-01' (hoặc 202601)."
        )
    return DATA_STORE[clean_month]


@app.get("/api/stations", response_model=List[StationSummary], tags=["Stations"])
def get_stations(
    month: str = Query("2026-04", description="Tháng quan sát (2026-04 hoặc 2026-01)"),
    cluster: Optional[int] = Query(None, description="Lọc theo mã cụm (0, 1, 2)"),
    limit: Optional[int] = Query(None, ge=1, le=5000, description="Giới hạn số lượng trạm trả về")
):
    """
    Lấy danh sách tất cả các trạm trong tháng cùng mã cụm và tọa độ để vẽ lên bản đồ.
    Có hỗ trợ lọc theo tháng và cụm.
    """
    df = get_df_by_month(month)
    
    if cluster is not None:
        if cluster not in [0, 1, 2]:
            raise HTTPException(status_code=422, detail="Mã cụm không hợp lệ. Chỉ chấp nhận cụm 0, 1, hoặc 2.")
        df = df[df['cluster'] == cluster]

    if limit is not None:
        df = df.head(limit)

    results = []
    for _, row in df.iterrows():
        c = int(row['cluster'])
        results.append(StationSummary(
            station_id=str(row['station_id']),
            station_name=str(row['station_name']),
            month=str(row['month']),
            lat=float(row['lat']),
            lng=float(row['lng']),
            cluster=c,
            cluster_label=CLUSTER_LABELS.get(c, f"Cụm {c}"),
            total_trips=int(row['total_trips'])
        ))
    return results


@app.get("/api/station/{station_id}", response_model=StationDetail, tags=["Stations"])
def get_station_detail(
    station_id: str,
    month: str = Query("2026-04", description="Tháng quan sát")
):
    """
    Xem chi tiết đầy đủ hồ sơ tỷ lệ và đặc trưng hành vi của một trạm cụ thể.
    """
    df = get_df_by_month(month)
    matched = df[df['station_id'].astype(str) == str(station_id).strip()]

    if matched.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Không tìm thấy trạm với ID '{station_id}' trong dữ liệu tháng {month}."
        )

    row = matched.iloc[0]
    c = int(row['cluster'])
    return StationDetail(
        station_id=str(row['station_id']),
        station_name=str(row['station_name']),
        month=str(row['month']),
        lat=float(row['lat']),
        lng=float(row['lng']),
        cluster=c,
        cluster_label=CLUSTER_LABELS.get(c, f"Cụm {c}"),
        total_trips=int(row['total_trips']),
        morning_ratio=float(row['morning_ratio']),
        midday_ratio=float(row['midday_ratio']),
        evening_ratio=float(row['evening_ratio']),
        night_ratio=float(row['night_ratio']),
        weekend_ratio=float(row['weekend_ratio']),
        member_share=float(row['member_share']),
        electric_share=float(row.get('electric_share', 0.0)),
        median_duration_min=float(row['median_duration_min']),
        morning_net_flow_ratio=float(row['morning_net_flow_ratio'])
    )


@app.get("/api/metrics", response_model=MetricsResponse, tags=["Evaluation"])
def get_evaluation_metrics():
    """
    Trả về toàn bộ các chỉ số đánh giá từ 4 thí nghiệm bắt buộc theo rubric của đề tài.
    """
    median_csv = os.path.join(MODEL_DIR, "cluster_median_profiles.csv")
    cluster_medians = []
    if os.path.exists(median_csv):
        df_med = pd.read_csv(median_csv)
        for _, r in df_med.iterrows():
            c = int(r['cluster'])
            cluster_medians.append(ClusterMedianProfile(
                cluster=c,
                cluster_label=CLUSTER_LABELS.get(c, f"Cụm {c}"),
                station_count=int(r['station_count']),
                morning_ratio=float(r['morning_ratio']),
                midday_ratio=float(r['midday_ratio']),
                evening_ratio=float(r['evening_ratio']),
                night_ratio=float(r['night_ratio']),
                weekend_ratio=float(r['weekend_ratio']),
                member_share=float(r['member_share']),
                median_duration_min=float(r['median_duration_min']),
                morning_net_flow_ratio=float(r['morning_net_flow_ratio']),
                total_trips=float(r['total_trips'])
            ))

    return MetricsResponse(
        k_selected=3,
        test_silhouette_score=0.1638,
        test_davies_bouldin_index=1.8154,
        volume_baseline_silhouette=0.5774,
        profile_kmeans_silhouette=0.1690,
        volume_vs_profile_ari=0.0115,
        seed_stability_mean_ari=0.9984,
        season_stability_ari=0.3873,
        season_stability_nmi=0.3345,
        common_stations_count=2129,
        cluster_medians=cluster_medians
    )


@app.get("/api/model-card", response_model=ModelCardResponse, tags=["Documentation"])
def get_model_card():
    """
    Trả về Model Card tiêu chuẩn phục vụ minh bạch học máy và sử dụng có trách nhiệm.
    """
    return ModelCardResponse(
        model_name="Citi Bike Station Usage Profiler",
        version="1.0.0",
        algorithm="K-Means Clustering với StandardScaler tiền xử lý",
        target_segments=[
            "Cụm 0: Điểm đến Đi làm / Thương mại (Commercial Destination Hub)",
            "Cụm 1: Khu Dân cư Đi làm (Residential Commuter Origin)",
            "Cụm 2: Trạm Hỗn hợp & Vui chơi Đêm (Mixed & Leisure/Nightlife)"
        ],
        input_features=[
            "morning_ratio (06-10h)",
            "midday_ratio (10-16h)",
            "evening_ratio (16-20h)",
            "night_ratio (20-06h)",
            "weekend_ratio (Thứ 7 & CN)",
            "member_share (Hội viên hàng năm)",
            "median_duration_min (Thời lượng trung vị)",
            "morning_net_flow_ratio (Chênh lệch luồng vào/ra sáng)"
        ],
        geographic_constraint="Tọa độ địa lý (lat, lng) KHÔNG đưa vào huấn luyện K-Means; chỉ dùng để vẽ bản đồ trực quan.",
        training_data="Tháng 04/2026 (Mùa xuân NYC) - Tập huấn luyện 1.559 trạm sau khi lọc.",
        test_data="Tập kiểm thử độc lập 335 trạm (15% split) và đối chứng mùa đông Tháng 01/2026 (2.129 trạm chung).",
        evaluation_metrics={
            "Best K": 3,
            "Test Silhouette Score": 0.1638,
            "Seed Stability ARI": 0.9984,
            "Season Stability ARI (Spring vs Winter)": 0.3873
        },
        limitations=[
            "Mô hình phân cụm không áp dụng trực tiếp cho các trạm mới mở có dưới 30 chuyến/tháng.",
            "Không dự đoán nhu cầu thời gian thực theo từng phút/giờ.",
            "Các yếu tố thời tiết cực đoan (bão tuyết, mưa lớn) có thể làm biến dạng tạm thời hồ sơ trạm."
        ],
        ethical_considerations=[
            "Tuân thủ nghiêm ngặt NYCBS Data Use Policy; không sử dụng dữ liệu định danh người dùng.",
            "Tuyệt đối không hiển thị ride_id hay lộ trình cá nhân của người sử dụng xe đạp trên giao diện.",
            "Dữ liệu được tổng hợp hoàn toàn ở cấp độ trạm để bảo vệ tối đa quyền riêng tư."
        ]
    )


# Phục vụ các biểu đồ báo cáo
REPORTS_FIGURES_DIR = r"d:\BTL_CumTramCiTiBike\reports\figures"
if os.path.exists(REPORTS_FIGURES_DIR):
    app.mount("/reports/figures", StaticFiles(directory=REPORTS_FIGURES_DIR), name="figures")

# Phục vụ thư mục static giao diện web
if os.path.exists(STATIC_DIR):
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
