<?php
// File: admin/index.php - Redirect to dashboard
require_once "../includes/auth.php";
if (isLoggedIn() && isAdmin()) {
    header("Location: /QuanLyPhongTro/admin/dashboard.php"); exit();
}
header("Location: /QuanLyPhongTro/login.php"); exit();
?>