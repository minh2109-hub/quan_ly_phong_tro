import os
import subprocess

img_dir = r"c:\xampp\htdocs\QuanLyPhongTro\assets\images"
html_dir = r"c:\xampp\htdocs\QuanLyPhongTro\assets\diagrams_html"
os.makedirs(html_dir, exist_ok=True)
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

diagrams = {}

# 1. Kiến trúc hệ thống
diagrams["sodo_kientruc.png"] = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
body { font-family: 'Segoe UI', Arial, sans-serif; background: #fff; margin: 0; padding: 30px; display: flex; justify-content: center; }
.container { width: 900px; }
.title { text-align: center; font-size: 22px; font-weight: bold; color: #1e3a8a; margin-bottom: 25px; text-transform: uppercase; }
.layer { border: 2px solid #2563eb; border-radius: 12px; padding: 18px 25px; margin-bottom: 20px; background: #f8fafc; position: relative; }
.layer-title { font-size: 16px; font-weight: bold; color: #1d4ed8; margin-bottom: 12px; display: flex; align-items: center; }
.layer-badge { background: #2563eb; color: #fff; padding: 4px 10px; border-radius: 6px; font-size: 12px; margin-right: 10px; }
.boxes { display: flex; gap: 15px; justify-content: space-around; }
.box { flex: 1; background: #fff; border: 1.5px solid #cbd5e1; border-radius: 8px; padding: 12px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.box h4 { margin: 0 0 6px; font-size: 14px; color: #0f172a; }
.box p { margin: 0; font-size: 12px; color: #64748b; line-height: 1.4; }
.arrow { text-align: center; font-size: 24px; color: #2563eb; margin: -10px 0 10px; font-weight: bold; }
</style></head><body><div class="container">
<div class="title">Sơ Đồ Kiến Trúc Hệ Thống Quản Lý Phòng Trọ</div>
<div class="layer">
  <div class="layer-title"><span class="layer-badge">TẦNG 1</span> PRESENTATION LAYER (TẦNG GIAO DIỆN CLIENT)</div>
  <div class="boxes">
    <div class="box"><h4>Trình Duyệt Web</h4><p>Chrome, Edge, Firefox, Safari<br>Responsive Desktop & Mobile</p></div>
    <div class="box"><h4>Frontend Framework</h4><p>HTML5, CSS3, JavaScript ES6<br>Bootstrap 5.3, Font Awesome 6</p></div>
    <div class="box"><h4>Thư Viện Trực Quan</h4><p>Chart.js 4.4 (Biểu đồ)<br>jQuery 3.7 (DOM & Event)</p></div>
  </div>
</div>
<div class="arrow">↓ ↑ &nbsp; HTTP / HTTPS &nbsp; (JSON & Form Request)</div>
<div class="layer">
  <div class="layer-title"><span class="layer-badge">TẦNG 2</span> APPLICATION LAYER (TẦNG MÁY CHỦ ỨNG DỤNG)</div>
  <div class="boxes">
    <div class="box"><h4>Web Server</h4><p>Apache 2.4 (XAMPP)<br>Routing & Virtual Host</p></div>
    <div class="box"><h4>Xác Thực & Phân Quyền</h4><p>Session Management<br>Bcrypt Password Hash<br>RBAC (Admin / Khách)</p></div>
    <div class="box"><h4>Business Logic (PHP 8)</h4><p>CRUD Phòng, Khách, Hợp đồng<br>Tính điện nước & Lập hóa đơn<br>Xử lý sự cố & Báo cáo</p></div>
    <div class="box"><h4>Database Access</h4><p>PDO (PHP Data Objects)<br>Prepared Statements<br>SQL Injection Prevention</p></div>
  </div>
</div>
<div class="arrow">↓ ↑ &nbsp; MySQL Native Protocol (Port 3306)</div>
<div class="layer">
  <div class="layer-title"><span class="layer-badge">TẦNG 3</span> DATABASE LAYER (TẦNG CƠ SỞ DỮ LIỆU)</div>
  <div class="boxes">
    <div class="box"><h4>Hệ Quản Trị MySQL 8.0</h4><p>Database: quan_ly_phong_tro<br>Storage Engine: InnoDB<br>Charset: utf8mb4_unicode_ci</p></div>
    <div class="box"><h4>Các Bảng Thực Thể</h4><p>users, rooms, tenants<br>contracts, services<br>maintenance_requests</p></div>
    <div class="box"><h4>Các Bảng Nghiệp Vụ</h4><p>electric_water, service_usage<br>invoices, payments<br>Ràng buộc Foreign Keys & Index</p></div>
  </div>
</div>
</div></body></html>"""

# 2. Sơ đồ Use Case tổng quát
diagrams["sodo_usecase_tongquat.png"] = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
body { font-family: 'Segoe UI', Arial, sans-serif; background: #fff; margin: 0; padding: 25px; display: flex; justify-content: center; }
.container { width: 950px; }
.title { text-align: center; font-size: 22px; font-weight: bold; color: #1e3a8a; margin-bottom: 25px; text-transform: uppercase; }
.layout { display: flex; justify-content: space-between; align-items: stretch; position: relative; }
.actor-col { width: 140px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.actor-box { background: #eff6ff; border: 2px solid #2563eb; border-radius: 50%; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; font-size: 30px; margin-bottom: 10px; }
.actor-name { font-weight: bold; color: #1e3a8a; font-size: 15px; text-align: center; }
.system-boundary { flex: 1; border: 2px dashed #3b82f6; border-radius: 16px; padding: 20px; margin: 0 20px; background: #f8fafc; }
.system-title { text-align: center; font-size: 14px; font-weight: bold; color: #475569; margin-bottom: 15px; letter-spacing: 1px; }
.uc-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.uc-oval { background: #fff; border: 1.5px solid #2563eb; border-radius: 25px; padding: 8px 12px; text-align: center; font-size: 12.5px; font-weight: 600; color: #1e293b; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
.uc-shared { border-color: #10b981; background: #ecfdf5; color: #065f46; }
.uc-user { border-color: #8b5cf6; background: #f5f3ff; color: #5b21b6; }
.legend { display: flex; justify-content: center; gap: 20px; margin-top: 20px; font-size: 12px; }
.leg-item { display: flex; align-items: center; gap: 6px; }
.leg-dot { width: 14px; height: 14px; border-radius: 50%; border: 1.5px solid; }
</style></head><body><div class="container">
<div class="title">Sơ Đồ Use Case Tổng Quát Hệ Thống</div>
<div class="layout">
  <div class="actor-col">
    <div class="actor-box">👨‍💼</div>
    <div class="actor-name">ADMIN<br>(Chủ Trọ)</div>
    <div style="font-size:11px;color:#64748b;margin-top:6px;text-align:center">Toàn quyền quản trị</div>
  </div>
  <div class="system-boundary">
    <div class="system-title">HỆ THỐNG QUẢN LÝ PHÒNG TRỌ</div>
    <div class="uc-grid">
      <div class="uc-oval uc-shared">UC01: Đăng nhập / Đăng xuất</div>
      <div class="uc-oval uc-shared">UC02: Đổi mật khẩu cá nhân</div>
      <div class="uc-oval">UC03: Xem Dashboard tổng quan</div>
      <div class="uc-oval uc-user">UC04: Xem Dashboard cá nhân</div>
      <div class="uc-oval">UC05: Quản lý phòng trọ (CRUD)</div>
      <div class="uc-oval uc-user">UC06: Xem thông tin phòng thuê</div>
      <div class="uc-oval">UC07: Quản lý người thuê (CRUD)</div>
      <div class="uc-oval uc-user">UC08: Xem thông tin hợp đồng</div>
      <div class="uc-oval">UC09: Quản lý hợp đồng & thời hạn</div>
      <div class="uc-oval uc-user">UC10: Xem tiền điện nước hàng tháng</div>
      <div class="uc-oval">UC11: Quản lý & tính điện nước</div>
      <div class="uc-oval uc-user">UC12: Xem hóa đơn & hạn đóng</div>
      <div class="uc-oval">UC13: Quản lý & in hóa đơn</div>
      <div class="uc-oval uc-user">UC14: Xem lịch sử thanh toán</div>
      <div class="uc-oval">UC15: Quản lý & ghi thanh toán</div>
      <div class="uc-oval uc-shared">UC16: Gửi & xử lý yêu cầu sự cố</div>
      <div class="uc-oval">UC17: Quản lý danh mục dịch vụ</div>
      <div class="uc-oval">UC18: Báo cáo thống kê doanh thu</div>
      <div class="uc-oval">UC19: Quản lý tài khoản & phân quyền</div>
      <div class="uc-oval uc-user">UC20: Cập nhật thông tin cá nhân</div>
    </div>
  </div>
  <div class="actor-col">
    <div class="actor-box">🧑‍🎓</div>
    <div class="actor-name">KHÁCH THUÊ<br>(Người Thuê)</div>
    <div style="font-size:11px;color:#64748b;margin-top:6px;text-align:center">Portal cá nhân</div>
  </div>
</div>
<div class="legend">
  <div class="leg-item"><div class="leg-dot" style="border-color:#2563eb;background:#fff"></div> Use Case dành cho Admin</div>
  <div class="leg-item"><div class="leg-dot" style="border-color:#8b5cf6;background:#f5f3ff"></div> Use Case dành cho Khách Thuê</div>
  <div class="leg-item"><div class="leg-dot" style="border-color:#10b981;background:#ecfdf5"></div> Use Case dùng chung (Chung hai tác nhân)</div>
</div>
</div></body></html>"""

# 3. Sơ đồ DFD Mức 0 (Context Diagram)
diagrams["sodo_dfd_muc0.png"] = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
body { font-family: 'Segoe UI', Arial, sans-serif; background: #fff; margin: 0; padding: 30px; display: flex; justify-content: center; }
.container { width: 920px; }
.title { text-align: center; font-size: 22px; font-weight: bold; color: #1e3a8a; margin-bottom: 35px; text-transform: uppercase; }
.diagram { display: flex; align-items: center; justify-content: space-between; position: relative; }
.entity { width: 180px; border: 2px solid #1e3a8a; border-radius: 10px; background: #eff6ff; padding: 18px 12px; text-align: center; }
.entity h3 { margin: 0 0 6px; font-size: 16px; color: #1e3a8a; }
.entity p { margin: 0; font-size: 12px; color: #64748b; }
.center-proc { width: 260px; height: 160px; border: 2.5px solid #2563eb; border-radius: 50%; background: #dbeafe; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 15px; box-shadow: 0 4px 10px rgba(37,99,235,0.15); }
.center-proc h3 { margin: 0 0 4px; font-size: 17px; color: #1e3a8a; }
.center-proc p { margin: 0; font-size: 12px; color: #1e40af; }
.flows { display: flex; flex-direction: column; gap: 14px; width: 190px; }
.flow-line { background: #fff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 6px 8px; font-size: 11.5px; color: #334155; font-weight: 500; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.flow-in { border-left: 3px solid #2563eb; }
.flow-out { border-right: 3px solid #10b981; }
</style></head><body><div class="container">
<div class="title">Sơ Đồ Luồng Dữ Liệu DFD Mức 0 (Biểu Đồ Ngữ Cảnh)</div>
<div class="diagram">
  <div class="entity">
    <h3>ADMIN</h3>
    <p>Chủ nhà trọ / Quản lý</p>
  </div>
  <div class="flows">
    <div class="flow-line flow-in">Thông tin phòng, dịch vụ →</div>
    <div class="flow-line flow-in">Chỉ số điện nước, phí khác →</div>
    <div class="flow-line flow-in">Ghi nhận thanh toán →</div>
    <div class="flow-line flow-out">← Hóa đơn, thống kê, doanh thu</div>
    <div class="flow-line flow-out">← Yêu cầu sự cố cần xử lý</div>
  </div>
  <div class="center-proc">
    <h3>0. HỆ THỐNG</h3>
    <h3>QUẢN LÝ PHÒNG TRỌ</h3>
    <p>(Hệ thống trung tâm)</p>
  </div>
  <div class="flows">
    <div class="flow-line flow-in">← Thông tin cá nhân, đăng nhập</div>
    <div class="flow-line flow-in">← Yêu cầu báo sự cố sửa chữa</div>
    <div class="flow-line flow-out">Thông báo hóa đơn tiền phòng →</div>
    <div class="flow-line flow-out">Tra cứu chỉ số điện nước →</div>
    <div class="flow-line flow-out">Trạng thái xử lý sự cố →</div>
  </div>
  <div class="entity">
    <h3>KHÁCH THUÊ</h3>
    <p>Người thuê phòng trọ</p>
  </div>
</div>
</div></body></html>"""

# 4. Sơ đồ DFD Mức 1
diagrams["sodo_dfd_muc1.png"] = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
body { font-family: 'Segoe UI', Arial, sans-serif; background: #fff; margin: 0; padding: 25px; display: flex; justify-content: center; }
.container { width: 950px; }
.title { text-align: center; font-size: 22px; font-weight: bold; color: #1e3a8a; margin-bottom: 25px; text-transform: uppercase; }
.grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }
.proc { border: 2px solid #2563eb; border-radius: 12px; background: #eff6ff; padding: 15px; position: relative; }
.proc-num { background: #2563eb; color: #fff; border-radius: 50%; width: 26px; height: 26px; display: inline-flex; align-items: center; justify-content: center; font-size: 13px; font-weight: bold; margin-right: 6px; }
.proc h4 { margin: 0 0 10px; font-size: 15px; color: #1e3a8a; display: flex; align-items: center; }
.proc ul { margin: 0; padding-left: 20px; font-size: 12px; color: #334155; line-height: 1.6; }
.dstore { border: 1.5px solid #059669; border-left: 5px solid #059669; border-radius: 6px; background: #ecfdf5; padding: 10px 12px; margin-top: 15px; font-size: 12px; color: #065f46; font-weight: 600; }
</style></head><body><div class="container">
<div class="title">Sơ Đồ Luồng Dữ Liệu DFD Mức 1 (Phân Rã 5 Phân Hệ Chính)</div>
<div class="grid">
  <div class="proc">
    <h4><span class="proc-num">1.0</span> Quản Lý Xác Thực</h4>
    <ul>
      <li>Tiếp nhận username & password</li>
      <li>Mã hóa kiểm tra bcrypt</li>
      <li>Tạo Session & phân quyền truy cập</li>
      <li>Quản lý mở/khóa tài khoản</li>
    </ul>
    <div class="dstore">D1: Bảng users (Tài khoản)</div>
  </div>
  <div class="proc">
    <h4><span class="proc-num">2.0</span> Quản Lý Phòng & Khách</h4>
    <ul>
      <li>Thêm, sửa, xóa phòng trọ</li>
      <li>Quản lý hồ sơ người thuê</li>
      <li>Tạo và theo dõi hợp đồng</li>
      <li>Cảnh báo hợp đồng sắp hết hạn</li>
    </ul>
    <div class="dstore">D2: Bảng rooms, tenants, contracts</div>
  </div>
  <div class="proc">
    <h4><span class="proc-num">3.0</span> Quản Lý Điện Nước & DV</h4>
    <ul>
      <li>Nhập chỉ số điện, nước theo tháng</li>
      <li>Tự động tính chênh lệch & tiền</li>
      <li>Quản lý bảng giá dịch vụ</li>
      <li>Ghi nhận sử dụng dịch vụ</li>
    </ul>
    <div class="dstore">D3: Bảng electric_water, services</div>
  </div>
  <div class="proc">
    <h4><span class="proc-num">4.0</span> Quản Lý Hóa Đơn & Thu</h4>
    <ul>
      <li>Tổng hợp tiền phòng, điện, nước, DV</li>
      <li>Lập hóa đơn & in phiếu thu</li>
      <li>Ghi nhận thanh toán đa phương thức</li>
      <li>Tự động đổi trạng thái Đã Thanh Toán</li>
    </ul>
    <div class="dstore">D4: Bảng invoices, payments</div>
  </div>
  <div class="proc">
    <h4><span class="proc-num">5.0</span> Quản Lý Báo Sự Cố</h4>
    <ul>
      <li>Khách thuê gửi yêu cầu sự cố</li>
      <li>Admin tiếp nhận và xử lý</li>
      <li>Cập nhật tiến độ & hoàn thành</li>
      <li>Khách theo dõi kết quả</li>
    </ul>
    <div class="dstore">D5: Bảng maintenance_requests</div>
  </div>
  <div class="proc">
    <h4><span class="proc-num">6.0</span> Báo Cáo & Thống Kê</h4>
    <ul>
      <li>Thống kê tỷ lệ lấp đầy phòng</li>
      <li>Biểu đồ doanh thu 12 tháng</li>
      <li>Biểu đồ chi phí điện nước</li>
      <li>Theo dõi nợ và hóa đơn quá hạn</li>
    </ul>
    <div class="dstore">D6: Tổng hợp dữ liệu đa bảng</div>
  </div>
</div>
</div></body></html>"""

# 5. Sơ đồ thực thể ERD
diagrams["sodo_erd.png"] = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
body { font-family: 'Segoe UI', Arial, sans-serif; background: #fff; margin: 0; padding: 20px; display: flex; justify-content: center; }
.container { width: 1000px; }
.title { text-align: center; font-size: 22px; font-weight: bold; color: #1e3a8a; margin-bottom: 20px; text-transform: uppercase; }
.grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.table-card { border: 1.5px solid #3b82f6; border-radius: 8px; background: #fff; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.06); font-size: 11px; }
.th-header { background: #1e3a8a; color: #fff; padding: 6px 8px; font-weight: bold; font-size: 12px; display: flex; justify-content: space-between; }
.col-list { padding: 6px 8px; line-height: 1.5; color: #334155; }
.pk { color: #dc2626; font-weight: bold; }
.fk { color: #2563eb; font-weight: bold; }
.rel-bar { margin-top: 15px; padding: 10px 14px; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; font-size: 12px; color: #1e40af; }
</style></head><body><div class="container">
<div class="title">Sơ Đồ Thực Thể Liên Kết (ERD) - 10 Bảng Cơ Sở Dữ Liệu</div>
<div class="grid">
  <div class="table-card">
    <div class="th-header"><span>users</span><span>[Tài khoản]</span></div>
    <div class="col-list">
      <span class="pk">🔑 id (INT, PK)</span><br>
      username (VARCHAR)<br>password (VARCHAR)<br>ho_ten (VARCHAR)<br>email (VARCHAR)<br>
      vai_tro (ENUM)<br>trang_thai (ENUM)<br><span class="fk">🔗 tenant_id (INT, FK)</span>
    </div>
  </div>
  <div class="table-card">
    <div class="th-header"><span>rooms</span><span>[Phòng trọ]</span></div>
    <div class="col-list">
      <span class="pk">🔑 id (INT, PK)</span><br>
      ma_phong (VARCHAR, UQ)<br>ten_phong (VARCHAR)<br>loai_phong (VARCHAR)<br>
      tang, khu, dien_tich<br>gia_thue, tien_coc<br>so_nguoi_toi_da (INT)<br>trang_thai (ENUM)
    </div>
  </div>
  <div class="table-card">
    <div class="th-header"><span>tenants</span><span>[Người thuê]</span></div>
    <div class="col-list">
      <span class="pk">🔑 id (INT, PK)</span><br>
      ho_ten, so_dien_thoai<br>ngay_sinh, gioi_tinh<br>email, so_cmnd, dia_chi<br>
      <span class="fk">🔗 room_id (INT, FK)</span><br>ngay_bat_dau_thue<br>trang_thai (ENUM)
    </div>
  </div>
  <div class="table-card">
    <div class="th-header"><span>contracts</span><span>[Hợp đồng]</span></div>
    <div class="col-list">
      <span class="pk">🔑 id (INT, PK)</span><br>
      ma_hop_dong (VARCHAR, UQ)<br><span class="fk">🔗 room_id (INT, FK)</span><br>
      <span class="fk">🔗 tenant_id (INT, FK)</span><br>ngay_bat_dau, ngay_ket_thuc<br>
      gia_thue, tien_coc<br>chu_ky_thanh_toan<br>trang_thai (ENUM)
    </div>
  </div>
  <div class="table-card">
    <div class="th-header"><span>electric_water</span><span>[Điện nước]</span></div>
    <div class="col-list">
      <span class="pk">🔑 id (INT, PK)</span><br>
      <span class="fk">🔗 room_id (INT, FK)</span><br>thang, nam (INT)<br>
      chi_so_dien_cu, moi<br>don_gia_dien<br>chi_so_nuoc_cu, moi<br>don_gia_nuoc
    </div>
  </div>
  <div class="table-card">
    <div class="th-header"><span>services</span><span>[Dịch vụ]</span></div>
    <div class="col-list">
      <span class="pk">🔑 id (INT, PK)</span><br>
      ma_dich_vu (VARCHAR)<br>ten_dich_vu (VARCHAR)<br>don_gia (DECIMAL)<br>
      don_vi_tinh (VARCHAR)<br>mo_ta, trang_thai
    </div>
  </div>
  <div class="table-card">
    <div class="th-header"><span>invoices</span><span>[Hóa đơn]</span></div>
    <div class="col-list">
      <span class="pk">🔑 id (INT, PK)</span><br>
      ma_hoa_don (VARCHAR, UQ)<br><span class="fk">🔗 room_id (INT, FK)</span><br>
      <span class="fk">🔗 tenant_id (INT, FK)</span><br>thang, nam, tien_phong<br>
      tien_dien, tien_nuoc<br>tien_dich_vu, phi_khac<br>
      <b>tong_tien</b>, han_thanh_toan<br>trang_thai (ENUM)
    </div>
  </div>
  <div class="table-card">
    <div class="th-header"><span>payments</span><span>[Thanh toán]</span></div>
    <div class="col-list">
      <span class="pk">🔑 id (INT, PK)</span><br>
      ma_thanh_toan (VARCHAR)<br><span class="fk">🔗 invoice_id (INT, FK)</span><br>
      <span class="fk">🔗 tenant_id (INT, FK)</span><br>so_tien (DECIMAL)<br>
      phuong_thuc, ngay_tt
    </div>
  </div>
</div>
<div class="rel-bar">
  <b>Quan hệ chính:</b> rooms (1) ── (N) tenants | rooms (1) ── (N) contracts | rooms (1) ── (N) electric_water | 
  tenants (1) ── (N) invoices (1) ── (N) payments | rooms (1) ── (N) maintenance_requests | users (1) ── (1) tenants
</div>
</div></body></html>"""

# 6. Sơ đồ tuần tự Đăng nhập
diagrams["sodo_sequence_login.png"] = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
body { font-family: 'Segoe UI', Arial, sans-serif; background: #fff; margin: 0; padding: 25px; display: flex; justify-content: center; }
.container { width: 900px; }
.title { text-align: center; font-size: 22px; font-weight: bold; color: #1e3a8a; margin-bottom: 25px; text-transform: uppercase; }
.seq-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.seq-table th { background: #1e3a8a; color: #fff; padding: 10px; border: 1px solid #1e3a8a; }
.seq-table td { padding: 10px 12px; border: 1px solid #e2e8f0; vertical-align: top; }
.seq-table tr:nth-child(even) { background: #f8fafc; }
.step-num { font-weight: bold; color: #2563eb; }
</style></head><body><div class="container">
<div class="title">Sơ Đồ Tuần Tự (Sequence) - Chức Năng Đăng Nhập & Phân Quyền</div>
<table class="seq-table">
  <tr><th>Bước</th><th>Người Dùng (Client)</th><th>Trang Xử Lý (login.php)</th><th>Cơ Sở Dữ Liệu (MySQL)</th><th>Kết Quả / Chuyển Hướng</th></tr>
  <tr>
    <td class="step-num">1</td>
    <td>Nhập username, password và submit form</td>
    <td>Tiếp nhận POST request, validate dữ liệu đầu vào</td>
    <td>-</td>
    <td>Kiểm tra không để trống</td>
  </tr>
  <tr>
    <td class="step-num">2</td>
    <td>-</td>
    <td>Thực hiện Prepared Statement query</td>
    <td>SELECT * FROM users WHERE username = ?</td>
    <td>Trả về bản ghi user (nếu có)</td>
  </tr>
  <tr>
    <td class="step-num">3</td>
    <td>-</td>
    <td>Gọi password_verify(password, hash)</td>
    <td>-</td>
    <td>Khớp mật khẩu bcrypt</td>
  </tr>
  <tr>
    <td class="step-num">4 (Lỗi)</td>
    <td>Nhận thông báo lỗi màu đỏ</td>
    <td>Set thông báo lỗi: "Tên đăng nhập hoặc mật khẩu không đúng"</td>
    <td>-</td>
    <td>Giữ nguyên trang login.php</td>
  </tr>
  <tr>
    <td class="step-num">5 (Đúng)</td>
    <td>-</td>
    <td>Khởi tạo $_SESSION (user_id, role, ho_ten, tenant_id)</td>
    <td>UPDATE users SET lan_cuoi_dang_nhap = NOW()</td>
    <td>Ghi nhận phiên đăng nhập</td>
  </tr>
  <tr>
    <td class="step-num">6</td>
    <td>Được chuyển hướng đến trang tương ứng</td>
    <td>Kiểm tra vai_tro:<br>• Admin → /admin/dashboard.php<br>• Khách thuê → /user/dashboard.php</td>
    <td>-</td>
    <td>Tải giao diện làm việc theo vai trò</td>
  </tr>
</table>
</div></body></html>"""

# Write all html files and capture with edge
for fname, html in diagrams.items():
    hname = fname.replace(".png", ".html")
    hpath = os.path.join(html_dir, hname)
    with open(hpath, "w", encoding="utf-8") as f:
        f.write(html)
    
    out_img = os.path.join(img_dir, fname)
    cmd = f'"{edge_path}" --headless=new --disable-gpu --window-size=1200,800 --screenshot="{out_img}" "file:///{hpath}"'
    subprocess.run(cmd, shell=True, capture_output=True)
    if os.path.exists(out_img):
        print(f"Generated diagram {fname}: {os.path.getsize(out_img)} bytes")
    else:
        print(f"FAILED diagram {fname}")

print("Done generating diagrams.")
