# 🚲 Bike Sharing Analysis Dashboard

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📌 Overview

Proyek ini merupakan **dashboard analisis data penyewaan sepeda (Bike Sharing)** yang dikembangkan sebagai bagian dari *submission* tugas akhir **Dicoding – Belajar Analisis Data dengan Python**.

Dashboard ini menyajikan visualisasi data interaktif untuk membantu memahami:

* Pola dan tren penyewaan sepeda
* Pengaruh kondisi cuaca terhadap jumlah penyewaan
* Perbandingan perilaku pengguna **Casual** dan **Registered**

## 📂 Project Structure

```text
.
├── dashboard
│   ├── dashboard.py      # File utama aplikasi Streamlit
│   └── main_data.csv     # Dataset bersih hasil cleaning & processing
├── data
│   ├── day.csv           # Dataset mentah (harian)
│   └── hour.csv          # Dataset mentah (per jam)
├── notebook.ipynb        # Jupyter Notebook untuk Exploratory Data Analysis (EDA)
├── README.md             # Dokumentasi proyek
└── requirements.txt      # Daftar library Python yang dibutuhkan
```

## 🚀 Getting Started

Ikuti langkah-langkah berikut untuk menjalankan dashboard secara lokal.

### 1. Clone Repository

```bash
git clone https://github.com/nfldffa/Bike-Sharing-Dashboard.git
cd Bike-Sharing-Dashboard
```

### 2. Setup Environment

Buat dan aktifkan *virtual environment*.

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Mac / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Streamlit App

```bash
streamlit run dashboard/dashboard.py
```

Setelah perintah dijalankan, dashboard akan otomatis terbuka di browser.

## 📊 Key Insights & Business Questions

Dashboard ini dirancang untuk menjawab tiga pertanyaan bisnis utama:

### 1️⃣ Bagaimana tren penyewaan sepeda?

* Terjadi peningkatan jumlah penyewaan yang signifikan pada **tahun 2012** dibandingkan **2011**.
* Aktivitas penyewaan tertinggi terjadi pada **bulan September**.
* Terjadi penurunan drastis pada **musim dingin (Desember)**.

### 2️⃣ Seberapa besar pengaruh kondisi cuaca?

* Kondisi **cerah / berawan** sangat mendukung tingginya jumlah penyewaan sepeda.
* Kondisi **hujan atau salju** menurunkan minat penyewa secara signifikan (lebih dari **50%**).

### 3️⃣ Bagaimana pola jam sibuk (Rush Hour)?

* Puncak penyewaan terjadi pada **pukul 08.00 (pagi)** dan **17.00 (sore)**.
* Pola ini mengindikasikan bahwa sepeda banyak digunakan sebagai sarana **transportasi harian (commuting)** untuk bekerja atau sekolah.

## 👤 Author

**Naufal Daffa Erlangga**

---

