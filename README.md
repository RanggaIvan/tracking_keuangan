# FinanKu — Aplikasi Keuangan Personal
### Python Flask + HTML/CSS + MySQL (XAMPP)

---

## 📁 Struktur Folder

```
keuangan/
├── app.py                  ← Backend utama (Flask)
├── setup_db.sql            ← Script SQL tambahan
├── requirements.txt        ← Daftar library Python
├── templates/
│   ├── base.html           ← Layout utama (sidebar + topbar)
│   ├── login.html          ← Halaman masuk
│   ├── register.html       ← Halaman daftar
│   ├── dashboard.html      ← Dashboard
│   ├── transactions.html   ← Manajemen Transaksi
│   ├── categories.html     ← Manajemen Kategori
│   ├── reports.html        ← Laporan Keuangan
│   └── profile.html        ← Profil Pengguna
└── static/
    ├── css/style.css       ← Stylesheet lengkap
    └── js/main.js          ← JavaScript utama
```

---

## ⚙️ Cara Instalasi & Menjalankan

### 1. Pastikan XAMPP berjalan
- Aktifkan **Apache** dan **MySQL** di XAMPP Control Panel
- Pastikan database `keuangan` sudah ada (sesuai diagram ER Anda)

### 2. Install Python & library yang dibutuhkan

```bash
# Install Python 3.8+ jika belum ada
# Kemudian install library:

pip install flask pymysql
```

Atau gunakan requirements.txt:
```bash
pip install -r requirements.txt
```

### 3. Sesuaikan konfigurasi database di app.py

Buka `app.py` dan sesuaikan bagian ini:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',       # Sesuaikan jika ada password MySQL
    'db': 'keuangan',     # Nama database
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}
```

### 4. Jalankan script SQL tambahan (jika perlu)

Di phpMyAdmin, pilih database `keuangan` lalu jalankan isi `setup_db.sql`
untuk memastikan kolom `user_id` ada di tabel `categories`.

### 5. Jalankan aplikasi

```bash
cd keuangan
python app.py
```

Buka browser: **http://localhost:5000**

---

## 🔐 Login Pertama Kali

Daftar akun baru melalui halaman **Register** (/register), kemudian masuk.

Jika ingin data contoh, uncomment bagian INSERT di `setup_db.sql`:
- Email: `demo@finanku.com`  
- Password: `password123`

---

## 🎨 Tema Warna

| Warna | Kode | Penggunaan |
|-------|------|-----------|
| Hijau Tua | `#346739` | Sidebar, tombol utama |
| Hijau Sedang | `#79AE6F` | Aksen, gradien |
| Hijau Muda | `#9FCB98` | Badge, hover states |
| Krem | `#F2EDC2` | Background kartu, text pada gelap |

---

## 📋 Fitur Lengkap

- ✅ **Login & Register** dengan enkripsi SHA-256
- ✅ **Dashboard** — ringkasan keuangan + grafik 6 bulan
- ✅ **Transaksi** — CRUD + filter tanggal, tipe, kategori + pagination
- ✅ **Kategori** — CRUD, tampilan terpisah income/expense
- ✅ **Laporan** — bulanan & tahunan, grafik pie + bar
- ✅ **Profil** — edit profil, ubah password, logout
- ✅ **Responsive** untuk desktop dan mobile

---

## ❗ Troubleshooting

**Error koneksi database:**
- Pastikan XAMPP MySQL berjalan
- Cek nama database dan password di `DB_CONFIG`

**ModuleNotFoundError:**
```bash
pip install flask pymysql
```

**Port sudah digunakan:**
```python
# Di app.py, ganti port:
app.run(debug=True, port=5001)
```
