"""
src/generate_ch4_figures.py
Tạo 4 đồ thị chất lượng cao cho Chương 4:
- fig4_1_architecture.png: Sơ đồ kiến trúc Serving phân tách Offline Training & Online Serving.
- fig4_2_screen1_intro.png: Thiết kế cấu trúc Giao diện Màn hình 1 (Tổng quan & Model Card).
- fig4_3_screen2_map.png: Thiết kế cấu trúc Giao diện Màn hình 2 (Bản đồ tương tác Leaflet & Profile Trạm).
- fig4_4_screen3_dashboard.png: Thiết kế cấu trúc Giao diện Màn hình 3 (Dashboard 4 Thí nghiệm & Metrics).
"""

import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

FIG_DIR = r"d:\BTL_CumTramCiTiBike\reports\figures"
os.makedirs(FIG_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 300


def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    # Tiêu đề
    ax.text(50, 95, "KIẾN TRÚC HỆ THỐNG SERVING PHÂN TÁCH OFFLINE VÀ ONLINE",
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1E293B')

    # Khối 1: Offline Training
    rect_offline = patches.FancyBboxPatch((4, 25), 42, 62, boxstyle="round,pad=2",
                                          ec="#3B82F6", fc="#EFF6FF", lw=2, linestyle='--')
    ax.add_patch(rect_offline)
    ax.text(25, 83, "1. OFFLINE TRAINING PIPELINE", ha='center', va='center',
            fontsize=11, fontweight='bold', color="#1D4ED8")

    box_data = patches.FancyBboxPatch((8, 65), 34, 12, boxstyle="round,pad=1", ec="#93C5FD", fc="#FFFFFF", lw=1.5)
    ax.add_patch(box_data)
    ax.text(25, 71, "Citi Bike Raw Data (5.67M trips)\nTháng 04/2026 & Tháng 01/2026", ha='center', va='center', fontsize=9)

    box_feat = patches.FancyBboxPatch((8, 47), 34, 12, boxstyle="round,pad=1", ec="#93C5FD", fc="#FFFFFF", lw=1.5)
    ax.add_patch(box_feat)
    ax.text(25, 53, "Feature Engineering (src/features.py)\n8 Tỷ lệ hành vi giờ giấc / hội viên", ha='center', va='center', fontsize=9)

    box_train = patches.FancyBboxPatch((8, 29), 34, 12, boxstyle="round,pad=1", ec="#93C5FD", fc="#FFFFFF", lw=1.5)
    ax.add_patch(box_train)
    ax.text(25, 35, "StandardScaler + K-Means (K=3)\nSplit: Train 70% | Val 15% | Test 15%", ha='center', va='center', fontsize=9)

    # Mũi tên giữa các khối Offline
    ax.annotate('', xy=(25, 65), xytext=(25, 59), arrowprops=dict(arrowstyle="->", color="#3B82F6", lw=1.5))
    ax.annotate('', xy=(25, 47), xytext=(25, 41), arrowprops=dict(arrowstyle="->", color="#3B82F6", lw=1.5))

    # Khối Lưu trữ ở giữa
    rect_store = patches.FancyBboxPatch((42, 3), 16, 18, boxstyle="round,pad=1", ec="#10B981", fc="#ECFDF5", lw=2)
    ax.add_patch(rect_store)
    ax.text(50, 12, "MODELS & ARTIFACTS\nkmeans_pipeline.joblib\nstation_profiles_*.csv", ha='center', va='center',
            fontsize=8.5, fontweight='bold', color="#047857")

    # Mũi tên xuống Model Store
    ax.annotate('', xy=(38, 29), xytext=(45, 21), arrowprops=dict(arrowstyle="->", color="#10B981", lw=2))

    # Khối 2: Online Serving
    rect_online = patches.FancyBboxPatch((54, 25), 42, 62, boxstyle="round,pad=2",
                                         ec="#8B5CF6", fc="#F5F3FF", lw=2)
    ax.add_patch(rect_online)
    ax.text(75, 83, "2. ONLINE SERVING ARCHITECTURE", ha='center', va='center',
            fontsize=11, fontweight='bold', color="#6D28D9")

    box_cache = patches.FancyBboxPatch((58, 65), 34, 12, boxstyle="round,pad=1", ec="#C4B5FD", fc="#FFFFFF", lw=1.5)
    ax.add_patch(box_cache)
    ax.text(75, 71, "In-Memory Cache (FastAPI Startup)\nNạp sẵn profiles trạm cả 2 tháng", ha='center', va='center', fontsize=9)

    box_api = patches.FancyBboxPatch((58, 47), 34, 12, boxstyle="round,pad=1", ec="#C4B5FD", fc="#FFFFFF", lw=1.5)
    ax.add_patch(box_api)
    ax.text(75, 53, "REST API Endpoints\nGET /api/stations | GET /api/metrics\nPydantic Schemas & Error Handling", ha='center', va='center', fontsize=9)

    box_ui = patches.FancyBboxPatch((58, 29), 34, 12, boxstyle="round,pad=1", ec="#C4B5FD", fc="#FFFFFF", lw=1.5)
    ax.add_patch(box_ui)
    ax.text(75, 35, "Frontend UI (HTML/CSS/JS)\nBản đồ Leaflet.js • Bộ lọc tháng/cụm\n3 Màn hình tương tác cao cấp", ha='center', va='center', fontsize=9)

    # Mũi tên từ Model Store lên Cache
    ax.annotate('', xy=(55, 21), xytext=(62, 65), arrowprops=dict(arrowstyle="->", color="#8B5CF6", lw=2, linestyle=':'))
    ax.annotate('', xy=(75, 65), xytext=(75, 59), arrowprops=dict(arrowstyle="->", color="#8B5CF6", lw=1.5))
    ax.annotate('', xy=(75, 47), xytext=(75, 41), arrowprops=dict(arrowstyle="<->", color="#8B5CF6", lw=1.5))

    out_file = os.path.join(FIG_DIR, "fig4_1_architecture.png")
    plt.tight_layout()
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()
    print(f"Đã tạo: {out_file}")


def create_ui_screen1():
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    # Frame màn hình
    ax.add_patch(patches.FancyBboxPatch((2, 2), 96, 96, boxstyle="round,pad=1", ec="#334155", fc="#0F172A", lw=2))
    # Header bar
    ax.add_patch(patches.Rectangle((2, 85), 96, 13, fc="#1E293B"))
    ax.text(8, 91.5, "🚲 CitiBike Profiler - Phân Nhóm Cụm Trạm", color="#FFFFFF", fontsize=11, fontweight='bold', va='center')
    ax.text(60, 91.5, "[ Tab 1: Giới thiệu ]   Tab 2: Bản đồ   Tab 3: Dashboard", color="#38BDF8", fontsize=9, va='center')

    # Hero Banner
    ax.add_patch(patches.FancyBboxPatch((6, 62), 88, 19, boxstyle="round,pad=1", ec="#1E3A8A", fc="#172554"))
    ax.text(50, 74, "NHẬN BIẾT TRẠM ĐI LÀM, DU LỊCH & HỖN HỢP TỪ MẪU SỬ DỤNG THỰC TẾ",
            color="#FFFFFF", fontsize=10.5, fontweight='bold', ha='center')
    ax.text(50, 67, "Học máy không giám sát K-Means (K=3) • Quy tắc địa lý: Tọa độ chỉ dùng vẽ bản đồ • Anti-Leakage Split",
            color="#94A3B8", fontsize=8.5, ha='center')

    # 3 Cards
    cards_data = [
        (6, "CỤM 0: THƯƠNG MẠI", "#2563EB", "Điểm đến làm việc\nNet Sáng: +31.87%\nTan sở chiều: 38.42%\nCuối tuần: 17.43%"),
        (37, "CỤM 1: DÂN CƯ ĐI LÀM", "#059669", "Xuất phát đi làm sáng\nSáng ra: 23.33%\nNet Sáng: -36.84%\nHội viên: 84.87%"),
        (68, "CỤM 2: HỖN HỢP & ĐÊM", "#D97706", "Giải trí & Du lịch\nĐêm: 21.88%\nCuối tuần: 23.46%\nThời lượng chuyến dài")
    ]
    for x, title, color, desc in cards_data:
        ax.add_patch(patches.FancyBboxPatch((x, 10), 26, 48, boxstyle="round,pad=1", ec=color, fc="#1E293B", lw=1.5))
        ax.add_patch(patches.Rectangle((x, 50), 26, 8, fc=color))
        ax.text(x + 13, 54, title, color="#FFFFFF", fontsize=8.5, fontweight='bold', ha='center', va='center')
        ax.text(x + 13, 30, desc, color="#E2E8F0", fontsize=8, ha='center', va='center', multialignment='center')

    out_file = os.path.join(FIG_DIR, "fig4_2_screen1_intro.png")
    plt.tight_layout()
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()
    print(f"Đã tạo: {out_file}")


def create_ui_screen2():
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    # Frame
    ax.add_patch(patches.FancyBboxPatch((2, 2), 96, 96, boxstyle="round,pad=1", ec="#334155", fc="#0B0F19", lw=2))
    # Header bar
    ax.add_patch(patches.Rectangle((2, 86), 96, 12, fc="#111827"))
    ax.text(8, 92, "🚲 CitiBike Profiler", color="#FFFFFF", fontsize=11, fontweight='bold', va='center')
    ax.text(60, 92, "Tab 1: Giới thiệu   [ Tab 2: Bản đồ trạm NYC ]   Tab 3: Dashboard", color="#38BDF8", fontsize=9, va='center')

    # Sidebar trái (Controls & Profile)
    ax.add_patch(patches.FancyBboxPatch((5, 6), 28, 77, boxstyle="round,pad=1", ec="#1E293B", fc="#111827"))
    ax.text(19, 79, "BỘ LỌC & TÌM KIẾM", color="#FFFFFF", fontsize=9, fontweight='bold', ha='center')
    ax.add_patch(patches.Rectangle((7, 68), 24, 7, fc="#1E293B"))
    ax.text(9, 71.5, "📅 Tháng: 04/2026 (2.229 trạm)", color="#93C5FD", fontsize=7.5, va='center')
    ax.add_patch(patches.Rectangle((7, 59), 24, 7, fc="#1E293B"))
    ax.text(9, 62.5, "🎯 Cụm: Tất cả các cụm (K=3)", color="#A7F3D0", fontsize=7.5, va='center')
    ax.add_patch(patches.Rectangle((7, 50), 24, 7, fc="#1E293B"))
    ax.text(9, 53.5, "🔍 Tìm trạm: 'Broadway, 7293...'", color="#CBD5E1", fontsize=7.5, va='center')

    # Station Profile Card ở Sidebar
    ax.add_patch(patches.FancyBboxPatch((7, 9), 24, 38, boxstyle="round,pad=1", ec="#3B82F6", fc="#1E293B", lw=1.2))
    ax.text(19, 43, "STATION PROFILE CARD", color="#60A5FA", fontsize=8, fontweight='bold', ha='center')
    ax.text(19, 38, "E 88 St & Park Ave", color="#FFFFFF", fontsize=8.5, fontweight='bold', ha='center')
    ax.text(19, 33, "ID: 7293.10 • Cụm 1 (Dân cư)", color="#94A3B8", fontsize=7.5, ha='center')
    ax.text(9, 26, "• Sáng (Out): 23.3% [████░░]", color="#E2E8F0", fontsize=7)
    ax.text(9, 21, "• Chiều (Out): 28.5% [█████░]", color="#E2E8F0", fontsize=7)
    ax.text(9, 16, "• Member: 84.8% [██████]", color="#10B981", fontsize=7)
    ax.text(9, 11, "• Net Sáng: -36.8% [Dân cư]", color="#F43F5E", fontsize=7)

    # Bản đồ Leaflet giả lập bên phải
    ax.add_patch(patches.FancyBboxPatch((35, 6), 61, 77, boxstyle="round,pad=1", ec="#1E293B", fc="#0F172A"))
    ax.text(65, 80, "BẢN ĐỒ TƯƠNG TÁC THÀNH PHỐ NEW YORK (LEAFLET.JS)", color="#FFFFFF", fontsize=9, fontweight='bold', ha='center')

    # Vẽ các cụm điểm giả lập Manhattan, Brooklyn, Queens
    import numpy as np
    np.random.seed(42)
    # Cụm 0 (Midtown - Commercial - Blue)
    c0_x = np.random.normal(63, 4, 35)
    c0_y = np.random.normal(52, 6, 35)
    ax.scatter(c0_x, c0_y, c='#3B82F6', s=45, alpha=0.85, edgecolors='white', linewidths=0.5, label='Cụm 0: Thương mại')

    # Cụm 1 (Residential - Upper Manhattan & Brooklyn - Green)
    c1_x = np.random.normal(54, 5, 50)
    c1_y = np.random.normal(32, 7, 50)
    ax.scatter(c1_x, c1_y, c='#10B981', s=45, alpha=0.85, edgecolors='white', linewidths=0.5, label='Cụm 1: Dân cư đi làm')

    # Cụm 2 (Leisure/Nightlife - Parks & Waterfront - Amber)
    c2_x = np.random.normal(74, 5, 40)
    c2_y = np.random.normal(44, 8, 40)
    ax.scatter(c2_x, c2_y, c='#F59E0B', s=45, alpha=0.85, edgecolors='white', linewidths=0.5, label='Cụm 2: Hỗn hợp & Giải trí')

    ax.legend(loc='lower right', facecolor='#1E293B', edgecolor='#334155', labelcolor='#FFFFFF', fontsize=7.5)

    out_file = os.path.join(FIG_DIR, "fig4_3_screen2_map.png")
    plt.tight_layout()
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()
    print(f"Đã tạo: {out_file}")


def create_ui_screen3():
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    # Frame
    ax.add_patch(patches.FancyBboxPatch((2, 2), 96, 96, boxstyle="round,pad=1", ec="#334155", fc="#0B0F19", lw=2))
    # Header bar
    ax.add_patch(patches.Rectangle((2, 86), 96, 12, fc="#111827"))
    ax.text(8, 92, "🚲 CitiBike Profiler", color="#FFFFFF", fontsize=11, fontweight='bold', va='center')
    ax.text(60, 92, "Tab 1: Giới thiệu   Tab 2: Bản đồ   [ Tab 3: Dashboard & Model Card ]", color="#38BDF8", fontsize=9, va='center')

    # 4 Metric Cards
    m_boxes = [
        (6, "K TỐI ƯU", "3 CỤM", "Phân khúc nghiệp vụ"),
        (28, "TEST SILHOUETTE", "0.1638", "Đánh giá 1 lần duy nhất"),
        (51, "SEED STABILITY", "ARI = 0.9984", "Ổn định qua 5 seeds"),
        (74, "SEASON STABILITY", "ARI = 0.3873", "2.129 trạm chung")
    ]
    for x, t, num, sub in m_boxes:
        ax.add_patch(patches.FancyBboxPatch((x, 66), 20, 16, boxstyle="round,pad=1", ec="#1E293B", fc="#1E293B"))
        ax.text(x + 10, 78, t, color="#94A3B8", fontsize=7, fontweight='bold', ha='center')
        ax.text(x + 10, 73, num, color="#38BDF8", fontsize=9.5, fontweight='bold', ha='center')
        ax.text(x + 10, 68, sub, color="#64748B", fontsize=6.5, ha='center')

    # Khối Model Card bên dưới
    ax.add_patch(patches.FancyBboxPatch((6, 6), 88, 55, boxstyle="round,pad=1", ec="#3B82F6", fc="#111827", lw=1.5))
    ax.text(50, 56, "📋 MODEL CARD: CITI BIKE STATION USAGE PROFILER v1.0", color="#FFFFFF", fontsize=10, fontweight='bold', ha='center')
    ax.text(10, 47, "• Thuật toán: K-Means (StandardScaler tiền xử lý) | Huấn luyện trên 1.559 trạm tập Train.", color="#CBD5E1", fontsize=8)
    ax.text(10, 40, "• 8 Đặc trưng: morning_ratio, midday_ratio, evening_ratio, night_ratio, weekend_ratio, member_share, duration, flow.", color="#CBD5E1", fontsize=8)
    ax.text(10, 33, "• Ràng buộc địa lý: Tọa độ địa lý (lat, lng) KHÔNG đưa vào vector K-Means; chỉ dùng hiển thị bản đồ trực quan.", color="#FCD34D", fontsize=8)
    ax.text(10, 26, "• Giới hạn mô hình: Không áp dụng cho trạm có dưới 30 chuyến/tháng (thiếu độ tin cậy mẫu thống kê).", color="#CBD5E1", fontsize=8)
    ax.text(10, 19, "• Đạo đức & Quyền riêng tư: Tuân thủ NYCBS Data Policy. Tuyệt đối không hiển thị ride_id hay lộ trình cá nhân.", color="#34D399", fontsize=8)
    ax.text(10, 12, "• API Endpoints: GET /api/stations, GET /api/station/{id}, GET /api/metrics, GET /api/model-card.", color="#93C5FD", fontsize=8)

    out_file = os.path.join(FIG_DIR, "fig4_4_screen3_dashboard.png")
    plt.tight_layout()
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()
    print(f"Đã tạo: {out_file}")


if __name__ == "__main__":
    create_architecture_diagram()
    create_ui_screen1()
    create_ui_screen2()
    create_ui_screen3()
    print("HOÀN THÀNH TẠO 4 ĐỒ THỊ CHƯƠNG 4 XUẤT SẮC!")
