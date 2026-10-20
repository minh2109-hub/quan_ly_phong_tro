<?php
// File: user/su_co.php - Bao su co
require_once "../config/database.php";
require_once "../includes/auth.php";
require_once "../includes/functions.php";
requireKhachThue();
define("PAGE_TITLE","Bao Cao Su Co");
$user = getCurrentUser(); $tid = (int)$user["tenant_id"];

// Lay phong cua nguoi thue
$t = $pdo->prepare("SELECT room_id FROM tenants WHERE id=?");
$t->execute([$tid]); $t = $t->fetch();
$roomId = (int)($t["room_id"] ?? 0);

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $tieu_de = trim($_POST["tieu_de"] ?? "");
    $mo_ta   = trim($_POST["mo_ta"] ?? "");
    $muc_do  = $_POST["muc_do"] ?? "trung_binh";

    if (empty($tieu_de) || !$roomId) { setFlash("danger","Vui long nhap tieu de su co."); }
    else {
        $ma = "SC" . date("YmdHis");
        $pdo->prepare("INSERT INTO maintenance_requests (ma_su_co,room_id,tenant_id,tieu_de,mo_ta,muc_do,trang_thai) VALUES (?,?,?,?,?,?,'moi_gui')")->execute([$ma,$roomId,$tid,$tieu_de,$mo_ta,$muc_do]);
        setFlash("success","Gui bao cao su co thanh cong! Ma: $ma");
    }
    header("Location: su_co.php"); exit();
}

$page   = max(1,(int)($_GET["page"] ?? 1));
$perPage = 10;
$total  = $pdo->prepare("SELECT COUNT(*) FROM maintenance_requests WHERE tenant_id=?");
$total->execute([$tid]); $total = $total->fetchColumn();
$pagination = paginate($total,$page,$perPage);
$stmt = $pdo->prepare("SELECT m.*,r.ma_phong FROM maintenance_requests m LEFT JOIN rooms r ON m.room_id=r.id WHERE m.tenant_id=? ORDER BY FIELD(m.trang_thai,'moi_gui','da_tiep_nhan','dang_xu_ly','hoan_thanh'),m.ngay_tao DESC LIMIT $perPage OFFSET {$pagination["offset"]}");
$stmt->execute([$tid]); $requests = $stmt->fetchAll();

require_once "../includes/header_user.php";
?>
<nav aria-label="breadcrumb"><ol class="breadcrumb"><li class="breadcrumb-item"><a href="dashboard.php">Trang Chu</a></li><li class="breadcrumb-item active">Bao Su Co</li></ol></nav>
<?= showFlash() ?>

<?php if($roomId): ?>
<!-- Form bao su co -->
<div class="card mb-4">
  <div class="card-header"><span class="card-title"><i class="fas fa-plus-circle me-2 text-primary"></i>Gui Bao Cao Su Co Moi</span></div>
  <div class="card-body">
    <form method="POST">
      <div class="row g-3">
        <div class="col-md-8"><label class="form-label">Tieu De Su Co *</label><input type="text" class="form-control" name="tieu_de" placeholder="Vi du: Ong nuoc bi re, den bi chay..." required></div>
        <div class="col-md-4"><label class="form-label">Muc Do Khan Cap</label>
          <select class="form-select" name="muc_do">
            <option value="thap">Thap - Khong gap</option>
            <option value="trung_binh" selected>Trung Binh - Can xu ly</option>
            <option value="cao">Cao - Gap</option>
            <option value="khan_cap">Khan Cap - Rat gap</option>
          </select>
        </div>
        <div class="col-12"><label class="form-label">Mo Ta Chi Tiet</label><textarea class="form-control" name="mo_ta" rows="3" placeholder="Mo ta chi tiet su co de chu tro co the xu ly hieu qua..."></textarea></div>
        <div class="col-12"><button type="submit" class="btn btn-primary"><i class="fas fa-paper-plane me-1"></i>Gui Bao Cao</button></div>
      </div>
    </form>
  </div>
</div>
<?php else: ?>
<div class="alert alert-warning"><i class="fas fa-exclamation-triangle me-2"></i>Ban chua duoc gan phong nen khong the bao su co. Lien he chu tro.</div>
<?php endif; ?>

<div class="card">
  <div class="card-header"><span class="card-title"><i class="fas fa-list me-2 text-primary"></i>Su Co Da Gui</span></div>
  <div class="card-body p-0">
    <div class="table-responsive">
      <table class="table table-hover align-middle mb-0">
        <thead><tr><th>Ma SC</th><th>Tieu De</th><th>Muc Do</th><th>Trang Thai</th><th>Ngay Gui</th><th>Ghi Chu XL</th></tr></thead>
        <tbody>
          <?php if(empty($requests)): ?><tr><td colspan="6"><div class="empty-state"><i class="fas fa-tools"></i><p>Chua gui su co nao.</p></div></td></tr>
          <?php else: foreach($requests as $sc): ?>
          <tr>
            <td><strong class="text-primary small"><?= e($sc["ma_su_co"]) ?></strong></td>
            <td>
              <strong><?= e($sc["tieu_de"]) ?></strong><br>
              <small class="text-muted"><?= e(mb_substr($sc["mo_ta"],0,60,"UTF-8")) ?>...</small>
            </td>
            <td><?= getStatusBadge($sc["muc_do"]) ?></td>
            <td><?= getStatusBadge($sc["trang_thai"]) ?></td>
            <td class="small"><?= formatDate($sc["ngay_tao"]) ?></td>
            <td class="small text-muted"><?= $sc["ghi_chu_xu_ly"] ? e(mb_substr($sc["ghi_chu_xu_ly"],0,80,"UTF-8")) : "-" ?></td>
          </tr>
          <?php endforeach; endif; ?>
        </tbody>
      </table>
    </div>
    <div class="p-3"><?= renderPagination($pagination,"su_co.php") ?></div>
  </div>
</div>
<?php require_once "../includes/footer_user.php"; ?>