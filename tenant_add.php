<?php
session_start();
require 'includes/db.php';

// Lấy danh sách phòng TRỐNG
$stmt = $pdo->query("SELECT id, name, price FROM rooms WHERE status = 'Trống' ORDER BY name ASC");
$emptyRooms = $stmt->fetchAll();

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $room_id = $_POST['room_id'];
    $full_name = trim($_POST['full_name']);
    $phone = trim($_POST['phone']);
    $identity_card = trim($_POST['identity_card']);
    $start_date = $_POST['start_date'];

    if (!empty($room_id) && !empty($full_name) && !empty($start_date)) {
        try {
            $pdo->beginTransaction();

            // Thêm khách
            $stmt = $pdo->prepare("INSERT INTO tenants (room_id, full_name, phone, identity_card, start_date) VALUES (?, ?, ?, ?, ?)");
            $stmt->execute([$room_id, $full_name, $phone, $identity_card, $start_date]);

            // Cập nhật trạng thái phòng
            $updateRoom = $pdo->prepare("UPDATE rooms SET status = 'Đã thuê' WHERE id = ?");
            $updateRoom->execute([$room_id]);

            $pdo->commit();

            $_SESSION['flash_msg'] = "Thêm khách và xếp phòng thành công!";
            $_SESSION['flash_type'] = "success";
            header("Location: tenants.php");
            exit;
        } catch(PDOException $e) {
            $pdo->rollBack();
            $error = "Lỗi CSDL: " . $e->getMessage();
        }
    } else {
        $error = "Vui lòng nhập đầy đủ thông tin bắt buộc.";
    }
}

require 'includes/header.php';
?>

<div class="row justify-content-center">
    <div class="col-md-8 col-lg-6">
        <div class="card shadow-sm border-0">
            <div class="card-header bg-white border-bottom-0 pt-4 pb-0">
                <h3 class="card-title text-center text-primary fw-bold"><i class="bi bi-person-plus"></i> Thêm Khách Thuê Mới</h3>
            </div>
            <div class="card-body p-4">
                <?php if (isset($error)): ?>
                    <div class="alert alert-danger"><?= $error ?></div>
                <?php endif; ?>

                <?php if (count($emptyRooms) === 0): ?>
                    <div class="alert alert-warning">
                        <i class="bi bi-exclamation-triangle"></i> Hiện tại không có phòng trống. Vui lòng <a href="room_add.php">thêm phòng mới</a> hoặc kiểm tra lại trạng thái phòng!
                    </div>
                <?php else: ?>
                    <form method="POST" action="">
                        <div class="mb-3">
                            <label for="room_id" class="form-label fw-semibold">Chọn phòng trống <span class="text-danger">*</span></label>
                            <select class="form-select" id="room_id" name="room_id" required>
                                <option value="">-- Chọn phòng --</option>
                                <?php foreach ($emptyRooms as $room): ?>
                                    <option value="<?= $room['id'] ?>"><?= htmlspecialchars($room['name']) ?> - <?= number_format($room['price'], 0, ',', '.') ?> VNĐ</option>
                                <?php endforeach; ?>
                            </select>
                        </div>

                        <div class="mb-3">
                            <label for="full_name" class="form-label fw-semibold">Họ và Tên khách <span class="text-danger">*</span></label>
                            <input type="text" class="form-control" id="full_name" name="full_name" required>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="phone" class="form-label fw-semibold">Số điện thoại</label>
                                <input type="text" class="form-control" id="phone" name="phone">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="identity_card" class="form-label fw-semibold">Số CCCD</label>
                                <input type="text" class="form-control" id="identity_card" name="identity_card">
                            </div>
                        </div>

                        <div class="mb-4">
                            <label for="start_date" class="form-label fw-semibold">Ngày bắt đầu thuê <span class="text-danger">*</span></label>
                            <input type="date" class="form-control" id="start_date" name="start_date" value="<?= date('Y-m-d') ?>" required>
                        </div>

                        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                            <a href="tenants.php" class="btn btn-light border"><i class="bi bi-x-circle"></i> Hủy</a>
                            <button type="submit" class="btn btn-primary"><i class="bi bi-save"></i> Lưu Thông Tin</button>
                        </div>
                    </form>
                <?php endif; ?>
            </div>
        </div>
    </div>
</div>

<?php require 'includes/footer.php'; ?>
