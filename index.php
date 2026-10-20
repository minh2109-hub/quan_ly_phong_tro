<?php
// File: index.php - Trang chu cong khai
require_once "config/database.php";

// Lay phong trong
$stmt = $pdo->query("SELECT * FROM rooms WHERE trang_thai = 'trong' ORDER BY gia_thue ASC");
$roomsTrong = $stmt->fetchAll();
?>
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nha Tro Phuong Nam - Phong Tro Gia Re Tien Nghi</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<style>
:root{--primary:#2563eb;--dark:#1e293b}
body{font-family:"Segoe UI",sans-serif}
.navbar-custom{background:var(--dark);padding:14px 0}
.hero{background:linear-gradient(135deg,#1e40af,#2563eb,#3b82f6);color:white;padding:100px 0 80px;text-align:center}
.hero h1{font-size:2.8rem;font-weight:800;margin-bottom:16px}
.hero p{font-size:1.1rem;opacity:.85;margin-bottom:30px}
.stat-item{text-align:center;padding:20px}
.stat-item .num{font-size:2.5rem;font-weight:800;color:var(--primary)}
.stat-item .lbl{color:#64748b;font-size:.875rem}
.room-card{border-radius:14px;overflow:hidden;border:1px solid #e2e8f0;transition:all .2s}
.room-card:hover{box-shadow:0 10px 30px rgba(0,0,0,.12);transform:translateY(-4px)}
.room-badge{background:var(--primary);color:white;padding:6px 14px;border-radius:20px;font-size:.8rem;font-weight:600}
.room-price{font-size:1.4rem;font-weight:800;color:var(--primary)}
.feature-icon{width:56px;height:56px;border-radius:14px;background:#eff6ff;display:flex;align-items:center;justify-content:center;font-size:1.4rem;color:var(--primary);margin:0 auto 12px}
.footer-dark{background:var(--dark);color:rgba(255,255,255,.7);padding:40px 0 20px}
.btn-login-nav{background:var(--primary);color:white;border:none;padding:8px 20px;border-radius:8px;font-weight:600;text-decoration:none}
.btn-login-nav:hover{background:#1d4ed8;color:white}
section{padding:60px 0}
</style>
</head>
<body>
<!-- Navbar -->
<nav class="navbar-custom">
  <div class="container d-flex justify-content-between align-items-center">
    <a href="/" class="text-white text-decoration-none d-flex align-items-center gap-2">
      <i class="fas fa-building fs-4"></i>
      <div><strong style="font-size:1.1rem">Nha Tro Phuong Nam</strong><br><small style="opacity:.6;font-size:.75rem">Khu tro uy tin - Chat luong</small></div>
    </a>
    <a href="/QuanLyPhongTro/login.php" class="btn-login-nav"><i class="fas fa-sign-in-alt me-1"></i> Dang Nhap</a>
  </div>
</nav>

<!-- Hero -->
<div class="hero">
  <div class="container">
    <h1><i class="fas fa-building me-2"></i> Nha Tro Phuong Nam</h1>
    <p>Phong tro gia re, tien nghi day du, an ninh 24/7 tai trung tam thanh pho</p>
    <a href="#phong-trong" class="btn btn-light btn-lg fw-bold px-5 me-2">
      <i class="fas fa-search me-2"></i>Xem Phong Trong
    </a>
    <a href="/QuanLyPhongTro/login.php" class="btn btn-outline-light btn-lg fw-bold px-5">
      <i class="fas fa-sign-in-alt me-2"></i>Dang Nhap
    </a>
  </div>
</div>

<!-- Stats -->
<section class="bg-white border-bottom">
  <div class="container">
    <div class="row">
      <div class="col-6 col-md-3"><div class="stat-item"><div class="num"><?= count($roomsTrong) ?></div><div class="lbl">Phong Con Trong</div></div></div>
      <div class="col-6 col-md-3"><div class="stat-item"><div class="num">8</div><div class="lbl">Tong So Phong</div></div></div>
      <div class="col-6 col-md-3"><div class="stat-item"><div class="num">24/7</div><div class="lbl">Bao Ve An Ninh</div></div></div>
      <div class="col-6 col-md-3"><div class="stat-item"><div class="num">5+</div><div class="lbl">Nam Hoat Dong</div></div></div>
    </div>
  </div>
</section>

<!-- Phong trong -->
<section id="phong-trong" class="bg-light">
  <div class="container">
    <div class="text-center mb-5">
      <h2 class="fw-bold">Phong Con Trong</h2>
      <p class="text-muted">Dat phong ngay hom nay, uu dai thang dau</p>
    </div>
    <?php if (empty($roomsTrong)): ?>
    <div class="text-center py-5 text-muted">
      <i class="fas fa-door-closed fa-3x mb-3 d-block"></i>
      <p>Hien tai khong co phong trong. Vui long lien he de duoc ho tro.</p>
    </div>
    <?php else: ?>
    <div class="row g-4">
      <?php foreach($roomsTrong as $r): ?>
      <div class="col-md-6 col-lg-4">
        <div class="room-card bg-white h-100">
          <div style="background:linear-gradient(135deg,#2563eb,#3b82f6);padding:20px;color:white">
            <div class="d-flex justify-content-between align-items-start">
              <div>
                <h5 class="mb-0 fw-bold"><?= htmlspecialchars($r["ten_phong"]) ?></h5>
                <small>Ma: <?= htmlspecialchars($r["ma_phong"]) ?> | Tang <?= $r["tang"] ?></small>
              </div>
              <span class="room-badge">Con Trong</span>
            </div>
          </div>
          <div class="p-4">
            <div class="room-price mb-3"><?= number_format($r["gia_thue"],0,",",".") ?> d/thang</div>
            <ul class="list-unstyled text-muted small mb-3">
              <li><i class="fas fa-expand-arrows-alt me-2 text-primary"></i><?= $r["dien_tich"] ?> m2</li>
              <li><i class="fas fa-users me-2 text-primary"></i>Toi da <?= $r["so_nguoi_toi_da"] ?> nguoi</li>
              <li><i class="fas fa-layer-group me-2 text-primary"></i><?= htmlspecialchars($r["loai_phong"]) ?></li>
              <?php if($r["khu"]): ?><li><i class="fas fa-map-marker-alt me-2 text-primary"></i><?= htmlspecialchars($r["khu"]) ?></li><?php endif; ?>
            </ul>
            <?php if($r["mo_ta"]): ?><p class="text-muted small"><?= htmlspecialchars($r["mo_ta"]) ?></p><?php endif; ?>
            <div class="border-top pt-3">
              <div class="row text-center">
                <div class="col"><small class="text-muted d-block">Dat coc</small><strong class="text-warning"><?= number_format($r["tien_coc"],0,",",".") ?> d</strong></div>
              </div>
            </div>
          </div>
          <div class="p-3 bg-light border-top">
            <a href="/QuanLyPhongTro/login.php" class="btn btn-primary w-100"><i class="fas fa-phone me-2"></i>Lien He Dat Phong</a>
          </div>
        </div>
      </div>
      <?php endforeach; ?>
    </div>
    <?php endif; ?>
  </div>
</section>

<!-- Tien ich -->
<section>
  <div class="container">
    <div class="text-center mb-5"><h2 class="fw-bold">Tien Ich Noi Bat</h2></div>
    <div class="row g-4 text-center">
      <?php $features = [["bolt","Dien nuoc rieng","Dong ho dien nuoc rieng tung phong, tinh chinh xac"],["wifi","Internet toc do cao","Wifi mien phi toc do cao 100Mbps"],["shield-alt","An ninh 24/7","Camera an ninh, bao ve ca ngay"],["parking","Bai giu xe","Bai giu xe may co mai che, an toan"],["broom","Ve sinh","Dich vu don ve sinh dinh ky"],["snowflake","Dieu hoa","Phong VIP co dieu hoa, nuoc nong lanh"]];
      foreach($features as $f): ?>
      <div class="col-6 col-md-4">
        <div class="feature-icon"><i class="fas fa-<?= $f[0] ?>"></i></div>
        <h6 class="fw-bold"><?= $f[1] ?></h6>
        <p class="text-muted small"><?= $f[2] ?></p>
      </div>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<!-- Lien he -->
<section class="bg-light">
  <div class="container">
    <div class="row align-items-center">
      <div class="col-md-6">
        <h2 class="fw-bold mb-3">Lien He Voi Chung Toi</h2>
        <p class="text-muted mb-4">Lien he ngay de duoc tu van va dat phong. Chung toi san sang ho tro ban.</p>
        <ul class="list-unstyled">
          <li class="mb-2"><i class="fas fa-phone me-2 text-primary"></i><strong>0901.234.567</strong></li>
          <li class="mb-2"><i class="fas fa-envelope me-2 text-primary"></i>admin@phongtro.com</li>
          <li class="mb-2"><i class="fas fa-map-marker-alt me-2 text-primary"></i>123 Duong ABC, Quan 1, TP.HCM</li>
          <li><i class="fas fa-clock me-2 text-primary"></i>7:00 - 22:00 hang ngay</li>
        </ul>
      </div>
      <div class="col-md-6 text-center mt-4 mt-md-0">
        <div style="background:linear-gradient(135deg,#2563eb,#3b82f6);border-radius:16px;padding:40px;color:white">
          <i class="fas fa-building fa-3x mb-3 d-block"></i>
          <h4 class="fw-bold">Nha Tro Phuong Nam</h4>
          <p class="mb-3 opacity-75">He thong quan ly chuyen nghiep</p>
          <a href="/QuanLyPhongTro/login.php" class="btn btn-light fw-bold px-4">
            <i class="fas fa-sign-in-alt me-2"></i>Dang Nhap He Thong
          </a>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Footer -->
<div class="footer-dark">
  <div class="container text-center">
    <p>&copy; 2026 Nha Tro Phuong Nam. He thong Quan Ly Phong Tro v1.0</p>
  </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>