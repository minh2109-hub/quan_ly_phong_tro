<?php
session_start();
$role = $_GET['role'] ?? 'admin';
$page = $_GET['page'] ?? 'admin/dashboard.php';

if ($role === 'admin') {
    $_SESSION['user_id'] = 1;
    $_SESSION['username'] = 'admin';
    $_SESSION['vai_tro'] = 'admin';
    $_SESSION['ho_ten'] = 'Quản Trị Viên';
} else {
    $_SESSION['user_id'] = 2;
    $_SESSION['username'] = 'nguyen.van.a';
    $_SESSION['vai_tro'] = 'khach_thue';
    $_SESSION['ho_ten'] = 'Nguyễn Văn A';
    $_SESSION['tenant_id'] = 1;
}

header("Location: " . $page);
exit;
