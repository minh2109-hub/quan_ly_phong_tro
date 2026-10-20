<?php
// File: admin/su_co.php - Quan ly su co / sua chua
require_once "../config/database.php";
require_once "../includes/auth.php";
require_once "../includes/functions.php";
requireAdmin();
define("PAGE_TITLE","Quan Ly Su Co / Sua Chua");

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $action  = $_POST["action"] ?? "";
    $id      = (int)($_POST["id"] ?? 0);
    $tt      = $_POST["trang_thai"] ?? "";
    $ghichu  = trim($_POST["ghi_chu_xu_ly"] ?? "");

    if ($action === "update_status" && $id) {
        $ngay_hoan = $tt === "hoan_thanh" ? date("Y-m-d H:i:s") : null;
        $pdo->prepare("UPDATE maintenance_requests SET trang_thai=?,ghi_chu_xu_ly=?,ngay_hoan_thanh=? WHERE id=?")->execute([$tt,$ghichu,$ngay_hoan,$id]);
        setFlash("success","Cap nhat trang thai thanh cong!");
    }
    header("Location: su_co.php"); exit();
}

if (isset($_GET["delete"])) {
    $pdo->prepare("DELETE FROM maintenance_requests WHERE id=?")->execute([(int)$_GET["delete"]]);
    setFlash("success","Da xoa!"); header("Location: su_co.php"); exit();
}

$search  = trim($_GET["search"] ?? "");
$status  = $_GET["status"] ?? "";
$mucdo   = $_GET["muc_do"] ?? "";
$page    = max(1,(int)($_GET["page"] ?? 1));
$perPage = 10;
$where   = "WHERE 1=1"; $params = [];
if ($search) { $where .= " AND (m.tieu_de LIKE ? OR t.ho_ten LIKE ? OR r.ma_phong LIKE ?)"; $params = ["%$search%","%$search%","%$search%"]; }
if ($status) { $where .= " AND m.trang_thai=?"; $params[] = $status; }
if ($mucdo)  { $where .= " AND m.muc_do=?"; $params[] = $mucdo; }

$total = $pdo->prepare("SELECT COUNT(*) FROM maintenance_requests m JOIN rooms r ON m.room_id=r.id JOIN tenants t ON m.tenant_id=t.id $where");
$total->execute($params); $total = $total->fetchColumn();
$pagination = paginate($total,$page,$perPage);
$stmt = $pdo->prepare("SELECT m.*,r.ma_phong,t.ho_ten FROM maintenance_requests m JOIN rooms r ON m.room_id=r.id JOIN tenants t ON m.tenant_id=t.id $where ORDER BY FIELD(m.trang_thai,'moi_gui','da_tiep_nhan','dang_xu_ly','hoan_thanh'),m.ngay_tao DESC LIMIT $perPage OFFSET {$pagination["offset"]}");
$stmt->execute($params);
$requests = $stmt->fetchAll();
$baseUrl = "su_co.php?" . http_build_query(array_filter(["search"=>$search,"status"=>$status,"muc_do"=>$mucdo]));

require_once "../includes/header.php";
?>
<nav aria-label="breadcrumb"><ol class="breadcrumb"><li class="breadcrumb-item"><a href="dashboard.php">Dashboard</a></li><li class="breadcrumb-item active">Su Co</li></ol></nav>
<?= showFlash() ?>
<div class="card">
  <div class="card-header"><span class="card-title"><i class="fas fa-tools me-2 text-primary"></i>Quan Ly Su Co / Yeu Cau Sua Chua</span></div>
  <div class="card-body">
    <form method="GET" class="row g-2 mb-3">
      <div class="col-md-4"><div class="search-bar"><i class="fas fa-search search-icon"></i><input type="text" class="form-control" name="search" value="<?= e($search) ?>" placeholder="Tim tieu de, ten, phong..."></div></div>
      <div class="col-md-2"><select class="form-select" name="status"><option value="">Tat ca TT</option><option value="moi_gui" <?= $status==="moi_gui"?"selected":"" ?>>Moi Gui</option><option value="da_tiep_nhan" <?= $status==="da_tiep_nhan"?"selected":"" ?>>Da Tiep Nhan</option><option value="dang_xu_ly" <?= $status==="dang_xu_ly"?"selected":"" ?>>Dang Xu Ly</option><option value="hoan_thanh" <?= $status==="hoan_thanh"?"selected":"" ?>>Hoan Thanh</option></select></div>
      <div class="col-md-2"><select class="form-select" name="muc_do"><option value="">Tat ca Muc Do</option><option value="thap" <?= $mucdo==="thap"?"selected":"" ?>>Thap</option><option value="trung_binh" <?= $mucdo==="trung_binh"?"selected":"" ?>>Trung Binh</option><option value="cao" <?= $mucdo==="cao"?"selected":"" ?>>Cao</option><option value="khan_cap" <?= $mucdo==="khan_cap"?"selected":"" ?>>Khan Cap</option></select></div>
      <div class="col-md-2"><button type="submit" class="btn btn-primary w-100">Tim</button></div>
      <div class="col-md-2"><a href="su_co.php" class="btn btn-secondary w-100">Dat Lai</a></div>
    </form>
    <div class="table-responsive">
      <table class="table table-hover align-middle">
        <thead><tr><th>Ma SC</th><th>Phong</th><th>Nguoi Gui</th><th>Tieu De</th><th>Muc Do</th><th>Trang Thai</th><th>Ngay Gui</th><th>Hanh Dong</th></tr></thead>
        <tbody>
          <?php if(empty($requests)): ?>
          <tr><td colspan="8"><div class="empty-state"><i class="fas fa-tools"></i><p>Khong co su co nao.</p></div></td></tr>
          <?php else: foreach($requests as $sc): ?>
          <tr>
            <td><strong class="text-primary small"><?= e($sc["ma_su_co"]) ?></strong></td>
            <td><span class="badge bg-info"><?= e($sc["ma_phong"]) ?></span></td>
            <td><?= e($sc["ho_ten"]) ?></td>
            <td style="max-width:200px">
              <strong><?= e($sc["tieu_de"]) ?></strong><br>
              <small class="text-muted" style="display:-webkit-box;-webkit-line-clamp:1;-webkit-box-orient:vertical;overflow:hidden"><?= e($sc["mo_ta"]) ?></small>
            </td>
            <td><?= getStatusBadge($sc["muc_do"]) ?></td>
            <td><?= getStatusBadge($sc["trang_thai"]) ?></td>
            <td class="small"><?= formatDate($sc["ngay_tao"]) ?></td>
            <td>
              <div class="btn-group btn-group-sm">
                <button class="btn btn-outline-primary" onclick="openUpdate(<?= htmlspecialchars(json_encode($sc)) ?>)" data-bs-toggle="modal" data-bs-target="#modalUpdate"><i class="fas fa-edit"></i></button>
                <a class="btn btn-outline-danger" href="?delete=<?= $sc["id"] ?>" onclick="return confirm('Xac nhan xoa?')"><i class="fas fa-trash"></i></a>
              </div>
            </td>
          </tr>
          <?php endforeach; endif; ?>
        </tbody>
      </table>
    </div>
    <div class="d-flex justify-content-between align-items-center mt-3">
      <small class="text-muted"><?= count($requests) ?>/<?= $total ?></small>
      <?= renderPagination($pagination,$baseUrl) ?>
    </div>
  </div>
</div>

<!-- Modal Cap Nhat Trang Thai -->
<div class="modal fade" id="modalUpdate" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <form method="POST">
        <div class="modal-header"><h5 class="modal-title">Cap Nhat Su Co</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
        <div class="modal-body">
          <input type="hidden" name="action" value="update_status"><input type="hidden" name="id" id="scId">
          <div class="mb-3">
            <p><strong id="scTitle"></strong></p>
            <p class="text-muted small" id="scMoTa"></p>
          </div>
          <div class="mb-3">
            <label class="form-label">Trang Thai Xu Ly</label>
            <select class="form-select" name="trang_thai" id="scTT">
              <option value="moi_gui">Moi Gui</option>
              <option value="da_tiep_nhan">Da Tiep Nhan</option>
              <option value="dang_xu_ly">Dang Xu Ly</option>
              <option value="hoan_thanh">Hoan Thanh</option>
            </select>
          </div>
          <div class="mb-3">
            <label class="form-label">Ghi Chu Xu Ly</label>
            <textarea class="form-control" name="ghi_chu_xu_ly" id="scGhiChu" rows="3" placeholder="Mo ta cach xu ly, ket qua..."></textarea>
          </div>
        </div>
        <div class="modal-footer"><button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Huy</button><button type="submit" class="btn btn-primary"><i class="fas fa-save me-1"></i>Cap Nhat</button></div>
      </form>
    </div>
  </div>
</div>
<script>
function openUpdate(sc){document.getElementById("scId").value=sc.id;document.getElementById("scTitle").textContent=sc.tieu_de;document.getElementById("scMoTa").textContent=sc.mo_ta;document.getElementById("scTT").value=sc.trang_thai;document.getElementById("scGhiChu").value=sc.ghi_chu_xu_ly||"";}
</script>
<?php require_once "../includes/footer.php"; ?>