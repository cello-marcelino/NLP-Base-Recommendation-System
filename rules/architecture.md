# Architecture & Design Rules for AI Agents

Aturan struktur proyek, arsitektur modul/layer, dan prinsip desain sistem. Berlaku saat membuat atau mengubah file, struktur module, class, atau layer.

---

## 1. Tujuan & Filosofi Utama (Purpose & Core Principles)

AI Agent wajib mempertahankan struktur proyek yang mudah diprediksi (*predictable*), terukur (*scalable*), dan mudah dipelihara (*maintainable*).

Sebelum membuat, memindahkan, atau mengubah nama file, periksa struktur repositori yang ada dan ikuti konvensi yang sudah berjalan. Jangan memperkenalkan pola arsitektur baru kecuali struktur saat ini benar-benar membutuhkannya.

### Prinsip Utama:
1. **KISS (Keep It Simple, Stupid)**
   - Gunakan solusi paling sederhana yang menyelesaikan masalah dengan benar.
   - Jangan menambahkan abstraksi tanpa kebutuhan nyata.
   - Jangan menggunakan design pattern hanya karena pattern tersebut tersedia.
   - Jangan memperkenalkan infrastruktur kompleks sebelum diperlukan.

2. **YAGNI (You Aren't Gonna Need It)**
   - Jangan implementasikan fitur yang belum dibutuhkan.
   - Jangan membuat generic abstraction untuk kebutuhan hipotetis masa depan.
   - Jangan melakukan optimasi sebelum ada bottleneck yang terukur.

3. **DRY (Don't Repeat Yourself) & SSOT**
   - Hindari duplikasi business logic, selalu miliki *Single Source of Truth*.
   - Jangan abstraksi hanya karena dua bagian kode terlihat mirip secara kebetulan.
   - Jika dua kode memiliki alasan perubahan yang berbeda, duplikasi dapat diterima.

4. **Predictability & Naming Clarity**
   - Letakkan file di lokasi yang secara natural diharapkan oleh developer lain.
   - Gunakan nama folder konvensional dan eksplisit seperti `config`, `modules`, `tests`, `docs`, dan `scripts`.
   - Dilarang membuat folder ambigu seperti `misc`, `stuff`, `random`, `temp`, atau `helpers` sebagai tempat pembuangan kode.

5. **Separation of Concerns & Single Responsibility**
   - Pisahkan logika bisnis, konfigurasi, infrastruktur, UI/Views, test, script, dan asset statis.
   - Setiap modul, class, dan fungsi harus memiliki satu tanggung jawab yang jelas.
   - Jangan pernah menaruh secrets, konfigurasi environment, atau konfigurasi deployment bersebelahan dengan domain logic aplikasi.

6. **Consistency Over Creativity**
   - Ikuti konvensi penamaan, import, struktur test, dan modul yang sudah ada di repositori.
   - Utamakan penamaan yang deskriptif dan baku dibandingkan penamaan yang unik/kreatif tapi ambigu.
   - Gunakan nama direktori berhuruf kecil (*lowercase*) kecuali konvensi bahasa/framework menentukan lain.

7. **Feature Cohesion & Low Coupling**
   - Kelompokkan kode yang menangani kapabilitas bisnis yang sama saling berdekatan (*feature/domain-first*).
   - Hindari dependensi sirkular (*circular dependency*) antar modul.
   - Modul harus bergantung pada interface/contract yang stabil, bukan detail implementasi internal modul lain.

---

## 2. Standar Layout Repositori (Standard Repository Layout)

Gunakan layout standar ini saat membuat proyek umum baru (kecuali framework memiliki aturan struktur bawaan yang berbeda):

```text
project/
├── src/
│   ├── core/
│   ├── modules/
│   ├── utils/
│   ├── config/
│   └── main.*
├── tests/
├── public/
├── scripts/
├── docs/
├── .env.example
├── .gitignore
├── README.md
└── package.json | requirements.txt | go.mod | pom.xml | equivalent
```

### Tanggung Jawab Direktori:

| Direktori | Tanggung Jawab |
|---|---|
| `src/` | Kode sumber aplikasi production |
| `src/core/` | Fondasi bersama aplikasi: interfaces, error handling dasar, abstraksi base, bootstrapping logic |
| `src/modules/` | Modul fitur atau domain bisnis |
| `src/utils/` | Utilitas kecil, generik, dan stateless tanpa domain bisnis |
| `src/config/` | Validasi dan adapter konfigurasi bertipe (*typed config loading*) |
| `tests/` | Pengujian yang tidak ditempatkan bersama modul fitur (misal: E2E/Integration test lintas fitur) |
| `public/` | Asset statis yang diekspos langsung ke klien/pengguna |
| `scripts/` | Skrip otomasi satu kali (*one-off*), migrasi, build, atau operasional/maintenance |
| `docs/` | Dokumentasi arsitektur, catatan keputusan (ADR), API docs, dan panduan kontribusi |

---

## 3. Aturan Proyek Kecil (Small Project Rules)

Untuk proyek berukuran kecil, mulai dengan struktur paling minimal:

```text
project/
├── src/
│   └── main.*
├── tests/
└── README.md
```

> **Aturan**: Jangan membuat folder `core`, `modules`, `utils`, `config`, `scripts`, atau `docs` sebelum ada kode atau dokumentasi nyata yang membutuhkannya.

---

## 4. Struktur Modul Fitur (Feature Module Rules)

Ketika aplikasi menangani beberapa domain/fitur bisnis, organisasikan kode berbasis fitur (*Feature/Domain-driven*):

```text
src/
├── modules/
│   ├── auth/
│   │   ├── auth.controller.*
│   │   ├── auth.service.*
│   │   ├── auth.repository.*
│   │   ├── auth.model.*
│   │   ├── auth.routes.*
│   │   └── auth.test.*
│   ├── users/
│   │   ├── users.controller.*
│   │   ├── users.service.*
│   │   ├── users.repository.*
│   │   ├── users.model.*
│   │   ├── users.routes.*
│   │   └── users.test.*
│   └── dashboard/
│       ├── dashboard.controller.*
│       ├── dashboard.service.*
│       └── dashboard.test.*
```

### Prinsip Modul:
- Setiap modul mewakili satu kapabilitas bisnis (misal: `auth`, `users`, `billing`, `orders`).
- Modul memiliki dan mengontrol detail implementasi internalnya sendiri.
- Utamakan import di dalam modul yang sama sebelum mengimpor dari modul fitur lain.
- **Dilarang** mengakses database model internal, private service, atau file privat milik modul lain secara langsung.
- Hanya ekspos antarmuka publik yang memang dirancang untuk dibagikan antar modul.
- Tempatkan test unit fitur sedekat mungkin dengan modul terkait (*colocated tests*).

---

## 5. Pemisahan Layer di Dalam Fitur (Layering Rules)

Di dalam modul fitur, pertahankan pemisahan tanggung jawab layer yang tegas:

```
Routes -> Controller/Handler -> Service/Use Case -> Repository/Data Access -> Database / External
```

- **Controller / Handler**: Menerima request transport, memvalidasi input transport-level, dan mengembalikan respons format DTO. Dilarang berisi business logic atau query database langsung.
- **Service / Use Case**: Menampung business rules, alur kerja (orchestration), dan domain logic. Tidak boleh bergantung langsung pada response objek HTTP framework.
- **Repository / Data Access**: Menangani operasi baca/tulis ke sumber data (Database, cache, external storage). Tidak boleh menentukan aturan bisnis.
- **Model / Entity**: Merepresentasikan struktur data domain atau persistensi. Dilarang memuat kode HTTP, UI, atau framework transport.
- **Routes**: Menghubungkan endpoint URL / method ke controller terkait.
- **Test**: Memverifikasi fungsionalitas dan perilaku fitur secara terisolasi.

---

## 6. Pengelolaan Kode Bersama (Shared Code Rules)

Sebelum membuat modul/utilitas bersama, evaluasi:

> *Apakah kode ini benar-benar digunakan ulang oleh banyak modul independen yang tidak saling berhubungan?*

- Jika **TIDAK**: Simpan kode di dalam modul fitur pemiliknya.
- Jika **YA**: Tempatkan di lokasi bersama paling minimal, seperti `src/core/` atau `src/utils/`.
- **Jangan** memindahkan kode ke `utils` hanya karena bingung menentukan tempatnya.
- Utilitas (`utils`) wajib bersifat **generik dan stateless**. Helper khusus domain bisnis tetap menjadi milik modul fiturnya.

---

## 7. Konfigurasi & Kredensial (Configuration & Secrets)

- Logika pemuatan konfigurasi wajib berada di `src/config/`.
- Baca seluruh environment variable melalui layer konfigurasi terpusat dan lakukan validasi tipe saat startup.
- **Dilarang keras** menaruh hardcoded secrets, token, password, API key, atau private URL di dalam kode sumber.
- **Dilarang** melakukan commit file `.env` yang berisi kredensial nyata.
- Sediakan `.env.example` dengan nilai placeholder dan deskripsi variabel yang dibutuhkan.

---

## 8. Aturan Direktori Root (Root Directory Rules)

Jaga direktori root tetap bersih dan minimal. File yang diizinkan berada di root umumnya meliputi:

```text
README.md
.gitignore
.env.example
package.json / package-lock.json / pnpm-lock.yaml / yarn.lock
requirements.txt / pyproject.toml
go.mod / go.sum
pom.xml / build.gradle
Dockerfile / docker-compose.yml
Makefile
```

- **Dilarang** menaruh file kode sumber aplikasi langsung di root folder.
- **Dilarang** membuat file cadangan berbasis nama (seperti `utils-final.*`, `utils-new.*`, `index-old.*`, `backup.*`). Gunakan Git version control.

---

## 9. Aturan Pengujian & Dokumentasi (Test & Docs Rules)

### Pengujian:
- Buat atau perbarui test setiap kali perilaku kode berubah.
- Beri nama test sesuai perilaku (*behavior*) atau unit yang diuji.
- Tempatkan test fixture/mock sedekat mungkin dengan test terkait.
- Dilarang menaruh kode produksi di direktori `tests/`.

### Dokumentasi:
- Perbarui `README.md` saat terjadi perubahan pada setup, env variables, perintah run/build/test, atau endpoint publik.
- Gunakan direktori `docs/` untuk dokumentasi teknis mendalam:
  ```text
  docs/
  ├── architecture.md
  ├── decisions/ (ADR)
  ├── api/
  └── deployment.md
  ```

---

## 10. Evolusi Kompleksitas Arsitektur & ADR

### Alur Evolusi Arsitektur
Gunakan arsitektur paling sederhana yang memenuhi kebutuhan saat ini. Jangan melompati tahap tanpa bukti beban terukur:
```
Simple Application -> Modular Application -> Modular Monolith
-> Horizontal Scaling -> Service Extraction -> Microservices
```

### Architecture Decision Record (ADR)
Keputusan arsitektur yang sulit dibalik dan berdampak besar wajib didokumentasikan di `docs/decisions/` menggunakan format:
```text
ADR-00X: [Judul Keputusan]
Status: [Proposed / Accepted / Deprecated]
Context: [Latar belakang masalah]
Decision: [Keputusan teknis yang diambil]
Consequences: [Dampak positif & negatif]
Rejected Options: [Opsi lain yang dipertimbangkan beserta alasan penolakan]
```
> Gunakan skill `write-adr` untuk membuat ADR baru.

---

## 11. Checklist Pembuatan File (File Creation Checklist)

Sebelum membuat file baru, tanyakan 5 pertanyaan ini:
1. **Fitur/domain apa yang memiliki tanggung jawab atas perilaku ini?**
2. **Apakah ini kode produksi, kode test, konfigurasi, dokumentasi, otomasi, atau aset statis?**
3. **Apakah sudah ada file dengan fungsi setara yang bisa digunakan/diperluas?**
4. **Bisakah kode ini diletakkan di dalam modul yang sudah ada tanpa membuat folder baru?**
5. **Apakah nama file sudah mendeskripsikan tanggung jawabnya secara jelas dan tidak ambigu?**

---

## 12. Larangan Mutlak (Prohibited Actions)

AI Agent **DILARANG**:
- Membuat folder secara spekulatif untuk fitur masa depan yang belum diminta (*YAGNI violation*).
- Mencampuradukkan konfigurasi/secret dengan logika aplikasi.
- Memasukkan kode yang tidak saling terkait ke dalam `utils`, `helpers`, atau `common`.
- Membuat folder global `controllers/`, `services/`, atau `models/` ketika proyek sudah menggunakan pendekatan modular per-fitur.
- Membuat dependensi sirkular (*circular dependency*) antar modul.
- Memindahkan file hanya demi estetika tanpa memperbarui path import, test, dan dokumentasi.
- Mengubah nama file tanpa memperbarui referensi di seluruh codebase.
- Membuat implementasi ganda (*duplicate code*) saat modul yang ada sudah menangani behavior tersebut.

---

## 13. Aturan Keputusan Lokasi Kode (Agent Decision Hierarchy)

Saat menentukan ke mana sebuah kode harus ditempatkan, gunakan urutan prioritas ini:
1. **Konvensi modul fitur yang sudah ada (*Existing feature module convention*)**
2. **Konvensi repositori yang sudah berjalan (*Existing repository convention*)**
3. **Kepemilikan fitur/domain (*Feature/domain ownership*)**
4. **Pemisahan tanggung jawab yang jelas (*Clear separation of responsibility*)**
5. **Penambahan struktur seminimal mungkin (*Minimal additional structure*)**

> *Bila ragu, pilih perubahan paling minimal yang tetap menjaga konsistensi codebase.*
