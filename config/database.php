<?php
/**
 * File: config/database.php
 * Ket noi database su dung PDO
 */

define("DB_HOST", "localhost");
define("DB_NAME", "quanlyphongtro");
define("DB_USER", "root");
define("DB_PASS", "");
define("DB_CHARSET", "utf8mb4");
define("APP_NAME", "Quan Ly Phong Tro");
define("APP_URL", "http://localhost/QuanLyPhongTro");

function getDB() {
    static $pdo = null;
    if ($pdo === null) {
        $dsn = "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=" . DB_CHARSET;
        $options = [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES   => false,
        ];
        try {
            $pdo = new PDO($dsn, DB_USER, DB_PASS, $options);
        } catch (PDOException $e) {
            die("Loi ket noi CSDL: " . $e->getMessage());
        }
    }
    return $pdo;
}

try {
    $pdo = getDB();
} catch (Exception $e) {
    die("Khong the ket noi database. Vui long kiem tra cau hinh.");
}
?>