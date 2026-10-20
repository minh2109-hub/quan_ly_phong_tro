<?php
// File: admin/hoa_don.php - Quan ly hoa don
require_once "../config/database.php";
require_once "../includes/auth.php";
require_once "../includes/functions.php";
requireAdmin();
define("PAGE_TITLE", "Quản Lý Hóa Đơn");

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $action    = $_POST["action"] ?? "";
    $room_id   = (int)($_POST["room_id"] ?? 0);
    $tenant_id = (int)($_POST["tenant_id"] ?? 0);
    $thang     = (int)($_POST["thang"] ?? date("n"));
    $nam       = (int)($_POST["nam"] ?? date("Y"));
    $tien_phong = (float)str_replace(",", "", $_POST["tien_phong"] ?? 0);
    $tien_dien  = (float)($_POST["tien_dien"] ?? 0);
    $tien_nuoc  = (float)($_POST["tien_nuoc"] ?? 0);
    $tien_dv    = (float)($_POST["tien_dich_vu"] ?? 0);
    $phi_khac   = (float)str_replace(",", "", $_POST["phi_khac"] ?? 0);
    $ghi_chu_pk = trim($_POST["ghi_chu_phi_khac"] ?? "");
    $tong_tien  = $tien_phong + $tien_dien + $tien_nuoc + $tien_dv + $phi_khac;
    $han_tt     = $_POST["han_thanh_toan"] ?? date("Y-m-d", strtotime("+7 days"));
    $tt         = $_POST["trang_thai"] ?? "chua_thanh_toan";
    $ghi_chu    = trim($_POST["ghi_chu"] ?? "");

    if (!$room_id || !$tenant_id || !$thang || !$nam) {
        setFlash("danger", "Vui lòng chọn đầy đủ phòng, người thuê, tháng/năm.");
    } else {
        if ($action === "add") {
            $ma = "HD" . $nam . str_pad($thang,2,"0",STR_PAD_LEFT) . sprintf("%03d", rand(1,999));
            $pdo->prepare("INSERT INTO invoices (ma_hoa_don,room_id,tenant_id,thang,nam,tien_phong,tien_dien,tien_nuoc,tien_dich_vu,phi_khac,ghi_chu_phi_khac,tong_tien,han_thanh_toan,trang_thai,ghi_chu) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)")
                ->execute([$ma,$room_id,$tenant_id,$thang,$nam,$tien_phong,$tien_dien,$tien_nuoc,$tien_dv,$phi_khac,$ghi_chu_pk?:null,$tong_tien,$han_tt,$tt,$ghi_chu?:null]);
            setFlash("success", "Tạo hóa đơn <strong>$ma</strong> thành công! Tổng: ".number_format($tong_tien,0,",",".")."đ");
        } elseif ($action === "edit") {
            $id = (int)$_POST["id"];
            $pdo->prepare("UPDATE invoices SET room_id=?,tenant_id=?,thang=?,nam=?,tien_phong=?,tien_dien=?,tien_nuoc=?,tien_dich_vu=?,phi_khac=?,ghi_chu_phi_khac=?,tong_tien=?,han_thanh_toan=?,trang_thai=?,ghi_chu=? WHERE id=?")
                ->execute([$room_id,$tenant_id,$thang,$nam,$tien_phong,$tien_dien,$tien_nuoc,$tien_dv,$phi_khac,$ghi_chu_pk?:null,$tong_tien,$han_tt,$tt,$ghi_chu?:null,$id]);
            setFlash("success", "Cập nhật hóa đơn thành công!");
        }
    }
    header("Location: hoa_don.php"); exit();
}

if (isset($_GET["delete"])) {
    $id = (int)$_GET["delete"];
    $pdo->prepare("DELETE FROM invoices WHERE id=?")->execute([$id]);
    setFlash("success", "Đã xóa hóa đơn!");
    header("Location: hoa_don.php"); exit();
}

// Filter
$search   = trim($_GET["search"] ?? "");
$filter_tt = $_GET["trang_thai"] ?? "";
$filter_thang = (int)($_GET["thang"] ?? 0);
$filter_nam   = (int)($_GET["nam"] ?? 0);
$page = max(1, (int)($_GET["page"] ?? 1)); $perPage = 12;

$where = "WHERE 1=1"; $params = [];
if ($search) { $where .= " AND (i.ma_hoa_don LIKE ? OR t.ho_ten LIKE ? OR r.ma_phong LIKE ?)"; $params = ["%$search%","%$search%","%$search%"]; }
if ($filter_tt) { $where .= " AND i.trang_thai=?"; $params[] = $filter_tt; }
if ($filter_thang) { $where .= " AND i.thang=?"; $params[] = $filter_thang; }
if ($filter_nam)   { $where .= " AND i.nam=?"; $params[] = $filter_nam; }

$cnt = $pdo->prepare("SELECT COUNT(*) FROM invoices i JOIN tenants t ON i.tenant_id=t.id JOIN rooms r ON i.room_id=r.id $where");
$cnt->execute($params); $total = $cnt->fetchColumn();
$pagination = paginate($total, $page, $perPage);
$offset = $pagination["offset"];

$stmt = $pdo->prepare("SELECT i.*,t.ho_ten,r.ma_phong FROM invoices i JOIN tenants t ON i.tenant_id=t.id JOIN rooms r ON i.room_id=r.id $where ORDER BY i.nam DESC,i.thang DESC,i.ngay_tao DESC LIMIT $perPage OFFSET $offset");
$stmt->execute($params); $invoices = $stmt->fetchAll();

// Tong thong ke
$tongChuaTT = $pdo->query("SELECT COALESCE(SUM(tong_tien),0) FROM invoices WHERE trang_thai IN ('chua_thanh_toan','qua_han')")->fetchColumn();
$tongDaTT   = $pdo->query("SELECT COALESCE(SUM(tong_tien),0) FROM invoices WHERE trang_thai='da_thanh_toan'")->fetchColumn();

// Du lieu cho select
$phongs  = $pdo->query("SELECT id,ma_phong,ten_phong,gia_thue FROM rooms ORDER BY ma_phong")->fetchAll();
$tenants_list = $pdo->query("SELECT id,ho_ten,room_id FROM tenants WHERE trang_thai='dang_thue' ORDER BY ho_ten")->fetchAll();

require_once "../includes/header.php";
?>
<nav aria-label="breadcrumb">
  <ol class="breadcrumb">
    <li class="breadcrumb-item"><a href="dashboard.php">Dashboard</a></li>
    <li class="breadcrumb-item active">Hóa Đơn</li>
  </ol>
</nav>
<?php echo showFlash(); ?>

<div class="row g-3 mb-4">
  <div class="col-6 col-md-4">
    <div class="stat-card"><div class="stat-icon bg-danger bg-opacity-10"><i class="fas fa-clock text-danger"></i></div>
    <div class="stat-value text-danger"><?php echo number_format($tongChuaTT/1000000,1); ?>M</div>
    <div class="stat-label">Chưa Thu (đ)</div></div>
  </div>
  <div class="col-6 col-md-4">
    <div class="stat-card"><div class="stat-icon bg-success bg-opacity-10"><i class="fas fa-check text-success"></i></div>
    <div class="stat-value text-success"><?php echo number_format($tongDaTT/1000000,1); ?>M</div>
    <div class="stat-label">Đã Thu (đ)</div></div>
  </div>
  <div class="col-6 col-md-4">
    <div class="stat-card"><div class="stat-icon bg-primary bg-opacity-10"><i class="fas fa-receipt text-primary"></i></div>
    <div class="stat-value"><?php echo $total; ?></div>
    <div class="stat-label">Tổng Hóa Đơn</div></div>
  </div>
</div>

<div class="card">
  <div class="card-header d-flex flex-wrap gap-2 justify-content-between align-items-center">
    <span class="card-title"><i class="fas fa-receipt me-2 text-primary"></i>Danh Sách Hóa Đơn</span>
    <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#modalHD" onclick="resetHD()">
      <i class="fas fa-plus me-1"></i>Tạo Hóa Đơn
    </button>
  </div>
  <div class="card-body">
    <form method="GET" class="row g-2 mb-3">
      <div class="col-md-3"><div class="search-bar"><i class="fas fa-search search-icon"></i><input type="text" class="form-control" name="search" value="<?php echo htmlspecialchars($search); ?>" placeholder="Tìm mã HD, tên khách..."></div></div>
      <div class="col-md-2"><select class="form-select" name="trang_thai"><option value="">Tất cả TT</option><option value="chua_thanh_toan" <?php echo $filter_tt==="chua_thanh_toan"?"selected":""; ?>>Chưa TT</option><option value="da_thanh_toan" <?php echo $filter_tt==="da_thanh_toan"?"selected":""; ?>>Đã TT</option><option value="qua_han" <?php echo $filter_tt==="qua_han"?"selected":""; ?>>Quá Hạn</option></select></div>
      <div class="col-md-2"><select class="form-select" name="thang"><option value="">Tất cả tháng</option><?php for($m=1;$m<=12;$m++): ?><option value="<?php echo $m; ?>" <?php echo $filter_thang==$m?"selected":""; ?>>Tháng <?php echo $m; ?></option><?php endfor; ?></select></div>
      <div class="col-md-2"><select class="form-select" name="nam"><option value="">Tất cả năm</option><?php for($y=2024;$y<=2027;$y++): ?><option value="<?php echo $y; ?>" <?php echo $filter_nam==$y?"selected":""; ?>><?php echo $y; ?></option><?php endfor; ?></select></div>
      <div class="col-md-1"><button type="submit" class="btn btn-primary w-100">Lọc</button></div>
      <div class="col-md-2"><a href="hoa_don.php" class="btn btn-secondary w-100">Đặt Lại</a></div>
    </form>

    <div class="table-responsive">
      <table class="table table-hover align-middle">
        <thead><tr><th>Mã HD</th><th>Khách Thuê</th><th>Phòng</th><th>Tháng/Năm</th><th>Tiền Phòng</th><th>Điện+Nước</th><th>Dịch Vụ</th><th>Tổng Tiền</th><th>Hạn TT</th><th>Trạng Thái</th><th>Hành Động</th></tr></thead>
        <tbody>
          <?php if (empty($invoices)): ?>
          <tr><td colspan="11"><div class="empty-state"><i class="fas fa-receipt"></i><p>Không có hóa đơn nào.</p></div></td></tr>
          <?php else: foreach ($invoices as $inv): ?>
          <tr class="<?php echo $inv["trang_thai"]==="qua_han"?"table-danger":($inv["trang_thai"]==="chua_thanh_toan"?"table-warning":""); ?>">
            <td><strong class="text-primary small"><?php echo htmlspecialchars($inv["ma_hoa_don"]); ?></strong></td>
            <td class="small"><?php echo htmlspecialchars($inv["ho_ten"]); ?></td>
            <td><span class="badge bg-secondary"><?php echo htmlspecialchars($inv["ma_phong"]); ?></span></td>
            <td class="fw-bold">T<?php echo $inv["thang"]; ?>/<?php echo $inv["nam"]; ?></td>
            <td><?php echo number_format($inv["tien_phong"],0,",",".")."đ"; ?></td>
            <td><?php echo number_format($inv["tien_dien"]+$inv["tien_nuoc"],0,",",".")."đ"; ?></td>
            <td><?php echo number_format($inv["tien_dich_vu"],0,",",".")."đ"; ?></td>
            <td class="fw-bold text-primary"><?php echo number_format($inv["tong_tien"],0,",",".")."đ"; ?></td>
            <td class="small"><?php echo formatDate($inv["han_thanh_toan"]); ?></td>
            <td><?php echo getStatusBadge($inv["trang_thai"]); ?></td>
            <td>
              <div class="btn-group btn-group-sm">
                <a class="btn btn-outline-secondary" href="hoa_don_in.php?id=<?php echo $inv["id"]; ?>" target="_blank" title="In"><i class="fas fa-print"></i></a>
                <button class="btn btn-outline-primary" onclick="editHD(<?php echo htmlspecialchars(json_encode($inv)); ?>)" data-bs-toggle="modal" data-bs-target="#modalHD" title="Sửa"><i class="fas fa-edit"></i></button>
                <a class="btn btn-outline-danger" href="?delete=<?php echo $inv["id"]; ?>" onclick="return confirm('Xóa hóa đơn này?')" title="Xóa"><i class="fas fa-trash"></i></a>
              </div>
            </td>
          </tr>
          <?php endforeach; endif; ?>
        </tbody>
      </table>
    </div>
    <?php echo renderPagination($pagination, "hoa_don.php?search=".urlencode($search)."&trang_thai=".urlencode($filter_tt)); ?>
  </div>
</div>

<!-- Modal -->
<div class="modal fade" id="modalHD" tabindex="-1">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <form method="POST">
        <div class="modal-header">
          <h5 class="modal-title" id="hdTitle">Tạo Hóa Đơn</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <input type="hidden" name="action" id="hdAction" value="add">
          <input type="hidden" name="id" id="hdId">
          <div class="row g-3">
            <div class="col-md-6"><label class="form-label">Phòng <span class="text-danger">*</span></label>
              <select class="form-select" name="room_id" id="hd_room" required onchange="loadTenant(this)">
                <option value="">-- Chọn phòng --</option>
                <?php foreach ($phongs as $p): ?>
                <option value="<?php echo $p["id"]; ?>" data-gia="<?php echo $p["gia_thue"]; ?>"><?php echo htmlspecialchars($p["ma_phong"]." - ".$p["ten_phong"]); ?></option>
                <?php endforeach; ?>
              </select>
            </div>
            <div class="col-md-6"><label class="form-label">Người Thuê <span class="text-danger">*</span></label>
              <select class="form-select" name="tenant_id" id="hd_tenant" required>
                <option value="">-- Chọn người thuê --</option>
                <?php foreach ($tenants_list as $t): ?>
                <option value="<?php echo $t["id"]; ?>" data-room="<?php echo $t["room_id"]; ?>"><?php echo htmlspecialchars($t["ho_ten"]); ?></option>
                <?php endforeach; ?>
              </select>
            </div>
            <div class="col-md-3"><label class="form-label">Tháng</label>
              <select class="form-select" name="thang" id="hd_thang">
                <?php for($m=1;$m<=12;$m++): ?><option value="<?php echo $m; ?>" <?php echo $m==date("n")?"selected":""; ?>>Tháng <?php echo $m; ?></option><?php endfor; ?>
              </select>
            </div>
            <div class="col-md-3"><label class="form-label">Năm</label>
              <select class="form-select" name="nam" id="hd_nam">
                <?php for($y=2024;$y<=2027;$y++): ?><option value="<?php echo $y; ?>" <?php echo $y==date("Y")?"selected":""; ?>><?php echo $y; ?></option><?php endfor; ?>
              </select>
            </div>
            <div class="col-md-3"><label class="form-label">Tiền Phòng (đ)</label><input type="number" class="form-control" name="tien_phong" id="hd_tienpphong" step="50000" oninput="calcTotal()" value="0"></div>
            <div class="col-md-3"><label class="form-label">Hạn Thanh Toán</label><input type="date" class="form-control" name="han_thanh_toan" id="hd_hantt" value="<?php echo date("Y-m-d", strtotime("+7 days")); ?>"></div>
            <div class="col-md-4"><label class="form-label">Tiền Điện (đ)</label><input type="number" class="form-control" name="tien_dien" id="hd_tienqdien" oninput="calcTotal()" value="0"></div>
            <div class="col-md-4"><label class="form-label">Tiền Nước (đ)</label><input type="number" class="form-control" name="tien_nuoc" id="hd_tienuoc" oninput="calcTotal()" value="0"></div>
            <div class="col-md-4"><label class="form-label">Tiền Dịch Vụ (đ)</label><input type="number" class="form-control" name="tien_dich_vu" id="hd_tiendv" oninput="calcTotal()" value="0"></div>
            <div class="col-md-6"><label class="form-label">Phí Khác (đ)</label><input type="number" class="form-control" name="phi_khac" id="hd_phikhac" oninput="calcTotal()" value="0"></div>
            <div class="col-md-6"><label class="form-label">Mô tả phí khác</label><input type="text" class="form-control" name="ghi_chu_phi_khac" id="hd_ghichuphikhac" placeholder="Phí vệ sinh, giữ xe..."></div>
            <div class="col-md-6"><label class="form-label">Trạng Thái</label>
              <select class="form-select" name="trang_thai" id="hd_tt">
                <option value="chua_thanh_toan">Chưa thanh toán</option>
                <option value="da_thanh_toan">Đã thanh toán</option>
                <option value="qua_han">Quá hạn</option>
              </select>
            </div>
            <div class="col-md-6">
              <label class="form-label">Tổng Tiền</label>
              <div class="form-control bg-success text-white fw-bold" id="hdTongTien">0đ</div>
            </div>
            <div class="col-12"><label class="form-label">Ghi Chú</label><textarea class="form-control" name="ghi_chu" id="hd_ghichu" rows="2"></textarea></div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Hủy</button>
          <button type="submit" class="btn btn-primary"><i class="fas fa-save me-1"></i>Lưu Hóa Đơn</button>
        </div>
      </form>
    </div>
  </div>
</div>
<script>
function calcTotal(){
  const ids=["hd_tienpphong","hd_tienqdien","hd_tienuoc","hd_tiendv","hd_phikhac"];
  let t=0; ids.forEach(id=>{t+=parseFloat(document.getElementById(id).value)||0;});
  document.getElementById("hdTongTien").textContent=new Intl.NumberFormat("vi-VN").format(t)+"đ";
}
function loadTenant(sel){
  const rid=sel.value;
  const opts=document.querySelectorAll("#hd_tenant option");
  opts.forEach(o=>{if(o.dataset.room===rid)o.selected=true;});
  const gia=sel.options[sel.selectedIndex]?.dataset.gia||0;
  document.getElementById("hd_tienpphong").value=gia;
  calcTotal();
}
function resetHD(){
  document.getElementById("hdAction").value="add";document.getElementById("hdId").value="";
  document.getElementById("hdTitle").textContent="Tạo Hóa Đơn";
  document.getElementById("modalHD").querySelector("form").reset();
  document.getElementById("hd_hantt").value="<?php echo date("Y-m-d", strtotime("+7 days")); ?>";
  document.getElementById("hdTongTien").textContent="0đ";
}
function editHD(inv){
  document.getElementById("hdAction").value="edit";document.getElementById("hdId").value=inv.id;
  document.getElementById("hdTitle").textContent="Sửa: "+inv.ma_hoa_don;
  document.getElementById("hd_room").value=inv.room_id;
  document.getElementById("hd_tenant").value=inv.tenant_id;
  document.getElementById("hd_thang").value=inv.thang;
  document.getElementById("hd_nam").value=inv.nam;
  document.getElementById("hd_tienpphong").value=inv.tien_phong;
  document.getElementById("hd_tienqdien").value=inv.tien_dien;
  document.getElementById("hd_tienuoc").value=inv.tien_nuoc;
  document.getElementById("hd_tiendv").value=inv.tien_dich_vu;
  document.getElementById("hd_phikhac").value=inv.phi_khac;
  document.getElementById("hd_ghichuphikhac").value=inv.ghi_chu_phi_khac||"";
  document.getElementById("hd_hantt").value=inv.han_thanh_toan;
  document.getElementById("hd_tt").value=inv.trang_thai;
  document.getElementById("hd_ghichu").value=inv.ghi_chu||"";
  calcTotal();
}
</script>
<?php require_once "../includes/footer.php"; ?>