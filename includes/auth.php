<?php
if (session_status() === PHP_SESSION_NONE) { session_start(); }

function isLoggedIn() { return isset($_SESSION["user_id"]) && !empty($_SESSION["user_id"]); }
function isAdmin() { return isLoggedIn() && $_SESSION["vai_tro"] === "admin"; }
function isKhachThue() { return isLoggedIn() && $_SESSION["vai_tro"] === "khach_thue"; }

function requireLogin() {
    if (!isLoggedIn()) { header("Location: " . getBaseUrl() . "/login.php?msg=require_login"); exit(); }
}
function requireAdmin() {
    requireLogin();
    if (!isAdmin()) { header("Location: " . getBaseUrl() . "/login.php?msg=access_denied"); exit(); }
}
function requireKhachThue() {
    requireLogin();
    if (!isKhachThue()) { header("Location: " . getBaseUrl() . "/admin/dashboard.php"); exit(); }
}
function getBaseUrl() {
    $protocol = (!empty($_SERVER["HTTPS"]) && $_SERVER["HTTPS"] !== "off") ? "https" : "http";
    $host = $_SERVER["HTTP_HOST"];
    return $protocol . "://" . $host . "/QuanLyPhongTro";
}
function getCurrentUser() {
    if (!isLoggedIn()) return null;
    return ["id" => $_SESSION["user_id"], "username" => $_SESSION["username"], "ho_ten" => $_SESSION["ho_ten"], "vai_tro" => $_SESSION["vai_tro"], "tenant_id" => $_SESSION["tenant_id"] ?? null];
}
function redirectByRole() {
    $base = getBaseUrl();
    if (isAdmin()) { header("Location: " . $base . "/admin/dashboard.php"); }
    else { header("Location: " . $base . "/user/dashboard.php"); }
    exit();
}
?>