Berikut adalah draf `README.md` terbaru yang disesuaikan agar lebih umum, ringkas, dan mudah dipahami oleh pembaca non-teknis, namun tetap mencakup poin-poin yang Anda minta:

---

# 🚀 SIREDO (Sistem Rekomendasi Dosen)

SIREDO (Sistem Rekomendasi Dosen) adalah sebuah mesin pencari dan sistem rekomendasi berbasis Kecerdasan Buatan (AI) dan *Natural Language Processing* (NLP). Aplikasi ini dirancang khusus untuk membantu mahasiswa menemukan dosen pembimbing skripsi yang paling relevan dengan memetakan judul dan abstrak rencana skripsi ke daftar dosen berdasarkan rekam jejak penelitian mereka.

---

## 🧠 Metode yang Digunakan

Aplikasi ini menggunakan pendekatan hibrida (gabungan) agar rekomendasi yang dihasilkan akurat, baik secara tulisan maupun makna:

1. **Metode Leksikal (BM25):** Mencari kecocokan kata kunci secara persis antara teks yang diinputkan mahasiswa dengan profil penelitian dosen.
2. **Metode Semantik (SBERT):** Memahami makna dan konteks topik penelitian (kedekatan vektor) meskipun menggunakan pilihan kata yang berbeda.
3. **Pembobotan Adaptif:** AI secara otomatis menyeimbangkan kedua metode di atas berdasarkan tingkat kerumitan dan kelangkaan kata pada judul skripsi mahasiswa.

---

## 🏗️ Layer Aplikasi

Sistem SIREDO dibangun dengan arsitektur terstruktur yang terbagi menjadi beberapa lapisan (layer):

* **Layer Antarmuka Pengguna (Frontend):** Dibangun menggunakan Vue.js. Berfungsi sebagai halaman interaktif tempat pengguna memasukkan data dan melihat visualisasi proses pemikiran AI.
* **Layer API dan Komunikasi (Backend):** Dibangun menggunakan Python Flask. Bertugas sebagai jembatan komunikasi antara antarmuka pengguna dengan mesin cerdas di server.
* **Layer Kecerdasan Buatan (AI Core):** Pusat otak sistem yang melakukan pembersihan teks, perhitungan kemiripan (leksikal & semantik), serta pemeringkatan hasil.
* **Layer Pangkalan Data (Database):** Tempat penyimpanan data rekam jejak dosen yang dihubungkan menggunakan MySQL dan didukung format data Excel.

---

## 📂 Struktur Direktori (Root Tree)

Proyek ini dipisahkan menjadi dua bagian utama untuk menjaga kerapian kode:

```text
SIREDO/
│
├── client/                     # Folder Antarmuka Pengguna (Frontend Vue.js)
│   ├── src/                    # Berisi desain halaman dan logika tampilan web
│   └── package.json            # Daftar pustaka kebutuhan antarmuka
│
└── server/                     # Folder Peladen & Mesin AI (Backend Python)
    ├── data/                   # File data statis dan memori vektor AI
    ├── database/               # Logika koneksi ke MySQL 
    ├── app.py                  # Pintu masuk utama server dan jalur API
    ├── rekomendasi.py          # Otak pemrosesan sistem NLP dan pemeringkatan
    └── requirements.txt        # Daftar pustaka kebutuhan peladen

```

---

## 🛠️ Cara Instalasi & Menjalankan Aplikasi

**Persyaratan Sistem:**

* Python 3.9 atau lebih baru
* Node.js v16 atau lebih baru
* XAMPP / MySQL Server

### 1. Menyalakan Peladen (Backend)

1. Buka *Terminal* atau *Command Prompt* dan masuk ke dalam folder `server`.
2. Instal semua pustaka yang dibutuhkan dengan menjalankan perintah:
```bash
pip install -r requirements.txt

```


3. Nyalakan mesin peladen dengan perintah:
```bash
python app.py

```


*(Tunggu beberapa saat hingga mesin AI selesai dimuat)*

### 2. Menyalakan Antarmuka (Frontend)

1. Buka *Terminal* baru dan masuk ke dalam folder `client`.
2. Instal dependensi antarmuka dengan menjalankan perintah:
```bash
npm install

```


3. Jalankan aplikasi web dengan perintah:
```bash
npm run dev

```


4. Buka tautan lokal (biasanya `http://localhost:5173`) di *browser* (peramban) Anda untuk mulai menggunakan aplikasi SIREDO.