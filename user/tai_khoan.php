<?php
// File: user/tai_khoan.php - Thay doi thong tin tai khoan
require_once "../config/database.php";
require_once "../includes/auth.php";
require_once "../includes/functions.php";
requireKhachThue();
define("PAGE_TITLE","Tai Khoan Cua Toi");
$user = getCurrentUser(); $uid = (int)$user["id"]; $tid = (int)$user["tenant_id"];

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $action = $_POST["action"] ?? "";

    if ($action === "update_profile") {
        $ho_ten = trim($_POST["ho_ten"] ?? "");
        $email  = trim($_POST["email"] ?? "");
        $sdt    = trim($_POST["so_dien_thoai"] ?? "");
        $dia_chi= trim($_POST["dia_chi"] ?? "");
        if (empty($ho_ten)) { setFlash("danger","Ho ten khong duoc de trong."); }
        else {
            $pdo->prepare("UPDATE users SET ho_ten=?,email=?,so_dien_thoai=? WHERE id=?")->execute([$ho_ten,$email?:null,$sdt?:null,$uid]);
            if ($tid) $pdo->prepare("UPDATE tenants SET ho_ten=?,email=?,so_dien_thoai=?,dia_chi=? WHERE id=?")->execute([$ho_ten,$email?:null,$sdt?:null,$dia_chi?:null,$tid]);
            $_SESSION["ho_ten"] = $ho_ten;
            setFlash("success","Cap nhat thong tin thanh cong!");
        }
    } elseif ($action === "change_password") {
        $old = $_POST["old_password"] ?? "";
        $new = $_POST["new_password"] ?? "";
        $cnf = $_POST["confirm_password"] ?? "";
        $u   = $pdo->prepare("SELECT password FROM users WHERE id=?");
        $u->execute([$uid]); $u = $u->fetch();
        if (!password_verify($old,$u["password"])) { setFlash("danger","Mat khau cu khong chinh xac."); }
        elseif (strlen($new) < 6) { setFlash("danger","Mat khau moi phai co it nhat 6 ky tu."); }
        elseif ($new !== $cnf) { setFlash("danger","Xac nhan mat khau khong khop."); }
        else {
            $pdo->prepare("UPDATE users SET password=? WHERE id=?")->execute([password_hash($new,PASSWORD_DEFAULT),$uid]);
            setFlash("success","Doi mat khau thanh cong!");
        }
    }
    header("Location: tai_khoan.php"); exit();
}

$u = $pdo->prepare("SELECT * FROM users WHERE id=?");
$u->execute([$uid]); $u = $u->fetch();
$t = null;
if ($tid) { $stmt=$pdo->prepare("SELECT * FROM tenants WHERE id=?"); $stmt->execute([$tid]); $t=$stmt->fetch(); }

require_once "../includes/header_user.php";
?>
<nav aria-label="breadcrumb"><ol class="breadcrumb"><li class="breadcrumb-item"><a href="dashboard.php">Trang Chu</a></li><li class="breadcrumb-item active">Tai Khoan</li></ol></nav>
<?= showFlash() ?>
<div class="row g-4">
  <!-- Thong tin ca nhan -->
  <div class="col-lg-7">
    <div class="card">
      <div class="card-header"><span class="card-title"><i class="fas fa-user-edit me-2 text-primary"></i>Thong Tin Ca Nhan</span></div>
      <div class="card-body">
        <form method="POST">
          <input type="hidden" name="action" value="update_profile">
          <div class="row g-3">
            <div class="col-md-6"><label class="form-label">Ten Dang Nhap</label><input type="text" class="form-control" value="<?= e($u["username"]) ?>" disabled></div>
            <div class="col-md-6"><label class="form-label">Vai Tro</label><input type="text" class="form-control" value="Khach Thue" disabled></div>
            <div class="col-12"><label class="form-label">Ho Ten *</label><input type="text" class="form-control" name="ho_ten" value="<?= e($u["ho_ten"]) ?>" required></div>
            <div class="col-md-6"><label class="form-label">Email</label><input type="email" class="form-control" name="email" value="<?= e($u["email"]??""  ) ?>"></div>
            <div class="col-md-6"><label class="form-label">So Dien Thoai</label><input type="text" class="form-control" name="so_dien_thoai" value="<?= e($u["so_dien_thoai"]??""  ) ?>"></div>
            <?php if($t): ?>
            <div class="col-12"><label class="form-label">Dia Chi</label><input type="text" class="form-control" name="dia_chi" value="<?= e($t["dia_chi"]??""  ) ?>"></div>
            <?php endif; ?>
            <div class="col-12"><button type="submit" class="btn btn-primary"><i class="fas fa-save me-1"></i>Cap Nhat</button></div>
          </div>
        </form>
      </div>
    </div>
  </div>
  <!-- Doi mat khau -->
  <div class="col-lg-5">
    <div class="card">
      <div class="card-header"><span class="card-title"><i class="fas fa-lock me-2 text-primary"></i>Doi Mat Khau</span></div>
      <div class="card-body">
        <form method="POST">
          <input type="hidden" name="action" value="change_password">
          <div class="mb-3">
            <label class="form-label">Mat Khau Hien Tai *</label>
            <div class="input-group"><input type="password" class="form-control" name="old_password" required><button type="button" class="btn btn-outline-secondary" onclick="togglePwd(this)"><i class="fas fa-eye"></i></button></div>
          </div>
          <div class="mb-3">
            <label class="form-label">Mat Khau Moi *</label>
            <div class="input-group"><input type="password" class="form-control" name="new_password" minlength="6" required><button type="button" class="btn btn-outline-secondary" onclick="togglePwd(this)"><i class="fas fa-eye"></i></button></div>
            <small class="text-muted">Toi thieu 6 ky tu</small>
          </div>
          <div class="mb-3">
            <label class="form-label">Xac Nhan Mat Khau Moi *</label>
            <div class="input-group"><input type="password" class="form-control" name="confirm_password" required><button type="button" class="btn btn-outline-secondary" onclick="togglePwd(this)"><i class="fas fa-eye"></i></button></div>
          </div>
          <button type="submit" class="btn btn-warning w-100"><i class="fas fa-key me-1"></i>Doi Mat Khau</button>
        </form>
      </div>
    </div>

    <!-- Thong tin dang nhap -->
    <div class="card mt-4">
      <div class="card-header"><span class="card-title"><i class="fas fa-info-circle me-2 text-primary"></i>Thong Tin Tai Khoan</span></div>
      <div class="card-body">
        <table class="table table-borderless table-sm mb-0">
          <tr><td><strong>Ngay Tao:</strong></td><td><?= formatDate($u["ngay_tao"]) ?></td></tr>
          <tr><td><strong>Lan Cuoi Dang Nhap:</strong></td><td><?= ($u["lan_cuoi_dang_nhap"] ?? null) ? formatDate(($u["lan_cuoi_dang_nhap"] ?? null)) : "-" ?></td></tr>
          <tr><td><strong>Trang Thai:</strong></td><td><?= getStatusBadge($u["trang_thai"]) ?></td></tr>
        </table>
      </div>
    </div>
  </div>
</div>
<script>
function togglePwd(btn){const inp=btn.previousElementSibling;const i=btn.querySelector("i");inp.type=inp.type==="password"?"text":"password";i.classList.toggle("fa-eye");i.classList.toggle("fa-eye-slash");}
</script>
<?php require_once "../includes/footer_user.php"; ?>