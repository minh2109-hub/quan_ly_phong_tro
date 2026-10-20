<?php
session_start();
$_SESSION['user_id'] = 1;
$_SESSION['username'] = 'admin';
$_SESSION['vai_tro'] = 'admin';
$_SESSION['ho_ten'] = 'Quản Trị Viên';

$file = $_GET['page'] ?? 'dashboard.php';
require_once __DIR__ . '/' . $file;
