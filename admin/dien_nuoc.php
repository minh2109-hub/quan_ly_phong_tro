<?php
// File: admin/dien_nuoc.php - Quan ly dien nuoc
require_once "../config/database.php";
require_once "../includes/auth.php";
require_once "../includes/functions.php";
requireAdmin();
define("PAGE_TITLE","Quan Ly Dien Nuoc");

$rooms = $pdo->query("SELECT id,ma_phong,ten_phong FROM rooms WHERE trang_thai='dang_thue' ORDER BY ma_phong")->fetchAll();
$my = getCurrentMonthYear();

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $action      = $_POST["action"] ?? "add";
    $room_id     = (int)$_POST["room_id"];
    $thang       = (int)$_POST["thang"];
    $nam         = (int)$_POST["nam"];
    $dien_cu     = (float)$_POST["chi_so_dien_cu"];
    $dien_moi    = (float)$_POST["chi_so_dien_moi"];
    $don_gia_dien= (float)$_POST["don_gia_dien"];
    $nuoc_cu     = (float)$_POST["chi_so_nuoc_cu"];
    $nuoc_moi    = (float)$_POST["chi_so_nuoc_moi"];
    $don_gia_nuoc= (float)$_POST["don_gia_nuoc"];
    $ghi_chu     = trim($_POST["ghi_chu"] ?? "");

    $err = "";
    if (!$room_id) $err = "Chon phong.";
    elseif ($dien_moi < $dien_cu) $err = "Chi so dien moi khong duoc nho hon chi so cu!";
    elseif ($nuoc_moi < $nuoc_cu) $err = "Chi so nuoc moi khong duoc nho hon chi so cu!";

    if ($err) { setFlash("danger",$err); }
    else {
        $data = [$room_id,$thang,$nam,$dien_cu,$dien_moi,$don_gia_dien,$nuoc_cu,$nuoc_moi,$don_gia_nuoc,$ghi_chu];
        if ($action === "add") {
            try {
                $pdo->prepare("INSERT INTO electric_water (room_id,thang,nam,chi_so_dien_cu,chi_so_dien_moi,don_gia_dien,chi_so_nuoc_cu,chi_so_nuoc_moi,don_gia_nuoc,ghi_chu) VALUES (?,?,?,?,?,?,?,?,?,?)")->execute($data);
                setFlash("success","Nhap dien nuoc thang $thang/$nam thanh cong!");
            } catch (PDOException $e) { setFlash("danger","Loi: Da co du lieu thang nay cho phong nay."); }
        } elseif ($action === "edit") {
            $id = (int)$_POST["id"];
            $data[] = $id;
            $pdo->prepare("UPDATE electric_water SET room_id=?,thang=?,nam=?,chi_so_dien_cu=?,chi_so_dien_moi=?,don_gia_dien=?,chi_so_nuoc_cu=?,chi_so_nuoc_moi=?,don_gia_nuoc=?,ghi_chu=? WHERE id=?")->execute($data);
            setFlash("success","Cap nhat thanh cong!");
        }
    }
    header("Location: dien_nuoc.php?thang=$thang&nam=$nam"); exit();
}

if (isset($_GET["delete"])) {
    $pdo->prepare("DELETE FROM electric_water WHERE id=?")->execute([(int)$_GET["delete"]]);
    setFlash("success","Da xoa!"); header("Location: dien_nuoc.php"); exit();
}

$filterThang = (int)($_GET["thang"] ?? $my["thang"]);
$filterNam   = (int)($_GET["nam"] ?? $my["nam"]);
$search      = trim($_GET["search"] ?? "");

$where = "WHERE ew.thang=? AND ew.nam=?"; $params = [$filterThang,$filterNam];
if ($search) { $where .= " AND (r.ma_phong LIKE ? OR r.ten_phong LIKE ?)"; $params = array_merge($params,["%$search%","%$search%"]); }

$data = $pdo->prepare("SELECT ew.*, r.ma_phong, r.ten_phong, (ew.chi_so_dien_moi-ew.chi_so_dien_cu) AS so_dien, (ew.chi_so_nuoc_moi-ew.chi_so_nuoc_cu) AS so_nuoc, ((ew.chi_so_dien_moi-ew.chi_so_dien_cu)*ew.don_gia_dien) AS tien_dien, ((ew.chi_so_nuoc_moi-ew.chi_so_nuoc_cu)*ew.don_gia_nuoc) AS tien_nuoc, ((ew.chi_so_dien_moi-ew.chi_so_dien_cu)*ew.don_gia_dien + (ew.chi_so_nuoc_moi-ew.chi_so_nuoc_cu)*ew.don_gia_nuoc) AS tong FROM electric_water ew JOIN rooms r ON ew.room_id=r.id $where ORDER BY r.ma_phong");
$data->execute($params);
$records = $data->fetchAll();

require_once "../includes/header.php";
?>
<nav aria-label="breadcrumb"><ol class="breadcrumb"><li class="breadcrumb-item"><a href="dashboard.php">Dashboard</a></li><li class="breadcrumb-item active">Dien Nuoc</li></ol></nav>
<?= showFlash() ?>

<div class="card mb-4">
  <div class="card-header d-flex flex-wrap gap-2 justify-content-between align-items-center">
    <span class="card-title"><i class="fas fa-bolt me-2 text-warning"></i>Chi So Dien Nuoc</span>
    <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#modalDN" onclick="resetDN()"><i class="fas fa-plus me-1"></i>Nhap Dien Nuoc</button>
  </div>
  <div class="card-body">
    <form method="GET" class="row g-2 mb-3">
      <div class="col-md-2"><select class="form-select" name="thang"><?php for($m=1;$m<=12;$m++): ?><option value="<?= $m ?>" <?= $filterThang==$m?"selected":"" ?>>Thang <?= $m ?></option><?php endfor; ?></select></div>
      <div class="col-md-2"><select class="form-select" name="nam"><?php for($y=2024;$y<=2027;$y++): ?><option value="<?= $y ?>" <?= $filterNam==$y?"selected":"" ?>><?= $y ?></option><?php endfor; ?></select></div>
      <div class="col-md-4"><div class="search-bar"><i class="fas fa-search search-icon"></i><input type="text" class="form-control" name="search" value="<?= e($search) ?>" placeholder="Tim phong..."></div></div>
      <div class="col-md-2"><button type="submit" class="btn btn-primary w-100">Tim</button></div>
      <div class="col-md-2"><a href="dien_nuoc.php" class="btn btn-secondary w-100">Dat Lai</a></div>
    </form>

    <div class="table-responsive">
      <table class="table table-hover align-middle">
        <thead>
          <tr>
            <th>Phong</th>
            <th class="text-center text-warning"><i class="fas fa-bolt"></i> Dien Cu</th>
            <th class="text-center text-warning">Dien Moi</th>
            <th class="text-center text-warning">So Dung (kWh)</th>
            <th class="text-center text-warning">Don Gia</th>
            <th class="text-center text-warning">Tien Dien</th>
            <th class="text-center text-info"><i class="fas fa-tint"></i> Nuoc Cu</th>
            <th class="text-center text-info">Nuoc Moi</th>
            <th class="text-center text-info">So Dung (m3)</th>
            <th class="text-center text-info">Tien Nuoc</th>
            <th class="text-center text-success">Tong Cong</th>
            <th>Hanh Dong</th>
          </tr>
        </thead>
        <tbody>
          <?php if(empty($records)): ?>
          <tr><td colspan="12"><div class="empty-state"><i class="fas fa-bolt"></i><p>Chua co du lieu dien nuoc thang <?= $filterThang ?>/<?= $filterNam ?>.</p></div></td></tr>
          <?php else: ?>
          <?php $tDien=0;$tNuoc=0;$tTong=0; foreach($records as $r): $tDien+=$r["tien_dien"];$tNuoc+=$r["tien_nuoc"];$tTong+=$r["tong"]; ?>
          <tr>
            <td><strong class="text-primary"><?= e($r["ma_phong"]) ?></strong></td>
            <td class="text-center"><?= number_format($r["chi_so_dien_cu"],1) ?></td>
            <td class="text-center"><?= number_format($r["chi_so_dien_moi"],1) ?></td>
            <td class="text-center fw-bold text-warning"><?= number_format($r["so_dien"],1) ?></td>
            <td class="text-center"><?= number_format($r["don_gia_dien"],0,",",".")  ?></td>
            <td class="text-center fw-semibold"><?= number_format($r["tien_dien"],0,",",".")  ?>d</td>
            <td class="text-center"><?= number_format($r["chi_so_nuoc_cu"],1) ?></td>
            <td class="text-center"><?= number_format($r["chi_so_nuoc_moi"],1) ?></td>
            <td class="text-center fw-bold text-info"><?= number_format($r["so_nuoc"],1) ?></td>
            <td class="text-center fw-semibold"><?= number_format($r["tien_nuoc"],0,",",".")  ?>d</td>
            <td class="text-center fw-bold text-success"><?= number_format($r["tong"],0,",",".")  ?>d</td>
            <td>
              <div class="btn-group btn-group-sm">
                <button class="btn btn-outline-primary" onclick="editDN(<?= htmlspecialchars(json_encode($r)) ?>)" data-bs-toggle="modal" data-bs-target="#modalDN"><i class="fas fa-edit"></i></button>
                <a class="btn btn-outline-danger" href="?delete=<?= $r["id"] ?>&thang=<?= $filterThang ?>&nam=<?= $filterNam ?>" onclick="return confirm('Xac nhan xoa?')"><i class="fas fa-trash"></i></a>
              </div>
            </td>
          </tr>
          <?php endforeach; ?>
          <tr class="table-active fw-bold">
            <td colspan="5" class="text-end">Tong Cong:</td>
            <td class="text-center"><?= number_format($tDien,0,",",".")  ?>d</td>
            <td colspan="3"></td>
            <td class="text-center"><?= number_format($tNuoc,0,",",".")  ?>d</td>
            <td class="text-center text-success"><?= number_format($tTong,0,",",".")  ?>d</td>
            <td></td>
          </tr>
          <?php endif; ?>
        </tbody>
      </table>
    </div>
  </div>
</div>

<!-- Modal -->
<div class="modal fade" id="modalDN" tabindex="-1">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <form method="POST" id="formDN">
        <div class="modal-header"><h5 class="modal-title" id="dnTitle">Nhap Chi So Dien Nuoc</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
        <div class="modal-body">
          <input type="hidden" name="action" id="dnAction" value="add"><input type="hidden" name="id" id="dnId">
          <div class="row g-3">
            <div class="col-md-4"><label class="form-label">Phong *</label><select class="form-select" name="room_id" id="dn_room" required><option value="">-- Chon phong --</option><?php foreach($rooms as $r): ?><option value="<?= $r["id"] ?>"><?= e($r["ma_phong"]." - ".$r["ten_phong"]) ?></option><?php endforeach; ?></select></div>
            <div class="col-md-4"><label class="form-label">Thang *</label><select class="form-select" name="thang" id="dn_thang"><?php for($m=1;$m<=12;$m++): ?><option value="<?= $m ?>" <?= $filterThang==$m?"selected":"" ?>>Thang <?= $m ?></option><?php endfor; ?></select></div>
            <div class="col-md-4"><label class="form-label">Nam *</label><input type="number" class="form-control" name="nam" id="dn_nam" value="<?= $filterNam ?>" required></div>

            <div class="col-12"><hr><h6 class="text-warning"><i class="fas fa-bolt me-2"></i>Dien</h6></div>
            <div class="col-md-4"><label class="form-label">Chi So Dien Cu</label><input type="number" step="0.1" class="form-control" name="chi_so_dien_cu" id="dn_dien_cu" value="0" oninput="calcDN()"></div>
            <div class="col-md-4"><label class="form-label">Chi So Dien Moi</label><input type="number" step="0.1" class="form-control" name="chi_so_dien_moi" id="dn_dien_moi" value="0" oninput="calcDN()"></div>
            <div class="col-md-4"><label class="form-label">Don Gia Dien (d/kWh)</label><input type="number" class="form-control" name="don_gia_dien" id="dn_don_gia_dien" value="3500" oninput="calcDN()"></div>
            <div class="col-md-6"><div class="alert alert-warning py-2 mb-0">So Dien: <strong id="so_dien">0</strong> kWh | Tien Dien: <strong id="tien_dien">0 d</strong></div></div>

            <div class="col-12"><hr><h6 class="text-info"><i class="fas fa-tint me-2"></i>Nuoc</h6></div>
            <div class="col-md-4"><label class="form-label">Chi So Nuoc Cu</label><input type="number" step="0.1" class="form-control" name="chi_so_nuoc_cu" id="dn_nuoc_cu" value="0" oninput="calcDN()"></div>
            <div class="col-md-4"><label class="form-label">Chi So Nuoc Moi</label><input type="number" step="0.1" class="form-control" name="chi_so_nuoc_moi" id="dn_nuoc_moi" value="0" oninput="calcDN()"></div>
            <div class="col-md-4"><label class="form-label">Don Gia Nuoc (d/m3)</label><input type="number" class="form-control" name="don_gia_nuoc" id="dn_don_gia_nuoc" value="15000" oninput="calcDN()"></div>
            <div class="col-md-6"><div class="alert alert-info py-2 mb-0">So Nuoc: <strong id="so_nuoc">0</strong> m3 | Tien Nuoc: <strong id="tien_nuoc">0 d</strong></div></div>
            <div class="col-md-6"><div class="alert alert-success py-2 mb-0">Tong Tien Dien Nuoc: <strong id="tong_dn">0 d</strong></div></div>

            <div class="col-12"><label class="form-label">Ghi Chu</label><textarea class="form-control" name="ghi_chu" id="dn_ghichu" rows="2"></textarea></div>
          </div>
        </div>
        <div class="modal-footer"><button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Huy</button><button type="submit" class="btn btn-primary"><i class="fas fa-save me-1"></i>Luu</button></div>
      </form>
    </div>
  </div>
</div>
<script>
function fmt(n){return new Intl.NumberFormat("vi-VN").format(Math.round(n))+" d";}
function calcDN(){
  const dc=parseFloat(document.getElementById("dn_dien_cu").value)||0;
  const dm=parseFloat(document.getElementById("dn_dien_moi").value)||0;
  const ddg=parseFloat(document.getElementById("dn_don_gia_dien").value)||0;
  const nc=parseFloat(document.getElementById("dn_nuoc_cu").value)||0;
  const nm=parseFloat(document.getElementById("dn_nuoc_moi").value)||0;
  const ndg=parseFloat(document.getElementById("dn_don_gia_nuoc").value)||0;
  const sd=Math.max(0,dm-dc); const td=sd*ddg;
  const sn=Math.max(0,nm-nc); const tn=sn*ndg;
  document.getElementById("so_dien").textContent=sd.toFixed(1);
  document.getElementById("tien_dien").textContent=fmt(td);
  document.getElementById("so_nuoc").textContent=sn.toFixed(1);
  document.getElementById("tien_nuoc").textContent=fmt(tn);
  document.getElementById("tong_dn").textContent=fmt(td+tn);
}
function resetDN(){document.getElementById("dnAction").value="add";document.getElementById("dnId").value="";document.getElementById("dnTitle").textContent="Nhap Chi So Dien Nuoc";document.getElementById("formDN").reset();document.getElementById("dn_don_gia_dien").value=3500;document.getElementById("dn_don_gia_nuoc").value=15000;calcDN();}
function editDN(r){document.getElementById("dnAction").value="edit";document.getElementById("dnId").value=r.id;document.getElementById("dnTitle").textContent="Sua Dien Nuoc: "+r.ma_phong+" T"+r.thang+"/"+r.nam;document.getElementById("dn_room").value=r.room_id;document.getElementById("dn_thang").value=r.thang;document.getElementById("dn_nam").value=r.nam;document.getElementById("dn_dien_cu").value=r.chi_so_dien_cu;document.getElementById("dn_dien_moi").value=r.chi_so_dien_moi;document.getElementById("dn_don_gia_dien").value=r.don_gia_dien;document.getElementById("dn_nuoc_cu").value=r.chi_so_nuoc_cu;document.getElementById("dn_nuoc_moi").value=r.chi_so_nuoc_moi;document.getElementById("dn_don_gia_nuoc").value=r.don_gia_nuoc;document.getElementById("dn_ghichu").value=r.ghi_chu||"";calcDN();}
</script>
<?php require_once "../includes/footer.php"; ?>