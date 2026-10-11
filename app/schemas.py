"""
app/schemas.py
Pydantic schemas định nghĩa cấu trúc dữ liệu đầu ra và xác thực API theo yêu cầu đề bài.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class StationSummary(BaseModel):
    station_id: str = Field(..., description="Mã định danh duy nhất của trạm")
    station_name: str = Field(..., description="Tên trạm")
    month: str = Field(..., description="Tháng quan sát (YYYY-MM)")
    lat: float = Field(..., description="Vĩ độ")
    lng: float = Field(..., description="Kinh độ")
    cluster: int = Field(..., description="Mã cụm K-Means (0, 1, 2)")
    cluster_label: str = Field(..., description="Tên nhãn nghiệp vụ của cụm")
    total_trips: int = Field(..., description="Tổng số chuyến đi trong tháng")


class StationDetail(StationSummary):
    morning_ratio: float = Field(..., description="Tỷ lệ xuất phát sáng (06-10h)")
    midday_ratio: float = Field(..., description="Tỷ lệ xuất phát trưa (10-16h)")
    evening_ratio: float = Field(..., description="Tỷ lệ xuất phát chiều (16-20h)")
    night_ratio: float = Field(..., description="Tỷ lệ xuất phát đêm (20-06h)")
    weekend_ratio: float = Field(..., description="Tỷ lệ chuyến vào cuối tuần")
    member_share: float = Field(..., description="Tỷ lệ người dùng hội viên (Annual Member)")
    electric_share: float = Field(..., description="Tỷ lệ sử dụng xe đạp điện")
    median_duration_min: float = Field(..., description="Thời lượng trung vị chuyến đi (phút)")
    morning_net_flow_ratio: float = Field(..., description="Tỷ lệ chênh lệch luồng vào/ra sáng")


class ClusterMedianProfile(BaseModel):
    cluster: int
    cluster_label: str
    station_count: int
    morning_ratio: float
    midday_ratio: float
    evening_ratio: float
    night_ratio: float
    weekend_ratio: float
    member_share: float
    median_duration_min: float
    morning_net_flow_ratio: float
    total_trips: float


class MetricsResponse(BaseModel):
    k_selected: int
    test_silhouette_score: float
    test_davies_bouldin_index: float
    volume_baseline_silhouette: float
    profile_kmeans_silhouette: float
    volume_vs_profile_ari: float
    seed_stability_mean_ari: float
    season_stability_ari: float
    season_stability_nmi: float
    common_stations_count: int
    cluster_medians: List[ClusterMedianProfile]


class ModelCardResponse(BaseModel):
    model_name: str
    version: str
    algorithm: str
    target_segments: List[str]
    input_features: List[str]
    geographic_constraint: str
    training_data: str
    test_data: str
    evaluation_metrics: Dict[str, Any]
    limitations: List[str]
    ethical_considerations: List[str]
