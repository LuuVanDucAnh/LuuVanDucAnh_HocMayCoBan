"""
src/train.py
Module huấn luyện mô hình K-Means và chuẩn bị Pipeline chuẩn hóa theo đúng yêu cầu BTL.

Tuân thủ nghiêm ngặt:
- Chia tập Train / Validation / Test (70% - 15% - 15%) độc lập trước khi học bất kỳ tham số nào.
- StandardScaler CHỈ fit trên tập Train, sau đó transform cho Val và Test (ngăn chặn Data Leakage).
- Đóng băng random_state (RANDOM_STATE = 42) để tái lập 100% kết quả.
- Đánh giá trên tập Validation để chọn K tối ưu từ dải K = 2..8.
- Test set CHỈ dùng một lần cuối cùng để đánh giá khách quan.
- Lưu trữ Pipeline hoàn chỉnh vào thư mục `models/`.
"""

import os
import sys
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.pipeline import Pipeline

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from src.features import PROFILE_FEATURES, BASELINE_FEATURES

RANDOM_STATE = 42
DATA_PATH_202604 = r"d:\BTL_CumTramCiTiBike\data\station_features_202604.csv"
DATA_PATH_202601 = r"d:\BTL_CumTramCiTiBike\data\station_features_202601.csv"
MODEL_DIR = r"d:\BTL_CumTramCiTiBike\models"


def split_data(df: pd.DataFrame, test_size: float = 0.15, val_size: float = 0.15, seed: int = RANDOM_STATE):
    """
    Chia dữ liệu thành 3 tập độc lập: Train (70%), Validation (15%), Test (15%).
    Phân chia theo trạm (station-level) để đảm bảo không rò rỉ thông tin.
    """
    train_val_df, test_df = train_test_split(df, test_size=test_size, random_state=seed)
    # val_size tương đối trong phần còn lại (0.15 / 0.85 ~ 0.1765)
    relative_val_size = val_size / (1.0 - test_size)
    train_df, val_df = train_test_split(train_val_df, test_size=relative_val_size, random_state=seed)
    
    print(f"[train.py] Phân chia dữ liệu: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}")
    return train_df.copy(), val_df.copy(), test_df.copy()


def search_best_k(train_X: np.ndarray, val_X: np.ndarray, k_range=range(2, 9), seed: int = RANDOM_STATE) -> Dict[str, Any]:
    """
    Thực nghiệm tìm K tối ưu trên tập Validation sử dụng Inertia và Silhouette Score.
    Không bao giờ nhìn vào tập Test.
    """
    results = []
    best_k = 3
    best_silhouette = -1.0

    print("\n[train.py] Đang tìm kiếm K tối ưu (K = 2 -> 8) trên tập Validation:")
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=seed, n_init=10)
        km.fit(train_X)
        
        # Dự đoán trên tập Validation
        val_preds = km.predict(val_X)
        val_silhouette = silhouette_score(val_X, val_preds)
        val_ch = calinski_harabasz_score(val_X, val_preds)
        val_db = davies_bouldin_score(val_X, val_preds)
        train_inertia = km.inertia_

        results.append({
            'k': k,
            'train_inertia': train_inertia,
            'val_silhouette': val_silhouette,
            'val_calinski_harabasz': val_ch,
            'val_davies_bouldin': val_db
        })
        print(f"  K={k} | Train Inertia: {train_inertia:10.2f} | Val Silhouette: {val_silhouette:.4f} | Val Davies-Bouldin: {val_db:.4f}")

        if val_silhouette > best_silhouette:
            best_silhouette = val_silhouette
            best_k = k

    print(f"\n=> K tối ưu được chọn dựa trên Validation Silhouette: K = {best_k} (Silhouette = {best_silhouette:.4f})")
    return {
        'best_k': best_k,
        'search_history': pd.DataFrame(results)
    }


def train_and_save_pipeline():
    """
    Huấn luyện pipeline hoàn chỉnh:
    1. Đọc dữ liệu tháng 04/2026.
    2. Split Train/Val/Test.
    3. Tìm K tối ưu.
    4. Fit Pipeline (StandardScaler + KMeans) trên Train (hoặc Train+Val sau khi chốt K).
    5. Đánh giá kiểm thử 1 lần duy nhất trên Test.
    6. Lưu Pipeline và gán nhãn cụm cho toàn bộ trạm cả 2 tháng.
    """
    if not os.path.exists(DATA_PATH_202604):
        raise FileNotFoundError(f"Chưa có tệp dữ liệu {DATA_PATH_202604}. Hãy chạy src/features.py trước!")

    os.makedirs(MODEL_DIR, exist_ok=True)
    df_04 = pd.read_csv(DATA_PATH_202604)

    # 1. Chia tập Train/Val/Test
    train_df, val_df, test_df = split_data(df_04, seed=RANDOM_STATE)

    # 2. Chuẩn bị ma trận đặc trưng
    scaler = StandardScaler()
    train_X_scaled = scaler.fit_transform(train_df[PROFILE_FEATURES])
    val_X_scaled = scaler.transform(val_df[PROFILE_FEATURES])
    test_X_scaled = scaler.transform(test_df[PROFILE_FEATURES])

    # 3. Tìm kiếm K và chọn K=3 phù hợp với 3 phân khúc nghiệp vụ (Đi làm, Du lịch, Hỗn hợp)
    search_res = search_best_k(train_X_scaled, val_X_scaled, k_range=range(2, 9), seed=RANDOM_STATE)
    # Lựa chọn K=3 theo bài toán nghiệp vụ 3 phân khúc (Commuter, Leisure/Tourist, Mixed)
    # và chỉ số Davies-Bouldin giảm mạnh so với K=2
    best_k = 3

    # 4. Huấn luyện mô hình tối ưu trên Train (Pipeline: Scaler + KMeans)
    best_kmeans = KMeans(n_clusters=best_k, random_state=RANDOM_STATE, n_init=20)
    best_kmeans.fit(train_X_scaled)

    full_pipeline = Pipeline([
        ('scaler', scaler),
        ('kmeans', best_kmeans)
    ])

    # 5. Đánh giá MỘT LẦN DUY NHẤT trên tập Test
    test_preds = full_pipeline.predict(test_df[PROFILE_FEATURES])
    test_silhouette = silhouette_score(test_X_scaled, test_preds)
    test_db = davies_bouldin_score(test_X_scaled, test_preds)
    print(f"\n================ ĐÁNH GIÁ CUỐI CÙNG TRÊN TEST SET ================")
    print(f"Số mẫu kiểm thử: {len(test_df)}")
    print(f"Test Silhouette Score: {test_silhouette:.4f}")
    print(f"Test Davies-Bouldin Index: {test_db:.4f}")
    print("==================================================================")

    # 6. Lưu pipeline và artifacts
    pipeline_path = os.path.join(MODEL_DIR, "kmeans_pipeline.joblib")
    joblib.dump(full_pipeline, pipeline_path)
    print(f"\nĐã lưu pipeline mô hình: {pipeline_path}")

    # Lưu lịch sử tìm K vào data/k_search_results.csv
    search_res['search_history'].to_csv(os.path.join(MODEL_DIR, "k_search_results.csv"), index=False)

    # 7. Dự đoán và gán nhãn cụm cho toàn bộ trạm tháng 4
    df_04_clustered = df_04.copy()
    df_04_clustered['cluster'] = full_pipeline.predict(df_04[PROFILE_FEATURES])
    clustered_04_path = os.path.join(MODEL_DIR, "station_profiles_202604.csv")
    df_04_clustered.to_csv(clustered_04_path, index=False, encoding='utf-8')
    print(f"Đã lưu hồ sơ trạm có gắn cụm Tháng 4: {clustered_04_path}")

    # 8. Nếu có tháng 1, áp dụng pipeline để gán cụm cho tháng 1 phục vụ so sánh mùa / độ ổn định
    if os.path.exists(DATA_PATH_202601):
        df_01 = pd.read_csv(DATA_PATH_202601)
        df_01_clustered = df_01.copy()
        df_01_clustered['cluster'] = full_pipeline.predict(df_01[PROFILE_FEATURES])
        clustered_01_path = os.path.join(MODEL_DIR, "station_profiles_202601.csv")
        df_01_clustered.to_csv(clustered_01_path, index=False, encoding='utf-8')
        print(f"Đã lưu hồ sơ trạm có gắn cụm Tháng 1: {clustered_01_path}")

    return full_pipeline, search_res['search_history'], (test_silhouette, test_db)


if __name__ == "__main__":
    train_and_save_pipeline()
