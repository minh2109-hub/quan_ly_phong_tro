import subprocess
import os
import time

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
img_dir = r"c:\xampp\htdocs\QuanLyPhongTro\assets\images"
os.makedirs(img_dir, exist_ok=True)

targets = [
    ("hinh_login.png", "http://localhost/QuanLyPhongTro/login.php", 1280, 800),
    ("hinh_admin_dashboard.png", "http://localhost/QuanLyPhongTro/admin/preview.php?page=dashboard.php", 1280, 950),
    ("hinh_admin_phong.png", "http://localhost/QuanLyPhongTro/admin/preview.php?page=phong.php", 1280, 850),
    ("hinh_admin_nguoithue.png", "http://localhost/QuanLyPhongTro/admin/preview.php?page=nguoi_thue.php", 1280, 850),
    ("hinh_admin_hopdong.png", "http://localhost/QuanLyPhongTro/admin/preview.php?page=hop_dong.php", 1280, 850),
    ("hinh_admin_diennuoc.png", "http://localhost/QuanLyPhongTro/admin/preview.php?page=dien_nuoc.php", 1280, 850),
    ("hinh_admin_dichvu.png", "http://localhost/QuanLyPhongTro/admin/preview.php?page=dich_vu.php", 1280, 850),
    ("hinh_admin_hoadon.png", "http://localhost/QuanLyPhongTro/admin/preview.php?page=hoa_don.php", 1280, 850),
    ("hinh_admin_hoadon_in.png", "http://localhost/QuanLyPhongTro/admin/preview.php?page=hoa_don_in.php", 1000, 800),
    ("hinh_admin_thanhtoan.png", "http://localhost/QuanLyPhongTro/admin/preview.php?page=thanh_toan.php", 1280, 850),
    ("hinh_admin_suco.png", "http://localhost/QuanLyPhongTro/admin/preview.php?page=su_co.php", 1280, 850),
    ("hinh_admin_taikhoan.png", "http://localhost/QuanLyPhongTro/admin/preview.php?page=tai_khoan.php", 1280, 850),
    ("hinh_admin_thongke.png", "http://localhost/QuanLyPhongTro/admin/preview.php?page=thong_ke.php", 1280, 950),
    ("hinh_user_dashboard.png", "http://localhost/QuanLyPhongTro/user/preview.php?page=dashboard.php", 1280, 850),
    ("hinh_user_phong.png", "http://localhost/QuanLyPhongTro/user/preview.php?page=phong.php", 1280, 800),
    ("hinh_user_hopdong.png", "http://localhost/QuanLyPhongTro/user/preview.php?page=hop_dong.php", 1280, 800),
    ("hinh_user_diennuoc.png", "http://localhost/QuanLyPhongTro/user/preview.php?page=dien_nuoc.php", 1280, 800),
    ("hinh_user_hoadon.png", "http://localhost/QuanLyPhongTro/user/preview.php?page=hoa_don.php", 1280, 800),
    ("hinh_user_thanhtoan.png", "http://localhost/QuanLyPhongTro/user/preview.php?page=thanh_toan.php", 1280, 800),
    ("hinh_user_suco.png", "http://localhost/QuanLyPhongTro/user/preview.php?page=su_co.php", 1280, 850),
    ("hinh_user_taikhoan.png", "http://localhost/QuanLyPhongTro/user/preview.php?page=tai_khoan.php", 1280, 800),
]

for filename, url, w, h in targets:
    out_path = os.path.join(img_dir, filename)
    cmd = f'"{edge_path}" --headless=new --disable-gpu --window-size={w},{h} --screenshot="{out_path}" "{url}"'
    subprocess.run(cmd, shell=True, capture_output=True)
    if os.path.exists(out_path):
        size = os.path.getsize(out_path)
        print(f"Captured {filename}: {size} bytes")
    else:
        print(f"FAILED {filename}")

print("Done capturing screenshots.")
