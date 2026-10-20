<?php
// File: admin/hoa_don_in.php - In hoa don
require_once "../config/database.php";
require_once "../includes/auth.php";
require_once "../includes/functions.php";
requireAdmin();
$id = (int)($_GET["id"] ?? 0);
if (!$id) die("Khong co hoa don.");
$inv = $pdo->prepare("SELECT i.*,r.ma_phong,r.ten_phong,t.ho_ten,t.so_dien_thoai,t.dia_chi FROM invoices i JOIN rooms r ON i.room_id=r.id JOIN tenants t ON i.tenant_id=t.id WHERE i.id=?");
$inv->execute([$id]); $inv = $inv->fetch();
if (!$inv) die("Hoa don khong ton tai.");
?>
<!DOCTYPE html><html lang="vi"><head>
<meta charset="UTF-8"><title>In Hoa Don <?= e($inv["ma_hoa_don"]) ?></title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>body{font-family:"Times New Roman",serif;color:#000}@media print{.no-print{display:none}}</style>
</head><body class="p-4">
<div class="no-print mb-3"><button onclick="window.print()" class="btn btn-primary"><i class="fas fa-print me-2"></i>In Hoa Don</button> <a href="hoa_don.php" class="btn btn-secondary">Quay Lai</a></div>
<div style="max-width:650px;margin:0 auto;border:2px solid #000;padding:20px">
  <div class="text-center mb-3">
    <h4 class="fw-bold mb-0">NHA TRO PHUONG NAM</h4>
    <small>123 Duong ABC, Quan 1, TP.HCM | Tel: 0901.234.567</small>
    <h5 class="fw-bold mt-3 text-decoration-underline">HOA DON TIEN PHONG TRANG 1</h5>
    <div>Thang <?= $inv["thang"] ?> Nam <?= $inv["nam"] ?></div>
  </div>
  <hr>
  <div class="row mb-3">
    <div class="col-6"><strong>Ma Hoa Don:</strong> <?= e($inv["ma_hoa_don"]) ?></div>
    <div class="col-6 text-end"><strong>Ngay Tao:</strong> <?= formatDate($inv["ngay_tao"]) ?></div>
    <div class="col-6"><strong>Nguoi Thue:</strong> <?= e($inv["ho_ten"]) ?></div>
    <div class="col-6 text-end"><strong>SDT:</strong> <?= e($inv["so_dien_thoai"]) ?></div>
    <div class="col-6"><strong>Phong:</strong> <?= e($inv["ma_phong"]." - ".$inv["ten_phong"]) ?></div>
    <div class="col-6 text-end"><strong>Han TT:</strong> <?= formatDate($inv["han_thanh_toan"]) ?></div>
  </div>
  <table class="table table-bordered table-sm">
    <thead class="table-dark"><tr><th>#</th><th>Dien Giai</th><th class="text-end">So Tien</th></tr></thead>
    <tbody>
      <tr><td>1</td><td>Tien Phong Thang <?= $inv["thang"] ?>/<?= $inv["nam"] ?></td><td class="text-end"><?= number_format($inv["tien_phong"],0,",",".")  ?></td></tr>
      <?php if($inv["tien_dien"]>0): ?><tr><td>2</td><td>Tien Dien</td><td class="text-end"><?= number_format($inv["tien_dien"],0,",",".")  ?></td></tr><?php endif; ?>
      <?php if($inv["tien_nuoc"]>0): ?><tr><td>3</td><td>Tien Nuoc</td><td class="text-end"><?= number_format($inv["tien_nuoc"],0,",",".")  ?></td></tr><?php endif; ?>
      <?php if($inv["tien_dich_vu"]>0): ?><tr><td>4</td><td>Tien Dich Vu</td><td class="text-end"><?= number_format($inv["tien_dich_vu"],0,",",".")  ?></td></tr><?php endif; ?>
      <?php if($inv["phi_khac"]>0): ?><tr><td>5</td><td>Phi Khac<?= $inv["ghi_chu_phi_khac"]?" (".$inv["ghi_chu_phi_khac"].")":"" ?></td><td class="text-end"><?= number_format($inv["phi_khac"],0,",",".")  ?></td></tr><?php endif; ?>
    </tbody>
    <tfoot>
      <tr class="fw-bold"><td colspan="2" class="text-end fs-5">TONG CONG:</td><td class="text-end fs-5 text-danger"><?= number_format($inv["tong_tien"],0,",",".")  ?> VND</td></tr>
    </tfoot>
  </table>
  <div class="row mt-4">
    <div class="col-6"><strong>Trang Thai:</strong> <?= strtoupper($inv["trang_thai"]) ?></div>
    <?php if($inv["ghi_chu"]): ?><div class="col-12 mt-2"><strong>Ghi Chu:</strong> <?= e($inv["ghi_chu"]) ?></div><?php endif; ?>
  </div>
  <div class="row text-center mt-4">
    <div class="col-6"><p class="mb-5">Chu Tro</p><p><strong>................................</strong></p></div>
    <div class="col-6"><p class="mb-5">Nguoi Thue</p><p><strong>................................</strong></p></div>
  </div>
  <div class="text-center text-muted small mt-2">Cam on quy khach da tin tuong su dung dich vu!</div>
</div>
</body></html>