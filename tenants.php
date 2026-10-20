<?php
require 'includes/db.php';
require 'includes/header.php';

// Lấy danh sách khách đang thuê kèm tên phòng
$sql = "SELECT t.*, r.name as room_name 
        FROM tenants t 
        JOIN rooms r ON t.room_id = r.id 
        ORDER BY t.start_date DESC";
$stmt = $pdo->query($sql);
$tenants = $stmt->fetchAll();
?>

<div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="mb-0"><i class="bi bi-people"></i> Quản Lý Khách Thuê</h2>
    <a href="tenant_add.php" class="btn btn-primary"><i class="bi bi-person-plus"></i> Thêm Khách / Gán Phòng</a>
</div>

<div class="card shadow-sm border-0">
    <div class="card-body p-0">
        <div class="table-responsive">
            <table class="table table-hover table-striped mb-0">
                <thead class="table-primary">
                    <tr>
                        <th scope="col" class="ps-4">Họ và Tên</th>
                        <th scope="col">Phòng</th>
                        <th scope="col">Điện thoại</th>
                        <th scope="col">CCCD</th>
                        <th scope="col">Ngày thuê</th>
                        <th scope="col" class="text-end pe-4">Thao tác</th>
                    </tr>
                </thead>
                <tbody>
                    <?php if (count($tenants) > 0): ?>
                        <?php foreach ($tenants as $tenant): ?>
                            <tr>
                                <td class="ps-4 fw-medium text-dark"><i class="bi bi-person-circle text-secondary me-2"></i><?= htmlspecialchars($tenant['full_name']) ?></td>
                                <td><span class="badge bg-light text-primary border border-primary"><i class="bi bi-door-closed"></i> <?= htmlspecialchars($tenant['room_name']) ?></span></td>
                                <td><?= htmlspecialchars($tenant['phone']) ?: '-' ?></td>
                                <td><?= htmlspecialchars($tenant['identity_card']) ?: '-' ?></td>
                                <td><?= date('d/m/Y', strtotime($tenant['start_date'])) ?></td>
                                <td class="text-end pe-4">
                                    <button onclick="confirmDelete('tenant_checkout.php?id=<?= $tenant['id'] ?>', 'Thao tác này sẽ trả phòng trống và xóa thông tin khách. Tiếp tục?')" class="btn btn-outline-danger btn-sm">
                                        <i class="bi bi-box-arrow-right"></i> Trả phòng
                                    </button>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    <?php else: ?>
                        <tr>
                            <td colspan="6" class="text-center py-4 text-muted">
                                <i class="bi bi-info-circle fs-4 d-block mb-2"></i>
                                Hiện chưa có khách thuê nào.
                            </td>
                        </tr>
                    <?php endif; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>

<?php require 'includes/footer.php'; ?>
