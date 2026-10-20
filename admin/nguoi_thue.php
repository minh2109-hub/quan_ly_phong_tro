<?php
// File: admin/nguoi_thue.php - Quan ly nguoi thue
require_once "../config/database.php";
require_once "../includes/auth.php";
require_once "../includes/functions.php";
requireAdmin();
define("PAGE_TITLE", "Quản Lý Người Thuê");

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $action  = $_POST["action"] ?? "";
    $ho_ten  = trim($_POST["ho_ten"] ?? "");
    $ngay_sinh = $_POST["ngay_sinh"] ?? null;
    $gioi_tinh = $_POST["gioi_tinh"] ?? "Nam";
    $sdt     = trim($_POST["so_dien_thoai"] ?? "");
    $email   = trim($_POST["email"] ?? "");
    $cmnd    = trim($_POST["so_cmnd"] ?? "");
    $dia_chi = trim($_POST["dia_chi"] ?? "");
    $nghe_nghiep = trim($_POST["nghe_nghiep"] ?? "");
    $room_id = (int)($_POST["room_id"] ?? 0) ?: null;
    $ngay_bd = $_POST["ngay_bat_dau_thue"] ?? date("Y-m-d");
    $tt      = $_POST["trang_thai"] ?? "dang_thue";
    $ghi_chu = trim($_POST["ghi_chu"] ?? "");

    if (empty($ho_ten) || empty($sdt)) {
        setFlash("danger", "Vui lòng nhập đầy đủ họ tên và số điện thoại.");
    } else {
        if ($action === "add") {
            try {
                $pdo->prepare("INSERT INTO tenants (ho_ten,ngay_sinh,gioi_tinh,so_dien_thoai,email,so_cmnd,dia_chi,nghe_nghiep,room_id,ngay_bat_dau_thue,trang_thai,ghi_chu) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)")
                    ->execute([$ho_ten,$ngay_sinh?:null,$gioi_tinh,$sdt,$email?:null,$cmnd?:null,$dia_chi?:null,$nghe_nghiep?:null,$room_id,$ngay_bd,$tt,$ghi_chu?:null]);
                // Cap nhat trang thai phong
                if ($room_id && $tt === "dang_thue") {
                    $pdo->prepare("UPDATE rooms SET trang_thai='dang_thue' WHERE id=?")->execute([$room_id]);
                }
                setFlash("success", "Thêm người thuê <strong>$ho_ten</strong> thành công!");
            } catch (PDOException $e) {
                setFlash("danger", "Lỗi: " . $e->getMessage());
            }
        } elseif ($action === "edit") {
            $id = (int)$_POST["id"];
            $pdo->prepare("UPDATE tenants SET ho_ten=?,ngay_sinh=?,gioi_tinh=?,so_dien_thoai=?,email=?,so_cmnd=?,dia_chi=?,nghe_nghiep=?,room_id=?,ngay_bat_dau_thue=?,trang_thai=?,ghi_chu=? WHERE id=?")
                ->execute([$ho_ten,$ngay_sinh?:null,$gioi_tinh,$sdt,$email?:null,$cmnd?:null,$dia_chi?:null,$nghe_nghiep?:null,$room_id,$ngay_bd,$tt,$ghi_chu?:null,$id]);
            if ($room_id && $tt === "dang_thue") {
                $pdo->prepare("UPDATE rooms SET trang_thai='dang_thue' WHERE id=?")->execute([$room_id]);
            }
            setFlash("success", "Cập nhật thông tin <strong>$ho_ten</strong> thành công!");
        }
    }
    header("Location: nguoi_thue.php"); exit();
}

if (isset($_GET["delete"])) {
    $id = (int)$_GET["delete"];
    $t = $pdo->prepare("SELECT ho_ten,trang_thai FROM tenants WHERE id=?");
    $t->execute([$id]); $t = $t->fetch();
    if ($t && $t["trang_thai"] === "dang_thue") {
        setFlash("danger", "Không thể xóa người đang thuê phòng! Hãy làm thủ tục trả phòng trước.");
    } else {
        $pdo->prepare("DELETE FROM tenants WHERE id=?")->execute([$id]);
        setFlash("success", "Đã xóa người thuê!");
    }
    header("Location: nguoi_thue.php"); exit();
}

// Filter + Phan trang
$search = trim($_GET["search"] ?? "");
$filter_tt = $_GET["trang_thai"] ?? "";
$page = max(1, (int)($_GET["page"] ?? 1)); $perPage = 12;
$where = "WHERE 1=1"; $params = [];
if ($search) { $where .= " AND (t.ho_ten LIKE ? OR t.so_dien_thoai LIKE ? OR t.so_cmnd LIKE ?)"; $params = ["%$search%","%$search%","%$search%"]; }
if ($filter_tt) { $where .= " AND t.trang_thai=?"; $params[] = $filter_tt; }

$cnt = $pdo->prepare("SELECT COUNT(*) FROM tenants t $where");
$cnt->execute($params); $total = $cnt->fetchColumn();
$pagination = paginate($total, $page, $perPage);

$stmt = $pdo->prepare("SELECT t.*, r.ma_phong, r.ten_phong FROM tenants t LEFT JOIN rooms r ON t.room_id=r.id $where ORDER BY t.trang_thai, t.ho_ten LIMIT $perPage OFFSET {$pagination['offset']}");
$stmt->execute($params); $tenants = $stmt->fetchAll();

// Danh sach phong trong de chon
$phongTrong = $pdo->query("SELECT id,ma_phong,ten_phong,gia_thue FROM rooms WHERE trang_thai IN ('trong','dang_thue') ORDER BY ma_phong")->fetchAll();

require_once "../includes/header.php";
?>

<nav aria-label="breadcrumb">
  <ol class="breadcrumb">
    <li class="breadcrumb-item"><a href="dashboard.php">Dashboard</a></li>
    <li class="breadcrumb-item active">Người Thuê</li>
  </ol>
</nav>
<?php echo showFlash(); ?>

<div class="card">
  <div class="card-header d-flex flex-wrap gap-2 justify-content-between align-items-center">
    <span class="card-title"><i class="fas fa-users me-2 text-primary"></i>Danh Sách Người Thuê</span>
    <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#modalNT" onclick="resetNT()">
      <i class="fas fa-plus me-1"></i>Thêm Người Thuê
    </button>
  </div>
  <div class="card-body">
    <form method="GET" class="row g-2 mb-3">
      <div class="col-md-5">
        <div class="search-bar">
          <i class="fas fa-search search-icon"></i>
          <input type="text" class="form-control" name="search" value="<?php echo htmlspecialchars($search); ?>" placeholder="Tìm họ tên, SĐT, CMND...">
        </div>
      </div>
      <div class="col-md-3">
        <select class="form-select" name="trang_thai">
          <option value="">Tất cả trạng thái</option>
          <option value="dang_thue" <?php echo $filter_tt==="dang_thue"?"selected":""; ?>>Đang thuê</option>
          <option value="da_roi" <?php echo $filter_tt==="da_roi"?"selected":""; ?>>Đã rời</option>
        </select>
      </div>
      <div class="col-md-2"><button type="submit" class="btn btn-primary w-100">Lọc</button></div>
      <div class="col-md-2"><a href="nguoi_thue.php" class="btn btn-secondary w-100">Đặt Lại</a></div>
    </form>

    <div class="table-responsive">
      <table class="table table-hover align-middle">
        <thead>
          <tr><th>#</th><th>Họ Tên</th><th>Giới Tính</th><th>SĐT</th><th>CMND</th><th>Phòng</th><th>Ngày Bắt Đầu</th><th>Trạng Thái</th><th>Hành Động</th></tr>
        </thead>
        <tbody>
          <?php $i = ($page-1)*$perPage+1; foreach ($tenants as $t): ?>
          <tr>
            <td><?php echo $i++; ?></td>
            <td>
              <div class="fw-bold"><?php echo htmlspecialchars($t["ho_ten"]); ?></div>
              <div class="text-muted small"><?php echo htmlspecialchars($t["email"] ?? ""); ?></div>
            </td>
            <td><?php echo htmlspecialchars($t["gioi_tinh"]); ?></td>
            <td><?php echo htmlspecialchars($t["so_dien_thoai"]); ?></td>
            <td class="small"><?php echo htmlspecialchars($t["so_cmnd"] ?? "-"); ?></td>
            <td>
              <?php if ($t["ma_phong"]): ?>
              <span class="badge bg-primary"><?php echo htmlspecialchars($t["ma_phong"]); ?></span>
              <?php else: ?><span class="text-muted">-</span><?php endif; ?>
            </td>
            <td class="small"><?php echo formatDate($t["ngay_bat_dau_thue"]); ?></td>
            <td><?php echo getStatusBadge($t["trang_thai"]); ?></td>
            <td>
              <div class="btn-group btn-group-sm">
                <button class="btn btn-outline-primary" onclick="editNT(<?php echo htmlspecialchars(json_encode($t)); ?>)" data-bs-toggle="modal" data-bs-target="#modalNT" title="Sửa">
                  <i class="fas fa-edit"></i>
                </button>
                <a class="btn btn-outline-danger" href="?delete=<?php echo $t["id"]; ?>" onclick="return confirm('Xác nhận xóa người thuê <?php echo htmlspecialchars($t["ho_ten"]); ?>?')" title="Xóa">
                  <i class="fas fa-trash"></i>
                </a>
              </div>
            </td>
          </tr>
          <?php endforeach; ?>
        </tbody>
      </table>
    </div>
    <?php echo renderPagination($pagination, "nguoi_thue.php?search=".urlencode($search)."&trang_thai=".urlencode($filter_tt)); ?>
  </div>
</div>

<!-- Modal them/sua nguoi thue -->
<div class="modal fade" id="modalNT" tabindex="-1">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <form method="POST">
        <div class="modal-header">
          <h5 class="modal-title" id="ntTitle">Thêm Người Thuê</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <input type="hidden" name="action" id="ntAction" value="add">
          <input type="hidden" name="id" id="ntId">
          <div class="row g-3">
            <div class="col-md-6"><label class="form-label">Họ Tên <span class="text-danger">*</span></label><input type="text" class="form-control" name="ho_ten" id="nt_hoten" required></div>
            <div class="col-md-3"><label class="form-label">Ngày Sinh</label><input type="date" class="form-control" name="ngay_sinh" id="nt_ngaysinh"></div>
            <div class="col-md-3"><label class="form-label">Giới Tính</label>
              <select class="form-select" name="gioi_tinh" id="nt_gioitinh">
                <option value="Nam">Nam</option>
                <option value="Nu">Nữ</option>
                <option value="Khac">Khác</option>
              </select>
            </div>
            <div class="col-md-6"><label class="form-label">Số Điện Thoại <span class="text-danger">*</span></label><input type="text" class="form-control" name="so_dien_thoai" id="nt_sdt" required></div>
            <div class="col-md-6"><label class="form-label">Email</label><input type="email" class="form-control" name="email" id="nt_email"></div>
            <div class="col-md-6"><label class="form-label">Số CMND/CCCD</label><input type="text" class="form-control" name="so_cmnd" id="nt_cmnd"></div>
            <div class="col-md-6"><label class="form-label">Nghề Nghiệp</label><input type="text" class="form-control" name="nghe_nghiep" id="nt_nghenghiep" placeholder="Sinh viên, Công nhân..."></div>
            <div class="col-12"><label class="form-label">Địa Chỉ Thường Trú</label><input type="text" class="form-control" name="dia_chi" id="nt_diachi"></div>
            <div class="col-md-6"><label class="form-label">Phòng Thuê</label>
              <select class="form-select" name="room_id" id="nt_room">
                <option value="">-- Chưa có phòng --</option>
                <?php foreach ($phongTrong as $p): ?>
                <option value="<?php echo $p["id"]; ?>"><?php echo htmlspecialchars($p["ma_phong"]." - ".$p["ten_phong"]." (".number_format($p["gia_thue"],0,",",".")."đ/th)"); ?></option>
                <?php endforeach; ?>
              </select>
            </div>
            <div class="col-md-6"><label class="form-label">Ngày Bắt Đầu Thuê</label><input type="date" class="form-control" name="ngay_bat_dau_thue" id="nt_ngaybd" value="<?php echo date("Y-m-d"); ?>"></div>
            <div class="col-md-6"><label class="form-label">Trạng Thái</label>
              <select class="form-select" name="trang_thai" id="nt_tt">
                <option value="dang_thue">Đang thuê</option>
                <option value="da_roi">Đã rời</option>
              </select>
            </div>
            <div class="col-12"><label class="form-label">Ghi Chú</label><textarea class="form-control" name="ghi_chu" id="nt_ghichu" rows="2"></textarea></div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Hủy</button>
          <button type="submit" class="btn btn-primary"><i class="fas fa-save me-1"></i>Lưu</button>
        </div>
      </form>
    </div>
  </div>
</div>
<script>
function resetNT(){
  document.getElementById("ntAction").value="add";
  document.getElementById("ntId").value="";
  document.getElementById("ntTitle").textContent="Thêm Người Thuê";
  document.getElementById("modalNT").querySelector("form").reset();
  document.getElementById("nt_ngaybd").value="<?php echo date("Y-m-d"); ?>";
}
function editNT(t){
  document.getElementById("ntAction").value="edit";
  document.getElementById("ntId").value=t.id;
  document.getElementById("ntTitle").textContent="Sửa: "+t.ho_ten;
  document.getElementById("nt_hoten").value=t.ho_ten;
  document.getElementById("nt_ngaysinh").value=t.ngay_sinh||"";
  document.getElementById("nt_gioitinh").value=t.gioi_tinh;
  document.getElementById("nt_sdt").value=t.so_dien_thoai;
  document.getElementById("nt_email").value=t.email||"";
  document.getElementById("nt_cmnd").value=t.so_cmnd||"";
  document.getElementById("nt_nghenghiep").value=t.nghe_nghiep||"";
  document.getElementById("nt_diachi").value=t.dia_chi||"";
  document.getElementById("nt_room").value=t.room_id||"";
  document.getElementById("nt_ngaybd").value=t.ngay_bat_dau_thue||"";
  document.getElementById("nt_tt").value=t.trang_thai;
  document.getElementById("nt_ghichu").value=t.ghi_chu||"";
}
</script>
<?php require_once "../includes/footer.php"; ?>