<?php
// File: admin/dich_vu.php - Quan ly dich vu
require_once "../config/database.php";
require_once "../includes/auth.php";
require_once "../includes/functions.php";
requireAdmin();
define("PAGE_TITLE","Quan Ly Dich Vu");

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $action    = $_POST["action"] ?? "";
    $ma_dv     = trim($_POST["ma_dich_vu"] ?? "");
    $ten_dv    = trim($_POST["ten_dich_vu"] ?? "");
    $don_gia   = (float)$_POST["don_gia"];
    $don_vi    = trim($_POST["don_vi"] ?? "thang");
    $mo_ta     = trim($_POST["mo_ta"] ?? "");
    $trang_thai= $_POST["trang_thai"] ?? "hoat_dong";

    if (empty($ten_dv) || $don_gia < 0) { setFlash("danger","Vui long nhap Ten dich vu va Don gia hop le."); }
    else {
        if ($action === "add") {
            if (empty($ma_dv)) $ma_dv = generateCode("DV",$pdo,"services","ma_dich_vu");
            try {
                $pdo->prepare("INSERT INTO services (ma_dich_vu,ten_dich_vu,don_gia,don_vi,mo_ta,trang_thai) VALUES (?,?,?,?,?,?)")->execute([$ma_dv,$ten_dv,$don_gia,$don_vi,$mo_ta,$trang_thai]);
                setFlash("success","Them dich vu thanh cong!");
            } catch (PDOException $e) { setFlash("danger","Loi: Ma dich vu da ton tai."); }
        } elseif ($action === "edit") {
            $id = (int)$_POST["id"];
            $pdo->prepare("UPDATE services SET ma_dich_vu=?,ten_dich_vu=?,don_gia=?,don_vi=?,mo_ta=?,trang_thai=? WHERE id=?")->execute([$ma_dv,$ten_dv,$don_gia,$don_vi,$mo_ta,$trang_thai,$id]);
            setFlash("success","Cap nhat thanh cong!");
        }
    }
    header("Location: dich_vu.php"); exit();
}
if (isset($_GET["delete"])) {
    try { $pdo->prepare("DELETE FROM services WHERE id=?")->execute([(int)$_GET["delete"]]); setFlash("success","Da xoa!"); }
    catch (PDOException $e) { setFlash("danger","Khong the xoa dich vu dang su dung."); }
    header("Location: dich_vu.php"); exit();
}

$search = trim($_GET["search"] ?? "");
$where = "WHERE 1=1"; $params = [];
if ($search) { $where .= " AND (ten_dich_vu LIKE ? OR ma_dich_vu LIKE ?)"; $params = ["%$search%","%$search%"]; }
$stmt = $pdo->prepare("SELECT * FROM services $where ORDER BY ma_dich_vu");
$stmt->execute($params);
$services = $stmt->fetchAll();

require_once "../includes/header.php";
?>
<nav aria-label="breadcrumb"><ol class="breadcrumb"><li class="breadcrumb-item"><a href="dashboard.php">Dashboard</a></li><li class="breadcrumb-item active">Dich Vu</li></ol></nav>
<?= showFlash() ?>
<div class="card">
  <div class="card-header d-flex flex-wrap gap-2 justify-content-between align-items-center">
    <span class="card-title"><i class="fas fa-concierge-bell me-2 text-primary"></i>Quan Ly Dich Vu</span>
    <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#modalDV" onclick="resetDV()"><i class="fas fa-plus me-1"></i>Them Dich Vu</button>
  </div>
  <div class="card-body">
    <form method="GET" class="row g-2 mb-3">
      <div class="col-md-6"><div class="search-bar"><i class="fas fa-search search-icon"></i><input type="text" class="form-control" name="search" value="<?= e($search) ?>" placeholder="Tim ten dich vu..."></div></div>
      <div class="col-md-2"><button type="submit" class="btn btn-primary w-100">Tim</button></div>
      <div class="col-md-2"><a href="dich_vu.php" class="btn btn-secondary w-100">Dat Lai</a></div>
    </form>
    <div class="table-responsive">
      <table class="table table-hover align-middle">
        <thead><tr><th>#</th><th>Ma DV</th><th>Ten Dich Vu</th><th>Don Gia</th><th>Don Vi</th><th>Mo Ta</th><th>Trang Thai</th><th>Hanh Dong</th></tr></thead>
        <tbody>
          <?php if(empty($services)): ?>
          <tr><td colspan="8"><div class="empty-state"><i class="fas fa-concierge-bell"></i><p>Chua co dich vu nao.</p></div></td></tr>
          <?php else: $i=1; foreach($services as $s): ?>
          <tr>
            <td><?= $i++ ?></td>
            <td><strong class="text-primary"><?= e($s["ma_dich_vu"]) ?></strong></td>
            <td><?= e($s["ten_dich_vu"]) ?></td>
            <td class="fw-semibold"><?= number_format($s["don_gia"],0,",",".")  ?>d</td>
            <td><?= e($s["don_vi"]) ?></td>
            <td><span class="text-muted small"><?= e($s["mo_ta"] ?? "-") ?></span></td>
            <td><?= getStatusBadge($s["trang_thai"]) ?></td>
            <td>
              <div class="btn-group btn-group-sm">
                <button class="btn btn-outline-primary" onclick="editDV(<?= htmlspecialchars(json_encode($s)) ?>)" data-bs-toggle="modal" data-bs-target="#modalDV"><i class="fas fa-edit"></i></button>
                <a class="btn btn-outline-danger" href="?delete=<?= $s["id"] ?>" onclick="return confirm('Xoa dich vu <?= e($s["ten_dich_vu"]) ?>?')"><i class="fas fa-trash"></i></a>
              </div>
            </td>
          </tr>
          <?php endforeach; endif; ?>
        </tbody>
      </table>
    </div>
  </div>
</div>

<div class="modal fade" id="modalDV" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <form method="POST">
        <div class="modal-header"><h5 class="modal-title" id="dvTitle">Them Dich Vu</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
        <div class="modal-body">
          <input type="hidden" name="action" id="dvAction" value="add"><input type="hidden" name="id" id="dvId">
          <div class="row g-3">
            <div class="col-md-6"><label class="form-label">Ma Dich Vu</label><input type="text" class="form-control" name="ma_dich_vu" id="dv_ma" placeholder="Tu dong..."></div>
            <div class="col-md-6"><label class="form-label">Ten Dich Vu *</label><input type="text" class="form-control" name="ten_dich_vu" id="dv_ten" required></div>
            <div class="col-md-6"><label class="form-label">Don Gia (d) *</label><input type="number" class="form-control" name="don_gia" id="dv_gia" required></div>
            <div class="col-md-6"><label class="form-label">Don Vi Tinh</label><input type="text" class="form-control" name="don_vi" id="dv_donvi" value="thang"></div>
            <div class="col-12"><label class="form-label">Mo Ta</label><textarea class="form-control" name="mo_ta" id="dv_mota" rows="2"></textarea></div>
            <div class="col-12"><label class="form-label">Trang Thai</label><select class="form-select" name="trang_thai" id="dv_tt"><option value="hoat_dong">Hoat Dong</option><option value="tam_ngung">Tam Ngung</option></select></div>
          </div>
        </div>
        <div class="modal-footer"><button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Huy</button><button type="submit" class="btn btn-primary"><i class="fas fa-save me-1"></i>Luu</button></div>
      </form>
    </div>
  </div>
</div>
<script>
function resetDV(){document.getElementById("dvAction").value="add";document.getElementById("dvId").value="";document.getElementById("dvTitle").textContent="Them Dich Vu";document.getElementById("modalDV").querySelector("form").reset();document.getElementById("dv_donvi").value="thang";}
function editDV(s){document.getElementById("dvAction").value="edit";document.getElementById("dvId").value=s.id;document.getElementById("dvTitle").textContent="Sua: "+s.ten_dich_vu;document.getElementById("dv_ma").value=s.ma_dich_vu;document.getElementById("dv_ten").value=s.ten_dich_vu;document.getElementById("dv_gia").value=s.don_gia;document.getElementById("dv_donvi").value=s.don_vi;document.getElementById("dv_mota").value=s.mo_ta||"";document.getElementById("dv_tt").value=s.trang_thai;}
</script>
<?php require_once "../includes/footer.php"; ?>