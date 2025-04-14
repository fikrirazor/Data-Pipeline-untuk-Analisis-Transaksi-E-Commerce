# Olist E-commerce ETL Pipeline

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
<!--- ![Status](https://img.shields.io/badge/Status-Completed-green) -->
![Status](https://img.shields.io/badge/Status-In_Progress-yellow)
## 📌 Overview
Proyek ini mengembangkan *end-to-end data pipeline* untuk menganalisis transaksi e-commerce menggunakan dataset **Olist**, platform e-commerce dari Brasil. Pipeline mencakup proses ETL (Extract, Transform, Load) untuk menghasilkan wawasan bisnis seperti tren penjualan bulanan dan kategori produk terlaris.

Proyek ini relevan dalam memahami dinamika e-commerce, termasuk di Indonesia yang mengalami pertumbuhan pesat dengan GMV mencapai **$65 miliar** pada tahun 2024 [(Google, 2024)](https://blog.google/intl/id-id/e-conomy-sea-2024-perekonomian-digital-indonesia-akan-mencapai-gmv-90-miliar-pada-tahun-2024/).

## 🎯 Tujuan
- Mengotomatisasi proses pengumpulan, pembersihan, dan penyimpanan data e-commerce.
- Menganalisis tren penjualan bulanan dan kategori produk terlaris.
- Menyediakan visualisasi data yang mendukung pengambilan keputusan strategis.

## 🗂️ Dataset
Dataset Olist tersedia di [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) dan berisi lebih dari 100.000 transaksi. Tabel yang digunakan:
- **orders**: Informasi pesanan (ID, tanggal pembelian, status).
- **customers**: Informasi pelanggan (ID, kota, negara bagian).
- **products**: Kategori, nama, dan harga produk.
- **payments**: Jenis pembayaran, nilai, dan cicilan.
- **order_reviews**: Skor dan komentar ulasan pelanggan.
- **geolocation**: Koordinat geografis pelanggan.

## 🛠️ Tools & Libraries
- Python 3.8+
- Jupyter Notebook
- Pandas
- NumPy
- Matplotlib

## 📦 Prasyarat
Pastikan Python 3.8+ telah terinstal, lalu jalankan:

```bash
pip install pandas numpy matplotlib
```

Unduh dataset Olist dari Kaggle dan simpan di folder `data/`.

## 📁 Struktur Proyek
```
olist-ecommerce-etl-pipeline/
├── data/                    # Dataset Olist (CSV files)
├── notebooks/               # Jupyter Notebooks untuk ETL dan EDA
├── visualizations/          # Output visualisasi (PNG)
├── requirements.txt         # Daftar dependensi
├── LICENSE                  # Lisensi proyek
└── README.md                # Dokumentasi proyek
```

## ⚙️ Langkah-langkah Proses

### 1. Preprocessing
- **Penggabungan Data**: Integrasi antar tabel menggunakan `order_id` dan `customer_id`.
- **Konversi Tipe Data**: Mengubah kolom waktu ke format `datetime`.
- **Pembersihan Data**:
  - Menangani nilai hilang dan duplikat.
  - Normalisasi format harga, kategori, dan tanggal.
- **Validasi Data**: Memastikan konsistensi, seperti tanggal pesanan valid.

### 2. Exploratory Data Analysis (EDA)
- **Tren Penjualan Bulanan**:
  - Mengelompokkan penjualan berdasarkan bulan.
  - Menemukan bulan dengan penjualan tertinggi/terendah.
- **Analisis Kategori Produk**:
  - Mengidentifikasi kategori produk terlaris berdasarkan jumlah pesanan.
- **Visualisasi**:
  - Line chart untuk tren penjualan bulanan.
  - Bar chart untuk distribusi penjualan per kategori.

### 3. Visualisasi
Contoh hasil visualisasi disimpan di folder `visualizations/`, seperti:

- ![Tren Penjualan Bulanan](visualizations/sales_trend.png)
- ![Kategori Produk Terlaris](visualizations/top_categories.png)

## ✅ Hasil
- Pipeline ETL otomatis untuk analisis e-commerce.
- Wawasan tren penjualan bulanan dan pola musiman.
- Analisis kategori produk terlaris.
- Notebook interaktif untuk eksplorasi data dan dokumentasi proses.

## ▶️ Cara Menjalankan

1. **Clone repositori**:
```bash
git clone https://github.com/<username>/olist-ecommerce-etl-pipeline.git
```

2. **Masuk ke direktori proyek**:
```bash
cd olist-ecommerce-etl-pipeline
```

3. **Instal dependensi**:
```bash
pip install -r requirements.txt
```

4. **Jalankan Jupyter Notebook**:
```bash
jupyter notebook notebooks/olist_analysis.ipynb
```

## 🧭 Rencana Pengembangan
- Menambahkan analisis **RFM** (Recency, Frequency, Monetary) untuk segmentasi pelanggan.
- Integrasi dengan **PostgreSQL** untuk penyimpanan skala besar.
- Pengembangan dashboard interaktif menggunakan **Streamlit** atau **Power BI**.
- Implementasi **prediksi penjualan** menggunakan machine learning.

## 📝 Lisensi
Proyek ini menggunakan lisensi **MIT**. Lihat file [LICENSE](LICENSE) untuk informasi lebih lanjut.

## 📬 Kontak 
- 💻 GitHub: [github.com/fikrirazor](https://github.com/fikrirazor)  

## 📚 Referensi
- Google. (2024). *e-Conomy SEA 2024: Perekonomian digital Indonesia akan mencapai GMV 90 miliar pada tahun 2024*.  
  [Link](https://blog.google/intl/id-id/e-conomy-sea-2024-perekonomian-digital-indonesia-akan-mencapai-gmv-90-miliar-pada-tahun-2024/)
- Olist. (2018). *Brazilian E-commerce Public Dataset*.  
  [Kaggle Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

