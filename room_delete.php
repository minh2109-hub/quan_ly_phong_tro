<?php
session_start();
require 'includes/db.php';

if (isset($_GET['id']) && is_numeric($_GET['id'])) {
    $id = $_GET['id'];

    // Kiểm tra xem phòng có khách thuê không
    $checkStmt = $pdo->prepare("SELECT status FROM rooms WHERE id = ?");
    $checkStmt->execute([$id]);
    $room = $checkStmt->fetch();

    if ($room && $room['status'] === 'Trống') {
        try {
            $stmt = $pdo->prepare("DELETE FROM rooms WHERE id = ?");
            $stmt->execute([$id]);
            
            $_SESSION['flash_msg'] = "Đã xóa phòng thành công!";
            $_SESSION['flash_type'] = "success";
        } catch(PDOException $e) {
            $_SESSION['flash_msg'] = "Không thể xóa phòng. Lỗi: " . $e->getMessage();
            $_SESSION['flash_type'] = "danger";
        }
    } else {
        $_SESSION['flash_msg'] = "Phòng đang có khách thuê, không thể xóa!";
        $_SESSION['flash_type'] = "danger";
    }
}

header("Location: rooms.php");
exit;
?>
