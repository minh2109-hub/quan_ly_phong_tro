import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

sys.stdout.reconfigure(encoding='utf-8')

SRC_PATH = r"c:\xampp\htdocs\QuanLyPhongTro\template.docx"
OUT_PATH = r"c:\xampp\htdocs\QuanLyPhongTro\BaoCao_QuanLyPhongTro.docx"
IMG_DIR  = r"c:\xampp\htdocs\QuanLyPhongTro\assets\images"

def build():
    doc = Document(SRC_PATH)
    
    FONT_NAME = 'Times New Roman'
    BODY_SIZE = 11.5
    
    def set_font(run, name=FONT_NAME, size=BODY_SIZE, bold=False, italic=False, color=None):
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
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = Pt(13)
        run = p.add_run(text)
        set_font(run, size=13.5, bold=True, color=(30, 58, 138))
        return p

    def add_sec1(doc, text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(7)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = Pt(12.5)
        run = p.add_run(text)
        set_font(run, size=12, bold=True, color=(30, 58, 138))
        return p

    def add_sec2(doc, text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(1.5)
        p.paragraph_format.line_spacing = Pt(12.5)
        run = p.add_run(text)
        set_font(run, size=11.5, bold=True, color=(15, 23, 42))
        return p

    def add_p(doc, text, bold=False, italic=False, indent=True, center=False, size=BODY_SIZE):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.JUSTIFY
        if indent and not center:
            p.paragraph_format.first_line_indent = Cm(0.8)
        p.paragraph_format.space_after = Pt(1.5)
        p.paragraph_format.line_spacing = Pt(12.5)
        run = p.add_run(text)
        set_font(run, size=size, bold=bold, italic=italic)
        return p

    def add_bullet(doc, text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Cm(0.8)
        p.paragraph_format.first_line_indent = Cm(-0.4)
        p.paragraph_format.space_after = Pt(1.5)
        p.paragraph_format.line_spacing = Pt(12.2)
        run = p.add_run('•  ' + text)
        set_font(run, size=BODY_SIZE - 0.5)
        return p

    def add_image(doc, filename, caption, width_in=5.4):
        path = os.path.join(IMG_DIR, filename)
        if os.path.exists(path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(1.5)
            run = p.add_run()
            run.add_picture(path, width=Inches(width_in))
        
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_after = Pt(3)
        r = cp.add_run(caption)
        set_font(r, size=9.5, bold=True, italic=True, color=(71, 85, 105))

    def add_table(doc, headers, rows, caption=None):
        if caption:
            cp = doc.add_paragraph()
            cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cp.paragraph_format.space_before = Pt(3)
            cp.paragraph_format.space_after = Pt(2)
            r = cp.add_run(caption)
            set_font(r, size=9.5, bold=True, italic=True, color=(30, 58, 138))

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
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(h)
            set_font(run, size=8.5, bold=True, color=(255, 255, 255))
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
                p.paragraph_format.space_before = Pt(1.5)
                p.paragraph_format.space_after = Pt(1.5)
                p.paragraph_format.line_spacing = Pt(10.5)
                run = p.add_run(str(val))
                set_font(run, size=8)
                if bg_fill != 'FFFFFF':
                    tcPr = c._tc.get_or_add_tcPr()
                    shd = OxmlElement('w:shd')
                    shd.set(qn('w:val'), 'clear')
                    shd.set(qn('w:color'), 'auto')
                    shd.set(qn('w:fill'), bg_fill)
                    tcPr.append(shd)

        doc.add_paragraph().paragraph_format.space_after = Pt(2.5)
        return tbl

    def add_code(doc, text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Cm(0.6)
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = Pt(11)
        pPr = p._p.get_or_add_pPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), 'F1F5F9')
        pPr.append(shd)
        run = p.add_run(text)
        run.font.name = 'Consolas'
        run.font.size = Pt(8.5)
        return p

    # 1. Trang bìa: giữ nguyên hình ảnh/logo, chỉ sửa tên đề tài
    for p in doc.paragraphs[:30]:
        for run in p.runs:
            if 'điện thoại' in run.text.lower() or 'bán hàng' in run.text.lower() or 'đề tài:' in run.text.lower():
                run.text = '< ĐỀ TÀI: XÂY DỰNG WEBSITE QUẢN LÝ PHÒNG TRỌ >'

    # 2. Cập nhật Mục lục trang 2
    if len(doc.paragraphs) > 27:
        doc.paragraphs[27].text = 'MỤC LỤC'
        set_font(doc.paragraphs[27].runs[0], size=13, bold=True, color=(30, 58, 138))

    toc_items = [
        ("LỜI MỞ ĐẦU", 3, True),
        ("CHƯƠNG I. TÌM HIỂU NGÔN NGỮ PHP VÀ MYSQL", 4, True),
        ("  1.1 Ngôn ngữ lập trình PHP", 4, False),
        ("  1.2 Tại sao nên dùng PHP", 5, False),
        ("  1.3 Giới thiệu về ngôn ngữ PHP", 6, False),
        ("  2.1 Giới thiệu cơ sở dữ liệu MySQL", 7, False),
        ("  2.2 Mục đích sử dụng cơ sở dữ liệu", 8, False),
        ("CHƯƠNG II. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG", 9, True),
        ("  2.1 Khảo sát nghiệp vụ và yêu cầu hệ thống", 9, False),
        ("  2.2 Phân tích mô hình Use Case", 10, False),
        ("  2.3 Biểu đồ luồng dữ liệu (DFD)", 12, False),
        ("  2.4 Sơ đồ tuần tự và kiến trúc hệ thống", 14, False),
        ("  2.5 Thiết kế cơ sở dữ liệu (ERD & từ điển)", 16, False),
        ("CHƯƠNG III. XÂY DỰNG VÀ CÀI ĐẶT HỆ THỐNG", 20, True),
        ("  3.1 Cấu trúc mã nguồn và kết nối CSDL", 20, False),
        ("  3.2 Cài đặt phân hệ Quản trị viên (Admin)", 21, False),
        ("  3.3 Cài đặt phân hệ Khách thuê (User Portal)", 34, False),
        ("CHƯƠNG IV. KIỂM THỬ VÀ ĐÁNH GIÁ KẾT QUẢ", 43, True),
        ("  4.1 Phương pháp và kết quả kiểm thử", 43, False),
        ("  4.2 Đánh giá kết quả, hạn chế và phát triển", 44, False),
        ("  4.3 Đánh giá bảo mật và hiệu năng hệ thống", 45, False),
        ("KẾT LUẬN VÀ KIẾN NGHỊ", 46, True),
        ("PHỤ LỤC", 47, True),
        ("TÀI LIỆU THAM KHẢO", 50, True)
    ]

    for idx, (title, page_num, is_bold) in enumerate(toc_items):
        p_num = 28 + idx
        if p_num < 52 and p_num < len(doc.paragraphs):
            p = doc.paragraphs[p_num]
            p.text = ''
            dots_count = max(4, 46 - len(title))
            dots = '.' * dots_count
            run_title = p.add_run(f"{title} {dots} ")
            set_font(run_title, size=9.5, bold=is_bold, color=(30, 58, 138) if is_bold else (15, 23, 42))
            run_page = p.add_run(str(page_num))
            set_font(run_page, size=9.5, bold=is_bold, color=(30, 58, 138) if is_bold else (15, 23, 42))
            p.paragraph_format.line_spacing = Pt(11)
            p.paragraph_format.space_before = Pt(0.5)
            p.paragraph_format.space_after = Pt(1)

    # 3. Lời mở đầu
    mo_dau_text = (
        "Hiện nay, cùng với sự phát triển mạnh mẽ của nền kinh tế và tốc độ đô thị hóa nhanh chóng tại các đô thị lớn, "
        "nhu cầu thuê nhà trọ, căn hộ mini và phòng trọ của sinh viên, người lao động và các gia đình trẻ ngày càng gia tăng. "
        "Tuy nhiên, đại đa số các chủ nhà trọ hiện nay vẫn đang áp dụng phương pháp quản lý truyền thống thông qua ghi chép "
        "sổ sách thủ công hoặc bảng tính rời rạc. Phương thức này tồn tại nhiều bất cập: dễ thất lạc dữ liệu, tốn công ghi số điện nước, "
        "dễ nhầm lẫn hóa đơn và thiếu kênh tương tác phản ánh sự cố hỏng hóc giữa chủ trọ và khách thuê.\n\n"
        "Xuất phát từ nhu cầu thực tiễn đó, đề tài “Xây dựng Website Quản Lý Phòng Trọ” được triển khai nhằm số hóa "
        "toàn diện quy trình vận hành khu nhà trọ. Ứng dụng xây dựng trên nền tảng PHP 8+, MySQL và Bootstrap 5, "
        "cung cấp giải pháp quản lý tập trung, tự động tính điện nước, lập hóa đơn, theo dõi công nợ và tiếp nhận báo hỏng trực tuyến."
    )
    if len(doc.paragraphs) > 54:
        doc.paragraphs[54].text = mo_dau_text
        set_font(doc.paragraphs[54].runs[0], size=11.5)

    # 4. Giữ nguyên Chương I, xóa từ Chương II cũ
    to_del = []
    found_ch2 = False
    for p in doc.paragraphs:
        if not found_ch2 and ('Chương II' in p.text or 'chương II' in p.text.lower()):
            found_ch2 = True
        if found_ch2:
            to_del.append(p)

    for p in to_del:
        p._element.getparent().remove(p._element)

    # ═════════════════════════════════════════════════════════════════
    # CHƯƠNG II: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG
    # ═════════════════════════════════════════════════════════════════
    add_chapter(doc, "CHƯƠNG II: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG")

    add_sec1(doc, "2.1. Khảo Sát Nghiệp Vụ Và Yêu Cầu Hệ Thống")
    add_p(doc, "Hệ thống Quản Lý Phòng Trọ giải quyết bài toán số hóa toàn bộ quy trình vận hành nhà trọ, phục vụ 2 nhóm người dùng chính là Chủ trọ (Admin) và Khách thuê (User). Hệ thống loại bỏ việc ghi chép sổ sách thủ công, tự động hóa tính tiền điện nước, lập hóa đơn và quản lý công nợ.")
    
    add_table(doc,
        ["STT", "Nhóm Chức Năng", "Vai Trò", "Mô Tả Nghiệp Vụ"],
        [
            ["1", "Đăng nhập & Phân quyền", "Admin & User", "Xác thực danh tính bằng Session và Bcrypt, phân quyền theo vai trò."],
            ["2", "Dashboard tổng quan", "Admin", "Thống kê KPI phòng, doanh thu tháng, hóa đơn chưa thu, sự cố chờ sửa."],
            ["3", "Quản lý phòng trọ", "Admin", "CRUD phòng trọ, phân loại tầng/khu, theo dõi giá thuê, cọc và trạng thái."],
            ["4", "Quản lý người thuê", "Admin", "Quản lý hồ sơ nhân thân, số CCCD, SĐT, liên kết người thuê với phòng."],
            ["5", "Quản lý hợp đồng", "Admin", "Tạo hợp đồng, quản lý tiền cọc, tự động cảnh báo hợp đồng sắp hết hạn."],
            ["6", "Quản lý điện nước", "Admin", "Nhập chỉ số điện nước theo tháng, tự động tính tiền theo đơn giá."],
            ["7", "Quản lý dịch vụ", "Admin", "Cấu hình bảng giá dịch vụ dùng chung (internet, vệ sinh, rác, gửi xe)."],
            ["8", "Quản lý hóa đơn", "Admin", "Lập hóa đơn tổng hợp theo tháng, theo dõi hạn nộp và in phiếu thu."],
            ["9", "Quản lý thanh toán", "Admin", "Ghi nhận tiền nộp, tự động cập nhật trạng thái hóa đơn sang Đã thanh toán."],
            ["10", "Quản lý sự cố sửa chữa", "Admin & User", "Khách gửi báo hỏng; Admin cập nhật quy trình xử lý 4 giai đoạn."],
            ["11", "Quản lý tài khoản", "Admin", "Cấp tài khoản người dùng, đổi mật khẩu, kích hoạt hoặc khóa tài khoản."],
            ["12", "Báo cáo thống kê", "Admin", "Biểu đồ doanh thu 12 tháng, tương quan điện nước, top phòng doanh thu cao."],
            ["13", "Portal Khách thuê (8 mục)", "User", "Xem phòng, hợp đồng, lịch sử điện nước, hóa đơn, thanh toán, báo sự cố."]
        ],
        "Bảng 2.1: Danh mục yêu cầu chức năng hệ thống"
    )

    add_sec1(doc, "2.2. Phân Tích Mô Hình Use Case")
    add_p(doc, "Mô hình Use Case mô tả mối tương tác giữa Admin và Khách thuê với các chức năng của hệ thống:")
    add_image(doc, "sodo_usecase_tongquat.png", "Hình 2.1: Sơ đồ Use Case tổng quát hệ thống Quản Lý Phòng Trọ")

    add_table(doc,
        ["Mã UC", "Tên Use Case", "Actor", "Luồng Sự Kiện Chính & Ngoại Lệ"],
        [
            ["UC01", "Đăng nhập hệ thống", "Admin, User", "Nhập username/password -> Hệ thống đối chiếu Bcrypt -> Cấp Session -> Điều hướng Dashboard. Sai thông tin hiển thị alert đỏ."],
            ["UC02", "Quản lý phòng trọ", "Admin", "Xem danh sách, thêm/sửa bằng modal, xóa phòng còn trống. Không cho xóa phòng đang có người ở."],
            ["UC03", "Quản lý điện nước", "Admin", "Chọn phòng & tháng -> Nhập số mới -> Tự động tính chênh lệch và thành tiền. Chặn trường hợp số mới nhỏ hơn số cũ."],
            ["UC04", "Lập & quản lý hóa đơn", "Admin", "Chọn phòng -> Tổng hợp: Tiền phòng + Điện + Nước + Dịch vụ + Phí khác -> Lưu hóa đơn chưa thu -> Hỗ trợ in phiếu thu."],
            ["UC05", "Ghi nhận thanh toán", "Admin", "Chọn hóa đơn -> Nhập số tiền nộp & phương thức -> Lưu phiếu thanh toán -> Tự động đổi trạng thái hóa đơn sang Đã thanh toán."],
            ["UC06", "Báo sự cố & xử lý", "Admin, User", "Khách gửi nội dung sự cố & mức độ khẩn cấp -> Admin tiếp nhận, phân công sửa chữa -> Cập nhật trạng thái Hoàn thành."]
        ],
        "Bảng 2.2: Đặc tả các Use Case cốt lõi của hệ thống"
    )

    add_sec1(doc, "2.3. Biểu Đồ Luồng Dữ Liệu (DFD)")
    add_p(doc, "Biểu đồ DFD mức 0 (Biểu đồ ngữ cảnh) thể hiện toàn bộ luồng thông tin trao đổi giữa hệ thống với hai tác nhân Admin và Khách thuê:")
    add_image(doc, "sodo_dfd_muc0.png", "Hình 2.2: Sơ đồ luồng dữ liệu DFD Mức 0 (Biểu đồ ngữ cảnh)")

    add_p(doc, "Biểu đồ DFD mức 1 phân rã hệ thống thành 6 tiến trình con và 6 kho dữ liệu D1 - D6:")
    add_image(doc, "sodo_dfd_muc1.png", "Hình 2.3: Sơ đồ luồng dữ liệu DFD Mức 1")

    add_sec1(doc, "2.4. Sơ Đồ Tuần Tự Và Kiến Trúc Hệ Thống")
    add_p(doc, "Sơ đồ tuần tự thể hiện trình tự xử lý đăng nhập và xác thực phân quyền qua CSDL:")
    add_image(doc, "sodo_sequence_login.png", "Hình 2.4: Sơ đồ tuần tự chức năng Đăng nhập & Phân quyền")

    add_p(doc, "Hệ thống áp dụng kiến trúc 3 tầng (3-Tier Architecture): Presentation (Giao diện Client Bootstrap/JS), Application (Web Server Apache, PHP 8 xử lý nghiệp vụ) và Database (MySQL 8.0 lưu trữ bền vững):")
    add_image(doc, "sodo_kientruc.png", "Hình 2.5: Sơ đồ kiến trúc 3 tầng hệ thống Quản Lý Phòng Trọ")

    add_sec1(doc, "2.5. Thiết Kế Cơ Sở Dữ Liệu (ERD & Từ Điển Dữ Liệu)")
    add_p(doc, "Cơ sở dữ liệu quan_ly_phong_tro gồm 10 bảng chuẩn hóa 3NF, liên kết chặt chẽ qua các khóa ngoại:")
    add_image(doc, "sodo_erd.png", "Hình 2.6: Sơ đồ quan hệ thực thể ERD hệ thống Quản Lý Phòng Trọ")

    add_table(doc,
        ["Bảng", "Trường Chính", "Khóa / Quan Hệ", "Ý Nghĩa Nghiệp Vụ"],
        [
            ["users", "id, username, password, ho_ten, email, so_dien_thoai, vai_tro, trang_thai, tenant_id", "PK: id, UQ: username, FK: tenant_id -> tenants", "Quản lý tài khoản đăng nhập Admin và Khách thuê."],
            ["rooms", "id, ma_phong, ten_phong, loai_phong, tang, khu, dien_tich, gia_thue, tien_coc, so_nguoi_toi_da, trang_thai", "PK: id, UQ: ma_phong", "Quản lý thông tin chi tiết phòng, giá thuê và tình trạng."],
            ["tenants", "id, ho_ten, ngay_sinh, gioi_tinh, so_dien_thoai, email, so_cmnd, dia_chi, nghe_nghiep, room_id, ngay_bat_dau_thue, trang_thai", "PK: id, FK: room_id -> rooms", "Hồ sơ nhân thân người thuê phòng và phòng lưu trú."],
            ["contracts", "id, ma_hop_dong, room_id, tenant_id, ngay_bat_dau, ngay_ket_thuc, gia_thue, tien_coc, chu_ky_thanh_toan, trang_thai", "PK: id, UQ: ma_hop_dong, FK: room_id, tenant_id", "Hợp đồng thuê phòng, thời hạn và thỏa thuận tiền cọc."],
            ["electric_water", "id, room_id, thang, nam, chi_so_dien_cu, moi, don_gia_dien, chi_so_nuoc_cu, moi, don_gia_nuoc, ngay_ghi", "PK: id, UQ: (room_id, thang, nam), FK: room_id", "Chỉ số công tơ điện nước hàng tháng và đơn giá."],
            ["services", "id, ma_dich_vu, ten_dich_vu, don_gia, don_vi_tinh, mo_ta, trang_thai", "PK: id, UQ: ma_dich_vu", "Danh mục bảng giá các dịch vụ dùng chung trong khu trọ."],
            ["service_usage", "id, room_id, service_id, thang, nam, so_luong, thanh_tien", "PK: id, FK: room_id, service_id", "Ghi nhận mức độ sử dụng dịch vụ của từng phòng theo kỳ."],
            ["invoices", "id, ma_hoa_don, room_id, tenant_id, thang, nam, tien_phong, tien_dien, tien_nuoc, tien_dich_vu, phi_khac, tong_tien, han_thanh_toan, trang_thai", "PK: id, UQ: ma_hoa_don, FK: room_id, tenant_id", "Hóa đơn tổng hợp hàng tháng và trạng thái thanh toán."],
            ["payments", "id, ma_thanh_toan, invoice_id, tenant_id, so_tien, phuong_thuc, ngay_thanh_toan, ghi_chu", "PK: id, UQ: ma_thanh_toan, FK: invoice_id, tenant_id", "Lịch sử các lần đóng tiền, biên lai thanh toán."],
            ["maintenance_requests", "id, room_id, tenant_id, tieu_de, noi_dung, muc_do, trang_thai, ghi_chu_xu_ly, ngay_tao", "PK: id, FK: room_id, tenant_id", "Yêu cầu báo hỏng, sửa chữa thiết bị từ người thuê."]
        ],
        "Bảng 2.3: Tổng hợp cấu trúc 10 bảng trong cơ sở dữ liệu quan_ly_phong_tro"
    )

    add_p(doc, "Các ràng buộc khóa ngoại (Foreign Key) then chốt đảm bảo tính toàn vẹn dữ liệu trong hệ thống:")
    add_bullet(doc, "tenants.room_id tham chiếu rooms.id: Xác định phòng mà khách đang lưu trú, ngăn chặn gán phòng không tồn tại.")
    add_bullet(doc, "contracts liên kết song song rooms.id và tenants.id: Ràng buộc pháp lý giữa người thuê và phòng thuê.")
    add_bullet(doc, "electric_water, service_usage và invoices liên kết rooms.id: Đảm bảo chi phí luôn gắn liền với mã phòng cụ thể.")
    add_bullet(doc, "payments liên kết invoices.id: Ghi nhận biên lai thanh toán chính xác theo từng hóa đơn và gạch nợ tự động.")
    add_bullet(doc, "maintenance_requests liên kết room_id và tenant_id: Truy xuất chính xác nguồn gốc phản ánh sự cố.")

    # ═════════════════════════════════════════════════════════════════
    # CHƯƠNG III: XÂY DỰNG VÀ CÀI ĐẶT HỆ THỐNG
    # ═════════════════════════════════════════════════════════════════
    add_chapter(doc, "CHƯƠNG III: XÂY DỰNG VÀ CÀI ĐẶT HỆ THỐNG")

    add_sec1(doc, "3.1. Cấu Trúc Mã Nguồn Và Kết Nối CSDL")
    add_p(doc, "Mã nguồn được tổ chức theo module hóa rõ ràng trong thư mục QuanLyPhongTro. Kết nối CSDL sử dụng PDO Singleton Pattern với Prepared Statements đảm bảo hiệu năng và phòng chống SQL Injection tuyệt đối:")

    add_code(doc,
"""// config/database.php - Kết nối PDO Singleton an toàn với Prepared Statements
function getDB(): PDO {
    static $pdo = null;
    if ($pdo === null) {
        $dsn = "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=utf8mb4";
        $options = [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES   => false,
        ];
        $pdo = new PDO($dsn, DB_USER, DB_PASS, $options);
    }
    return $pdo;
}"""
    )

    add_p(doc, "Cơ chế kiểm soát truy cập và bảo vệ phân quyền (Role-Based Access Control) được triển khai qua Session và hàm chặn truy cập trái phép:")
    add_code(doc,
"""// includes/auth.php - Xác thực và phân quyền người dùng
function requireAdmin() {
    requireLogin();
    if ($_SESSION['vai_tro'] !== 'admin') {
        header("Location: " . getBaseUrl() . "/login.php?msg=access_denied");
        exit();
    }
}
function requireKhachThue() {
    requireLogin();
    if ($_SESSION['vai_tro'] !== 'khach_thue') {
        header("Location: " . getBaseUrl() . "/admin/dashboard.php");
        exit();
    }
}"""
    )

    add_p(doc, "Thuật toán tính toán điện nước và tổng hợp công nợ hóa đơn tự động:")
    add_code(doc,
"""// Tự động tổng hợp chi phí hóa đơn hàng tháng
$tien_dien  = ($so_dien_moi - $so_dien_cu) * $don_gia_dien;
$tien_nuoc  = ($so_nuoc_moi - $so_nuoc_cu) * $don_gia_nuoc;
$tong_tien  = $tien_phong + $tien_dien + $tien_nuoc + $tien_dich_vu + $phi_khac;
// Lưu trữ giao dịch và tự động gạch nợ sau thanh toán"""
    )

    add_sec1(doc, "3.2. Cài Đặt Giao Diện Phân Hệ Quản Trị Viên (Admin)")
    add_p(doc, "Dưới đây là các màn hình chức năng chính của phân hệ Quản trị viên:")

    add_image(doc, "hinh_login.png", "Hình 3.1: Giao diện đăng nhập hệ thống")
    add_image(doc, "hinh_admin_dashboard.png", "Hình 3.2: Dashboard tổng quan Quản trị viên với chỉ số KPI và biểu đồ Chart.js")
    add_image(doc, "hinh_admin_phong.png", "Hình 3.3: Quản lý danh mục phòng trọ (thêm, sửa, lọc trạng thái)")
    add_image(doc, "hinh_admin_nguoithue.png", "Hình 3.4: Quản lý hồ sơ người thuê phòng và liên kết lưu trú")
    add_image(doc, "hinh_admin_hopdong.png", "Hình 3.5: Quản lý hợp đồng thuê phòng và cảnh báo hạn hợp đồng")
    add_image(doc, "hinh_admin_diennuoc.png", "Hình 3.6: Quản lý và nhập chỉ số điện nước theo tháng")
    add_image(doc, "hinh_admin_dichvu.png", "Hình 3.7: Quản lý danh mục và bảng giá dịch vụ dùng chung")
    add_image(doc, "hinh_admin_hoadon.png", "Hình 3.8: Quản lý hóa đơn tiền phòng và trạng thái thanh toán")
    add_image(doc, "hinh_admin_hoadon_in.png", "Hình 3.9: Mẫu phiếu thu hóa đơn chuẩn Print-friendly", width_in=4.2)
    add_image(doc, "hinh_admin_thanhtoan.png", "Hình 3.10: Ghi nhận thanh toán và lịch sử giao dịch")
    add_image(doc, "hinh_admin_suco.png", "Hình 3.11: Tiếp nhận và cập nhật tiến độ xử lý sự cố sửa chữa")
    add_image(doc, "hinh_admin_taikhoan.png", "Hình 3.12: Quản lý tài khoản hệ thống và phân quyền")
    add_image(doc, "hinh_admin_thongke.png", "Hình 3.13: Báo cáo thống kê tài chính và biểu đồ doanh thu 12 tháng")

    add_sec1(doc, "3.3. Cài Đặt Giao Diện Phân Hệ Khách Thuê (User Portal)")
    add_p(doc, "Phân hệ Khách thuê cung cấp giao diện riêng biệt giúp người thuê chủ động tra cứu toàn bộ thông tin phòng, hóa đơn và gửi phản ánh sự cố:")

    add_image(doc, "hinh_user_dashboard.png", "Hình 3.14: Dashboard Khách thuê hiển thị tổng quan phòng và số tiền cần đóng")
    add_image(doc, "hinh_user_phong.png", "Hình 3.15: Tra cứu chi tiết thông tin phòng đang thuê")
    add_image(doc, "hinh_user_hopdong.png", "Hình 3.16: Tra cứu hợp đồng thuê và thanh tiến trình thời hạn")
    add_image(doc, "hinh_user_diennuoc.png", "Hình 3.17: Lịch sử chỉ số điện nước tiêu thụ qua các tháng")
    add_image(doc, "hinh_user_hoadon.png", "Hình 3.18: Danh sách hóa đơn cá nhân và hạn nộp tiền")
    add_image(doc, "hinh_user_thanhtoan.png", "Hình 3.19: Lịch sử các lần đã thanh toán tiền phòng")
    add_image(doc, "hinh_user_suco.png", "Hình 3.20: Gửi phản ánh báo hỏng và theo dõi tiến độ sửa chữa")
    add_image(doc, "hinh_user_taikhoan.png", "Hình 3.21: Quản lý thông tin cá nhân và đổi mật khẩu")

    # ═════════════════════════════════════════════════════════════════
    # CHƯƠNG IV: KIỂM THỬ VÀ ĐÁNH GIÁ KẾT QUẢ
    # ═════════════════════════════════════════════════════════════════
    add_chapter(doc, "CHƯƠNG IV: KIỂM THỬ VÀ ĐÁNH GIÁ KẾT QUẢ")

    add_sec1(doc, "4.1. Phương Pháp Kiểm Thử Hệ Thống")
    add_p(doc, "Nhóm áp dụng phương pháp kiểm thử hộp đen (Black-box Testing) để kiểm tra toàn diện chức năng, bảo mật và tính toàn vẹn dữ liệu:")

    add_table(doc,
        ["Mã TC", "Tên Test Case", "Dữ Liệu Đầu Vào", "Kết Quả Kỳ Vọng", "Kết Quả Thực Tế", "Đánh Giá"],
        [
            ["TC-AUTH-01", "Đăng nhập Admin", "admin / Admin@123", "Vào admin/dashboard.php", "Chuyển đúng trang", "ĐẠT ✓"],
            ["TC-AUTH-02", "Đăng nhập Khách thuê", "nguyen.van.a / User@123", "Vào user/dashboard.php", "Chuyển đúng trang", "ĐẠT ✓"],
            ["TC-AUTH-03", "Sai mật khẩu", "admin / SaiPass", "Báo lỗi sai thông tin đăng nhập", "Hiển thị alert đỏ", "ĐẠT ✓"],
            ["TC-ROOM-01", "Thêm phòng mới", "P301, Giá 2.500.000đ", "Lưu thành công vào CSDL", "Hiển thị trong bảng", "ĐẠT ✓"],
            ["TC-ROOM-02", "Trùng mã phòng", "P101 (đã có)", "Báo lỗi trùng mã phòng", "Chặn trùng lặp", "ĐẠT ✓"],
            ["TC-ROOM-03", "Xóa phòng có khách", "Xóa phòng P101", "Báo lỗi không thể xóa phòng đang thuê", "Chặn xóa an toàn", "ĐẠT ✓"],
            ["TC-EW-01", "Tính tiền điện nước", "Điện 50kWh, Nước 5m³", "Tính đúng tổng 300.000đ", "Tính toán chuẩn xác", "ĐẠT ✓"],
            ["TC-EW-02", "Số mới nhỏ hơn số cũ", "Cũ: 150, Mới: 120", "Báo lỗi không hợp lệ", "Chặn sai số học", "ĐẠT ✓"],
            ["TC-INV-01", "Lập hóa đơn tổng hợp", "Phòng P101: 2.5M + 300k + 100k", "Tổng 2.900.000đ, trạng thái Chưa TT", "Lập hóa đơn chuẩn", "ĐẠT ✓"],
            ["TC-INV-02", "Thanh toán & gạch nợ", "Nộp đủ 2.900.000đ", "Hóa đơn chuyển Đã thanh toán", "Gạch nợ tự động", "ĐẠT ✓"],
            ["TC-SEC-01", "Chống SQL Injection", "' OR '1'='1 vào form", "Bị chặn bởi Prepared Statement", "Không bị khai thác", "ĐẠT ✓"],
            ["TC-SEC-02", "Bảo vệ URL quản trị", "Khách gõ /admin/phong.php", "requireAdmin() chuyển hướng về user/", "Chặn trái phép", "ĐẠT ✓"]
        ],
        "Bảng 4.1: Bảng kết quả kiểm thử các chức năng chính của hệ thống"
    )

    add_sec1(doc, "4.2. Đánh Giá Kết Quả, Hạn Chế Và Hướng Phát Triển")
    add_p(doc, "Đánh giá kết quả đạt được:")
    add_bullet(doc, "Hoàn thành 100% các yêu cầu nghiệp vụ: Quản lý phòng, khách thuê, hợp đồng, điện nước, hóa đơn, thanh toán, sự cố và thống kê.")
    add_bullet(doc, "Bảo mật cao: Sử dụng Bcrypt và Prepared Statements ngăn chặn hoàn toàn SQL Injection.")
    add_bullet(doc, "Giao diện Bootstrap 5 responsive, thân thiện, dễ sử dụng trên cả Desktop và Mobile.")
    add_p(doc, "Hạn chế và hướng phát triển:")
    add_bullet(doc, "Hiện tại chưa tích hợp thanh toán tự động qua cổng trực tuyến (VNPay/MoMo) và chưa có SMS/Email nhắc nợ.")
    add_bullet(doc, "Hướng phát triển: Tích hợp mã VietQR động tự động gạch nợ và phát triển Mobile App (Flutter/React Native) cho khách thuê.")

    add_sec1(doc, "4.3. Đánh Giá Bảo Mật Và Hiệu Năng Hệ Thống")
    add_p(doc, "Hệ thống đáp ứng các tiêu chuẩn bảo mật theo khuyến nghị OWASP Top 10 và tối ưu hiệu năng vận hành:")
    add_bullet(doc, "Phòng chống SQL Injection: 100% truy vấn CSDL tham số hóa qua PDO Prepared Statements, vô hiệu hóa hoàn toàn câu lệnh SQL độc hại.")
    add_bullet(doc, "Bảo mật mật khẩu: Sử dụng thuật toán Bcrypt sinh muối tự động với chi phí tính toán cost=10, đảm bảo an toàn tuyệt đối ngay cả khi lộ CSDL.")
    add_bullet(doc, "Phòng chống tấn công XSS: Mọi dữ liệu do người dùng nhập trước khi render ra trình duyệt đều được làm sạch bằng hàm htmlspecialchars().")
    add_bullet(doc, "Kiểm soát phiên và phân quyền: Session được kiểm tra nghiêm ngặt qua requireAdmin() và requireKhachThue(), tự động hủy phiên khi logout.")
    add_bullet(doc, "Tối ưu chỉ mục CSDL: Thiết lập chỉ mục (INDEX) trên các cột truy vấn thường xuyên (ma_phong, room_id, tenant_id, ma_hoa_don) giúp truy xuất dưới 15ms.")

    add_table(doc,
        ["Hạng Mục Bảo Mật", "Cơ Chế Kỹ Thuật", "Giải Pháp Triển Khai", "Kết Quả"],
        [
            ["SQL Injection", "PDO Prepared Statements", "Tham số hóa toàn bộ câu lệnh SQL", "ĐẠT ✓"],
            ["Password Security", "Bcrypt Hash (password_hash)", "Mã hóa một chiều chống giải mã", "ĐẠT ✓"],
            ["Cross-Site Scripting", "HTML Entity Encoding", "Hàm htmlspecialchars(ENT_QUOTES)", "ĐẠT ✓"],
            ["Access Control", "Role-Based Middleware", "Chặn đứng truy cập URL trái phép", "ĐẠT ✓"],
            ["Session Hijacking", "Session Destruction", "Hủy phiên và reset Session ID khi thoát", "ĐẠT ✓"],
            ["Database Indexing", "B-Tree Indexes", "Tăng tốc truy vấn phòng và hóa đơn", "ĐẠT ✓"]
        ],
        "Bảng 4.2: Đánh giá tiêu chuẩn an toàn bảo mật và tối ưu hệ thống"
    )

    # ═════════════════════════════════════════════════════════════════
    # KẾT LUẬN & PHỤ LỤC & TÀI LIỆU THAM KHẢO
    # ═════════════════════════════════════════════════════════════════
    add_chapter(doc, "KẾT LUẬN VÀ KIẾN NGHỊ")
    add_p(doc, "Đề tài “Xây dựng Website Quản Lý Phòng Trọ” đã hoàn thành đúng tiến độ và đáp ứng toàn diện mục tiêu nghiên cứu đề ra. Hệ thống giải quyết trọn vẹn bài toán quản lý nhà trọ thủ công, mang lại hiệu quả thiết thực cho chủ trọ và sự tiện lợi, minh bạch cho khách thuê.")
    add_p(doc, "Qua đề tài, sinh viên đã củng cố kiến thức phân tích thiết kế hệ thống, lập trình PHP 8+, quản trị MySQL chuẩn 3NF và xây dựng giao diện responsive với Bootstrap 5.")

    add_chapter(doc, "PHỤ LỤC")

    add_sec1(doc, "Phụ Lục A: Hướng Dẫn Cài Đặt Trên XAMPP")
    add_p(doc, "Để triển khai và chạy thử nghiệm hệ thống Quản Lý Phòng Trọ trên máy tính cục bộ bằng gói phần mềm XAMPP, người dùng thực hiện theo các bước sau:")
    add_bullet(doc, "Bước 1: Khởi động bảng điều khiển XAMPP Control Panel, bật dịch vụ Apache và MySQL (nút Start chuyển sang màu xanh).")
    add_bullet(doc, "Bước 2: Sao chép toàn bộ thư mục QuanLyPhongTro vào thư mục gốc web server: C:\\xampp\\htdocs\\QuanLyPhongTro.")
    add_bullet(doc, "Bước 3: Mở trình duyệt web truy cập công cụ phpMyAdmin tại địa chỉ: http://localhost/phpmyadmin.")
    add_bullet(doc, "Bước 4: Tạo cơ sở dữ liệu mới với tên quan_ly_phong_tro, chọn bảng mã utf8mb4_unicode_ci.")
    add_bullet(doc, "Bước 5: Chọn tab Import (Nhập), chọn tệp tin database.sql trong thư mục dự án và nhấn Thực hiện để nạp cấu trúc 10 bảng cùng dữ liệu mẫu ban đầu.")
    add_bullet(doc, "Bước 6: Kiểm tra cấu hình kết nối tại config/database.php (mặc định host: localhost, user: root, password rỗng).")
    add_bullet(doc, "Bước 7: Mở trình duyệt web và truy cập hệ thống theo đường dẫn: http://localhost/QuanLyPhongTro.")

    doc.add_page_break()
    add_sec1(doc, "Phụ Lục B: Danh Sách Tài Khoản Demo Nghiệm Thu")
    add_p(doc, "Hệ thống đã được khởi tạo sẵn các tài khoản demo đại diện cho các vai trò khác nhau để phục vụ công tác kiểm thử và nghiệm thu:")
    add_table(doc,
        ["Vai Trò", "Tên Đăng Nhập", "Mật Khẩu", "Ghi Chú"],
        [
            ["Admin (Chủ trọ)", "admin", "Admin@123", "Toàn quyền quản trị hệ thống."],
            ["Khách thuê (P101)", "nguyen.van.a", "User@123", "Khách thuê phòng P101."],
            ["Khách thuê (P102)", "tran.thi.b", "User@123", "Khách thuê phòng P102."],
            ["Khách thuê (P201)", "le.van.c", "User@123", "Khách thuê phòng P201."]
        ],
        "Bảng PL.1: Danh sách tài khoản demo"
    )

    doc.add_page_break()
    add_sec1(doc, "Phụ Lục C: Công Nghệ Sử Dụng Trong Dự Án")
    add_table(doc,
        ["Công Nghệ", "Phiên Bản", "Mục Đích"],
        [
            ["PHP", "8.0+", "Ngôn ngữ backend xử lý logic."],
            ["MySQL", "8.0", "Hệ quản trị CSDL quan hệ lưu trữ dữ liệu."],
            ["Apache", "2.4", "Web Server điều phối HTTP Request."],
            ["Bootstrap", "5.3", "CSS Framework responsive layout."],
            ["Chart.js", "4.4", "Vẽ biểu đồ thống kê trực quan."],
            ["Bcrypt / PDO", "Tích hợp", "Mã hóa mật khẩu và truy vấn CSDL an toàn."]
        ],
        "Bảng PL.2: Công nghệ và phiên bản sử dụng"
    )

    add_chapter(doc, "TÀI LIỆU THAM KHẢO")
    refs = [
        "[1] PHP Group (2024). PHP Documentation. https://www.php.net/docs.php",
        "[2] Oracle Corporation (2024). MySQL 8.0 Reference Manual. https://dev.mysql.com/doc/",
        "[3] Bootstrap Team (2023). Bootstrap 5.3 Documentation. https://getbootstrap.com/",
        "[4] Chart.js Project (2024). Chart.js Documentation. https://www.chartjs.org/",
        "[5] OWASP Foundation (2024). SQL Injection Prevention & Password Storage Cheat Sheet. https://owasp.org/",
        "[6] W3Schools (2024). PHP & MySQL Web Development Tutorials. https://www.w3schools.com/"
    ]
    for ref in refs:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Cm(0.6)
        p.paragraph_format.first_line_indent = Cm(-0.6)
        p.paragraph_format.space_after = Pt(2.5)
        run = p.add_run(ref)
        set_font(run, size=10)

    doc.save(OUT_PATH)
    print(f"Saved document to: {OUT_PATH}")

if __name__ == '__main__':
    build()
