<?php
session_start();
$_SESSION['user_id'] = 2;
$_SESSION['username'] = 'nguyen.van.a';
$_SESSION['vai_tro'] = 'khach_thue';
$_SESSION['ho_ten'] = 'Nguyễn Văn A';
$_SESSION['tenant_id'] = 1;

$file = $_GET['page'] ?? 'dashboard.php';
require_once __DIR__ . '/' . $file;
