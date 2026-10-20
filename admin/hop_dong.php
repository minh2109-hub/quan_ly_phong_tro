<?php
// File: admin/hop_dong.php - Quan ly hop dong
require_once "../config/database.php";
require_once "../includes/auth.php";
require_once "../includes/functions.php";
requireAdmin();
define("PAGE_TITLE","Quan Ly Hop Dong");

$tenants = $pdo->query("SELECT id,ho_ten,so_dien_thoai FROM tenants WHERE trang_thai='dang_thue' ORDER BY ho_ten")->fetchAll();
$rooms   = $pdo->query("SELECT id,ma_phong,ten_phong FROM rooms ORDER BY ma_phong")->fetchAll();

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $action   = $_POST["action"] ?? "";
    $ma_hd    = trim($_POST["ma_hop_dong"] ?? "");
    $t_id     = (int)$_POST["tenant_id"];
    $r_id     = (int)$_POST["room_id"];
    $ngay_bd  = $_POST["ngay_bat_dau"];
    $ngay_kt  = $_POST["ngay_ket_thuc"];
    $gia_thue = (float)$_POST["gia_thue"];
    $tien_coc = (float)($_POST["tien_coc"] ?? 0);
    $chu_ky   = $_POST["chu_ky_thanh_toan"] ?? "thang";
    $trang_thai = $_POST["trang_thai"] ?? "hieu_luc";
    $noi_dung = trim($_POST["noi_dung"] ?? "");
    $ghi_chu  = trim($_POST["ghi_chu"] ?? "");

    if (!$t_id || !$r_id || !$ngay_bd || !$ngay_kt || $gia_thue <= 0) {
        setFlash("danger","Vui long nhap day du cac truong bat buoc.");
    } else {
        $data = [$ma_hd,$t_id,$r_id,$ngay_bd,$ngay_kt,$gia_thue,$tien_coc,$chu_ky,$trang_thai,$noi_dung,$ghi_chu];
        if ($action === "add") {
            if (empty($ma_hd)) $ma_hd = generateCode("HD",$pdo,"contracts","ma_hop_dong");
            $data[0] = $ma_hd;
            try {
                $pdo->prepare("INSERT INTO contracts (ma_hop_dong,tenant_id,room_id,ngay_bat_dau,ngay_ket_thuc,gia_thue,tien_coc,chu_ky_thanh_toan,trang_thai,noi_dung,ghi_chu) VALUES (?,?,?,?,?,?,?,?,?,?,?)")->execute($data);
                setFlash("success","Tao hop dong thanh cong!");
            } catch (PDOException $e) { setFlash("danger","Loi: ".$e->getMessage()); }
        } elseif ($action === "edit") {
            $id = (int)$_POST["id"];
            $data[] = $id;
            try {
                $pdo->prepare("UPDATE contracts SET ma_hop_dong=?,tenant_id=?,room_id=?,ngay_bat_dau=?,ngay_ket_thuc=?,gia_thue=?,tien_coc=?,chu_ky_thanh_toan=?,trang_thai=?,noi_dung=?,ghi_chu=? WHERE id=?")->execute($data);
                setFlash("success","Cap nhat hop dong thanh cong!");
            } catch (PDOException $e) { setFlash("danger","Loi: ".$e->getMessage()); }
        } elseif ($action === "thanh_ly") {
            $id = (int)$_POST["id"];
            $pdo->prepare("UPDATE contracts SET trang_thai='thanh_ly' WHERE id=?")->execute([$id]);
            setFlash("success","Da thanh ly hop dong!");
        }
    }
    header("Location: hop_dong.php"); exit();
}

if (isset($_GET["delete"])) {
    try { $pdo->prepare("DELETE FROM contracts WHERE id=?")->execute([(int)$_GET["delete"]]); setFlash("success","Da xoa!"); }
    catch (PDOException $e) { setFlash("danger","Khong the xoa hop dong."); }
    header("Location: hop_dong.php"); exit();
}

// Auto cap nhat trang thai
$pdo->exec("UPDATE contracts SET trang_thai='het_han' WHERE trang_thai='hieu_luc' AND ngay_ket_thuc < CURDATE()");
$pdo->exec("UPDATE contracts SET trang_thai='sap_het_han' WHERE trang_thai='hieu_luc' AND ngay_ket_thuc BETWEEN CURDATE() AND DATE_ADD(CURDATE(),INTERVAL 30 DAY)");

$search = trim($_GET["search"] ?? "");
$status = $_GET["status"] ?? "";
$page   = max(1,(int)($_GET["page"] ?? 1));
$perPage = 10;
$where = "WHERE 1=1"; $params = [];
if ($search) { $where .= " AND (c.ma_hop_dong LIKE ? OR t.ho_ten LIKE ? OR r.ma_phong LIKE ?)"; $params = ["%$search%","%$search%","%$search%"]; }
if ($status) { $where .= " AND c.trang_thai=?"; $params[] = $status; }
$total = $pdo->prepare("SELECT COUNT(*) FROM contracts c JOIN tenants t ON c.tenant_id=t.id JOIN rooms r ON c.room_id=r.id $where");
$total->execute($params); $total = $total->fetchColumn();
$pagination = paginate($total,$page,$perPage);
$stmt = $pdo->prepare("SELECT c.*,t.ho_ten,t.so_dien_thoai,r.ma_phong,r.ten_phong FROM contracts c JOIN tenants t ON c.tenant_id=t.id JOIN rooms r ON c.room_id=r.id $where ORDER BY c.ngay_tao DESC LIMIT $perPage OFFSET {$pagination["offset"]}");
$stmt->execute($params);
$contracts = $stmt->fetchAll();
$baseUrl = "hop_dong.php?" . http_build_query(array_filter(["search"=>$search,"status"=>$status]));

require_once "../includes/header.php";
?>
<nav aria-label="breadcrumb"><ol class="breadcrumb"><li class="breadcrumb-item"><a href="dashboard.php">Dashboard</a></li><li class="breadcrumb-item active">Hop Dong</li></ol></nav>
<?= showFlash() ?>
<div class="card">
  <div class="card-header d-flex flex-wrap gap-2 justify-content-between align-items-center">
    <span class="card-title"><i class="fas fa-file-contract me-2 text-primary"></i>Quan Ly Hop Dong</span>
    <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#modalHD" onclick="resetHD()"><i class="fas fa-plus me-1"></i>Tao Hop Dong</button>
  </div>
  <div class="card-body">
    <form method="GET" class="row g-2 mb-3">
      <div class="col-md-5"><div class="search-bar"><i class="fas fa-search search-icon"></i><input type="text" class="form-control" name="search" value="<?= e($search) ?>" placeholder="Tim ma HD, ten, phong..."></div></div>
      <div class="col-md-3"><select class="form-select" name="status"><option value="">-- Tat ca --</option><option value="hieu_luc" <?= $status==="hieu_luc"?"selected":"" ?>>Hieu Luc</option><option value="sap_het_han" <?= $status==="sap_het_han"?"selected":"" ?>>Sap Het Han</option><option value="het_han" <?= $status==="het_han"?"selected":"" ?>>Het Han</option><option value="thanh_ly" <?= $status==="thanh_ly"?"selected":"" ?>>Thanh Ly</option></select></div>
      <div class="col-md-2"><button type="submit" class="btn btn-primary w-100">Tim</button></div>
      <div class="col-md-2"><a href="hop_dong.php" class="btn btn-secondary w-100">Dat Lai</a></div>
    </form>
    <div class="table-responsive">
      <table class="table table-hover align-middle">
        <thead><tr><th>Ma HD</th><th>Nguoi Thue</th><th>Phong</th><th>Ngay BD</th><th>Ngay KT</th><th>Gia Thue</th><th>Trang Thai</th><th>Hanh Dong</th></tr></thead>
        <tbody>
          <?php if(empty($contracts)): ?>
          <tr><td colspan="8"><div class="empty-state"><i class="fas fa-file-contract"></i><p>Khong co hop dong.</p></div></td></tr>
          <?php else: foreach($contracts as $c): ?>
          <tr>
            <td><strong class="text-primary"><?= e($c["ma_hop_dong"]) ?></strong></td>
            <td><?= e($c["ho_ten"]) ?><br><small class="text-muted"><?= e($c["so_dien_thoai"]) ?></small></td>
            <td><span class="badge bg-info"><?= e($c["ma_phong"]) ?></span></td>
            <td><?= formatDate($c["ngay_bat_dau"]) ?></td>
            <td><?= formatDate($c["ngay_ket_thuc"]) ?></td>
            <td class="fw-semibold"><?= number_format($c["gia_thue"],0,",",".")  ?>d</td>
            <td><?= getStatusBadge($c["trang_thai"]) ?></td>
            <td>
              <div class="btn-group btn-group-sm">
                <button class="btn btn-outline-primary" onclick="editHD(<?= htmlspecialchars(json_encode($c)) ?>)" data-bs-toggle="modal" data-bs-target="#modalHD"><i class="fas fa-edit"></i></button>
                <?php if($c["trang_thai"]!=="thanh_ly"): ?>
                <form method="POST" style="display:inline" onsubmit="return confirm('Thanh ly hop dong nay?')">
                  <input type="hidden" name="action" value="thanh_ly"><input type="hidden" name="id" value="<?= $c["id"] ?>">
                  <button type="submit" class="btn btn-outline-warning" title="Thanh Ly"><i class="fas fa-file-signature"></i></button>
                </form>
                <?php endif; ?>
                <a class="btn btn-outline-danger" href="?delete=<?= $c["id"] ?>" onclick="return confirm('Xac nhan xoa?')"><i class="fas fa-trash"></i></a>
              </div>
            </td>
          </tr>
          <?php endforeach; endif; ?>
        </tbody>
      </table>
    </div>
    <div class="d-flex justify-content-between align-items-center mt-3">
      <small class="text-muted"><?= count($contracts) ?>/<?= $total ?></small>
      <?= renderPagination($pagination,$baseUrl) ?>
    </div>
  </div>
</div>

<div class="modal fade" id="modalHD" tabindex="-1">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <form method="POST">
        <div class="modal-header"><h5 class="modal-title" id="hdTitle">Tao Hop Dong</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
        <div class="modal-body">
          <input type="hidden" name="action" id="hdAction" value="add"><input type="hidden" name="id" id="hdId">
          <div class="row g-3">
            <div class="col-md-4"><label class="form-label">Ma Hop Dong</label><input type="text" class="form-control" name="ma_hop_dong" id="hd_ma" placeholder="Tu dong tao..."></div>
            <div class="col-md-4"><label class="form-label">Nguoi Thue *</label><select class="form-select" name="tenant_id" id="hd_tenant" required><option value="">-- Chon --</option><?php foreach($tenants as $t): ?><option value="<?= $t["id"] ?>"><?= e($t["ho_ten"]) ?></option><?php endforeach; ?></select></div>
            <div class="col-md-4"><label class="form-label">Phong *</label><select class="form-select" name="room_id" id="hd_room" required><option value="">-- Chon --</option><?php foreach($rooms as $r): ?><option value="<?= $r["id"] ?>"><?= e($r["ma_phong"]." - ".$r["ten_phong"]) ?></option><?php endforeach; ?></select></div>
            <div class="col-md-3"><label class="form-label">Ngay BD *</label><input type="date" class="form-control" name="ngay_bat_dau" id="hd_bd" required></div>
            <div class="col-md-3"><label class="form-label">Ngay KT *</label><input type="date" class="form-control" name="ngay_ket_thuc" id="hd_kt" required></div>
            <div class="col-md-3"><label class="form-label">Gia Thue *</label><input type="number" class="form-control" name="gia_thue" id="hd_gia" required></div>
            <div class="col-md-3"><label class="form-label">Tien Coc</label><input type="number" class="form-control" name="tien_coc" id="hd_coc"></div>
            <div class="col-md-4"><label class="form-label">Chu Ky TT</label><select class="form-select" name="chu_ky_thanh_toan" id="hd_chuky"><option value="thang">Hang Thang</option><option value="quy">Hang Quy</option><option value="nam">Hang Nam</option></select></div>
            <div class="col-md-4"><label class="form-label">Trang Thai</label><select class="form-select" name="trang_thai" id="hd_tt"><option value="hieu_luc">Hieu Luc</option><option value="thanh_ly">Thanh Ly</option></select></div>
            <div class="col-12"><label class="form-label">Noi Dung HopDong</label><textarea class="form-control" name="noi_dung" id="hd_noidung" rows="2"></textarea></div>
            <div class="col-12"><label class="form-label">Ghi Chu</label><textarea class="form-control" name="ghi_chu" id="hd_ghichu" rows="2"></textarea></div>
          </div>
        </div>
        <div class="modal-footer"><button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Huy</button><button type="submit" class="btn btn-primary"><i class="fas fa-save me-1"></i>Luu</button></div>
      </form>
    </div>
  </div>
</div>
<script>
function resetHD(){document.getElementById("hdAction").value="add";document.getElementById("hdId").value="";document.getElementById("hdTitle").textContent="Tao Hop Dong";document.getElementById("modalHD").querySelector("form").reset();}
function editHD(c){document.getElementById("hdAction").value="edit";document.getElementById("hdId").value=c.id;document.getElementById("hdTitle").textContent="Sua HD: "+c.ma_hop_dong;document.getElementById("hd_ma").value=c.ma_hop_dong;document.getElementById("hd_tenant").value=c.tenant_id;document.getElementById("hd_room").value=c.room_id;document.getElementById("hd_bd").value=c.ngay_bat_dau;document.getElementById("hd_kt").value=c.ngay_ket_thuc;document.getElementById("hd_gia").value=c.gia_thue;document.getElementById("hd_coc").value=c.tien_coc||"";document.getElementById("hd_chuky").value=c.chu_ky_thanh_toan;document.getElementById("hd_tt").value=c.trang_thai;document.getElementById("hd_noidung").value=c.noi_dung||"";document.getElementById("hd_ghichu").value=c.ghi_chu||"";}
</script>
<?php require_once "../includes/footer.php"; ?>