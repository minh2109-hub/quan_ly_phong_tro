<?php
// File: admin/thong_ke.php - Thong ke bao cao
require_once "../config/database.php";
require_once "../includes/auth.php";
require_once "../includes/functions.php";
requireAdmin();
define("PAGE_TITLE","Thong Ke - Bao Cao");

$nam = (int)($_GET["nam"] ?? date("Y"));

// Doanh thu theo tung thang trong nam
$dtTheoThang = [];
for ($m=1;$m<=12;$m++) {
    $stmt = $pdo->prepare("SELECT COALESCE(SUM(so_tien),0) FROM payments WHERE MONTH(ngay_thanh_toan)=? AND YEAR(ngay_thanh_toan)=?");
    $stmt->execute([$m,$nam]);
    $dtTheoThang[$m] = (float)$stmt->fetchColumn();
}
$tongNam = array_sum($dtTheoThang);

// Tong quan
$tongPhong = $pdo->query("SELECT COUNT(*) FROM rooms")->fetchColumn();
$phongTrong = $pdo->query("SELECT COUNT(*) FROM rooms WHERE trang_thai='trong'")->fetchColumn();
$tongNguoiThue = $pdo->query("SELECT COUNT(*) FROM tenants WHERE trang_thai='dang_thue'")->fetchColumn();
$hdSapHetHan = $pdo->query("SELECT COUNT(*) FROM contracts WHERE trang_thai IN ('hieu_luc','sap_het_han') AND ngay_ket_thuc BETWEEN CURDATE() AND DATE_ADD(CURDATE(),INTERVAL 30 DAY)")->fetchColumn();
$hdChuaTT = $pdo->query("SELECT COUNT(*),COALESCE(SUM(tong_tien),0) FROM invoices WHERE trang_thai IN ('chua_thanh_toan','qua_han')")->fetch(PDO::FETCH_NUM);
$scChuaXL = $pdo->query("SELECT COUNT(*) FROM maintenance_requests WHERE trang_thai IN ('moi_gui','da_tiep_nhan','dang_xu_ly')")->fetchColumn();

// Top 5 phong co doanh thu cao nhat trong nam
$topPhong = $pdo->prepare("SELECT r.ma_phong, r.ten_phong, COUNT(DISTINCT i.id) as so_hd, SUM(p.so_tien) as doanh_thu FROM rooms r JOIN invoices i ON r.id=i.room_id JOIN payments p ON i.id=p.invoice_id WHERE YEAR(p.ngay_thanh_toan)=? GROUP BY r.id ORDER BY doanh_thu DESC LIMIT 5");
$topPhong->execute([$nam]);
$topPhong = $topPhong->fetchAll();

// Thong ke tien dien nuoc theo quy
$dienNuocTheoThang = [];
for ($m=1;$m<=12;$m++) {
    $stmt = $pdo->prepare("SELECT COALESCE(SUM((chi_so_dien_moi-chi_so_dien_cu)*don_gia_dien),0) as tien_dien, COALESCE(SUM((chi_so_nuoc_moi-chi_so_nuoc_cu)*don_gia_nuoc),0) as tien_nuoc FROM electric_water WHERE thang=? AND nam=?");
    $stmt->execute([$m,$nam]);
    $dienNuocTheoThang[$m] = $stmt->fetch();
}

$chartMonths = json_encode(array_map(fn($m)=>"T$m",$_=range(1,12)));
$chartRevenue = json_encode(array_values($dtTheoThang));
$chartDien = json_encode(array_map(fn($d)=>round($d["tien_dien"]),array_values($dienNuocTheoThang)));
$chartNuoc = json_encode(array_map(fn($d)=>round($d["tien_nuoc"]),array_values($dienNuocTheoThang)));

require_once "../includes/header.php";
?>
<nav aria-label="breadcrumb"><ol class="breadcrumb"><li class="breadcrumb-item"><a href="dashboard.php">Dashboard</a></li><li class="breadcrumb-item active">Thong Ke</li></ol></nav>

<div class="d-flex justify-content-between align-items-center mb-4">
  <div></div>
  <form method="GET" class="d-flex gap-2">
    <select class="form-select" name="nam" style="width:120px"><?php for($y=2024;$y<=2027;$y++): ?><option value="<?= $y ?>" <?= $nam==$y?"selected":"" ?>><?= $y ?></option><?php endfor; ?></select>
    <button type="submit" class="btn btn-primary">Xem</button>
  </form>
</div>

<!-- Stat Cards -->
<div class="row g-4 mb-4">
  <div class="col-6 col-md-3"><div class="stat-card"><div class="stat-icon bg-success bg-opacity-10"><i class="fas fa-money-bill text-success"></i></div><div class="stat-value text-success" style="font-size:1.2rem"><?= number_format($tongNam,0,",",".")  ?></div><div class="stat-label">Tong DT Nam <?= $nam ?> (d)</div></div></div>
  <div class="col-6 col-md-3"><div class="stat-card"><div class="stat-icon bg-primary bg-opacity-10"><i class="fas fa-door-open text-primary"></i></div><div class="stat-value"><?= $tongPhong ?></div><div class="stat-label">Tong Phong | Trong: <?= $phongTrong ?></div></div></div>
  <div class="col-6 col-md-3"><div class="stat-card"><div class="stat-icon bg-info bg-opacity-10"><i class="fas fa-users text-info"></i></div><div class="stat-value text-info"><?= $tongNguoiThue ?></div><div class="stat-label">Nguoi Dang Thue</div></div></div>
  <div class="col-6 col-md-3"><div class="stat-card"><div class="stat-icon bg-danger bg-opacity-10"><i class="fas fa-receipt text-danger"></i></div><div class="stat-value text-danger"><?= $hdChuaTT[0] ?></div><div class="stat-label">HD Chua TT (<?= number_format($hdChuaTT[1],0,",",".")  ?>d)</div></div></div>
</div>

<!-- Bieu do doanh thu -->
<div class="row g-4 mb-4">
  <div class="col-12">
    <div class="card">
      <div class="card-header"><span class="card-title"><i class="fas fa-chart-bar me-2 text-primary"></i>Doanh Thu Theo Thang Nam <?= $nam ?></span></div>
      <div class="card-body">
        <div style="height:300px"><canvas id="chartDT"></canvas></div>
        <div class="row mt-3">
          <?php for($m=1;$m<=12;$m++): ?>
          <div class="col-md-1 col-2 text-center mb-2">
            <div class="small text-muted">T<?= $m ?></div>
            <div class="fw-bold small"><?= $dtTheoThang[$m]>0?number_format($dtTheoThang[$m]/1000000,1)."M":"0" ?></div>
          </div>
          <?php endfor; ?>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="row g-4 mb-4">
  <!-- Bieu do dien nuoc -->
  <div class="col-lg-8">
    <div class="card">
      <div class="card-header"><span class="card-title"><i class="fas fa-bolt me-2 text-warning"></i>Tien Dien Nuoc Theo Thang</span></div>
      <div class="card-body"><div style="height:250px"><canvas id="chartDN"></canvas></div></div>
    </div>
  </div>

  <!-- Top phong -->
  <div class="col-lg-4">
    <div class="card h-100">
      <div class="card-header"><span class="card-title"><i class="fas fa-trophy me-2 text-warning"></i>Top Phong Doanh Thu Cao</span></div>
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table mb-0">
            <thead><tr><th>#</th><th>Phong</th><th>Doanh Thu</th></tr></thead>
            <tbody>
              <?php $rank=1; foreach($topPhong as $tp): ?>
              <tr>
                <td><span class="badge bg-<?= $rank===1?"warning":($rank===2?"secondary":"light text-dark") ?>"><?= $rank++ ?></span></td>
                <td><strong><?= e($tp["ma_phong"]) ?></strong></td>
                <td class="fw-bold"><?= number_format($tp["doanh_thu"]/1000000,1) ?>M</td>
              </tr>
              <?php endforeach; ?>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script>
new Chart(document.getElementById("chartDT"),{type:"bar",data:{labels:<?= $chartMonths ?>,datasets:[{label:"Doanh Thu (d)",data:<?= $chartRevenue ?>,backgroundColor:"rgba(37,99,235,0.7)",borderColor:"#2563eb",borderWidth:2,borderRadius:6}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,ticks:{callback:v=>new Intl.NumberFormat("vi-VN").format(v)}}}}});
new Chart(document.getElementById("chartDN"),{type:"line",data:{labels:<?= $chartMonths ?>,datasets:[{label:"Tien Dien",data:<?= $chartDien ?>,borderColor:"#f59e0b",backgroundColor:"rgba(245,158,11,0.1)",fill:true,tension:0.4},{label:"Tien Nuoc",data:<?= $chartNuoc ?>,borderColor:"#3b82f6",backgroundColor:"rgba(59,130,246,0.1)",fill:true,tension:0.4}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:true}},scales:{y:{beginAtZero:true}}}});
</script>
<?php require_once "../includes/footer.php"; ?>