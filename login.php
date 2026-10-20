<?php
// File: login.php - Trang dang nhap he thong
session_start();
require_once "config/database.php";

// Neu da dang nhap, chuyen trang
if (isset($_SESSION["user_id"]) && !empty($_SESSION["user_id"])) {
    $role = $_SESSION["vai_tro"] ?? "";
    if ($role === "admin") { header("Location: /QuanLyPhongTro/admin/dashboard.php"); exit(); }
    else { header("Location: /QuanLyPhongTro/user/dashboard.php"); exit(); }
}

$error = "";
$msg = $_GET["msg"] ?? "";

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $username = trim($_POST["username"] ?? "");
    $password = $_POST["password"] ?? "";

    if (empty($username) || empty($password)) {
        $error = "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.";
    } else {
        $stmt = $pdo->prepare("SELECT * FROM users WHERE username = ? AND trang_thai = \"hoat_dong\"");
        $stmt->execute([$username]);
        $user = $stmt->fetch();

        if ($user && password_verify($password, $user["password"])) {
            session_regenerate_id(true);
            $_SESSION["user_id"]  = $user["id"];
            $_SESSION["username"] = $user["username"];
            $_SESSION["ho_ten"]   = $user["ho_ten"];
            $_SESSION["vai_tro"]  = $user["vai_tro"];
            $_SESSION["tenant_id"]= $user["tenant_id"] ?? null;

            // Cap nhat lan cuoi dang nhap neu co cot nay
            try {
                $pdo->prepare("UPDATE users SET lan_cuoi_dang_nhap=NOW() WHERE id=?")->execute([$user["id"]]);
            } catch (Exception $e) { /* Ignore if column missing */ }

            if ($user["vai_tro"] === "admin") {
                header("Location: /QuanLyPhongTro/admin/dashboard.php"); exit();
            } else {
                header("Location: /QuanLyPhongTro/user/dashboard.php"); exit();
            }
        } else {
            $error = "Tên đăng nhập hoặc mật khẩu không đúng. Vui lòng thử lại.";
        }
    }
}
?>
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Đăng Nhập | Quản Lý Phòng Trọ</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<link href="/QuanLyPhongTro/assets/css/login.css" rel="stylesheet">
</head>
<body>
<div class="login-wrapper">
  <div class="login-card">
    <!-- Logo -->
    <div class="login-header">
      <div class="login-logo">
        <i class="fas fa-building"></i>
      </div>
      <h4>Quản Lý Phòng Trọ</h4>
      <p>Hệ thống quản lý khu nhà trọ chuyên nghiệp</p>
    </div>

    <!-- Thong bao -->
    <?php if ($error): ?>
    <div class="alert alert-danger alert-dismissible fade show" role="alert">
      <i class="fas fa-exclamation-circle me-2"></i><?= htmlspecialchars($error) ?>
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
    <?php endif; ?>
    <?php if ($msg === "logged_out"): ?>
    <div class="alert alert-success">
      <i class="fas fa-check-circle me-2"></i>Đã đăng xuất thành công!
    </div>
    <?php elseif ($msg === "require_login"): ?>
    <div class="alert alert-warning">
      <i class="fas fa-lock me-2"></i>Vui lòng đăng nhập để tiếp tục.
    </div>
    <?php elseif ($msg === "access_denied"): ?>
    <div class="alert alert-danger">
      <i class="fas fa-ban me-2"></i>Bạn không có quyền truy cập trang này.
    </div>
    <?php endif; ?>

    <!-- Form dang nhap -->
    <form method="POST" action="" autocomplete="off" novalidate>
      <div class="mb-3">
        <label for="username" class="form-label">Tên Đăng Nhập</label>
        <div class="input-group">
          <span class="input-group-text"><i class="fas fa-user"></i></span>
          <input type="text" class="form-control" id="username" name="username"
                 placeholder="Nhập tên đăng nhập"
                 value="<?= htmlspecialchars($_POST["username"] ?? "") ?>" required autofocus>
        </div>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Mật Khẩu</label>
        <div class="input-group">
          <span class="input-group-text"><i class="fas fa-lock"></i></span>
          <input type="password" class="form-control" id="password" name="password"
                 placeholder="Nhập mật khẩu" required>
          <button type="button" class="btn btn-outline-secondary" onclick="togglePwd()" id="toggleBtn">
            <i class="fas fa-eye" id="eyeIcon"></i>
          </button>
        </div>
      </div>
      <div class="d-grid mb-3">
        <button type="submit" class="btn btn-primary btn-lg">
          <i class="fas fa-sign-in-alt me-2"></i>Đăng Nhập
        </button>
      </div>
    </form>

    <!-- Tai khoan demo -->
    <div class="demo-accounts">
      <p class="demo-title"><i class="fas fa-info-circle me-1"></i>Tài khoản demo:</p>
      <div class="row g-2">
        <div class="col-6">
          <div class="demo-card demo-admin" onclick="fillDemo('admin','Admin@123')">
            <div class="demo-role"><i class="fas fa-shield-alt me-1"></i>Quản Trị</div>
            <div class="demo-user">admin / Admin@123</div>
          </div>
        </div>
        <div class="col-6">
          <div class="demo-card demo-user" onclick="fillDemo('nguyen.van.a','User@123')">
            <div class="demo-role"><i class="fas fa-user me-1"></i>Khách Thuê</div>
            <div class="demo-user">nguyen.van.a / User@123</div>
          </div>
        </div>
      </div>
    </div>

    <div class="text-center mt-3">
      <a href="/QuanLyPhongTro/index.php" class="text-muted small">
        <i class="fas fa-home me-1"></i>Về trang chủ
      </a>
    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script>
function togglePwd() {
  const p = document.getElementById("password");
  const i = document.getElementById("eyeIcon");
  p.type = p.type === "password" ? "text" : "password";
  i.classList.toggle("fa-eye");
  i.classList.toggle("fa-eye-slash");
}
function fillDemo(user, pass) {
  document.getElementById("username").value = user;
  document.getElementById("password").value = pass;
  document.getElementById("username").focus();
}
</script>
</body>
</html>