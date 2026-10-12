/* ==========================================================================
   CitiBike Profiler - Frontend Application Logic
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Quản lý Chuyển Tab (3 Màn hình)
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-tab');

      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));

      btn.classList.add('active');
      const targetContent = document.getElementById(targetId);
      if (targetContent) {
        targetContent.classList.add('active');
      }

      // Khi chuyển sang Tab Bản đồ, resize lại Leaflet Map
      if (targetId === 'tab-map' && window.mapInstance) {
        setTimeout(() => {
          window.mapInstance.invalidateSize();
        }, 200);
      }
    });
  });

  // 2. Khởi tạo Bản đồ Leaflet (New York City)
  const mapElement = document.getElementById('leaflet-map');
  if (mapElement) {
    initLeafletMap();
  }

  // 3. Khởi tạo Module Mô phỏng & Dự đoán Trạm mới
  initPredictionModule();
});

let mapInstance = null;
let currentMarkersLayer = null;
let allStationsCache = [];

const CLUSTER_COLORS = {
  0: '#3B82F6', // Xanh dương - Thương mại / Công sở
  1: '#10B981', // Xanh ngọc - Dân cư đi làm
  2: '#F59E0B'  // Hổ phách / Cam - Hỗn hợp & Giải trí
};

const CLUSTER_NAMES = {
  0: 'Cụm 0: Thương Mại / Văn Phòng',
  1: 'Cụm 1: Dân Cư Đi Làm',
  2: 'Cụm 2: Hỗn Hợp & Giải Trí'
};

function initLeafletMap() {
  // Tọa độ trung tâm Manhattan NYC: [40.7580, -73.9855]
  mapInstance = L.map('leaflet-map', {
    zoomControl: true,
    preferCanvas: true
  }).setView([40.7580, -73.9855], 12);
  window.mapInstance = mapInstance;

  // Lớp bản đồ nền CartoDB Dark Matter tối giản, hiện đại
  L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19
  }).addTo(mapInstance);

  currentMarkersLayer = L.layerGroup().addTo(mapInstance);

  // Lắng nghe sự kiện Bộ lọc
  const monthSelect = document.getElementById('month-select');
  const clusterSelect = document.getElementById('cluster-select');
  const searchInput = document.getElementById('search-input');

  if (monthSelect) {
    monthSelect.addEventListener('change', () => {
      loadStations(monthSelect.value);
    });
  }

  if (clusterSelect) {
    clusterSelect.addEventListener('change', filterAndRenderStations);
  }

  if (searchInput) {
    searchInput.addEventListener('input', debounce(filterAndRenderStations, 250));
  }

  // Tải dữ liệu mặc định ban đầu (Tháng 04/2026)
  loadStations('2026-04');
}

async function loadStations(month) {
  const countEl = document.getElementById('visible-station-count');
  if (countEl) countEl.innerText = 'Đang tải...';

  try {
    const res = await fetch(`/api/stations?month=${encodeURIComponent(month)}`);
    if (!res.ok) {
      throw new Error(`Lỗi tải dữ liệu: HTTP ${res.status}`);
    }
    allStationsCache = await res.json();
    filterAndRenderStations();
  } catch (err) {
    console.error('Lỗi API Stations:', err);
    if (countEl) countEl.innerText = 'Lỗi kết nối API';
  }
}

function filterAndRenderStations() {
  if (!currentMarkersLayer) return;
  currentMarkersLayer.clearLayers();

  const clusterVal = document.getElementById('cluster-select')?.value || 'all';
  const searchVal = (document.getElementById('search-input')?.value || '').trim().toLowerCase();

  const filtered = allStationsCache.filter(st => {
    // Lọc theo cụm
    if (clusterVal !== 'all' && st.cluster.toString() !== clusterVal) {
      return false;
    }
    // Lọc theo từ khóa tìm kiếm
    if (searchVal) {
      const matchName = st.station_name.toLowerCase().includes(searchVal);
      const matchId = st.station_id.toLowerCase().includes(searchVal);
      if (!matchName && !matchId) return false;
    }
    return true;
  });

  // Cập nhật số lượng trạm hiển thị
  const countEl = document.getElementById('visible-station-count');
  if (countEl) countEl.innerText = filtered.length.toLocaleString();

  // Vẽ các điểm trạm lên bản đồ
  filtered.forEach(st => {
    const color = CLUSTER_COLORS[st.cluster] || '#9CA3AF';
    const marker = L.circleMarker([st.lat, st.lng], {
      radius: 6,
      fillColor: color,
      color: '#FFFFFF',
      weight: 1,
      opacity: 0.9,
      fillOpacity: 0.85
    });

    // Tooltip ngắn khi hover
    marker.bindTooltip(`
      <div style="font-family: Inter, sans-serif; font-size: 12px; line-height: 1.4;">
        <strong style="color: ${color};">${CLUSTER_NAMES[st.cluster]}</strong><br>
        <strong>${st.station_name}</strong><br>
        <span style="color: #6B7280;">${st.total_trips.toLocaleString()} chuyến đi</span>
      </div>
    `, { direction: 'top', offset: [0, -4] });

    // Click xem profile chi tiết
    marker.on('click', () => {
      fetchAndDisplayStationDetail(st.station_id, st.month);
    });

    currentMarkersLayer.addLayer(marker);
  });
}

async function fetchAndDisplayStationDetail(stationId, month) {
  try {
    const res = await fetch(`/api/station/${encodeURIComponent(stationId)}?month=${encodeURIComponent(month)}`);
    if (!res.ok) throw new Error('Không lấy được chi tiết trạm');
    const data = await res.json();
    renderStationDetailCard(data);
  } catch (err) {
    console.error('Lỗi xem chi tiết trạm:', err);
  }
}

function renderStationDetailCard(st) {
  const placeholder = document.getElementById('profile-placeholder');
  const details = document.getElementById('profile-details');
  if (placeholder) placeholder.style.display = 'none';
  if (details) details.classList.remove('hidden');

  // Điền thông tin cơ bản
  const tag = document.getElementById('detail-cluster-tag');
  tag.innerText = `Cụm ${st.cluster}: ${st.cluster_label.split('(')[0]}`;
  tag.style.background = `${CLUSTER_COLORS[st.cluster]}33`;
  tag.style.color = CLUSTER_COLORS[st.cluster];

  document.getElementById('detail-station-name').innerText = st.station_name;
  document.getElementById('detail-station-id').innerText = st.station_id;
  document.getElementById('detail-total-trips').innerText = `${st.total_trips.toLocaleString()} chuyến`;

  // Cập nhật giá trị và thanh đo (Progress Bars)
  const mPct = (st.morning_ratio * 100).toFixed(1);
  document.getElementById('bar-val-morning').innerText = `${mPct}%`;
  document.getElementById('bar-morning').style.width = `${Math.min(100, mPct * 2.5)}%`;

  const ePct = (st.evening_ratio * 100).toFixed(1);
  document.getElementById('bar-val-evening').innerText = `${ePct}%`;
  document.getElementById('bar-evening').style.width = `${Math.min(100, ePct * 2.5)}%`;

  const wPct = (st.weekend_ratio * 100).toFixed(1);
  document.getElementById('bar-val-weekend').innerText = `${wPct}%`;
  document.getElementById('bar-weekend').style.width = `${Math.min(100, wPct * 2.5)}%`;

  const memPct = (st.member_share * 100).toFixed(1);
  document.getElementById('bar-val-member').innerText = `${memPct}%`;
  document.getElementById('bar-member').style.width = `${memPct}%`;

  const flowVal = (st.morning_net_flow_ratio * 100).toFixed(1);
  const flowPrefix = st.morning_net_flow_ratio > 0 ? '+' : '';
  const flowEl = document.getElementById('bar-val-flow');
  flowEl.innerText = `${flowPrefix}${flowVal}%`;
  flowEl.style.color = st.morning_net_flow_ratio > 0 ? '#38BDF8' : '#F43F5E';
  
  // Chiều thanh đo flow (offset từ giữa 50%)
  const flowFill = document.getElementById('bar-flow');
  const normalizedFlow = Math.max(5, Math.min(95, 50 + (st.morning_net_flow_ratio * 50)));
  flowFill.style.width = `${normalizedFlow}%`;
  flowFill.style.background = st.morning_net_flow_ratio > 0 ? '#38BDF8' : '#F43F5E';

  document.getElementById('detail-duration').innerText = `${st.median_duration_min} phút`;
  document.getElementById('detail-coords').innerText = `${st.lat.toFixed(4)}, ${st.lng.toFixed(4)}`;
}

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/* ==========================================================================
   Module Mô Phỏng & Dự Đoán Trạm Mới (K-Means Online Inference)
   ========================================================================== */
let simulatedMarker = null;
let lastPredictionResult = null;

function initPredictionModule() {
  const btnExplore = document.getElementById('btn-mode-explore');
  const btnPredict = document.getElementById('btn-mode-predict');
  const exploreContainer = document.getElementById('explore-view-container');
  const predictContainer = document.getElementById('predict-view-container');

  // Chuyển đổi giữa 2 chế độ ở Sidebar
  if (btnExplore && btnPredict) {
    btnExplore.addEventListener('click', () => {
      btnExplore.classList.add('active');
      btnPredict.classList.remove('active');
      if (exploreContainer) exploreContainer.classList.remove('hidden');
      if (predictContainer) predictContainer.classList.add('hidden');
    });

    btnPredict.addEventListener('click', () => {
      btnPredict.classList.add('active');
      btnExplore.classList.remove('active');
      if (predictContainer) predictContainer.classList.remove('hidden');
      if (exploreContainer) exploreContainer.classList.add('hidden');
    });
  }

  // Danh sách slider và nhãn đồng bộ
  const sliderConfig = [
    { id: 'p-morning', lbl: 'lbl-morning', suffix: '%' },
    { id: 'p-evening', lbl: 'lbl-evening', suffix: '%' },
    { id: 'p-midday', lbl: 'lbl-midday', suffix: '%' },
    { id: 'p-night', lbl: 'lbl-night', suffix: '%' },
    { id: 'p-weekend', lbl: 'lbl-weekend', suffix: '%' },
    { id: 'p-member', lbl: 'lbl-member', suffix: '%' },
    { id: 'p-duration', lbl: 'lbl-duration', suffix: ' phút' },
    { id: 'p-flow', lbl: 'lbl-flow', suffix: '%', isFlow: true }
  ];

  sliderConfig.forEach(item => {
    const el = document.getElementById(item.id);
    const lbl = document.getElementById(item.lbl);
    if (el && lbl) {
      el.addEventListener('input', () => {
        let val = el.value;
        if (item.isFlow) {
          const prefix = Number(val) > 0 ? '+' : '';
          lbl.innerText = `${prefix}${val}${item.suffix}`;
          lbl.style.color = Number(val) > 0 ? '#38BDF8' : '#F43F5E';
        } else {
          lbl.innerText = `${val}${item.suffix}`;
        }
      });
    }
  });

  // Mẫu trạm điển hình (Presets)
  const presets = {
    commuter: {
      name: "Trạm Dân Cư (Queens Commuter Origin)",
      morning: 28, evening: 18, midday: 18, night: 10, weekend: 15, member: 88, duration: 9.0, flow: -42
    },
    commercial: {
      name: "Trạm Văn Phòng (Midtown Destination)",
      morning: 8, evening: 39, midday: 26, night: 12, weekend: 14, member: 80, duration: 11.5, flow: 38
    },
    leisure: {
      name: "Trạm Du Lịch (Central Park Leisure)",
      morning: 11, evening: 24, midday: 25, night: 24, weekend: 27, member: 65, duration: 16.0, flow: 5
    }
  };

  const presetBtns = document.querySelectorAll('.preset-btn');
  presetBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const pKey = btn.getAttribute('data-preset');
      const data = presets[pKey];
      if (data) {
        document.getElementById('p-name').value = data.name;
        setSliderValue('p-morning', 'lbl-morning', data.morning, '%');
        setSliderValue('p-evening', 'lbl-evening', data.evening, '%');
        setSliderValue('p-midday', 'lbl-midday', data.midday, '%');
        setSliderValue('p-night', 'lbl-night', data.night, '%');
        setSliderValue('p-weekend', 'lbl-weekend', data.weekend, '%');
        setSliderValue('p-member', 'lbl-member', data.member, '%');
        setSliderValue('p-duration', 'lbl-duration', data.duration, ' phút');
        setSliderValue('p-flow', 'lbl-flow', data.flow, '%', true);
      }
    });
  });

  // Xử lý gửi Form dự đoán
  const formPredict = document.getElementById('form-predict');
  if (formPredict) {
    formPredict.addEventListener('submit', async (e) => {
      e.preventDefault();
      await runPrediction();
    });
  }

  // Nút Cắm mốc trạm trên bản đồ
  const btnPin = document.getElementById('btn-pin-simulated');
  if (btnPin) {
    btnPin.addEventListener('click', () => {
      if (lastPredictionResult && window.mapInstance) {
        pinSimulatedStationOnMap(lastPredictionResult);
      }
    });
  }
}

function setSliderValue(inputId, lblId, val, suffix, isFlow = false) {
  const el = document.getElementById(inputId);
  const lbl = document.getElementById(lblId);
  if (el) el.value = val;
  if (lbl) {
    if (isFlow) {
      const prefix = Number(val) > 0 ? '+' : '';
      lbl.innerText = `${prefix}${val}${suffix}`;
      lbl.style.color = Number(val) > 0 ? '#38BDF8' : '#F43F5E';
    } else {
      lbl.innerText = `${val}${suffix}`;
    }
  }
}

async function runPrediction() {
  const btnSubmit = document.getElementById('btn-submit-predict');
  if (btnSubmit) {
    btnSubmit.disabled = true;
    btnSubmit.innerHTML = '<span>⏳</span> Đang tính toán K-Means...';
  }

  const payload = {
    station_name: document.getElementById('p-name')?.value || "Trạm mô phỏng mới",
    morning_ratio: Number(document.getElementById('p-morning')?.value || 24) / 100,
    evening_ratio: Number(document.getElementById('p-evening')?.value || 22) / 100,
    midday_ratio: Number(document.getElementById('p-midday')?.value || 22) / 100,
    night_ratio: Number(document.getElementById('p-night')?.value || 12) / 100,
    weekend_ratio: Number(document.getElementById('p-weekend')?.value || 18) / 100,
    member_share: Number(document.getElementById('p-member')?.value || 85) / 100,
    median_duration_min: Number(document.getElementById('p-duration')?.value || 10.0),
    morning_net_flow_ratio: Number(document.getElementById('p-flow')?.value || -35) / 100,
    lat: 40.7580 + (Math.random() - 0.5) * 0.04,
    lng: -73.9855 + (Math.random() - 0.5) * 0.04
  };

  const startTime = performance.now();
  try {
    const res = await fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      throw new Error(`Lỗi API: ${res.status}`);
    }

    const data = await res.json();
    const elapsed = Math.round(performance.now() - startTime);
    lastPredictionResult = data;
    renderPredictionResult(data, elapsed);
  } catch (err) {
    console.error('Lỗi khi dự đoán K-Means:', err);
    alert('Không thể kết nối API dự đoán: ' + err.message);
  } finally {
    if (btnSubmit) {
      btnSubmit.disabled = false;
      btnSubmit.innerHTML = '<span>🚀</span> Chạy Dự Đoán K-Means';
    }
  }
}

function renderPredictionResult(data, elapsedMs) {
  const card = document.getElementById('predict-result-card');
  if (!card) return;
  card.classList.remove('hidden');

  const badge = document.getElementById('res-badge');
  badge.innerText = `Cụm ${data.predicted_cluster}`;
  badge.style.background = data.cluster_color;
  badge.style.color = '#FFFFFF';

  document.getElementById('res-time').innerText = `< ${elapsedMs}ms`;
  document.getElementById('res-label').innerText = data.cluster_label;

  // Khoảng cách tới các tâm
  const d0 = data.distances_to_centroids["Cụm 0"] ?? '--';
  const d1 = data.distances_to_centroids["Cụm 1"] ?? '--';
  const d2 = data.distances_to_centroids["Cụm 2"] ?? '--';

  document.getElementById('dist-0').innerText = d0;
  document.getElementById('dist-1').innerText = d1;
  document.getElementById('dist-2').innerText = d2;

  ['dist-0', 'dist-1', 'dist-2'].forEach((id, idx) => {
    const el = document.getElementById(id);
    if (el) {
      if (idx === data.predicted_cluster) {
        el.className = 'highlight-dist';
        el.innerText += ' (Gần nhất ★)';
      } else {
        el.className = '';
      }
    }
  });

  // Khuyến nghị điều phối
  document.getElementById('res-recommendation').innerText = data.strategy_recommendation;

  // Cuộn nhẹ xuống xem kết quả
  card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function pinSimulatedStationOnMap(data) {
  if (!window.mapInstance) return;

  if (simulatedMarker) {
    window.mapInstance.removeLayer(simulatedMarker);
  }

  // Tạo marker cắm cờ mô phỏng nổi bật
  const customIcon = L.divIcon({
    className: 'simulated-station-pin',
    html: `
      <div style="
        background: ${data.cluster_color};
        width: 24px;
        height: 24px;
        border-radius: 50%;
        border: 3px solid #FFFFFF;
        box-shadow: 0 0 15px ${data.cluster_color}, 0 0 5px rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #FFFFFF;
        font-weight: bold;
        font-size: 11px;
      ">
        ★
      </div>
    `,
    iconSize: [24, 24],
    iconAnchor: [12, 12]
  });

  simulatedMarker = L.marker([data.lat, data.lng], { icon: customIcon }).addTo(window.mapInstance);

  simulatedMarker.bindPopup(`
    <div style="font-family: Inter, sans-serif; min-width: 200px;">
      <span style="
        background: ${data.cluster_color};
        color: #FFFFFF;
        font-size: 11px;
        font-weight: bold;
        padding: 2px 8px;
        border-radius: 6px;
        display: inline-block;
        margin-bottom: 6px;
      ">
        ★ TRẠM MÔ PHỎNG: Cụm ${data.predicted_cluster}
      </span>
      <h4 style="margin: 4px 0 6px; font-size: 14px; color: #1E293B;">${data.station_name}</h4>
      <p style="margin: 0; font-size: 12px; color: #475569;">
        <strong>Phân loại:</strong> ${data.cluster_label}<br>
        <strong>Tọa độ:</strong> ${data.lat.toFixed(4)}, ${data.lng.toFixed(4)}
      </p>
    </div>
  `).openPopup();

  window.mapInstance.flyTo([data.lat, data.lng], 14, { duration: 1.2 });
}
