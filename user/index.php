<?php
// File: user/index.php - Redirect to dashboard
require_once "../includes/auth.php";
if (isLoggedIn() && isKhachThue()) {
    header("Location: /QuanLyPhongTro/user/dashboard.php"); exit();
}
header("Location: /QuanLyPhongTro/login.php"); exit();
?>