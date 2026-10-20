<?php
// File: admin/dashboard.php - Trang tong quan quan tri
require_once "../config/database.php";
require_once "../includes/auth.php";
require_once "../includes/functions.php";
requireAdmin();
define("PAGE_TITLE", "Dashboard");

// Thong ke tong quan
$tongPhong      = $pdo->query("SELECT COUNT(*) FROM rooms")->fetchColumn();
$phongTrong     = $pdo->query("SELECT COUNT(*) FROM rooms WHERE trang_thai='trong'")->fetchColumn();
$phongDangThue  = $pdo->query("SELECT COUNT(*) FROM rooms WHERE trang_thai='dang_thue'")->fetchColumn();
$tongNguoiThue  = $pdo->query("SELECT COUNT(*) FROM tenants WHERE trang_thai='dang_thue'")->fetchColumn();

// Doanh thu thang nay
$thangNay = date("n"); $namNay = date("Y");
$dtThangNay = $pdo->prepare("SELECT COALESCE(SUM(so_tien),0) FROM payments WHERE MONTH(ngay_thanh_toan)=? AND YEAR(ngay_thanh_toan)=?");
$dtThangNay->execute([$thangNay, $namNay]);
$dtThangNay = (float)$dtThangNay->fetchColumn();

// Hoa don chua thanh toan
$hdChuaTT = $pdo->query("SELECT COUNT(*),COALESCE(SUM(tong_tien),0) FROM invoices WHERE trang_thai IN ('chua_thanh_toan','qua_han')")->fetch(PDO::FETCH_NUM);

// Su co chua xu ly
$scChuaXL = $pdo->query("SELECT COUNT(*) FROM maintenance_requests WHERE trang_thai IN ('moi_gui','da_tiep_nhan','dang_xu_ly')")->fetchColumn();

// Hop dong sap het han (30 ngay)
$hdSapHetHan = $pdo->query("SELECT COUNT(*) FROM contracts WHERE trang_thai IN ('hieu_luc','sap_het_han') AND ngay_ket_thuc BETWEEN CURDATE() AND DATE_ADD(CURDATE(),INTERVAL 30 DAY)")->fetchColumn();

// Doanh thu 6 thang gan nhat
$dtSauThang = [];
for ($i = 5; $i >= 0; $i--) {
    $d = new DateTime();
    $d->modify("-$i months");
    $m = (int)$d->format("n"); $y = (int)$d->format("Y");
    $s = $pdo->prepare("SELECT COALESCE(SUM(so_tien),0) FROM payments WHERE MONTH(ngay_thanh_toan)=? AND YEAR(ngay_thanh_toan)=?");
    $s->execute([$m, $y]);
    $dtSauThang[] = ["label"=>"T$m/$y", "value"=>(float)$s->fetchColumn()];
}

// Phong theo trang thai
$phongSuaChua = $pdo->query("SELECT COUNT(*) FROM rooms WHERE trang_thai='dang_sua_chua'")->fetchColumn();

// Hoa don gan day
$recentHD = $pdo->query("SELECT i.*,t.ho_ten,r.ma_phong FROM invoices i JOIN tenants t ON i.tenant_id=t.id JOIN rooms r ON i.room_id=r.id ORDER BY i.ngay_tao DESC LIMIT 8")->fetchAll();

// Su co moi
$recentSC = $pdo->query("SELECT m.*,r.ma_phong,t.ho_ten FROM maintenance_requests m JOIN rooms r ON m.room_id=r.id JOIN tenants t ON m.tenant_id=t.id WHERE m.trang_thai IN ('moi_gui','da_tiep_nhan') ORDER BY m.ngay_tao DESC LIMIT 5")->fetchAll();

$chartLabels = json_encode(array_column($dtSauThang, "label"));
$chartValues = json_encode(array_column($dtSauThang, "value"));

require_once "../includes/header.php";
?>

<?php echo showFlash(); ?>

<!-- Stat Cards -->
<div class="row g-4 mb-4">
  <div class="col-6 col-md-3">
    <div class="stat-card">
      <div class="stat-icon bg-primary bg-opacity-10"><i class="fas fa-door-open text-primary"></i></div>
      <div class="stat-value"><?php echo $tongPhong; ?></div>
      <div class="stat-label">Tổng Số Phòng</div>
      <div class="stat-sub">Trống: <?php echo $phongTrong; ?> | Đang thuê: <?php echo $phongDangThue; ?></div>
    </div>
  </div>
  <div class="col-6 col-md-3">
    <div class="stat-card">
      <div class="stat-icon bg-success bg-opacity-10"><i class="fas fa-money-bill-wave text-success"></i></div>
      <div class="stat-value text-success"><?php echo number_format($dtThangNay/1000000, 1); ?>M</div>
      <div class="stat-label">Doanh Thu Tháng Này</div>
      <div class="stat-sub"><?php echo number_format($dtThangNay, 0, ",", "."); ?>đ</div>
    </div>
  </div>
  <div class="col-6 col-md-3">
    <div class="stat-card">
      <div class="stat-icon bg-danger bg-opacity-10"><i class="fas fa-receipt text-danger"></i></div>
      <div class="stat-value text-danger"><?php echo $hdChuaTT[0]; ?></div>
      <div class="stat-label">Hóa Đơn Chưa TT</div>
      <div class="stat-sub"><?php echo number_format($hdChuaTT[1]/1000000, 1); ?>M đồng</div>
    </div>
  </div>
  <div class="col-6 col-md-3">
    <div class="stat-card">
      <div class="stat-icon bg-warning bg-opacity-10"><i class="fas fa-tools text-warning"></i></div>
      <div class="stat-value text-warning"><?php echo $scChuaXL; ?></div>
      <div class="stat-label">Sự Cố Chờ Xử Lý</div>
      <div class="stat-sub">Hợp đồng sắp hết: <?php echo $hdSapHetHan; ?></div>
    </div>
  </div>
</div>

<!-- Trang thai phong -->
<div class="row g-4 mb-4">
  <div class="col-md-4">
    <div class="card">
      <div class="card-header"><span class="card-title"><i class="fas fa-building me-2 text-primary"></i>Tình Trạng Phòng</span></div>
      <div class="card-body">
        <div style="height:200px"><canvas id="chartPhong"></canvas></div>
        <div class="row text-center mt-3">
          <div class="col-4">
            <div class="fw-bold text-success fs-5"><?php echo $phongDangThue; ?></div>
            <div class="small text-muted">Đang thuê</div>
          </div>
          <div class="col-4">
            <div class="fw-bold text-info fs-5"><?php echo $phongTrong; ?></div>
            <div class="small text-muted">Còn trống</div>
          </div>
          <div class="col-4">
            <div class="fw-bold text-warning fs-5"><?php echo $phongSuaChua; ?></div>
            <div class="small text-muted">Sửa chữa</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="col-md-8">
    <div class="card">
      <div class="card-header"><span class="card-title"><i class="fas fa-chart-bar me-2 text-primary"></i>Doanh Thu 6 Tháng Gần Nhất</span></div>
      <div class="card-body"><div style="height:230px"><canvas id="chartDT"></canvas></div></div>
    </div>
  </div>
</div>

<div class="row g-4">
  <!-- Hoa don gan day -->
  <div class="col-lg-7">
    <div class="card">
      <div class="card-header d-flex justify-content-between align-items-center">
        <span class="card-title"><i class="fas fa-receipt me-2"></i>Hóa Đơn Gần Đây</span>
        <a href="hoa_don.php" class="btn btn-sm btn-outline-primary">Xem tất cả</a>
      </div>
      <div class="card-body p-0">
        <table class="table table-hover table-sm mb-0">
          <thead><tr><th>Mã HD</th><th>Khách</th><th>Phòng</th><th>Tổng Tiền</th><th>Trạng Thái</th></tr></thead>
          <tbody>
            <?php foreach ($recentHD as $hd): ?>
            <tr>
              <td class="small fw-bold"><?php echo htmlspecialchars($hd["ma_hoa_don"]); ?></td>
              <td class="small"><?php echo htmlspecialchars($hd["ho_ten"]); ?></td>
              <td><span class="badge bg-secondary"><?php echo htmlspecialchars($hd["ma_phong"]); ?></span></td>
              <td class="fw-bold small"><?php echo number_format($hd["tong_tien"], 0, ",", "."); ?>đ</td>
              <td><?php echo getStatusBadge($hd["trang_thai"]); ?></td>
            </tr>
            <?php endforeach; ?>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Su co moi -->
  <div class="col-lg-5">
    <div class="card">
      <div class="card-header d-flex justify-content-between align-items-center">
        <span class="card-title"><i class="fas fa-tools me-2 text-warning"></i>Sự Cố Mới</span>
        <a href="su_co.php" class="btn btn-sm btn-outline-warning">Xem tất cả</a>
      </div>
      <div class="card-body p-0">
        <?php if (empty($recentSC)): ?>
        <div class="empty-state"><i class="fas fa-check-circle text-success"></i><p>Không có sự cố mới!</p></div>
        <?php else: ?>
        <ul class="list-group list-group-flush">
          <?php foreach ($recentSC as $sc): ?>
          <li class="list-group-item">
            <div class="d-flex justify-content-between align-items-start">
              <div>
                <div class="fw-semibold small"><?php echo htmlspecialchars($sc["tieu_de"]); ?></div>
                <div class="text-muted small"><?php echo htmlspecialchars($sc["ho_ten"]); ?> - Phòng <?php echo htmlspecialchars($sc["ma_phong"]); ?></div>
              </div>
              <?php echo getStatusBadge($sc["muc_do"]); ?>
            </div>
          </li>
          <?php endforeach; ?>
        </ul>
        <?php endif; ?>
      </div>
    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script>
new Chart(document.getElementById("chartPhong"), {
  type: "doughnut",
  data: {
    labels: ["Đang thuê", "Còn trống", "Sửa chữa"],
    datasets: [{ data: [<?php echo $phongDangThue; ?>, <?php echo $phongTrong; ?>, <?php echo $phongSuaChua; ?>], backgroundColor: ["#22c55e","#3b82f6","#f59e0b"], borderWidth: 0 }]
  },
  options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: "bottom" } } }
});
new Chart(document.getElementById("chartDT"), {
  type: "bar",
  data: {
    labels: <?php echo $chartLabels; ?>,
    datasets: [{ label: "Doanh thu (đ)", data: <?php echo $chartValues; ?>, backgroundColor: "rgba(37,99,235,0.7)", borderColor: "#2563eb", borderWidth: 2, borderRadius: 6 }]
  },
  options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { callback: v => (v/1000000).toFixed(1) + "M" } } } }
});
</script>
<?php require_once "../includes/footer.php"; ?>