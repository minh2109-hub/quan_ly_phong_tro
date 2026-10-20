<?php
// File: admin/thanh_toan.php - Quan ly thanh toan
require_once "../config/database.php";
require_once "../includes/auth.php";
require_once "../includes/functions.php";
requireAdmin();
define("PAGE_TITLE", "Quản Lý Thanh Toán");

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $action     = $_POST["action"] ?? "";
    $invoice_id = (int)($_POST["invoice_id"] ?? 0);
    $tenant_id  = (int)($_POST["tenant_id"] ?? 0);
    $so_tien    = (float)str_replace(",", "", $_POST["so_tien"] ?? 0);
    $phuong_thuc= $_POST["phuong_thuc"] ?? "tien_mat";
    $ngay_tt    = $_POST["ngay_thanh_toan"] ?? date("Y-m-d");
    $ghi_chu    = trim($_POST["ghi_chu"] ?? "");

    if (!$invoice_id || $so_tien <= 0) {
        setFlash("danger", "Vui lòng chọn hóa đơn và nhập số tiền hợp lệ.");
    } else {
        $ma = "TT" . date("YmdHis");
        $pdo->prepare("INSERT INTO payments (ma_thanh_toan,invoice_id,tenant_id,so_tien,phuong_thuc,ngay_thanh_toan,ghi_chu) VALUES (?,?,?,?,?,?,?)")
            ->execute([$ma, $invoice_id, $tenant_id, $so_tien, $phuong_thuc, $ngay_tt, $ghi_chu?:null]);

        // Cap nhat trang thai hoa don
        $inv = $pdo->prepare("SELECT tong_tien FROM invoices WHERE id=?");
        $inv->execute([$invoice_id]); $inv = $inv->fetch();
        $tongDaTT = $pdo->prepare("SELECT COALESCE(SUM(so_tien),0) FROM payments WHERE invoice_id=?");
        $tongDaTT->execute([$invoice_id]); $tongDaTT = $tongDaTT->fetchColumn();

        $newTT = ($tongDaTT >= $inv["tong_tien"]) ? "da_thanh_toan" : "chua_thanh_toan";
        $pdo->prepare("UPDATE invoices SET trang_thai=? WHERE id=?")->execute([$newTT, $invoice_id]);

        setFlash("success", "Ghi nhận thanh toán <strong>".number_format($so_tien,0,",",".")."đ</strong> thành công! Mã: $ma");
    }
    header("Location: thanh_toan.php"); exit();
}

if (isset($_GET["delete"])) {
    $id = (int)$_GET["delete"];
    $p = $pdo->prepare("SELECT invoice_id FROM payments WHERE id=?");
    $p->execute([$id]); $p = $p->fetch();
    $pdo->prepare("DELETE FROM payments WHERE id=?")->execute([$id]);
    // Kiem tra lai trang thai hoa don
    if ($p) {
        $tongDaTT = $pdo->prepare("SELECT COALESCE(SUM(so_tien),0) FROM payments WHERE invoice_id=?");
        $tongDaTT->execute([$p["invoice_id"]]); $tongDaTT = $tongDaTT->fetchColumn();
        $inv = $pdo->prepare("SELECT tong_tien FROM invoices WHERE id=?");
        $inv->execute([$p["invoice_id"]]); $inv = $inv->fetch();
        $newTT = ($inv && $tongDaTT >= $inv["tong_tien"]) ? "da_thanh_toan" : "chua_thanh_toan";
        $pdo->prepare("UPDATE invoices SET trang_thai=? WHERE id=?")->execute([$newTT, $p["invoice_id"]]);
    }
    setFlash("success", "Đã xóa bản ghi thanh toán!");
    header("Location: thanh_toan.php"); exit();
}

// Filter
$search = trim($_GET["search"] ?? "");
$filter_pm = $_GET["phuong_thuc"] ?? "";
$page = max(1, (int)($_GET["page"] ?? 1)); $perPage = 12;

$where = "WHERE 1=1"; $params = [];
if ($search) { $where .= " AND (p.ma_thanh_toan LIKE ? OR t.ho_ten LIKE ? OR i.ma_hoa_don LIKE ?)"; $params = ["%$search%","%$search%","%$search%"]; }
if ($filter_pm) { $where .= " AND p.phuong_thuc=?"; $params[] = $filter_pm; }

$cnt = $pdo->prepare("SELECT COUNT(*) FROM payments p JOIN invoices i ON p.invoice_id=i.id JOIN tenants t ON p.tenant_id=t.id $where");
$cnt->execute($params); $total = $cnt->fetchColumn();
$pagination = paginate($total, $page, $perPage);
$offset = $pagination["offset"];

$stmt = $pdo->prepare("SELECT p.*,i.ma_hoa_don,i.thang,i.nam,t.ho_ten,r.ma_phong FROM payments p JOIN invoices i ON p.invoice_id=i.id JOIN tenants t ON p.tenant_id=t.id JOIN rooms r ON i.room_id=r.id $where ORDER BY p.ngay_tao DESC LIMIT $perPage OFFSET $offset");
$stmt->execute($params); $payments = $stmt->fetchAll();

$tongTT = $pdo->query("SELECT COALESCE(SUM(so_tien),0) FROM payments WHERE MONTH(ngay_thanh_toan)=".date("n")." AND YEAR(ngay_thanh_toan)=".date("Y"))->fetchColumn();

// Hoa don chua thanh toan de chon
$invoiceList = $pdo->query("SELECT i.id,i.ma_hoa_don,i.tong_tien,i.thang,i.nam,t.ho_ten,t.id as tid FROM invoices i JOIN tenants t ON i.tenant_id=t.id WHERE i.trang_thai IN ('chua_thanh_toan','qua_han') ORDER BY i.nam DESC,i.thang DESC")->fetchAll();

require_once "../includes/header.php";
?>
<nav aria-label="breadcrumb"><ol class="breadcrumb"><li class="breadcrumb-item"><a href="dashboard.php">Dashboard</a></li><li class="breadcrumb-item active">Thanh Toán</li></ol></nav>
<?php echo showFlash(); ?>

<div class="row g-3 mb-4">
  <div class="col-md-4">
    <div class="stat-card"><div class="stat-icon bg-success bg-opacity-10"><i class="fas fa-money-bill text-success"></i></div>
    <div class="stat-value text-success"><?php echo number_format($tongTT/1000000,1); ?>M</div>
    <div class="stat-label">Thu Tháng Này (đ)</div></div>
  </div>
  <div class="col-md-4">
    <div class="stat-card"><div class="stat-icon bg-primary bg-opacity-10"><i class="fas fa-list text-primary"></i></div>
    <div class="stat-value"><?php echo $total; ?></div>
    <div class="stat-label">Tổng Giao Dịch</div></div>
  </div>
  <div class="col-md-4">
    <div class="stat-card"><div class="stat-icon bg-warning bg-opacity-10"><i class="fas fa-clock text-warning"></i></div>
    <div class="stat-value text-warning"><?php echo count($invoiceList); ?></div>
    <div class="stat-label">Hóa Đơn Chưa TT</div></div>
  </div>
</div>

<div class="row g-4">
  <!-- Form ghi nhan thanh toan -->
  <div class="col-lg-4">
    <div class="card">
      <div class="card-header"><span class="card-title"><i class="fas fa-plus-circle me-2 text-primary"></i>Ghi Nhận Thanh Toán</span></div>
      <div class="card-body">
        <form method="POST">
          <div class="mb-3">
            <label class="form-label">Chọn Hóa Đơn <span class="text-danger">*</span></label>
            <select class="form-select" name="invoice_id" id="selInv" required onchange="loadInvInfo(this)">
              <option value="">-- Chọn hóa đơn chưa TT --</option>
              <?php foreach ($invoiceList as $inv): ?>
              <option value="<?php echo $inv["id"]; ?>" data-tid="<?php echo $inv["tid"]; ?>" data-so="<?php echo $inv["tong_tien"]; ?>">
                <?php echo htmlspecialchars($inv["ma_hoa_don"]." | T".$inv["thang"]."/".$inv["nam"]." | ".$inv["ho_ten"]." | ".number_format($inv["tong_tien"],0,",",".")."đ"); ?>
              </option>
              <?php endforeach; ?>
            </select>
          </div>
          <input type="hidden" name="tenant_id" id="tenantIdHidden">
          <div class="mb-3">
            <label class="form-label">Số Tiền Thanh Toán (đ) <span class="text-danger">*</span></label>
            <input type="number" class="form-control" name="so_tien" id="soTienInput" step="1000" required>
            <small class="text-muted">Tổng hóa đơn: <strong id="tongHD">-</strong></small>
          </div>
          <div class="mb-3">
            <label class="form-label">Phương Thức</label>
            <select class="form-select" name="phuong_thuc">
              <option value="tien_mat">Tiền mặt</option>
              <option value="chuyen_khoan">Chuyển khoản</option>
              <option value="the_atm">Thẻ ATM</option>
              <option value="vi_dien_tu">Ví điện tử</option>
            </select>
          </div>
          <div class="mb-3">
            <label class="form-label">Ngày Thanh Toán</label>
            <input type="date" class="form-control" name="ngay_thanh_toan" value="<?php echo date("Y-m-d"); ?>">
          </div>
          <div class="mb-3">
            <label class="form-label">Ghi Chú</label>
            <textarea class="form-control" name="ghi_chu" rows="2" placeholder="Ghi chú thêm..."></textarea>
          </div>
          <button type="submit" class="btn btn-success w-100"><i class="fas fa-check me-1"></i>Ghi Nhận Thanh Toán</button>
        </form>
      </div>
    </div>
  </div>

  <!-- Lich su thanh toan -->
  <div class="col-lg-8">
    <div class="card">
      <div class="card-header d-flex justify-content-between align-items-center flex-wrap gap-2">
        <span class="card-title"><i class="fas fa-history me-2"></i>Lịch Sử Thanh Toán</span>
        <form method="GET" class="d-flex gap-2">
          <div class="search-bar"><i class="fas fa-search search-icon"></i><input type="text" class="form-control form-control-sm" name="search" value="<?php echo htmlspecialchars($search); ?>" placeholder="Tìm..."></div>
          <select class="form-select form-select-sm" name="phuong_thuc">
            <option value="">Tất cả PT</option>
            <option value="tien_mat" <?php echo $filter_pm==="tien_mat"?"selected":""; ?>>Tiền mặt</option>
            <option value="chuyen_khoan" <?php echo $filter_pm==="chuyen_khoan"?"selected":""; ?>>Chuyển khoản</option>
          </select>
          <button type="submit" class="btn btn-sm btn-primary">Lọc</button>
        </form>
      </div>
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead><tr><th>Mã TT</th><th>Hóa Đơn</th><th>Khách</th><th>Phòng</th><th>Số Tiền</th><th>PT</th><th>Ngày TT</th><th></th></tr></thead>
            <tbody>
              <?php if (empty($payments)): ?>
              <tr><td colspan="8"><div class="empty-state"><i class="fas fa-money-bill"></i><p>Chưa có giao dịch.</p></div></td></tr>
              <?php else: foreach ($payments as $p): ?>
              <tr>
                <td><strong class="text-success small"><?php echo htmlspecialchars($p["ma_thanh_toan"]); ?></strong></td>
                <td class="small"><?php echo htmlspecialchars($p["ma_hoa_don"]); ?> <span class="text-muted">T<?php echo $p["thang"]; ?>/<?php echo $p["nam"]; ?></span></td>
                <td class="small"><?php echo htmlspecialchars($p["ho_ten"]); ?></td>
                <td><span class="badge bg-secondary"><?php echo htmlspecialchars($p["ma_phong"]); ?></span></td>
                <td class="fw-bold text-success"><?php echo number_format($p["so_tien"],0,",",".")."đ"; ?></td>
                <td><?php echo $p["phuong_thuc"]==="tien_mat"?"<span class=\"badge bg-warning text-dark\">Tiền mặt</span>":"<span class=\"badge bg-info\">Chuyển khoản</span>"; ?></td>
                <td class="small"><?php echo formatDate($p["ngay_thanh_toan"]); ?></td>
                <td><a class="btn btn-outline-danger btn-sm" href="?delete=<?php echo $p["id"]; ?>" onclick="return confirm('Xóa giao dịch này?')"><i class="fas fa-trash"></i></a></td>
              </tr>
              <?php endforeach; endif; ?>
            </tbody>
          </table>
        </div>
        <div class="p-3"><?php echo renderPagination($pagination, "thanh_toan.php?search=".urlencode($search)); ?></div>
      </div>
    </div>
  </div>
</div>
<script>
function loadInvInfo(sel){
  const o=sel.options[sel.selectedIndex];
  document.getElementById("tenantIdHidden").value=o.dataset.tid||"";
  document.getElementById("soTienInput").value=o.dataset.so||"";
  document.getElementById("tongHD").textContent=o.dataset.so?new Intl.NumberFormat("vi-VN").format(o.dataset.so)+"đ":"-";
}
</script>
<?php require_once "../includes/footer.php"; ?>