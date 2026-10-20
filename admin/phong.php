<?php
// File: admin/phong.php - Quan ly phong tro
require_once "../config/database.php";
require_once "../includes/auth.php";
require_once "../includes/functions.php";
requireAdmin();
define("PAGE_TITLE", "Quản Lý Phòng");

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $action = $_POST["action"] ?? "";
    $ma     = strtoupper(trim($_POST["ma_phong"] ?? ""));
    $ten    = trim($_POST["ten_phong"] ?? "");
    $loai   = $_POST["loai_phong"] ?? "Phòng thường";
    $tang   = (int)($_POST["tang"] ?? 1);
    $khu    = trim($_POST["khu"] ?? "");
    $dien_tich = (float)($_POST["dien_tich"] ?? 0);
    $gia    = (float)str_replace([",","."], ["",""], $_POST["gia_thue"] ?? 0);
    $coc    = (float)str_replace([",","."], ["",""], $_POST["tien_coc"] ?? 0);
    $nguoi  = (int)($_POST["so_nguoi_toi_da"] ?? 2);
    $tt     = $_POST["trang_thai"] ?? "trong";
    $mo_ta  = trim($_POST["mo_ta"] ?? "");

    if (empty($ma) || empty($ten)) {
        setFlash("danger", "Vui lòng nhập đầy đủ mã phòng và tên phòng.");
    } else {
        if ($action === "add") {
            try {
                $pdo->prepare("INSERT INTO rooms (ma_phong,ten_phong,loai_phong,tang,khu,dien_tich,gia_thue,tien_coc,so_nguoi_toi_da,trang_thai,mo_ta) VALUES (?,?,?,?,?,?,?,?,?,?,?)")
                    ->execute([$ma,$ten,$loai,$tang,$khu?:null,$dien_tich,$gia,$coc,$nguoi,$tt,$mo_ta?:null]);
                setFlash("success", "Thêm phòng <strong>$ma</strong> thành công!");
            } catch (PDOException $e) {
                setFlash("danger", "Mã phòng đã tồn tại. Vui lòng chọn mã khác.");
            }
        } elseif ($action === "edit") {
            $id = (int)$_POST["id"];
            $pdo->prepare("UPDATE rooms SET ma_phong=?,ten_phong=?,loai_phong=?,tang=?,khu=?,dien_tich=?,gia_thue=?,tien_coc=?,so_nguoi_toi_da=?,trang_thai=?,mo_ta=? WHERE id=?")
                ->execute([$ma,$ten,$loai,$tang,$khu?:null,$dien_tich,$gia,$coc,$nguoi,$tt,$mo_ta?:null,$id]);
            setFlash("success", "Cập nhật phòng <strong>$ma</strong> thành công!");
        }
    }
    header("Location: phong.php"); exit();
}

if (isset($_GET["delete"])) {
    $id = (int)$_GET["delete"];
    $check = $pdo->prepare("SELECT COUNT(*) FROM tenants WHERE room_id=? AND trang_thai='dang_thue'");
    $check->execute([$id]);
    if ($check->fetchColumn() > 0) {
        setFlash("danger", "Không thể xóa phòng đang có người thuê!");
    } else {
        $pdo->prepare("DELETE FROM rooms WHERE id=?")->execute([$id]);
        setFlash("success", "Đã xóa phòng thành công!");
    }
    header("Location: phong.php"); exit();
}

// Filter
$search = trim($_GET["search"] ?? "");
$filter_tt = $_GET["trang_thai"] ?? "";
$filter_loai = $_GET["loai"] ?? "";

$where = "WHERE 1=1"; $params = [];
if ($search) { $where .= " AND (ma_phong LIKE ? OR ten_phong LIKE ?)"; $params[] = "%$search%"; $params[] = "%$search%"; }
if ($filter_tt) { $where .= " AND trang_thai=?"; $params[] = $filter_tt; }
if ($filter_loai) { $where .= " AND loai_phong=?"; $params[] = $filter_loai; }

// Phan trang
$page = max(1, (int)($_GET["page"] ?? 1));
$perPage = 10;
$cnt = $pdo->prepare("SELECT COUNT(*) FROM rooms $where");
$cnt->execute($params); $total = $cnt->fetchColumn();
$pagination = paginate($total, $page, $perPage);

$stmt = $pdo->prepare("SELECT r.*, (SELECT COUNT(*) FROM tenants t WHERE t.room_id=r.id AND t.trang_thai='dang_thue') as so_nguoi FROM rooms r $where ORDER BY r.tang, r.ma_phong LIMIT $perPage OFFSET {$pagination['offset']}");
$stmt->execute($params);
$rooms = $stmt->fetchAll();

// Tong hop
$tongKhau = $pdo->query("SELECT trang_thai, COUNT(*) as so_luong FROM rooms GROUP BY trang_thai")->fetchAll(PDO::FETCH_KEY_PAIR);

require_once "../includes/header.php";
?>

<nav aria-label="breadcrumb">
  <ol class="breadcrumb">
    <li class="breadcrumb-item"><a href="dashboard.php">Dashboard</a></li>
    <li class="breadcrumb-item active">Phòng Trọ</li>
  </ol>
</nav>

<?php echo showFlash(); ?>

<!-- Stat mini cards -->
<div class="row g-3 mb-4">
  <div class="col-6 col-md-3">
    <div class="card text-center py-3">
      <div class="fw-bold fs-4 text-primary"><?php echo array_sum($tongKhau); ?></div>
      <div class="small text-muted">Tổng Phòng</div>
    </div>
  </div>
  <div class="col-6 col-md-3">
    <div class="card text-center py-3">
      <div class="fw-bold fs-4 text-success"><?php echo $tongKhau["dang_thue"] ?? 0; ?></div>
      <div class="small text-muted">Đang Thuê</div>
    </div>
  </div>
  <div class="col-6 col-md-3">
    <div class="card text-center py-3">
      <div class="fw-bold fs-4 text-info"><?php echo $tongKhau["trong"] ?? 0; ?></div>
      <div class="small text-muted">Còn Trống</div>
    </div>
  </div>
  <div class="col-6 col-md-3">
    <div class="card text-center py-3">
      <div class="fw-bold fs-4 text-warning"><?php echo $tongKhau["dang_sua_chua"] ?? 0; ?></div>
      <div class="small text-muted">Sửa Chữa</div>
    </div>
  </div>
</div>

<div class="card">
  <div class="card-header d-flex flex-wrap gap-2 justify-content-between align-items-center">
    <span class="card-title"><i class="fas fa-door-open me-2 text-primary"></i>Danh Sách Phòng</span>
    <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#modalPhong" onclick="resetForm()">
      <i class="fas fa-plus me-1"></i>Thêm Phòng
    </button>
  </div>
  <div class="card-body">
    <!-- Bo loc -->
    <form method="GET" class="row g-2 mb-3">
      <div class="col-md-4">
        <div class="search-bar">
          <i class="fas fa-search search-icon"></i>
          <input type="text" class="form-control" name="search" value="<?php echo htmlspecialchars($search); ?>" placeholder="Tìm mã phòng, tên phòng...">
        </div>
      </div>
      <div class="col-md-2">
        <select class="form-select" name="trang_thai">
          <option value="">Tất cả trạng thái</option>
          <option value="trong" <?php echo $filter_tt==="trong"?"selected":""; ?>>Còn trống</option>
          <option value="dang_thue" <?php echo $filter_tt==="dang_thue"?"selected":""; ?>>Đang thuê</option>
          <option value="dang_sua_chua" <?php echo $filter_tt==="dang_sua_chua"?"selected":""; ?>>Sửa chữa</option>
        </select>
      </div>
      <div class="col-md-2">
        <select class="form-select" name="loai">
          <option value="">Tất cả loại</option>
          <option value="Phòng thường" <?php echo $filter_loai==="Phòng thường"?"selected":""; ?>>Phòng thường</option>
          <option value="Phòng studio" <?php echo $filter_loai==="Phòng studio"?"selected":""; ?>>Studio</option>
          <option value="Phòng cao cấp" <?php echo $filter_loai==="Phòng cao cấp"?"selected":""; ?>>Cao cấp</option>
        </select>
      </div>
      <div class="col-md-2"><button type="submit" class="btn btn-primary w-100">Lọc</button></div>
      <div class="col-md-2"><a href="phong.php" class="btn btn-secondary w-100">Đặt Lại</a></div>
    </form>

    <div class="table-responsive">
      <table class="table table-hover align-middle">
        <thead>
          <tr>
            <th>Mã Phòng</th><th>Tên Phòng</th><th>Loại</th><th>Tầng/Khu</th>
            <th>Diện Tích</th><th>Giá Thuê</th><th>Tiền Cọc</th>
            <th>Người Thuê</th><th>Trạng Thái</th><th>Hành Động</th>
          </tr>
        </thead>
        <tbody>
          <?php if (empty($rooms)): ?>
          <tr><td colspan="10"><div class="empty-state"><i class="fas fa-door-open"></i><p>Không tìm thấy phòng nào.</p></div></td></tr>
          <?php else: foreach ($rooms as $r): ?>
          <tr>
            <td><strong class="text-primary"><?php echo htmlspecialchars($r["ma_phong"]); ?></strong></td>
            <td><?php echo htmlspecialchars($r["ten_phong"]); ?></td>
            <td><span class="badge bg-secondary"><?php echo htmlspecialchars($r["loai_phong"]); ?></span></td>
            <td>Tầng <?php echo $r["tang"]; ?><?php echo $r["khu"] ? " / ".$r["khu"] : ""; ?></td>
            <td><?php echo $r["dien_tich"]; ?> m²</td>
            <td class="fw-bold text-primary"><?php echo number_format($r["gia_thue"], 0, ",", "."); ?>đ</td>
            <td><?php echo number_format($r["tien_coc"] ?? 0, 0, ",", "."); ?>đ</td>
            <td class="text-center"><?php echo $r["so_nguoi"]; ?>/<?php echo $r["so_nguoi_toi_da"]; ?></td>
            <td><?php echo getStatusBadge($r["trang_thai"]); ?></td>
            <td>
              <div class="btn-group btn-group-sm">
                <button class="btn btn-outline-primary" onclick="editPhong(<?php echo htmlspecialchars(json_encode($r)); ?>)" data-bs-toggle="modal" data-bs-target="#modalPhong" title="Sửa">
                  <i class="fas fa-edit"></i>
                </button>
                <a class="btn btn-outline-danger" href="?delete=<?php echo $r["id"]; ?>" onclick="return confirm('Xác nhận xóa phòng <?php echo htmlspecialchars($r["ma_phong"]); ?>?')" title="Xóa">
                  <i class="fas fa-trash"></i>
                </a>
              </div>
            </td>
          </tr>
          <?php endforeach; endif; ?>
        </tbody>
      </table>
    </div>
    <?php echo renderPagination($pagination, "phong.php?search=".urlencode($search)."&trang_thai=".urlencode($filter_tt)."&loai=".urlencode($filter_loai)); ?>
  </div>
</div>

<!-- Modal them/sua phong -->
<div class="modal fade" id="modalPhong" tabindex="-1">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <form method="POST">
        <div class="modal-header">
          <h5 class="modal-title" id="modalTitle">Thêm Phòng Mới</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <input type="hidden" name="action" id="formAction" value="add">
          <input type="hidden" name="id" id="phongId">
          <div class="row g-3">
            <div class="col-md-4">
              <label class="form-label">Mã Phòng <span class="text-danger">*</span></label>
              <input type="text" class="form-control text-uppercase" name="ma_phong" id="ma_phong" placeholder="P101" required>
            </div>
            <div class="col-md-8">
              <label class="form-label">Tên Phòng <span class="text-danger">*</span></label>
              <input type="text" class="form-control" name="ten_phong" id="ten_phong" placeholder="Phòng 101" required>
            </div>
            <div class="col-md-4">
              <label class="form-label">Loại Phòng</label>
              <select class="form-select" name="loai_phong" id="loai_phong">
                <option>Phòng thường</option>
                <option>Phòng studio</option>
                <option>Phòng cao cấp</option>
                <option>Phòng VIP</option>
              </select>
            </div>
            <div class="col-md-4">
              <label class="form-label">Tầng</label>
              <input type="number" class="form-control" name="tang" id="tang" value="1" min="1" max="20">
            </div>
            <div class="col-md-4">
              <label class="form-label">Khu</label>
              <input type="text" class="form-control" name="khu" id="khu" placeholder="Khu A">
            </div>
            <div class="col-md-4">
              <label class="form-label">Diện Tích (m²)</label>
              <input type="number" class="form-control" name="dien_tich" id="dien_tich" step="0.5" value="20">
            </div>
            <div class="col-md-4">
              <label class="form-label">Giá Thuê (đ/tháng) <span class="text-danger">*</span></label>
              <input type="number" class="form-control" name="gia_thue" id="gia_thue" step="50000" value="2000000">
            </div>
            <div class="col-md-4">
              <label class="form-label">Tiền Cọc (đ)</label>
              <input type="number" class="form-control" name="tien_coc" id="tien_coc" step="50000" value="2000000">
            </div>
            <div class="col-md-4">
              <label class="form-label">Số Người Tối Đa</label>
              <input type="number" class="form-control" name="so_nguoi_toi_da" id="so_nguoi_toi_da" value="2" min="1" max="10">
            </div>
            <div class="col-md-4">
              <label class="form-label">Trạng Thái</label>
              <select class="form-select" name="trang_thai" id="trang_thai_phong">
                <option value="trong">Còn trống</option>
                <option value="dang_thue">Đang thuê</option>
                <option value="dang_sua_chua">Đang sửa chữa</option>
              </select>
            </div>
            <div class="col-12">
              <label class="form-label">Mô Tả</label>
              <textarea class="form-control" name="mo_ta" id="mo_ta" rows="2" placeholder="Mô tả đặc điểm phòng..."></textarea>
            </div>
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
function resetForm() {
  document.getElementById("formAction").value = "add";
  document.getElementById("phongId").value = "";
  document.getElementById("modalTitle").textContent = "Thêm Phòng Mới";
  document.getElementById("modalPhong").querySelector("form").reset();
  document.getElementById("tang").value = "1";
  document.getElementById("dien_tich").value = "20";
  document.getElementById("gia_thue").value = "2000000";
  document.getElementById("tien_coc").value = "2000000";
  document.getElementById("so_nguoi_toi_da").value = "2";
}
function editPhong(r) {
  document.getElementById("formAction").value = "edit";
  document.getElementById("phongId").value = r.id;
  document.getElementById("modalTitle").textContent = "Sửa Phòng: " + r.ma_phong;
  document.getElementById("ma_phong").value = r.ma_phong;
  document.getElementById("ten_phong").value = r.ten_phong;
  document.getElementById("loai_phong").value = r.loai_phong;
  document.getElementById("tang").value = r.tang;
  document.getElementById("khu").value = r.khu || "";
  document.getElementById("dien_tich").value = r.dien_tich;
  document.getElementById("gia_thue").value = r.gia_thue;
  document.getElementById("tien_coc").value = r.tien_coc || 0;
  document.getElementById("so_nguoi_toi_da").value = r.so_nguoi_toi_da;
  document.getElementById("trang_thai_phong").value = r.trang_thai;
  document.getElementById("mo_ta").value = r.mo_ta || "";
}
</script>
<?php require_once "../includes/footer.php"; ?>