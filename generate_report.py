"""
Script tạo báo cáo đồ án Quản Lý Phòng Trọ - Fixed version
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document(r'c:\xampp\htdocs\QuanLyPhongTro\template.docx')

# ─── Helpers ──────────────────────────────────────────────────────────────────
def set_font(run, name='Times New Roman', size=13, bold=False, italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)
    # Ensure CJK/Vietnamese font
    rPr = run._r.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:eastAsia'), name)
    rPr.insert(0, rFonts)

def h1(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    set_font(run, size=14, bold=True)
    return p

def h2(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    set_font(run, size=13, bold=True)
    return p

def h3(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run(text)
    set_font(run, size=12, bold=True, italic=True)
    return p

def body(doc, text, bold=False, italic=False, indent=True, center=False, size=13):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.JUSTIFY
    if indent and not center:
        p.paragraph_format.first_line_indent = Cm(1.27)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    set_font(run, size=size, bold=bold, italic=italic)
    return p

def bul(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Cm(1.27)
    p.paragraph_format.first_line_indent = Cm(-0.63)
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run('\u2022  ' + text)
    set_font(run, size=12)
    return p

def img_placeholder(doc, caption):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(f'[ Ảnh chụp màn hình: {caption} ]')
    set_font(run, size=11, italic=True, color=(120, 120, 120))
    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run2 = p2.add_run(caption)
    set_font(run2, size=11, italic=True, bold=True)
    doc.add_paragraph()

def make_table(doc, headers, rows, caption=None):
    if caption:
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = cp.add_run(caption)
        set_font(r, size=11, bold=True, italic=True)

    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.style = 'Table Grid'

    # Header row
    hr = tbl.rows[0]
    for i, h in enumerate(headers):
        c = hr.cells[i]
        c.text = ''
        run = c.paragraphs[0].add_run(h)
        set_font(run, size=11, bold=True)
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        # Gray background
        tc = c._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), 'DDEEFF')
        tcPr.append(shd)

    # Data rows
    for ri, row in enumerate(rows):
        tr = tbl.rows[ri + 1]
        for ci, val in enumerate(row):
            c = tr.cells[ci]
            c.text = ''
            run = c.paragraphs[0].add_run(str(val))
            set_font(run, size=10)

    doc.add_paragraph()
    return tbl

def code_block(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.left_indent = Cm(1)
    p.paragraph_format.space_after = Pt(6)
    # Light gray background
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), 'F5F5F5')
    pPr.append(shd)
    run = p.add_run(text)
    run.font.name = 'Courier New'
    run.font.size = Pt(9)
    return p

def pb(doc):
    doc.add_page_break()

# ─── Tìm và xóa từ Chương II trở đi ─────────────────────────────────────────
to_del = []
found = False
for p in doc.paragraphs:
    if not found and ('Chương II' in p.text or 'chương II' in p.text.lower()):
        found = True
    if found:
        to_del.append(p)

print(f"Xóa {len(to_del)} đoạn từ Chương II trở đi")
for p in to_del:
    p._element.getparent().remove(p._element)

# Sửa tên đề tài trên bìa
for p in doc.paragraphs:
    for run in p.runs:
        if 'điện thoại' in run.text.lower() or 'bán hàng' in run.text.lower():
            run.text = run.text.replace('Website bán điện thoại di động trực tuyến', 'WEBSITE QUẢN LÝ PHÒNG TRỌ')
            run.text = run.text.replace('website bán điện thoại di động trực tuyến', 'WEBSITE QUẢN LÝ PHÒNG TRỌ')
            run.text = run.text.replace('Website bán điện thoại', 'WEBSITE QUẢN LÝ PHÒNG TRỌ')

print("Đã chuẩn bị xong, bắt đầu viết nội dung...")

# ═══════════════════════════════════════════════════════════════════════════════
# CHƯƠNG II
# ═══════════════════════════════════════════════════════════════════════════════
pb(doc)
h1(doc, 'CHƯƠNG II: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG')

h2(doc, '2.1. Khảo Sát Và Xác Định Yêu Cầu Hệ Thống')
body(doc, 'Hệ thống Quản Lý Phòng Trọ được xây dựng nhằm số hóa toàn bộ quy trình quản lý hoạt động '
     'của một khu nhà trọ, từ khâu tiếp nhận người thuê, ký kết hợp đồng, theo dõi chỉ số điện nước, '
     'lập hóa đơn đến quản lý thu chi và xử lý sự cố. Việc khảo sát thực tế cho thấy hầu hết các chủ '
     'nhà trọ hiện nay đang quản lý bằng sổ sách thủ công, dẫn đến nhiều sai sót và tốn thời gian.')

body(doc, 'Mô hình quản lý thủ công có nhiều bất cập: chủ trọ phải ghi chép số liệu điện nước bằng tay, '
     'tính toán hóa đơn theo từng phòng mỗi tháng, khó theo dõi lịch sử thanh toán và không thể '
     'thông báo tức thì cho người thuê khi có hóa đơn mới. Website Quản Lý Phòng Trọ ra đời '
     'giải quyết triệt để những vấn đề này.')

h3(doc, '2.1.1. Đối Tượng Sử Dụng Hệ Thống')
body(doc, 'Hệ thống phục vụ cho hai nhóm đối tượng chính:')
bul(doc, 'Admin / Chủ trọ: Người quản lý toàn bộ khu nhà trọ, có đầy đủ quyền hạn trên hệ thống. Admin có thể thêm/sửa/xóa phòng, quản lý người thuê, hợp đồng, hóa đơn, thanh toán, điện nước, dịch vụ và xử lý sự cố.')
bul(doc, 'Khách thuê: Người đang thuê phòng tại khu trọ. Khách thuê chỉ được xem thông tin cá nhân, thông tin phòng đang thuê, hóa đơn, lịch sử thanh toán và gửi yêu cầu sửa chữa/báo sự cố. Không thể truy cập trang quản trị.')

h3(doc, '2.1.2. Yêu Cầu Chức Năng')
body(doc, 'Dựa trên kết quả khảo sát, hệ thống cần đáp ứng các yêu cầu chức năng sau:')
make_table(doc,
    ['STT', 'Chức Năng', 'Mô Tả', 'Đối Tượng'],
    [
        ['1', 'Đăng nhập / Đăng xuất', 'Xác thực người dùng, phân quyền theo vai trò', 'Admin, Khách thuê'],
        ['2', 'Quản lý tài khoản', 'Thêm, sửa, khóa/mở tài khoản người dùng', 'Admin'],
        ['3', 'Quản lý phòng', 'CRUD phòng, theo dõi trạng thái phòng', 'Admin'],
        ['4', 'Quản lý người thuê', 'CRUD thông tin khách thuê, liên kết với phòng', 'Admin'],
        ['5', 'Quản lý hợp đồng', 'Tạo, sửa, gia hạn, thanh lý hợp đồng thuê phòng', 'Admin'],
        ['6', 'Quản lý điện nước', 'Nhập chỉ số điện/nước theo tháng, tự động tính tiền', 'Admin'],
        ['7', 'Quản lý dịch vụ', 'Định nghĩa và quản lý dịch vụ đi kèm', 'Admin'],
        ['8', 'Quản lý hóa đơn', 'Tạo hóa đơn tổng hợp theo tháng, in hóa đơn', 'Admin'],
        ['9', 'Quản lý thanh toán', 'Ghi nhận thanh toán, cập nhật trạng thái hóa đơn', 'Admin'],
        ['10', 'Quản lý sự cố', 'Tiếp nhận, xử lý và cập nhật trạng thái sự cố', 'Admin, Khách thuê'],
        ['11', 'Thống kê báo cáo', 'Biểu đồ doanh thu, điện nước, top phòng', 'Admin'],
        ['12', 'Dashboard tổng quan', 'Hiển thị các chỉ số quan trọng khi đăng nhập', 'Admin, Khách thuê'],
        ['13', 'Xem thông tin cá nhân', 'Khách thuê xem phòng, hóa đơn, hợp đồng của mình', 'Khách thuê'],
        ['14', 'Đổi mật khẩu', 'Người dùng tự đổi mật khẩu tài khoản', 'Admin, Khách thuê'],
    ],
    'Bảng 2.1: Danh sách yêu cầu chức năng hệ thống'
)

h3(doc, '2.1.3. Yêu Cầu Phi Chức Năng')
body(doc, 'Ngoài các yêu cầu chức năng, hệ thống cần đáp ứng các yêu cầu phi chức năng:')
bul(doc, 'Bảo mật: Sử dụng Session PHP để quản lý đăng nhập, mã hóa mật khẩu bằng password_hash() (bcrypt), sử dụng Prepared Statements để ngăn SQL Injection.')
bul(doc, 'Giao diện: Responsive Design sử dụng Bootstrap 5, tương thích với mọi thiết bị và trình duyệt hiện đại (Chrome, Firefox, Edge).')
bul(doc, 'Hiệu năng: Tối ưu truy vấn SQL bằng INDEX trên các trường thường xuyên tìm kiếm (username, trang_thai, room_id).')
bul(doc, 'Khả năng mở rộng: Cấu trúc code rõ ràng, tách biệt theo module, dễ bổ sung tính năng mới.')
bul(doc, 'Môi trường chạy: XAMPP (Apache + PHP 8+ + MySQL 8.0), không yêu cầu cài đặt phức tạp.')
bul(doc, 'Tính đúng đắn dữ liệu: Sử dụng FOREIGN KEY và UNIQUE KEY trong CSDL để đảm bảo tính toàn vẹn dữ liệu.')

h2(doc, '2.2. Phân Tích Hệ Thống Theo Use Case')

h3(doc, '2.2.1. Sơ Đồ Use Case Tổng Quát')
body(doc, 'Sơ đồ Use Case tổng quát mô tả các tác nhân (Actor) tương tác với hệ thống và '
     'các chức năng chính mà hệ thống cung cấp. Hệ thống có hai tác nhân chính:')
bul(doc, 'Actor 1 – Admin (Chủ trọ): Quản lý toàn diện hệ thống với 12 nhóm chức năng chính.')
bul(doc, 'Actor 2 – Khách Thuê: Sử dụng portal riêng với 8 chức năng xem thông tin và gửi yêu cầu.')

img_placeholder(doc, 'Hình 2.1: Sơ đồ Use Case tổng quát hệ thống Quản Lý Phòng Trọ')

h3(doc, '2.2.2. Mô Tả Chi Tiết Use Case Đăng Nhập (UC-01)')
make_table(doc,
    ['Thuộc Tính', 'Nội Dung'],
    [
        ['Tên Use Case', 'Đăng nhập hệ thống'],
        ['Mã UC', 'UC-01'],
        ['Tác nhân', 'Admin, Khách Thuê'],
        ['Mô tả', 'Người dùng nhập tên đăng nhập và mật khẩu để xác thực và truy cập hệ thống'],
        ['Tiền điều kiện', 'Người dùng đã có tài khoản được cấp bởi Admin'],
        ['Hậu điều kiện', 'Hệ thống tạo Session và chuyển hướng theo vai trò'],
        ['Luồng chính', '1. Truy cập trang login.php\n2. Nhập username và password\n3. Hệ thống kiểm tra thông tin với CSDL\n4. Nếu đúng: tạo $_SESSION, redirect theo vai trò\n5. Admin → admin/dashboard.php | Khách thuê → user/dashboard.php'],
        ['Luồng ngoại lệ', 'Tài khoản bị khóa → thông báo lỗi\nSai mật khẩu → thông báo "Tên đăng nhập hoặc mật khẩu không đúng"'],
    ],
    'Bảng 2.2: Mô tả Use Case UC-01 – Đăng nhập hệ thống'
)

h3(doc, '2.2.3. Mô Tả Chi Tiết Use Case Quản Lý Hóa Đơn (UC-08)')
make_table(doc,
    ['Thuộc Tính', 'Nội Dung'],
    [
        ['Tên Use Case', 'Quản lý hóa đơn'],
        ['Mã UC', 'UC-08'],
        ['Tác nhân', 'Admin'],
        ['Mô tả', 'Admin tạo hóa đơn tổng hợp hàng tháng cho từng phòng (tiền phòng + điện + nước + dịch vụ)'],
        ['Tiền điều kiện', 'Phòng đang có người thuê; Đã nhập chỉ số điện nước tháng đó'],
        ['Hậu điều kiện', 'Hóa đơn được lưu với trạng thái "Chưa thanh toán"; Khách thuê có thể xem trên portal'],
        ['Luồng chính', '1. Admin chọn phòng và tháng/năm\n2. Nhập tiền phòng, điện, nước, dịch vụ, phí khác\n3. Hệ thống tự động tính tổng tiền theo thời gian thực\n4. Admin xác nhận lưu hóa đơn\n5. Có thể in hóa đơn (print-friendly page)'],
        ['Mở rộng', 'Admin có thể lọc hóa đơn theo tháng/năm/trạng thái;\nCó thể cập nhật trạng thái hóa đơn thủ công'],
    ],
    'Bảng 2.3: Mô tả Use Case UC-08 – Quản lý hóa đơn'
)

h2(doc, '2.3. Biểu Đồ Luồng Dữ Liệu (DFD)')

h3(doc, '2.3.1. DFD Mức 0 – Biểu Đồ Ngữ Cảnh')
body(doc, 'Biểu đồ ngữ cảnh mức 0 thể hiện toàn bộ hệ thống như một tiến trình duy nhất, '
     'mô tả mối quan hệ giữa hệ thống với các tác nhân bên ngoài. Admin cung cấp thông tin '
     'quản lý và nhận báo cáo thống kê; Khách Thuê nhập thông tin sự cố và nhận thông tin '
     'hóa đơn, hợp đồng từ hệ thống.')

img_placeholder(doc, 'Hình 2.2: DFD Mức 0 – Biểu đồ ngữ cảnh hệ thống Quản Lý Phòng Trọ')

h3(doc, '2.3.2. DFD Mức 1 – Biểu Đồ Chi Tiết Các Tiến Trình')
body(doc, 'DFD mức 1 phân rã hệ thống thành 5 tiến trình con chính:')
bul(doc, 'Tiến trình 1 – Xác thực người dùng: Xử lý đăng nhập/đăng xuất, kiểm tra quyền truy cập')
bul(doc, 'Tiến trình 2 – Quản lý phòng & người thuê: CRUD phòng, người thuê, hợp đồng')
bul(doc, 'Tiến trình 3 – Quản lý tài chính: Điện nước, hóa đơn, thanh toán, dịch vụ')
bul(doc, 'Tiến trình 4 – Quản lý sự cố: Tiếp nhận, xử lý yêu cầu sửa chữa')
bul(doc, 'Tiến trình 5 – Thống kê báo cáo: Tổng hợp doanh thu, biểu đồ, xuất báo cáo')

img_placeholder(doc, 'Hình 2.3: DFD Mức 1 – Luồng dữ liệu chi tiết các module chức năng')

h2(doc, '2.4. Thiết Kế Cơ Sở Dữ Liệu')

h3(doc, '2.4.1. Mô Hình Thực Thể Liên Kết (ERD)')
body(doc, 'Mô hình ERD thể hiện cấu trúc dữ liệu và mối quan hệ giữa các thực thể trong hệ thống. '
     'Cơ sở dữ liệu có tên quan_ly_phong_tro với 10 bảng dữ liệu chính, được chuẩn hóa '
     'về dạng chuẩn 3NF (Third Normal Form) để giảm thiểu dư thừa dữ liệu.')

img_placeholder(doc, 'Hình 2.4: Mô hình ERD – Quan hệ giữa 10 bảng dữ liệu trong hệ thống')

h3(doc, '2.4.2. Mô Tả Các Bảng Dữ Liệu')
make_table(doc,
    ['STT', 'Tên Bảng', 'Mô Tả Chức Năng', 'Quan Hệ Chính'],
    [
        ['1', 'users', 'Tài khoản người dùng, vai trò và trạng thái', 'FK: tenant_id → tenants'],
        ['2', 'rooms', 'Thông tin chi tiết các phòng trọ', 'Referenced by: tenants, contracts, invoices'],
        ['3', 'tenants', 'Thông tin người thuê phòng', 'FK: room_id → rooms'],
        ['4', 'contracts', 'Hợp đồng thuê phòng', 'FK: room_id → rooms, tenant_id → tenants'],
        ['5', 'electric_water', 'Chỉ số điện nước theo tháng của từng phòng', 'FK: room_id → rooms'],
        ['6', 'services', 'Danh mục dịch vụ và đơn giá', 'Referenced by: service_usage'],
        ['7', 'service_usage', 'Sử dụng dịch vụ của từng phòng theo tháng', 'FK: room_id, service_id'],
        ['8', 'invoices', 'Hóa đơn tổng hợp theo tháng', 'FK: room_id → rooms, tenant_id → tenants'],
        ['9', 'payments', 'Lịch sử thanh toán hóa đơn', 'FK: invoice_id → invoices, tenant_id → tenants'],
        ['10', 'maintenance_requests', 'Yêu cầu sửa chữa/sự cố', 'FK: room_id → rooms, tenant_id → tenants'],
    ],
    'Bảng 2.4: Danh sách và quan hệ các bảng trong CSDL'
)

h3(doc, '2.4.3. Cấu Trúc Bảng users – Quản Lý Tài Khoản')
make_table(doc,
    ['STT', 'Tên Cột', 'Kiểu Dữ Liệu', 'Ràng Buộc', 'Mô Tả'],
    [
        ['1', 'id', 'INT', 'PK, AI', 'Khóa chính tự tăng'],
        ['2', 'username', 'VARCHAR(50)', 'UNIQUE, NN', 'Tên đăng nhập duy nhất'],
        ['3', 'password', 'VARCHAR(255)', 'NOT NULL', 'Mật khẩu mã hóa bcrypt'],
        ['4', 'ho_ten', 'VARCHAR(100)', 'NOT NULL', 'Họ và tên đầy đủ'],
        ['5', 'email', 'VARCHAR(100)', 'UNIQUE', 'Địa chỉ email'],
        ['6', 'so_dien_thoai', 'VARCHAR(20)', '', 'Số điện thoại liên hệ'],
        ['7', 'vai_tro', "ENUM('admin','khach_thue')", 'NOT NULL', 'Vai trò người dùng'],
        ['8', 'trang_thai', "ENUM('hoat_dong','khoa')", 'DEFAULT hoat_dong', 'Trạng thái tài khoản'],
        ['9', 'tenant_id', 'INT', 'FK → tenants.id', 'Liên kết với người thuê'],
        ['10', 'ngay_tao', 'DATETIME', 'DEFAULT NOW()', 'Ngày tạo tài khoản'],
    ],
    'Bảng 2.5: Cấu trúc bảng users'
)

h3(doc, '2.4.4. Cấu Trúc Bảng rooms – Quản Lý Phòng')
make_table(doc,
    ['STT', 'Tên Cột', 'Kiểu Dữ Liệu', 'Ràng Buộc', 'Mô Tả'],
    [
        ['1', 'id', 'INT', 'PK, AI', 'Khóa chính'],
        ['2', 'ma_phong', 'VARCHAR(20)', 'UNIQUE, NN', 'Mã phòng (vd: P101, A201)'],
        ['3', 'ten_phong', 'VARCHAR(100)', 'NOT NULL', 'Tên phòng'],
        ['4', 'loai_phong', 'VARCHAR(50)', '', 'Loại phòng (thường/studio/cao cấp)'],
        ['5', 'tang', 'INT', '', 'Số tầng'],
        ['6', 'khu', 'VARCHAR(20)', '', 'Khu (A, B, C...)'],
        ['7', 'dien_tich', 'DECIMAL(5,2)', '', 'Diện tích m²'],
        ['8', 'gia_thue', 'DECIMAL(12,2)', 'NOT NULL', 'Giá thuê tháng (đồng)'],
        ['9', 'tien_coc', 'DECIMAL(12,2)', '', 'Tiền đặt cọc (đồng)'],
        ['10', 'so_nguoi_toi_da', 'INT', 'DEFAULT 2', 'Số người ở tối đa'],
        ['11', 'trang_thai', 'ENUM', 'DEFAULT trong', 'trong/dang_thue/dang_sua_chua'],
        ['12', 'mo_ta', 'TEXT', '', 'Mô tả chi tiết phòng'],
    ],
    'Bảng 2.6: Cấu trúc bảng rooms'
)

h3(doc, '2.4.5. Cấu Trúc Bảng invoices – Quản Lý Hóa Đơn')
make_table(doc,
    ['STT', 'Tên Cột', 'Kiểu Dữ Liệu', 'Ràng Buộc', 'Mô Tả'],
    [
        ['1', 'id', 'INT', 'PK, AI', 'Khóa chính'],
        ['2', 'ma_hoa_don', 'VARCHAR(30)', 'UNIQUE', 'Mã hóa đơn tự sinh (VD: HD2024010001)'],
        ['3', 'room_id', 'INT', 'FK → rooms', 'Phòng tương ứng'],
        ['4', 'tenant_id', 'INT', 'FK → tenants', 'Người thuê tương ứng'],
        ['5', 'thang', 'INT', 'NOT NULL', 'Tháng lập hóa đơn (1-12)'],
        ['6', 'nam', 'INT', 'NOT NULL', 'Năm lập hóa đơn'],
        ['7', 'tien_phong', 'DECIMAL(12,2)', '', 'Tiền thuê phòng tháng đó'],
        ['8', 'tien_dien', 'DECIMAL(12,2)', 'DEFAULT 0', 'Tiền điện (tính từ electric_water)'],
        ['9', 'tien_nuoc', 'DECIMAL(12,2)', 'DEFAULT 0', 'Tiền nước (tính từ electric_water)'],
        ['10', 'tien_dich_vu', 'DECIMAL(12,2)', 'DEFAULT 0', 'Tổng tiền dịch vụ'],
        ['11', 'phi_khac', 'DECIMAL(12,2)', 'DEFAULT 0', 'Phí phát sinh khác'],
        ['12', 'tong_tien', 'DECIMAL(12,2)', 'NOT NULL', 'Tổng = tiền phòng+điện+nước+dịch vụ+khác'],
        ['13', 'han_thanh_toan', 'DATE', '', 'Hạn phải thanh toán'],
        ['14', 'trang_thai', 'ENUM', 'DEFAULT chua_tt', 'chua_thanh_toan/da_thanh_toan/qua_han'],
        ['15', 'ghi_chu', 'TEXT', '', 'Ghi chú hóa đơn'],
        ['16', 'ngay_tao', 'DATETIME', 'DEFAULT NOW()', 'Thời điểm tạo hóa đơn'],
    ],
    'Bảng 2.7: Cấu trúc bảng invoices'
)

# ═══════════════════════════════════════════════════════════════════════════════
# CHƯƠNG III
# ═══════════════════════════════════════════════════════════════════════════════
pb(doc)
h1(doc, 'CHƯƠNG III: XÂY DỰNG HỆ THỐNG')

h2(doc, '3.1. Cấu Trúc Thư Mục Dự Án')
body(doc, 'Dự án được tổ chức theo cấu trúc thư mục rõ ràng, tách biệt các thành phần '
     'theo chức năng, phù hợp với nguyên tắc Separation of Concerns trong lập trình web. '
     'Toàn bộ dự án nằm trong thư mục QuanLyPhongTro trong XAMPP htdocs:')

make_table(doc,
    ['Thư Mục / File', 'Mô Tả Chức Năng'],
    [
        ['config/database.php', 'Cấu hình và khởi tạo kết nối PDO đến MySQL'],
        ['includes/auth.php', 'Hàm xác thực: isLoggedIn(), requireAdmin(), requireKhachThue(), getCurrentUser()'],
        ['includes/functions.php', 'Hàm tiện ích: formatMoney(), getStatusBadge(), renderPagination(), showFlash()'],
        ['includes/header.php', 'HTML head + topbar cho Admin (load CSS, Bootstrap)'],
        ['includes/sidebar.php', 'Menu sidebar điều hướng 13 mục cho Admin'],
        ['includes/header_user.php', 'HTML head + topbar cho Khách Thuê'],
        ['includes/sidebar_user.php', 'Menu sidebar điều hướng 8 mục cho Khách Thuê'],
        ['includes/footer.php', 'Đóng HTML, load Bootstrap JS, jQuery, script.js'],
        ['assets/css/style.css', 'CSS tùy chỉnh: layout 2 cột, sidebar, card, bảng, badge'],
        ['assets/css/login.css', 'CSS trang đăng nhập với gradient và animation'],
        ['assets/js/script.js', 'JavaScript: toggle sidebar, đồng hồ real-time, confirm delete'],
        ['admin/ (12 file PHP)', 'Trang quản trị: dashboard, phòng, người thuê, hóa đơn...'],
        ['user/ (8 file PHP)', 'Portal khách thuê: xem thông tin, báo sự cố...'],
        ['login.php / logout.php', 'Đăng nhập và xử lý đăng xuất'],
        ['database.sql', 'Script SQL tạo CSDL, bảng và dữ liệu mẫu'],
    ],
    'Bảng 3.1: Cấu trúc thư mục dự án'
)

h2(doc, '3.2. Kết Nối Và Bảo Mật Cơ Sở Dữ Liệu')

h3(doc, '3.2.1. Kết Nối PDO Với Singleton Pattern')
body(doc, 'File config/database.php sử dụng PDO (PHP Data Objects) với Singleton Pattern '
     '– chỉ tạo một kết nối CSDL duy nhất cho toàn bộ request, tiết kiệm tài nguyên server:')

code_block(doc,
    '<?php\n'
    'define("DB_HOST", "localhost");\n'
    'define("DB_NAME", "quan_ly_phong_tro");\n'
    'define("DB_USER", "root");\n'
    'define("DB_PASS", "");\n\n'
    'function getDB(): PDO {\n'
    '    static $pdo = null;\n'
    '    if ($pdo === null) {\n'
    '        $dsn = "mysql:host=".DB_HOST.";dbname=".DB_NAME.";charset=utf8mb4";\n'
    '        $pdo = new PDO($dsn, DB_USER, DB_PASS, [\n'
    '            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,\n'
    '            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,\n'
    '            PDO::ATTR_EMULATE_PREPARES   => false,\n'
    '        ]);\n'
    '    }\n'
    '    return $pdo;\n'
    '}\n'
    '$pdo = getDB();'
)

h3(doc, '3.2.2. Bảo Mật SQL Injection Bằng Prepared Statements')
body(doc, 'Toàn bộ truy vấn SQL trong hệ thống đều sử dụng Prepared Statements – phương '
     'pháp an toàn nhất để ngăn SQL Injection. Thay vì nối chuỗi trực tiếp vào câu lệnh SQL, '
     'các tham số được truyền vào sau khi câu lệnh đã được biên dịch:')

code_block(doc,
    '// SAI - Dễ bị SQL Injection\n'
    '$sql = "SELECT * FROM users WHERE username=\'" . $username . "\'";\n\n'
    '// ĐÚNG - Prepared Statement an toàn\n'
    '$stmt = $pdo->prepare("SELECT * FROM users WHERE username=? AND trang_thai=?");\n'
    '$stmt->execute([$username, "hoat_dong"]);\n'
    '$user = $stmt->fetch();\n\n'
    '// Kiểm tra mật khẩu bcrypt\n'
    'if ($user && password_verify($password, $user["password"])) {\n'
    '    $_SESSION["user_id"] = $user["id"];\n'
    '    $_SESSION["vai_tro"] = $user["vai_tro"];\n'
    '    // Redirect theo vai trò\n'
    '    redirectByRole($user["vai_tro"]);\n'
    '}'
)

h2(doc, '3.3. Module Đăng Nhập Và Phân Quyền')

body(doc, 'Hệ thống đăng nhập sử dụng PHP Session để duy trì trạng thái đăng nhập giữa '
     'các trang. Mật khẩu được mã hóa một chiều bằng thuật toán bcrypt (cost factor = 10) '
     'thông qua password_hash() của PHP – thuật toán được khuyến nghị bởi OWASP và các '
     'chuyên gia bảo mật toàn cầu.')

body(doc, 'Giao diện trang đăng nhập được thiết kế hiện đại với:')
bul(doc, 'Gradient background xanh dương chuyển tiếp mượt mà (135deg gradient)')
bul(doc, 'Card đăng nhập trắng với border-radius 20px, box-shadow tạo độ nổi')
bul(doc, 'Input group có icon hiển thị/ẩn mật khẩu (toggle password visibility)')
bul(doc, 'Khối demo accounts: click để tự động điền thông tin đăng nhập')
bul(doc, 'Animation fadeInUp khi load trang (CSS @keyframes)')
bul(doc, 'Thông báo lỗi rõ ràng trong alert Bootstrap khi sai thông tin')

img_placeholder(doc, 'Hình 3.1: Giao diện trang đăng nhập hệ thống Quản Lý Phòng Trọ')

body(doc, 'Hệ thống phân quyền dựa trên trường vai_tro trong bảng users. Hàm '
     'requireAdmin() và requireKhachThue() trong includes/auth.php kiểm tra quyền '
     'ở đầu mỗi file PHP, tự động redirect nếu không đủ quyền:')

code_block(doc,
    '// includes/auth.php\n'
    'function requireAdmin() {\n'
    '    if (!isLoggedIn()) { header("Location: /QuanLyPhongTro/login.php"); exit(); }\n'
    '    if ($_SESSION["vai_tro"] !== "admin") {\n'
    '        header("Location: /QuanLyPhongTro/user/dashboard.php"); exit();\n'
    '    }\n'
    '}\n\n'
    '// Sử dụng ở đầu mỗi trang admin\n'
    'require_once "../includes/auth.php";\n'
    'requireAdmin(); // Khách thuê không vào được trang này'
)

h2(doc, '3.4. Module Dashboard Tổng Quan (Admin)')

body(doc, 'Dashboard (admin/dashboard.php) là trang đầu tiên Admin thấy sau khi đăng nhập. '
     'Trang này hiển thị tổng quan toàn bộ hoạt động của khu nhà trọ, giúp Admin nắm bắt '
     'tình hình ngay lập tức mà không cần vào từng module.')

body(doc, 'Các thành phần của Dashboard Admin:')
bul(doc, '4 thẻ thống kê (Stat Cards): Tổng số phòng, Doanh thu tháng này, Hóa đơn chưa thanh toán, Sự cố chờ xử lý')
bul(doc, 'Biểu đồ Donut (Chart.js): Tỷ lệ phòng đang thuê / còn trống / sửa chữa')
bul(doc, 'Biểu đồ cột (Chart.js): Doanh thu 6 tháng gần nhất (tự động cập nhật)')
bul(doc, 'Bảng hóa đơn gần đây: 8 hóa đơn mới nhất với trạng thái màu sắc trực quan')
bul(doc, 'Danh sách sự cố mới: 5 sự cố chưa xử lý, cần chú ý ngay')

img_placeholder(doc, 'Hình 3.2: Dashboard Admin – 4 thẻ thống kê và biểu đồ tình trạng phòng')

img_placeholder(doc, 'Hình 3.3: Dashboard Admin – Biểu đồ doanh thu 6 tháng và bảng hóa đơn gần đây')

h2(doc, '3.5. Module Quản Lý Phòng Trọ (admin/phong.php)')

body(doc, 'Module quản lý phòng cho phép Admin thực hiện đầy đủ thao tác CRUD trên '
     'danh sách phòng trọ. Giao diện sử dụng modal Bootstrap để thêm/sửa phòng '
     'mà không phải tải lại trang, mang lại trải nghiệm mượt mà như ứng dụng desktop.')

body(doc, 'Chức năng chính:')
bul(doc, '4 thẻ thống kê nhanh: Tổng phòng, Đang thuê, Còn trống, Đang sửa chữa')
bul(doc, 'Tìm kiếm theo mã phòng hoặc tên phòng (tức thời khi submit form)')
bul(doc, 'Lọc theo trạng thái (trống/đang thuê/sửa chữa) và loại phòng')
bul(doc, 'Phân trang 10 phòng/trang với nút Previous/Next')
bul(doc, 'Thêm phòng mới qua modal – dữ liệu reset tự động khi mở modal')
bul(doc, 'Sửa phòng qua modal – JavaScript tự động điền dữ liệu phòng vào form')
bul(doc, 'Xóa phòng với kiểm tra ràng buộc: không xóa được phòng đang có người thuê')
bul(doc, 'Hiển thị số người hiện tại / tối đa cho mỗi phòng')

img_placeholder(doc, 'Hình 3.4: Trang quản lý phòng – Danh sách, thẻ thống kê và bộ lọc')

img_placeholder(doc, 'Hình 3.5: Modal thêm/sửa phòng với đầy đủ thông tin chi tiết')

h2(doc, '3.6. Module Quản Lý Người Thuê (admin/nguoi_thue.php)')

body(doc, 'Module quản lý người thuê lưu trữ thông tin cá nhân đầy đủ của tất cả '
     'người thuê (hiện tại và lịch sử). Mỗi người thuê được liên kết với phòng '
     'và tài khoản đăng nhập tương ứng.')

body(doc, 'Thông tin quản lý bao gồm:')
bul(doc, 'Thông tin cá nhân: Họ tên, ngày sinh, giới tính, số CMND/CCCD, nghề nghiệp')
bul(doc, 'Liên lạc: Số điện thoại, email, địa chỉ thường trú')
bul(doc, 'Thông tin thuê: Phòng đang thuê (dropdown), ngày bắt đầu thuê, trạng thái')
bul(doc, 'Ghi chú tự do về người thuê')
bul(doc, 'Khi thêm người thuê mới và gán phòng: hệ thống tự động cập nhật trạng thái phòng sang "đang thuê"')

img_placeholder(doc, 'Hình 3.6: Trang quản lý người thuê – Danh sách với tìm kiếm và lọc trạng thái')

img_placeholder(doc, 'Hình 3.7: Modal thêm mới người thuê với đầy đủ thông tin cá nhân')

h2(doc, '3.7. Module Quản Lý Hợp Đồng (admin/hop_dong.php)')

body(doc, 'Module hợp đồng cho phép Admin tạo và quản lý hợp đồng thuê phòng. '
     'Hệ thống tự động theo dõi và cảnh báo hợp đồng sắp hết hạn (30 ngày) '
     'trên Dashboard.')

body(doc, 'Trạng thái hợp đồng được quản lý tự động với 4 mức:')
bul(doc, 'Đang hiệu lực: Hợp đồng đang trong thời hạn, còn hơn 30 ngày')
bul(doc, 'Sắp hết hạn: Còn dưới 30 ngày → hiển thị cảnh báo màu cam trên Dashboard')
bul(doc, 'Đã hết hạn: Quá ngày kết thúc, tự động cập nhật trạng thái')
bul(doc, 'Đã thanh lý: Admin xác nhận kết thúc hợp đồng, khách đã trả phòng')

body(doc, 'Portal Khách Thuê hiển thị thanh tiến trình (progress bar) cho thấy '
     'tỷ lệ thời gian đã qua / tổng thời hạn hợp đồng, giúp người thuê biết '
     'còn bao lâu nữa hết hạn.')

img_placeholder(doc, 'Hình 3.8: Trang quản lý hợp đồng – Danh sách với thanh tiến trình thời hạn')

h2(doc, '3.8. Module Quản Lý Điện Nước (admin/dien_nuoc.php)')

body(doc, 'Module điện nước cho phép Admin nhập chỉ số đồng hồ điện và nước '
     'hàng tháng cho từng phòng. Hệ thống tự động tính số lượng tiêu thụ và '
     'số tiền theo công thức:')

body(doc, 'Tiền điện (đ) = (Chỉ số điện mới − Chỉ số điện cũ) × Đơn giá điện', bold=True, center=True, italic=True)
body(doc, 'Tiền nước (đ) = (Chỉ số nước mới − Chỉ số nước cũ) × Đơn giá nước', bold=True, center=True, italic=True)

body(doc, 'Validation đặc biệt: Hệ thống kiểm tra chỉ số mới phải lớn hơn hoặc bằng '
     'chỉ số cũ. CSDL có UNIQUE KEY trên (room_id, thang, nam) để tránh nhập '
     'trùng dữ liệu một phòng trong cùng một tháng.')

body(doc, 'Modal nhập liệu có tính năng tính tiền theo thời gian thực: khi Admin '
     'nhập chỉ số, JavaScript ngay lập tức hiển thị số kWh/m³ đã dùng và số tiền '
     'tương ứng, giúp kiểm tra trước khi lưu.')

img_placeholder(doc, 'Hình 3.9: Trang nhập chỉ số điện nước – Tính tiền tự động theo thời gian thực')

h2(doc, '3.9. Module Quản Lý Hóa Đơn (admin/hoa_don.php)')

body(doc, 'Module hóa đơn là trung tâm của hệ thống tài chính. Admin tạo hóa đơn '
     'tổng hợp hàng tháng gồm tất cả các khoản chi phí:')

body(doc, 'Tổng tiền = Tiền phòng + Tiền điện + Tiền nước + Tiền dịch vụ + Phí khác', bold=True, center=True, italic=True)

body(doc, 'Tính năng nổi bật:')
bul(doc, 'Tự động tính tổng tiền theo thời gian thực (oninput event) khi Admin nhập từng khoản')
bul(doc, 'Khi chọn phòng: tự động điền giá thuê và người thuê tương ứng')
bul(doc, 'Màu sắc trực quan: hóa đơn quá hạn màu đỏ, chưa thanh toán màu vàng, đã thanh toán màu trắng')
bul(doc, 'Lọc hóa đơn theo tháng, năm, trạng thái')
bul(doc, 'In hóa đơn: trang hoa_don_in.php chỉ hiển thị nội dung cần in, không có sidebar')
bul(doc, 'Thống kê tổng tiền chưa thu và đã thu ở đầu trang')

img_placeholder(doc, 'Hình 3.10: Trang danh sách hóa đơn với bộ lọc và thống kê tổng quan')

img_placeholder(doc, 'Hình 3.11: Modal tạo hóa đơn – Tổng tiền tự động cập nhật khi nhập liệu')

img_placeholder(doc, 'Hình 3.12: Giao diện in hóa đơn (Print-friendly) – Không có sidebar/header')

h2(doc, '3.10. Module Quản Lý Thanh Toán (admin/thanh_toan.php)')

body(doc, 'Module thanh toán ghi nhận các lần khách thuê nộp tiền. Khi ghi nhận '
     'thanh toán, hệ thống so sánh tổng tiền đã thu với tổng hóa đơn để tự động '
     'cập nhật trạng thái hóa đơn:')

code_block(doc,
    '// Tự động cập nhật trạng thái hóa đơn sau khi ghi nhận thanh toán\n'
    '$tongDaTT = $pdo->prepare("SELECT COALESCE(SUM(so_tien),0) FROM payments WHERE invoice_id=?");\n'
    '$tongDaTT->execute([$invoice_id]);\n'
    '$tongDaTT = $tongDaTT->fetchColumn();\n\n'
    '$inv = $pdo->prepare("SELECT tong_tien FROM invoices WHERE id=?");\n'
    '$inv->execute([$invoice_id]);\n'
    '$inv = $inv->fetch();\n\n'
    '// Nếu tổng tiền đã nộp >= tổng hóa đơn → Đã thanh toán\n'
    '$newTT = ($tongDaTT >= $inv["tong_tien"]) ? "da_thanh_toan" : "chua_thanh_toan";\n'
    '$pdo->prepare("UPDATE invoices SET trang_thai=? WHERE id=?")->execute([$newTT, $invoice_id]);'
)

body(doc, 'Phương thức thanh toán được hỗ trợ: Tiền mặt, Chuyển khoản ngân hàng, Thẻ ATM, Ví điện tử. '
     'Giao diện chia 2 cột: trái là form ghi nhận thanh toán (chọn hóa đơn → tự điền tổng tiền), '
     'phải là bảng lịch sử tất cả giao dịch.')

img_placeholder(doc, 'Hình 3.13: Trang thanh toán – Form ghi nhận (trái) và lịch sử giao dịch (phải)')

h2(doc, '3.11. Module Quản Lý Sự Cố (admin/su_co.php + user/su_co.php)')

body(doc, 'Module sự cố tạo kênh giao tiếp hai chiều giữa khách thuê và chủ trọ. '
     'Quy trình xử lý sự cố:')

make_table(doc,
    ['Bước', 'Người Thực Hiện', 'Hành Động', 'Trạng Thái'],
    [
        ['1', 'Khách thuê', 'Điền form báo sự cố (tiêu đề, mô tả, mức độ)', 'Mới gửi'],
        ['2', 'Hệ thống', 'Tự sinh mã sự cố, lưu CSDL, hiển thị trên Admin', 'Mới gửi'],
        ['3', 'Admin', 'Xem sự cố, xác nhận tiếp nhận', 'Đã tiếp nhận'],
        ['4', 'Admin', 'Cử người sửa chữa, cập nhật trạng thái', 'Đang xử lý'],
        ['5', 'Admin', 'Hoàn tất sửa chữa, ghi chú kết quả', 'Đã hoàn thành'],
        ['6', 'Khách thuê', 'Theo dõi trạng thái và ghi chú từ portal', '—'],
    ],
    'Bảng 3.2: Quy trình xử lý sự cố trong hệ thống'
)

body(doc, 'Mức độ sự cố được phân loại: Khẩn cấp (màu đỏ), Cao (màu cam), Bình thường (màu vàng), '
     'Thấp (màu xanh). Admin có thể lọc theo mức độ và trạng thái để ưu tiên xử lý.')

img_placeholder(doc, 'Hình 3.14: Form báo sự cố của Khách Thuê (user/su_co.php)')

img_placeholder(doc, 'Hình 3.15: Trang Admin quản lý sự cố – Cập nhật trạng thái và ghi chú xử lý')

h2(doc, '3.12. Module Thống Kê Báo Cáo (admin/thong_ke.php)')

body(doc, 'Module thống kê cung cấp góc nhìn tổng quan về tình hình hoạt động '
     'của khu trọ theo năm. Sử dụng Chart.js để vẽ biểu đồ trực quan, '
     'dữ liệu được tính toán và gửi từ PHP dưới dạng JSON:')

code_block(doc,
    '// PHP tính doanh thu 12 tháng, gửi sang JS\n'
    '$doanhThu12Thang = [];\n'
    'for ($m = 1; $m <= 12; $m++) {\n'
    '    $s = $pdo->prepare("SELECT COALESCE(SUM(so_tien),0) FROM payments\n'
    '                        WHERE MONTH(ngay_thanh_toan)=? AND YEAR(ngay_thanh_toan)=?");\n'
    '    $s->execute([$m, $selectedYear]);\n'
    '    $doanhThu12Thang[] = (float)$s->fetchColumn();\n'
    '}\n'
    '$chartData = json_encode($doanhThu12Thang);\n\n'
    '// JavaScript nhận dữ liệu từ PHP\n'
    'new Chart(ctx, { type: "bar",\n'
    '    data: { labels: ["T1","T2",...,"T12"],\n'
    '            datasets: [{ data: <?php echo $chartData; ?> }] }\n'
    '});'
)

body(doc, 'Các báo cáo được cung cấp:')
bul(doc, 'Biểu đồ cột: Doanh thu 12 tháng trong năm (có thể chọn năm khác)')
bul(doc, 'Biểu đồ đường: So sánh tiền điện và tiền nước theo từng tháng trong năm')
bul(doc, 'Bảng top 5 phòng có doanh thu cao nhất trong năm')
bul(doc, '4 thẻ tổng quan: Tổng doanh thu năm, tổng phòng, người đang thuê, hóa đơn chưa thu')

img_placeholder(doc, 'Hình 3.16: Trang thống kê – Biểu đồ doanh thu 12 tháng và so sánh điện/nước')

h2(doc, '3.13. Portal Khách Thuê')

body(doc, 'Portal Khách Thuê (thư mục user/) cung cấp giao diện riêng biệt với sidebar '
     'và menu khác Admin. Khách thuê chỉ xem được thông tin của chính mình, '
     'không thể truy cập dữ liệu người khác (kiểm tra tenant_id trong mọi truy vấn).')

make_table(doc,
    ['Trang', 'File', 'Chức Năng Chính'],
    [
        ['Dashboard', 'dashboard.php', 'Thông tin phòng, hóa đơn chưa TT, điện nước tháng hiện tại, sự cố'],
        ['Phòng Của Tôi', 'phong.php', 'Chi tiết phòng: mã, loại, diện tích, giá thuê, thông tin chủ trọ'],
        ['Hợp Đồng', 'hop_dong.php', 'Xem hợp đồng với thanh tiến trình thời hạn và điều khoản'],
        ['Điện Nước', 'dien_nuoc.php', 'Lịch sử chỉ số và tiền điện nước từng tháng theo bảng'],
        ['Hóa Đơn', 'hoa_don.php', 'Danh sách hóa đơn, cảnh báo đỏ cho hóa đơn quá hạn'],
        ['Lịch Sử TT', 'thanh_toan.php', 'Xem tất cả lần đã thanh toán với số tiền và phương thức'],
        ['Báo Sự Cố', 'su_co.php', 'Gửi yêu cầu sửa chữa và theo dõi trạng thái xử lý'],
        ['Tài Khoản', 'tai_khoan.php', 'Cập nhật thông tin cá nhân và đổi mật khẩu'],
    ],
    'Bảng 3.3: Các trang trong Portal Khách Thuê'
)

img_placeholder(doc, 'Hình 3.17: Dashboard Khách Thuê – Thông tin phòng, hóa đơn chưa TT, điện nước')

img_placeholder(doc, 'Hình 3.18: Khách Thuê – Trang hóa đơn với cảnh báo quá hạn màu đỏ')

img_placeholder(doc, 'Hình 3.19: Khách Thuê – Form báo sự cố và danh sách sự cố đã gửi')

h2(doc, '3.14. Giao Diện Và Trải Nghiệm Người Dùng')

h3(doc, '3.14.1. Layout 2 Cột Với Sidebar Co Rút')
body(doc, 'Toàn bộ trang quản trị sử dụng layout 2 cột: sidebar bên trái (260px) '
     'và nội dung chính bên phải. Sidebar có thể co rút về 70px khi click nút '
     'hamburger, giúp tăng không gian làm việc trên màn hình nhỏ:')

code_block(doc,
    '/* assets/css/style.css */\n'
    '.sidebar { width: 260px; transition: width 0.3s ease; }\n'
    '.sidebar.collapsed { width: 70px; }\n'
    '.sidebar.collapsed .sidebar-text { display: none; }\n'
    '.main-content { margin-left: 260px; transition: margin-left 0.3s ease; }\n'
    '.main-content.expanded { margin-left: 70px; }\n\n'
    '/* assets/js/script.js */\n'
    'function toggleSidebar() {\n'
    '    document.getElementById("sidebar").classList.toggle("collapsed");\n'
    '    document.getElementById("mainContent").classList.toggle("expanded");\n'
    '}'
)

h3(doc, '3.14.2. Màu Sắc Và Trạng Thái')
body(doc, 'Hệ thống sử dụng màu sắc nhất quán để phân biệt trạng thái:')
make_table(doc,
    ['Trạng Thái', 'Màu Hiển Thị', 'Ý Nghĩa'],
    [
        ['dang_thue / da_thanh_toan', 'Xanh lá (success)', 'Đang hoạt động bình thường'],
        ['trong / hieu_luc', 'Xanh dương (primary)', 'Sẵn sàng / Hiệu lực'],
        ['chua_thanh_toan / moi_gui', 'Vàng (warning)', 'Cần chú ý'],
        ['qua_han / khoa', 'Đỏ (danger)', 'Cần xử lý khẩn'],
        ['dang_sua_chua / dang_xu_ly', 'Cam (warning dark)', 'Đang tiến hành'],
        ['da_thanh_ly / hoan_thanh', 'Xám (secondary)', 'Đã kết thúc'],
    ],
    'Bảng 3.4: Quy ước màu sắc trạng thái trong hệ thống'
)

# ═══════════════════════════════════════════════════════════════════════════════
# CHƯƠNG IV
# ═══════════════════════════════════════════════════════════════════════════════
pb(doc)
h1(doc, 'CHƯƠNG IV: KẾT QUẢ VÀ ĐÁNH GIÁ')

h2(doc, '4.1. Kết Quả Đạt Được')

h3(doc, '4.1.1. Về Mặt Kỹ Thuật')
body(doc, 'Sau quá trình nghiên cứu và phát triển, hệ thống đã đạt được các kết quả kỹ thuật:')
bul(doc, 'Xây dựng thành công hệ thống với hơn 40 file PHP, CSS, JavaScript theo cấu trúc module rõ ràng')
bul(doc, 'Kết nối CSDL MySQL an toàn bằng PDO với Prepared Statements, ngăn hoàn toàn SQL Injection')
bul(doc, 'Mã hóa mật khẩu bằng bcrypt (cost=10) – thuật toán bảo mật cao nhất cho web hiện nay')
bul(doc, 'Phân quyền chặt chẽ: Admin và Khách Thuê không thể truy cập tài nguyên của nhau')
bul(doc, 'Giao diện responsive hoạt động tốt trên Desktop (1920px), Laptop (1366px), Tablet (768px) và Mobile (375px)')
bul(doc, 'Tích hợp Chart.js v4.4 vẽ biểu đồ doanh thu (cột) và điện nước (đường) trực quan')
bul(doc, 'Sidebar co rút/mở rộng với animation CSS transition mượt mà')
bul(doc, 'Đồng hồ thời gian thực trên topbar (cập nhật mỗi giây bằng setInterval)')
bul(doc, 'Flash message hiển thị thông báo thành công/lỗi sau mỗi thao tác CRUD')

h3(doc, '4.1.2. Bảng Tổng Kết Các Chức Năng')
make_table(doc,
    ['STT', 'Chức Năng', 'Trang PHP', 'Trạng Thái', 'Ghi Chú'],
    [
        ['1', 'Đăng nhập / Phân quyền', 'login.php', 'Hoàn thành ✓', 'Session + bcrypt'],
        ['2', 'Dashboard Admin', 'admin/dashboard.php', 'Hoàn thành ✓', 'Chart.js, stat cards'],
        ['3', 'Quản lý phòng', 'admin/phong.php', 'Hoàn thành ✓', 'CRUD + modal + lọc'],
        ['4', 'Quản lý người thuê', 'admin/nguoi_thue.php', 'Hoàn thành ✓', 'CRUD + tìm kiếm'],
        ['5', 'Quản lý hợp đồng', 'admin/hop_dong.php', 'Hoàn thành ✓', 'Cảnh báo hết hạn'],
        ['6', 'Quản lý điện nước', 'admin/dien_nuoc.php', 'Hoàn thành ✓', 'Tự tính tiền real-time'],
        ['7', 'Quản lý dịch vụ', 'admin/dich_vu.php', 'Hoàn thành ✓', 'CRUD danh mục dịch vụ'],
        ['8', 'Quản lý hóa đơn', 'admin/hoa_don.php', 'Hoàn thành ✓', 'In hóa đơn, tổng tự động'],
        ['9', 'Quản lý thanh toán', 'admin/thanh_toan.php', 'Hoàn thành ✓', 'Auto cập nhật TT hóa đơn'],
        ['10', 'Quản lý sự cố', 'admin/su_co.php', 'Hoàn thành ✓', '2 chiều admin-khách'],
        ['11', 'Thống kê báo cáo', 'admin/thong_ke.php', 'Hoàn thành ✓', 'Biểu đồ cột + đường'],
        ['12', 'Quản lý tài khoản', 'admin/tai_khoan.php', 'Hoàn thành ✓', 'Khóa/mở, đổi mật khẩu'],
        ['13', 'Dashboard Khách Thuê', 'user/dashboard.php', 'Hoàn thành ✓', 'Tổng quan thông tin'],
        ['14', 'Xem phòng/hợp đồng', 'user/phong.php + hop_dong.php', 'Hoàn thành ✓', 'Progress bar hợp đồng'],
        ['15', 'Xem điện nước/hóa đơn', 'user/dien_nuoc.php + hoa_don.php', 'Hoàn thành ✓', 'Cảnh báo quá hạn'],
        ['16', 'Báo sự cố', 'user/su_co.php', 'Hoàn thành ✓', 'Theo dõi trạng thái'],
    ],
    'Bảng 4.1: Kết quả hoàn thành toàn bộ chức năng hệ thống'
)

h2(doc, '4.2. Kiểm Thử Hệ Thống')

h3(doc, '4.2.1. Kiểm Thử Chức Năng Đăng Nhập')
make_table(doc,
    ['STT', 'Test Case', 'Dữ Liệu Đầu Vào', 'Kết Quả Mong Đợi', 'Kết Quả Thực Tế'],
    [
        ['1', 'Đăng nhập Admin đúng', 'admin / Admin@123', 'Vào admin/dashboard.php', 'Đúng ✓'],
        ['2', 'Đăng nhập Khách Thuê đúng', 'nguyen.van.a / User@123', 'Vào user/dashboard.php', 'Đúng ✓'],
        ['3', 'Sai mật khẩu', 'admin / saimatkhau', 'Thông báo lỗi', 'Đúng ✓'],
        ['4', 'Tài khoản không tồn tại', 'khongco / 123', 'Thông báo lỗi', 'Đúng ✓'],
        ['5', 'Bỏ trống username', '(trống) / Admin@123', 'Thông báo validate', 'Đúng ✓'],
        ['6', 'Khách thuê vào URL admin', '/admin/dashboard.php', 'Redirect về user/', 'Đúng ✓'],
        ['7', 'Chưa đăng nhập vào trang quản trị', '/admin/phong.php', 'Redirect về login.php', 'Đúng ✓'],
    ],
    'Bảng 4.2: Test case kiểm thử chức năng đăng nhập và phân quyền'
)

h3(doc, '4.2.2. Kiểm Thử Quản Lý Phòng')
make_table(doc,
    ['STT', 'Test Case', 'Dữ Liệu Đầu Vào', 'Kết Quả Mong Đợi', 'Kết Quả Thực Tế'],
    [
        ['1', 'Thêm phòng mới hợp lệ', 'Mã P301, Giá 2.5M', 'Thêm thành công, hiển thị flash', 'Đúng ✓'],
        ['2', 'Thêm phòng mã trùng', 'Mã P101 (đã có)', 'Thông báo lỗi mã đã tồn tại', 'Đúng ✓'],
        ['3', 'Sửa giá phòng', 'P101, giá mới 3M', 'Cập nhật thành công', 'Đúng ✓'],
        ['4', 'Xóa phòng không có người', 'P301 (trống)', 'Xóa thành công', 'Đúng ✓'],
        ['5', 'Xóa phòng có người thuê', 'P101 (đang thuê)', 'Thông báo không thể xóa', 'Đúng ✓'],
        ['6', 'Tìm kiếm phòng', 'Từ khóa "P10"', 'Hiển thị P101, P102...', 'Đúng ✓'],
        ['7', 'Lọc phòng trống', 'trang_thai = trong', 'Chỉ hiện phòng trống', 'Đúng ✓'],
    ],
    'Bảng 4.3: Test case kiểm thử quản lý phòng trọ'
)

h2(doc, '4.3. Hạn Chế Của Đề Tài')
body(doc, 'Bên cạnh những kết quả đạt được, đề tài vẫn còn một số hạn chế:')
bul(doc, 'Thanh toán trực tuyến: Chưa tích hợp VNPay/Momo; Admin phải ghi nhận thanh toán thủ công sau khi khách chuyển khoản.')
bul(doc, 'Thông báo tự động: Chưa gửi Email/SMS khi có hóa đơn mới, hợp đồng sắp hết hạn.')
bul(doc, 'Upload hình ảnh sự cố: Khách thuê chưa thể đính kèm ảnh khi báo sự cố.')
bul(doc, 'Xuất báo cáo file: Chưa xuất Excel/PDF từ trang thống kê.')
bul(doc, 'Chưa hỗ trợ đa khu nhà trọ: Hệ thống chỉ quản lý một khu trọ duy nhất.')
bul(doc, 'AJAX nâng cao: Lọc/tìm kiếm cần tải lại trang thay vì cập nhật AJAX không reload.')

h2(doc, '4.4. Hướng Phát Triển')
body(doc, 'Với nền tảng đã xây dựng, hệ thống có thể phát triển thêm:')
bul(doc, 'Tích hợp thanh toán: Kết nối VNPay hoặc Momo API, khách thuê thanh toán trực tuyến, hóa đơn tự cập nhật.')
bul(doc, 'Thông báo đa kênh: Gửi email qua PHPMailer/SMTP và SMS qua ESMS.vn khi có sự kiện quan trọng.')
bul(doc, 'Ứng dụng Mobile: API RESTful PHP + ứng dụng Flutter cho iOS/Android.')
bul(doc, 'Xuất báo cáo: Tích hợp TCPDF (xuất PDF) và PhpSpreadsheet (xuất Excel).')
bul(doc, 'Quản lý đa cơ sở: Một Admin quản lý nhiều khu nhà trọ khác nhau.')
bul(doc, 'Dashboard nâng cao: Dự báo doanh thu tháng sau dựa trên lịch sử bằng thuật toán đơn giản.')

h2(doc, '4.5. Kết Luận')
body(doc, 'Đề tài "Website Quản Lý Phòng Trọ" đã được hoàn thiện đúng mục tiêu đề ra. '
     'Hệ thống giải quyết bài toán thực tế của chủ nhà trọ trong việc số hóa quy trình '
     'quản lý, tiết kiệm thời gian, giảm sai sót và nâng cao hiệu quả.')

body(doc, 'Qua quá trình thực hiện đề tài, sinh viên đã củng cố và vận dụng được:')
bul(doc, 'Kiến thức lập trình web: PHP 8+, HTML5, CSS3, JavaScript ES6, Bootstrap 5')
bul(doc, 'Thiết kế CSDL: MySQL với 10 bảng, đầy đủ FOREIGN KEY, INDEX và dữ liệu mẫu')
bul(doc, 'Bảo mật web: Session management, mã hóa bcrypt, SQL Injection prevention bằng PDO')
bul(doc, 'Thiết kế UI/UX: Responsive design, giao diện hiện đại, trải nghiệm người dùng tốt')
bul(doc, 'Tích hợp thư viện: Chart.js, Bootstrap 5, Font Awesome 6')
bul(doc, 'Quy trình phát triển: Phân tích → Thiết kế CSDL → Cài đặt → Kiểm thử')

body(doc, 'Hệ thống đáp ứng đầy đủ yêu cầu của một website quản lý phòng trọ hoàn chỉnh '
     'và là nền tảng tốt để tiếp tục phát triển, mở rộng trong tương lai với các '
     'tính năng thanh toán trực tuyến, ứng dụng mobile và thông báo tự động.')

# ─── PHỤ LỤC ──────────────────────────────────────────────────────────────────
pb(doc)
h1(doc, 'PHỤ LỤC')

h2(doc, 'Phụ Lục A: Hướng Dẫn Cài Đặt Và Chạy Hệ Thống')
body(doc, 'Hệ thống chạy trên môi trường XAMPP. Các bước cài đặt:')

body(doc, 'Bước 1 – Chuẩn bị môi trường', bold=True)
bul(doc, 'Tải XAMPP từ https://www.apachefriends.org (phiên bản 8.2+)')
bul(doc, 'Cài đặt XAMPP, khởi động XAMPP Control Panel')
bul(doc, 'Click Start cho Apache và MySQL')

body(doc, 'Bước 2 – Copy mã nguồn', bold=True)
bul(doc, 'Copy thư mục QuanLyPhongTro vào: C:\\xampp\\htdocs\\QuanLyPhongTro\\')

body(doc, 'Bước 3 – Tạo cơ sở dữ liệu', bold=True)
bul(doc, 'Mở trình duyệt → http://localhost/phpmyadmin')
bul(doc, 'Tạo database mới: quan_ly_phong_tro (charset: utf8mb4)')
bul(doc, 'Tab SQL hoặc Import → chọn file database.sql → Execute')

body(doc, 'Bước 4 – Truy cập hệ thống', bold=True)
bul(doc, 'Admin: http://localhost/QuanLyPhongTro → Đăng nhập: admin / Admin@123')
bul(doc, 'Khách thuê: Đăng nhập: nguyen.van.a / User@123')

h2(doc, 'Phụ Lục B: Danh Sách Tài Khoản Demo')
make_table(doc,
    ['Username', 'Password', 'Vai Trò', 'Thông Tin'],
    [
        ['admin', 'Admin@123', 'Admin', 'Quản trị viên hệ thống'],
        ['nguyen.van.a', 'User@123', 'Khách Thuê', 'Nguyễn Văn A – Phòng P101'],
        ['tran.thi.b', 'User@123', 'Khách Thuê', 'Trần Thị B – Phòng P102'],
        ['le.van.c', 'User@123', 'Khách Thuê', 'Lê Văn C – Phòng P201'],
    ],
    'Bảng PL.1: Tài khoản demo trong hệ thống'
)

h2(doc, 'Phụ Lục C: Công Nghệ Và Thư Viện Sử Dụng')
make_table(doc,
    ['Công Nghệ', 'Phiên Bản', 'Mục Đích'],
    [
        ['PHP', '8.0+', 'Ngôn ngữ lập trình backend chính'],
        ['MySQL', '8.0', 'Hệ quản trị cơ sở dữ liệu quan hệ'],
        ['Apache', '2.4', 'Web server (trong XAMPP)'],
        ['Bootstrap', '5.3.0', 'CSS Framework responsive'],
        ['Font Awesome', '6.4.0', 'Bộ icon vector đa dạng'],
        ['Chart.js', '4.4.0', 'Thư viện vẽ biểu đồ JavaScript'],
        ['jQuery', '3.7.0', 'Thư viện JavaScript hỗ trợ DOM'],
        ['PDO', 'Built-in PHP', 'Kết nối và truy vấn CSDL an toàn'],
        ['password_hash()', 'Built-in PHP', 'Mã hóa mật khẩu bcrypt'],
    ],
    'Bảng PL.2: Công nghệ và thư viện sử dụng'
)

# ─── TÀI LIỆU THAM KHẢO ──────────────────────────────────────────────────────
pb(doc)
h1(doc, 'TÀI LIỆU THAM KHẢO')
refs = [
    '[1]  PHP Group. (2024). PHP Manual. https://www.php.net/manual/en/',
    '[2]  Oracle Corporation. (2024). MySQL 8.0 Reference Manual. https://dev.mysql.com/doc/',
    '[3]  Bootstrap Team. (2023). Bootstrap 5.3 Documentation. https://getbootstrap.com/docs/5.3/',
    '[4]  Font Awesome. (2023). Font Awesome 6 Documentation. https://fontawesome.com/',
    '[5]  Chart.js Team. (2024). Chart.js v4 Documentation. https://www.chartjs.org/docs/',
    '[6]  OWASP. (2024). SQL Injection Prevention Cheat Sheet. https://cheatsheetseries.owasp.org/',
    '[7]  OWASP. (2024). Session Management Cheat Sheet. https://cheatsheetseries.owasp.org/',
    '[8]  OWASP. (2024). Password Storage Cheat Sheet. https://cheatsheetseries.owasp.org/',
    '[9]  Mozilla MDN. (2024). JavaScript Reference. https://developer.mozilla.org/en-US/docs/Web/JavaScript/',
    '[10] W3Schools. (2024). PHP Tutorial. https://www.w3schools.com/php/',
    '[11] W3Schools. (2024). MySQL Tutorial. https://www.w3schools.com/mysql/',
    '[12] Bootstrap. (2023). Bootstrap 5 Components – Modal. https://getbootstrap.com/docs/5.3/components/modal/',
    '[13] php.net. (2024). PDO – PHP Data Objects. https://www.php.net/manual/en/book.pdo.php',
    '[14] php.net. (2024). password_hash() Function. https://www.php.net/manual/en/function.password-hash.php',
]

for ref in refs:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.space_after = Pt(5)
    run = p.add_run(ref)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)

# ─── Save ─────────────────────────────────────────────────────────────────────
output = r'c:\xampp\htdocs\QuanLyPhongTro\BaoCao_QuanLyPhongTro.docx'
doc.save(output)
print(f"\n✅ Đã lưu báo cáo: {output}")
print(f"   Tổng đoạn văn: {len(doc.paragraphs)}")
print(f"   Tổng bảng: {len(doc.tables)}")
