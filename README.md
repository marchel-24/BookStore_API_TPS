# BookStore_API_TPS

Good Reading Book (GRD) adalah start up company yang bergerak dalam bidang penjualan buku. Usaha ini ingin mengembangan usaha yang dia miliki. Pada tugas sebelumnya, saya sudah mengembangkan database dari perusahaan ini. Berikut adalah ERD yang sudah saya rancang:

![ERD GRB](https://github.com/marchel-24/BookStore_API_TPS/blob/main/asset/ERD.png)

## API Endpoint
Saya sudah membuat beberapa endpoint yang dapat digunakan. Berikut adalah endpoint yang sudah dibuat.

1. **/api/table**
   - Untuk menampilkan seluruh informasi dari tabel yang diinginkan
2. **/api/get_book_profile**
   - Untuk menampilkan buku yang dicari
3. **/api/insert_book**
   - Untuk memasukkan profile buku baru
4. **/api/delete_book**
   - Untuk menghapus profile buku tertentu
5. **/api/change_book_profile**
   - Untuk mengubah identitas dari suatu buku
6. **/api/insert_wishlist**
    - Untuk memasukkan wishlist dari seorang kustomer
7. **/api/delete_wishlist**
    - Untuk menghapus wishlist dari seorang kustomer
8. **/api/update_wishlist**
    - Untuk mengupdate wishlist dari seorang kustomer
9. **/api/create_table**
    - Merupakan fungsi tambahan jika kedepannya ingin menambahkan tabel baru pada database
10. **/api/get_all_book**
   - Merupakan fungsi untuk menampilkan seluruh daftar buku yang tersedia

## Instalasi
Untuk melakukan instalasi, dapat dilakukan dengan cara berikut:
1. Clone Repository
   ```bash
   https://github.com/marchel-24/BookStore_API_TPS.git
   cd BookStore_API_TPS
   ```
2. Membuat virtual env
   ```bash
   python -m venv .venv
   source .venv/bin/activate 
   ```
3. Menginstall seluruh yang diperlukan
   ```bash
   pip install -r requirements.txt
   ```
4. Menjalankan program
   ```bash
   flask run
   ```
   
