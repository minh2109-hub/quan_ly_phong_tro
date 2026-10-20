"""
build_full_report.py - Toàn bộ nội dung đồ án hoàn chỉnh > 50 trang
"""
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC_PATH = r"c:\xampp\htdocs\QuanLyPhongTro\Mẫu báo cáo Đồ án website.docx"
OUT_PATH = r"c:\xampp\htdocs\QuanLyPhongTro\BaoCao_QuanLyPhongTro.docx"
IMG_DIR  = r"c:\xampp\htdocs\QuanLyPhongTro\assets\images"

doc = Document(SRC_PATH)

def set_font(run, name='Times New Roman', size=13, bold=False, italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)
    rPr = run._r.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:eastAsia'), name)
    rFonts.set(qn('w:ascii'), name)
    rFonts.set(qn('w:hAnsi'), name)
    rPr.insert(0, rFonts)

def add_chapter(doc, text):
    doc.add_page_break()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.line_spacing = 1.3
    run = p.add_run(text)
    set_font(run, size=15, bold=True, color=(30, 58, 138))
    return p

def add_sec1(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.3
    run = p.add_run(text)
    set_font(run, size=13.5, bold=True, color=(30, 58, 138))
    return p

def add_sec2(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(9)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.3
    run = p.add_run(text)
    set_font(run, size=13, bold=True, color=(15, 23, 42))
    return p

def add_sec3(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(7)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.3
    run = p.add_run(text)
    set_font(run, size=12.5, bold=True, italic=True, color=(51, 65, 85))
    return p

def add_p(doc, text, bold=False, italic=False, indent=True, center=False, size=13):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.JUSTIFY
    if indent and not center:
        p.paragraph_format.first_line_indent = Cm(1.27)
    p.paragraph_format.space_after = Pt(4.5)
    p.paragraph_format.line_spacing = 1.3
    run = p.add_run(text)
    set_font(run, size=size, bold=bold, italic=italic)
    return p

def add_bullet(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Cm(1.27)
    p.paragraph_format.first_line_indent = Cm(-0.63)
    p.paragraph_format.space_after = Pt(3.5)
    p.paragraph_format.line_spacing = 1.25
    run = p.add_run('•  ' + text)
    set_font(run, size=12.5)
    return p

def add_image(doc, filename, caption, width_in=4.6):
    path = os.path.join(IMG_DIR, filename)
    if os.path.exists(path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run()
        run.add_picture(path, width=Inches(width_in))
    else:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(f"[Hình ảnh: {filename}]")
        set_font(run, size=11, italic=True, color=(150, 150, 150))
    
    cp = doc.add_paragraph()
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cp.paragraph_format.space_after = Pt(8)
    r = cp.add_run(caption)
    set_font(r, size=11, bold=True, italic=True, color=(71, 85, 105))

def add_table(doc, headers, rows, caption=None):
    if caption:
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_before = Pt(6)
        cp.paragraph_format.space_after = Pt(4)
        r = cp.add_run(caption)
        set_font(r, size=11, bold=True, italic=True, color=(30, 58, 138))

    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tblPr = tbl._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for b_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{b_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '4')
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), 'CBD5E1')
        tblBorders.append(border)
    tblPr.append(tblBorders)
    tbl.autofit = True

    hr = tbl.rows[0]
    for i, h in enumerate(headers):
        c = hr.cells[i]
        c.text = ''
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(h)
        set_font(run, size=10, bold=True, color=(255, 255, 255))
        tcPr = c._tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), '1E3A8A')
        tcPr.append(shd)

    for ri, row in enumerate(rows):
        tr = tbl.rows[ri + 1]
        bg_fill = 'F8FAFC' if ri % 2 == 1 else 'FFFFFF'
        for ci, val in enumerate(row):
            c = tr.cells[ci]
            c.text = ''
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if ci == 0 and len(str(val)) < 6 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(2.5)
            p.paragraph_format.space_after = Pt(2.5)
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(str(val))
            set_font(run, size=9.5)
            if bg_fill != 'FFFFFF':
                tcPr = c._tc.get_or_add_tcPr()
                shd = OxmlElement('w:shd')
                shd.set(qn('w:val'), 'clear')
                shd.set(qn('w:color'), 'auto')
                shd.set(qn('w:fill'), bg_fill)
                tcPr.append(shd)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return tbl

def add_code(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.left_indent = Cm(0.8)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), 'F1F5F9')
    pPr.append(shd)
    run = p.add_run(text)
    run.font.name = 'Consolas'
    run.font.size = Pt(9)
    return p

print("1. Updating Cover and Front Matter...")

# Cover title
for p in doc.paragraphs[:30]:
    for run in p.runs:
        if 'điện thoại' in run.text.lower() or 'bán hàng' in run.text.lower() or 'đề tài:' in run.text.lower():
            run.text = '< ĐỀ TÀI: XÂY DỰNG WEBSITE QUẢN LÝ PHÒNG TRỌ >'

# TOC header
if len(doc.paragraphs) > 27:
    doc.paragraphs[27].text = 'MỤC LỤC'
    set_font(doc.paragraphs[27].runs[0], size=14, bold=True, color=(30, 58, 138))

toc_entries = [
    ("LỜI MỞ ĐẦU", 3, True),
    ("CHƯƠNG I. TÌM HIỂU NGÔN NGỮ PHP VÀ MYSQL", 5, True),
    ("  1.1 Ngôn ngữ lập trình PHP", 5, False),
    ("  1.2 Tại sao nên dùng PHP", 6, False),
    ("  1.3 Giới thiệu về ngôn ngữ PHP", 7, False),
    ("  2.1 Giới thiệu cơ sở dữ liệu MySQL", 8, False),
    ("  2.2 Mục đích sử dụng cơ sở dữ liệu", 9, False),
    ("CHƯƠNG II. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG", 10, True),
    ("  2.1 Tổng quan bài toán và khảo sát thực tế", 10, False),
    ("  2.2 Xác định yêu cầu hệ thống", 12, False),
    ("  2.3 Phân tích hệ thống theo mô hình Use Case", 15, False),
    ("  2.4 Biểu đồ luồng dữ liệu (DFD)", 25, False),
    ("  2.5 Biểu đồ tuần tự (Sequence Diagram)", 29, False),
    ("  2.6 Thiết kế kiến trúc hệ thống 3 tầng", 31, False),
    ("  2.7 Thiết kế cơ sở dữ liệu và từ điển dữ liệu", 33, False),
    ("CHƯƠNG III. XÂY DỰNG VÀ CÀI ĐẶT HỆ THỐNG", 62, True),
    ("  3.1 Cấu trúc thư mục dự án và tổ chức mã nguồn", 62, False),
    ("  3.2 Cài đặt kết nối cơ sở dữ liệu an toàn", 64, False),
    ("  3.3 Cài đặt chi tiết phân hệ Quản trị viên (Admin)", 66, False),
    ("  3.4 Cài đặt chi tiết phân hệ Khách thuê (User)", 80, False),
    ("CHƯƠNG IV. KIỂM THỬ VÀ ĐÁNH GIÁ KẾT QUẢ", 89, True),
    ("KẾT LUẬN VÀ KIẾN NGHỊ", 98, True),
    ("PHỤ LỤC", 100, True),
    ("TÀI LIỆU THAM KHẢO", 106, True)
]

for idx, (title, page_num, is_bold) in enumerate(toc_entries):
    p_num = 28 + idx
    if p_num < 52 and p_num < len(doc.paragraphs):
        p = doc.paragraphs[p_num]
        p.text = ''
        dots_count = max(4, 46 - len(title))
        dots = '.' * dots_count
        run_title = p.add_run(f"{title} {dots} ")
        set_font(run_title, size=10, bold=is_bold, color=(30, 58, 138) if is_bold else (15, 23, 42))
        run_page = p.add_run(str(page_num))
        set_font(run_page, size=10, bold=is_bold, color=(30, 58, 138) if is_bold else (15, 23, 42))
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1.5)

# Introduction text
mo_dau_text = (
    "Hiện nay, cùng với sự phát triển mạnh mẽ của nền kinh tế và tốc độ đô thị hóa nhanh chóng tại các đô thị lớn, "
    "nhu cầu thuê nhà trọ, căn hộ mini và phòng trọ của sinh viên, người lao động và các gia đình trẻ ngày càng gia tăng. "
    "Tuy nhiên, đại đa số các chủ nhà trọ hiện nay vẫn đang áp dụng phương pháp quản lý truyền thống thông qua ghi chép "
    "sổ sách thủ công hoặc sử dụng các bảng tính Excel rời rạc. Phương thức quản lý thủ công này bộc lộ rất nhiều bất cập "
    "nghiêm trọng: dễ thất lạc dữ liệu, tốn nhiều thời gian và công sức ghi chỉ số điện nước hàng tháng, thường xuyên xảy ra "
    "sai sót trong quá trình tính toán cộng dồn hóa đơn, khó khăn trong việc theo dõi hạn hợp đồng thuê phòng, và đặc biệt "
    "là thiếu kênh tương tác hai chiều kịp thời giữa chủ trọ và khách thuê khi phát sinh sự cố kỹ thuật hỏng hóc.\n\n"
    "Xuất phát từ nhu cầu thực tiễn cấp thiết đó, đề tài “Xây dựng Website Quản Lý Phòng Trọ” được triển khai nhằm số hóa "
    "toàn diện quy trình vận hành khu nhà trọ. Ứng dụng được xây dựng trên nền tảng web PHP 8+ kết hợp hệ quản trị cơ sở "
    "dữ liệu MySQL và thư viện giao diện hiện đại Bootstrap 5, mang lại giải pháp quản trị tập trung, tự động hóa tính toán "
    "điện nước, lập hóa đơn, ghi nhận lịch sử thanh toán và tiếp nhận báo hỏng trực tuyến. Bản báo cáo đồ án này trình bày "
    "chi tiết từ cơ sở lý thuyết, phân tích thiết kế, cài đặt mã nguồn cho đến kiểm thử và đánh giá kết quả thực nghiệm."
)
if len(doc.paragraphs) > 54:
    doc.paragraphs[54].text = mo_dau_text
    set_font(doc.paragraphs[54].runs[0], size=12.5)

# Remove old Chapter II onwards
to_del = []
found_ch2 = False
for p in doc.paragraphs:
    if not found_ch2 and ('Chương II' in p.text or 'chương II' in p.text.lower()):
        found_ch2 = True
    if found_ch2:
        to_del.append(p)

for p in to_del:
    p._element.getparent().remove(p._element)

print("2. Writing Chapter II: Analysis and Design...")

add_chapter(doc, "CHƯƠNG II: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG")

add_sec1(doc, "2.1. Tổng Quan Bài Toán Và Khảo Sát Thực Tế")
add_sec2(doc, "2.1.1. Bối cảnh thực tiễn và những bất cập trong quản lý truyền thống")
add_p(doc, "Trong xu thế phát triển đô thị hiện đại, các khu nhà trọ, dãy phòng trọ cho thuê mọc lên ngày càng nhiều nhằm đáp ứng nhu cầu lưu trú của đông đảo học sinh, sinh viên và người lao động ngoại tỉnh. Tuy nhiên, qua khảo sát thực tế tại các khu nhà trọ trên địa bàn các thành phố lớn, mô hình quản lý của các chủ nhà trọ vẫn chủ yếu mang tính tự phát và thủ công. Quy trình làm việc hàng ngày thường bao gồm việc ghi chép thông tin cá nhân của người thuê vào sổ tay, sử dụng giấy tờ biên lai tự viết khi thu tiền phòng, và kiểm tra công tơ điện nước vào cuối mỗi tháng bằng cách ghi chép số liệu trên giấy nháp.")
add_p(doc, "Phương thức vận hành thủ công này tồn tại hàng loạt nhược điểm cố hữu:")
add_bullet(doc, "Thất lạc và phân tán thông tin: Hồ sơ cá nhân của người thuê, chứng minh nhân dân/CCCD, thông tin hợp đồng thường bị lưu trữ rải rác, dễ bị rách nát, mất mát sau thời gian dài.")
add_bullet(doc, "Sai sót trong tính toán chi phí: Việc tính toán tiền điện, tiền nước tiêu thụ, tiền dịch vụ rác thải, wifi, gửi xe và tiền thuê phòng cho hàng chục phòng trọ mỗi tháng bằng máy tính cầm tay tốn rất nhiều thời gian và rất dễ xảy ra nhầm lẫn, dẫn đến tranh chấp giữa chủ trọ và khách thuê.")
add_bullet(doc, "Khó khăn trong theo dõi công nợ: Chủ trọ khó kiểm soát chính xác ai đã thanh toán, ai chưa thanh toán, ai nợ bao nhiêu tiền và hóa đơn nào đã quá hạn đóng tiền.")
add_bullet(doc, "Thiếu minh bạch và kênh tương tác: Khách thuê không thể chủ động tra cứu chỉ số điện nước cũ/mới, không nắm được chi tiết từng khoản cấu thành hóa đơn, và gặp nhiều phiền toái khi cần phản ánh các sự cố hỏng hóc đường ống nước, cháy bóng đèn hay hỏng khóa cửa.")

add_sec2(doc, "2.1.2. Mục tiêu nghiên cứu và giải pháp đề xuất")
add_p(doc, "Mục tiêu then chốt của đề tài là xây dựng một hệ thống phần mềm web hoàn chỉnh, dễ sử dụng, ổn định và bảo mật cao nhằm tin học hóa toàn diện quy trình quản lý nhà trọ. Hệ thống đóng vai trò như một cầu nối số hóa hiện đại giữa chủ trọ và người thuê phòng:")
add_bullet(doc, "Đối với chủ trọ: Cung cấp bảng điều khiển trung tâm giúp nắm bắt tức thời toàn bộ tình hình kinh doanh (tỷ lệ phòng trống/đang thuê, doanh thu lũy kế, công nợ tồn đọng, sự cố kỹ thuật cần xử lý); tự động hóa nghiệp vụ chốt số điện nước và phát hành hóa đơn.")
add_bullet(doc, "Đối với khách thuê: Cung cấp portal cá nhân hóa trên trình duyệt web, cho phép xem chi tiết hợp đồng, theo dõi lịch sử hóa đơn chi tiết, tra cứu chỉ số điện nước minh bạch và gửi yêu cầu sửa chữa tức thì.")

add_sec1(doc, "2.2. Xác Định Yêu Cầu Hệ Thống")
add_sec2(doc, "2.2.1. Yêu cầu chức năng (Functional Requirements)")
add_p(doc, "Dựa trên kết quả khảo sát và phân tích nghiệp vụ thực tế, hệ thống được phân rã thành hai phân hệ lớn tương ứng với hai vai trò người dùng trong hệ thống:")

add_table(doc,
    ["STT", "Phân Hệ", "Mã Chức Năng", "Tên Chức Năng", "Mô Tả Nghiệp Vụ Chi Tiết"],
    [
        ["1", "Quản Trị (Admin)", "F-ADM-01", "Đăng nhập & Xác thực", "Xác thực danh tính chủ trọ qua username/password, cấp phiên làm việc."],
        ["2", "Quản Trị (Admin)", "F-ADM-02", "Dashboard tổng quan", "Hiển thị 8 thẻ chỉ số KPI, biểu đồ doanh thu, biểu đồ phòng, sự cố mới."],
        ["3", "Quản Trị (Admin)", "F-ADM-03", "Quản lý phòng trọ", "CRUD phòng, phân loại tầng/khu, quản lý giá thuê, tiền cọc, trạng thái phòng."],
        ["4", "Quản Trị (Admin)", "F-ADM-04", "Quản lý người thuê", "CRUD thông tin khách thuê, số CCCD, SĐT, liên kết người thuê với phòng."],
        ["5", "Quản Trị (Admin)", "F-ADM-05", "Quản lý hợp đồng", "Lập hợp đồng thuê, quản lý thời hạn, tự động cảnh báo hợp đồng sắp hết hạn."],
        ["6", "Quản Trị (Admin)", "F-ADM-06", "Quản lý điện nước", "Nhập chỉ số điện/nước hàng tháng, tự động tính tiền theo đơn giá thiết lập."],
        ["7", "Quản Trị (Admin)", "F-ADM-07", "Quản lý dịch vụ", "Định nghĩa bảng giá dịch vụ dùng chung: internet, vệ sinh, rác, gửi xe."],
        ["8", "Quản Trị (Admin)", "F-ADM-08", "Quản lý hóa đơn", "Tự động lập hóa đơn tổng hợp theo tháng, hỗ trợ xem chi tiết và in phiếu thu."],
        ["9", "Quản Trị (Admin)", "F-ADM-09", "Quản lý thanh toán", "Ghi nhận giao dịch nộp tiền, tự động cập nhật hóa đơn sang 'Đã thanh toán'."],
        ["10", "Quản Trị (Admin)", "F-ADM-10", "Quản lý sự cố", "Tiếp nhận thông tin báo hỏng, cập nhật quy trình xử lý 4 bước đến hoàn thành."],
        ["11", "Quản Trị (Admin)", "F-ADM-11", "Quản lý tài khoản", "Tạo tài khoản người dùng, đổi mật khẩu, kích hoạt hoặc khóa tài khoản."],
        ["12", "Quản Trị (Admin)", "F-ADM-12", "Thống kê báo cáo", "Biểu đồ cột doanh thu 12 tháng, so sánh điện nước, top phòng doanh thu cao."],
        ["13", "Khách Thuê (User)", "F-USR-01", "Dashboard khách thuê", "Xem tổng quan phòng đang ở, số tiền cần đóng, hạn thanh toán, sự cố."],
        ["14", "Khách Thuê (User)", "F-USR-02", "Xem phòng của tôi", "Tra cứu thông tin phòng đang thuê: diện tích, giá thuê, người cùng phòng."],
        ["15", "Khách Thuê (User)", "F-USR-03", "Tra cứu hợp đồng", "Xem chi tiết hợp đồng, thời hạn thuê, thanh tiến trình thời gian hợp đồng."],
        ["16", "Khách Thuê (User)", "F-USR-04", "Lịch sử điện nước", "Tra cứu lịch sử chỉ số công tơ điện và đồng hồ nước từng tháng."],
        ["17", "Khách Thuê (User)", "F-USR-05", "Tra cứu hóa đơn", "Xem danh sách hóa đơn theo tháng, chi tiết cấu thành tổng tiền, cảnh báo quá hạn."],
        ["18", "Khách Thuê (User)", "F-USR-06", "Lịch sử thanh toán", "Theo dõi lịch sử các lần đã nộp tiền, ngày thanh toán, phương thức đóng tiền."],
        ["19", "Khách Thuê (User)", "F-USR-07", "Gửi yêu cầu sự cố", "Gửi phản ánh hỏng hóc kèm mức độ khẩn cấp, theo dõi tiến độ sửa chữa."],
        ["20", "Khách Thuê (User)", "F-USR-08", "Quản lý hồ sơ", "Xem thông tin cá nhân, cập nhật số điện thoại, email và đổi mật khẩu."]
    ],
    "Bảng 2.1: Bảng tổng hợp yêu cầu chức năng hệ thống"
)

add_sec2(doc, "2.2.2. Yêu cầu phi chức năng (Non-Functional Requirements)")
add_p(doc, "Hệ thống cần thỏa mãn các tiêu chuẩn kỹ thuật nghiêm ngặt nhằm đảm bảo khả năng ứng dụng thực tế lâu dài:")
add_bullet(doc, "Bảo mật dữ liệu (Security): Mật khẩu phải được băm một chiều an toàn bằng thuật toán Bcrypt; toàn bộ các câu lệnh truy vấn dữ liệu phải sử dụng Prepared Statements để loại trừ triệt để nguy cơ tấn công SQL Injection; quản lý phiên làm việc bằng PHP Session có cơ chế kiểm tra quyền chặt chẽ.")
add_bullet(doc, "Hiệu năng và độ tin cậy (Performance & Reliability): Thời gian phản hồi của trang không vượt quá 1.5 giây trong điều kiện mạng bình thường; cơ sở dữ liệu được tối ưu bằng các chỉ mục (Indexes) trên các trường khóa ngoại và các trường thường xuyên tìm kiếm.")
add_bullet(doc, "Tính toàn vẹn dữ liệu (Data Integrity): Thiết lập khóa chính (Primary Key), khóa ngoại (Foreign Key) với các ràng buộc kiểm tra logic (ví dụ chỉ số điện mới không được nhỏ hơn chỉ số cũ, không cho phép xóa phòng đang có người thuê).")
add_bullet(doc, "Giao diện và tính tiện dụng (UI/UX): Thiết kế theo phong cách hiện đại với gam màu chủ đạo xanh dương - trắng - xám; bố cục thích ứng (Responsive Layout) tương thích mượt mà trên Desktop, Laptop, Máy tính bảng và Điện thoại di động.")

add_sec2(doc, "2.2.3. Ma trận phân quyền RBAC (Role-Based Access Control)")
add_p(doc, "Để bảo vệ các tài nguyên quản trị và ngăn chặn hành vi truy cập trái phép, hệ thống áp dụng mô hình phân quyền dựa trên vai trò (RBAC). Ma trận phân quyền được thể hiện cụ thể trong bảng dưới đây:")

add_table(doc,
    ["Mã Nghiệp Vụ", "Tên Nghiệp Vụ / Tài Nguyên", "Khách Thuê (User)", "Quản Trị Viên (Admin)"],
    [
        ["RBAC-01", "Truy cập Dashboard Quản trị", "Từ chối (Cấm truy cập)", "Toàn quyền (Xem thống kê, biểu đồ)"],
        ["RBAC-02", "Quản lý thông tin phòng trọ", "Không có quyền", "Toàn quyền (Thêm, sửa, xóa, tìm kiếm)"],
        ["RBAC-03", "Xem phòng đang thuê của mình", "Chỉ xem thông tin phòng mình", "Toàn quyền"],
        ["RBAC-04", "Quản lý hồ sơ người thuê", "Không có quyền", "Toàn quyền (Thêm, sửa, xóa, lọc)"],
        ["RBAC-05", "Quản lý hợp đồng cho thuê", "Chỉ xem hợp đồng của mình", "Toàn quyền (Tạo mới, thanh lý, sửa)"],
        ["RBAC-06", "Nhập và tính toán điện nước", "Chỉ xem lịch sử số phòng mình", "Toàn quyền nhập chỉ số các phòng"],
        ["RBAC-07", "Quản lý danh mục dịch vụ", "Không có quyền", "Toàn quyền (Thêm giá, sửa dịch vụ)"],
        ["RBAC-08", "Lập và phát hành hóa đơn", "Chỉ xem hóa đơn phòng mình", "Toàn quyền lập, sửa, xóa hóa đơn"],
        ["RBAC-09", "In phiếu thu hóa đơn", "Không có quyền", "Toàn quyền in phiếu thu giao khách"],
        ["RBAC-10", "Ghi nhận thanh toán tiền", "Chỉ xem lịch sử đã nộp", "Toàn quyền tạo phiếu thanh toán"],
        ["RBAC-11", "Gửi yêu cầu báo sự cố", "Được phép tạo yêu cầu", "Tiếp nhận và cập nhật tiến độ xử lý"],
        ["RBAC-12", "Quản lý tài khoản hệ thống", "Chỉ được đổi mật khẩu cá nhân", "Toàn quyền cấp tài khoản, khóa tài khoản"],
        ["RBAC-13", "Báo cáo thống kê doanh thu", "Không có quyền", "Toàn quyền xem biểu đồ & báo cáo năm"]
    ],
    "Bảng 2.2: Ma trận phân quyền RBAC chi tiết trong hệ thống"
)

add_sec1(doc, "2.3. Phân Tích Hệ Thống Theo Mô Hình Use Case")
add_sec2(doc, "2.3.1. Sơ đồ Use Case tổng quát")
add_p(doc, "Mô hình Use Case thể hiện trực quan mối tương tác giữa các tác nhân (Actors) bên ngoài và các ca sử dụng (Use Cases) của hệ thống. Hệ thống có hai Actor chính là Admin (Quản trị viên / Chủ trọ) và Khách thuê (Người thuê phòng).")

add_image(doc, "sodo_usecase_tongquat.png", "Hình 2.1: Sơ đồ Use Case tổng quát hệ thống Quản Lý Phòng Trọ")

add_sec2(doc, "2.3.2. Đặc tả chi tiết các Use Case trọng tâm")
add_p(doc, "Dưới đây là bảng đặc tả chi tiết các Use Case quan trọng nhất của hệ thống, bao gồm tiền điều kiện, hậu điều kiện, luồng sự kiện chính và luồng sự kiện ngoại lệ:")

add_table(doc,
    ["Thuộc Tính", "Nội Dung Đặc Tả"],
    [
        ["Tên Use Case", "UC01: Đăng nhập hệ thống"],
        ["Tác nhân (Actor)", "Admin, Khách Thuê"],
        ["Mục đích", "Xác thực danh tính người dùng và cấp phiên làm việc tương ứng với quyền hạn."],
        ["Tiền điều kiện", "Người dùng truy cập vào trang login.php và đã có tài khoản được cấp."],
        ["Hậu điều kiện", "Khởi tạo Session đăng nhập; điều hướng người dùng tới Dashboard phù hợp."],
        ["Luồng sự kiện chính", "1. Người dùng nhập Tên đăng nhập (username) và Mật khẩu (password).\n2. Người dùng nhấn nút 'Đăng Nhập'.\n3. Hệ thống kiểm tra dữ liệu không để trống.\n4. Hệ thống truy vấn CSDL theo username bằng Prepared Statement.\n5. Hệ thống xác thực mật khẩu bằng hàm password_verify().\n6. Nếu hợp lệ: Lưu thông tin vào $_SESSION, cập nhật thời gian đăng nhập.\n7. Nếu vai trò là 'admin', chuyển hướng tới /admin/dashboard.php.\n8. Nếu vai trò là 'khach_thue', chuyển hướng tới /user/dashboard.php."],
        ["Luồng ngoại lệ", "• Người dùng để trống trường thông tin: Hệ thống báo lỗi yêu cầu nhập đầy đủ.\n• Sai tên đăng nhập hoặc mật khẩu: Hệ thống hiển thị cảnh báo đỏ.\n• Tài khoản đang bị khóa (trang_thai = 'khoa'): Hệ thống từ chối đăng nhập."]
    ],
    "Bảng 2.3: Đặc tả Use Case UC01 - Đăng nhập hệ thống"
)

add_table(doc,
    ["Thuộc Tính", "Nội Dung Đặc Tả"],
    [
        ["Tên Use Case", "UC05: Quản lý phòng trọ"],
        ["Tác nhân (Actor)", "Admin (Chủ trọ)"],
        ["Mục đích", "Cho phép Admin thêm mới phòng, cập nhật thông tin phòng, xem danh sách và xóa phòng."],
        ["Tiền điều kiện", "Admin đã đăng nhập thành công vào hệ thống."],
        ["Hậu điều kiện", "Dữ liệu phòng trong bảng rooms được thêm mới hoặc cập nhật chính xác."],
        ["Luồng sự kiện chính", "1. Admin truy cập trang Quản lý phòng (admin/phong.php).\n2. Hệ thống tải danh sách phòng kèm trạng thái, số người ở hiện tại, giá thuê.\n3. Thêm mới: Admin nhấn 'Thêm Phòng', điền mã phòng, loại phòng, tầng, diện tích, giá thuê, tiền cọc, số người tối đa, nhấn 'Lưu'.\n4. Sửa: Admin nhấn icon 'Sửa', modal tự động điền dữ liệu phòng, Admin chỉnh sửa và nhấn 'Lưu'.\n5. Xóa: Admin nhấn icon 'Xóa', xác nhận hộp thoại cảnh báo của trình duyệt."],
        ["Luồng ngoại lệ", "• Mã phòng đã tồn tại: Hệ thống hiển thị thông báo lỗi trùng mã phòng.\n• Xóa phòng đang có người thuê: Hệ thống ngăn chặn xóa và thông báo yêu cầu chuyển khách trước."]
    ],
    "Bảng 2.4: Đặc tả Use Case UC05 - Quản lý phòng trọ"
)

add_table(doc,
    ["Thuộc Tính", "Nội Dung Đặc Tả"],
    [
        ["Tên Use Case", "UC11: Nhập và tính tiền điện nước"],
        ["Tác nhân (Actor)", "Admin (Chủ trọ)"],
        ["Mục đích", "Nhập số công tơ điện và đồng hồ nước hàng tháng, hệ thống tự động tính thành tiền."],
        ["Tiền điều kiện", "Phòng đã tồn tại trong hệ thống; Admin chọn đúng tháng và năm chốt số."],
        ["Hậu điều kiện", "Bản ghi điện nước được lưu vào bảng electric_water, sẵn sàng để tổng hợp vào hóa đơn."],
        ["Luồng sự kiện chính", "1. Admin truy cập trang Điện nước (admin/dien_nuoc.php).\n2. Admin nhấn nút 'Nhập Điện Nước'.\n3. Admin chọn phòng, chọn tháng/năm, nhập chỉ số điện cũ, chỉ số điện mới, đơn giá điện; nhập chỉ số nước cũ, chỉ số nước mới, đơn giá nước.\n4. JavaScript tự động tính tức thời số điện dùng, tiền điện, số nước dùng, tiền nước và tổng cộng.\n5. Admin kiểm tra số liệu và nhấn 'Lưu Dữ Liệu'.\n6. Hệ thống thực hiện Prepared Statement lưu vào bảng electric_water."],
        ["Luồng ngoại lệ", "• Chỉ số mới nhỏ hơn chỉ số cũ: Hệ thống báo lỗi không hợp lệ.\n• Đã nhập chỉ số cho phòng này trong tháng: Hệ thống yêu cầu chỉnh sửa bản ghi cũ thay vì tạo mới."]
    ],
    "Bảng 2.5: Đặc tả Use Case UC11 - Nhập và tính tiền điện nước"
)

add_table(doc,
    ["Thuộc Tính", "Nội Dung Đặc Tả"],
    [
        ["Tên Use Case", "UC13: Lập và quản lý hóa đơn"],
        ["Tác nhân (Actor)", "Admin (Chủ trọ)"],
        ["Mục đích", "Tự động tổng hợp chi phí tiền phòng, tiền điện, tiền nước, tiền dịch vụ thành hóa đơn hoàn chỉnh."],
        ["Tiền điều kiện", "Phòng đang có người thuê và đã có số liệu điện nước của tháng tương ứng."],
        ["Hậu điều kiện", "Hóa đơn được lưu vào bảng invoices với trạng thái ban đầu là 'Chưa thanh toán'."],
        ["Luồng sự kiện chính", "1. Admin truy cập trang Hóa đơn (admin/hoa_don.php).\n2. Admin nhấn 'Tạo Hóa Đơn'.\n3. Admin chọn phòng: hệ thống tự động điền khách thuê và giá phòng theo hợp đồng.\n4. Admin nhập số tiền điện, tiền nước (hoặc lấy từ bảng điện nước), tiền dịch vụ và phụ phí khác.\n5. Hệ thống tính tự động: Tổng tiền = Tiền phòng + Điện + Nước + Dịch vụ + Phí khác.\n6. Admin thiết lập hạn thanh toán (mặc định +7 ngày) và nhấn 'Lưu Hóa Đơn'.\n7. Admin có thể chọn xem bản in (hoa_don_in.php) để in phiếu gửi khách thuê."],
        ["Luồng ngoại lệ", "• Thiếu thông tin người thuê hoặc phòng: Hệ thống thông báo bắt buộc điền."]
    ],
    "Bảng 2.6: Đặc tả Use Case UC13 - Lập và quản lý hóa đơn"
)

add_table(doc,
    ["Thuộc Tính", "Nội Dung Đặc Tả"],
    [
        ["Tên Use Case", "UC16: Gửi và xử lý phản ánh sự cố"],
        ["Tác nhân (Actor)", "Khách thuê (gửi) và Admin (xử lý)"],
        ["Mục đích", "Kênh tiếp nhận báo hỏng hóc thiết bị và cập nhật tiến độ sửa chữa hai chiều."],
        ["Tiền điều kiện", "Khách thuê đã đăng nhập và đang có phòng thuê hợp lệ."],
        ["Hậu điều kiện", "Yêu cầu sự cố được cập nhật tiến độ từ 'Mới gửi' đến 'Đã hoàn thành'."],
        ["Luồng sự kiện chính", "1. Khách thuê vào trang user/su_co.php, nhập tiêu đề sự cố, mô tả chi tiết, chọn mức độ khẩn cấp (Thấp/Bình thường/Cao/Khẩn cấp), nhấn 'Gửi yêu cầu'.\n2. Hệ thống lưu bản ghi vào maintenance_requests với trạng thái 'moi_gui'.\n3. Admin xem danh sách sự cố trên admin/su_co.php, thấy sự cố mới nổi bật.\n4. Admin chuyển trạng thái: 'Đã tiếp nhận' -> 'Đang xử lý' kèm ghi chú phân công thợ sửa.\n5. Sau khi sửa xong, Admin chuyển trạng thái 'Đã hoàn thành' kèm ghi chú chi phí/kết quả.\n6. Khách thuê kiểm tra trang cá nhân thấy trạng thái đã hoàn tất."]
    ],
    "Bảng 2.7: Đặc tả Use Case UC16 - Gửi và xử lý sự cố sửa chữa"
)

add_sec1(doc, "2.4. Biểu Đồ Luồng Dữ Liệu (Data Flow Diagram - DFD)")
add_sec2(doc, "2.4.1. Biểu đồ ngữ cảnh DFD Mức 0")
add_p(doc, "Biểu đồ luồng dữ liệu mức 0 (Context Diagram) mô tả toàn bộ hệ thống dưới dạng một tiến trình duy nhất (Tiến trình 0), làm rõ các luồng dữ liệu trao đổi giữa hệ thống với hai thực thể ngoài là Quản Trị Viên (Admin) và Khách Thuê.")

add_image(doc, "sodo_dfd_muc0.png", "Hình 2.2: Sơ đồ luồng dữ liệu DFD mức 0 (Biểu đồ ngữ cảnh)")

add_p(doc, "Phân tích luồng dữ liệu mức 0:")
add_bullet(doc, "Luồng từ Admin vào hệ thống: Thông tin phòng trọ, hồ sơ người thuê, hợp đồng, đơn giá và chỉ số điện nước, phiếu thu thanh toán, phản hồi xử lý sự cố.")
add_bullet(doc, "Luồng từ hệ thống trả về Admin: Báo cáo doanh thu, tình trạng phòng, danh sách hóa đơn nợ đọng, danh sách sự cố phát sinh từ người thuê.")
add_bullet(doc, "Luồng từ Khách thuê vào hệ thống: Thông tin xác thực đăng nhập, yêu cầu báo hỏng sự cố, yêu cầu đổi mật khẩu.")
add_bullet(doc, "Luồng từ hệ thống trả về Khách thuê: Thông báo hóa đơn tiền phòng hàng tháng, lịch sử chỉ số điện nước, tình trạng hợp đồng, kết quả xử lý báo hỏng.")

add_sec2(doc, "2.4.2. Biểu đồ DFD Mức 1 - Phân rã tiến trình")
add_p(doc, "Biểu đồ DFD mức 1 phân rã hệ thống thành 6 tiến trình con chính cùng với 6 kho dữ liệu (Data Stores D1 - D6) tương ứng:")

add_image(doc, "sodo_dfd_muc1.png", "Hình 2.3: Sơ đồ luồng dữ liệu DFD mức 1")

add_p(doc, "Các tiến trình trong DFD mức 1 bao gồm:")
add_bullet(doc, "Tiến trình 1.0 (Quản lý xác thực): Tiếp nhận thông tin đăng nhập, xác thực qua kho dữ liệu D1 (users), phân quyền điều hướng.")
add_bullet(doc, "Tiến trình 2.0 (Quản lý phòng & người thuê): Thực hiện thêm/sửa/xóa phòng, cập nhật hồ sơ khách thuê và hợp đồng qua kho dữ liệu D2 (rooms, tenants, contracts).")
add_bullet(doc, "Tiến trình 3.0 (Quản lý điện nước & dịch vụ): Tiếp nhận số đo công tơ, tính tiền theo đơn giá lưu tại kho D3 (electric_water, services).")
add_bullet(doc, "Tiến trình 4.0 (Quản lý hóa đơn & thanh toán): Tổng hợp các chi phí, lập hóa đơn, ghi nhận thanh toán tại kho D4 (invoices, payments).")
add_bullet(doc, "Tiến trình 5.0 (Quản lý sự cố kỹ thuật): Tiếp nhận báo hỏng từ khách, cập nhật quy trình giải quyết tại kho D5 (maintenance_requests).")
add_bullet(doc, "Tiến trình 6.0 (Thống kê báo cáo): Khai thác dữ liệu tổng hợp từ các kho để lập biểu đồ doanh thu và báo cáo hoạt động.")

add_sec1(doc, "2.5. Biểu Đồ Tuần Tự (Sequence Diagram)")
add_sec2(doc, "2.5.1. Sơ đồ tuần tự chức năng Đăng nhập & Phân quyền")
add_p(doc, "Biểu đồ tuần tự mô tả các thông điệp trao đổi theo trình tự thời gian giữa Người dùng (Client), Trình xử lý nghiệp vụ (login.php) và Cơ sở dữ liệu (MySQL).")

add_image(doc, "sodo_sequence_login.png", "Hình 2.4: Sơ đồ tuần tự chức năng Đăng nhập và Phân quyền")

add_sec2(doc, "2.5.2. Phân tích luồng xử lý tự động hóa hóa đơn và thanh toán")
add_p(doc, "Quy trình lập hóa đơn và thanh toán được thiết kế khép kín nhằm loại bỏ hoàn toàn các sai số thủ công:")
add_bullet(doc, "Bước 1: Khi đến kỳ chốt sổ cuối tháng, Admin nhập chỉ số điện và nước mới. Hệ thống tự động lấy chỉ số cũ đã lưu của tháng trước, tính mức tiêu thụ chênh lệch và nhân với đơn giá.")
add_bullet(doc, "Bước 2: Khi tạo hóa đơn cho phòng, hệ thống tự động trích xuất tiền phòng từ hợp đồng đang hiệu lực, tiền điện nước từ bản ghi tháng tương ứng, và tiền dịch vụ đăng ký.")
add_bullet(doc, "Bước 3: Tổng tiền hóa đơn = Tiền phòng + Tiền điện + Tiền nước + Tiền dịch vụ + Phí phát sinh. Hóa đơn lưu ở trạng thái 'chua_thanh_toan'.")
add_bullet(doc, "Bước 4: Khi khách thuê nộp tiền, Admin lập phiếu thanh toán. Hệ thống đối soát tổng tiền đã nộp với tổng hóa đơn: nếu số tiền thanh toán >= tổng tiền hóa đơn, trạng thái hóa đơn tự động chuyển thành 'da_thanh_toan'.")

add_sec1(doc, "2.6. Thiết Kế Kiến Trúc Hệ Thống")
add_p(doc, "Hệ thống được xây dựng theo kiến trúc 3 tầng (3-Tier Architecture) kinh điển trong phát triển ứng dụng web, đảm bảo sự tách bạch rõ ràng giữa giao diện, nghiệp vụ và dữ liệu:")

add_image(doc, "sodo_kientruc.png", "Hình 2.5: Sơ đồ kiến trúc 3 tầng hệ thống Quản Lý Phòng Trọ")

add_bullet(doc, "Tầng 1 - Presentation Layer (Giao diện người dùng): Chạy trực tiếp trên trình duyệt của người dùng (Client-Side). Sử dụng HTML5, CSS3, JavaScript ES6 và framework Bootstrap 5.3 để xây dựng giao diện responsive thích ứng. Tích hợp thư viện Chart.js để vẽ biểu đồ và Font Awesome 6 cho hệ thống biểu tượng.")
add_bullet(doc, "Tầng 2 - Application Layer (Tầng xử lý ứng dụng): Chạy trên Web Server Apache 2.4. Mã nguồn backend được lập trình bằng ngôn ngữ PHP 8+. Đảm nhiệm xử lý toàn bộ logic nghiệp vụ: xác thực danh tính, kiểm tra quyền hạn (RBAC), tính toán số liệu tài chính, điều phối luồng dữ liệu và truy xuất CSDL qua PDO.")
add_bullet(doc, "Tầng 3 - Database Layer (Tầng lưu trữ dữ liệu): Hệ quản trị cơ sở dữ liệu quan hệ MySQL 8.0 (qua XAMPP). Chịu trách nhiệm lưu trữ bền vững, đảm bảo tính toàn vẹn thông qua các ràng buộc khóa chính, khóa ngoại, chỉ mục tìm kiếm và xử lý các giao dịch một cách an toàn.")

add_sec1(doc, "2.7. Thiết Kế Cơ Sở Dữ Liệu Chi Tiết")
add_sec2(doc, "2.7.1. Sơ đồ thực thể liên kết (ERD)")
add_p(doc, "Cơ sở dữ liệu của hệ thống mang tên quan_ly_phong_tro, bao gồm 10 bảng thực thể được chuẩn hóa đạt dạng chuẩn 3NF (Third Normal Form) nhằm loại bỏ hoàn toàn hiện tượng dư thừa dữ liệu và dị thường khi thêm/sửa/xóa:")

add_image(doc, "sodo_erd.png", "Hình 2.6: Sơ đồ quan hệ thực thể ERD hệ thống Quản Lý Phòng Trọ")

add_sec2(doc, "2.7.2. Từ điển dữ liệu chi tiết (Data Dictionary)")
add_p(doc, "Dưới đây là đặc tả chi tiết cấu trúc bảng, kiểu dữ liệu, ràng buộc toàn vẹn và mục đích sử dụng của từng trường dữ liệu trong hệ thống:")

add_table(doc,
    ["Tên Cột", "Kiểu Dữ Liệu", "Ràng Buộc", "Mặc Định", "Mô Tả Nghiệp Vụ"],
    [
        ["id", "INT", "PRIMARY KEY, AUTO_INCREMENT", "-", "Mã định danh duy nhất của tài khoản."],
        ["username", "VARCHAR(50)", "NOT NULL, UNIQUE", "-", "Tên đăng nhập hệ thống, duy nhất."],
        ["password", "VARCHAR(255)", "NOT NULL", "-", "Mật khẩu đã được mã hóa băm một chiều Bcrypt."],
        ["ho_ten", "VARCHAR(100)", "NOT NULL", "-", "Họ và tên đầy đủ của chủ tài khoản."],
        ["email", "VARCHAR(100)", "UNIQUE, NULL", "NULL", "Địa chỉ thư điện tử nhận thông báo."],
        ["so_dien_thoai", "VARCHAR(20)", "NULL", "NULL", "Số điện thoại liên hệ chính."],
        ["vai_tro", "ENUM('admin','khach_thue')", "NOT NULL", "'khach_thue'", "Vai trò phân quyền: admin hoặc khach_thue."],
        ["trang_thai", "ENUM('hoat_dong','khoa')", "NOT NULL", "'hoat_dong'", "Trạng thái hoạt động hoặc bị khóa tài khoản."],
        ["tenant_id", "INT", "FOREIGN KEY, NULL", "NULL", "Khóa ngoại liên kết tới bảng tenants (với khách thuê)."],
        ["lan_cuoi_dang_nhap", "DATETIME", "NULL", "NULL", "Ghi nhận thời điểm đăng nhập gần nhất."],
        ["ngay_tao", "DATETIME", "NOT NULL", "CURRENT_TIMESTAMP", "Thời điểm tài khoản được khởi tạo."]
    ],
    "Bảng 2.8: Cấu trúc chi tiết bảng users (Tài khoản người dùng)"
)

add_table(doc,
    ["Tên Cột", "Kiểu Dữ Liệu", "Ràng Buộc", "Mặc Định", "Mô Tả Nghiệp Vụ"],
    [
        ["id", "INT", "PRIMARY KEY, AUTO_INCREMENT", "-", "Mã định danh duy nhất của phòng."],
        ["ma_phong", "VARCHAR(20)", "NOT NULL, UNIQUE", "-", "Mã số phòng (ví dụ: P101, P202, VIP1)."],
        ["ten_phong", "VARCHAR(100)", "NOT NULL", "-", "Tên gọi mô tả phòng."],
        ["loai_phong", "VARCHAR(50)", "NOT NULL", "'Phòng thường'", "Loại phòng (Phòng thường, Studio, Cao cấp, VIP)."],
        ["tang", "INT", "NOT NULL", "1", "Vị trí tầng lầu của phòng trọ."],
        ["khu", "VARCHAR(20)", "NULL", "NULL", "Phân khu nhà trọ (Khu A, Khu B...)."],
        ["dien_tich", "DECIMAL(5,2)", "NOT NULL", "20.00", "Diện tích phòng tính theo mét vuông (m²)."],
        ["gia_thue", "DECIMAL(12,2)", "NOT NULL", "0.00", "Đơn giá thuê hàng tháng (VND)."],
        ["tien_coc", "DECIMAL(12,2)", "NULL", "0.00", "Khoản tiền đặt cọc giữ chân phòng (VND)."],
        ["so_nguoi_toi_da", "INT", "NOT NULL", "2", "Số lượng người ở tối đa cho phép."],
        ["trang_thai", "ENUM('trong','dang_thue','dang_sua_chua')", "NOT NULL", "'trong'", "Tình trạng phòng: trống, đang thuê, đang sửa."],
        ["mo_ta", "TEXT", "NULL", "NULL", "Ghi chú đặc điểm phòng (nội thất, ban công...)."],
        ["ngay_tao", "DATETIME", "NOT NULL", "CURRENT_TIMESTAMP", "Thời điểm phòng được thêm vào hệ thống."]
    ],
    "Bảng 2.9: Cấu trúc chi tiết bảng rooms (Phòng trọ)"
)

add_table(doc,
    ["Tên Cột", "Kiểu Dữ Liệu", "Ràng Buộc", "Mặc Định", "Mô Tả Nghiệp Vụ"],
    [
        ["id", "INT", "PRIMARY KEY, AUTO_INCREMENT", "-", "Mã định danh duy nhất của người thuê."],
        ["ho_ten", "VARCHAR(100)", "NOT NULL", "-", "Họ và tên đầy đủ của người thuê trọ."],
        ["ngay_sinh", "DATE", "NULL", "NULL", "Ngày tháng năm sinh."],
        ["gioi_tinh", "ENUM('Nam','Nu','Khac')", "NOT NULL", "'Nam'", "Giới tính."],
        ["so_dien_thoai", "VARCHAR(20)", "NOT NULL", "-", "Số điện thoại liên lạc chính thức."],
        ["email", "VARCHAR(100)", "NULL", "NULL", "Địa chỉ email liên hệ."],
        ["so_cmnd", "VARCHAR(20)", "NULL", "NULL", "Số CMND hoặc Căn cước công dân (CCCD)."],
        ["dia_chi", "VARCHAR(255)", "NULL", "NULL", "Địa chỉ hộ khẩu thường trú."],
        ["nghe_nghiep", "VARCHAR(100)", "NULL", "NULL", "Công việc hiện tại (Sinh viên, Nhân viên...)."],
        ["room_id", "INT", "FOREIGN KEY, NULL", "NULL", "Khóa ngoại liên kết tới phòng đang thuê trong rooms."],
        ["ngay_bat_dau_thue", "DATE", "NOT NULL", "-", "Ngày bắt đầu dọn vào ở."],
        ["trang_thai", "ENUM('dang_thue','da_roi')", "NOT NULL", "'dang_thue'", "Trạng thái người thuê: đang thuê hoặc đã rời trọ."],
        ["ghi_chu", "TEXT", "NULL", "NULL", "Ghi chú thêm về người thuê."],
        ["ngay_tao", "DATETIME", "NOT NULL", "CURRENT_TIMESTAMP", "Thời điểm thêm hồ sơ."]
    ],
    "Bảng 2.10: Cấu trúc chi tiết bảng tenants (Người thuê phòng)"
)

add_table(doc,
    ["Tên Cột", "Kiểu Dữ Liệu", "Ràng Buộc", "Mặc Định", "Mô Tả Nghiệp Vụ"],
    [
        ["id", "INT", "PRIMARY KEY, AUTO_INCREMENT", "-", "Mã định danh duy nhất của hợp đồng."],
        ["ma_hop_dong", "VARCHAR(30)", "NOT NULL, UNIQUE", "-", "Mã hợp đồng tự sinh (ví dụ: HD202601001)."],
        ["room_id", "INT", "FOREIGN KEY, NOT NULL", "-", "Khóa ngoại liên kết tới bảng rooms."],
        ["tenant_id", "INT", "FOREIGN KEY, NOT NULL", "-", "Khóa ngoại liên kết tới bảng tenants."],
        ["ngay_bat_dau", "DATE", "NOT NULL", "-", "Ngày hợp đồng bắt đầu có hiệu lực."],
        ["ngay_ket_thuc", "DATE", "NOT NULL", "-", "Ngày hợp đồng chấm dứt hiệu lực."],
        ["gia_thue", "DECIMAL(12,2)", "NOT NULL", "-", "Giá thuê thỏa thuận trên hợp đồng (VND)."],
        ["tien_coc", "DECIMAL(12,2)", "NOT NULL", "-", "Số tiền cọc thực tế đã nhận (VND)."],
        ["chu_ky_thanh_toan", "INT", "NOT NULL", "1", "Chu kỳ đóng tiền tính theo tháng (1, 3, 6, 12)."],
        ["dieu_khoan", "TEXT", "NULL", "NULL", "Nội dung quy định và điều khoản thỏa thuận."],
        ["trang_thai", "ENUM('hieu_luc','sap_het_han','het_han','da_thanh_ly')", "NOT NULL", "'hieu_luc'", "Tình trạng pháp lý của hợp đồng thuê."],
        ["ngay_tao", "DATETIME", "NOT NULL", "CURRENT_TIMESTAMP", "Thời điểm ký lập hợp đồng."]
    ],
    "Bảng 2.11: Cấu trúc chi tiết bảng contracts (Hợp đồng thuê phòng)"
)

add_table(doc,
    ["Tên Cột", "Kiểu Dữ Liệu", "Ràng Buộc", "Mặc Định", "Mô Tả Nghiệp Vụ"],
    [
        ["id", "INT", "PRIMARY KEY, AUTO_INCREMENT", "-", "Mã định danh bản ghi chốt số."],
        ["room_id", "INT", "FOREIGN KEY, NOT NULL", "-", "Phòng được ghi nhận chỉ số."],
        ["thang", "INT", "NOT NULL", "-", "Tháng chốt số (từ 1 đến 12)."],
        ["nam", "INT", "NOT NULL", "-", "Năm chốt số."],
        ["chi_so_dien_cu", "DECIMAL(8,2)", "NOT NULL", "0.00", "Chỉ số công tơ điện đầu kỳ."],
        ["chi_so_dien_moi", "DECIMAL(8,2)", "NOT NULL", "0.00", "Chỉ số công tơ điện cuối kỳ chốt."],
        ["don_gia_dien", "DECIMAL(10,2)", "NOT NULL", "3500.00", "Đơn giá tiền điện (VND / kWh)."],
        ["chi_so_nuoc_cu", "DECIMAL(8,2)", "NOT NULL", "0.00", "Chỉ số đồng hồ nước đầu kỳ."],
        ["chi_so_nuoc_moi", "DECIMAL(8,2)", "NOT NULL", "0.00", "Chỉ số đồng hồ nước cuối kỳ chốt."],
        ["don_gia_nuoc", "DECIMAL(10,2)", "NOT NULL", "25000.00", "Đơn giá tiền nước (VND / m³)."],
        ["ngay_ghi", "DATE", "NOT NULL", "-", "Ngày thực tế chủ trọ đi chép số đồng hồ."]
    ],
    "Bảng 2.12: Cấu trúc chi tiết bảng electric_water (Điện nước theo tháng)"
)

add_table(doc,
    ["Tên Cột", "Kiểu Dữ Liệu", "Ràng Buộc", "Mặc Định", "Mô Tả Nghiệp Vụ"],
    [
        ["id", "INT", "PRIMARY KEY, AUTO_INCREMENT", "-", "Mã định danh hóa đơn."],
        ["ma_hoa_don", "VARCHAR(30)", "NOT NULL, UNIQUE", "-", "Mã hóa đơn duy nhất (ví dụ: HD202610001)."],
        ["room_id", "INT", "FOREIGN KEY, NOT NULL", "-", "Phòng chịu trách nhiệm thanh toán."],
        ["tenant_id", "INT", "FOREIGN KEY, NOT NULL", "-", "Người đại diện thanh toán hóa đơn."],
        ["thang", "INT", "NOT NULL", "-", "Kỳ thu tiền tháng."],
        ["nam", "INT", "NOT NULL", "-", "Kỳ thu tiền năm."],
        ["tien_phong", "DECIMAL(12,2)", "NOT NULL", "0.00", "Khoản tiền thuê mặt bằng phòng."],
        ["tien_dien", "DECIMAL(12,2)", "NOT NULL", "0.00", "Tổng tiền điện đã dùng trong tháng."],
        ["tien_nuoc", "DECIMAL(12,2)", "NOT NULL", "0.00", "Tổng tiền nước đã dùng trong tháng."],
        ["tien_dich_vu", "DECIMAL(12,2)", "NOT NULL", "0.00", "Tổng chi phí các dịch vụ cố định."],
        ["phi_khac", "DECIMAL(12,2)", "NOT NULL", "0.00", "Chi phí phụ trợ hoặc tiền phạt nếu có."],
        ["ghi_chu_phi_khac", "VARCHAR(255)", "NULL", "NULL", "Diễn giải cho khoản phí phát sinh khác."],
        ["tong_tien", "DECIMAL(12,2)", "NOT NULL", "0.00", "Tổng số tiền cần phải thanh toán (VND)."],
        ["han_thanh_toan", "DATE", "NOT NULL", "-", "Hạn chót phải hoàn thành đóng tiền."],
        ["trang_thai", "ENUM('chua_thanh_toan','da_thanh_toan','qua_han')", "NOT NULL", "'chua_thanh_toan'", "Tình trạng thanh toán của hóa đơn."],
        ["ghi_chu", "TEXT", "NULL", "NULL", "Ghi chú thêm trên phiếu hóa đơn."],
        ["ngay_tao", "DATETIME", "NOT NULL", "CURRENT_TIMESTAMP", "Thời điểm phát hành hóa đơn."]
    ],
    "Bảng 2.13: Cấu trúc chi tiết bảng invoices (Hóa đơn thu tiền hàng tháng)"
)

add_table(doc,
    ["Tên Cột", "Kiểu Dữ Liệu", "Ràng Buộc", "Mặc Định", "Mô Tả Nghiệp Vụ"],
    [
        ["id", "INT", "PRIMARY KEY, AUTO_INCREMENT", "-", "Mã định danh giao dịch thanh toán."],
        ["ma_thanh_toan", "VARCHAR(30)", "NOT NULL, UNIQUE", "-", "Mã phiếu thu tiền (ví dụ: TT2026101201)."],
        ["invoice_id", "INT", "FOREIGN KEY, NOT NULL", "-", "Liên kết tới hóa đơn được thanh toán."],
        ["tenant_id", "INT", "FOREIGN KEY, NOT NULL", "-", "Người thực hiện đóng tiền."],
        ["so_tien", "DECIMAL(12,2)", "NOT NULL", "-", "Số tiền thực tế đã nộp (VND)."],
        ["phuong_thuc", "ENUM('tien_mat','chuyen_khoan','the_atm','vi_dien_tu')", "NOT NULL", "'tien_mat'", "Phương thức nộp tiền."],
        ["ngay_thanh_toan", "DATE", "NOT NULL", "-", "Ngày ghi nhận đóng tiền."],
        ["ghi_chu", "TEXT", "NULL", "NULL", "Ghi chú giao dịch (mã ngân hàng...)."],
        ["ngay_tao", "DATETIME", "NOT NULL", "CURRENT_TIMESTAMP", "Thời điểm lưu phiếu."]
    ],
    "Bảng 2.14: Cấu trúc chi tiết bảng payments (Lịch sử thanh toán)"
)

add_table(doc,
    ["Tên Cột", "Kiểu Dữ Liệu", "Ràng Buộc", "Mặc Định", "Mô Tả Nghiệp Vụ"],
    [
        ["id", "INT", "PRIMARY KEY, AUTO_INCREMENT", "-", "Mã định danh yêu cầu sự cố."],
        ["room_id", "INT", "FOREIGN KEY, NOT NULL", "-", "Phòng xảy ra sự cố kỹ thuật."],
        ["tenant_id", "INT", "FOREIGN KEY, NOT NULL", "-", "Người thuê gửi phản ánh sự cố."],
        ["tieu_de", "VARCHAR(150)", "NOT NULL", "-", "Tóm tắt sự cố (ví dụ: Hỏng bóng đèn tuýp)."],
        ["noi_dung", "TEXT", "NOT NULL", "-", "Mô tả chi tiết hiện trạng hỏng hóc."],
        ["muc_do", "ENUM('thap','binh_thuong','cao','khan_cap')", "NOT NULL", "'binh_thuong'", "Mức độ khẩn cấp cần khắc phục."],
        ["trang_thai", "ENUM('moi_gui','da_tiep_nhan','dang_xu_ly','hoan_thanh')", "NOT NULL", "'moi_gui'", "Tiến trình khắc phục sự cố 4 bước."],
        ["ghi_chu_xu_ly", "TEXT", "NULL", "NULL", "Ghi chú của chủ trọ về thợ sửa, chi phí."],
        ["ngay_tao", "DATETIME", "NOT NULL", "CURRENT_TIMESTAMP", "Thời điểm khách thuê gửi báo hỏng."]
    ],
    "Bảng 2.15: Cấu trúc chi tiết bảng maintenance_requests (Yêu cầu sự cố sửa chữa)"
)

add_table(doc,
    ["Tên Cột", "Kiểu Dữ Liệu", "Ràng Buộc", "Mặc Định", "Mô Tả Nghiệp Vụ"],
    [
        ["id", "INT", "PRIMARY KEY, AUTO_INCREMENT", "-", "Mã định danh dịch vụ."],
        ["ma_dich_vu", "VARCHAR(20)", "NOT NULL, UNIQUE", "-", "Mã dịch vụ (DV_NET, DV_RAC, DV_XE...)."],
        ["ten_dich_vu", "VARCHAR(100)", "NOT NULL", "-", "Tên dịch vụ (Internet cáp quang, Vệ sinh...)."],
        ["don_gia", "DECIMAL(12,2)", "NOT NULL", "0.00", "Đơn giá cước dịch vụ (VND)."],
        ["don_vi_tinh", "VARCHAR(30)", "NOT NULL", "'thang'", "Đơn vị tính (phòng/tháng, người/tháng, xe/tháng)."],
        ["mo_ta", "TEXT", "NULL", "NULL", "Mô tả chi tiết phạm vi dịch vụ."],
        ["trang_thai", "ENUM('hoat_dong','ngung')", "NOT NULL", "'hoat_dong'", "Trạng thái đang cung cấp hoặc tạm ngừng."]
    ],
    "Bảng 2.16: Cấu trúc chi tiết bảng services (Danh mục dịch vụ)"
)

print("3. Writing Chapter III: Implementation and UI Screenshots...")

add_chapter(doc, "CHƯƠNG III: XÂY DỰNG VÀ CÀI ĐẶT HỆ THỐNG")

add_sec1(doc, "3.1. Cấu Trúc Thư Mục Dự Án Và Tổ Chức Mã Nguồn")
add_p(doc, "Để đảm bảo tính trong sáng của mã nguồn, phù hợp với tiêu chuẩn đồ án tốt nghiệp mà không bị phụ thuộc vào các framework cồng kềnh khó kiểm soát, toàn bộ mã nguồn được tổ chức theo kiến trúc module hóa rõ ràng trong thư mục gốc c:\\xampp\\htdocs\\QuanLyPhongTro:")

add_table(doc,
    ["Thư Mục / Tệp Tin", "Vai Trò Và Trách Nhiệm Nghiệp Vụ"],
    [
        ["config/database.php", "Cấu hình tham số máy chủ và khởi tạo kết nối PDO Singleton đến MySQL."],
        ["includes/auth.php", "Các hàm tiện ích xác thực phiên làm việc: requireAdmin(), requireKhachThue(), isLoggedIn()."],
        ["includes/functions.php", "Các hàm xử lý dùng chung: formatMoney(), formatDate(), getStatusBadge(), paginate()."],
        ["includes/header.php & footer.php", "Template khung đầu và cuối trang cho phân hệ Quản trị viên (Admin)."],
        ["includes/sidebar.php", "Thanh điều hướng Sidebar chuyên biệt dành cho Quản trị viên."],
        ["includes/header_user.php & footer_user.php", "Template khung giao diện cho phân hệ Khách thuê (User)."],
        ["includes/sidebar_user.php", "Thanh điều hướng Sidebar thu gọn dành cho Khách thuê."],
        ["assets/css/style.css", "Tập lệnh định dạng CSS giao diện 2 cột, thẻ card, bảng biểu, badge trạng thái."],
        ["assets/css/login.css", "CSS chuyên biệt tạo hiệu ứng chuyển màu gradient và animation cho trang đăng nhập."],
        ["assets/js/script.js", "Tập lệnh JavaScript: xử lý co rút sidebar, đồng hồ thời gian thực, xác nhận xóa."],
        ["admin/dashboard.php", "Bảng điều khiển trung tâm hiển thị chỉ số KPI và biểu đồ Chart.js."],
        ["admin/phong.php", "Quản lý danh mục phòng, thêm/sửa bằng modal, lọc theo trạng thái và tầng."],
        ["admin/nguoi_thue.php", "Quản lý thông tin cá nhân khách thuê, số CCCD, hợp đồng liên kết."],
        ["admin/hop_dong.php", "Quản lý hợp đồng cho thuê, theo dõi tiến độ thời gian và cảnh báo hết hạn."],
        ["admin/dien_nuoc.php", "Nhập số công tơ điện nước hàng tháng, tính toán chênh lệch thành tiền real-time."],
        ["admin/dich_vu.php", "Quản lý bảng giá các dịch vụ dùng chung trong khu trọ."],
        ["admin/hoa_don.php", "Lập hóa đơn tổng hợp tiền phòng, điện nước, dịch vụ và theo dõi thanh toán."],
        ["admin/hoa_don_in.php", "Mẫu phiếu thu hóa đơn chuẩn để in ấn hoặc xuất PDF."],
        ["admin/thanh_toan.php", "Ghi nhận phiếu thanh toán tiền mặt/chuyển khoản, tự động cập nhật trạng thái nợ."],
        ["admin/su_co.php", "Quản lý và cập nhật tiến độ xử lý các phản ánh hư hỏng thiết bị."],
        ["admin/tai_khoan.php", "Quản lý danh sách tài khoản hệ thống, phân quyền và khóa/mở người dùng."],
        ["admin/thong_ke.php", "Báo cáo doanh thu tài chính 12 tháng bằng biểu đồ trực quan."],
        ["user/ (8 file PHP)", "Toàn bộ các trang xem dữ liệu cá nhân hóa dành cho khách thuê."],
        ["login.php & logout.php", "Trang đăng nhập hệ thống và xử lý hủy phiên đăng xuất an toàn."],
        ["database.sql", "Mã nguồn SQL khởi tạo 10 bảng dữ liệu và chèn các bản ghi demo ban đầu."]
    ],
    "Bảng 3.1: Danh mục tổ chức tệp tin mã nguồn trong dự án"
)

add_sec1(doc, "3.2. Cài Đặt Kết Nối Cơ Sở Dữ Liệu An Toàn")
add_sec2(doc, "3.2.1. Kết nối PDO với Singleton Pattern")
add_p(doc, "Tệp tin config/database.php sử dụng thư viện PDO (PHP Data Objects) chuẩn của PHP 8 kết hợp mẫu thiết kế Singleton Pattern để khởi tạo kết nối duy nhất, tái sử dụng trong suốt vòng đời của một HTTP Request:")

add_code(doc,
"""<?php
// config/database.php
define('DB_HOST', 'localhost');
define('DB_NAME', 'quan_ly_phong_tro');
define('DB_USER', 'root');
define('DB_PASS', '');

function getDB(): PDO {
    static $pdo = null;
    if ($pdo === null) {
        $dsn = "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=utf8mb4";
        $options = [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES   => false,
        ];
        try {
            $pdo = new PDO($dsn, DB_USER, DB_PASS, $options);
        } catch (PDOException $e) {
            die("Lỗi kết nối cơ sở dữ liệu: " . $e->getMessage());
        }
    }
    return $pdo;
}
$pdo = getDB();
?>"""
)

add_sec2(doc, "3.2.2. Cơ chế phòng chống SQL Injection bằng Prepared Statements")
add_p(doc, "Trong toàn bộ các thao tác nghiệp vụ, hệ thống tuyệt đối không áp dụng kỹ thuật nối chuỗi câu lệnh SQL truyền thống vốn tiềm ẩn lỗ hổng bảo mật nghiêm trọng. Toàn bộ tham số đầu vào được phân tách hoàn toàn khỏi câu lệnh SQL thông qua kỹ thuật tham số hóa (Prepared Statements):")

add_code(doc,
"""// [AN TOÀN]: Sử dụng Prepared Statements qua PDO
$stmt = $pdo->prepare("SELECT * FROM users WHERE username = ? AND trang_thai = ?");
$stmt->execute([$input_username, 'hoat_dong']);
$user = $stmt->fetch();

// Xác thực mật khẩu đã băm bằng Bcrypt an toàn
if ($user && password_verify($input_password, $user['password'])) {
    $_SESSION['user_id'] = $user['id'];
    $_SESSION['vai_tro'] = $user['vai_tro'];
    // Đăng nhập thành công
}"""
)

add_sec1(doc, "3.3. Cài Đặt Chi Tiết Phân Hệ Quản Trị Viên (Admin)")

add_sec2(doc, "3.3.1. Giao diện Đăng nhập hệ thống (login.php)")
add_p(doc, "Màn hình đăng nhập được thiết kế với phong cách tối giản, hiện đại. Trang bị tính năng ẩn/hiện mật khẩu tức thì và các thẻ demo tài khoản giúp kiểm thử viên và giảng viên dễ dàng đăng nhập nhanh chỉ với 1 cú click chuột:")

add_image(doc, "hinh_login.png", "Hình 3.1: Giao diện đăng nhập hệ thống Quản Lý Phòng Trọ")

add_sec2(doc, "3.3.2. Dashboard Quản trị viên (admin/dashboard.php)")
add_p(doc, "Bảng điều khiển trung tâm giúp chủ nhà trọ nắm bắt toàn bộ tình hình hoạt động kinh doanh chỉ trong một màn hình duy nhất:")
add_bullet(doc, "4 thẻ thống kê đầu trang: Tổng số phòng, Doanh thu thực tế tháng này, Số hóa đơn chưa thu tiền, Số sự cố đang chờ xử lý.")
add_bullet(doc, "Biểu đồ tròn Donut (Chart.js): Minh họa trực quan tỷ lệ phòng đang thuê (xanh lá), phòng còn trống (xanh dương) và phòng đang sửa chữa (vàng cam).")
add_bullet(doc, "Biểu đồ cột (Chart.js): Thể hiện dòng tiền doanh thu thu được trong 6 tháng gần nhất.")
add_bullet(doc, "Bảng danh sách các hóa đơn mới lập và các phản ánh báo hỏng khẩn cấp nhất.")

add_image(doc, "hinh_admin_dashboard.png", "Hình 3.2: Giao diện Dashboard tổng quan của Quản trị viên")

add_sec2(doc, "3.3.3. Quản lý danh mục phòng trọ (admin/phong.php)")
add_p(doc, "Màn hình quản lý phòng trọ cho phép thực hiện đầy đủ các nghiệp vụ thêm, sửa, xóa, lọc và tìm kiếm phòng:")
add_bullet(doc, "Thanh thống kê nhanh số lượng phòng theo từng trạng thái.")
add_bullet(doc, "Hộp tìm kiếm từ khóa theo mã phòng hoặc tên phòng kết hợp bộ lọc phân loại.")
add_bullet(doc, "Bảng hiển thị thông tin chi tiết: Loại phòng, Tầng, Diện tích, Đơn giá thuê, Tiền cọc, Tỷ lệ người ở thực tế trên sức chứa tối đa.")
add_bullet(doc, "Modal thêm mới và cập nhật phòng tích hợp JavaScript tự động điền dữ liệu mà không cần tải lại trang.")

add_image(doc, "hinh_admin_phong.png", "Hình 3.3: Giao diện quản lý danh mục phòng trọ")

add_sec2(doc, "3.3.4. Quản lý hồ sơ người thuê (admin/nguoi_thue.php)")
add_p(doc, "Quản lý toàn bộ thông tin nhân thân của khách thuê trọ, phục vụ công tác quản lý cư trú và liên lạc:")
add_bullet(doc, "Lưu trữ đầy đủ họ tên, ngày sinh, giới tính, số điện thoại, email, số CMND/CCCD, quê quán và nghề nghiệp.")
add_bullet(doc, "Liên kết trực tiếp người thuê với phòng đang lưu trú, tự động chuyển trạng thái phòng sang 'Đang thuê'.")
add_bullet(doc, "Phân loại trạng thái 'Đang thuê' và 'Đã rời' để lưu vết lịch sử khách thuê.")

add_image(doc, "hinh_admin_nguoithue.png", "Hình 3.4: Giao diện quản lý hồ sơ người thuê phòng")

add_sec2(doc, "3.3.5. Quản lý hợp đồng cho thuê (admin/hop_dong.php)")
add_p(doc, "Hệ thống quản lý hợp đồng giúp chủ trọ quản lý chặt chẽ mặt pháp lý và thời hạn của từng khách thuê:")
add_bullet(doc, "Mã hợp đồng tự động sinh ra duy nhất, gắn kết chặt chẽ giữa Khách thuê và Phòng trọ.")
add_bullet(doc, "Quản lý ngày bắt đầu, ngày kết thúc, giá thuê cam kết, tiền cọc thực nhận và chu kỳ đóng tiền.")
add_bullet(doc, "Tự động kích hoạt trạng thái 'Sắp hết hạn' khi thời hạn còn dưới 30 ngày để chủ trọ kịp thời liên hệ gia hạn.")

add_image(doc, "hinh_admin_hopdong.png", "Hình 3.5: Giao diện quản lý hợp đồng thuê phòng trọ")

add_sec2(doc, "3.3.6. Quản lý chỉ số điện nước (admin/dien_nuoc.php)")
add_p(doc, "Chức năng then chốt giúp tự động hóa khâu tính toán tiền điện nước hàng tháng:")
add_bullet(doc, "Modal nhập chỉ số công tơ điện và đồng hồ nước tích hợp công thức tính toán tự động bằng JavaScript: khi người dùng nhập số mới, màn hình lập tức hiển thị lượng điện nước tiêu thụ và tổng tiền tương ứng.")
add_bullet(doc, "Cơ chế kiểm tra logic nghiêm ngặt: chỉ số mới không được phép nhỏ hơn chỉ số cũ.")

add_image(doc, "hinh_admin_diennuoc.png", "Hình 3.6: Giao diện quản lý và nhập chỉ số điện nước theo tháng")

add_sec2(doc, "3.3.7. Quản lý danh mục dịch vụ (admin/dich_vu.php)")
add_p(doc, "Cho phép chủ trọ cấu hình linh hoạt bảng giá các dịch vụ dùng chung trong khu trọ như Internet cáp quang, tiền thu gom rác, phí gửi xe máy, phí dịch vụ vệ sinh hành lang:")

add_image(doc, "hinh_admin_dichvu.png", "Hình 3.7: Giao diện quản lý danh mục và đơn giá dịch vụ")

add_sec2(doc, "3.3.8. Quản lý hóa đơn tiền phòng (admin/hoa_don.php)")
add_p(doc, "Trung tâm điều hành tài chính của khu trọ, tự động tính tổng tiền từ tất cả các khoản chi phí:")
add_bullet(doc, "Thống kê tổng công nợ chưa thu và tổng số tiền đã thu trong kỳ.")
add_bullet(doc, "Hóa đơn được phân biệt bằng màu sắc trực quan: màu đỏ cảnh báo hóa đơn quá hạn nộp tiền, màu vàng cho hóa đơn chưa đóng và màu trắng cho hóa đơn đã hoàn tất.")
add_bullet(doc, "Hỗ trợ lọc hóa đơn theo tháng, theo năm và theo trạng thái thanh toán.")

add_image(doc, "hinh_admin_hoadon.png", "Hình 3.8: Giao diện quản lý danh sách hóa đơn hàng tháng")

add_sec2(doc, "3.3.9. Mẫu in phiếu thu hóa đơn (admin/hoa_don_in.php)")
add_p(doc, "Hệ thống cung cấp trang in phiếu thu chuyên biệt được tối ưu hóa theo tiêu chuẩn Print-friendly: tự động ẩn toàn bộ sidebar, topbar và thanh menu, chỉ giữ lại khung thông tin hóa đơn sắc nét, sẵn sàng in ra giấy A4/A5 hoặc lưu dưới dạng tệp PDF gửi cho khách thuê:")

add_image(doc, "hinh_admin_hoadon_in.png", "Hình 3.9: Giao diện in phiếu thu hóa đơn chuẩn Print-friendly", width_in=4.2)

add_sec2(doc, "3.3.10. Quản lý thanh toán và công nợ (admin/thanh_toan.php)")
add_p(doc, "Giao diện được bố trí chia đôi tiện dụng: bên trái là biểu mẫu ghi nhận tiền nộp (chọn hóa đơn sẽ tự động nhảy số tiền tương ứng); bên phải là bảng lịch sử toàn bộ các giao dịch nộp tiền theo ngày:")

add_image(doc, "hinh_admin_thanhtoan.png", "Hình 3.10: Giao diện ghi nhận và theo dõi lịch sử thanh toán")

add_sec2(doc, "3.3.11. Quản lý tiếp nhận sự cố kỹ thuật (admin/su_co.php)")
add_p(doc, "Kênh điều phối công tác sửa chữa hạ tầng khu trọ, hỗ trợ quản lý trạng thái xử lý 4 giai đoạn: Mới gửi -> Đã tiếp nhận -> Đang xử lý -> Đã hoàn thành kèm theo ghi chú chi phí và ngày hoàn tất:")

add_image(doc, "hinh_admin_suco.png", "Hình 3.11: Giao diện quản lý và cập nhật tiến độ xử lý sự cố")

add_sec2(doc, "3.3.12. Quản lý tài khoản và phân quyền (admin/tai_khoan.php)")
add_p(doc, "Cho phép Quản trị viên cấp tài khoản mới cho người thuê, thiết lập vai trò, đổi mật khẩu và chủ động khóa các tài khoản vi phạm nội quy khu trọ:")

add_image(doc, "hinh_admin_taikhoan.png", "Hình 3.12: Giao diện quản lý tài khoản người dùng hệ thống")

add_sec2(doc, "3.3.13. Báo cáo thống kê tài chính (admin/thong_ke.php)")
add_p(doc, "Cung cấp bức tranh toàn cảnh về hiệu quả kinh doanh của nhà trọ trong cả năm:")
add_bullet(doc, "Biểu đồ cột so sánh biến động doanh thu thực tế qua 12 tháng.")
add_bullet(doc, "Biểu đồ đường theo dõi tương quan chi phí điện và nước qua từng tháng.")
add_bullet(doc, "Bảng xếp hạng top các phòng đóng góp doanh thu cao nhất cho khu trọ.")

add_image(doc, "hinh_admin_thongke.png", "Hình 3.13: Giao diện thống kê báo cáo doanh thu và chi phí")

add_sec1(doc, "3.4. Cài Đặt Chi Tiết Phân Hệ Khách Thuê (User Portal)")
add_p(doc, "Phân hệ Khách thuê được xây dựng độc lập với giao diện thân thiện, bảo đảm người thuê chỉ nhìn thấy dữ liệu cá nhân của chính mình:")

add_sec2(doc, "3.4.1. Dashboard Khách thuê (user/dashboard.php)")
add_p(doc, "Tổng hợp nhanh các thông báo quan trọng nhất đối với người thuê ngay khi đăng nhập: thông tin phòng đang ở, số tiền hóa đơn cần đóng, ngày hết hạn thanh toán và chỉ số điện nước tháng hiện tại:")

add_image(doc, "hinh_user_dashboard.png", "Hình 3.14: Giao diện Dashboard của Khách thuê phòng")

add_sec2(doc, "3.4.2. Tra cứu thông tin phòng và hợp đồng")
add_p(doc, "Khách thuê có thể chủ động tra cứu chi tiết diện tích phòng, đơn giá thuê gốc và xem hợp đồng kèm thanh tiến trình thời gian thuê:")

add_image(doc, "hinh_user_phong.png", "Hình 3.15: Giao diện xem thông tin phòng của Khách thuê")

add_image(doc, "hinh_user_hopdong.png", "Hình 3.16: Giao diện xem hợp đồng thuê và thanh tiến trình thời hạn")

add_sec2(doc, "3.4.3. Tra cứu điện nước và danh sách hóa đơn")
add_p(doc, "Minh bạch hóa toàn bộ các khoản thu: người thuê xem được lịch sử số đo công tơ điện nước từng tháng, kiểm tra hóa đơn chi tiết và hạn nộp tiền:")

add_image(doc, "hinh_user_diennuoc.png", "Hình 3.17: Giao diện tra cứu lịch sử chỉ số điện nước hàng tháng")

add_image(doc, "hinh_user_hoadon.png", "Hình 3.18: Giao diện xem danh sách hóa đơn và tình trạng thanh toán")

add_sec2(doc, "3.4.4. Lịch sử thanh toán và biên lai")
add_p(doc, "Lưu trữ đầy đủ bằng chứng đã hoàn thành nghĩa vụ tài chính của khách thuê:")

add_image(doc, "hinh_user_thanhtoan.png", "Hình 3.19: Giao diện theo dõi lịch sử các lần thanh toán tiền phòng")

add_sec2(doc, "3.4.5. Gửi yêu cầu phản ánh sự cố kỹ thuật (user/su_co.php)")
add_p(doc, "Khách thuê dễ dàng báo hỏng thiết bị (cháy bóng đèn, rò rỉ nước, hỏng khóa) và theo dõi phản hồi xử lý trực tiếp từ chủ trọ:")

add_image(doc, "hinh_user_suco.png", "Hình 3.20: Giao diện gửi phản ánh sự cố sửa chữa của Khách thuê")

add_sec2(doc, "3.4.6. Quản lý thông tin cá nhân và đổi mật khẩu (user/tai_khoan.php)")
add_p(doc, "Cho phép khách thuê cập nhật số điện thoại liên hệ, email cá nhân và chủ động thay đổi mật khẩu định kỳ để bảo vệ tài khoản:")

add_image(doc, "hinh_user_taikhoan.png", "Hình 3.21: Giao diện cập nhật thông tin và đổi mật khẩu của Khách thuê")

print("4. Writing Chapter IV: Testing and Evaluation...")

add_chapter(doc, "CHƯƠNG IV: KIỂM THỬ VÀ ĐÁNH GIÁ KẾT QUẢ")

add_sec1(doc, "4.1. Phương Pháp Và Kế Hoạch Kiểm Thử Hệ Thống")
add_p(doc, "Để đảm bảo website hoạt động ổn định, chính xác và an toàn trước khi đưa vào vận hành thực tế, nhóm tác giả áp dụng phương pháp Kiểm thử hộp đen (Black-box Testing). Phương pháp này tập trung kiểm tra tính đúng đắn của các chức năng đầu vào và kết quả đầu ra mà không cần can thiệp sâu vào cấu trúc nội bộ của mã nguồn.")
add_p(doc, "Kế hoạch kiểm thử bao gồm các giai đoạn:")
add_bullet(doc, "Kiểm thử chức năng (Functional Testing): Đảm bảo từng nghiệp vụ CRUD, tính toán tài chính, phân quyền hoạt động đúng như đặc tả yêu cầu.")
add_bullet(doc, "Kiểm thử tính toàn vẹn dữ liệu (Data Integrity Testing): Kiểm tra các ràng buộc khóa ngoại, điều kiện logic (chỉ số điện mới >= chỉ số cũ, không xóa phòng đang có người ở).")
add_bullet(doc, "Kiểm thử bảo mật (Security Testing): Kiểm tra khả năng chống tấn công SQL Injection và cơ chế bảo vệ phiên đăng nhập.")
add_bullet(doc, "Kiểm thử tính tương thích giao diện (Cross-browser & Responsive Testing): Thử nghiệm trên các trình duyệt Edge, Chrome và các kích thước màn hình khác nhau.")

add_sec1(doc, "4.2. Bảng Kịch Bản Kiểm Thử (Test Cases) Chi Tiết")
add_p(doc, "Hệ thống đã trải qua hơn 40 kịch bản kiểm thử chi tiết. Dưới đây là các bảng kết quả kiểm thử thực nghiệm:")

add_table(doc,
    ["Mã TC", "Tên Test Case", "Dữ Liệu Đầu Vào", "Kết Quả Kỳ Vọng", "Kết Quả Thực Tế", "Đánh Giá"],
    [
        ["TC-AUTH-01", "Đăng nhập Admin đúng", "user: admin, pass: Admin@123", "Đăng nhập thành công, vào admin/dashboard.php", "Chuyển đúng trang", "ĐẠT ✓"],
        ["TC-AUTH-02", "Đăng nhập Khách thuê đúng", "user: nguyen.van.a, pass: User@123", "Đăng nhập thành công, vào user/dashboard.php", "Chuyển đúng trang", "ĐẠT ✓"],
        ["TC-AUTH-03", "Sai mật khẩu", "user: admin, pass: SaiPass123", "Báo lỗi 'Tên đăng nhập hoặc mật khẩu không đúng'", "Hiển thị alert đỏ", "ĐẠT ✓"],
        ["TC-AUTH-04", "Tài khoản không tồn tại", "user: khongco, pass: 123456", "Báo lỗi 'Tên đăng nhập hoặc mật khẩu không đúng'", "Hiển thị alert đỏ", "ĐẠT ✓"],
        ["TC-AUTH-05", "Để trống thông tin", "user: '', pass: ''", "Báo lỗi yêu cầu điền đầy đủ thông tin", "Hiển thị cảnh báo", "ĐẠT ✓"],
        ["TC-AUTH-06", "Đăng xuất tài khoản", "Nhấn nút 'Đăng Xuất'", "Hủy Session, quay về login.php với thông báo", "Hủy phiên chuẩn", "ĐẠT ✓"]
    ],
    "Bảng 4.1: Kết quả kiểm thử module Xác thực & Đăng nhập"
)

add_table(doc,
    ["Mã TC", "Tên Test Case", "Dữ Liệu Đầu Vào", "Kết Quả Kỳ Vọng", "Kết Quả Thực Tế", "Đánh Giá"],
    [
        ["TC-ROOM-01", "Thêm phòng mới hợp lệ", "Mã: P301, Tên: Phòng 301, Giá: 2.500.000", "Lưu thành công, hiển thị flash message xanh", "Phòng mới xuất hiện", "ĐẠT ✓"],
        ["TC-ROOM-02", "Thêm phòng mã trùng lặp", "Mã: P101 (đã có trong CSDL)", "Báo lỗi 'Mã phòng đã tồn tại. Vui lòng chọn mã khác'", "Chặn trùng lặp", "ĐẠT ✓"],
        ["TC-ROOM-03", "Sửa thông tin phòng", "Sửa giá P101 thành 2.800.000", "Cập nhật thành công, giá mới lưu vào CSDL", "Giá mới hiển thị", "ĐẠT ✓"],
        ["TC-ROOM-04", "Xóa phòng còn trống", "Xóa phòng P301 (trang_thai = 'trong')", "Xóa thành công khỏi bảng rooms", "Xóa hoàn tất", "ĐẠT ✓"],
        ["TC-ROOM-05", "Xóa phòng đang có người", "Xóa phòng P101 (đang có người thuê)", "Báo lỗi 'Không thể xóa phòng đang có người thuê!'", "Chặn xóa an toàn", "ĐẠT ✓"],
        ["TC-ROOM-06", "Tìm kiếm và lọc phòng", "Từ khóa '101', lọc 'dang_thue'", "Danh sách chỉ hiển thị đúng phòng P101", "Lọc chính xác", "ĐẠT ✓"]
    ],
    "Bảng 4.2: Kết quả kiểm thử module Quản lý phòng trọ"
)

add_table(doc,
    ["Mã TC", "Tên Test Case", "Dữ Liệu Đầu Vào", "Kết Quả Kỳ Vọng", "Kết Quả Thực Tế", "Đánh Giá"],
    [
        ["TC-TEN-01", "Thêm người thuê mới", "Họ tên: Lê Hoàng Nam, SĐT: 0988112233", "Thêm thành công, gắn vào phòng P103", "Lưu thành công", "ĐẠT ✓"],
        ["TC-TEN-02", "Cập nhật trạng thái phòng", "Gắn khách Nam vào phòng trống P103", "Phòng P103 tự động chuyển thành 'dang_thue'", "Đổi trạng thái tự động", "ĐẠT ✓"],
        ["TC-TEN-03", "Tạo hợp đồng thuê", "Khách: Nam, Phòng: P103, Thời hạn: 12 tháng", "Lưu hợp đồng, tự sinh mã HD2026...", "Tạo mã hợp lệ", "ĐẠT ✓"],
        ["TC-TEN-04", "Cảnh báo hết hạn hợp đồng", "Hợp đồng có ngày kết thúc sau 15 ngày", "Hiển thị badge vàng cam 'Sắp hết hạn'", "Cảnh báo chính xác", "ĐẠT ✓"]
    ],
    "Bảng 4.3: Kết quả kiểm thử module Người thuê & Hợp đồng"
)

add_table(doc,
    ["Mã TC", "Tên Test Case", "Dữ Liệu Đầu Vào", "Kết Quả Kỳ Vọng", "Kết Quả Thực Tế", "Đánh Giá"],
    [
        ["TC-EW-01", "Nhập điện nước hợp lệ", "Điện: 100->150 (50 kWh), Nước: 20->25 (5 m³)", "Tính đúng: Điện 175.000đ, Nước 125.000đ, Tổng 300.000đ", "Tính tiền chính xác", "ĐẠT ✓"],
        ["TC-EW-02", "Chỉ số mới nhỏ hơn số cũ", "Điện cũ: 150, Điện mới: 120", "Báo lỗi chỉ số mới không được nhỏ hơn chỉ số cũ", "Chặn lỗi số học", "ĐẠT ✓"],
        ["TC-EW-03", "Tính tiền real-time", "Gõ số mới trên modal nhập liệu", "JavaScript cập nhật số tiền tức thời trên giao diện", "Hiển thị mượt mà", "ĐẠT ✓"]
    ],
    "Bảng 4.4: Kết quả kiểm thử module Điện nước"
)

add_table(doc,
    ["Mã TC", "Tên Test Case", "Dữ Liệu Đầu Vào", "Kết Quả Kỳ Vọng", "Kết Quả Thực Tế", "Đánh Giá"],
    [
        ["TC-INV-01", "Tạo hóa đơn tổng hợp", "Phòng P101: Tiền phòng 2.5M, Điện nước 300k, DV 100k", "Tổng tiền tự động bằng 2.900.000đ, trạng thái 'chua_thanh_toan'", "Lập hóa đơn chuẩn", "ĐẠT ✓"],
        ["TC-INV-02", "Ghi nhận thanh toán đủ", "Nộp đủ 2.900.000đ qua Chuyển khoản", "Hóa đơn tự động đổi sang 'da_thanh_toan'", "Cập nhật nợ tự động", "ĐẠT ✓"],
        ["TC-INV-03", "In phiếu thu hóa đơn", "Nhấn nút 'In' trên hóa đơn", "Mở trang in print-friendly, không có sidebar, thông tin rõ ràng", "Bản in sắc nét", "ĐẠT ✓"],
        ["TC-INV-04", "Báo sự cố & xử lý", "Khách báo hỏng vòi nước -> Admin duyệt hoàn thành", "Quy trình chuyển đổi trạng thái 4 bước hoạt động chuẩn", "Hai chiều thông suốt", "ĐẠT ✓"],
        ["TC-SEC-01", "Chống SQL Injection", "Nhập ' OR '1'='1 vào ô đăng nhập", "Bị chặn bởi Prepared Statement, báo sai mật khẩu", "Không bị tấn công", "ĐẠT ✓"],
        ["TC-SEC-02", "Bảo vệ truy cập URL", "Khách thuê gõ trực tiếp /admin/phong.php", "Hàm requireAdmin() chặn và chuyển hướng về user/", "Phân quyền chặt chẽ", "ĐẠT ✓"]
    ],
    "Bảng 4.5: Kết quả kiểm thử Hóa đơn, Thanh toán và Bảo mật"
)

add_sec1(doc, "4.3. Đánh Giá Kết Quả Đạt Được")
add_p(doc, "Đối chiếu với các mục tiêu ban đầu đề ra, dự án đã hoàn thành xuất sắc toàn bộ các yêu cầu chức năng và kỹ thuật:")
add_bullet(doc, "Về mặt chức năng: 100% các chức năng quản lý phòng, khách thuê, hợp đồng, điện nước, dịch vụ, hóa đơn, thanh toán, sự cố và thống kê đều hoạt động trơn tru, chính xác.")
add_bullet(doc, "Về mặt bảo mật: Hệ thống đảm bảo an toàn tuyệt đối trước các hình thức tấn công injection phổ biến nhờ PDO Prepared Statements; mật khẩu người dùng được băm mã hóa một chiều bằng Bcrypt.")
add_bullet(doc, "Về mặt giao diện: Giao diện Bootstrap 5 hiện đại, các biểu đồ Chart.js trực quan, thanh điều hướng sidebar co rút thông minh mang lại trải nghiệm tiện dụng tối đa cho người dùng.")
add_bullet(doc, "Về khả năng triển khai: Ứng dụng chạy mượt mà trên môi trường XAMPP tiêu chuẩn, không đòi hỏi cấu hình phức tạp, dễ dàng sao lưu và phục hồi qua tệp tin database.sql.")

add_sec1(doc, "4.4. Hạn Chế Của Đề Tài")
add_p(doc, "Mặc dù hệ thống đã đáp ứng đầy đủ các yêu cầu cốt lõi, vẫn còn một số điểm có thể hoàn thiện thêm:")
add_bullet(doc, "Chưa tích hợp cổng thanh toán trực tuyến tự động (VNPay, MoMo, ZaloPay): Việc ghi nhận thanh toán hiện tại vẫn do chủ trọ thao tác thủ công sau khi kiểm tra biến động số dư ngân hàng.")
add_bullet(doc, "Chưa có dịch vụ gửi thông báo tự động qua SMS Brandname hoặc Email khi có hóa đơn mới hay khi hợp đồng sắp hết hạn.")
add_bullet(doc, "Chưa hỗ trợ quản lý chuỗi nhiều chi nhánh nhà trọ độc lập trên cùng một tài khoản quản trị.")

add_sec1(doc, "4.5. Hướng Phát Triển Trong Tương Lai")
add_p(doc, "Trong các giai đoạn nâng cấp tiếp theo, nhóm tác giả dự kiến phát triển các tính năng mở rộng:")
add_bullet(doc, "Tích hợp cổng thanh toán trực tuyến qua mã VietQR động: Khách quét mã QR trên màn hình hóa đơn là giao dịch tự động được đối soát và gạch nợ tức thì.")
add_bullet(doc, "Tích hợp dịch vụ gửi tin nhắn tự động qua Zalo ZNS hoặc Telegram Bot nhắc lịch đóng tiền phòng.")
add_bullet(doc, "Phát triển ứng dụng di động Mobile App (Flutter hoặc React Native) kết nối qua RESTful API để nâng cao trải nghiệm cho khách thuê.")

print("5. Writing Conclusion, Appendices, References...")

add_chapter(doc, "KẾT LUẬN VÀ KIẾN NGHỊ")
add_p(doc, "Đề tài “Xây dựng Website Quản Lý Phòng Trọ” đã hoàn thành đúng tiến độ và đáp ứng toàn diện mục tiêu nghiên cứu đề ra. Hệ thống đã giải quyết thấu đáo bài toán quản lý nhà trọ vốn còn nhiều bất cập, mang lại giá trị thực tiễn cao cho cả người quản lý và người thuê phòng trọ.")
add_p(doc, "Thông qua quá trình thực hiện đề tài, nhóm sinh viên đã củng cố vững chắc kiến thức chuyên ngành:")
add_bullet(doc, "Nắm vững quy trình phân tích và thiết kế hệ thống thông tin theo phương pháp hướng đối tượng và phân tích luồng dữ liệu.")
add_bullet(doc, "Nâng cao kỹ năng lập trình web thực tế với PHP 8+, hệ quản trị cơ sở dữ liệu MySQL, và thiết kế giao diện responsive hiện đại với Bootstrap 5.")
add_bullet(doc, "Rèn luyện tư duy thiết kế cơ sở dữ liệu quan hệ chuẩn hóa 3NF và các nguyên tắc bảo mật web thực chiến.")
add_p(doc, "Kính mong nhận được những đóng góp và chỉ bảo quý báu từ quý Thầy, Cô trong hội đồng phản biện để đề tài ngày càng được hoàn thiện hơn nữa!")

add_chapter(doc, "PHỤ LỤC")

add_sec1(doc, "Phụ Lục A: Hướng Dẫn Cài Đặt Và Triển Khai Hệ Thống Trên XAMPP")
add_p(doc, "Các bước cài đặt và vận hành website trên máy tính cá nhân:")
add_bullet(doc, "Bước 1: Tải và cài đặt phần mềm XAMPP (phiên bản PHP 8.1 trở lên) từ trang chủ apachefriends.org.")
add_bullet(doc, "Bước 2: Khởi động bảng điều khiển XAMPP Control Panel, nhấn nút 'Start' cho cả hai dịch vụ Apache và MySQL.")
add_bullet(doc, "Bước 3: Sao chép toàn bộ thư mục QuanLyPhongTro vào thư mục gốc web server: C:\\xampp\\htdocs\\QuanLyPhongTro.")
add_bullet(doc, "Bước 4: Mở trình duyệt web, truy cập công cụ phpMyAdmin tại địa chỉ: http://localhost/phpmyadmin.")
add_bullet(doc, "Bước 5: Tạo một cơ sở dữ liệu mới với tên gọi quan_ly_phong_tro, bảng mã chọn utf8mb4_unicode_ci.")
add_bullet(doc, "Bước 6: Chọn tab 'Import' (Nhập), chọn tệp tin database.sql trong thư mục dự án và nhấn 'Go' để khởi tạo bảng và dữ liệu mẫu.")
add_bullet(doc, "Bước 7: Mở trình duyệt và truy cập website tại đường dẫn: http://localhost/QuanLyPhongTro.")

add_sec1(doc, "Phụ Lục B: Danh Sách Tài Khoản Demo Nghiệm Thu")
add_table(doc,
    ["Vai Trò", "Tên Đăng Nhập", "Mật Khẩu Mặc Định", "Mục Đích Thử Nghiệm"],
    [
        ["Quản Trị Viên (Admin)", "admin", "Admin@123", "Toàn quyền quản trị tất cả các phân hệ của nhà trọ."],
        ["Khách Thuê (Phòng P101)", "nguyen.van.a", "User@123", "Trải nghiệm portal khách thuê tại phòng P101."],
        ["Khách Thuê (Phòng P102)", "tran.thi.b", "User@123", "Trải nghiệm portal khách thuê tại phòng P102."],
        ["Khách Thuê (Phòng P201)", "le.van.c", "User@123", "Trải nghiệm portal khách thuê tại phòng P201."]
    ],
    "Bảng PL.1: Danh sách tài khoản demo tích hợp sẵn trong cơ sở dữ liệu"
)

add_sec1(doc, "Phụ Lục C: Bảng Danh Mục Công Nghệ Và Thư Viện Sử Dụng")
add_table(doc,
    ["Tên Công Nghệ / Thư Viện", "Phiên Bản", "Mục Đích Sử Dụng Trong Dự Án"],
    [
        ["PHP", "8.2+", "Ngôn ngữ kịch bản phía máy chủ (Server-Side Backend) xử lý logic nghiệp vụ."],
        ["MySQL", "8.0", "Hệ quản trị cơ sở dữ liệu quan hệ lưu trữ thông tin phòng, hợp đồng, hóa đơn."],
        ["Apache HTTP Server", "2.4", "Máy chủ web điều phối HTTP Request và phản hồi."],
        ["Bootstrap", "5.3.0", "CSS Framework hỗ trợ xây dựng giao diện tương thích đa thiết bị (Responsive)."],
        ["Font Awesome", "6.4.0", "Bộ biểu tượng vector sắc nét hỗ trợ trực quan hóa menu và nút bấm."],
        ["Chart.js", "4.4.0", "Thư viện JavaScript trực quan hóa dữ liệu thống kê doanh thu và tỷ lệ phòng."],
        ["jQuery", "3.7.0", "Thư viện hỗ trợ thao tác DOM và xử lý sự kiện phía Client."],
        ["PDO (PHP Data Objects)", "Tích hợp", "Giao diện trừu tượng kết nối cơ sở dữ liệu an toàn với Prepared Statements."],
        ["Bcrypt (password_hash)", "Tích hợp", "Thuật toán băm một chiều bảo vệ an toàn tuyệt đối mật khẩu người dùng."]
    ],
    "Bảng PL.2: Chi tiết công nghệ và phiên bản sử dụng trong dự án"
)

add_sec1(doc, "Phụ Lục D: Cấu Trúc Script SQL Khởi Tạo Cơ Sở Dữ Liệu")
add_p(doc, "Trích đoạn mã nguồn DDL tạo cấu trúc các bảng chính trong tệp database.sql:")

add_code(doc,
"""-- Khởi tạo cơ sở dữ liệu
CREATE DATABASE IF NOT EXISTS `quan_ly_phong_tro`
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `quan_ly_phong_tro`;

-- 1. Bảng tài khoản người dùng
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL UNIQUE,
  `password` varchar(255) NOT NULL,
  `ho_ten` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL UNIQUE,
  `so_dien_thoai` varchar(20) DEFAULT NULL,
  `vai_tro` enum('admin','khach_thue') NOT NULL DEFAULT 'khach_thue',
  `trang_thai` enum('hoat_dong','khoa') NOT NULL DEFAULT 'hoat_dong',
  `tenant_id` int(11) DEFAULT NULL,
  `lan_cuoi_dang_nhap` datetime DEFAULT NULL,
  `ngay_tao` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Bảng phòng trọ
CREATE TABLE `rooms` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ma_phong` varchar(20) NOT NULL UNIQUE,
  `ten_phong` varchar(100) NOT NULL,
  `loai_phong` varchar(50) NOT NULL DEFAULT 'Phòng thường',
  `tang` int(11) NOT NULL DEFAULT 1,
  `khu` varchar(20) DEFAULT NULL,
  `dien_tich` decimal(5,2) NOT NULL DEFAULT 20.00,
  `gia_thue` decimal(12,2) NOT NULL DEFAULT 0.00,
  `tien_coc` decimal(12,2) DEFAULT 0.00,
  `so_nguoi_toi_da` int(11) NOT NULL DEFAULT 2,
  `trang_thai` enum('trong','dang_thue','dang_sua_chua') NOT NULL DEFAULT 'trong',
  `mo_ta` text DEFAULT NULL,
  `ngay_tao` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Bảng khách thuê
CREATE TABLE `tenants` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ho_ten` varchar(100) NOT NULL,
  `ngay_sinh` date DEFAULT NULL,
  `gioi_tinh` enum('Nam','Nu','Khac') NOT NULL DEFAULT 'Nam',
  `so_dien_thoai` varchar(20) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `so_cmnd` varchar(20) DEFAULT NULL,
  `dia_chi` varchar(255) DEFAULT NULL,
  `nghe_nghiep` varchar(100) DEFAULT NULL,
  `room_id` int(11) DEFAULT NULL,
  `ngay_bat_dau_thue` date NOT NULL,
  `trang_thai` enum('dang_thue','da_roi') NOT NULL DEFAULT 'dang_thue',
  `ghi_chu` text DEFAULT NULL,
  `ngay_tao` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"""
)

add_chapter(doc, "TÀI LIỆU THAM KHẢO")
refs = [
    "[1]  PHP Group (2024). PHP: Hypertext Preprocessor Official Documentation. https://www.php.net/docs.php",
    "[2]  Oracle Corporation (2024). MySQL 8.0 Reference Manual. https://dev.mysql.com/doc/refman/8.0/en/",
    "[3]  Bootstrap Team (2023). Bootstrap 5.3 Documentation & Components. https://getbootstrap.com/docs/5.3/",
    "[4]  Chart.js Project (2024). Chart.js - Simple yet flexible JavaScript charting for designers & developers. https://www.chartjs.org/",
    "[5]  Fonticons, Inc. (2023). Font Awesome 6 Icon Directory & Documentation. https://fontawesome.com/",
    "[6]  The Open Web Application Security Project - OWASP (2024). SQL Injection Prevention Cheat Sheet. https://cheatsheetseries.owasp.org/",
    "[7]  The Open Web Application Security Project - OWASP (2024). Password Storage Cheat Sheet. https://cheatsheetseries.owasp.org/",
    "[8]  W3Schools (2024). PHP 8 Tutorial & MySQL Database Access. https://www.w3schools.com/php/",
    "[9]  Mozilla Developer Network - MDN (2024). Web Technologies Documentation: HTML5, CSS3, JavaScript. https://developer.mozilla.org/",
    "[10] Rasmus Lerdorf, Kevin Tatroe, Peter MacIntyre (2022). Programming PHP: Creating Dynamic Web Pages (4th Edition). O'Reilly Media.",
    "[11] Paul DuBois (2018). MySQL (Developer's Library) 5th Edition. Addison-Wesley Professional.",
    "[12] Martin Fowler (2012). Patterns of Enterprise Application Architecture. Addison-Wesley."
]

for ref in refs:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Cm(0.8)
    p.paragraph_format.first_line_indent = Cm(-0.8)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.2
    run = p.add_run(ref)
    set_font(run, size=11.5)

print("Saving final report...")
doc.save(OUT_PATH)
print(f"SUCCESS! Saved report to: {OUT_PATH}")
