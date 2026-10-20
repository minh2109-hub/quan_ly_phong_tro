CREATE DATABASE IF NOT EXISTS quanlyphongtro CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE quanlyphongtro;

CREATE TABLE IF NOT EXISTS rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    status ENUM('Trống', 'Đã thuê', 'Bảo trì') DEFAULT 'Trống',
    description TEXT
);

CREATE TABLE IF NOT EXISTS tenants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    identity_card VARCHAR(20),
    start_date DATE,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE RESTRICT
);
