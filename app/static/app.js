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
