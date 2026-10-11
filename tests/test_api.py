"""
tests/test_api.py
Kiểm thử tự động API Backend FastAPI sử dụng TestClient của Starlette/FastAPI.
Đảm bảo kiểm tra schema, mã trạng thái HTTP, trường dữ liệu bắt buộc và xử lý lỗi.
"""

import sys
import os

# Thêm đường dẫn gốc vào sys.path
sys.path.insert(0, r"d:\BTL_CumTramCiTiBike")

from fastapi.testclient import TestClient
from app.main import app, load_cached_data

# Khởi động và nạp dữ liệu offline
load_cached_data()
client = TestClient(app)


def test_get_stations_april():
    """Kiểm tra lấy danh sách trạm Tháng 04/2026."""
    response = client.get("/api/stations?month=2026-04")
    assert response.status_code == 200, f"Lỗi: {response.text}"
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 2000, "Số lượng trạm tháng 4 phải lớn hơn 2000"
    
    first = data[0]
    for key in ['station_id', 'station_name', 'lat', 'lng', 'cluster', 'total_trips']:
        assert key in first, f"Thiếu trường {key} trong StationSummary"
    print(f"PASS: test_get_stations_april ({len(data)} stations)")


def test_get_stations_january():
    """Kiểm tra lấy danh sách trạm Tháng 01/2026."""
    response = client.get("/api/stations?month=2026-01")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 2000
    print(f"PASS: test_get_stations_january ({len(data)} stations)")


def test_filter_by_cluster():
    """Kiểm tra lọc theo cụm."""
    response = client.get("/api/stations?month=2026-04&cluster=1")
    assert response.status_code == 200
    data = response.json()
    assert all(st['cluster'] == 1 for st in data), "Tất cả trạm trả về phải có cluster=1"
    print(f"PASS: test_filter_by_cluster (Cluster 1 has {len(data)} stations)")


def test_get_station_detail():
    """Kiểm tra xem chi tiết 1 trạm cụ thể."""
    # Lấy 1 station_id bất kỳ
    res_list = client.get("/api/stations?month=2026-04&limit=1")
    sid = res_list.json()[0]['station_id']

    res = client.get(f"/api/station/{sid}?month=2026-04")
    assert res.status_code == 200
    detail = res.json()
    assert detail['station_id'] == sid
    assert 'morning_ratio' in detail
    assert 'member_share' in detail
    assert 'morning_net_flow_ratio' in detail
    print(f"PASS: test_get_station_detail (ID={sid}, Name={detail['station_name']})")


def test_metrics_endpoint():
    """Kiểm tra API Metrics trả về kết quả 4 thí nghiệm."""
    res = client.get("/api/metrics")
    assert res.status_code == 200
    metrics = res.json()
    assert metrics['k_selected'] == 3
    assert 'test_silhouette_score' in metrics
    assert 'season_stability_ari' in metrics
    assert len(metrics['cluster_medians']) == 3
    print("PASS: test_metrics_endpoint")


def test_model_card_endpoint():
    """Kiểm tra API Model Card."""
    res = client.get("/api/model-card")
    assert res.status_code == 200
    card = res.json()
    assert card['model_name'] == "Citi Bike Station Usage Profiler"
    assert len(card['target_segments']) == 3
    print("PASS: test_model_card_endpoint")


def test_error_handling():
    """Kiểm tra xử lý lỗi 404 và 422 hợp lý."""
    # Tháng không hợp lệ -> 404
    res_invalid_month = client.get("/api/stations?month=2099-12")
    assert res_invalid_month.status_code == 404

    # Mã cụm không hợp lệ -> 422
    res_invalid_cluster = client.get("/api/stations?cluster=99")
    assert res_invalid_cluster.status_code == 422

    # Trạm không tồn tại -> 404
    res_invalid_st = client.get("/api/station/non_existent_id?month=2026-04")
    assert res_invalid_st.status_code == 404
    print("PASS: test_error_handling (404 and 422 handled correctly)")


if __name__ == "__main__":
    print("\n--- BẮT ĐẦU CHẠY KIỂM THỬ TỰ ĐỘNG HỆ THỐNG ---")
    test_get_stations_april()
    test_get_stations_january()
    test_filter_by_cluster()
    test_get_station_detail()
    test_metrics_endpoint()
    test_model_card_endpoint()
    test_error_handling()
    print("\n=== TẤT CẢ 7 TEST CASES ĐỀU ĐẠT CHUẨN 100%! ===\n")
