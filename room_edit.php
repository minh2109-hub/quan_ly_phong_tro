<?php
session_start();
require 'includes/db.php';

if (!isset($_GET['id']) || !is_numeric($_GET['id'])) {
    header("Location: rooms.php");
    exit;
}

$id = $_GET['id'];

// Lấy thông tin phòng
$stmt = $pdo->prepare("SELECT * FROM rooms WHERE id = ?");
$stmt->execute([$id]);
$room = $stmt->fetch();

if (!$room) {
    $_SESSION['flash_msg'] = "Phòng không tồn tại!";
    $_SESSION['flash_type'] = "danger";
    header("Location: rooms.php");
    exit;
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $name = trim($_POST['name']);
    $price = str_replace(',', '', $_POST['price']);
    $status = $_POST['status'];
    $description = trim($_POST['description']);

    if (!empty($name) && !empty($price) && is_numeric($price)) {
        try {
            $updateStmt = $pdo->prepare("UPDATE rooms SET name = ?, price = ?, status = ?, description = ? WHERE id = ?");
            $updateStmt->execute([$name, $price, $status, $description, $id]);
            
            $_SESSION['flash_msg'] = "Cập nhật phòng thành công!";
            $_SESSION['flash_type'] = "success";
            header("Location: rooms.php");
            exit;
        } catch(PDOException $e) {
            $error = "Lỗi CSDL: " . $e->getMessage();
        }
    } else {
        $error = "Vui lòng nhập đầy đủ tên và giá hợp lệ.";
    }
}

require 'includes/header.php';
?>

<div class="row justify-content-center">
    <div class="col-md-8 col-lg-6">
        <div class="card shadow-sm border-0">
            <div class="card-header bg-white border-bottom-0 pt-4 pb-0">
                <h3 class="card-title text-center text-primary fw-bold"><i class="bi bi-pencil-square"></i> Cập Nhật Phòng</h3>
            </div>
            <div class="card-body p-4">
                <?php if (isset($error)): ?>
                    <div class="alert alert-danger"><?= $error ?></div>
                <?php endif; ?>

                <form method="POST" action="">
                    <div class="mb-3">
                        <label for="name" class="form-label fw-semibold">Tên/Số phòng <span class="text-danger">*</span></label>
                        <input type="text" class="form-control" id="name" name="name" value="<?= htmlspecialchars($room['name']) ?>" required>
                    </div>
                    
                    <div class="mb-3">
                        <label for="price" class="form-label fw-semibold">Giá thuê (VNĐ/tháng) <span class="text-danger">*</span></label>
                        <div class="input-group">
                            <input type="number" class="form-control" id="price" name="price" value="<?= htmlspecialchars($room['price']) ?>" required min="0" step="1000">
                            <span class="input-group-text">VNĐ</span>
                        </div>
                    </div>

                    <div class="mb-3">
                        <label for="status" class="form-label fw-semibold">Trạng thái</label>
                        <select class="form-select" id="status" name="status">
                            <option value="Trống" <?= $room['status'] == 'Trống' ? 'selected' : '' ?>>Trống</option>
                            <option value="Đã thuê" <?= $room['status'] == 'Đã thuê' ? 'selected' : '' ?>>Đã thuê</option>
                            <option value="Bảo trì" <?= $room['status'] == 'Bảo trì' ? 'selected' : '' ?>>Bảo trì</option>
                        </select>
                        <div class="form-text text-warning"><i class="bi bi-exclamation-triangle"></i> Lưu ý: Đổi trạng thái 'Đã thuê' sang 'Trống' không đồng nghĩa với việc tự động xóa khách thuê. Hãy sử dụng chức năng trả phòng.</div>
                    </div>

                    <div class="mb-4">
                        <label for="description" class="form-label fw-semibold">Mô tả thêm</label>
                        <textarea class="form-control" id="description" name="description" rows="3"><?= htmlspecialchars($room['description']) ?></textarea>
                    </div>

                    <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                        <a href="rooms.php" class="btn btn-light border"><i class="bi bi-x-circle"></i> Hủy</a>
                        <button type="submit" class="btn btn-primary"><i class="bi bi-save"></i> Cập Nhật</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>

<?php require 'includes/footer.php'; ?>
