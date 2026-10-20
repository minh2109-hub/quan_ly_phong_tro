<?php
// File: user/dien_nuoc.php - Xem lich su dien nuoc
require_once "../config/database.php";
require_once "../includes/auth.php";
require_once "../includes/functions.php";
requireKhachThue();
define("PAGE_TITLE","Dien Nuoc Cua Toi");
$user = getCurrentUser(); $tid = (int)$user["tenant_id"];

// Lay room_id cua nguoi thue
$t = $pdo->prepare("SELECT room_id FROM tenants WHERE id=?");
$t->execute([$tid]); $t = $t->fetch();
$roomId = (int)($t["room_id"] ?? 0);

$page    = max(1,(int)($_GET["page"] ?? 1));
$perPage = 12;
$total   = $roomId ? (int)$pdo->prepare("SELECT COUNT(*) FROM electric_water WHERE room_id=?")->execute([$roomId]) : 0;
if ($roomId) {
    $cnt = $pdo->prepare("SELECT COUNT(*) FROM electric_water WHERE room_id=?");
    $cnt->execute([$roomId]); $total = $cnt->fetchColumn();
}
$pagination = paginate($total,$page,$perPage);
$records = [];
if ($roomId) {
    $stmt = $pdo->prepare("SELECT *, (chi_so_dien_moi-chi_so_dien_cu) AS so_dien, (chi_so_nuoc_moi-chi_so_nuoc_cu) AS so_nuoc, (chi_so_dien_moi-chi_so_dien_cu)*don_gia_dien AS tien_dien, (chi_so_nuoc_moi-chi_so_nuoc_cu)*don_gia_nuoc AS tien_nuoc FROM electric_water WHERE room_id=? ORDER BY nam DESC,thang DESC LIMIT $perPage OFFSET {$pagination["offset"]}");
    $stmt->execute([$roomId]); $records = $stmt->fetchAll();
}
require_once "../includes/header_user.php";
?>
<nav aria-label="breadcrumb"><ol class="breadcrumb"><li class="breadcrumb-item"><a href="dashboard.php">Trang Chu</a></li><li class="breadcrumb-item active">Dien Nuoc</li></ol></nav>
<div class="card">
  <div class="card-header"><span class="card-title"><i class="fas fa-bolt me-2 text-warning"></i>Lich Su Dien Nuoc</span></div>
  <div class="card-body">
    <?php if(empty($records)): ?>
    <div class="empty-state"><i class="fas fa-bolt"></i><p>Chua co du lieu dien nuoc.</p></div>
    <?php else: ?>
    <div class="table-responsive">
      <table class="table table-hover align-middle">
        <thead>
          <tr>
            <th>Thang/Nam</th>
            <th class="text-center text-warning">So Dung Dien (kWh)</th>
            <th class="text-center text-warning">Don Gia Dien</th>
            <th class="text-center text-warning">Tien Dien</th>
            <th class="text-center text-info">So Dung Nuoc (m3)</th>
            <th class="text-center text-info">Don Gia Nuoc</th>
            <th class="text-center text-info">Tien Nuoc</th>
            <th class="text-center text-success">Tong</th>
          </tr>
        </thead>
        <tbody>
          <?php foreach($records as $r): ?>
          <tr>
            <td><strong>T<?= $r["thang"] ?>/<?= $r["nam"] ?></strong></td>
            <td class="text-center fw-bold text-warning"><?= number_format($r["so_dien"],1) ?></td>
            <td class="text-center"><?= number_format($r["don_gia_dien"],0,",",".")  ?>d</td>
            <td class="text-center fw-semibold"><?= number_format($r["tien_dien"],0,",",".")  ?>d</td>
            <td class="text-center fw-bold text-info"><?= number_format($r["so_nuoc"],1) ?></td>
            <td class="text-center"><?= number_format($r["don_gia_nuoc"],0,",",".")  ?>d</td>
            <td class="text-center fw-semibold"><?= number_format($r["tien_nuoc"],0,",",".")  ?>d</td>
            <td class="text-center fw-bold text-success"><?= number_format($r["tien_dien"]+$r["tien_nuoc"],0,",",".")  ?>d</td>
          </tr>
          <?php endforeach; ?>
        </tbody>
      </table>
    </div>
    <?= renderPagination($pagination,"dien_nuoc.php") ?>
    <?php endif; ?>
  </div>
</div>
<?php require_once "../includes/footer_user.php"; ?>