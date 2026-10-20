<?php
// File: user/phong.php - Xem thong tin phong cua toi
require_once "../config/database.php";
require_once "../includes/auth.php";
require_once "../includes/functions.php";
requireKhachThue();
define("PAGE_TITLE","Phong Cua Toi");
$user = getCurrentUser();
$tid  = (int)$user["tenant_id"];
$tenant = $pdo->prepare("SELECT t.*,r.ma_phong,r.ten_phong,r.gia_thue,r.dien_tich,r.so_nguoi_toi_da,r.loai_phong,r.tang,r.khu,r.tien_coc,r.mo_ta AS mo_ta_phong FROM tenants t LEFT JOIN rooms r ON t.room_id=r.id WHERE t.id=?");
$tenant->execute([$tid]); $tenant = $tenant->fetch();
require_once "../includes/header_user.php";
?>
<nav aria-label="breadcrumb"><ol class="breadcrumb"><li class="breadcrumb-item"><a href="dashboard.php">Trang Chu</a></li><li class="breadcrumb-item active">Phong Cua Toi</li></ol></nav>
<?php if(!$tenant || !$tenant["room_id"]): ?>
<div class="alert alert-info"><i class="fas fa-info-circle me-2"></i>Ban chua duoc gan phong. Vui long lien he chu tro.</div>
<?php else: ?>
<div class="row g-4">
  <div class="col-md-6">
    <div class="card h-100">
      <div class="card-header"><span class="card-title"><i class="fas fa-door-open me-2 text-primary"></i>Thong Tin Phong</span></div>
      <div class="card-body">
        <table class="table table-borderless mb-0">
          <tr><th width="45%">Ma Phong</th><td><span class="badge bg-primary fs-6"><?= e($tenant["ma_phong"]) ?></span></td></tr>
          <tr><th>Ten Phong</th><td><?= e($tenant["ten_phong"]) ?></td></tr>
          <tr><th>Loai Phong</th><td><?= e($tenant["loai_phong"]) ?></td></tr>
          <tr><th>Tang / Khu</th><td>Tang <?= $tenant["tang"] ?><?= $tenant["khu"] ? " / ".$tenant["khu"] : "" ?></td></tr>
          <tr><th>Dien Tich</th><td><?= $tenant["dien_tich"] ?> m2</td></tr>
          <tr><th>So Nguoi Toi Da</th><td><?= $tenant["so_nguoi_toi_da"] ?> nguoi</td></tr>
          <tr><th>Gia Thue</th><td class="fw-bold text-primary fs-5"><?= number_format($tenant["gia_thue"],0,",",".")  ?>d/thang</td></tr>
          <tr><th>Tien Coc</th><td><?= number_format($tenant["tien_coc"]?:0,0,",",".")  ?>d</td></tr>
          <?php if($tenant["mo_ta_phong"]): ?><tr><th>Mo Ta</th><td class="text-muted"><?= e($tenant["mo_ta_phong"]) ?></td></tr><?php endif; ?>
        </table>
      </div>
    </div>
  </div>
  <div class="col-md-6">
    <div class="card h-100">
      <div class="card-header"><span class="card-title"><i class="fas fa-user me-2 text-primary"></i>Thong Tin Ca Nhan</span></div>
      <div class="card-body">
        <table class="table table-borderless mb-0">
          <tr><th width="45%">Ho Ten</th><td><strong><?= e($tenant["ho_ten"]) ?></strong></td></tr>
          <tr><th>Ngay Sinh</th><td><?= formatDate($tenant["ngay_sinh"]) ?></td></tr>
          <tr><th>Gioi Tinh</th><td><?= e($tenant["gioi_tinh"]) ?></td></tr>
          <tr><th>So Dien Thoai</th><td><?= e($tenant["so_dien_thoai"]) ?></td></tr>
          <tr><th>Email</th><td><?= e($tenant["email"]??"-") ?></td></tr>
          <tr><th>So CMND</th><td><?= e($tenant["so_cmnd"]??"-") ?></td></tr>
          <tr><th>Dia Chi</th><td><?= e($tenant["dia_chi"]??"-") ?></td></tr>
          <tr><th>Nghe Nghiep</th><td><?= e($tenant["nghe_nghiep"]??"-") ?></td></tr>
          <tr><th>Ngay BD Thue</th><td><?= formatDate($tenant["ngay_bat_dau_thue"]) ?></td></tr>
          <tr><th>Trang Thai</th><td><?= getStatusBadge($tenant["trang_thai"]) ?></td></tr>
        </table>
      </div>
    </div>
  </div>
</div>
<?php endif; ?>
<?php require_once "../includes/footer_user.php"; ?>