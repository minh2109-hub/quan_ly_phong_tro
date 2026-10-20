<?php
// File: user/dashboard.php - Trang chu khach thue
require_once "../config/database.php";
require_once "../includes/auth.php";
require_once "../includes/functions.php";
requireKhachThue();
define("PAGE_TITLE", "Trang Chủ");

$user = getCurrentUser();
$tid  = (int)$user["tenant_id"];

// Thong tin nguoi thue va phong
$tenant = $pdo->prepare("SELECT t.*,r.ma_phong,r.ten_phong,r.gia_thue,r.dien_tich FROM tenants t LEFT JOIN rooms r ON t.room_id=r.id WHERE t.id=?");
$tenant->execute([$tid]); $tenant = $tenant->fetch();

// Hoa don chua thanh toan
$hdChuaTT = $pdo->prepare("SELECT COUNT(*),COALESCE(SUM(tong_tien),0) FROM invoices WHERE tenant_id=? AND trang_thai IN ('chua_thanh_toan','qua_han')");
$hdChuaTT->execute([$tid]); $hdChuaTT = $hdChuaTT->fetch(PDO::FETCH_NUM);

// Su co dang xu ly
$scDangXL = $pdo->prepare("SELECT COUNT(*) FROM maintenance_requests WHERE tenant_id=? AND trang_thai != 'hoan_thanh'");
$scDangXL->execute([$tid]); $scDangXL = $scDangXL->fetchColumn();

// Hop dong hien tai
$hopDong = $pdo->prepare("SELECT * FROM contracts WHERE tenant_id=? AND trang_thai IN ('hieu_luc','sap_het_han') ORDER BY ngay_ket_thuc DESC LIMIT 1");
$hopDong->execute([$tid]); $hopDong = $hopDong->fetch();

// Hoa don gan day
$recentHD = $pdo->prepare("SELECT i.*,r.ma_phong FROM invoices i JOIN rooms r ON i.room_id=r.id WHERE i.tenant_id=? ORDER BY i.nam DESC,i.thang DESC LIMIT 5");
$recentHD->execute([$tid]); $recentHD = $recentHD->fetchAll();

// Dien nuoc thang nay
$my = getCurrentMonthYear();
$dienNuoc = null;
if ($tenant && $tenant["room_id"]) {
    $dn = $pdo->prepare("SELECT *,(chi_so_dien_moi-chi_so_dien_cu)*don_gia_dien as tien_dien,(chi_so_nuoc_moi-chi_so_nuoc_cu)*don_gia_nuoc as tien_nuoc FROM electric_water WHERE room_id=? AND thang=? AND nam=?");
    $dn->execute([$tenant["room_id"], $my["thang"], $my["nam"]]);
    $dienNuoc = $dn->fetch();
}

require_once "../includes/header_user.php";
?>
<?php echo showFlash(); ?>

<?php if ($tenant && $tenant["ma_phong"]): ?>
<div class="card mb-4" style="border-left:4px solid #2563eb">
  <div class="card-body">
    <div class="row align-items-center">
      <div class="col-md-8">
        <h5 class="fw-bold mb-1"><i class="fas fa-door-open me-2 text-primary"></i><?php echo htmlspecialchars($tenant["ma_phong"]." - ".$tenant["ten_phong"]); ?></h5>
        <p class="text-muted mb-1">Diện tích: <strong><?php echo $tenant["dien_tich"]; ?>m²</strong> | Giá thuê: <strong class="text-primary"><?php echo number_format($tenant["gia_thue"],0,",",".")."đ/tháng"; ?></strong></p>
        <p class="text-muted small mb-0">Bắt đầu thuê từ: <?php echo formatDate($tenant["ngay_bat_dau_thue"]); ?></p>
      </div>
      <div class="col-md-4 text-md-end mt-3 mt-md-0">
        <a href="phong.php" class="btn btn-outline-primary btn-sm"><i class="fas fa-info-circle me-1"></i>Xem Chi Tiết</a>
      </div>
    </div>
  </div>
</div>
<?php endif; ?>

<!-- Stat Cards -->
<div class="row g-4 mb-4">
  <div class="col-6 col-md-3">
    <div class="stat-card">
      <div class="stat-icon bg-danger bg-opacity-10"><i class="fas fa-receipt text-danger"></i></div>
      <div class="stat-value text-danger"><?php echo $hdChuaTT[0]; ?></div>
      <div class="stat-label">Hóa Đơn Chưa TT</div>
    </div>
  </div>
  <div class="col-6 col-md-3">
    <div class="stat-card">
      <div class="stat-icon bg-danger bg-opacity-10"><i class="fas fa-money-bill text-danger"></i></div>
      <div class="stat-value text-danger" style="font-size:1.1rem"><?php echo number_format($hdChuaTT[1]/1000000,2); ?>M</div>
      <div class="stat-label">Tổng Nợ Chưa TT</div>
    </div>
  </div>
  <div class="col-6 col-md-3">
    <div class="stat-card">
      <div class="stat-icon bg-warning bg-opacity-10"><i class="fas fa-tools text-warning"></i></div>
      <div class="stat-value text-warning"><?php echo $scDangXL; ?></div>
      <div class="stat-label">Sự Cố Đang Xử Lý</div>
    </div>
  </div>
  <div class="col-6 col-md-3">
    <div class="stat-card">
      <div class="stat-icon bg-success bg-opacity-10"><i class="fas fa-file-contract text-success"></i></div>
      <div class="stat-value text-success" style="font-size:0.9rem"><?php echo $hopDong ? formatDate($hopDong["ngay_ket_thuc"]) : "N/A"; ?></div>
      <div class="stat-label">Hợp Đồng Hết Hạn</div>
    </div>
  </div>
</div>

<div class="row g-4">
  <div class="col-lg-7">
    <div class="card">
      <div class="card-header d-flex justify-content-between align-items-center">
        <span class="card-title"><i class="fas fa-receipt me-2"></i>Hóa Đơn Gần Đây</span>
        <a href="hoa_don.php" class="btn btn-sm btn-outline-primary">Xem tất cả</a>
      </div>
      <div class="card-body p-0">
        <table class="table table-hover mb-0">
          <thead><tr><th>Tháng/Năm</th><th>Tổng Tiền</th><th>Hạn TT</th><th>Trạng Thái</th></tr></thead>
          <tbody>
            <?php if (empty($recentHD)): ?>
            <tr><td colspan="4" class="text-center text-muted py-4">Chưa có hóa đơn.</td></tr>
            <?php else: foreach ($recentHD as $hd): ?>
            <tr class="<?php echo $hd["trang_thai"]==="qua_han"?"table-danger":($hd["trang_thai"]==="chua_thanh_toan"?"table-warning":""); ?>">
              <td>T<?php echo $hd["thang"]; ?>/<?php echo $hd["nam"]; ?></td>
              <td class="fw-bold"><?php echo number_format($hd["tong_tien"],0,",",".")."đ"; ?></td>
              <td class="small"><?php echo formatDate($hd["han_thanh_toan"]); ?></td>
              <td><?php echo getStatusBadge($hd["trang_thai"]); ?></td>
            </tr>
            <?php endforeach; endif; ?>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <div class="col-lg-5">
    <div class="card">
      <div class="card-header"><span class="card-title"><i class="fas fa-bolt me-2 text-warning"></i>Điện Nước T<?php echo $my["thang"]; ?>/<?php echo $my["nam"]; ?></span></div>
      <div class="card-body">
        <?php if ($dienNuoc): ?>
        <div class="row g-3">
          <div class="col-6">
            <div class="text-center p-3 bg-warning bg-opacity-10 rounded">
              <i class="fas fa-bolt fa-2x text-warning mb-2 d-block"></i>
              <div class="fw-bold"><?php echo number_format($dienNuoc["chi_so_dien_moi"]-$dienNuoc["chi_so_dien_cu"],1); ?> kWh</div>
              <div class="text-success fw-bold"><?php echo number_format($dienNuoc["tien_dien"],0,",",".")."đ"; ?></div>
            </div>
          </div>
          <div class="col-6">
            <div class="text-center p-3 bg-info bg-opacity-10 rounded">
              <i class="fas fa-tint fa-2x text-info mb-2 d-block"></i>
              <div class="fw-bold"><?php echo number_format($dienNuoc["chi_so_nuoc_moi"]-$dienNuoc["chi_so_nuoc_cu"],1); ?> m³</div>
              <div class="text-success fw-bold"><?php echo number_format($dienNuoc["tien_nuoc"],0,",",".")."đ"; ?></div>
            </div>
          </div>
          <div class="col-12">
            <div class="alert alert-success py-2 mb-0 text-center">
              Tổng Điện Nước: <strong><?php echo number_format($dienNuoc["tien_dien"]+$dienNuoc["tien_nuoc"],0,",",".")."đ"; ?></strong>
            </div>
          </div>
        </div>
        <?php else: ?>
        <div class="empty-state"><i class="fas fa-bolt"></i><p>Chưa có dữ liệu điện nước tháng này.</p></div>
        <?php endif; ?>
      </div>
    </div>
  </div>
</div>
<?php require_once "../includes/footer_user.php"; ?>