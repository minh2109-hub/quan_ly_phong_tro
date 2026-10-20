<?php
// File: user/hoa_don.php - Xem hoa don
require_once "../config/database.php";
require_once "../includes/auth.php";
require_once "../includes/functions.php";
requireKhachThue();
define("PAGE_TITLE","Hoa Don Cua Toi");
$user = getCurrentUser(); $tid = (int)$user["tenant_id"];
$status = $_GET["status"] ?? "";
$page   = max(1,(int)($_GET["page"] ?? 1));
$perPage = 10;
$where = "WHERE i.tenant_id=?"; $params = [$tid];
if ($status) { $where .= " AND i.trang_thai=?"; $params[] = $status; }
$total = $pdo->prepare("SELECT COUNT(*) FROM invoices i $where");
$total->execute($params); $total = $total->fetchColumn();
$pagination = paginate($total,$page,$perPage);
$stmt = $pdo->prepare("SELECT i.*,r.ma_phong FROM invoices i JOIN rooms r ON i.room_id=r.id $where ORDER BY i.nam DESC,i.thang DESC LIMIT $perPage OFFSET {$pagination["offset"]}");
$stmt->execute($params); $invoices = $stmt->fetchAll();
// Tong chua thanh toan
$tongNo = $pdo->prepare("SELECT COALESCE(SUM(tong_tien),0) FROM invoices WHERE tenant_id=? AND trang_thai IN ('chua_thanh_toan','qua_han')");
$tongNo->execute([$tid]); $tongNo = $tongNo->fetchColumn();
require_once "../includes/header_user.php";
?>
<nav aria-label="breadcrumb"><ol class="breadcrumb"><li class="breadcrumb-item"><a href="dashboard.php">Trang Chu</a></li><li class="breadcrumb-item active">Hoa Don</li></ol></nav>
<?php if($tongNo > 0): ?>
<div class="alert alert-danger"><i class="fas fa-exclamation-circle me-2"></i>Ban con <strong><?= number_format($tongNo,0,",",".")  ?>d</strong> chua thanh toan. Vui long thanh toan dung han!</div>
<?php endif; ?>
<div class="card">
  <div class="card-header d-flex justify-content-between align-items-center flex-wrap gap-2">
    <span class="card-title"><i class="fas fa-receipt me-2 text-primary"></i>Hoa Don Cua Toi</span>
    <form method="GET" class="d-flex gap-2">
      <select class="form-select form-select-sm" name="status">
        <option value="">Tat ca</option>
        <option value="chua_thanh_toan" <?= $status==="chua_thanh_toan"?"selected":"" ?>>Chua TT</option>
        <option value="da_thanh_toan" <?= $status==="da_thanh_toan"?"selected":"" ?>>Da TT</option>
        <option value="qua_han" <?= $status==="qua_han"?"selected":"" ?>>Qua Han</option>
      </select>
      <button type="submit" class="btn btn-sm btn-primary">Loc</button>
    </form>
  </div>
  <div class="card-body p-0">
    <div class="table-responsive">
      <table class="table table-hover align-middle mb-0">
        <thead><tr><th>Ma HD</th><th>Thang/Nam</th><th>Tien Phong</th><th>Dien+Nuoc</th><th>Dich Vu</th><th>Tong Tien</th><th>Han TT</th><th>Trang Thai</th></tr></thead>
        <tbody>
          <?php if(empty($invoices)): ?>
          <tr><td colspan="8"><div class="empty-state"><i class="fas fa-receipt"></i><p>Khong co hoa don.</p></div></td></tr>
          <?php else: foreach($invoices as $inv): ?>
          <tr class="<?= $inv["trang_thai"]==="qua_han"?"table-danger":($inv["trang_thai"]==="chua_thanh_toan"?"table-warning":"") ?>">
            <td><small class="fw-bold"><?= e($inv["ma_hoa_don"]) ?></small></td>
            <td>T<?= $inv["thang"] ?>/<?= $inv["nam"] ?></td>
            <td><?= number_format($inv["tien_phong"],0,",",".")  ?>d</td>
            <td><?= number_format($inv["tien_dien"]+$inv["tien_nuoc"],0,",",".")  ?>d</td>
            <td><?= number_format($inv["tien_dich_vu"],0,",",".")  ?>d</td>
            <td class="fw-bold"><?= number_format($inv["tong_tien"],0,",",".")  ?>d</td>
            <td class="small"><?= formatDate($inv["han_thanh_toan"]) ?></td>
            <td><?= getStatusBadge($inv["trang_thai"]) ?></td>
          </tr>
          <?php endforeach; endif; ?>
        </tbody>
      </table>
    </div>
    <div class="p-3"><?= renderPagination($pagination,"hoa_don.php?status=".$status) ?></div>
  </div>
</div>
<?php require_once "../includes/footer_user.php"; ?>