===========================================
TOOL EXTRACT LOGIN URL DARI FILE .TXT
===========================================

📌 DESKRIPSI:
---------------
Script Python ini digunakan untuk mengekstrak URL login dari file .txt yang berada dalam folder `ulp/`.
URL login akan dikategorikan secara otomatis berdasarkan jenis platform (seperti WordPress, cPanel, FTP, Joomla, dll).
Hasil ekstraksi akan disimpan di folder `result/` ke dalam file .txt sesuai kategori.

📂 STRUKTUR FOLDER:
---------------------
- ulp/           -> Tempat Anda meletakkan semua file .txt yang ingin diproses
- result/        -> Folder hasil output, akan dibuat otomatis jika belum ada
  └── wordpress.txt
  └── ftp.txt
  └── drupal.txt
  └── ... (dan kategori lainnya)

⚙️ CARA PENGGUNAAN:
---------------------
1. Pastikan Anda sudah menginstall Python di sistem Anda.
2. Buat folder bernama `ulp` di satu folder dengan script ini.
3. Masukkan semua file `.txt` yang berisi daftar URL ke dalam folder `ulp`.
4. Jalankan script ini dengan perintah:
   
   python script.py

5. Setelah proses selesai, hasil akan muncul di folder `result/` sesuai kategori masing-masing.

🔎 KATEGORI YANG DICARI:
---------------------------
Script ini mencari URL login dari berbagai platform dengan kata kunci berikut:

- wordpress       → wp-admin, wp-login.php
- ftp             → ftp://
- cpanel          → :2082, :2083, /cpanel.
- whm             → :2086, :2087, /whm.
- plesk           → :8443, login_up.php
- drupal          → /user/login
- joomla          → /administrator
- directadmin     → :2222
- cyberpanel      → :7080
- aapanel         → :7800/login
- zpanel          → zpanel
- web-admin       → /web-admin
- clientarea      → clientarea.php
- Cms-Website     → .id/index.php/auth/signin
- moodle          → moodle.
- zcom            → .z.com
- sar             → sar.
- smss            → smss.

📌 CATATAN TAMBAHAN:
------------------------
- Script ini menghindari duplikat hasil dalam file output.
- Encoding file yang didukung: utf-8, utf-8-sig, dan latin-1.
- Jika file tidak bisa dibaca, akan ditampilkan pesan error.

📧 KONTAK: https://t.me/popmiedower
------------
