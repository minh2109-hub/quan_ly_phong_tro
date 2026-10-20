<?php
// File: includes/sidebar.php - Sidebar Admin
$currentPage = basename($_SERVER["PHP_SELF"]);
function isActive($pages) {
    global $currentPage;
    return in_array($currentPage, (array)$pages) ? "active" : "";
}
?>
<nav class="sidebar" id="sidebar">
  <div class="sidebar-logo">
    <i class="fas fa-building me-2"></i>
    <span class="sidebar-text">Quản Lý Trọ</span>
  </div>

  <div class="sidebar-user-info">
    <div style="width:38px;height:38px;border-radius:50%;background:#3b82f6;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.9rem;flex-shrink:0">
      <?php echo strtoupper(mb_substr($_SESSION["ho_ten"] ?? "A", 0, 1, "UTF-8")); ?>
    </div>
    <div class="sidebar-text ms-2">
      <div style="font-size:.8rem;font-weight:600;color:#f8fafc;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:130px">
        <?php echo htmlspecialchars($_SESSION["ho_ten"] ?? ""); ?>
      </div>
      <div style="font-size:.7rem;color:#94a3b8">Quản Trị Viên</div>
    </div>
  </div>

  <ul class="sidebar-menu">
    <li class="menu-section">TỔNG QUAN</li>
    <li>
      <a href="/QuanLyPhongTro/admin/dashboard.php" class="<?php echo isActive("dashboard.php"); ?>">
        <i class="fas fa-tachometer-alt"></i>
        <span class="sidebar-text">Dashboard</span>
      </a>
    </li>
    <li>
      <a href="/QuanLyPhongTro/admin/thong_ke.php" class="<?php echo isActive("thong_ke.php"); ?>">
        <i class="fas fa-chart-line"></i>
        <span class="sidebar-text">Thống Kê</span>
      </a>
    </li>

    <li class="menu-section">QUẢN LÝ</li>
    <li>
      <a href="/QuanLyPhongTro/admin/phong.php" class="<?php echo isActive("phong.php"); ?>">
        <i class="fas fa-door-open"></i>
        <span class="sidebar-text">Phòng Trọ</span>
      </a>
    </li>
    <li>
      <a href="/QuanLyPhongTro/admin/nguoi_thue.php" class="<?php echo isActive("nguoi_thue.php"); ?>">
        <i class="fas fa-users"></i>
        <span class="sidebar-text">Người Thuê</span>
      </a>
    </li>
    <li>
      <a href="/QuanLyPhongTro/admin/hop_dong.php" class="<?php echo isActive("hop_dong.php"); ?>">
        <i class="fas fa-file-contract"></i>
        <span class="sidebar-text">Hợp Đồng</span>
      </a>
    </li>
    <li>
      <a href="/QuanLyPhongTro/admin/dich_vu.php" class="<?php echo isActive("dich_vu.php"); ?>">
        <i class="fas fa-concierge-bell"></i>
        <span class="sidebar-text">Dịch Vụ</span>
      </a>
    </li>

    <li class="menu-section">TÀI CHÍNH</li>
    <li>
      <a href="/QuanLyPhongTro/admin/dien_nuoc.php" class="<?php echo isActive("dien_nuoc.php"); ?>">
        <i class="fas fa-bolt"></i>
        <span class="sidebar-text">Điện Nước</span>
      </a>
    </li>
    <li>
      <a href="/QuanLyPhongTro/admin/hoa_don.php" class="<?php echo isActive("hoa_don.php"); ?>">
        <i class="fas fa-receipt"></i>
        <span class="sidebar-text">Hóa Đơn</span>
      </a>
    </li>
    <li>
      <a href="/QuanLyPhongTro/admin/thanh_toan.php" class="<?php echo isActive("thanh_toan.php"); ?>">
        <i class="fas fa-money-bill-wave"></i>
        <span class="sidebar-text">Thanh Toán</span>
      </a>
    </li>

    <li class="menu-section">HỆ THỐNG</li>
    <li>
      <a href="/QuanLyPhongTro/admin/su_co.php" class="<?php echo isActive("su_co.php"); ?>">
        <i class="fas fa-tools"></i>
        <span class="sidebar-text">Sự Cố</span>
      </a>
    </li>
    <li>
      <a href="/QuanLyPhongTro/admin/tai_khoan.php" class="<?php echo isActive("tai_khoan.php"); ?>">
        <i class="fas fa-user-cog"></i>
        <span class="sidebar-text">Tài Khoản</span>
      </a>
    </li>
    <li>
      <a href="/QuanLyPhongTro/logout.php" onclick="return confirm('Bạn có chắc muốn đăng xuất?')">
        <i class="fas fa-sign-out-alt"></i>
        <span class="sidebar-text">Đăng Xuất</span>
      </a>
    </li>
  </ul>
</nav>