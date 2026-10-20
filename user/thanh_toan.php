<?php
// File: user/thanh_toan.php - Lich su thanh toan
require_once "../config/database.php";
require_once "../includes/auth.php";
require_once "../includes/functions.php";
requireKhachThue();
define("PAGE_TITLE","Lich Su Thanh Toan");
$user = getCurrentUser(); $tid = (int)$user["tenant_id"];
$page   = max(1,(int)($_GET["page"] ?? 1));
$perPage = 10;
$total  = $pdo->prepare("SELECT COUNT(*) FROM payments WHERE tenant_id=?");
$total->execute([$tid]); $total = $total->fetchColumn();
$pagination = paginate($total,$page,$perPage);
$stmt = $pdo->prepare("SELECT p.*,i.ma_hoa_don,i.thang,i.nam FROM payments p JOIN invoices i ON p.invoice_id=i.id WHERE p.tenant_id=? ORDER BY p.ngay_tao DESC LIMIT $perPage OFFSET {$pagination["offset"]}");
$stmt->execute([$tid]); $payments = $stmt->fetchAll();
$tongDaTT = $pdo->prepare("SELECT COALESCE(SUM(so_tien),0) FROM payments WHERE tenant_id=?");
$tongDaTT->execute([$tid]); $tongDaTT = $tongDaTT->fetchColumn();
require_once "../includes/header_user.php";
?>
<nav aria-label="breadcrumb"><ol class="breadcrumb"><li class="breadcrumb-item"><a href="dashboard.php">Trang Chu</a></li><li class="breadcrumb-item active">Lich Su Thanh Toan</li></ol></nav>
<div class="row g-4 mb-4">
  <div class="col-md-4">
    <div class="stat-card"><div class="stat-icon bg-success bg-opacity-10"><i class="fas fa-money-bill text-success"></i></div><div class="stat-value text-success"><?= number_format($tongDaTT,0,",",".")  ?>d</div><div class="stat-label">Tong Da Thanh Toan</div></div>
  </div>
  <div class="col-md-4">
    <div class="stat-card"><div class="stat-icon bg-primary bg-opacity-10"><i class="fas fa-receipt text-primary"></i></div><div class="stat-value"><?= $total ?></div><div class="stat-label">Tong Giao Dich</div></div>
  </div>
</div>
<div class="card">
  <div class="card-header"><span class="card-title"><i class="fas fa-money-bill-wave me-2 text-primary"></i>Lich Su Thanh Toan</span></div>
  <div class="card-body p-0">
    <div class="table-responsive">
      <table class="table table-hover align-middle mb-0">
        <thead><tr><th>Ma TT</th><th>Hoa Don</th><th>Thang/Nam</th><th>So Tien</th><th>Ngay TT</th><th>Phuong Thuc</th></tr></thead>
        <tbody>
          <?php if(empty($payments)): ?><tr><td colspan="6"><div class="empty-state"><i class="fas fa-money-bill-wave"></i><p>Chua co lich su thanh toan.</p></div></td></tr>
          <?php else: foreach($payments as $p): ?>
          <tr>
            <td><strong class="text-success small"><?= e($p["ma_thanh_toan"]) ?></strong></td>
            <td class="small"><?= e($p["ma_hoa_don"]) ?></td>
            <td>T<?= $p["thang"] ?>/<?= $p["nam"] ?></td>
            <td class="fw-bold text-success"><?= number_format($p["so_tien"],0,",",".")  ?>d</td>
            <td><?= formatDate($p["ngay_thanh_toan"]) ?></td>
            <td><?= $p["phuong_thuc"]==="tien_mat"?"<span class=\"badge bg-warning text-dark\">Tien Mat</span>":"<span class=\"badge bg-info\">Chuyen Khoan</span>" ?></td>
          </tr>
          <?php endforeach; endif; ?>
        </tbody>
      </table>
    </div>
    <div class="p-3"><?= renderPagination($pagination,"thanh_toan.php") ?></div>
  </div>
</div>
<?php require_once "../includes/footer_user.php"; ?>