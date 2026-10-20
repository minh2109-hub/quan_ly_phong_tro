<?php
// File: includes/header.php - HTML head + Topbar Admin
$baseUrl = "/QuanLyPhongTro";
if (!defined("PAGE_TITLE")) define("PAGE_TITLE", "Quản Lý Phòng Trọ");
?>
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title><?php echo PAGE_TITLE; ?> | Quản Lý Phòng Trọ</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<link href="<?php echo $baseUrl; ?>/assets/css/style.css" rel="stylesheet">
</head>
<body>
<div class="wrapper">
<?php require_once __DIR__ . "/sidebar.php"; ?>
<div class="main-content" id="mainContent">
  <header class="topbar">
    <button class="btn btn-sm btn-outline-secondary me-3" onclick="toggleSidebar()" id="sidebarToggle">
      <i class="fas fa-bars"></i>
    </button>
    <div class="topbar-title"><?php echo PAGE_TITLE; ?></div>
    <div class="topbar-right">
      <span class="me-3 text-muted small d-none d-md-inline" id="clock"></span>
      <div class="dropdown">
        <button class="btn btn-sm btn-outline-primary dropdown-toggle" data-bs-toggle="dropdown">
          <i class="fas fa-user-shield me-1"></i><?php echo htmlspecialchars($_SESSION["ho_ten"] ?? "Admin"); ?>
        </button>
        <ul class="dropdown-menu dropdown-menu-end">
          <li><a class="dropdown-item" href="/QuanLyPhongTro/admin/tai_khoan.php">
            <i class="fas fa-user-cog me-2"></i>Tài Khoản</a></li>
          <li><hr class="dropdown-divider"></li>
          <li><a class="dropdown-item text-danger" href="/QuanLyPhongTro/logout.php">
            <i class="fas fa-sign-out-alt me-2"></i>Đăng Xuất</a></li>
        </ul>
      </div>
    </div>
  </header>
  <div class="page-content">