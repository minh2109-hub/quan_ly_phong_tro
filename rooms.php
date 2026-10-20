<?php
require 'includes/db.php';
require 'includes/header.php';

// Fetch all rooms
$stmt = $pdo->query("SELECT * FROM rooms ORDER BY name ASC");
$rooms = $stmt->fetchAll();

// Function to format price
function formatPrice($price) {
    return number_format($price, 0, ',', '.') . ' VNĐ';
}

// Function to get badge class
function getStatusBadge($status) {
    switch ($status) {
        case 'Trống': return 'bg-success';
        case 'Đã thuê': return 'bg-danger';
        case 'Bảo trì': return 'bg-warning text-dark';
        default: return 'bg-secondary';
    }
}
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="mb-0"><i class="bi bi-door-open"></i> Quản Lý Phòng Trọ</h2>
    <a href="room_add.php" class="btn btn-primary"><i class="bi bi-plus-circle"></i> Thêm Phòng Mới</a>
</div>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
    <?php if (count($rooms) > 0): ?>
        <?php foreach ($rooms as $room): ?>
            <div class="col">
                <div class="card card-room h-100 shadow-sm position-relative">
                    <span class="badge rounded-pill status-badge <?= getStatusBadge($room['status']) ?>">
                        <?= htmlspecialchars($room['status']) ?>
                    </span>
                    <div class="card-body">
                        <h4 class="card-title fw-bold text-dark mb-3">
                            <i class="bi bi-house"></i> <?= htmlspecialchars($room['name']) ?>
                        </h4>
                        <p class="room-price mb-2"><i class="bi bi-cash-stack"></i> <?= formatPrice($room['price']) ?> / tháng</p>
                        <p class="room-desc card-text text-muted">
                            <i class="bi bi-info-circle"></i> <?= htmlspecialchars($room['description']) ?: 'Không có mô tả' ?>
                        </p>
                    </div>
                    <div class="card-footer bg-white border-top-0 d-flex justify-content-between action-buttons pb-3">
                        <a href="room_edit.php?id=<?= $room['id'] ?>" class="btn btn-outline-primary btn-sm">
                            <i class="bi bi-pencil-square"></i> Sửa
                        </a>
                        <?php if ($room['status'] === 'Trống'): ?>
                            <button onclick="confirmDelete('room_delete.php?id=<?= $room['id'] ?>', 'Phòng này sẽ bị xóa vĩnh viễn!')" class="btn btn-outline-danger btn-sm">
                                <i class="bi bi-trash"></i> Xóa
                            </button>
                        <?php else: ?>
                            <button class="btn btn-outline-secondary btn-sm" disabled title="Không thể xóa phòng đang có khách">
                                <i class="bi bi-trash"></i> Xóa
                            </button>
                        <?php endif; ?>
                    </div>
                </div>
            </div>
        <?php endforeach; ?>
    <?php else: ?>
        <div class="col-12">
            <div class="alert alert-info text-center py-4">
                <i class="bi bi-info-circle fs-3 d-block mb-2"></i>
                Chưa có phòng trọ nào. Hãy <a href="room_add.php" class="alert-link">thêm phòng mới</a>!
            </div>
        </div>
    <?php endif; ?>
</div>

<?php require 'includes/footer.php'; ?>
