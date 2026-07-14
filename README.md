# Scraper Hadis Matematika

Script Python untuk mengumpulkan **hadis-hadis yang berkaitan dengan konsep matematika** (hitungan, bilangan, pecahan, zakat, waris, dll.) dari [API myquran.com v3](https://api.myquran.com/v3), lalu menyimpannya ke dalam file CSV.

## ✨ Fitur

- Mencari hadis berdasarkan **14 kata kunci matematis**, di antaranya:
  - `hitung`, `bilangan`, `angka`, `jumlah`
  - `timbangan`, `ukuran`
  - `separuh`, `setengah`, `sepertiga`, `dua pertiga`
  - `zakat`, `warisan`, `waris`, `nisab`
- Mengambil **semua halaman hasil pencarian** secara otomatis untuk tiap kata kunci (pagination)
- **Deduplikasi otomatis** — hadis yang sama (berdasarkan `id`) tidak akan tersimpan dua kali meskipun muncul di beberapa kata kunci
- Penanganan **rate limit (HTTP 429)** — script akan menunggu otomatis lalu mencoba ulang
- Jeda antar request (1 detik) dan antar kata kunci (1.5 detik) untuk menghindari pembatasan API
- Progress ditampilkan secara real-time di terminal (halaman ke berapa, jumlah hadis terkumpul)

## 📦 Data yang Diambil

Untuk setiap hadis yang ditemukan, script menyimpan kolom berikut:

| Kolom | Keterangan |
|---|---|
| `keyword_pencarian` | Kata kunci yang menghasilkan hadis ini |
| `id` | ID unik hadis dari API myquran.com |
| `teks_indonesia` | Teks terjemahan hadis dalam Bahasa Indonesia |

## 🛠️ Instalasi

Pastikan Python 3.7+ sudah terpasang, lalu install dependency yang dibutuhkan:

```bash
pip install requests
```

## 🚀 Cara Menggunakan

Jalankan script secara langsung:

```bash
python scrape_hadis_matematika.py
```

Data akan tersimpan otomatis ke `hadis_matematika_1.csv` di folder yang sama dengan script.

Jika ingin menyesuaikan daftar kata kunci pencarian, ubah list `KEYWORDS` di bagian atas file:

```python
KEYWORDS = [
    "hitung",
    "bilangan",
    "angka",
    # tambahkan kata kunci lain di sini
]
```

## ⚠️ Catatan & Etika Scraping

- Script ini menggunakan jeda antar request untuk mengurangi beban pada API dan menghormati batas rate limit yang diterapkan.
- Data hadis diambil dari [api.myquran.com](https://api.myquran.com/), gunakan sesuai dengan ketentuan penggunaan API tersebut.
- Hasil pencarian bergantung pada kata kunci yang tersedia di database API; script tidak melakukan verifikasi keabsahan (sanad/derajat) hadis secara otomatis — disarankan untuk memverifikasi ulang dari sumber rujukan hadis yang terpercaya sebelum digunakan untuk keperluan keagamaan.
- Struktur response API dapat berubah sewaktu-waktu, yang berpotensi memerlukan penyesuaian pada logika parsing.

## 📄 Lisensi

Silakan gunakan dan modifikasi script ini secara bebas untuk keperluan riset, edukasi, atau pengembangan aplikasi terkait.
