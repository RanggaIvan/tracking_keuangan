-- ═══════════════════════════════════════════════
--  FinanKu — Database Setup Script
--  Jalankan di phpMyAdmin atau MySQL console
-- ═══════════════════════════════════════════════

-- 1. Gunakan database keuangan (sesuai diagram)
USE keuangan;

-- DDL (Data Definition Language): perintah untuk mengubah struktur database
--   - USE            : memilih database aktif
--   - ALTER TABLE    : mengubah struktur tabel (menambah atau memodifikasi kolom)
--
-- DML (Data Manipulation Language): perintah untuk mengelola data di tabel
--   - INSERT INTO    : menambahkan baris data baru ke dalam tabel

-- 2. Tambahkan kolom user_id di tabel categories jika belum ada
--    (opsional, agar kategori bersifat per-user)
ALTER TABLE categories ADD COLUMN IF NOT EXISTS user_id INT(11) DEFAULT NULL AFTER created_at;

-- 3. Pastikan kolom password di users berukuran cukup untuk SHA-256
ALTER TABLE users MODIFY COLUMN password VARCHAR(255) NOT NULL;

-- ═══════════════════════════════════════════
--  CATATAN: Struktur tabel sudah ada di database
--  keuangan sesuai diagram ER. Script ini hanya
--  memastikan kolom tambahan tersedia.
-- ═══════════════════════════════════════════

-- 4. Contoh data awal (opsional - hapus tanda -- untuk mengaktifkan)

-- Insert sample user (password = "password123" di-hash SHA-256)
-- Hash SHA-256 dari "password123" = ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f
/*
INSERT INTO users (name, email, password, role) VALUES
('Admin FinanKu', 'admin@finanku.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'admin'),
('Pengguna Demo', 'demo@finanku.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'user');
*/

-- Insert sample categories
/*
INSERT INTO categories (name, type, user_id) VALUES
('Gaji', 'income', 1),
('Freelance', 'income', 1),
('Bonus', 'income', 1),
('Investasi', 'income', 1),
('Makan & Minum', 'expense', 1),
('Transport', 'expense', 1),
('Belanja', 'expense', 1),
('Tagihan', 'expense', 1),
('Hiburan', 'expense', 1),
('Kesehatan', 'expense', 1);
*/
