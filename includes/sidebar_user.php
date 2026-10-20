<?php
// File: includes/sidebar_user.php - Sidebar Khách Thuê
$currentPage = basename($_SERVER["PHP_SELF"]);
function uActive($pages) {
    global $currentPage;
    return in_array($currentPage, (array)$pages) ? "active" : "";
}
?>
<nav class="sidebar" id="sidebar">
  <div class="sidebar-logo">
    <i class="fas fa-home me-2"></i>
    <span class="sidebar-text">Nhà Trọ</span>
  </div>
  <div class="sidebar-user-info">
    <div style="width:38px;height:38px;border-radius:50%;background:#3b82f6;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.9rem;flex-shrink:0">
      <?php echo strtoupper(mb_substr($_SESSION["ho_ten"] ?? "K", 0, 1, "UTF-8")); ?>
    </div>
    <div class="sidebar-text ms-2">
      <div style="font-size:.8rem;font-weight:600;color:#f8fafc;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:130px">
        <?php echo htmlspecialchars($_SESSION["ho_ten"] ?? ""); ?>
      </div>
      <div style="font-size:.7rem;color:#94a3b8">Khách Thuê</div>
    </div>
  </div>
  <ul class="sidebar-menu">
    <li>
      <a href="/QuanLyPhongTro/user/dashboard.php" class="<?php echo uActive("dashboard.php"); ?>">
        <i class="fas fa-home"></i><span class="sidebar-text">Trang Chủ</span>
      </a>
    </li>
    <li>
      <a href="/QuanLyPhongTro/user/phong.php" class="<?php echo uActive("phong.php"); ?>">
        <i class="fas fa-door-open"></i><span class="sidebar-text">Phòng Của Tôi</span>
      </a>
    </li>
    <li>
      <a href="/QuanLyPhongTro/user/hop_dong.php" class="<?php echo uActive("hop_dong.php"); ?>">
        <i class="fas fa-file-contract"></i><span class="sidebar-text">Hợp Đồng</span>
      </a>
    </li>
    <li>
      <a href="/QuanLyPhongTro/user/dien_nuoc.php" class="<?php echo uActive("dien_nuoc.php"); ?>">
        <i class="fas fa-bolt"></i><span class="sidebar-text">Điện Nước</span>
      </a>
    </li>
    <li>
      <a href="/QuanLyPhongTro/user/hoa_don.php" class="<?php echo uActive("hoa_don.php"); ?>">
        <i class="fas fa-receipt"></i><span class="sidebar-text">Hóa Đơn</span>
      </a>
    </li>
    <li>
      <a href="/QuanLyPhongTro/user/thanh_toan.php" class="<?php echo uActive("thanh_toan.php"); ?>">
        <i class="fas fa-money-bill-wave"></i><span class="sidebar-text">Lịch Sử TT</span>
      </a>
    </li>
    <li>
      <a href="/QuanLyPhongTro/user/su_co.php" class="<?php echo uActive("su_co.php"); ?>">
        <i class="fas fa-tools"></i><span class="sidebar-text">Báo Sự Cố</span>
      </a>
    </li>
    <li>
      <a href="/QuanLyPhongTro/user/tai_khoan.php" class="<?php echo uActive("tai_khoan.php"); ?>">
        <i class="fas fa-user-cog"></i><span class="sidebar-text">Tài Khoản</span>
      </a>
    </li>
    <li class="mt-2">
      <a href="/QuanLyPhongTro/logout.php" onclick="return confirm('Bạn có chắc muốn đăng xuất?')">
        <i class="fas fa-sign-out-alt"></i><span class="sidebar-text">Đăng Xuất</span>
      </a>
    </li>
  </ul>
</nav>