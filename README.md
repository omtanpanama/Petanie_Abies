# Petani_Abies AI 🐟

Aplikasi ini merupakan sistem deteksi cerdas berbasis web menggunakan Convolutional Neural Network (CNN) dengan arsitektur ResNet-50. Sistem ini dirancang khusus untuk mengklasifikasi kualitas fisik benih ikan mas secara otomatis guna mendukung produktivitas pembudidaya ikan di wilayah Kecamatan Karanggeneng, Lamongan.

## 🚀 Akses Aplikasi Ter-Deploy
Anda dapat langsung menggunakan aplikasi ini secara online tanpa perlu melakukan instalasi di komputer. Silakan kunjungi tautan berikut:
[Buka Petani_Abies AI di Streamlit](https://petanieabies-dvxihktoehoh4tab646vca.streamlit.app)

## 🔗 Tautan Resource Eksternal
Sistem ini terintegrasi dengan beberapa layanan cloud untuk menampung file berukuran besar dan merekam log data. Berikut adalah tautan publiknya:
* **File Model AI (.keras):** [Unduh model_petani_siap.keras dari Google Drive](https://drive.google.com/uc?id=1kcCLln1DIDCVyEC_Qw26k8fKu2clLI2f)
* **Database Laporan (Google Sheets):** [Akses Log Data Scan](https://docs.google.com/spreadsheets/d/1FjrDbsj0djlcytm3fAp1igNcM8SlDd3z5gPcrmaYEoI/edit?usp=sharing)

## 💻 Panduan Instalasi Lokal (Localhost)
Jika Anda ingin mengembangkan atau menjalankan aplikasi ini secara offline di laptop/komputer, ikuti langkah-langkah di bawah ini:

1. Unduh atau *Clone* repository ini ke komputer Anda.
2. Buka Terminal atau *Command Prompt* (CMD) dan arahkan ke dalam folder proyek ini.
3. Instal semua dependensi pustaka Python yang dibutuhkan dengan perintah berikut:
   `pip install -r requirements.txt`
4. Jalankan server lokal Streamlit dengan perintah:
   `streamlit run main.py`
5. Aplikasi akan otomatis terbuka di browser pada alamat default `http://localhost:8501`.

**Catatan Penting:** 
Saat dijalankan untuk pertama kalinya, kode akan otomatis mengunduh file model AI dari Google Drive. Pastikan koneksi internet Anda stabil saat proses *loading* pertama ini berlangsung.

---
#affan_owner# Petanie_Abies
