<?php
session_start();
require 'includes/db.php';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $name = trim($_POST['name']);
    $price = str_replace(',', '', $_POST['price']); // Bỏ dấu phẩy nếu có
    $status = $_POST['status'];
    $description = trim($_POST['description']);

    if (!empty($name) && !empty($price) && is_numeric($price)) {
        try {
            $stmt = $pdo->prepare("INSERT INTO rooms (name, price, status, description) VALUES (?, ?, ?, ?)");
            $stmt->execute([$name, $price, $status, $description]);
            
            $_SESSION['flash_msg'] = "Thêm phòng thành công!";
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
                <h3 class="card-title text-center text-primary fw-bold"><i class="bi bi-plus-circle"></i> Thêm Phòng Mới</h3>
            </div>
            <div class="card-body p-4">
                <?php if (isset($error)): ?>
                    <div class="alert alert-danger"><?= $error ?></div>
                <?php endif; ?>

                <form method="POST" action="">
                    <div class="mb-3">
                        <label for="name" class="form-label fw-semibold">Tên/Số phòng <span class="text-danger">*</span></label>
                        <input type="text" class="form-control" id="name" name="name" required placeholder="VD: Phòng 101">
                    </div>
                    
                    <div class="mb-3">
                        <label for="price" class="form-label fw-semibold">Giá thuê (VNĐ/tháng) <span class="text-danger">*</span></label>
                        <div class="input-group">
                            <input type="number" class="form-control" id="price" name="price" required placeholder="VD: 2500000" min="0" step="1000">
                            <span class="input-group-text">VNĐ</span>
                        </div>
                    </div>

                    <div class="mb-3">
                        <label for="status" class="form-label fw-semibold">Trạng thái</label>
                        <select class="form-select" id="status" name="status">
                            <option value="Trống">Trống</option>
                            <option value="Bảo trì">Bảo trì</option>
                        </select>
                        <div class="form-text">Phòng mới mặc định nên là 'Trống' hoặc 'Bảo trì'. Trạng thái 'Đã thuê' sẽ được cập nhật khi thêm khách thuê.</div>
                    </div>

                    <div class="mb-4">
                        <label for="description" class="form-label fw-semibold">Mô tả thêm</label>
                        <textarea class="form-control" id="description" name="description" rows="3" placeholder="Diện tích, tiện ích, tình trạng..."></textarea>
                    </div>

                    <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                        <a href="rooms.php" class="btn btn-light border"><i class="bi bi-x-circle"></i> Hủy</a>
                        <button type="submit" class="btn btn-primary"><i class="bi bi-save"></i> Lưu Phòng</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>

<?php require 'includes/footer.php'; ?>
