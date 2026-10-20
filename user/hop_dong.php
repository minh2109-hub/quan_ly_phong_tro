<?php
// File: user/hop_dong.php - Xem hop dong
require_once "../config/database.php";
require_once "../includes/auth.php";
require_once "../includes/functions.php";
requireKhachThue();
define("PAGE_TITLE","Hop Dong Cua Toi");
$user = getCurrentUser(); $tid = (int)$user["tenant_id"];
$contracts = $pdo->prepare("SELECT c.*,r.ma_phong,r.ten_phong FROM contracts c JOIN rooms r ON c.room_id=r.id WHERE c.tenant_id=? ORDER BY c.ngay_tao DESC");
$contracts->execute([$tid]); $contracts = $contracts->fetchAll();
require_once "../includes/header_user.php";
?>
<nav aria-label="breadcrumb"><ol class="breadcrumb"><li class="breadcrumb-item"><a href="dashboard.php">Trang Chu</a></li><li class="breadcrumb-item active">Hop Dong</li></ol></nav>
<div class="card">
  <div class="card-header"><span class="card-title"><i class="fas fa-file-contract me-2 text-primary"></i>Hop Dong Cua Toi</span></div>
  <div class="card-body">
    <?php if(empty($contracts)): ?>
    <div class="empty-state"><i class="fas fa-file-contract"></i><p>Chua co hop dong nao.</p></div>
    <?php else: foreach($contracts as $c): ?>
    <div class="card mb-3 <?= $c["trang_thai"]==="hieu_luc"?"border-success":($c["trang_thai"]==="sap_het_han"?"border-warning":"") ?>">
      <div class="card-body">
        <div class="row">
          <div class="col-md-8">
            <h6 class="fw-bold text-primary"><i class="fas fa-file-contract me-2"></i><?= e($c["ma_hop_dong"]) ?></h6>
            <table class="table table-borderless table-sm mb-0">
              <tr><td width="35%"><strong>Phong:</strong></td><td><span class="badge bg-info"><?= e($c["ma_phong"]) ?></span> <?= e($c["ten_phong"]) ?></td></tr>
              <tr><td><strong>Ngay Bat Dau:</strong></td><td><?= formatDate($c["ngay_bat_dau"]) ?></td></tr>
              <tr><td><strong>Ngay Ket Thuc:</strong></td><td><?= formatDate($c["ngay_ket_thuc"]) ?></td></tr>
              <tr><td><strong>Gia Thue:</strong></td><td class="fw-bold text-primary"><?= number_format($c["gia_thue"],0,",",".")  ?>d/thang</td></tr>
              <tr><td><strong>Tien Coc:</strong></td><td><?= number_format($c["tien_coc"]?:0,0,",",".")  ?>d</td></tr>
              <tr><td><strong>Chu Ky TT:</strong></td><td><?= ucfirst($c["chu_ky_thanh_toan"]) ?></td></tr>
            </table>
          </div>
          <div class="col-md-4 text-end d-flex flex-column align-items-end justify-content-between">
            <div><?= getStatusBadge($c["trang_thai"]) ?></div>
            <?php
              $today = new DateTime(); $kt = new DateTime($c["ngay_ket_thuc"]);
              $diff = $today->diff($kt);
              if ($c["trang_thai"]==="hieu_luc"||$c["trang_thai"]==="sap_het_han"):
            ?>
            <div class="mt-2">
              <small class="text-muted">Con <?= $diff->days ?> ngay</small>
              <div class="progress mt-1" style="height:6px;width:120px">
                <?php $bd=new DateTime($c["ngay_bat_dau"]);$tong=$bd->diff($kt)->days;$qua=(new DateTime())->diff($bd)->days;$pct=min(100,round($qua/$tong*100)); ?>
                <div class="progress-bar bg-<?= $c["trang_thai"]==="sap_het_han"?"warning":"primary" ?>" style="width:<?= $pct ?>%"></div>
              </div>
            </div>
            <?php endif; ?>
          </div>
        </div>
        <?php if($c["noi_dung"]): ?><hr><p class="small text-muted mb-0"><strong>Noi Dung:</strong> <?= e($c["noi_dung"]) ?></p><?php endif; ?>
      </div>
    </div>
    <?php endforeach; endif; ?>
  </div>
</div>
<?php require_once "../includes/footer_user.php"; ?>