# SISTEM ANALISIS & EKSPLORASI DATA KARTU KREDIT NASABAH

Aplikasi web dashboard analitik interaktif berbasis **Python** dan **Streamlit** untuk mengeksplorasi, menganalisis, dan memvisualisasikan data portofolio kartu kredit nasabah secara mendalam. Proyek ini dikembangkan untuk memenuhi tugas mata kuliah **Praktikum Pengolahan dan Analisis Data (Bab 1 dan Bab 2)**.

---

## 👥 Identitas Pengembang (Kelompok 5)

- **Ridwan Ramadhani** — `241011400477` *(Mahasiswa Pengembang Utama)*
- **Sihabudin Firmansyah** — `241011400486`
- **Dendi Bayu Saputra** — `241011400468`

**Program Studi:** Teknik Informatika, Semester 5  
**Institusi:** Universitas Pamulang  

---

## 🚀 Gambaran Umum & Tujuan

Aplikasi ini menyajikan dashboard analisis data berstandar industri dengan tema **Modern Professional Analytics Dashboard** (dominan *Navy Blue* dan *Slate Light*). Sistem ini memungkinkan analis, mahasiswa, dan pemangku kepentingan untuk:
1. Mengetahui ringkasan eksekutif karakteristik portofolio nasabah (total nasabah, rata-rata limit kredit, dan kepemilikan kartu).
2. Memahami perilaku interaksi multichannel nasabah (*online banking*, kantor cabang fisik, dan panggilan layanan).
3. Melakukan pemfilteran data interaktif dan pemeriksaan statistik lima angka (*descriptive statistics*).
4. Menganalisis korelasi linier Pearson antarvariabel analitik menggunakan visualisasi heatmap interaktif.
5. Melakukan simulasi profil pengajuan nasabah baru secara eksploratif.
6. Mengelola dataset secara dinamis (unggah CSV alternatif, edit data tabel interaktif, unduh CSV terfilter/aktif, dan pemulihan data).

> **Pernyataan Kepatuhan & Akademik:**  
> Dataset tidak memuat label persetujuan (*approval*) kredit. Fitur simulasi dibuat murni untuk eksplorasi statistik data akademik, bukan sebagai rekomendasi resmi perbankan atau alat penilaian kelayakan risiko kredit resmi.

---

## 🛠️ Teknologi & Pustaka

| Teknologi / Pustaka | Fungsi Utama |
|---|---|
| **Python 3.10+** | Bahasa pemrograman utama |
| **Streamlit** | Framework web interaktif dan arsitektur dashboard responsif |
| **Pandas** | Manipulasi data tabular, pemfilteran, dan agregasi data |
| **NumPy** | Perhitungan numerik dan operasi matriks |
| **Matplotlib** | Pembuatan matriks korelasi heatmap beranotasi |
| **Altair** | Scatter plot interaktif dengan tooltip berbasis Vega-Lite |
| **Plotly Express** | Histogram distribusi dan box plot interaktif |

---

## 📁 Struktur Berkas Proyek

```text
credit-card-analysis/
│
├── app.py                            # Kode aplikasi utama (seluruh fitur terintegrasi)
├── Credit Card Customer Data.csv     # Dataset utama (660 baris, 7 kolom)
├── requirements.txt                  # Daftar dependensi pustaka Python
├── README.md                         # Dokumentasi lengkap proyek dan panduan deployment
├── .gitignore                        # Konfigurasi pengabaian file Git
└── Sistem_Analisis_Data_Kartu_Kredit.txt.txt # Dokumen spesifikasi teknis (PRD)
```

---

## 📊 Karakteristik Dataset

Dataset bawaan adalah **`Credit Card Customer Data.csv`** dengan 660 baris dan 7 kolom:

1. `Sl_No`: Nomor urut indeks data nasabah.
2. `Customer Key`: Kunci unik tanda pengenal nasabah (*string/identifier*, dilengkapi fitur *privacy masking*).
3. `Avg_Credit_Limit`: Rata-rata batas kredit nasabah.
4. `Total_Credit_Cards`: Jumlah kartu kredit aktif yang dimiliki nasabah.
5. `Total_visits_bank`: Frekuensi kunjungan langsung nasabah ke kantor cabang bank fisik.
6. `Total_visits_online`: Frekuensi akses nasabah melalui layanan *online / mobile banking*.
7. `Total_calls_made`: Jumlah panggilan yang dilakukan nasabah ke *customer care / call center*.

---

## 🧩 Modul & Fitur Utama

Aplikasi dibagi menjadi 7 modul navigasi pada sidebar:

1. **🏠 Dashboard Utama**  
   - 4 Kartu metrik utama: Total Nasabah, Rata-rata Batas Kredit, Rata-rata Kartu, dan Interaksi Multichannel.
   - Tabel ringkasan parameter dataset (baris, kolom, missing values, duplikat, min, max, median).
   - Diagram batang distribusi kepemilikan kartu kredit.
   - Analisis naratif otomatis kondisi dataset aktif.

2. **🔍 Eksplorasi Data**  
   - Tabel interaktif dataset lengkap dengan fitur penyamaran (*privacy masking*) Customer Key.
   - Panel filter interaktif (*multiselect* kartu, *slider* batas kredit, kunjungan bank, akses online, panggilan telepon).
   - Struktur data & inspeksi skema metadata JSON.
   - Kamus variabel lengkap dan tabel statistik deskriptif lima angka (Count, Mean, Std, Min, Q1, Median, Q3, Max).
   - Penelusuran nilai ekstrem (Top 5 dan Bottom 5) untuk setiap atribut numerik.

3. **📊 Visualisasi Data**  
   - **Line Chart**: Tren batas kredit berdasarkan kepemilikan kartu kredit.
   - **Area Chart**: Pola aktivitas saluran interaksi multichannel nasabah.
   - **Bar Chart**: Perbandingan batas kredit terhadap frekuensi kunjungan bank fisik.
   - **Altair Scatter Chart**: Hubungan aktivitas online dengan batas kredit dilengkapi *interactive tooltip*.
   - **Plotly Express**: Histogram distribusi batas kredit dan diagram box plot sebaran data.

4. **🔗 Analisis Korelasi**  
   - Matriks korelasi Pearson 5x5 antarvariabel numerik analitik.
   - Heatmap korelasi Matplotlib beranotasi angka dan skala warna intuitif.
   - Tabel koefisien korelasi dan interpretasi objektif hubungan positif/negatif.
   - Scatter plot hubungan kunci (Batas Kredit vs Jumlah Kartu & Batas Kredit vs Kunjungan Online).

5. **🧪 Simulasi Nasabah**  
   - Formulir interaktif pengajuan parameter profil nasabah baru (`st.form`).
   - Validasi input numerik non-negatif dan format identitas string.
   - Penyimpanan hasil simulasi ke `st.session_state`.
   - Diagram batang perbandingan metrik simulasi terhadap rata-rata portofolio aktif.

6. **⚙️ Pengelolaan Data**  
   - **Upload CSV**: Dukungan unggah file CSV alternatif dengan validasi struktur 7 kolom wajib.
   - **Data Editor**: Pengeditan nilai tabel interaktif langsung di peramban tanpa merusak file CSV fisik.
   - **Download CSV**: Opsi unduh Dataset Aktif, Dataset Hasil Filter, dan Hasil Simulasi.
   - **Reset Data**: Tombol pemulihan instan kembali ke data bawaan asli.

7. **ℹ️ Tentang Aplikasi**  
   - Informasi tim pengembang Kelompok 5 Universitas Pamulang.
   - Spesifikasi pustaka perangkat lunak.
   - Ringkasan dataset aktual dan penafian akademik (*academic disclaimer*).

---

## 💻 Panduan Menjalankan Secara Lokal

### 1. Persyaratan Sistem
- Pastikan komputer telah terinstal **Python 3.10** atau versi lebih baru.
- Terminal / Command Prompt / PowerShell.

### 2. Kloning atau Buka Direktori Proyek
Buka terminal dan arahkan ke direktori proyek:
```bash
cd "c:/WEB RIDWAN/Credit Card Customer Data"
```

### 3. (Opsional) Buat dan Aktifkan Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalasi Dependensi Pustaka
Jalankan perintah berikut:
```bash
pip install -r requirements.txt
```

### 5. Menjalankan Aplikasi Web
Eksekusi perintah Streamlit:
```bash
streamlit run app.py
```

Aplikasi akan otomatis terbuka di peramban web default Anda pada alamat:
```text
http://localhost:8501
```

---

## ☁️ Panduan Deployment ke GitHub & Streamlit Community Cloud

Aplikasi telah dirancang menggunakan path relatif aman (`Path(__file__).resolve().parent`) sehingga **100% siap dipublikasikan secara daring (*cloud deployment*)**.

### Langkah A: Unggah ke GitHub
1. Masuk ke akun [GitHub](https://github.com).
2. Buat repository baru (contoh: `credit-card-analysis`), pilih opsi **Public**.
3. Inisialisasi Git pada folder lokal dan unggah:
   ```bash
   git init
   git add .
   git commit -m "feat: initial commit credit card analysis web dashboard"
   git branch -M main
   git remote add origin https://github.com/USERNAME/credit-card-analysis.git
   git push -u origin main
   ```
4. Pastikan file `app.py`, `Credit Card Customer Data.csv`, dan `requirements.txt` berada di *root directory* repositori.

### Langkah B: Publikasikan ke Streamlit Community Cloud
1. Kunjungi [Streamlit Community Cloud](https://share.streamlit.io).
2. Masuk menggunakan akun GitHub yang terhubung.
3. Klik tombol **New app**.
4. Isi konfigurasi aplikasi:
   - **Repository:** Pilih repositori GitHub Anda (misal `USERNAME/credit-card-analysis`).
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Klik **Deploy!**
6. Tunggu proses instalasi dependensi selesai. Dalam 1-2 menit, URL publik aplikasi Anda akan aktif dan dapat diakses siapa saja.

---

## 🔒 Kebijakan Keamanan & Privasi Data Publik

1. **Pencegahan Kebocoran Identitas:**  
   Pada modul Eksplorasi Data, atribut `Customer Key` secara default disamarkan (*masked*, contoh: `***073`) untuk melindungi privasi data nasabah saat aplikasi diakses di domain publik.
2. **Integritas File Asli:**  
   Seluruh operasi manipulasi data (penambahan baris, pengeditan nilai di *Data Editor*, dan unggah berkas alternatif) disimpan secara terisolasi di dalam `st.session_state` memori sesi dan **tidak pernah mengubah atau menimpa berkas `Credit Card Customer Data.csv` asli di penyimpanan komputer**.
3. **Bebas Kredensial Rahasia:**  
   Kode sumber bersih dari kata sandi, token otentikasi, maupun API Key privat.

---

## ❓ Penanganan Kendala Umum (Troubleshooting)

| Gejala Error | Penyebab Potensial | Solusi |
|---|---|---|
| `FileNotFoundError` | File CSV tidak berada di folder yang sama dengan `app.py`. | Pastikan file bernama persis `Credit Card Customer Data.csv` dan diletakkan bersebelahan dengan `app.py`. |
| `ModuleNotFoundError` | Pustaka belum terinstal di lingkungan Python aktif. | Jalankan `pip install -r requirements.txt`. |
| Tabel kosong setelah filter | Kriteria filter terlalu sempit sehingga tidak ada data yang cocok. | Klik tombol **Reset Filter** pada panel filter di menu Eksplorasi Data. |
| Perubahan data tidak terlihat | Belum menekan tombol simpan perubahan. | Pada tab Edit Data, klik tombol **Simpan Perubahan ke Sesi Aktif**. |

---

*Hak Cipta © 2026 Kelompok 5 — Teknik Informatika Universitas Pamulang.*
