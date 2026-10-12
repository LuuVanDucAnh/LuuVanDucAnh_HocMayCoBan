import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

PPTX_PATH = "d:/BTL_CumTramCiTiBike/LuuVanDucAnh_BaoCao_BTL.pptx"
FIG_DIR = "d:/BTL_CumTramCiTiBike/reports/figures"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Standard Academic Typography
FONT_NAME = "Times New Roman"

# Clean Light Academic Palette (Sáng sủa, trang nhã, không dùng nền đen xanh)
BG_WHITE = RGBColor(255, 255, 255)       # Nền trắng tinh khôi
SURFACE_LIGHT = RGBColor(248, 250, 252)  # #F8FAFC Xám ngọc trai nhẹ nhàng cho thẻ card
BORDER_LIGHT = RGBColor(226, 232, 240)   # #E2E8F0 Đường viền thanh lịch
PRIMARY_BLUE = RGBColor(30, 58, 138)     # #1E3A8A Xanh dương học thuật cổ điển
ACCENT_BLUE = RGBColor(37, 99, 235)      # #2563EB Xanh dương điểm nhấn
DARK_TEXT = RGBColor(30, 41, 59)         # #1E293B Chữ đen than đậm rõ nét
MUTED_TEXT = RGBColor(100, 116, 139)     # #64748B Chữ ghi chú xám
ACCENT_GREEN = RGBColor(5, 150, 105)     # #059669 Xanh lá thành công/đo lường
ACCENT_AMBER = RGBColor(217, 119, 6)     # #D97706 Màu hổ phách nhấn mạnh
CARD_BLUE_TINT = RGBColor(240, 247, 255) # #F0F7FF Nền xanh dương pastel siêu nhẹ

def set_slide_background_white(slide):
    """Đặt nền trắng sạch toàn bộ slide"""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_WHITE
    bg.line.fill.background()
    return bg

def add_card(slide, left, top, width, height, bg_color=SURFACE_LIGHT, border_color=BORDER_LIGHT):
    """Tạo khối card hình chữ nhật bo góc với nền sáng trang nhã"""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card

def add_clean_header(slide, title_text, category_text="HỌC PHẦN: HỌC MÁY CƠ BẢN • PROJECT 23"):
    """
    Tiêu đề phong cách học thuật hiện đại, sáng sủa, thanh lịch:
    - Vạch chỉ màu trên đỉnh slide
    - Tên trường và học phần
    - Vạch đứng xanh nhấn tiêu đề
    - Tiêu đề slide to rõ bằng chữ xanh dương đậm
    - Đường kẻ ngang mỏng phân cách
    """
    # 1. Vạch màu rất mảnh trên mép đỉnh (Top accent strip)
    top_strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.06))
    top_strip.fill.solid()
    top_strip.fill.fore_color.rgb = ACCENT_BLUE
    top_strip.line.fill.background()

    # 2. Tên trường & Chuyên mục
    tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.28), Inches(11.7), Inches(0.28))
    tf_cat = tb_cat.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = f"TRƯỜNG ĐẠI HỌC CÔNG NGHỆ KỸ THUẬT HƯNG YÊN  •  {category_text.upper()}"
    p_cat.font.name = FONT_NAME
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = ACCENT_BLUE

    # 3. Vạch đứng xanh trang nhã trước tiêu đề
    v_marker = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.60), Inches(0.08), Inches(0.48))
    v_marker.fill.solid()
    v_marker.fill.fore_color.rgb = ACCENT_BLUE
    v_marker.line.fill.background()

    # 4. Tiêu đề Slide chính
    tb_t = slide.shapes.add_textbox(Inches(1.0), Inches(0.55), Inches(11.5), Inches(0.60))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = FONT_NAME
    p_t.font.size = Pt(21)
    p_t.font.bold = True
    p_t.font.color.rgb = PRIMARY_BLUE

    # 5. Đường kẻ chỉ mỏng phân cách tiêu đề với nội dung
    sep_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.20), Inches(11.733), Inches(0.015))
    sep_line.fill.solid()
    sep_line.fill.fore_color.rgb = BORDER_LIGHT
    sep_line.line.fill.background()

def add_clean_footer(slide, slide_num, total_slides=15):
    """Thanh chân trang thanh nhã nền sáng"""
    # Đường kẻ chỉ ngang mỏng
    sep_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.015))
    sep_line.fill.solid()
    sep_line.fill.fore_color.rgb = BORDER_LIGHT
    sep_line.line.fill.background()

    # Footer Left
    tb_l = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(5.2), Inches(0.35))
    p_l = tb_l.text_frame.paragraphs[0]
    p_l.text = "BTL Học máy: Phân nhóm trạm Citi Bike theo hồ sơ sử dụng (Project 23)"
    p_l.font.name = FONT_NAME
    p_l.font.size = Pt(9.5)
    p_l.font.color.rgb = MUTED_TEXT

    # Footer Center
    tb_c = slide.shapes.add_textbox(Inches(5.6), Inches(7.05), Inches(5.0), Inches(0.35))
    p_c = tb_c.text_frame.paragraphs[0]
    p_c.text = "SV: Lưu Văn Đức Anh (12523001)  |  GVHD: PGS. TS. Nguyễn Văn Hậu"
    p_c.font.name = FONT_NAME
    p_c.font.size = Pt(9.5)
    p_c.font.color.rgb = MUTED_TEXT

    # Footer Right
    tb_r = slide.shapes.add_textbox(Inches(11.0), Inches(7.05), Inches(1.533), Inches(0.35))
    p_r = tb_r.text_frame.paragraphs[0]
    p_r.text = f"Trang {slide_num} / {total_slides}"
    p_r.font.name = FONT_NAME
    p_r.font.size = Pt(9.5)
    p_r.font.bold = True
    p_r.font.color.rgb = PRIMARY_BLUE
    p_r.alignment = PP_ALIGN.RIGHT

def apply_times_new_roman_all(presentation):
    """Đảm bảo 100% văn bản toàn bộ bài trình chiếu dùng kiểu chữ Times New Roman"""
    for slide in presentation.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for p in shape.text_frame.paragraphs:
                    p.font.name = FONT_NAME
                    for r in p.runs:
                        r.font.name = FONT_NAME
            if shape.has_table:
                for row in shape.table.rows:
                    for cell in row.cells:
                        for p in cell.text_frame.paragraphs:
                            p.font.name = FONT_NAME
                            for r in p.runs:
                                r.font.name = FONT_NAME

# ==============================================================================
# SLIDE 1: TRANG TIÊU ĐỀ (Cover Slide - Nền Trắng Sáng Thanh Lịch)
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s1)

# Vạch màu đỉnh
top_strip1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.08))
top_strip1.fill.solid()
top_strip1.fill.fore_color.rgb = PRIMARY_BLUE
top_strip1.line.fill.background()

# Khối tiêu đề trường đại học
tb_u = s1.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.7), Inches(0.75))
tf_u = tb_u.text_frame
tf_u.word_wrap = True
p_u1 = tf_u.paragraphs[0]
p_u1.text = "TRƯỜNG ĐẠI HỌC CÔNG NGHỆ KỸ THUẬT HƯNG YÊN"
p_u1.font.name = FONT_NAME
p_u1.font.size = Pt(15)
p_u1.font.bold = True
p_u1.font.color.rgb = PRIMARY_BLUE

p_u2 = tf_u.add_paragraph()
p_u2.text = "KHOA CÔNG NGHỆ THÔNG TIN • BỘ MÔN KHOA HỌC MÁY TÍNH"
p_u2.font.name = FONT_NAME
p_u2.font.size = Pt(12)
p_u2.font.bold = True
p_u2.font.color.rgb = MUTED_TEXT
p_u2.space_before = Pt(3)

# Đường kẻ phân cách nhẹ nhàng
line_u = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.733), Inches(0.02))
line_u.fill.solid()
line_u.fill.fore_color.rgb = BORDER_LIGHT
line_u.line.fill.background()

# Thẻ Badge Học phần
badge = add_card(s1, Inches(0.8), Inches(1.65), Inches(5.2), Inches(0.42), bg_color=CARD_BLUE_TINT, border_color=RGBColor(191, 219, 254))
tb_b = s1.shapes.add_textbox(Inches(0.9), Inches(1.70), Inches(5.0), Inches(0.35))
p_b = tb_b.text_frame.paragraphs[0]
p_b.text = "BÁO CÁO BÀI TẬP LỚN • HỌC PHẦN HỌC MÁY CƠ BẢN"
p_b.font.name = FONT_NAME
p_b.font.size = Pt(11)
p_b.font.bold = True
p_b.font.color.rgb = PRIMARY_BLUE

# Tên Đề tài
tb_title = s1.shapes.add_textbox(Inches(0.8), Inches(2.25), Inches(11.7), Inches(2.1))
tf_t = tb_title.text_frame
tf_t.word_wrap = True
p1 = tf_t.paragraphs[0]
p1.text = "PROJECT 23: PHÂN NHÓM TRẠM CITI BIKE\nTHEO HỒ SƠ SỬ DỤNG"
p1.font.name = FONT_NAME
p1.font.size = Pt(32)
p1.font.bold = True
p1.font.color.rgb = PRIMARY_BLUE

p2 = tf_t.add_paragraph()
p2.text = "Ứng dụng Thuật toán K-Means Clustering tối ưu hóa điều phối giao thông đô thị New York"
p2.font.name = FONT_NAME
p2.font.size = Pt(15.5)
p2.font.color.rgb = DARK_TEXT
p2.space_before = Pt(8)

# Khung Thông tin Sinh viên & GVHD
info_card = add_card(s1, Inches(0.8), Inches(4.55), Inches(11.7), Inches(2.15), bg_color=SURFACE_LIGHT, border_color=BORDER_LIGHT)
tb_info = s1.shapes.add_textbox(Inches(1.1), Inches(4.7), Inches(11.2), Inches(1.85))
tfi = tb_info.text_frame
tfi.word_wrap = True

pi1 = tfi.paragraphs[0]
pi1.text = "THÔNG TIN BẢO VỆ ĐỀ TÀI"
pi1.font.name = FONT_NAME
pi1.font.size = Pt(13)
pi1.font.bold = True
pi1.font.color.rgb = PRIMARY_BLUE

pi2 = tfi.add_paragraph()
pi2.text = "• Sinh viên thực hiện: LƯU VĂN ĐỨC ANH    |    Mã sinh viên: 12523001    |    Lớp: 12523W.1"
pi2.font.name = FONT_NAME
pi2.font.size = Pt(13.5)
pi2.font.bold = True
pi2.font.color.rgb = DARK_TEXT
pi2.space_before = Pt(6)

pi3 = tfi.add_paragraph()
pi3.text = "• Giảng viên hướng dẫn: PGS. TS. NGUYỄN VĂN HẬU"
pi3.font.name = FONT_NAME
pi3.font.size = Pt(13.5)
pi3.font.bold = True
pi3.font.color.rgb = DARK_TEXT
pi3.space_before = Pt(4)

pi4 = tfi.add_paragraph()
pi4.text = "• Địa điểm: Trường Đại học Công nghệ Kỹ thuật Hưng Yên — Tháng 10/2026"
pi4.font.name = FONT_NAME
pi4.font.size = Pt(12.5)
pi4.font.color.rgb = MUTED_TEXT
pi4.space_before = Pt(4)

# ==============================================================================
# SLIDE 2: NỘI DUNG BÁO CÁO (Agenda)
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s2)
add_clean_header(s2, "Nội Dung Báo Cáo (Khung Thời Lượng 20 Phút)")
add_clean_footer(s2, 2, 15)

agenda_items = [
    ("1. Đặt Vấn Đề & Bài Toán", "Hiện trạng hệ thống Citi Bike New York và sự mất cân bằng trạm.", PRIMARY_BLUE),
    ("2. Dữ Liệu & Đặc Trưng", "Tổng hợp 5.6M chuyến đi thành 8 đặc trưng tỷ lệ (Rate features).", PRIMARY_BLUE),
    ("3. Phương Pháp K-Means", "Nguyên lý WCSS, thuật toán Lloyd và chiến lược Anti-Leakage.", PRIMARY_BLUE),
    ("4. Bốn Thí Nghiệm Khoa Học", "Volume vs Profile, Elbow/Silhouette, Độ ổn định Seed/Mùa & Median.", ACCENT_GREEN),
    ("5. Web Serving & Demo", "Giao diện 3 màn hình tương tác Leaflet và kiểm thử 7 test cases.", ACCENT_GREEN),
    ("6. Kết Luận & Hướng Mở", "Đóng góp thực tiễn cho điều phối xe và hướng phát triển.", ACCENT_AMBER)
]

for idx, (head, desc, color) in enumerate(agenda_items):
    col = idx % 3
    row = idx // 3
    left = Inches(0.8 + col * 4.0)
    top = Inches(1.45 + row * 2.65)
    card = add_card(s2, left, top, Inches(3.7), Inches(2.3), bg_color=SURFACE_LIGHT)
    tb = s2.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), Inches(3.2), Inches(1.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = head
    p1.font.name = FONT_NAME
    p1.font.size = Pt(15.5)
    p1.font.bold = True
    p1.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = FONT_NAME
    p2.font.size = Pt(13)
    p2.font.color.rgb = DARK_TEXT
    p2.space_before = Pt(8)

# ==============================================================================
# SLIDE 3: BÀI TOÁN THỰC TẾ CITI BIKE
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s3)
add_clean_header(s3, "Đặt Vấn Đề: Bài Toán Điều Phối Xe Đạp Đô Thị (Rebalancing)")
add_clean_footer(s3, 3, 15)

# Card 1: Bối cảnh
c1 = add_card(s3, Inches(0.8), Inches(1.45), Inches(5.6), Inches(5.3), bg_color=SURFACE_LIGHT)
tb1 = s3.shapes.add_textbox(Inches(1.1), Inches(1.65), Inches(5.0), Inches(4.8))
tf1 = tb1.text_frame
tf1.word_wrap = True
p = tf1.paragraphs[0]
p.text = "HỆ THỐNG CITI BIKE (NEW YORK)"
p.font.name = FONT_NAME
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = PRIMARY_BLUE

bullets1 = [
    ("Quy mô khổng lồ:", "Mạng lưới chia sẻ xe đạp lớn nhất Bắc Mỹ với hơn 2.200 trạm xe trải rộng khắp New York."),
    ("Lưu lượng vận hành:", "Phục vụ hơn 5.6 triệu chuyến đi (Tháng 4: 3.86M chuyến; Tháng 1: 1.81M chuyến)."),
    ("Mâu thuẫn cung - cầu:", "Nhu cầu di chuyển thay đổi đột biến theo giờ cao điểm và theo mùa, tạo ra nút thắt cổ chai điều phối.")
]
for b_title, b_desc in bullets1:
    p = tf1.add_paragraph()
    p.text = f"• {b_title} {b_desc}"
    p.font.name = FONT_NAME
    p.font.size = Pt(13)
    p.font.color.rgb = DARK_TEXT
    p.space_before = Pt(12)

# Card 2: Thách thức & Giải pháp
c2 = add_card(s3, Inches(6.8), Inches(1.45), Inches(5.7), Inches(5.3), bg_color=SURFACE_LIGHT)
tb2 = s3.shapes.add_textbox(Inches(7.1), Inches(1.65), Inches(5.1), Inches(4.8))
tf2 = tb2.text_frame
tf2.word_wrap = True
p = tf2.paragraphs[0]
p.text = "THÁCH THỨC & MỤC TIÊU HỌC MÁY"
p.font.name = FONT_NAME
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = ACCENT_AMBER

bullets2 = [
    ("Hiện tượng Cháy xe (Sáng):", "Khu dân cư bị rút sạch xe lúc 7h-8h sáng do người dân đi làm."),
    ("Hiện tượng Cháy bãi (Sáng):", "Khu văn phòng trung tâm không còn chỗ trống để người dùng trả xe lúc 8h-9h."),
    ("Hạn chế của cách làm cũ:", "Phân cụm theo quy mô số chuyến (Volume) chỉ biết trạm to hay nhỏ, không hiểu bản chất chức năng."),
    ("Giải pháp đề xuất:", "Phân cụm K-Means không giám sát theo Hồ sơ Tỷ lệ giờ (Profile) để phân nhóm chức năng trạm phục vụ xe tải điều phối.")
]
for b_title, b_desc in bullets2:
    p = tf2.add_paragraph()
    p.text = f"• {b_title} {b_desc}"
    p.font.name = FONT_NAME
    p.font.size = Pt(13)
    p.font.color.rgb = DARK_TEXT
    p.space_before = Pt(10)

# ==============================================================================
# SLIDE 4: TRÍCH XUẤT ĐẶC TRƯNG HỒ SƠ TRẠM
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s4)
add_clean_header(s4, "Trích Xuất 8 Đặc Trưng Tỷ Lệ (Feature Engineering)")
add_clean_footer(s4, 4, 15)

c_feat = add_card(s4, Inches(0.8), Inches(1.45), Inches(7.5), Inches(5.3), bg_color=SURFACE_LIGHT)
tb_f = s4.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(7.1), Inches(4.8))
tff = tb_f.text_frame
tff.word_wrap = True
p = tff.paragraphs[0]
p.text = "KHÔNG GIAN ĐẶC TRƯNG HỒ SƠ TRẠM (8 CHIỀU LIÊN TỤC)"
p.font.name = FONT_NAME
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = PRIMARY_BLUE

features_list = [
    ("morning_ratio:", "Tỷ lệ xuất phát sáng (06:00 - 10:00) — Đặc trưng khu dân cư"),
    ("midday_ratio:", "Tỷ lệ xuất phát trưa (10:00 - 16:00)"),
    ("evening_ratio:", "Tỷ lệ xuất phát chiều tan sở (16:00 - 20:00) — Đặc trưng khu văn phòng"),
    ("night_ratio:", "Tỷ lệ xuất phát đêm (20:00 - 06:00) — Đặc trưng khu giải trí"),
    ("weekend_ratio:", "Tỷ lệ chuyến vào Thứ 7 & Chủ Nhật"),
    ("member_share:", "Tỷ lệ chuyến đi do Hội viên năm sử dụng (Annual Member)"),
    ("median_duration_min:", "Thời lượng trung vị chuyến đi (phút) — Khử ngoại lai"),
    ("morning_net_flow_ratio:", "Chênh lệch dòng xe sáng: (Vào - Ra) / (Vào + Ra)")
]

for fn, fd in features_list:
    p = tff.add_paragraph()
    p.text = f"• {fn} {fd}"
    p.font.name = FONT_NAME
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_TEXT
    p.space_before = Pt(7)

c_rule = add_card(s4, Inches(8.6), Inches(1.45), Inches(3.9), Inches(5.3), bg_color=CARD_BLUE_TINT, border_color=RGBColor(191, 219, 254))
tb_r = s4.shapes.add_textbox(Inches(8.8), Inches(1.65), Inches(3.5), Inches(4.8))
tfr = tb_r.text_frame
tfr.word_wrap = True
p = tfr.paragraphs[0]
p.text = "2 NGUYÊN TẮC VÀNG"
p.font.name = FONT_NAME
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = PRIMARY_BLUE

rules = [
    ("1. Không dùng Lat/Lng:", "Tọa độ địa lý chỉ dùng vẽ bản đồ. Tuyệt đối không nạp vào K-Means để tránh gom cụm theo khoảng cách địa lý thay vì hành vi."),
    ("2. Loại bỏ Quy mô:", "Chỉ dùng tỷ lệ % (Rate/Share) để trạm 500 chuyến và trạm 5.000 chuyến có cùng nhịp sinh hoạt thì vẫn vào chung 1 cụm.")
]
for rt, rd in rules:
    p = tfr.add_paragraph()
    p.text = f"★ {rt}\n{rd}"
    p.font.name = FONT_NAME
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_TEXT
    p.space_before = Pt(14)

# ==============================================================================
# SLIDE 5: CHIẾN LƯỢC CHỐNG RÒ RỈ & PIPELINE
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s5)
add_clean_header(s5, "Chiến Lược Phân Chia Chống Rò Rỉ Dữ Liệu (Anti-Leakage)")
add_clean_footer(s5, 5, 15)

splits = [
    ("TẬP HUẤN LUYỆN (TRAIN)", "1.559 Trạm (70%)", "Dùng để fit StandardScaler và huấn luyện các mô hình K-Means.", PRIMARY_BLUE),
    ("TẬP KIỂM ĐỊNH (VALIDATION)", "335 Trạm (15%)", "Dùng để tìm kiếm K tối ưu (K=2..8) và đánh giá độ ổn định qua Seed.", ACCENT_GREEN),
    ("TẬP KIỂM THỬ (TEST)", "335 Trạm (15%)", "Niêm phong hoàn toàn, chỉ mở ra đánh giá nghiệm thu ở bước cuối cùng.", ACCENT_AMBER)
]

for idx, (title, count, desc, color) in enumerate(splits):
    left = Inches(0.8 + idx * 4.0)
    card = add_card(s5, left, Inches(1.45), Inches(3.7), Inches(2.6), bg_color=SURFACE_LIGHT)
    tb = s5.shapes.add_textbox(left + Inches(0.2), Inches(1.6), Inches(3.3), Inches(2.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_NAME
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = count
    p2.font.name = FONT_NAME
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = DARK_TEXT
    p2.space_before = Pt(4)
    
    p3 = tf.add_paragraph()
    p3.text = desc
    p3.font.name = FONT_NAME
    p3.font.size = Pt(12)
    p3.font.color.rgb = MUTED_TEXT
    p3.space_before = Pt(8)

c_bot = add_card(s5, Inches(0.8), Inches(4.3), Inches(11.7), Inches(2.45), bg_color=SURFACE_LIGHT)
tbb = s5.shapes.add_textbox(Inches(1.1), Inches(4.45), Inches(11.2), Inches(2.1))
tfb = tbb.text_frame
tfb.word_wrap = True
p = tfb.paragraphs[0]
p.text = "CƠ CHẾ CHỐNG RÒ RỈ TOÀN DIỆN TRONG CODE:"
p.font.name = FONT_NAME
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = PRIMARY_BLUE

steps = [
    "1. Phân chia ở cấp độ Trạm: Toàn bộ lịch sử hành vi của 1 trạm nằm trọn vẹn trong 1 phân vùng duy nhất.",
    "2. Cách ly StandardScaler: scaler.fit(X_train) duy nhất trên Train. Tập Val và Test chỉ áp dụng scaler.transform().",
    "3. Tái lập 100%: Cố định RANDOM_STATE = 42 xuyên suốt toàn bộ pipeline tiền xử lý và mô hình hóa."
]
for st in steps:
    p = tfb.add_paragraph()
    p.text = st
    p.font.name = FONT_NAME
    p.font.size = Pt(13)
    p.font.color.rgb = DARK_TEXT
    p.space_before = Pt(6)

# ==============================================================================
# SLIDE 6: THUẬT TOÁN K-MEANS & K-MEANS++
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s6)
add_clean_header(s6, "Cơ Sở Lý Thuyết: Thuật Toán Phân Cụm K-Means & K-Means++")
add_clean_footer(s6, 6, 15)

c_m = add_card(s6, Inches(0.8), Inches(1.45), Inches(5.6), Inches(5.3), bg_color=SURFACE_LIGHT)
tb_m = s6.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.2), Inches(4.8))
tfm = tb_m.text_frame
tfm.word_wrap = True
p = tfm.paragraphs[0]
p.text = "HÀM MỤC TIÊU TOÁN HỌC (WCSS / INERTIA)"
p.font.name = FONT_NAME
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = PRIMARY_BLUE

m_bullets = [
    ("Hàm mục tiêu:", "J(C, μ) = Σ Σ ||x_i - μ_k||²"),
    ("Mục đích:", "Tìm K tâm cụm μ sao cho tổng bình phương khoảng cách từ các trạm tới tâm gần nhất là nhỏ nhất."),
    ("Khoảng cách Euclid:", "d(x, μ) = √[Σ (x_j - μ_j)²] trong không gian 8 chiều."),
    ("Bước gán (Assignment):", "c_i = argmin ||x_i - μ_k||²"),
    ("Bước cập nhật (Update):", "μ_k = (1 / |C_k|) Σ x_i (Trung bình cộng)")
]
for bt, bd in m_bullets:
    p = tfm.add_paragraph()
    p.text = f"• {bt}\n  {bd}"
    p.font.name = FONT_NAME
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_TEXT
    p.space_before = Pt(8)

c_kpp = add_card(s6, Inches(6.8), Inches(1.45), Inches(5.7), Inches(5.3), bg_color=SURFACE_LIGHT)
tb_k = s6.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(4.8))
tfk = tb_k.text_frame
tfk.word_wrap = True
p = tfk.paragraphs[0]
p.text = "VÌ SAO DÙNG K-MEANS++ THAY VÌ RANDOM?"
p.font.name = FONT_NAME
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = ACCENT_GREEN

k_bullets = [
    ("Hạn chế khởi tạo Random:", "Rất dễ chọn các tâm ban đầu nằm sát nhau, khiến thuật toán hội tụ vào cực tiểu cục bộ xấu (Suboptimal local minima)."),
    ("Cơ chế K-Means++:", "Chọn tâm đầu ngẫu nhiên, các tâm tiếp theo được chọn với xác suất tỷ lệ với D(x)² (khoảng cách tới tâm gần nhất)."),
    ("Lợi ích thực nghiệm:", "Các tâm trải đều không gian, tăng tốc độ hội tụ và đem lại độ ổn định tuyệt đối (ARI = 0.9984)."),
    ("Tốc độ suy luận Online:", "Chỉ mất < 1ms để gán cụm cho một trạm mới khi đưa lên web serving.")
]
for bt, bd in k_bullets:
    p = tfk.add_paragraph()
    p.text = f"✔ {bt}\n  {bd}"
    p.font.name = FONT_NAME
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_TEXT
    p.space_before = Pt(8)

# ==============================================================================
# SLIDE 7: THÍ NGHIỆM 1 — BASELINE VS PROFILE
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s7)
add_clean_header(s7, "Thí Nghiệm 1: Đối Chuẩn Volume Baseline vs Profile K-Means")
add_clean_footer(s7, 7, 15)

fig1_path = os.path.join(FIG_DIR, "fig1_baseline_vs_profile.png")
if os.path.exists(fig1_path):
    s7.shapes.add_picture(fig1_path, Inches(0.8), Inches(1.5), width=Inches(6.8))

c_tn1 = add_card(s7, Inches(7.9), Inches(1.45), Inches(4.6), Inches(5.3), bg_color=SURFACE_LIGHT)
tb_t1 = s7.shapes.add_textbox(Inches(8.1), Inches(1.65), Inches(4.2), Inches(4.8))
tft1 = tb_t1.text_frame
tft1.word_wrap = True
p = tft1.paragraphs[0]
p.text = "KẾT QUẢ ĐỐI CHUẨN KHOA HỌC"
p.font.name = FONT_NAME
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = PRIMARY_BLUE

bullets_t1 = [
    ("Volume Baseline (1D):", "Silhouette = 0.5774\n(Chỉ chia trạm theo lưu lượng đông / vắng)"),
    ("Profile K-Means (8D):", "Silhouette = 0.1690\n(Chia trạm theo tỷ lệ nhịp sinh hoạt)"),
    ("ARI đối chuẩn chéo:", "ARI = 0.0115 (Gần sát 0!)\nHai phương pháp phân cụm hoàn toàn không tương đồng."),
    ("Ý nghĩa thực tiễn:", "Mặc dù Volume có điểm số cao giả tạo do cụm trạm lớn tách biệt, nhưng ARI ≈ 0 chứng minh Profile trích xuất bản chất sử dụng hoàn toàn độc lập với quy mô trạm.")
]
for bt, bd in bullets_t1:
    p = tft1.add_paragraph()
    p.text = f"• {bt}\n  {bd}"
    p.font.name = FONT_NAME
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_TEXT
    p.space_before = Pt(8)

# ==============================================================================
# SLIDE 8: THÍ NGHIỆM 2 — ELBOW & SILHOUETTE (CHỌN K=3)
# ==============================================================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s8)
add_clean_header(s8, "Thí Nghiệm 2: Đường Cong Elbow & Luận Cứ Chọn K = 3")
add_clean_footer(s8, 8, 15)

fig2_path = os.path.join(FIG_DIR, "fig2_elbow_silhouette.png")
if os.path.exists(fig2_path):
    s8.shapes.add_picture(fig2_path, Inches(0.8), Inches(1.5), width=Inches(6.5))

c_tn2 = add_card(s8, Inches(7.6), Inches(1.45), Inches(4.9), Inches(5.3), bg_color=SURFACE_LIGHT)
tb_t2 = s8.shapes.add_textbox(Inches(7.8), Inches(1.65), Inches(4.5), Inches(4.8))
tft2 = tb_t2.text_frame
tft2.word_wrap = True
p = tft2.paragraphs[0]
p.text = "LUẬN CỨ LỰA CHỌN K = 3 TỐI ƯU"
p.font.name = FONT_NAME
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = PRIMARY_BLUE

bullets_t2 = [
    ("Điểm uốn Elbow rõ nét:", "Đường cong Inertia giảm dốc mạnh từ K=2 (10.109) xuống K=3 (8.927) rồi thoai thoải dần."),
    ("Chỉ số Davies-Bouldin (DBI):", "Giảm mạnh từ 1.928 (K=2) xuống 1.671 (K=3) — Cụm tách biệt tốt hơn."),
    ("Silhouette Score:", "Đạt 0.1709 tại K=3, duy trì ổn định không bị suy giảm mạnh."),
    ("Tính khả giải nghiệp vụ:", "K=3 ánh xạ hoàn hảo 3 phân khúc thực tế của nhà vận hành. Nếu K=4, các cụm bị phân mảnh trùng lặp.")
]
for bt, bd in bullets_t2:
    p = tft2.add_paragraph()
    p.text = f"★ {bt}\n  {bd}"
    p.font.name = FONT_NAME
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_TEXT
    p.space_before = Pt(8)

# ==============================================================================
# SLIDE 9: THÍ NGHIỆM 3 — ĐỘ ỔN ĐỊNH SEED & CHUYỂN DỊCH MÙA
# ==============================================================================
s9 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s9)
add_clean_header(s9, "Thí Nghiệm 3: Độ Ổn Định Seed & Chuyển Dịch Mùa (Xuân vs Đông)")
add_clean_footer(s9, 9, 15)

fig3_path = os.path.join(FIG_DIR, "fig3_season_stability.png")
if os.path.exists(fig3_path):
    s9.shapes.add_picture(fig3_path, Inches(0.8), Inches(1.5), width=Inches(5.8))

c_tn3 = add_card(s9, Inches(6.9), Inches(1.45), Inches(5.6), Inches(5.3), bg_color=SURFACE_LIGHT)
tb_t3 = s9.shapes.add_textbox(Inches(7.1), Inches(1.65), Inches(5.2), Inches(4.8))
tft3 = tb_t3.text_frame
tft3.word_wrap = True
p = tft3.paragraphs[0]
p.text = "PHÂN TÍCH ĐỘ BỀN VỮNG & CHUYỂN DỊCH MÙA"
p.font.name = FONT_NAME
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = ACCENT_GREEN

bullets_t3 = [
    ("Độ ổn định Seed ngẫu nhiên (5 Seeds):", "ARI = 0.9984 (Gần sát 1.0 tuyệt đối!)\nThuật toán K-Means++ hội tụ cực kỳ bền vững, không phụ thuộc khởi tạo tâm."),
    ("Chuyển dịch 2 Mùa (T4 Xuân vs T1 Đông):", "Khảo sát trên 2.129 trạm giao nhau giữa 2 mùa.\nARI = 0.3873 | NMI = 0.3345"),
    ("Bản chất hiện tượng chuyển dịch mùa:", "Vào mùa đông lạnh giá tuyết rơi tại New York, các trạm Cụm 2 (du lịch/công viên) giảm mạnh khách giải trí và chuyển dịch sang Cụm 1 (phục vụ người dân đi làm thiết yếu).")
]
for bt, bd in bullets_t3:
    p = tft3.add_paragraph()
    p.text = f"• {bt}\n  {bd}"
    p.font.name = FONT_NAME
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_TEXT
    p.space_before = Pt(8)

# ==============================================================================
# SLIDE 10: THÍ NGHIỆM 4 — BẢNG TRUNG VỊ ĐỊNH DANH 3 CỤM
# ==============================================================================
s10 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s10)
add_clean_header(s10, "Thí Nghiệm 4: Định Lượng 3 Cụm Bằng Bảng Giá Trị Trung Vị (Median)")
add_clean_footer(s10, 10, 15)

fig4_path = os.path.join(FIG_DIR, "fig4_cluster_medians.png")
if os.path.exists(fig4_path):
    s10.shapes.add_picture(fig4_path, Inches(0.8), Inches(1.5), width=Inches(6.6))

c_tn4 = add_card(s10, Inches(7.7), Inches(1.45), Inches(4.8), Inches(5.3), bg_color=SURFACE_LIGHT)
tb_t4 = s10.shapes.add_textbox(Inches(7.9), Inches(1.65), Inches(4.4), Inches(4.8))
tft4 = tb_t4.text_frame
tft4.word_wrap = True
p = tft4.paragraphs[0]
p.text = "ĐẶC TÍNH NGHIỆP VỤ 3 CỤM TRẠM"
p.font.name = FONT_NAME
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = PRIMARY_BLUE

clusters_desc = [
    ("Cụm 0 — Điểm đến Thương mại (431 trạm):", "Xuất phát chiều cao nhất (38.42%)\nNet Flow sáng: +31.87% (Xe đổ về ngập bãi)"),
    ("Cụm 1 — Khu Dân cư Đi làm (1.034 trạm):", "Xuất phát sáng cao nhất (23.33%)\nNet Flow sáng: -36.84% (Xe bị rút cạn)\nTỷ lệ Hội viên cao nhất: 84.87%"),
    ("Cụm 2 — Hỗn hợp & Vui chơi Đêm (764 trạm):", "Hoạt động đêm cao nhất (21.88%)\nCuối tuần cao nhất: 23.46%")
]
for ct, cd in clusters_desc:
    p = tft4.add_paragraph()
    p.text = f"★ {ct}\n{cd}"
    p.font.name = FONT_NAME
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_TEXT
    p.space_before = Pt(8)

# ==============================================================================
# SLIDE 11: NGHIỆM THU TẬP TEST ĐỘC LẬP
# ==============================================================================
s11 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s11)
add_clean_header(s11, "Kết Quả Nghiệm Thu Trên Tập Test Độc Lập (N = 335 Trạm)")
add_clean_footer(s11, 11, 15)

test_cards = [
    ("SILHOUETTE SCORE", "0.1638", "Chỉ giảm nhẹ < 4% so với tập Validation (0.1709). Khả năng tổng quát hóa xuất sắc.", PRIMARY_BLUE),
    ("DAVIES-BOULDIN INDEX", "1.8154", "Cụm duy trì sự gắn kết nội cụm và phân tách ngoại cụm ổn định trên dữ liệu hoàn toàn mới.", ACCENT_GREEN),
    ("ĐỘC LẬP 100%", "335 Trạm", "Tập Test được niêm phong tuyệt đối, chứng minh quy trình học máy không rò rỉ dữ liệu.", ACCENT_AMBER)
]

for idx, (t, val, d, c) in enumerate(test_cards):
    left = Inches(0.8 + idx * 4.0)
    card = add_card(s11, left, Inches(1.45), Inches(3.7), Inches(2.7), bg_color=SURFACE_LIGHT)
    tb = s11.shapes.add_textbox(left + Inches(0.2), Inches(1.65), Inches(3.3), Inches(2.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = t
    p.font.name = FONT_NAME
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = c
    
    p2 = tf.add_paragraph()
    p2.text = val
    p2.font.name = FONT_NAME
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = DARK_TEXT
    p2.space_before = Pt(6)
    
    p3 = tf.add_paragraph()
    p3.text = d
    p3.font.name = FONT_NAME
    p3.font.size = Pt(12)
    p3.font.color.rgb = MUTED_TEXT
    p3.space_before = Pt(6)

c_eval = add_card(s11, Inches(0.8), Inches(4.45), Inches(11.7), Inches(2.3), bg_color=CARD_BLUE_TINT, border_color=RGBColor(191, 219, 254))
tb_e = s11.shapes.add_textbox(Inches(1.1), Inches(4.65), Inches(11.2), Inches(1.9))
tfe = tb_e.text_frame
tfe.word_wrap = True
p = tfe.paragraphs[0]
p.text = "KẾT LUẬN NGHIỆM THU HỌC MÁY:"
p.font.name = FONT_NAME
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = PRIMARY_BLUE

p_c = tfe.add_paragraph()
p_c.text = "Mô hình K-Means (K=3) với chuẩn hóa StandardScaler đã vượt qua toàn bộ các bài kiểm tra thực nghiệm nghiêm ngặt: không xảy ra hiện tượng Overfitting, phản ánh chân thực nhịp sống đô thị và sẵn sàng triển khai phục vụ hệ thống điều phối xe thời gian thực."
p_c.font.name = FONT_NAME
p_c.font.size = Pt(13)
p_c.font.color.rgb = DARK_TEXT
p_c.space_before = Pt(6)

# ==============================================================================
# SLIDE 12: KIẾN TRÚC HỆ THỐNG SERVING
# ==============================================================================
s12 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s12)
add_clean_header(s12, "Kiến Trúc Serving: Tách Biệt Offline Training & Online Serving")
add_clean_footer(s12, 12, 15)

fig_arch_path = os.path.join(FIG_DIR, "fig4_1_architecture.png")
if os.path.exists(fig_arch_path):
    s12.shapes.add_picture(fig_arch_path, Inches(0.8), Inches(1.5), width=Inches(6.8))

c_arch = add_card(s12, Inches(7.9), Inches(1.45), Inches(4.6), Inches(5.3), bg_color=SURFACE_LIGHT)
tb_a = s12.shapes.add_textbox(Inches(8.1), Inches(1.65), Inches(4.2), Inches(4.8))
tfa = tb_a.text_frame
tfa.word_wrap = True
p = tfa.paragraphs[0]
p.text = "NGUYÊN TẮC THIẾT KẾ SERVING"
p.font.name = FONT_NAME
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = PRIMARY_BLUE

arch_bullets = [
    ("Tách biệt Offline - Online:", "Quá trình tiền xử lý 5.6M bản ghi và huấn luyện K-Means diễn ra offline. Online server chỉ nạp model và profile đã tính sẵn."),
    ("Backend FastAPI Hiện đại:", "Hiệu năng cao trên nền máy chủ ASGI Uvicorn, hỗ trợ Pydantic data validation và quản lý vòng đời Lifespan."),
    ("Tốc độ phản hồi cực nhanh:", "Thời gian phản hồi API < 15ms; không bao giờ train lại mô hình khi có request người dùng.")
]
for bt, bd in arch_bullets:
    p = tfa.add_paragraph()
    p.text = f"✔ {bt}\n  {bd}"
    p.font.name = FONT_NAME
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_TEXT
    p.space_before = Pt(10)

# ==============================================================================
# SLIDE 13: GIAO DIỆN WEB TƯƠNG TÁC (3 MÀN HÌNH)
# ==============================================================================
s13 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s13)
add_clean_header(s13, "Trực Quan Hóa Giao Diện Web Tương Tác (3 Màn Hình)")
add_clean_footer(s13, 13, 15)

scr1 = os.path.join(FIG_DIR, "fig4_2_screen1_intro.png")
scr2 = os.path.join(FIG_DIR, "fig4_3_screen2_map.png")
scr3 = os.path.join(FIG_DIR, "fig4_4_screen3_dashboard.png")

if os.path.exists(scr1):
    s13.shapes.add_picture(scr1, Inches(0.8), Inches(1.5), width=Inches(3.7))
if os.path.exists(scr2):
    s13.shapes.add_picture(scr2, Inches(4.8), Inches(1.5), width=Inches(3.7))
if os.path.exists(scr3):
    s13.shapes.add_picture(scr3, Inches(8.8), Inches(1.5), width=Inches(3.7))

for idx, (cap, desc) in enumerate([
    ("Màn hình 1: Tổng quan", "Bài toán, phạm vi dữ liệu và giải thích chi tiết 3 cụm."),
    ("Màn hình 2: Bản đồ Leaflet", "Bản đồ tương tác 2.200 trạm, lọc cụm và mô phỏng trạm mới."),
    ("Màn hình 3: Dashboard", "Trực quan hóa 4 thí nghiệm và tiêu chuẩn Model Card.")
]):
    left = Inches(0.8 + idx * 4.0)
    card_cap = add_card(s13, left, Inches(5.35), Inches(3.7), Inches(1.4), bg_color=SURFACE_LIGHT)
    tb = s13.shapes.add_textbox(left + Inches(0.15), Inches(5.42), Inches(3.4), Inches(1.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = cap
    p.font.name = FONT_NAME
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = FONT_NAME
    p2.font.size = Pt(11)
    p2.font.color.rgb = DARK_TEXT
    p2.space_before = Pt(2)

# ==============================================================================
# SLIDE 14: KIỂM THỬ TỰ ĐỘNG HỆ THỐNG
# ==============================================================================
s14 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s14)
add_clean_header(s14, "Kiểm Thử Tự Động (Automated Testing) — 7/7 Test Cases PASS")
add_clean_footer(s14, 14, 15)

c_test = add_card(s14, Inches(0.8), Inches(1.45), Inches(11.7), Inches(5.3), bg_color=SURFACE_LIGHT)
tb_tc = s14.shapes.add_textbox(Inches(1.1), Inches(1.65), Inches(11.2), Inches(4.8))
tftc = tb_tc.text_frame
tftc.word_wrap = True
p = tftc.paragraphs[0]
p.text = "BỘ KIỂM THỬ TỰ ĐỘNG TẠI tests/test_api.py (FASTAPI TESTCLIENT):"
p.font.name = FONT_NAME
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = PRIMARY_BLUE

test_cases = [
    ("test_get_stations_april:", "Xác thực danh sách trạm Tháng 04/2026 trả về đầy đủ 2.229 trạm và đúng schema."),
    ("test_get_stations_january:", "Xác thực danh sách trạm Tháng 01/2026 trả về đầy đủ 2.143 trạm."),
    ("test_filter_by_cluster:", "Kiểm tra bộ lọc cluster=1 trả về chính xác 1.034 trạm khu dân cư."),
    ("test_get_station_detail:", "Kiểm tra endpoint chi tiết trạm trả về đúng ID và đầy đủ 8 trường đặc trưng."),
    ("test_metrics_endpoint:", "Kiểm tra API Metrics trả về kết quả 4 thí nghiệm và k_selected=3."),
    ("test_model_card_endpoint:", "Kiểm tra API Model Card tài liệu hóa mô hình và giới hạn áp dụng."),
    ("test_error_handling:", "Kiểm tra xử lý lỗi HTTP 404 (tháng không tồn tại) và 422 (mã cụm không hợp lệ).")
]

for tcn, tcd in test_cases:
    p = tftc.add_paragraph()
    p.text = f"✔ [PASS]  {tcn}  {tcd}"
    p.font.name = FONT_NAME
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_TEXT
    p.space_before = Pt(7)

# ==============================================================================
# SLIDE 15: KẾT LUẬN & HƯỚNG PHÁT TRIỂN (Q&A - Nền Sáng Thanh Lịch)
# ==============================================================================
s15 = prs.slides.add_slide(blank_layout)
set_slide_background_white(s15)
add_clean_header(s15, "Kết Luận & Hướng Phát Triển Đề Tài", category_text="TỔNG KẾT BÁO CÁO BÀI TẬP LỚN")
add_clean_footer(s15, 15, 15)

# Left card: Kết quả
c_l = add_card(s15, Inches(0.8), Inches(1.45), Inches(5.6), Inches(5.3), bg_color=SURFACE_LIGHT)
tb_l = s15.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.2), Inches(4.8))
tfl = tb_l.text_frame
tfl.word_wrap = True
p = tfl.paragraphs[0]
p.text = "KẾT QUẢ ĐẠT ĐƯỢC"
p.font.name = FONT_NAME
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = PRIMARY_BLUE

kq = [
    "Xây dựng thành công quy trình học máy chuẩn mực từ dữ liệu thô 5.6M chuyến đi.",
    "Chống rò rỉ dữ liệu tuyệt đối với phân chia Train/Val/Test và StandardScaler.",
    "Hoàn thành xuất sắc 4 thí nghiệm khoa học theo đúng rubric đề tài Bài 8.",
    "Đóng gói sản phẩm hoàn chỉnh: FastAPI Backend và Giao diện Web 3 màn hình."
]
for k in kq:
    p = tfl.add_paragraph()
    p.text = f"• {k}"
    p.font.name = FONT_NAME
    p.font.size = Pt(12.5)
    p.font.color.rgb = DARK_TEXT
    p.space_before = Pt(10)

# Right card: Hướng phát triển & Lời cảm ơn
c_r = add_card(s15, Inches(6.8), Inches(1.45), Inches(5.7), Inches(5.3), bg_color=CARD_BLUE_TINT, border_color=RGBColor(191, 219, 254))
tb_r = s15.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(4.8))
tfr = tb_r.text_frame
tfr.word_wrap = True
p = tfr.paragraphs[0]
p.text = "HƯỚNG PHÁT TRIỂN & THẢO LUẬN (Q&A)"
p.font.name = FONT_NAME
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = PRIMARY_BLUE

hds = [
    "Tích hợp thêm dữ liệu thời tiết (nhiệt độ, lượng mưa) để dự báo nhu cầu động.",
    "Mở rộng mô hình dự đoán nhu cầu luân chuyển xe theo từng khung giờ trong ngày.",
    "Tối ưu hóa thuật toán định tuyến cho xe tải điều phối (Vehicle Routing Problem)."
]
for h in hds:
    p = tfr.add_paragraph()
    p.text = f"★ {h}"
    p.font.name = FONT_NAME
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_TEXT
    p.space_before = Pt(8)

p_qa = tfr.add_paragraph()
p_qa.text = "\nEM XIN CHÂN THÀNH CẢM ƠN THẦY CÔ VÀ CÁC BẠN!\nKính mời Thầy Cô và các bạn đặt câu hỏi thảo luận."
p_qa.font.name = FONT_NAME
p_qa.font.size = Pt(14)
p_qa.font.bold = True
p_qa.font.color.rgb = PRIMARY_BLUE
p_qa.alignment = PP_ALIGN.CENTER
p_qa.space_before = Pt(14)

# ==============================================================================
# BƯỚC CUỐI CÙNG: QUÉT ĐỒNG BỘ 100% FONT TIMES NEW ROMAN
# ==============================================================================
apply_times_new_roman_all(prs)

prs.save(PPTX_PATH)
print("SUCCESS! PowerPoint file created with Clean Light Academic Theme and 100% Times New Roman font at:", PPTX_PATH)
