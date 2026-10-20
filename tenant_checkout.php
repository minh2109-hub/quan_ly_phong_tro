<?php
session_start();
require 'includes/db.php';

if (isset($_GET['id']) && is_numeric($_GET['id'])) {
    $id = $_GET['id'];

    try {
        $pdo->beginTransaction();

        // Lấy room_id trước khi xóa
        $stmt = $pdo->prepare("SELECT room_id FROM tenants WHERE id = ?");
        $stmt->execute([$id]);
        $tenant = $stmt->fetch();

        if ($tenant) {
            $room_id = $tenant['room_id'];

            // Xóa khách thuê
            $deleteStmt = $pdo->prepare("DELETE FROM tenants WHERE id = ?");
            $deleteStmt->execute([$id]);

            // Cập nhật trạng thái phòng thành 'Trống'
            $updateRoom = $pdo->prepare("UPDATE rooms SET status = 'Trống' WHERE id = ?");
            $updateRoom->execute([$room_id]);

            $pdo->commit();
            
            $_SESSION['flash_msg'] = "Đã trả phòng và xóa thông tin khách thành công!";
            $_SESSION['flash_type'] = "success";
        } else {
            $pdo->rollBack();
            $_SESSION['flash_msg'] = "Không tìm thấy khách thuê!";
            $_SESSION['flash_type'] = "danger";
        }

    } catch(PDOException $e) {
        $pdo->rollBack();
        $_SESSION['flash_msg'] = "Lỗi xử lý: " . $e->getMessage();
        $_SESSION['flash_type'] = "danger";
    }
}

header("Location: tenants.php");
exit;
?>
