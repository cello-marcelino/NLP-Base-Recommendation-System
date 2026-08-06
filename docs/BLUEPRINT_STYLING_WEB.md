# 🎨 Blueprint Styling Web — SiReDo (NLP-Based Recommendation System)

> **Versi:** V2 Refactored | **Tanggal:** Juli 2026  
> Dokumen ini adalah panduan styling **word-for-word dari source code frontend**. Setiap warna, spacing, border-radius, tipografi, dan animasi dicatat persis dari file `.vue`. Implementasi dengan dokumen ini akan menghasilkan tampilan yang **identik piksel demi piksel**.

---

## 📌 Daftar Isi

1. [Stack Teknologi Frontend](#1-stack-teknologi-frontend)
2. [Design Token — Sistem Warna](#2-design-token--sistem-warna)
3. [Design Token — Tipografi](#3-design-token--tipografi)
4. [Design Token — Spacing, Radius, Shadow](#4-design-token--spacing-radius-shadow)
5. [Layout Global & Shell Aplikasi](#5-layout-global--shell-aplikasi)
6. [Komponen: Status Bar (Top Bar)](#6-komponen-status-bar-top-bar)
7. [Komponen: Navbar](#7-komponen-navbar)
8. [Komponen: Toast Notification](#8-komponen-toast-notification)
9. [Halaman Rekomendasi — Left Panel (Form Input)](#9-halaman-rekomendasi--left-panel-form-input)
10. [Komponen: Pipeline Stepper (Right Panel)](#10-komponen-pipeline-stepper-right-panel)
11. [Komponen: DosenCard (Table Row)](#11-komponen-dosencard-table-row)
12. [Komponen: XAI Modal](#12-komponen-xai-modal)
13. [Halaman Admin Panel](#13-halaman-admin-panel)
14. [Animasi & Transisi](#14-animasi--transisi)
15. [Custom CSS & Scrollbar](#15-custom-css--scrollbar)
16. [Color Coding Semantik per Komponen AI](#16-color-coding-semantik-per-komponen-ai)
17. [Kamus Kelas Tailwind → Nilai CSS Nyata](#17-kamus-kelas-tailwind--nilai-css-nyata)

---

## 1. Stack Teknologi Frontend

| Teknologi | Versi | Peran |
|---|---|---|
| **Vue.js** | `^3.5.34` | Framework UI reaktif |
| **Vite** | `^8.0.12` | Build tool & dev server |
| **Tailwind CSS** | `^4.3.0` | Utility-first CSS framework |
| **@tailwindcss/vite** | `^4.3.0` | Plugin Vite untuk Tailwind v4 |
| **vue-router** | `^5.1.0` | Client-side routing |

> **PENTING — Tailwind v4:** Sistem ini menggunakan **Tailwind CSS v4**, bukan v3. Konfigurasi dilakukan via `@theme {}` block di dalam CSS file — **bukan** melalui `tailwind.config.js`. Tidak ada file konfigurasi JS terpisah.

**Entry Point:** `client/src/main.js` → import `client/src/assets/main.css`

---

## 2. Design Token — Sistem Warna

### 2.1 Cara Konfigurasi (Tailwind v4 — `src/assets/main.css`)

```css
@import "tailwindcss";

@theme {
  /* Color Alias: primary = teal */
  --color-primary-50:  var(--color-teal-50);
  --color-primary-100: var(--color-teal-100);
  --color-primary-200: var(--color-teal-200);
  --color-primary-300: var(--color-teal-300);
  --color-primary-400: var(--color-teal-400);
  --color-primary-500: var(--color-teal-500);
  --color-primary-600: var(--color-teal-600);
  --color-primary-700: var(--color-teal-700);
  --color-primary-800: var(--color-teal-800);
  --color-primary-900: var(--color-teal-900);
  --color-primary-950: var(--color-teal-950);

  /* Color Alias: surface = slate */
  --color-surface-50:  var(--color-slate-50);
  --color-surface-100: var(--color-slate-100);
  --color-surface-200: var(--color-slate-200);
  --color-surface-300: var(--color-slate-300);
  --color-surface-400: var(--color-slate-400);
  --color-surface-500: var(--color-slate-500);
  --color-surface-600: var(--color-slate-600);
  --color-surface-700: var(--color-slate-700);
  --color-surface-800: var(--color-slate-800);
  --color-surface-900: var(--color-slate-900);
  --color-surface-950: var(--color-slate-950);
}
```

### 2.2 Palet Warna Nyata (Hex Referensi)

#### Palette Primary (Teal) — Aksen Utama Sistem
| Token | Kelas Tailwind | Hex |
|---|---|---|
| primary-50 | `bg-primary-50` | `#f0fdfa` |
| primary-100 | `bg-primary-100` | `#ccfbf1` |
| primary-200 | `bg-primary-200` | `#99f6e4` |
| primary-400 | `text-primary-400` | `#2dd4bf` |
| primary-500 | `bg-primary-500` | `#14b8a6` |
| **primary-600** | `bg-primary-600` | **`#0d9488`** ← Warna tombol utama |
| primary-700 | `bg-primary-700` | `#0f766e` |
| primary-900 | `text-primary-900` | `#134e4a` |

#### Palette Surface (Slate) — Warna Teks & Background Netral
| Token | Kelas Tailwind | Hex |
|---|---|---|
| surface-50 | `bg-surface-50` | `#f8fafc` ← Background halaman |
| surface-100 | `bg-surface-100` | `#f1f5f9` |
| surface-200 | `border-surface-200` | `#e2e8f0` ← Border umum |
| surface-300 | `text-surface-300` | `#cbd5e1` |
| surface-400 | `text-surface-400` | `#94a3b8` ← Placeholder & label |
| surface-500 | `text-surface-500` | `#64748b` ← Teks deskripsi |
| surface-600 | `text-surface-600` | `#475569` |
| surface-700 | `text-surface-700` | `#334155` ← Label form |
| **surface-800** | `text-surface-800` | **`#1e293b`** ← Teks heading utama |
| **surface-900** | `bg-surface-900` | **`#0f172a`** ← Background status bar |
| surface-950 | `bg-surface-950` | `#020617` |

#### Warna Aksen Tambahan (Non-kustom — dari Tailwind default)
| Peran | Kelas | Hex |
|---|---|---|
| **BM25 (Lexical)** — badge, progress bar, teks | `text-blue-500 / 600`, `bg-blue-50 / 100` | `#3b82f6 / #2563eb` |
| **SBERT (Semantic)** — badge, progress bar, teks | `text-fuchsia-500 / 600`, `bg-fuchsia-50 / 100` | `#d946ef / #c026d3` |
| **Sukses / Server Ready** | `bg-emerald-500`, `text-emerald-400` | `#10b981` |
| **Error / Offline** | `bg-red-500`, `text-red-400 / 700` | `#ef4444` |
| **Amber (Warning/Sinonim)** | `bg-amber-50`, `text-amber-500 / 700` | `#f59e0b` |
| **Highlight Sukses Toast** | `bg-green-50`, `border-green-200`, `text-green-700` | `#f0fdf4` border |
| **Highlight Error Toast** | `bg-red-50`, `border-red-200`, `text-red-700` | `#fef2f2` border |

---

## 3. Design Token — Tipografi

> **Font Stack:** `font-sans` → sistem default Tailwind → `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`  
> **Font Mono:** `font-mono` → `ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace`

Tidak ada import Google Font eksternal. Sistem menggunakan system font stack standar.

### Hierarki Tipografi yang Digunakan

| Peran | Class Tailwind | Ukuran (px equiv.) | Weight |
|---|---|---|---|
| Heading Halaman | `text-3xl font-extrabold tracking-tight` | 30px | 800 |
| Heading Seksi | `text-2xl font-extrabold` | 24px | 800 |
| Subheading Card | `text-lg font-extrabold` | 18px | 800 |
| Nama Merek (Navbar) | `text-lg font-black tracking-tight leading-none` | 18px | 900 |
| Sub-label Merek | `text-xs font-bold text-surface-400 tracking-widest` | 12px | 700 |
| Label Form | `text-sm font-bold text-surface-700` | 14px | 700 |
| Deskripsi Step | `text-xs text-surface-500 font-medium` | 12px | 500 |
| **Label Uppercase Section** | `text-[10px] font-bold uppercase tracking-widest text-surface-400` | 10px | 700 |
| Teks Konten | `text-sm text-surface-600` | 14px | 400 |
| Teks Monospace (kode) | `font-mono text-xs` | 12px | 400 |
| Badge Skor | `text-[10px] font-bold px-3 py-1 rounded-lg uppercase tracking-wider` | 10px | 700 |
| Micro-label angka | `text-[9px]` | 9px | 400 |

> **Pattern berulang paling penting:** Label section header selalu menggunakan class `text-[10px] font-bold text-surface-400 uppercase tracking-widest mb-N` — ini adalah penanda visual konsisten di seluruh aplikasi.

---

## 4. Design Token — Spacing, Radius, Shadow

### Border Radius (Digunakan Secara Konsisten)

| Komponen | Class | Nilai CSS |
|---|---|---|
| Card utama / Panel besar | `rounded-2xl` | `border-radius: 1rem` (16px) |
| Input, textarea, tombol besar | `rounded-xl` | `border-radius: 0.75rem` (12px) |
| Tombol kecil (action) | `rounded-lg` | `border-radius: 0.5rem` (8px) |
| Badge / pill teks | `rounded-lg` | `border-radius: 0.5rem` (8px) |
| Icon container kecil | `rounded-xl` | `border-radius: 0.75rem` (12px) |
| Progress bar | `rounded-full` | `border-radius: 9999px` |
| Bulatan status dot | `rounded-full` | `border-radius: 9999px` |
| Tombol close (X) modal | `rounded-full` | `border-radius: 9999px` |

### Shadow

| Konteks | Class | Nilai CSS |
|---|---|---|
| Card default | `shadow-sm` | `0 1px 2px 0 rgb(0 0 0 / 0.05)` |
| Tombol primer | `shadow-md shadow-primary-200` | medium + warna |
| Modal | `shadow-2xl` | `0 25px 50px -12px rgb(0 0 0 / 0.25)` |
| Step aktif (running) | `shadow-lg shadow-primary-100/50` | large + teal transparan |
| Badge/pill kecil | `shadow-sm` | minimal |

### Spacing Penting

| Elemen | Class | Nilai |
|---|---|---|
| Padding halaman (atas-bawah) | `py-8` | 32px |
| Padding konten card | `p-5` atau `p-6` | 20px atau 24px |
| Gap antar kartu | `gap-8` | 32px |
| Gap antar elemen form | `space-y-5` | 20px antara anak |
| Padding header modal | `px-8 py-6` | 32px horizontal, 24px vertikal |
| Padding body modal | `p-8` | 32px semua sisi |
| Max-width konten utama | `max-w-7xl mx-auto` | 80rem (1280px), center |

---

## 5. Layout Global & Shell Aplikasi

> **File:** `src/App.vue`

### Struktur HTML Global

```html
<div class="min-h-screen bg-surface-50 font-sans text-surface-800 
            selection:bg-primary-200 selection:text-primary-900 relative">

  <!-- 1. Toast (fixed, z-100) -->
  <!-- 2. Status Bar (bg-surface-900, z-50) -->
  <!-- 3. Navbar (sticky top-0, z-40) -->
  <!-- 4. <main> (flex-1 w-full z-0) -->
    <!-- router-view wrapped in keep-alive -->

</div>
```

**Selection Style:**
```css
::selection {
  background-color: #ccfbf1; /* primary-200 / teal-200 */
  color: #134e4a;            /* primary-900 / teal-900 */
}
```

### Z-Index Stack

| Layer | Z-Index | Class |
|---|---|---|
| Toast notification | `z-100` | `fixed top-6 left-1/2` |
| Status Bar | `z-50` | bagian dari flow |
| Navbar | `z-40` | `sticky top-0` |
| Modal overlay | `z-50` | `fixed inset-0` |
| Konten halaman | `z-0` | default |

---

## 6. Komponen: Status Bar (Top Bar)

> **File:** `src/App.vue` — Bar tipis di atas navbar

```html
<!-- Container -->
<div class="bg-surface-900 text-surface-50 text-xs py-1.5 px-4 md:px-8 
            flex justify-between items-center relative z-50">

  <!-- Kiri: Status dot + pesan -->
  <div class="flex items-center gap-2.5">
    
    <!-- Animated dot wrapper -->
    <span class="relative flex h-2.5 w-2.5">
      <!-- Ping animation (hanya saat ready=true) -->
      <span class="animate-ping absolute inline-flex h-full w-full 
                   rounded-full bg-emerald-400 opacity-75"></span>
      <!-- Dot inti — hijau jika ready, merah jika offline -->
      <span class="relative inline-flex rounded-full h-2.5 w-2.5 
                   [ready? bg-emerald-500 : bg-red-500]"></span>
    </span>
    
    <!-- Teks status -->
    <span class="font-bold tracking-wide 
                 [ready? text-surface-100 : text-surface-400]">
      {{ serverMessage }}
    </span>
  </div>

  <!-- Kanan: Sumber data -->
  <div class="flex items-center gap-2 font-mono text-[10px] 
              uppercase tracking-widest text-surface-400">
    <span class="hidden sm:inline">ALOKASI DATA:</span>
    <!-- Warna: MySQL=primary-400, Lain=amber-400, Tidak ada=surface-600 -->
    <strong class="[MySQL? text-primary-400 : lain? text-amber-400 : text-surface-600]">
      {{ sumberData }}
    </strong>
  </div>
</div>
```

**Detail Visual:**
- Background: `bg-surface-900` = `#0f172a` (hampir hitam)
- Tinggi efektif: `py-1.5` = 6px atas+bawah + konten → ~28px total
- Dot "ping": `w-2.5 h-2.5` = 10px × 10px, `animate-ping`, `bg-emerald-400 opacity-75`
- Dot inti: `w-2.5 h-2.5` = 10px × 10px, `bg-emerald-500` (#10b981) ketika ready

---

## 7. Komponen: Navbar

> **File:** `src/App.vue` — Navigasi utama

```html
<nav class="bg-white/80 backdrop-blur-md border-b border-surface-200 sticky top-0 z-40">
  <div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-center h-16 px-4 sm:px-6 lg:px-8">

      <!-- Logo / Merek -->
      <div class="flex items-center gap-3">
        <div class="flex flex-col">
          <span class="font-black text-lg text-surface-800 tracking-tight leading-none">
            SiReDo
          </span>
          <span class="text-xs font-bold text-surface-400 tracking-widest mt-0.5">
            Sistem Rekomendasi Dosen
          </span>
        </div>
      </div>

      <!-- Menu Links -->
      <div class="flex gap-2">
        <!-- Link AKTIF -->
        <a class="px-4 py-2 text-sm font-semibold rounded-lg transition-all duration-200 
                  hidden sm:inline-block
                  bg-primary-100 text-primary-600">
          
        <!-- Link TIDAK AKTIF -->
        <a class="px-4 py-2 text-sm font-semibold rounded-lg transition-all duration-200 
                  hidden sm:inline-block
                  text-surface-500 hover:text-primary-600 hover:bg-primary-50">
        
        <!-- Tombol hamburger (mobile only) -->
        <button class="sm:hidden p-2 text-surface-500 hover:text-primary-600 
                       hover:bg-primary-50 rounded-lg">
      </div>
    </div>
  </div>
</nav>
```

**Detail Visual:**
- Background: `bg-white/80` = putih dengan opacity 80% + `backdrop-blur-md` = blur 12px
- Tinggi: `h-16` = 64px
- Border bawah: `border-b border-surface-200` = 1px solid `#e2e8f0`
- State aktif: `bg-primary-100` (`#ccfbf1`) + `text-primary-600` (`#0d9488`)
- State hover: `hover:bg-primary-50` (`#f0fdfa`) + `hover:text-primary-600`
- Transisi: `transition-all duration-200`

**Menu yang ada (4 item):**
1. `Rekomendasi Proposal` → path `/`
2. `Daftar Dosen` → path `/dosen`
3. `Admin Panel` → path `/admin/dosen`
4. `Riwayat` → path `/admin/riwayat`

---

## 8. Komponen: Toast Notification

> **File:** `src/App.vue` — Notifikasi floating global

```html
<!-- Fixed, center-top, z-100 -->
<div class="fixed top-6 left-1/2 transform -translate-x-1/2 z-100 
            transition-all duration-200 ease-out
            flex items-center gap-3 px-5 py-3 rounded-2xl shadow-xl border
            [show? translate-y-0 opacity-100 : -translate-y-10 opacity-0 pointer-events-none]
            [error? bg-red-50 border-red-200 text-red-700 : bg-green-50 border-green-200 text-green-700]">

  <!-- Ikon Error: circle dengan exclamation -->
  <!-- Ikon Success: circle dengan checkmark -->
  
  <span class="text-sm font-bold">{{ message }}</span>
</div>
```

**State Masuk:** `translate-y-0 opacity-100`  
**State Keluar:** `-translate-y-10 opacity-0 pointer-events-none`  
**Transisi:** `transition-all duration-200 ease-out`

| Tipe | Background | Border | Teks |
|---|---|---|---|
| Success | `bg-green-50` | `border-green-200` | `text-green-700` |
| Error | `bg-red-50` | `border-red-200` | `text-red-700` |

---

## 9. Halaman Rekomendasi — Left Panel (Form Input)

> **File:** `src/views/RecommendationView.vue`

### Layout Halaman

```html
<!-- Wrapper halaman -->
<div class="max-w-7xl mx-auto py-8">

  <!-- Header + Tombol Refresh -->
  <div class="mb-8 flex flex-col md:flex-row md:justify-between md:items-end gap-4">
    <h1 class="text-3xl font-extrabold text-surface-900 tracking-tight">
      <span class="text-primary-600">Recommendation</span> System
    </h1>
    <p class="text-surface-500 mt-1 font-medium">
      ... <span class="text-blue-500 font-bold">BM25</span> & 
      <span class="text-fuchsia-500 font-bold">SBERT</span> ...
    </p>
  </div>

  <!-- 12-kolom grid -->
  <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
    <!-- Left Panel: lg:col-span-4 (33%) -->
    <!-- Right Panel: lg:col-span-8 (67%) -->
  </div>
</div>
```

### Card Form Input (Left Panel)

```html
<!-- Card container -->
<div class="bg-white border border-surface-200 rounded-2xl shadow-sm p-6 relative overflow-hidden">
  
  <!-- Overlay saat processing -->
  <div v-if="isProcessing" 
       class="absolute inset-0 bg-linear-to-br from-primary-50 to-white/20 opacity-60 z-10">
  </div>
  
  <!-- Label section -->
  <h2 class="text-sm font-bold text-surface-400 mb-5 uppercase tracking-widest relative z-20">
    Data Rencana Skripsi
  </h2>
  
  <!-- Input Judul -->
  <label class="block text-sm font-bold text-surface-700 mb-1.5">Judul Proposal</label>
  <input class="w-full p-3 bg-surface-50 border border-surface-200 rounded-xl 
                focus:ring-2 focus:ring-primary-500 focus:border-primary-500 
                outline-none transition-all text-sm font-medium"
         placeholder="Contoh: Sistem Rekomendasi NLP...">
  
  <!-- Textarea Abstrak -->
  <textarea rows="5"
    class="w-full p-3 bg-surface-50 border border-surface-200 rounded-xl
           focus:ring-2 focus:ring-primary-500 focus:border-primary-500
           outline-none transition-all text-sm resize-none">
  </textarea>
```

**Spesifikasi Input/Textarea:**
- Background rest: `bg-surface-50` = `#f8fafc`
- Border rest: `border-surface-200` = 1px solid `#e2e8f0`
- Border focus: `border-primary-500` = `#14b8a6` + ring `ring-primary-500`
- Ring focus: `focus:ring-2` = 2px ring
- Radius: `rounded-xl` = 12px
- Padding: `p-3` = 12px semua sisi
- Font: `text-sm font-medium` = 14px weight 500

### Mode Toggle (Pembobotan AI)

```html
<!-- Container toggle -->
<div class="bg-surface-50 border border-surface-100 p-4 rounded-xl">
  
  <!-- Toggle switch (custom CSS toggle) -->
  <label class="relative inline-flex items-center cursor-pointer">
    <input type="checkbox" class="sr-only peer">
    <div class="w-9 h-5 bg-surface-300 peer-focus:outline-none rounded-full peer 
                peer-checked:after:translate-x-full peer-checked:after:border-white
                after:content-[''] after:absolute after:top-0.5 after:left-0.5 
                after:bg-white after:border-surface-300 after:border after:rounded-full 
                after:h-4 after:w-4 after:transition-all 
                peer-checked:bg-primary-600"></div>
  </label>
  
  <!-- Mode Adaptif — Info box -->
  <div class="bg-primary-50 border border-primary-100 p-3 rounded-lg 
              text-xs text-primary-700 font-medium leading-relaxed animate-fade-in">
    <span class="font-bold text-primary-800">✨ Adaptif Otomatis:</span> ...
  </div>
  
  <!-- Mode Manual — Range slider -->
  <div class="flex justify-between items-center mb-2">
    <span class="text-[10px] font-mono font-bold bg-surface-200 text-surface-700 px-2 py-0.5 rounded">
      Manual
    </span>
    <span class="text-[10px] font-mono font-bold bg-primary-100 text-primary-700 px-2 py-0.5 rounded">
      L:{{ bobotLexical }}% | S:{{ 100 - bobotLexical }}%
    </span>
  </div>
  <input type="range" class="w-full h-1.5 bg-surface-200 rounded-lg 
                              appearance-none cursor-pointer accent-primary-600">
```

**Toggle Spesifikasi:**
- Track OFF: `w-9 h-5 bg-surface-300` = 36px × 20px, warna slate-300
- Thumb: `after:h-4 after:w-4` = 16px × 16px, putih
- Track ON: `peer-checked:bg-primary-600` = teal-600 (`#0d9488`)

**Range Slider:**
- Track height: `h-1.5` = 6px
- Accent color: `accent-primary-600` = teal-600

### Tombol Utama (Submit)

```html
<button class="w-2/3 bg-primary-600 hover:bg-primary-700 disabled:bg-surface-300 
               text-white font-bold rounded-xl transition-all active:scale-95 
               shadow-md shadow-primary-200 mt-6 relative overflow-hidden">
  
  <!-- Overlay pulse saat loading -->
  <span v-if="isProcessing" 
        class="absolute inset-0 w-full h-full bg-white/20 animate-pulse"></span>
  
  <span class="relative z-10 flex items-center justify-center gap-2 py-3">
    <!-- Spinner icon saat loading: animate-spin w-4 h-4 -->
    {{ isProcessing ? 'Memproses API...' : 'Mulai Analisis AI' }}
  </span>
</button>
```

**Spesifikasi Tombol Primer:**
- Background rest: `bg-primary-600` = `#0d9488`
- Background hover: `hover:bg-primary-700` = `#0f766e`
- Background disabled: `disabled:bg-surface-300` = `#cbd5e1`
- Shadow: `shadow-md shadow-primary-200` = medium shadow + teal-200 color
- Press: `active:scale-95` = scale 95%
- Transisi: `transition-all`
- Padding vertikal: `py-3` = 12px (via inner span)

---

## 10. Komponen: Pipeline Stepper (Right Panel)

> **File:** `src/components/ProgressStepper.vue`

### Empty State

```html
<div class="h-full min-h-96 flex flex-col items-center justify-center 
            border-2 border-dashed border-surface-200 rounded-2xl 
            bg-surface-50/50 text-surface-400">
  <!-- SVG icon w-16 h-16 mb-4 text-surface-300 -->
  <span class="font-bold text-surface-500">Panel proses analisis AI akan muncul di sini.</span>
  <span class="text-sm text-surface-400 mt-1">...</span>
</div>
```

### Step Card (Setiap Langkah Pipeline)

```javascript
// Computed class untuk card step
const stepClass = (step) => [
  'rounded-2xl border transition-all duration-500 overflow-hidden relative bg-white',
  step.status === 'running'
    ? 'border-primary-400 shadow-lg shadow-primary-100/50 scale-[1.01]'
    : 'border-surface-200 opacity-85 hover:opacity-100'
];
```

**State Visual Tiap Step:**

| Status | Border | Shadow | Opacity | Scale |
|---|---|---|---|---|
| `idle` | tidak ditampilkan | — | — | — |
| `running` | `border-primary-400` | `shadow-lg shadow-primary-100/50` | 100% | `scale-[1.01]` |
| `done` | `border-surface-200` | none | 85% hover 100% | 1 |
| `error` | `border-surface-200` | none | 85% | 1 |

**Progress Line (atas card saat running):**
```html
<!-- Step 1,2,5 (primary): -->
<div class="absolute top-0 left-0 h-0.5 bg-primary-500 animate-pulse w-full"></div>
<!-- Step 3 (BM25/blue): -->
<div class="absolute top-0 left-0 h-0.5 bg-blue-500 animate-pulse w-full"></div>
<!-- Step 4 (SBERT/fuchsia): -->
<div class="absolute top-0 left-0 h-0.5 bg-fuchsia-500 animate-pulse w-full"></div>
```
- Tinggi: `h-0.5` = 2px
- Animasi: `animate-pulse`

### Icon Step

```javascript
const stepIconClass = (step) => [
  'w-10 h-10 rounded-xl flex items-center justify-center text-lg font-bold transition-all',
  step.status === 'running'
    ? 'bg-primary-100 text-primary-600 animate-pulse'
    : step.status === 'done'
      ? 'bg-emerald-100 text-emerald-600'   // ← Hijau dengan centang ✓
      : 'bg-surface-100 text-surface-500'   // ← Abu-abu untuk idle
];
```

| Status | Background | Warna Teks | Konten |
|---|---|---|---|
| `running` | `bg-primary-100` | `text-primary-600` | Nomor step + `animate-pulse` |
| `done` | `bg-emerald-100` | `text-emerald-600` | Simbol `✓` |
| `idle/error` | `bg-surface-100` | `text-surface-500` | Nomor step |

**Override khusus Step 3 (BM25) saat running:**
```html
class="bg-blue-100! text-blue-600!"
```

**Override khusus Step 4 (SBERT) saat running:**
```html
class="bg-fuchsia-100! text-fuchsia-600!"
```

### Badge Status

```javascript
const stepBadgeClass = (step) => [
  'text-[10px] font-bold px-3 py-1 rounded-lg uppercase tracking-wider',
  step.status === 'running' 
    ? 'bg-primary-100 text-primary-700'   // "Proses"
    : 'bg-surface-100 text-surface-600'   // "Selesai"
];
```

**Override BM25 saat running:** `bg-blue-100! text-blue-700!`  
**Override SBERT saat running:** `bg-fuchsia-100! text-fuchsia-700!`

### Chevron Rotasi (Accordion)

```html
<svg class="['w-4 h-4 text-surface-400 transition-transform', 
             step.open ? 'rotate-180' : '']">
```

### Panel Konten Step (Accordion Body)

```html
<div class="px-5 pb-5 border-t border-surface-100 bg-surface-50/30 
            animate-fade-in space-y-4 pt-4">
  <!-- Konten spesifik per step -->
</div>
```

### Pola Token Tags (Unigram/Bigram)

```html
<!-- Unigram: hijau emerald -->
<span class="bg-emerald-50 text-emerald-700 border border-emerald-100 
             px-2 py-0.5 rounded text-[10px] font-mono font-bold">
  {{ token }}
</span>

<!-- Bigram: hijau teal -->  
<span class="bg-teal-50 text-teal-700 border border-teal-100 
             px-2 py-0.5 rounded text-[10px] font-mono font-bold">
  {{ bigram }}
</span>
```

### Token Match Highlight (BM25 Step)

```html
<!-- Token MATCH (ada di profil dosen) -->
<span class="bg-blue-500 text-white shadow-md shadow-blue-200 
             border border-blue-600 scale-105
             px-2.5 py-1.5 rounded-md text-xs font-mono font-bold 
             transition-all duration-500 flex items-center gap-1.5">
  <span class="text-[9px]">✓</span> {{ token }}
</span>

<!-- Token TIDAK MATCH -->
<span class="bg-white text-surface-400 border border-surface-200 
             line-through opacity-50
             px-2.5 py-1.5 rounded-md text-xs font-mono font-bold">
  {{ token }}
</span>
```

### Progress Bar Skor

```html
<!-- Bar BM25 (biru) -->
<div class="flex-1 bg-surface-100 rounded-full h-2 overflow-hidden">
  <div class="bg-blue-400 h-2 rounded-full transition-all duration-700"
       :style="`width: ${score}%`">
  </div>
</div>

<!-- Bar SBERT (fuchsia gradient) -->
<div class="w-full bg-surface-100 rounded-full h-3 overflow-hidden">
  <div class="bg-linear-to-r from-fuchsia-400 to-fuchsia-600 h-3 rounded-full 
              transition-all duration-1000"
       :style="`width: ${score}%`">
  </div>
</div>
```

**Detail:**
- BM25 bar: `h-2` (8px), `bg-blue-400`, `duration-700`
- SBERT bar: `h-3` (12px), gradient fuchsia, `duration-1000`

### Tabel Peringkat Akhir

```html
<div class="border border-surface-200 rounded-xl overflow-hidden bg-white shadow-sm">
  <table class="w-full text-left border-collapse">
    <thead class="bg-surface-50 border-b border-surface-200 
                  text-[10px] font-bold text-surface-500 uppercase tracking-wider font-mono">
      <tr>
        <th class="p-3 text-center">#</th>
        <th class="p-3">Nama Dosen</th>
        <th class="p-3">Program Studi</th>
        <th class="p-3 text-center text-blue-600">BM25</th>
        <th class="p-3 text-center text-fuchsia-600">SBERT</th>
        <th class="p-3 text-center text-primary-600">Hybrid</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-surface-100 text-sm">
      <!-- <DosenCard> per baris -->
    </tbody>
  </table>
</div>
```

---

## 11. Komponen: DosenCard (Table Row)

> **File:** `src/components/DosenCard.vue`

```html
<tr class="['hover:bg-surface-50 transition-colors font-mono', 
            index === 0 ? 'bg-primary-50/50' : '']"
    style="cursor: pointer;">

  <!-- Kolom # (Rank) -->
  <td class="p-3 text-center">
    <!-- Rank #1: Badge lingkaran primary -->
    <span class="text-xs font-extrabold bg-primary-500 text-white rounded-full 
                 w-6 h-6 inline-flex items-center justify-center">1</span>
    <!-- Rank lain: teks abu-abu -->
    <span class="text-surface-400 font-bold text-xs">{{ index + 1 }}</span>
  </td>

  <!-- Kolom Nama Dosen -->
  <td class="p-3">
    <div class="font-bold text-surface-800 font-sans text-sm">{{ dosen.NAMA }}</div>
    <div class="text-[9px] text-blue-500 mt-0.5 truncate max-w-40">
      Kata: {{ irisan_kata }}
    </div>
  </td>

  <!-- Kolom Program Studi -->
  <td class="p-3">
    <div class="text-[10px] text-surface-500 font-sans">{{ dosen.PROGRAM_STUDI }}</div>
  </td>

  <!-- Kolom BM25 Score -->
  <td class="p-3 text-center text-blue-600 font-bold bg-blue-50/30">
    <div>{{ lexical_score }}</div>
    <div class="text-[9px] text-blue-400">{{ persen }}%</div>
  </td>

  <!-- Kolom SBERT Score -->
  <td class="p-3 text-center text-fuchsia-600 font-bold bg-fuchsia-50/30">
    <div>{{ semantic_score }}</div>
    <div class="text-[9px] text-fuchsia-400">{{ persen }}%</div>
  </td>

  <!-- Kolom Hybrid Score -->
  <td class="p-3 text-center bg-primary-50">
    <div class="text-primary-700 font-extrabold">{{ hybrid_score }}</div>
    <!-- Mini progress bar hybrid -->
    <div class="w-full bg-primary-100 rounded-full h-1.5 mt-1 overflow-hidden">
      <div class="bg-primary-500 h-1.5 rounded-full" :style="`width: ${persen}%`"></div>
    </div>
  </td>
</tr>
```

**Spesifikasi Baris:**
- Baris Rank #1: `bg-primary-50/50` = teal-50 dengan opacity 50%
- Baris lain: background transparan, `hover:bg-surface-50`
- Kolom BM25: background `bg-blue-50/30` = biru sangat transparan
- Kolom SBERT: background `bg-fuchsia-50/30` = fuchsia sangat transparan
- Kolom Hybrid: background `bg-primary-50` = teal-50 penuh
- Badge #1: `w-6 h-6 rounded-full bg-primary-500 text-white` = lingkaran 24px
- Mini bar hybrid: `h-1.5` = 6px, `bg-primary-500`

---

## 12. Komponen: XAI Modal

> **File:** `src/components/XaiModal.vue`

```html
<!-- Overlay backdrop -->
<div class="fixed inset-0 bg-surface-900/40 backdrop-blur-sm 
            flex items-center justify-center p-4 z-50">

  <!-- Panel Modal -->
  <div class="bg-white rounded-2xl shadow-2xl max-w-3xl w-full 
              max-h-[85vh] flex flex-col overflow-hidden border border-surface-100">

    <!-- Header Modal -->
    <div class="px-8 py-6 border-b border-surface-100 flex justify-between 
                items-start bg-white">
      <div>
        <h3 class="text-2xl font-extrabold text-surface-800 mb-1">{{ NAMA }}</h3>
        <p class="text-sm font-medium text-primary-600">{{ PROGRAM_STUDI }}</p>
      </div>
      <!-- Tombol Close -->
      <button class="p-2 rounded-full bg-surface-50 hover:bg-red-50 
                     text-surface-400 hover:text-red-500 transition-colors">
        <!-- X SVG w-5 h-5 -->
      </button>
    </div>

    <!-- Body Modal (scrollable) -->
    <div class="p-8 overflow-y-auto space-y-8 bg-surface-50/50">

      <!-- Section Bidang Keahlian -->
      <h4 class="text-xs font-bold uppercase tracking-widest text-surface-400 mb-3">
        Bidang Keahlian Utama
      </h4>
      <div class="flex flex-wrap gap-2">
        <!-- Badge keahlian -->
        <span class="bg-primary-100 text-primary-700 border border-primary-200 
                     px-3 py-1.5 rounded-lg text-sm font-medium">
          {{ skill }}
        </span>
      </div>

      <!-- Section Jurnal -->
      <h4 class="text-xs font-bold uppercase tracking-widest text-surface-400 mb-3 
                  flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-primary-400"></span>
        Publikasi Jurnal
      </h4>
      <div class="bg-white border border-surface-200 rounded-xl p-5 shadow-sm">
        <ul class="space-y-3">
          <li class="text-sm text-surface-600 pl-4 relative
                     before:content-[''] before:w-1.5 before:h-1.5 
                     before:bg-surface-300 before:rounded-full 
                     before:absolute before:left-0 before:top-2">
            {{ item }}
          </li>
        </ul>
      </div>

      <!-- Section Riwayat Uji & Bimbingan (2 kolom) -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <h4>...<span class="w-2 h-2 rounded-full bg-amber-400"></span> Historis Uji</h4>
        <h4>...<span class="w-2 h-2 rounded-full bg-emerald-400"></span> Historis Bimbingan</h4>
      </div>
    </div>
  </div>
</div>
```

**Detail Modal:**
- Backdrop: `bg-surface-900/40` = slate-900 opacity 40% + `backdrop-blur-sm` = 4px blur
- Panel max-width: `max-w-3xl` = 48rem (768px)
- Panel max-height: `max-h-[85vh]` = 85% viewport height
- Header padding: `px-8 py-6` = 32px × 24px
- Body padding: `p-8` = 32px semua sisi

**Color Dot Section:**
- Jurnal: `bg-primary-400` (teal)
- Historis Uji: `bg-amber-400` (kuning)
- Historis Bimbingan: `bg-emerald-400` (hijau)

**Badge Keahlian:**
- `bg-primary-100 text-primary-700 border border-primary-200`
- `px-3 py-1.5 rounded-lg text-sm font-medium`

**Bullet List (before pseudo-element):**
```css
li::before {
  content: '';
  width: 6px;
  height: 6px;
  background-color: #cbd5e1; /* surface-300 */
  border-radius: 50%;
  position: absolute;
  left: 0;
  top: 8px;
}
```

---

## 13. Halaman Admin Panel

> **File:** `src/views/AdminDosenView.vue`

### Layout & Header

```html
<div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
  
  <!-- Header flex row (responsive) -->
  <div class="flex flex-col md:flex-row md:justify-between md:items-end gap-5 mb-8">
    <h2 class="text-3xl font-extrabold text-surface-800 tracking-tight">
      Manajemen Dosen
    </h2>
    <!-- Tombol Tambah Dosen (primer) -->
    <button class="flex items-center gap-2 bg-primary-600 hover:bg-primary-700 
                   text-white px-5 py-2.5 rounded-xl shadow-sm font-medium 
                   transition-all focus:ring-2 focus:ring-primary-500 
                   focus:ring-offset-2 outline-none">
```

### Tabel Admin

```html
<div class="bg-white rounded-2xl shadow-sm border border-surface-200 overflow-hidden mb-6">
  <table class="w-full text-left border-collapse">
    <thead>
      <tr class="bg-surface-50/50 border-b border-surface-200 
                 text-xs uppercase tracking-widest text-surface-400 font-bold">
        <th class="p-5 font-bold">Informasi Dosen</th>
        <th class="p-5 font-bold">Bidang Keahlian</th>
        <th class="p-5 font-bold text-center">Aksi Manajemen</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-surface-100">
      <tr class="hover:bg-surface-50/80 transition-colors group">
        <td class="p-5">
          <div class="font-bold text-surface-800 text-base">{{ dosen.nama }}</div>
          <div class="text-sm font-medium text-primary-600 mt-0.5">
            {{ dosen.program_studi }}
          </div>
        </td>
        <td class="p-5 max-w-md">
          <!-- Badge keahlian -->
          <span class="bg-surface-100 text-surface-600 px-2.5 py-1 rounded-md 
                       text-[10px] font-bold border border-surface-200 
                       uppercase tracking-wider">
            {{ skill }}
          </span>
        </td>
        <td class="p-5 text-center">
          <!-- Tombol Edit -->
          <button class="text-sm bg-white border border-surface-300 text-surface-600 
                         font-semibold px-3 py-1.5 rounded-lg transition-all 
                         hover:border-primary-400 hover:bg-primary-50 hover:text-primary-700 
                         shadow-sm">Edit</button>
          <!-- Tombol Hapus -->
          <button class="text-sm bg-white border border-surface-300 text-surface-600 
                         font-semibold px-3 py-1.5 rounded-lg transition-all 
                         hover:border-red-400 hover:bg-red-50 hover:text-red-600 
                         shadow-sm">Hapus</button>
        </td>
      </tr>
    </tbody>
  </table>
</div>
```

**Badge keahlian di tabel Admin (berbeda dari modal XAI):**
- Admin: `bg-surface-100 text-surface-600 border-surface-200` = abu-abu netral
- XAI Modal: `bg-primary-100 text-primary-700 border-primary-200` = teal

### Modal Form (Tambah/Edit Dosen)

```html
<!-- Backdrop -->
<div class="fixed inset-0 bg-surface-800/40 backdrop-blur-sm">

<!-- Panel form -->
<div class="relative w-full max-w-2xl bg-white rounded-2xl shadow-xl 
            border border-surface-200 overflow-hidden transform transition-all 
            flex flex-col max-h-[90vh]">

  <!-- Header form -->
  <div class="px-6 py-5 border-b border-surface-100 flex justify-between 
              items-center bg-surface-50/50">
    <h3 class="text-lg font-extrabold text-surface-800">Edit/Tambah...</h3>
  </div>

  <!-- Form body (scrollable) -->
  <form class="px-6 py-5 space-y-5 overflow-y-auto custom-scrollbar">
    
    <!-- Input field dalam form -->
    <input class="w-full px-4 py-2.5 bg-white border border-surface-200 rounded-xl 
                  shadow-sm text-sm focus:ring-2 focus:ring-primary-500 
                  focus:border-primary-500 outline-none transition-all 
                  placeholder-surface-400 text-surface-700 font-medium">
  </form>

  <!-- Footer tombol -->
  <div class="px-6 py-4 bg-surface-50/80 border-t border-surface-100 
              flex justify-end gap-3 rounded-b-2xl shrink-0">
    <!-- Tombol Batal (sekunder) -->
    <button class="px-5 py-2.5 border border-surface-300 shadow-sm text-sm font-bold 
                   rounded-xl text-surface-600 bg-white hover:bg-surface-50 
                   hover:text-surface-800 transition-colors">Batal</button>
    <!-- Tombol Simpan (primer) -->
    <button class="inline-flex items-center px-6 py-2.5 border border-transparent 
                   shadow-sm text-sm font-bold rounded-xl text-white 
                   bg-primary-600 hover:bg-primary-700 transition-all 
                   disabled:opacity-70 disabled:cursor-not-allowed">Simpan</button>
  </div>
</div>
```

**Perbedaan input Admin vs input RecommendationView:**
| | Admin Form | Recommendation Form |
|---|---|---|
| Background | `bg-white` | `bg-surface-50` |
| Padding | `px-4 py-2.5` | `p-3` |
| Shadow | `shadow-sm` | tidak ada |

---

## 14. Animasi & Transisi

### Animasi Custom (didefinisikan di `<style scoped>`)

```css
/* Di RecommendationView.vue */
.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

**Durasi:** 0.4s, easing: ease-out, fill-mode: forwards  
**Transform:** slide up 5px sambil fade in

### Animasi Tailwind yang Digunakan

| Class | Efek | Digunakan di |
|---|---|---|
| `animate-pulse` | Opacity 0.5 ↔ 1, 2s loop | Status bar dot ping, step icon saat running, overlay tombol, progress line |
| `animate-ping` | Scale 1→2 + fade out, 1s loop | Dot ping di status bar |
| `animate-spin` | Rotasi 360° kontinyu | Spinner tombol, icon refresh |
| `animate-fade-in` | Custom fadeIn | Accordion body, info box toggle |

### Transisi State Card Step

```css
/* class: transition-all duration-500 */
/* Saat berubah running↔done: border, shadow, opacity, scale berubah smooth */
transition-property: all;
transition-duration: 500ms;
```

### Transisi Progress Bar

```css
/* BM25 bar: transition-all duration-700 */
transition-duration: 700ms;

/* SBERT bar: transition-all duration-1000 */
transition-duration: 1000ms;
```

### Transisi Modal (Vue `<transition>`)

```javascript
// Enter
enter-active-class="ease-out duration-300"
enter-from-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
enter-to-class="opacity-100 translate-y-0 sm:scale-100"

// Leave
leave-active-class="ease-in duration-200"
leave-from-class="opacity-100 translate-y-0 sm:scale-100"
leave-to-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
```

### Hover Effects

| Elemen | Efek |
|---|---|
| Nav link | `hover:bg-primary-50 hover:text-primary-600` |
| Tombol Action | `hover:border-primary-400 hover:bg-primary-50` |
| Tombol Hapus | `hover:border-red-400 hover:bg-red-50 hover:text-red-600` |
| Tabel row | `hover:bg-surface-50` |
| Tombol close modal | `hover:bg-red-50 hover:text-red-500` |
| Tombol utama press | `active:scale-95` |
| Tombol refresh | `active:scale-95` |

---

## 15. Custom CSS & Scrollbar

> **File:** `src/views/AdminDosenView.vue` — `<style scoped>`

```css
/* Custom scrollbar untuk form modal */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;   /* slate-300 / surface-300 */
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;   /* slate-400 / surface-400 */
}
```

**Digunakan pada:** `<form>` di dalam modal Admin, class `.custom-scrollbar`

---

## 16. Color Coding Semantik per Komponen AI

Ini adalah sistem warna **konsisten dan bermakna** di seluruh aplikasi:

| Komponen AI | Warna | Token Tailwind | Hex |
|---|---|---|---|
| **BM25 / Leksikal** | Biru | `blue-400/500/600` + `blue-50/100` | `#3b82f6` |
| **SBERT / Semantik** | Fuchsia/Magenta | `fuchsia-400/500/600` + `fuchsia-50/100` | `#d946ef` |
| **Hybrid Score** | Teal (Primary) | `primary-500/600/700` + `primary-50/100` | `#14b8a6` |
| **Preprocessing / Token Unigram** | Emerald | `emerald-50/100/700` | `#10b981` |
| **N-gram Bigram** | Teal | `teal-50/100/700` | `#14b8a6` |
| **Ekspansi Sinonim** | Amber | `amber-50/100/200/700` | `#f59e0b` |
| **Server Ready / Selesai** | Emerald | `emerald-400/500` | `#10b981` |
| **Error / Offline** | Red | `red-400/500/600` | `#ef4444` |

**Aturan penting:** Warna ini **tidak boleh ditukar antar-komponen** — konsistensi warna adalah identitas visual sistem.

---

## 17. Kamus Kelas Tailwind → Nilai CSS Nyata

Referensi cepat untuk nilai CSS aktual dari kelas yang paling sering digunakan:

### Sizing
| Kelas | Nilai CSS |
|---|---|
| `w-2.5 h-2.5` | `width/height: 10px` |
| `w-4 h-4` | `width/height: 16px` |
| `w-5 h-5` | `width/height: 20px` |
| `w-6 h-6` | `width/height: 24px` |
| `w-7 h-7` | `width/height: 28px` |
| `w-9 h-5` | `width: 36px, height: 20px` (toggle) |
| `w-10 h-10` | `width/height: 40px` (step icon) |
| `w-16 h-16` | `width/height: 64px` (empty state icon) |
| `h-0.5` | `height: 2px` (progress line) |
| `h-1.5` | `height: 6px` (mini bar) |
| `h-2` | `height: 8px` (BM25 bar) |
| `h-3` | `height: 12px` (SBERT bar) |
| `h-16` | `height: 64px` (navbar) |
| `max-w-7xl` | `max-width: 80rem = 1280px` |
| `max-w-3xl` | `max-width: 48rem = 768px` |
| `max-w-2xl` | `max-width: 42rem = 672px` |

### Spacing
| Kelas | Nilai CSS |
|---|---|
| `p-3` | `padding: 12px` |
| `p-4` | `padding: 16px` |
| `p-5` | `padding: 20px` |
| `p-6` | `padding: 24px` |
| `p-8` | `padding: 32px` |
| `px-4 py-2` | `padding: 8px 16px` |
| `px-5 py-3` | `padding: 12px 20px` |
| `px-6 py-5` | `padding: 20px 24px` |
| `px-8 py-6` | `padding: 24px 32px` |
| `py-1.5` | `padding-top/bottom: 6px` |
| `py-2.5` | `padding-top/bottom: 10px` |
| `gap-2` | `gap: 8px` |
| `gap-3` | `gap: 12px` |
| `gap-4` | `gap: 16px` |
| `gap-8` | `gap: 32px` |
| `mb-1.5` | `margin-bottom: 6px` |
| `mb-5` | `margin-bottom: 20px` |
| `mb-8` | `margin-bottom: 32px` |
| `mt-0.5` | `margin-top: 2px` |
| `space-y-4` | `> * + *: margin-top: 16px` |
| `space-y-5` | `> * + *: margin-top: 20px` |
| `space-y-6` | `> * + *: margin-top: 24px` |

### Border Radius
| Kelas | Nilai CSS |
|---|---|
| `rounded-lg` | `border-radius: 8px` |
| `rounded-xl` | `border-radius: 12px` |
| `rounded-2xl` | `border-radius: 16px` |
| `rounded-full` | `border-radius: 9999px` |
| `rounded-md` | `border-radius: 6px` |

### Typography Scale
| Kelas | Font Size | Line Height |
|---|---|---|
| `text-[9px]` | 9px | auto |
| `text-[10px]` | 10px | auto |
| `text-xs` | 12px | 16px |
| `text-sm` | 14px | 20px |
| `text-base` | 16px | 24px |
| `text-lg` | 18px | 28px |
| `text-xl` | 20px | 28px |
| `text-2xl` | 24px | 32px |
| `text-3xl` | 30px | 36px |

### Font Weight
| Kelas | `font-weight` |
|---|---|
| `font-medium` | 500 |
| `font-semibold` | 600 |
| `font-bold` | 700 |
| `font-extrabold` | 800 |
| `font-black` | 900 |

### Letter Spacing
| Kelas | `letter-spacing` |
|---|---|
| `tracking-tight` | -0.025em |
| default | 0 |
| `tracking-wide` | 0.025em |
| `tracking-wider` | 0.05em |
| `tracking-widest` | 0.1em |

---

*Blueprint ini dibangun dari pembacaan langsung seluruh file Vue component SiReDo V2. Setiap kelas, nilai, dan pola visual telah diverifikasi terhadap source code aktual.*
