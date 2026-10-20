-- ========================================
-- DATABASE: quanlyphongtro
-- He thong Quan Ly Phong Tro
-- Phien ban: 1.0
-- ========================================

CREATE DATABASE IF NOT EXISTS `quanlyphongtro`
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE `quanlyphongtro`;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `maintenance_requests`;
DROP TABLE IF EXISTS `payments`;
DROP TABLE IF EXISTS `invoices`;
DROP TABLE IF EXISTS `service_usage`;
DROP TABLE IF EXISTS `services`;
DROP TABLE IF EXISTS `electric_water`;
DROP TABLE IF EXISTS `contracts`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `tenants`;
DROP TABLE IF EXISTS `rooms`;
SET FOREIGN_KEY_CHECKS = 1;

-- Bang 1: users - Tai khoan he thong
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `ho_ten` VARCHAR(100) NOT NULL,
    `email` VARCHAR(100) UNIQUE,
    `so_dien_thoai` VARCHAR(20),
    `vai_tro` ENUM('admin', 'khach_thue') NOT NULL DEFAULT 'khach_thue',
    `trang_thai` ENUM('hoat_dong', 'khoa') NOT NULL DEFAULT 'hoat_dong',
    `tenant_id` INT DEFAULT NULL,
    `ngay_tao` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `ngay_cap_nhat` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_username` (`username`),
    INDEX `idx_vai_tro` (`vai_tro`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bang 2: rooms - Phong tro
CREATE TABLE IF NOT EXISTS `rooms` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `ma_phong` VARCHAR(20) NOT NULL UNIQUE,
    `ten_phong` VARCHAR(100) NOT NULL,
    `tang` INT DEFAULT 1,
    `khu` VARCHAR(50) DEFAULT NULL,
    `loai_phong` VARCHAR(50) DEFAULT 'Phong thuong',
    `dien_tich` DECIMAL(8,2) DEFAULT NULL,
    `gia_thue` DECIMAL(12,2) NOT NULL,
    `tien_coc` DECIMAL(12,2) DEFAULT 0,
    `so_nguoi_toi_da` INT DEFAULT 2,
    `mo_ta` TEXT DEFAULT NULL,
    `trang_thai` ENUM('trong', 'dang_thue', 'dang_sua_chua') NOT NULL DEFAULT 'trong',
    `ngay_tao` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `ngay_cap_nhat` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_ma_phong` (`ma_phong`),
    INDEX `idx_trang_thai` (`trang_thai`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bang 3: tenants - Nguoi thue
CREATE TABLE IF NOT EXISTS `tenants` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `ho_ten` VARCHAR(100) NOT NULL,
    `ngay_sinh` DATE DEFAULT NULL,
    `gioi_tinh` ENUM('Nam', 'Nu', 'Khac') DEFAULT 'Nam',
    `so_dien_thoai` VARCHAR(20) NOT NULL,
    `email` VARCHAR(100) DEFAULT NULL,
    `dia_chi` TEXT DEFAULT NULL,
    `so_cmnd` VARCHAR(20) DEFAULT NULL,
    `ngay_cap_cmnd` DATE DEFAULT NULL,
    `noi_cap_cmnd` VARCHAR(100) DEFAULT NULL,
    `nghe_nghiep` VARCHAR(100) DEFAULT NULL,
    `room_id` INT DEFAULT NULL,
    `ngay_bat_dau_thue` DATE DEFAULT NULL,
    `trang_thai` ENUM('dang_thue', 'da_roi', 'tam_ngung') NOT NULL DEFAULT 'dang_thue',
    `ghi_chu` TEXT DEFAULT NULL,
    `ngay_tao` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `ngay_cap_nhat` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`room_id`) REFERENCES `rooms`(`id`) ON DELETE SET NULL,
    INDEX `idx_so_dien_thoai` (`so_dien_thoai`),
    INDEX `idx_trang_thai` (`trang_thai`),
    INDEX `idx_room_id` (`room_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bang 4: contracts - Hop dong
CREATE TABLE IF NOT EXISTS `contracts` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `ma_hop_dong` VARCHAR(20) NOT NULL UNIQUE,
    `tenant_id` INT NOT NULL,
    `room_id` INT NOT NULL,
    `ngay_bat_dau` DATE NOT NULL,
    `ngay_ket_thuc` DATE NOT NULL,
    `gia_thue` DECIMAL(12,2) NOT NULL,
    `tien_coc` DECIMAL(12,2) DEFAULT 0,
    `chu_ky_thanh_toan` ENUM('thang', 'quy', 'nam') DEFAULT 'thang',
    `trang_thai` ENUM('hieu_luc', 'sap_het_han', 'het_han', 'thanh_ly') DEFAULT 'hieu_luc',
    `noi_dung` TEXT DEFAULT NULL,
    `ghi_chu` TEXT DEFAULT NULL,
    `ngay_tao` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `ngay_cap_nhat` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`tenant_id`) REFERENCES `tenants`(`id`) ON DELETE RESTRICT,
    FOREIGN KEY (`room_id`) REFERENCES `rooms`(`id`) ON DELETE RESTRICT,
    INDEX `idx_tenant_id` (`tenant_id`),
    INDEX `idx_room_id` (`room_id`),
    INDEX `idx_trang_thai` (`trang_thai`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bang 5: electric_water - Dien nuoc
CREATE TABLE IF NOT EXISTS `electric_water` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `room_id` INT NOT NULL,
    `thang` INT NOT NULL,
    `nam` INT NOT NULL,
    `chi_so_dien_cu` DECIMAL(10,2) DEFAULT 0,
    `chi_so_dien_moi` DECIMAL(10,2) DEFAULT 0,
    `don_gia_dien` DECIMAL(10,2) DEFAULT 3500,
    `chi_so_nuoc_cu` DECIMAL(10,2) DEFAULT 0,
    `chi_so_nuoc_moi` DECIMAL(10,2) DEFAULT 0,
    `don_gia_nuoc` DECIMAL(10,2) DEFAULT 15000,
    `ghi_chu` TEXT DEFAULT NULL,
    `ngay_tao` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `ngay_cap_nhat` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`room_id`) REFERENCES `rooms`(`id`) ON DELETE RESTRICT,
    UNIQUE KEY `uk_room_thang_nam` (`room_id`, `thang`, `nam`),
    INDEX `idx_thang_nam` (`thang`, `nam`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bang 6: services - Dich vu
CREATE TABLE IF NOT EXISTS `services` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `ma_dich_vu` VARCHAR(20) NOT NULL UNIQUE,
    `ten_dich_vu` VARCHAR(100) NOT NULL,
    `don_gia` DECIMAL(12,2) NOT NULL,
    `don_vi` VARCHAR(50) DEFAULT 'thang',
    `mo_ta` TEXT DEFAULT NULL,
    `trang_thai` ENUM('hoat_dong', 'tam_ngung') DEFAULT 'hoat_dong',
    `ngay_tao` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bang 7: service_usage - Su dung dich vu
CREATE TABLE IF NOT EXISTS `service_usage` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `room_id` INT NOT NULL,
    `service_id` INT NOT NULL,
    `thang` INT NOT NULL,
    `nam` INT NOT NULL,
    `so_luong` DECIMAL(10,2) DEFAULT 1,
    `don_gia` DECIMAL(12,2) NOT NULL,
    `ghi_chu` TEXT DEFAULT NULL,
    `ngay_tao` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`room_id`) REFERENCES `rooms`(`id`) ON DELETE RESTRICT,
    FOREIGN KEY (`service_id`) REFERENCES `services`(`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bang 8: invoices - Hoa don
CREATE TABLE IF NOT EXISTS `invoices` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `ma_hoa_don` VARCHAR(30) NOT NULL UNIQUE,
    `room_id` INT NOT NULL,
    `tenant_id` INT NOT NULL,
    `thang` INT NOT NULL,
    `nam` INT NOT NULL,
    `tien_phong` DECIMAL(12,2) NOT NULL DEFAULT 0,
    `tien_dien` DECIMAL(12,2) DEFAULT 0,
    `tien_nuoc` DECIMAL(12,2) DEFAULT 0,
    `tien_dich_vu` DECIMAL(12,2) DEFAULT 0,
    `phi_khac` DECIMAL(12,2) DEFAULT 0,
    `ghi_chu_phi_khac` VARCHAR(255) DEFAULT NULL,
    `tong_tien` DECIMAL(12,2) DEFAULT 0,
    `han_thanh_toan` DATE DEFAULT NULL,
    `trang_thai` ENUM('chua_thanh_toan', 'da_thanh_toan', 'qua_han') DEFAULT 'chua_thanh_toan',
    `ghi_chu` TEXT DEFAULT NULL,
    `ngay_tao` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `ngay_cap_nhat` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`room_id`) REFERENCES `rooms`(`id`) ON DELETE RESTRICT,
    FOREIGN KEY (`tenant_id`) REFERENCES `tenants`(`id`) ON DELETE RESTRICT,
    INDEX `idx_trang_thai` (`trang_thai`),
    INDEX `idx_thang_nam` (`thang`, `nam`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bang 9: payments - Thanh toan
CREATE TABLE IF NOT EXISTS `payments` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `ma_thanh_toan` VARCHAR(20) NOT NULL UNIQUE,
    `invoice_id` INT NOT NULL,
    `tenant_id` INT NOT NULL,
    `so_tien` DECIMAL(12,2) NOT NULL,
    `ngay_thanh_toan` DATE NOT NULL,
    `phuong_thuc` ENUM('tien_mat', 'chuyen_khoan') DEFAULT 'tien_mat',
    `ma_giao_dich` VARCHAR(100) DEFAULT NULL,
    `ghi_chu` TEXT DEFAULT NULL,
    `ngay_tao` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`invoice_id`) REFERENCES `invoices`(`id`) ON DELETE RESTRICT,
    FOREIGN KEY (`tenant_id`) REFERENCES `tenants`(`id`) ON DELETE RESTRICT,
    INDEX `idx_invoice_id` (`invoice_id`),
    INDEX `idx_ngay_thanh_toan` (`ngay_thanh_toan`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bang 10: maintenance_requests - Su co
CREATE TABLE IF NOT EXISTS `maintenance_requests` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `ma_su_co` VARCHAR(20) NOT NULL UNIQUE,
    `room_id` INT NOT NULL,
    `tenant_id` INT NOT NULL,
    `tieu_de` VARCHAR(200) NOT NULL,
    `mo_ta` TEXT NOT NULL,
    `muc_do` ENUM('thap', 'trung_binh', 'cao', 'khan_cap') DEFAULT 'trung_binh',
    `hinh_anh` VARCHAR(255) DEFAULT NULL,
    `trang_thai` ENUM('moi_gui', 'da_tiep_nhan', 'dang_xu_ly', 'hoan_thanh') DEFAULT 'moi_gui',
    `ghi_chu_xu_ly` TEXT DEFAULT NULL,
    `nguoi_xu_ly` INT DEFAULT NULL,
    `ngay_hoan_thanh` DATETIME DEFAULT NULL,
    `ngay_tao` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `ngay_cap_nhat` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`room_id`) REFERENCES `rooms`(`id`) ON DELETE RESTRICT,
    FOREIGN KEY (`tenant_id`) REFERENCES `tenants`(`id`) ON DELETE RESTRICT,
    INDEX `idx_trang_thai` (`trang_thai`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Du lieu mau
-- Admin: admin / Admin@123
-- Khach thue: nguyen.van.a / User@123 (password hash cho "User@123")
INSERT INTO `users` (`username`, `password`, `ho_ten`, `email`, `so_dien_thoai`, `vai_tro`) VALUES
('admin', '$2y$10$monKe9kTzcJRAhmGO8INKe.vPF9LF3zUFepsJNc.Jh8WYKPm32jti', 'Nguyen Van Admin', 'admin@phongtro.com', '0901234567', 'admin'),
('nguyen.van.a', '$2y$10$G4Kox7qnxs0APNG/HiUa4uhFplZ1BrItl2EjeYBKR5Mr/uObKAFjG', 'Nguyen Van A', 'nguyenvana@email.com', '0912345678', 'khach_thue'),
('tran.thi.b', '$2y$10$G4Kox7qnxs0APNG/HiUa4uhFplZ1BrItl2EjeYBKR5Mr/uObKAFjG', 'Tran Thi B', 'tranthib@email.com', '0923456789', 'khach_thue'),
('le.van.c', '$2y$10$G4Kox7qnxs0APNG/HiUa4uhFplZ1BrItl2EjeYBKR5Mr/uObKAFjG', 'Le Van C', 'levanc@email.com', '0934567890', 'khach_thue');

INSERT INTO `rooms` (`ma_phong`, `ten_phong`, `tang`, `khu`, `loai_phong`, `dien_tich`, `gia_thue`, `tien_coc`, `so_nguoi_toi_da`, `trang_thai`, `mo_ta`) VALUES
('P101', 'Phong 101', 1, 'Khu A', 'Phong thuong', 25.00, 2500000, 2500000, 2, 'dang_thue', 'Phong thoang mat, co ban cong'),
('P102', 'Phong 102', 1, 'Khu A', 'Phong thuong', 25.00, 2500000, 2500000, 2, 'dang_thue', 'Phong thoang mat, co ban cong'),
('P103', 'Phong 103', 1, 'Khu A', 'Phong thuong', 25.00, 2500000, 2500000, 2, 'trong', 'Phong thoang mat'),
('P201', 'Phong 201', 2, 'Khu A', 'Phong VIP', 35.00, 3500000, 3500000, 2, 'dang_thue', 'Phong cao cap, dieu hoa, nong lanh'),
('P202', 'Phong 202', 2, 'Khu A', 'Phong VIP', 35.00, 3500000, 3500000, 2, 'trong', 'Phong cao cap, dieu hoa, nong lanh'),
('P301', 'Phong 301', 3, 'Khu B', 'Studio', 40.00, 4500000, 4500000, 2, 'dang_thue', 'Studio day du tien nghi'),
('P302', 'Phong 302', 3, 'Khu B', 'Studio', 40.00, 4500000, 4500000, 2, 'trong', 'Studio day du tien nghi'),
('P401', 'Phong 401', 4, 'Khu B', 'Phong thuong', 25.00, 2500000, 2500000, 2, 'dang_sua_chua', 'Dang sua chua he thong dien');

INSERT INTO `tenants` (`ho_ten`, `ngay_sinh`, `gioi_tinh`, `so_dien_thoai`, `email`, `dia_chi`, `so_cmnd`, `ngay_cap_cmnd`, `noi_cap_cmnd`, `nghe_nghiep`, `room_id`, `ngay_bat_dau_thue`, `trang_thai`) VALUES
('Nguyen Van A', '1995-05-15', 'Nam', '0912345678', 'nguyenvana@email.com', '123 Duong ABC, TP.HCM', '079095012345', '2020-01-15', 'TP. Ho Chi Minh', 'Nhan vien van phong', 1, '2024-01-01', 'dang_thue'),
('Tran Thi B', '1998-08-20', 'Nu', '0923456789', 'tranthib@email.com', '456 Duong XYZ, TP.HCM', '079098023456', '2021-03-20', 'TP. Ho Chi Minh', 'Sinh vien', 2, '2024-02-01', 'dang_thue'),
('Le Van C', '1993-12-10', 'Nam', '0934567890', 'levanc@email.com', '789 Duong DEF, TP.HCM', '079093034567', '2019-06-10', 'TP. Ho Chi Minh', 'Ky su', 4, '2024-01-15', 'dang_thue'),
('Pham Thi D', '2000-03-25', 'Nu', '0945678901', 'phamthid@email.com', '321 Duong GHI, TP.HCM', '079000045678', '2022-01-25', 'TP. Ho Chi Minh', 'Sinh vien', 6, '2024-03-01', 'dang_thue');

UPDATE `users` SET `tenant_id` = 1 WHERE `username` = 'nguyen.van.a';
UPDATE `users` SET `tenant_id` = 2 WHERE `username` = 'tran.thi.b';
UPDATE `users` SET `tenant_id` = 3 WHERE `username` = 'le.van.c';

INSERT INTO `contracts` (`ma_hop_dong`, `tenant_id`, `room_id`, `ngay_bat_dau`, `ngay_ket_thuc`, `gia_thue`, `tien_coc`, `chu_ky_thanh_toan`, `trang_thai`, `noi_dung`) VALUES
('HD001', 1, 1, '2024-01-01', '2025-01-01', 2500000, 2500000, 'thang', 'het_han', 'Hop dong thue phong P101'),
('HD002', 2, 2, '2024-02-01', '2025-02-01', 2500000, 2500000, 'thang', 'hieu_luc', 'Hop dong thue phong P102'),
('HD003', 3, 4, '2024-01-15', '2025-01-15', 3500000, 3500000, 'thang', 'sap_het_han', 'Hop dong thue phong P201'),
('HD004', 4, 6, '2024-03-01', '2025-03-01', 4500000, 4500000, 'thang', 'hieu_luc', 'Hop dong thue phong P301'),
('HD005', 1, 1, '2025-01-01', '2026-01-01', 2500000, 2500000, 'thang', 'sap_het_han', 'Hop dong gia han P101');

INSERT INTO `services` (`ma_dich_vu`, `ten_dich_vu`, `don_gia`, `don_vi`, `mo_ta`, `trang_thai`) VALUES
('DV001', 'Internet', 100000, 'thang', 'Internet toc do cao 100Mbps', 'hoat_dong'),
('DV002', 'Ve sinh', 50000, 'thang', 'Don ve sinh hanh lang, khu chung', 'hoat_dong'),
('DV003', 'Rac', 20000, 'thang', 'Thu gom rac hang ngay', 'hoat_dong'),
('DV004', 'Gui xe may', 100000, 'thang', 'Bai giu xe co mai che, bao ve 24/7', 'hoat_dong'),
('DV005', 'Gui xe dap', 30000, 'thang', 'Bai giu xe dap', 'hoat_dong'),
('DV006', 'Dieu hoa', 200000, 'thang', 'Phi bao duong va dien dieu hoa', 'hoat_dong');

INSERT INTO `electric_water` (`room_id`, `thang`, `nam`, `chi_so_dien_cu`, `chi_so_dien_moi`, `don_gia_dien`, `chi_so_nuoc_cu`, `chi_so_nuoc_moi`, `don_gia_nuoc`) VALUES
(1, 8, 2026, 1200, 1280, 3500, 50, 58, 15000),
(2, 8, 2026, 800, 865, 3500, 30, 36, 15000),
(4, 8, 2026, 2100, 2185, 3500, 80, 89, 15000),
(6, 8, 2026, 500, 570, 3500, 20, 27, 15000),
(1, 7, 2026, 1130, 1200, 3500, 43, 50, 15000),
(2, 7, 2026, 740, 800, 3500, 25, 30, 15000);

INSERT INTO `service_usage` (`room_id`, `service_id`, `thang`, `nam`, `so_luong`, `don_gia`) VALUES
(1, 1, 8, 2026, 1, 100000),(1, 2, 8, 2026, 1, 50000),(1, 3, 8, 2026, 1, 20000),(1, 4, 8, 2026, 1, 100000),
(2, 1, 8, 2026, 1, 100000),(2, 2, 8, 2026, 1, 50000),(2, 3, 8, 2026, 1, 20000),
(4, 1, 8, 2026, 1, 100000),(4, 2, 8, 2026, 1, 50000),(4, 3, 8, 2026, 1, 20000),(4, 6, 8, 2026, 1, 200000),
(6, 1, 8, 2026, 1, 100000),(6, 2, 8, 2026, 1, 50000),(6, 3, 8, 2026, 1, 20000),(6, 6, 8, 2026, 1, 200000);

INSERT INTO `invoices` (`ma_hoa_don`, `room_id`, `tenant_id`, `thang`, `nam`, `tien_phong`, `tien_dien`, `tien_nuoc`, `tien_dich_vu`, `phi_khac`, `tong_tien`, `han_thanh_toan`, `trang_thai`) VALUES
('HD-2026-08-001', 1, 1, 8, 2026, 2500000, 280000, 120000, 270000, 0, 3170000, '2026-09-10', 'da_thanh_toan'),
('HD-2026-08-002', 2, 2, 8, 2026, 2500000, 227500, 90000, 170000, 0, 2987500, '2026-09-10', 'chua_thanh_toan'),
('HD-2026-08-003', 4, 3, 8, 2026, 3500000, 297500, 135000, 370000, 0, 4302500, '2026-09-10', 'qua_han'),
('HD-2026-08-004', 6, 4, 8, 2026, 4500000, 245000, 105000, 370000, 0, 5220000, '2026-09-10', 'chua_thanh_toan'),
('HD-2026-07-001', 1, 1, 7, 2026, 2500000, 245000, 105000, 270000, 0, 3120000, '2026-08-10', 'da_thanh_toan'),
('HD-2026-07-002', 2, 2, 7, 2026, 2500000, 210000, 75000, 170000, 0, 2955000, '2026-08-10', 'da_thanh_toan'),
('HD-2026-06-001', 1, 1, 6, 2026, 2500000, 227500, 90000, 270000, 0, 3087500, '2026-07-10', 'da_thanh_toan'),
('HD-2026-06-002', 2, 2, 6, 2026, 2500000, 192500, 60000, 170000, 0, 2922500, '2026-07-10', 'da_thanh_toan');

INSERT INTO `payments` (`ma_thanh_toan`, `invoice_id`, `tenant_id`, `so_tien`, `ngay_thanh_toan`, `phuong_thuc`, `ghi_chu`) VALUES
('TT001', 1, 1, 3170000, '2026-09-05', 'chuyen_khoan', 'Thanh toan thang 8/2026'),
('TT002', 5, 1, 3120000, '2026-08-05', 'chuyen_khoan', 'Thanh toan thang 7/2026'),
('TT003', 6, 2, 2955000, '2026-08-07', 'tien_mat', 'Thanh toan thang 7/2026'),
('TT004', 7, 1, 3087500, '2026-07-05', 'chuyen_khoan', 'Thanh toan thang 6/2026'),
('TT005', 8, 2, 2922500, '2026-07-08', 'tien_mat', 'Thanh toan thang 6/2026');

INSERT INTO `maintenance_requests` (`ma_su_co`, `room_id`, `tenant_id`, `tieu_de`, `mo_ta`, `muc_do`, `trang_thai`, `ghi_chu_xu_ly`) VALUES
('SC001', 1, 1, 'Hong bong den phong ngu', 'Bong den phong ngu bi hong, can thay the', 'thap', 'hoan_thanh', 'Da thay bong den moi loai LED 12W'),
('SC002', 2, 2, 'Voi nuoc bi chay', 'Voi nuoc rua chen bi chay nuoc lien tuc', 'trung_binh', 'dang_xu_ly', 'Da dat mua phu kien, du kien sua ngay mai'),
('SC003', 4, 3, 'Dieu hoa khong lanh', 'Dieu hoa bat nhung khong ra hoi lanh', 'cao', 'da_tiep_nhan', NULL),
('SC004', 6, 4, 'Mat dien phong', 'Dot ngot mat dien toan phong tu toi qua', 'khan_cap', 'moi_gui', NULL);
