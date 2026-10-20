<?php
// File: admin/tai_khoan.php - Quan ly tai khoan
require_once "../config/database.php";
require_once "../includes/auth.php";
require_once "../includes/functions.php";
requireAdmin();
define("PAGE_TITLE","Quan Ly Tai Khoan");

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $action   = $_POST["action"] ?? "";
    $username = trim($_POST["username"] ?? "");
    $ho_ten   = trim($_POST["ho_ten"] ?? "");
    $email    = trim($_POST["email"] ?? "");
    $sdt      = trim($_POST["so_dien_thoai"] ?? "");
    $vai_tro  = $_POST["vai_tro"] ?? "khach_thue";
    $trang_thai= $_POST["trang_thai"] ?? "hoat_dong";
    $password = $_POST["password"] ?? "";

    if (empty($username) || empty($ho_ten)) { setFlash("danger","Nhap day du ten dang nhap va ho ten."); }
    else {
        if ($action === "add") {
            if (empty($password)) { setFlash("danger","Mat khau khong duoc trong khi them moi."); }
            else {
                $hash = password_hash($password, PASSWORD_DEFAULT);
                try {
                    $pdo->prepare("INSERT INTO users (username,password,ho_ten,email,so_dien_thoai,vai_tro,trang_thai) VALUES (?,?,?,?,?,?,?)")->execute([$username,$hash,$ho_ten,$email?:null,$sdt?:null,$vai_tro,$trang_thai]);
                    setFlash("success","Them tai khoan thanh cong!");
                } catch (PDOException $e) { setFlash("danger","Loi: Ten dang nhap da ton tai."); }
            }
        } elseif ($action === "edit") {
            $id = (int)$_POST["id"];
            if (!empty($password)) {
                $hash = password_hash($password, PASSWORD_DEFAULT);
                $pdo->prepare("UPDATE users SET username=?,password=?,ho_ten=?,email=?,so_dien_thoai=?,vai_tro=?,trang_thai=? WHERE id=?")->execute([$username,$hash,$ho_ten,$email?:null,$sdt?:null,$vai_tro,$trang_thai,$id]);
            } else {
                $pdo->prepare("UPDATE users SET username=?,ho_ten=?,email=?,so_dien_thoai=?,vai_tro=?,trang_thai=? WHERE id=?")->execute([$username,$ho_ten,$email?:null,$sdt?:null,$vai_tro,$trang_thai,$id]);
            }
            setFlash("success","Cap nhat tai khoan thanh cong!");
        } elseif ($action === "toggle") {
            $id = (int)$_POST["id"];
            $pdo->prepare("UPDATE users SET trang_thai = IF(trang_thai='hoat_dong','khoa','hoat_dong') WHERE id=?")->execute([$id]);
            setFlash("success","Da doi trang thai tai khoan!");
        }
    }
    header("Location: tai_khoan.php"); exit();
}

if (isset($_GET["delete"])) {
    $id = (int)$_GET["delete"];
    if ($id == $_SESSION["user_id"]) { setFlash("danger","Khong the xoa tai khoan dang dung!"); }
    else { $pdo->prepare("DELETE FROM users WHERE id=?")->execute([$id]); setFlash("success","Da xoa!"); }
    header("Location: tai_khoan.php"); exit();
}

$search = trim($_GET["search"] ?? "");
$role   = $_GET["role"] ?? "";
$where  = "WHERE 1=1"; $params = [];
if ($search) { $where .= " AND (username LIKE ? OR ho_ten LIKE ? OR email LIKE ?)"; $params = ["%$search%","%$search%","%$search%"]; }
if ($role)   { $where .= " AND vai_tro=?"; $params[] = $role; }
$stmt = $pdo->prepare("SELECT * FROM users $where ORDER BY vai_tro,ho_ten");
$stmt->execute($params);
$users = $stmt->fetchAll();

require_once "../includes/header.php";
?>
<nav aria-label="breadcrumb"><ol class="breadcrumb"><li class="breadcrumb-item"><a href="dashboard.php">Dashboard</a></li><li class="breadcrumb-item active">Tai Khoan</li></ol></nav>
<?= showFlash() ?>
<div class="card">
  <div class="card-header d-flex flex-wrap gap-2 justify-content-between align-items-center">
    <span class="card-title"><i class="fas fa-user-cog me-2 text-primary"></i>Quan Ly Tai Khoan</span>
    <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#modalTK" onclick="resetTK()"><i class="fas fa-plus me-1"></i>Them Tai Khoan</button>
  </div>
  <div class="card-body">
    <form method="GET" class="row g-2 mb-3">
      <div class="col-md-5"><div class="search-bar"><i class="fas fa-search search-icon"></i><input type="text" class="form-control" name="search" value="<?= e($search) ?>" placeholder="Tim ten dang nhap, ho ten, email..."></div></div>
      <div class="col-md-3"><select class="form-select" name="role"><option value="">Tat ca vai tro</option><option value="admin" <?= $role==="admin"?"selected":"" ?>>Admin</option><option value="khach_thue" <?= $role==="khach_thue"?"selected":"" ?>>Khach Thue</option></select></div>
      <div class="col-md-2"><button type="submit" class="btn btn-primary w-100">Tim</button></div>
      <div class="col-md-2"><a href="tai_khoan.php" class="btn btn-secondary w-100">Dat Lai</a></div>
    </form>
    <div class="table-responsive">
      <table class="table table-hover align-middle">
        <thead><tr><th>#</th><th>Ten DN</th><th>Ho Ten</th><th>Email</th><th>SDT</th><th>Vai Tro</th><th>Trang Thai</th><th>Ngay Tao</th><th>Hanh Dong</th></tr></thead>
        <tbody>
          <?php $i=1; foreach($users as $u): ?>
          <tr>
            <td><?= $i++ ?></td>
            <td><strong><?= e($u["username"]) ?></strong><?= $u["id"]==$_SESSION["user_id"] ? " <span class=\"badge bg-success\">Ban</span>" : "" ?></td>
            <td><?= e($u["ho_ten"]) ?></td>
            <td class="small"><?= e($u["email"] ?? "-") ?></td>
            <td><?= e($u["so_dien_thoai"] ?? "-") ?></td>
            <td><?= $u["vai_tro"]==="admin" ? "<span class=\"badge bg-danger\"><i class=\"fas fa-shield-alt me-1\"></i>Admin</span>" : "<span class=\"badge bg-primary\">Khach Thue</span>" ?></td>
            <td><?= getStatusBadge($u["trang_thai"]) ?></td>
            <td class="small"><?= formatDate($u["ngay_tao"]) ?></td>
            <td>
              <div class="btn-group btn-group-sm">
                <button class="btn btn-outline-primary" onclick="editTK(<?= htmlspecialchars(json_encode($u)) ?>)" data-bs-toggle="modal" data-bs-target="#modalTK"><i class="fas fa-edit"></i></button>
                <form method="POST" style="display:inline"><input type="hidden" name="action" value="toggle"><input type="hidden" name="id" value="<?= $u["id"] ?>"><button type="submit" class="btn btn-outline-warning" title="Doi TT"><i class="fas fa-toggle-on"></i></button></form>
                <?php if($u["id"]!=$_SESSION["user_id"]): ?><a class="btn btn-outline-danger" href="?delete=<?= $u["id"] ?>" onclick="return confirm('Xac nhan xoa tai khoan?')"><i class="fas fa-trash"></i></a><?php endif; ?>
              </div>
            </td>
          </tr>
          <?php endforeach; ?>
        </tbody>
      </table>
    </div>
  </div>
</div>

<div class="modal fade" id="modalTK" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <form method="POST">
        <div class="modal-header"><h5 class="modal-title" id="tkTitle">Them Tai Khoan</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
        <div class="modal-body">
          <input type="hidden" name="action" id="tkAction" value="add"><input type="hidden" name="id" id="tkId">
          <div class="row g-3">
            <div class="col-md-6"><label class="form-label">Ten Dang Nhap *</label><input type="text" class="form-control" name="username" id="tk_user" required></div>
            <div class="col-md-6"><label class="form-label">Ho Ten *</label><input type="text" class="form-control" name="ho_ten" id="tk_hoten" required></div>
            <div class="col-md-6"><label class="form-label">Email</label><input type="email" class="form-control" name="email" id="tk_email"></div>
            <div class="col-md-6"><label class="form-label">So Dien Thoai</label><input type="text" class="form-control" name="so_dien_thoai" id="tk_sdt"></div>
            <div class="col-12"><label class="form-label">Mat Khau <span id="pwdNote" class="text-muted small">(Bo trong de giu nguyen)</span></label>
              <div class="input-group"><input type="password" class="form-control" name="password" id="tk_pwd" placeholder="Nhap mat khau..."><button type="button" class="btn btn-outline-secondary" onclick="togglePwd()"><i class="fas fa-eye" id="eyeI"></i></button></div>
            </div>
            <div class="col-md-6"><label class="form-label">Vai Tro</label><select class="form-select" name="vai_tro" id="tk_role"><option value="khach_thue">Khach Thue</option><option value="admin">Admin</option></select></div>
            <div class="col-md-6"><label class="form-label">Trang Thai</label><select class="form-select" name="trang_thai" id="tk_tt"><option value="hoat_dong">Hoat Dong</option><option value="khoa">Bi Khoa</option></select></div>
          </div>
        </div>
        <div class="modal-footer"><button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Huy</button><button type="submit" class="btn btn-primary"><i class="fas fa-save me-1"></i>Luu</button></div>
      </form>
    </div>
  </div>
</div>
<script>
function resetTK(){document.getElementById("tkAction").value="add";document.getElementById("tkId").value="";document.getElementById("tkTitle").textContent="Them Tai Khoan";document.getElementById("modalTK").querySelector("form").reset();document.getElementById("pwdNote").style.display="none";}
function editTK(u){document.getElementById("tkAction").value="edit";document.getElementById("tkId").value=u.id;document.getElementById("tkTitle").textContent="Sua: "+u.username;document.getElementById("tk_user").value=u.username;document.getElementById("tk_hoten").value=u.ho_ten;document.getElementById("tk_email").value=u.email||"";document.getElementById("tk_sdt").value=u.so_dien_thoai||"";document.getElementById("tk_role").value=u.vai_tro;document.getElementById("tk_tt").value=u.trang_thai;document.getElementById("tk_pwd").value="";document.getElementById("pwdNote").style.display="";}
function togglePwd(){const p=document.getElementById("tk_pwd");const i=document.getElementById("eyeI");p.type=p.type==="password"?"text":"password";i.classList.toggle("fa-eye");i.classList.toggle("fa-eye-slash");}
</script>
<?php require_once "../includes/footer.php"; ?>