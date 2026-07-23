<!-- HalamanBatch.vue — Batch Processing Rekomendasi Dosen Penguji -->
<template>
  <div class="max-w-7xl mx-auto py-8 space-y-8">

    <!-- ═══════════════════════════════════════════════════════
         HEADER
    ════════════════════════════════════════════════════════════ -->
    <div class="flex flex-col md:flex-row md:justify-between md:items-end gap-4">
      <div>
        <div class="flex items-center gap-3 mb-1">
          <div class="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center">
            <svg class="w-4 h-4 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
          </div>
          <span class="text-xs font-bold text-primary-600 uppercase tracking-widest">Batch Processing</span>
        </div>
        <h1 class="text-3xl font-extrabold text-surface-900 tracking-tight">
          Rekomendasi <span class="text-primary-600">Massal</span>
        </h1>
        <p class="text-surface-500 mt-1 font-medium text-sm">
          Upload Excel/CSV → Sistem merekomendasikan 2 dosen penguji per mahasiswa secara otomatis
        </p>
      </div>

      <button @click="unduhTemplate"
        class="flex items-center gap-2 bg-white hover:bg-surface-50 border border-surface-200 text-surface-600 px-4 py-2 rounded-xl text-sm font-bold shadow-sm transition-all active:scale-95">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
        </svg>
        Unduh Template Excel
      </button>
    </div>

    <!-- ═══════════════════════════════════════════════════════
         ATURAN & INFO SISTEM
    ════════════════════════════════════════════════════════════ -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="bg-blue-50 border border-blue-100 rounded-2xl p-4 flex gap-3">
        <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center shrink-0 mt-0.5">
          <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
          </svg>
        </div>
        <div>
          <div class="text-xs font-bold text-blue-700 uppercase tracking-widest mb-1">Kolom Wajib di File</div>
          <div class="text-xs text-blue-600 leading-relaxed">
            <span class="font-mono bg-blue-100 px-1 rounded">nama_mahasiswa</span>,
            <span class="font-mono bg-blue-100 px-1 rounded">nim</span>,
            <span class="font-mono bg-blue-100 px-1 rounded">judul_ta</span>,
            <span class="font-mono bg-blue-100 px-1 rounded">abstrak</span>
          </div>
        </div>
      </div>

      <div class="bg-amber-50 border border-amber-100 rounded-2xl p-4 flex gap-3">
        <div class="w-8 h-8 bg-amber-100 rounded-lg flex items-center justify-center shrink-0 mt-0.5">
          <svg class="w-4 h-4 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
        </div>
        <div>
          <div class="text-xs font-bold text-amber-700 uppercase tracking-widest mb-1">Aturan Deduplikasi</div>
          <div class="text-xs text-amber-600 leading-relaxed">
            Setiap dosen hanya bisa menguji <strong>1 judul TA</strong>. Jika sudah terpakai, sistem otomatis pilih dosen terbaik berikutnya yang masih tersedia.
          </div>
        </div>
      </div>

      <div class="bg-emerald-50 border border-emerald-100 rounded-2xl p-4 flex gap-3">
        <div class="w-8 h-8 bg-emerald-100 rounded-lg flex items-center justify-center shrink-0 mt-0.5">
          <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <div>
          <div class="text-xs font-bold text-emerald-700 uppercase tracking-widest mb-1">Output</div>
          <div class="text-xs text-emerald-600 leading-relaxed">
            File Excel berisi nama mahasiswa, NIM, judul TA, Penguji 1 &amp; Penguji 2 beserta skor relevansi.
          </div>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════
         AREA UPLOAD
    ════════════════════════════════════════════════════════════ -->
    <div class="bg-white border border-surface-200 rounded-2xl shadow-sm overflow-hidden">
      <div class="p-6 border-b border-surface-100">
        <h2 class="text-sm font-bold text-surface-400 uppercase tracking-widest">Upload File Data Mahasiswa</h2>
      </div>

      <div class="p-6">
        <!-- Drop zone -->
        <div
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="handleDrop"
          :class="[
            'border-2 border-dashed rounded-2xl p-10 text-center transition-all duration-200 cursor-pointer relative',
            isDragging
              ? 'border-primary-400 bg-primary-50'
              : fileTerpilih
                ? 'border-emerald-300 bg-emerald-50'
                : 'border-surface-200 hover:border-primary-300 hover:bg-surface-50'
          ]"
          @click="$refs.inputFile.click()"
        >
          <input ref="inputFile" type="file" accept=".xlsx,.xls,.csv" class="hidden" @change="handleFileChange" />

          <div v-if="!fileTerpilih">
            <div class="w-14 h-14 bg-surface-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <svg class="w-7 h-7 text-surface-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
              </svg>
            </div>
            <p class="text-sm font-bold text-surface-600 mb-1">Seret file ke sini atau klik untuk memilih</p>
            <p class="text-xs text-surface-400">Format yang diterima: <span class="font-mono">.xlsx</span>, <span class="font-mono">.xls</span>, <span class="font-mono">.csv</span></p>
          </div>

          <div v-else class="flex items-center justify-center gap-4">
            <div class="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center shrink-0">
              <svg class="w-6 h-6 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
            </div>
            <div class="text-left">
              <div class="font-bold text-surface-800 text-sm">{{ fileTerpilih.name }}</div>
              <div class="text-xs text-surface-500 mt-0.5">{{ formatUkuranFile(fileTerpilih.size) }} · Klik untuk ganti file</div>
            </div>
            <button @click.stop="hapusFile" class="ml-2 w-7 h-7 bg-surface-100 hover:bg-red-50 hover:text-red-500 rounded-lg flex items-center justify-center transition-colors">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Preview tabel -->
        <div v-if="dataMahasiswa.length > 0" class="mt-6 space-y-3">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="text-sm font-bold text-surface-700">Preview Data</span>
              <span class="text-xs font-bold bg-primary-100 text-primary-700 px-2 py-0.5 rounded-lg">
                {{ dataMahasiswa.length }} mahasiswa
              </span>
            </div>
            <span class="text-xs text-surface-400">Menampilkan {{ Math.min(5, dataMahasiswa.length) }} dari {{ dataMahasiswa.length }} data</span>
          </div>

          <div class="border border-surface-200 rounded-xl overflow-hidden">
            <table class="w-full text-left text-xs">
              <thead class="bg-surface-50 border-b border-surface-200 text-[10px] font-bold text-surface-500 uppercase tracking-wider">
                <tr>
                  <th class="px-4 py-2.5">No</th>
                  <th class="px-4 py-2.5">Nama Mahasiswa</th>
                  <th class="px-4 py-2.5">NIM</th>
                  <th class="px-4 py-2.5">Judul TA</th>
                  <th class="px-4 py-2.5">Abstrak</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-surface-100">
                <tr v-for="(mhs, i) in dataMahasiswa.slice(0, 5)" :key="i" class="hover:bg-surface-50">
                  <td class="px-4 py-2.5 text-surface-400 font-bold font-mono">{{ i + 1 }}</td>
                  <td class="px-4 py-2.5 font-medium text-surface-800">{{ mhs.nama_mahasiswa }}</td>
                  <td class="px-4 py-2.5 font-mono text-surface-600">{{ mhs.nim }}</td>
                  <td class="px-4 py-2.5 text-surface-600 max-w-48">
                    <div class="truncate">{{ mhs.judul_ta }}</div>
                  </td>
                  <td class="px-4 py-2.5 text-surface-400 max-w-48">
                    <div class="truncate">{{ mhs.abstrak }}</div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Validasi error -->
          <div v-if="errorValidasi.length > 0" class="bg-red-50 border border-red-200 rounded-xl p-4">
            <div class="text-xs font-bold text-red-700 uppercase tracking-widest mb-2">⚠ Masalah Ditemukan di File ({{ errorValidasi.length }})</div>
            <ul class="space-y-1 max-h-40 overflow-y-auto">
              <li v-for="(err, ei) in errorValidasi.slice(0, 30)" :key="ei" class="text-xs text-red-600 flex items-start gap-1.5">
                <span class="shrink-0 mt-0.5">•</span>{{ err }}
              </li>
            </ul>
            <div v-if="errorValidasi.length > 30" class="text-[10px] text-red-400 font-bold mt-2">
              ...dan {{ errorValidasi.length - 30 }} masalah lainnya. Perbaiki file lalu upload ulang.
            </div>
          </div>

          <!-- Peringatan dosen tidak cukup -->
          <div v-if="!isMemproses && peringatanKapasitas" class="bg-amber-50 border border-amber-200 rounded-xl p-4">
            <div class="text-xs font-bold text-amber-700 uppercase tracking-widest mb-1">⚠ Perhatian Kapasitas Dosen</div>
            <div class="text-xs text-amber-600 leading-relaxed">{{ peringatanKapasitas }}</div>
          </div>

          <!-- Tombol proses -->
          <div class="flex justify-end pt-2">
            <button
              @click="prosesBatch"
              :disabled="isMemproses || errorValidasi.length > 0"
              class="flex items-center gap-2 bg-primary-600 hover:bg-primary-700 disabled:bg-surface-300 text-white font-bold px-6 py-3 rounded-xl transition-all active:scale-95 shadow-md shadow-primary-200 relative overflow-hidden">
              <span v-if="isMemproses" class="absolute inset-0 bg-white/20 animate-pulse"></span>
              <svg v-if="isMemproses" class="w-4 h-4 animate-spin relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
              <svg v-else class="w-4 h-4 relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
              <span class="relative z-10">{{ isMemproses ? `Memproses ${progressSelesai}/${dataMahasiswa.length}...` : 'Mulai Proses Batch' }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════
         PROGRESS SAAT MEMPROSES
    ════════════════════════════════════════════════════════════ -->
    <div v-if="isMemproses" class="bg-white border border-primary-200 rounded-2xl shadow-sm p-6 animate-fade-in">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h3 class="font-bold text-surface-800">Sedang Memproses...</h3>
          <p class="text-xs text-surface-500 mt-0.5">Sistem menganalisis setiap judul TA dengan Hybrid BM25 + SBERT</p>
        </div>
        <span class="text-2xl font-extrabold text-primary-600 font-mono">
          {{ progressSelesai }}<span class="text-surface-300">/{{ dataMahasiswa.length }}</span>
        </span>
      </div>

      <div class="w-full bg-surface-100 rounded-full h-2.5 overflow-hidden mb-3">
        <div
          class="bg-primary-500 h-2.5 rounded-full transition-all duration-500"
          :style="`width: ${dataMahasiswa.length > 0 ? (progressSelesai / dataMahasiswa.length) * 100 : 0}%`">
        </div>
      </div>

      <div class="flex flex-wrap gap-2">
        <div v-for="(mhs, i) in dataMahasiswa" :key="i"
          :class="[
            'flex items-center gap-1.5 text-[10px] font-bold px-2 py-1 rounded-lg border transition-all',
            i < progressSelesai
              ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
              : i === progressSelesai
                ? 'bg-primary-50 text-primary-700 border-primary-200 animate-pulse'
                : 'bg-surface-50 text-surface-400 border-surface-200'
          ]">
          <span v-if="i < progressSelesai">✓</span>
          <span v-else-if="i === progressSelesai" class="w-1.5 h-1.5 bg-primary-500 rounded-full animate-ping inline-block"></span>
          {{ mhs.nama_mahasiswa.split(' ')[0] }}
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════
         HASIL BATCH
    ════════════════════════════════════════════════════════════ -->
    <div v-if="hasilBatch.length > 0" class="space-y-4 animate-fade-in">

      <!-- Header hasil -->
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-xl font-extrabold text-surface-900">Hasil Rekomendasi</h2>
          <p class="text-sm text-surface-500 mt-0.5">
            {{ hasilBatch.length }} mahasiswa · {{ jumlahDosenTerpakai }} dosen terpakai · Mode: <span class="text-primary-600 font-bold">Adaptif</span>
          </p>
        </div>
        <button @click="unduhHasil"
          class="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-5 py-2.5 rounded-xl text-sm transition-all active:scale-95 shadow-md shadow-emerald-200">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
          </svg>
          Unduh Hasil Excel
        </button>
      </div>

      <!-- Peringatan slot habis saat proses -->
      <div v-if="jumlahGagalKapasitas > 0" class="bg-red-50 border border-red-200 rounded-xl p-4">
        <div class="text-xs font-bold text-red-700 uppercase tracking-widest mb-1">⚠ {{ jumlahGagalKapasitas }} Mahasiswa Tidak Mendapat Penguji Lengkap</div>
        <div class="text-xs text-red-600 leading-relaxed">
          Jumlah dosen tersedia tidak cukup untuk semua mahasiswa (setiap dosen hanya bisa menguji 1 judul). Tambahkan dosen baru atau kurangi jumlah mahasiswa per batch, lalu proses ulang baris yang gagal.
        </div>
      </div>

      <!-- Statistik ringkas -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div class="bg-white border border-surface-200 rounded-xl p-4 text-center">
          <div class="text-2xl font-extrabold text-primary-600">{{ hasilBatch.length }}</div>
          <div class="text-[10px] font-bold text-surface-400 uppercase mt-1">Total Mahasiswa</div>
        </div>
        <div class="bg-white border border-surface-200 rounded-xl p-4 text-center">
          <div class="text-2xl font-extrabold text-emerald-600">{{ jumlahDosenTerpakai }}</div>
          <div class="text-[10px] font-bold text-surface-400 uppercase mt-1">Dosen Dilibatkan</div>
        </div>
        <div class="bg-white border border-surface-200 rounded-xl p-4 text-center">
          <div class="text-2xl font-extrabold text-blue-600">{{ rerataSkorHybrid }}</div>
          <div class="text-[10px] font-bold text-surface-400 uppercase mt-1">Rata-rata Skor</div>
        </div>
        <div class="bg-white border border-surface-200 rounded-xl p-4 text-center">
          <div class="text-2xl font-extrabold text-amber-600">{{ jumlahFallback }}</div>
          <div class="text-[10px] font-bold text-surface-400 uppercase mt-1">Fallback Dipakai</div>
        </div>
      </div>

      <!-- Tabel hasil utama -->
      <div class="bg-white border border-surface-200 rounded-2xl shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead class="bg-surface-50 border-b border-surface-200 text-[10px] font-bold text-surface-500 uppercase tracking-wider">
              <tr>
                <th class="px-4 py-3 text-center">#</th>
                <th class="px-4 py-3">Mahasiswa</th>
                <th class="px-4 py-3">Judul TA</th>
                <th class="px-4 py-3 text-center bg-blue-50/50">Penguji 1</th>
                <th class="px-4 py-3 text-center bg-fuchsia-50/50">Penguji 2</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-surface-100">
              <template v-for="(hasil, i) in hasilBatch" :key="i">
                <!-- Baris utama -->
                <tr
                  :class="[
                    'hover:bg-surface-50 transition-colors cursor-pointer',
                    (hasil.penguji_1.nama === 'Tidak tersedia' || hasil.penguji_2.nama === 'Tidak tersedia') ? 'bg-red-50/40' : ''
                  ]"
                  @click="toggleDetail(i)">

                  <td class="px-4 py-4 text-center">
                    <span class="text-xs font-bold text-surface-400 font-mono">{{ i + 1 }}</span>
                  </td>

                  <td class="px-4 py-4">
                    <div class="font-bold text-surface-800 text-sm">{{ hasil.nama_mahasiswa }}</div>
                    <div class="text-[10px] font-mono text-surface-400 mt-0.5">{{ hasil.nim }}</div>
                  </td>

                  <td class="px-4 py-4 max-w-xs">
                    <div class="text-xs text-surface-700 leading-relaxed line-clamp-2">{{ hasil.judul_ta }}</div>
                  </td>

                  <!-- Penguji 1 -->
                  <td class="px-4 py-4 bg-blue-50/30 text-center min-w-48">
                    <div class="font-bold text-surface-800 text-xs">{{ hasil.penguji_1.nama }}</div>
                    <div class="text-[10px] text-surface-500 mt-0.5">{{ hasil.penguji_1.program_studi }}</div>
                    <div class="flex items-center justify-center gap-1.5 mt-2">
                      <div v-if="hasil.penguji_1.nama !== 'Tidak tersedia' && hasil.penguji_1.nama !== 'Gagal diproses'"
                        class="bg-blue-100 text-blue-700 text-[10px] font-bold px-2 py-0.5 rounded font-mono">
                        {{ Math.round(hasil.penguji_1.hybrid_score * 100) }}%
                      </div>
                      <div v-if="hasil.penguji_1.is_fallback" class="bg-amber-100 text-amber-700 text-[9px] font-bold px-1.5 py-0.5 rounded">
                        fallback
                      </div>
                    </div>
                  </td>

                  <!-- Penguji 2 -->
                  <td class="px-4 py-4 bg-fuchsia-50/30 text-center min-w-48">
                    <div class="font-bold text-surface-800 text-xs">{{ hasil.penguji_2.nama }}</div>
                    <div class="text-[10px] text-surface-500 mt-0.5">{{ hasil.penguji_2.program_studi }}</div>
                    <div class="flex items-center justify-center gap-1.5 mt-2">
                      <div v-if="hasil.penguji_2.nama !== 'Tidak tersedia' && hasil.penguji_2.nama !== 'Gagal diproses'"
                        class="bg-fuchsia-100 text-fuchsia-700 text-[10px] font-bold px-2 py-0.5 rounded font-mono">
                        {{ Math.round(hasil.penguji_2.hybrid_score * 100) }}%
                      </div>
                      <div v-if="hasil.penguji_2.is_fallback" class="bg-amber-100 text-amber-700 text-[9px] font-bold px-1.5 py-0.5 rounded">
                        fallback
                      </div>
                    </div>
                  </td>
                </tr>

                <!-- Baris detail (expand) -->
                <tr v-if="detailTerbuka === i" class="bg-surface-50/80">
                  <td colspan="5" class="px-6 py-5 border-t border-surface-100">

                    <!-- Pesan kapasitas habis -->
                    <div v-if="hasil.penguji_1.nama === 'Tidak tersedia' || hasil.penguji_2.nama === 'Tidak tersedia'"
                      class="bg-red-50 border border-red-200 rounded-xl p-4 mb-4 text-xs text-red-600 leading-relaxed">
                      <strong class="text-red-700">Stok dosen tersedia habis</strong> untuk mahasiswa ini — semua kandidat dalam daftar top-{{ topKDigunakan }} sudah terpakai oleh mahasiswa lain. Naikkan jumlah kandidat yang diminta dari server, atau proses ulang setelah menambah dosen.
                    </div>

                    <div v-if="hasil.semua_kandidat.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4 animate-fade-in">

                      <!-- Detail Penguji 1 -->
                      <div class="bg-white border border-blue-200 rounded-xl p-4">
                        <div class="text-[10px] font-bold text-blue-500 uppercase tracking-widest mb-3">Detail Penguji 1</div>
                        <div class="font-bold text-surface-800 mb-1">{{ hasil.penguji_1.nama }}</div>
                        <div class="text-[10px] text-surface-400 mb-3">{{ hasil.penguji_1.program_studi }}</div>

                        <div class="space-y-2">
                          <div class="text-[10px] font-bold text-surface-400 uppercase tracking-widest mb-1">
                            Semua Kandidat (Urutan Relevansi)
                          </div>
                          <div v-for="(kand, ki) in tampilKandidat(hasil.semua_kandidat, hasil.penguji_1.ranking_asli)" :key="'p1kand'+ki"
                            :class="[
                              'flex items-center gap-2 p-2 rounded-lg border text-xs transition-all',
                              ki === hasil.penguji_1.ranking_asli
                                ? 'bg-blue-50 border-blue-300 font-bold ring-1 ring-blue-200'
                                : kand.sudah_terpakai && ki !== hasil.penguji_1.ranking_asli
                                  ? 'bg-surface-50 border-surface-100 opacity-50'
                                  : 'bg-white border-surface-100'
                            ]">
                            <span class="text-[10px] font-mono font-bold text-surface-400 w-4 shrink-0">{{ ki + 1 }}</span>
                            <div class="flex-1 min-w-0">
                              <div class="font-bold text-surface-700 truncate">{{ kand.NAMA }}</div>
                              <div class="text-[9px] text-surface-400 truncate">{{ kand.PROGRAM_STUDI }}</div>
                            </div>
                            <div class="flex items-center gap-1 shrink-0">
                              <span class="font-mono font-bold text-surface-600 text-[10px]">{{ Math.round(kand['Hybrid Score'] * 100) }}%</span>
                              <span v-if="kand.sudah_terpakai && ki !== hasil.penguji_1.ranking_asli"
                                class="text-[9px] bg-red-100 text-red-500 px-1 rounded font-bold">terpakai</span>
                              <span v-else-if="ki === hasil.penguji_1.ranking_asli"
                                class="text-[9px] bg-blue-100 text-blue-600 px-1 rounded font-bold">✓ dipilih</span>
                            </div>
                          </div>
                        </div>
                      </div>

                      <!-- Detail Penguji 2 -->
                      <div class="bg-white border border-fuchsia-200 rounded-xl p-4">
                        <div class="text-[10px] font-bold text-fuchsia-500 uppercase tracking-widest mb-3">Detail Penguji 2</div>
                        <div class="font-bold text-surface-800 mb-1">{{ hasil.penguji_2.nama }}</div>
                        <div class="text-[10px] text-surface-400 mb-3">{{ hasil.penguji_2.program_studi }}</div>

                        <div class="space-y-2">
                          <div class="text-[10px] font-bold text-surface-400 uppercase tracking-widest mb-1">
                            Semua Kandidat (Urutan Relevansi)
                          </div>
                          <div v-for="(kand, ki) in tampilKandidat(hasil.semua_kandidat, hasil.penguji_2.ranking_asli)" :key="'p2kand'+ki"
                            :class="[
                              'flex items-center gap-2 p-2 rounded-lg border text-xs transition-all',
                              ki === hasil.penguji_2.ranking_asli
                                ? 'bg-fuchsia-50 border-fuchsia-300 font-bold ring-1 ring-fuchsia-200'
                                : kand.sudah_terpakai && ki !== hasil.penguji_2.ranking_asli
                                  ? 'bg-surface-50 border-surface-100 opacity-50'
                                  : 'bg-white border-surface-100'
                            ]">
                            <span class="text-[10px] font-mono font-bold text-surface-400 w-4 shrink-0">{{ ki + 1 }}</span>
                            <div class="flex-1 min-w-0">
                              <div class="font-bold text-surface-700 truncate">{{ kand.NAMA }}</div>
                              <div class="text-[9px] text-surface-400 truncate">{{ kand.PROGRAM_STUDI }}</div>
                            </div>
                            <div class="flex items-center gap-1 shrink-0">
                              <span class="font-mono font-bold text-surface-600 text-[10px]">{{ Math.round(kand['Hybrid Score'] * 100) }}%</span>
                              <span v-if="kand.sudah_terpakai && ki !== hasil.penguji_2.ranking_asli"
                                class="text-[9px] bg-red-100 text-red-500 px-1 rounded font-bold">terpakai</span>
                              <span v-else-if="ki === hasil.penguji_2.ranking_asli"
                                class="text-[9px] bg-fuchsia-100 text-fuchsia-600 px-1 rounded font-bold">✓ dipilih</span>
                            </div>
                          </div>
                        </div>
                      </div>

                      <!-- Breakdown skor -->
                      <div class="md:col-span-2 bg-surface-50 border border-surface-200 rounded-xl p-4">
                        <div class="text-[10px] font-bold text-surface-400 uppercase tracking-widest mb-3">Breakdown Skor Komponen</div>
                        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono text-center">
                          <div class="bg-white border border-blue-100 rounded-lg p-2.5">
                            <div class="text-[10px] text-blue-400 uppercase mb-1">BM25 — Penguji 1</div>
                            <div class="text-blue-700 font-bold text-base">{{ Math.round(hasil.penguji_1.lexical_score * 100) }}%</div>
                          </div>
                          <div class="bg-white border border-fuchsia-100 rounded-lg p-2.5">
                            <div class="text-[10px] text-fuchsia-400 uppercase mb-1">SBERT — Penguji 1</div>
                            <div class="text-fuchsia-700 font-bold text-base">{{ Math.round(hasil.penguji_1.semantic_score * 100) }}%</div>
                          </div>
                          <div class="bg-white border border-blue-100 rounded-lg p-2.5">
                            <div class="text-[10px] text-blue-400 uppercase mb-1">BM25 — Penguji 2</div>
                            <div class="text-blue-700 font-bold text-base">{{ Math.round(hasil.penguji_2.lexical_score * 100) }}%</div>
                          </div>
                          <div class="bg-white border border-fuchsia-100 rounded-lg p-2.5">
                            <div class="text-[10px] text-fuchsia-400 uppercase mb-1">SBERT — Penguji 2</div>
                            <div class="text-fuchsia-700 font-bold text-base">{{ Math.round(hasil.penguji_2.semantic_score * 100) }}%</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
        <div class="px-4 py-3 bg-surface-50 border-t border-surface-100 text-[10px] text-surface-400 text-center">
          Klik baris untuk melihat detail kandidat dan breakdown skor
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import * as XLSX from 'xlsx';
import api from '../services/api.js';
import { showToast } from '../utils/toast.js';

// ─── Konfigurasi ─────────────────────────────────────────────────────
// Top-K yang diminta ke server per mahasiswa. Karena setiap dosen hanya
// bisa dipakai 1x di seluruh batch, daftar kandidat yang diminta harus
// jauh lebih besar dari 2x jumlah mahasiswa supaya fallback tidak mentok
// duluan padahal dosen lain yang relevan masih ada.
const MARGIN_FALLBACK = 10; // ekstra kandidat di luar yang dibutuhkan murni

// ─── State ───────────────────────────────────────────────────────────
const isDragging       = ref(false);
const fileTerpilih     = ref(null);
const dataMahasiswa    = ref([]);
const errorValidasi    = ref([]);
const isMemproses      = ref(false);
const progressSelesai  = ref(0);
const hasilBatch       = ref([]);
const detailTerbuka    = ref(null);
const topKDigunakan    = ref(20);
const jumlahTotalDosen = ref(null); // diisi dari respons server jika tersedia

// ─── Computed ────────────────────────────────────────────────────────
const jumlahDosenTerpakai = computed(() => {
  const set = new Set();
  hasilBatch.value.forEach(h => {
    if (h.penguji_1.nama && h.penguji_1.nama !== 'Tidak tersedia' && h.penguji_1.nama !== 'Gagal diproses') {
      set.add(h.penguji_1.nama);
    }
    if (h.penguji_2.nama && h.penguji_2.nama !== 'Tidak tersedia' && h.penguji_2.nama !== 'Gagal diproses') {
      set.add(h.penguji_2.nama);
    }
  });
  return set.size;
});

const rerataSkorHybrid = computed(() => {
  if (!hasilBatch.value.length) return '0%';
  let total = 0;
  let count = 0;
  hasilBatch.value.forEach(h => {
    if (h.penguji_1.hybrid_score > 0) { total += h.penguji_1.hybrid_score; count++; }
    if (h.penguji_2.hybrid_score > 0) { total += h.penguji_2.hybrid_score; count++; }
  });
  if (count === 0) return '0%';
  return Math.round((total / count) * 100) + '%';
});

const jumlahFallback = computed(() =>
  hasilBatch.value.filter(h => h.penguji_1.is_fallback || h.penguji_2.is_fallback).length
);

const jumlahGagalKapasitas = computed(() =>
  hasilBatch.value.filter(h => h.penguji_1.nama === 'Tidak tersedia' || h.penguji_2.nama === 'Tidak tersedia').length
);

// Peringatan dini sebelum proses: jika dosen yang diketahui terlalu sedikit
// dibanding kebutuhan (2 slot unik per mahasiswa), beri tahu pengguna.
// jumlahTotalDosen hanya terisi setelah panggilan pertama ke server (lihat prosesBatch),
// jadi peringatan ini bersifat informasi pasca-percobaan pertama kali batch sebelumnya dijalankan.
const peringatanKapasitas = computed(() => {
  if (!jumlahTotalDosen.value) return '';
  const kebutuhanSlot = dataMahasiswa.value.length * 2;
  if (jumlahTotalDosen.value < kebutuhanSlot) {
    return `Total dosen yang terdaftar di sistem (${jumlahTotalDosen.value}) lebih kecil dari kebutuhan slot (${kebutuhanSlot} = ${dataMahasiswa.value.length} mahasiswa × 2 penguji). Sebagian mahasiswa kemungkinan tidak akan mendapat 2 penguji lengkap.`;
  }
  return '';
});

// ─── Helper: tampilkan kandidat cukup sampai ranking yang dipilih terlihat ─
const tampilKandidat = (semua, rankingAsli) => {
  const minTampil = Math.max(5, (rankingAsli ?? 0) + 2);
  return semua.slice(0, minTampil);
};

// ─── File Handling ───────────────────────────────────────────────────
const handleFileChange = (e) => {
  const file = e.target.files[0];
  if (file) prosesBacaFile(file);
};

const handleDrop = (e) => {
  isDragging.value = false;
  const file = e.dataTransfer.files[0];
  if (file) prosesBacaFile(file);
};

const hapusFile = () => {
  fileTerpilih.value = null;
  dataMahasiswa.value = [];
  errorValidasi.value = [];
  hasilBatch.value = [];
  detailTerbuka.value = null;
};

const formatUkuranFile = (bytes) => {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
};

const prosesBacaFile = async (file) => {
  fileTerpilih.value = file;
  hasilBatch.value = [];
  errorValidasi.value = [];
  detailTerbuka.value = null;

  let rows;
  try {
    const buffer = await file.arrayBuffer();
    const workbook = XLSX.read(buffer, { type: 'array' });
    const sheet = workbook.Sheets[workbook.SheetNames[0]];
    rows = XLSX.utils.sheet_to_json(sheet, { defval: '' });
  } catch (err) {
    errorValidasi.value = ['File tidak bisa dibaca. Pastikan formatnya .xlsx, .xls, atau .csv yang valid.'];
    dataMahasiswa.value = [];
    return;
  }

  // Normalisasi header (case-insensitive, trim spasi)
  const normalized = rows.map(row => {
    const obj = {};
    Object.keys(row).forEach(k => {
      obj[k.toLowerCase().trim().replace(/\s+/g, '_')] = String(row[k]).trim();
    });
    return obj;
  });

  // Validasi kolom wajib
  const kolomWajib = ['nama_mahasiswa', 'nim', 'judul_ta', 'abstrak'];
  const errors = [];

  if (normalized.length === 0) {
    errors.push('File tidak memiliki data (kosong).');
  } else {
    const kolomAda = Object.keys(normalized[0]);
    kolomWajib.forEach(k => {
      if (!kolomAda.includes(k)) errors.push(`Kolom "${k}" tidak ditemukan. Pastikan header sesuai template.`);
    });

    if (errors.length === 0) {
      normalized.forEach((row, i) => {
        if (!row.nama_mahasiswa) errors.push(`Baris ${i + 2}: Nama mahasiswa kosong.`);
        if (!row.nim) errors.push(`Baris ${i + 2}: NIM kosong.`);
        if (!row.judul_ta) errors.push(`Baris ${i + 2}: Judul TA kosong.`);
        if (!row.abstrak) errors.push(`Baris ${i + 2}: Abstrak kosong.`);
      });

      // Deteksi NIM duplikat di dalam file itu sendiri
      const nimCount = {};
      normalized.forEach((row) => {
        if (row.nim) nimCount[row.nim] = (nimCount[row.nim] || 0) + 1;
      });
      Object.entries(nimCount).forEach(([nim, count]) => {
        if (count > 1) errors.push(`NIM "${nim}" muncul ${count} kali di file. Setiap mahasiswa harus unik.`);
      });
    }
  }

  errorValidasi.value = errors;
  dataMahasiswa.value = normalized;
};

// ─── Proses Batch ────────────────────────────────────────────────────
const prosesBatch = async () => {
  isMemproses.value = true;
  progressSelesai.value = 0;
  hasilBatch.value = [];
  detailTerbuka.value = null;

  // Top-K dinamis: minta cukup kandidat agar fallback punya ruang gerak
  // walau hampir semua dosen sudah terpakai di akhir batch.
  // Tiap mahasiswa butuh 2 slot unik; di titik mahasiswa terakhir, hingga
  // (n-1)*2 dosen sudah terpakai, jadi minta keseluruhan + margin.
  const totalMahasiswa = dataMahasiswa.value.length;
  const topK = Math.max(20, totalMahasiswa * 2 + MARGIN_FALLBACK);
  topKDigunakan.value = topK;

  // Set dosen terpakai global — deduplikasi lintas mahasiswa
  const dosenTerpakai = new Set();
  const hasil = [];

  for (let i = 0; i < dataMahasiswa.value.length; i++) {
    const mhs = dataMahasiswa.value[i];

    try {
      const res = await api.getRekomendasi(mhs.judul_ta, mhs.abstrak, topK, -1, -1);
      const semua = res.data.hasil_rekomendasi;

      // Simpan info jumlah total dosen di sistem (jika server menyediakannya)
      // untuk keperluan peringatan kapasitas di UI.
      if (res.data.metadata_mesin && typeof res.data.metadata_mesin.total_dosen === 'number') {
        jumlahTotalDosen.value = res.data.metadata_mesin.total_dosen;
      } else if (jumlahTotalDosen.value === null) {
        // fallback kasar: panjang daftar yang dikembalikan, minimal sebagai estimasi
        jumlahTotalDosen.value = semua.length;
      }

      // Snapshot status terpakai SEBELUM memilih (untuk tampilan UI yang akurat)
      const kandidatDenganStatus = semua.map(d => ({
        ...d,
        sudah_terpakai: dosenTerpakai.has(d.NAMA),
      }));

      // ── Pilih Penguji 1: dosen terbaik yang belum terpakai ──
      let penguji1Data = null;
      let rankingP1 = -1;
      for (let r = 0; r < kandidatDenganStatus.length; r++) {
        if (!kandidatDenganStatus[r].sudah_terpakai) {
          penguji1Data = kandidatDenganStatus[r];
          rankingP1 = r;
          break;
        }
      }

      // Tandai Penguji 1 sebagai terpakai, update snapshot untuk P2
      if (penguji1Data) {
        dosenTerpakai.add(penguji1Data.NAMA);
        kandidatDenganStatus.forEach(k => {
          if (k.NAMA === penguji1Data.NAMA) k.sudah_terpakai = true;
        });
      }

      // ── Pilih Penguji 2: dosen terbaik berikutnya yang belum terpakai ──
      let penguji2Data = null;
      let rankingP2 = -1;
      for (let r = 0; r < kandidatDenganStatus.length; r++) {
        if (!kandidatDenganStatus[r].sudah_terpakai) {
          penguji2Data = kandidatDenganStatus[r];
          rankingP2 = r;
          break;
        }
      }

      if (penguji2Data) dosenTerpakai.add(penguji2Data.NAMA);

      // is_fallback didefinisikan konsisten untuk P1 dan P2:
      // true jika ada kandidat dengan peringkat lebih tinggi yang dilewati
      // karena sudah terpakai oleh mahasiswa sebelumnya.
      // Untuk P1: fallback jika rankingP1 melewati kandidat #0 (yang berarti
      //   kandidat #0..rankingP1-1 semuanya sudah terpakai).
      // Untuk P2: fallback jika rankingP2 melewati slot ideal langsung
      //   setelah P1 (rankingP1 + 1).
      const isFallbackP1 = rankingP1 > 0;
      const rankingIdealP2 = rankingP1 >= 0 ? rankingP1 + 1 : 1;
      const isFallbackP2 = rankingP2 > rankingIdealP2;

      hasil.push({
        nama_mahasiswa: mhs.nama_mahasiswa,
        nim: mhs.nim,
        judul_ta: mhs.judul_ta,
        semua_kandidat: kandidatDenganStatus,
        kapasitas_habis: !penguji1Data || !penguji2Data,
        penguji_1: penguji1Data ? {
          nama: penguji1Data.NAMA,
          program_studi: penguji1Data.PROGRAM_STUDI,
          hybrid_score: penguji1Data['Hybrid Score'],
          lexical_score: penguji1Data['Lexical Score'],
          semantic_score: penguji1Data['Semantic Score'],
          ranking_asli: rankingP1,
          is_fallback: isFallbackP1,
        } : {
          nama: 'Tidak tersedia', program_studi: '-',
          hybrid_score: 0, lexical_score: 0, semantic_score: 0,
          ranking_asli: -1, is_fallback: false,
        },
        penguji_2: penguji2Data ? {
          nama: penguji2Data.NAMA,
          program_studi: penguji2Data.PROGRAM_STUDI,
          hybrid_score: penguji2Data['Hybrid Score'],
          lexical_score: penguji2Data['Lexical Score'],
          semantic_score: penguji2Data['Semantic Score'],
          ranking_asli: rankingP2,
          is_fallback: isFallbackP2,
        } : {
          nama: 'Tidak tersedia', program_studi: '-',
          hybrid_score: 0, lexical_score: 0, semantic_score: 0,
          ranking_asli: -1, is_fallback: false,
        },
      });

    } catch (err) {
      console.error(`Gagal proses mahasiswa ${mhs.nama_mahasiswa}:`, err);
      hasil.push({
        nama_mahasiswa: mhs.nama_mahasiswa,
        nim: mhs.nim,
        judul_ta: mhs.judul_ta,
        semua_kandidat: [],
        kapasitas_habis: false,
        penguji_1: { nama: 'Gagal diproses', program_studi: '-', hybrid_score: 0, lexical_score: 0, semantic_score: 0, ranking_asli: -1, is_fallback: false },
        penguji_2: { nama: 'Gagal diproses', program_studi: '-', hybrid_score: 0, lexical_score: 0, semantic_score: 0, ranking_asli: -1, is_fallback: false },
      });
    }

    progressSelesai.value = i + 1;
  }

  hasilBatch.value = hasil;
  isMemproses.value = false;

  const gagalKapasitas = hasil.filter(h => h.kapasitas_habis).length;
  const gagalError = hasil.filter(h => h.penguji_1.nama === 'Gagal diproses').length;

  if (gagalError > 0) {
    showToast(`Selesai dengan catatan: ${gagalError} mahasiswa gagal diproses karena error server.`, 'error');
  } else if (gagalKapasitas > 0) {
    showToast(`Selesai, tapi ${gagalKapasitas} mahasiswa tidak mendapat 2 penguji lengkap (stok dosen habis).`, 'error');
  } else {
    showToast(`Selesai! ${hasil.length} mahasiswa berhasil diproses dengan 2 penguji masing-masing.`, 'success');
  }
};

// ─── Toggle detail row ────────────────────────────────────────────────
const toggleDetail = (i) => {
  detailTerbuka.value = detailTerbuka.value === i ? null : i;
};

// ─── Unduh Template ──────────────────────────────────────────────────
const unduhTemplate = () => {
  const template = [
    {
      nama_mahasiswa: 'Budi Santoso',
      nim: '12345001',
      judul_ta: 'Implementasi Machine Learning untuk Klasifikasi Penyakit',
      abstrak: 'Penelitian ini mengembangkan model machine learning untuk mengklasifikasikan penyakit berdasarkan data gejala pasien menggunakan algoritma Random Forest dan SVM.',
    },
    {
      nama_mahasiswa: 'Siti Rahayu',
      nim: '12345002',
      judul_ta: 'Sistem Deteksi Wajah Menggunakan Deep Learning',
      abstrak: 'Sistem ini menggunakan metode deep learning dengan arsitektur CNN untuk mendeteksi dan mengenali wajah secara real-time pada video surveillance.',
    },
    {
      nama_mahasiswa: 'Ahmad Fauzi',
      nim: '12345003',
      judul_ta: 'Analisis Sentimen Ulasan Produk dengan NLP',
      abstrak: 'Penelitian menggunakan Natural Language Processing untuk menganalisis sentimen ulasan produk e-commerce menggunakan model BERT dan LSTM.',
    },
    {
      nama_mahasiswa: 'Dewi Lestari',
      nim: '12345004',
      judul_ta: 'Rancang Bangun Sistem Informasi Akademik Berbasis Web',
      abstrak: 'Penelitian ini membangun sistem informasi akademik berbasis web menggunakan Laravel untuk mempermudah pengelolaan data mahasiswa, dosen, dan jadwal kuliah.',
    },
    {
      nama_mahasiswa: 'Rizky Pratama',
      nim: '12345005',
      judul_ta: 'Implementasi Internet of Things untuk Smart Home',
      abstrak: 'Sistem smart home dikembangkan menggunakan ESP32 dan MQTT untuk mengendalikan perangkat elektronik serta memantau kondisi rumah secara real-time.',
    },
    {
      nama_mahasiswa: 'Nabila Putri',
      nim: '12345006',
      judul_ta: 'Prediksi Harga Saham Menggunakan Long Short-Term Memory',
      abstrak: 'Penelitian ini memanfaatkan algoritma LSTM untuk memprediksi pergerakan harga saham berdasarkan data historis dengan tingkat akurasi yang optimal.',
    },
    {
      nama_mahasiswa: 'Andi Saputra',
      nim: '12345007',
      judul_ta: 'Sistem Rekomendasi Buku Menggunakan Collaborative Filtering',
      abstrak: 'Penelitian mengembangkan sistem rekomendasi buku berbasis collaborative filtering untuk memberikan rekomendasi yang sesuai dengan preferensi pengguna.',
    },
    {
      nama_mahasiswa: 'Maya Kusuma',
      nim: '12345008',
      judul_ta: 'Klasifikasi Citra Daun Tanaman Menggunakan Convolutional Neural Network',
      abstrak: 'Model CNN diterapkan untuk mengidentifikasi jenis tanaman berdasarkan citra daun dengan tujuan membantu proses identifikasi secara otomatis.',
    },
    {
      nama_mahasiswa: 'Fajar Nugroho',
      nim: '12345009',
      judul_ta: 'Sistem Monitoring Kualitas Udara Berbasis IoT',
      abstrak: 'Penelitian membangun sistem monitoring kualitas udara menggunakan sensor gas dan mikrokontroler yang terhubung ke platform cloud untuk pemantauan jarak jauh.',
    },
    {
      nama_mahasiswa: 'Putri Ayuningtyas',
      nim: '12345010',
      judul_ta: 'Chatbot Layanan Akademik Menggunakan Large Language Model',
      abstrak: 'Penelitian mengembangkan chatbot akademik berbasis Large Language Model untuk menjawab pertanyaan mahasiswa secara otomatis dan kontekstual.',
    },
  ];
  const wb = XLSX.utils.book_new();
  const ws = XLSX.utils.json_to_sheet(template);
  ws['!cols'] = [{ wch: 25 }, { wch: 15 }, { wch: 60 }, { wch: 80 }];
  XLSX.utils.book_append_sheet(wb, ws, 'Data Mahasiswa');
  XLSX.writeFile(wb, 'template_batch_rekomendasi.xlsx');
  showToast('Template berhasil diunduh!', 'success');
};

// ─── Unduh Hasil ─────────────────────────────────────────────────────
const unduhHasil = () => {
  if (!hasilBatch.value.length) return;

  const rows = hasilBatch.value.map((h, i) => ({
    'No': i + 1,
    'Nama Mahasiswa': h.nama_mahasiswa,
    'NIM': h.nim,
    'Judul TA': h.judul_ta,
    'Penguji 1': h.penguji_1.nama,
    'Prodi Penguji 1': h.penguji_1.program_studi,
    'Skor Penguji 1 (%)': Math.round(h.penguji_1.hybrid_score * 100),
    'BM25 Penguji 1 (%)': Math.round(h.penguji_1.lexical_score * 100),
    'SBERT Penguji 1 (%)': Math.round(h.penguji_1.semantic_score * 100),
    'Ranking Penguji 1': h.penguji_1.ranking_asli >= 0 ? h.penguji_1.ranking_asli + 1 : '-',
    'Penguji 1 Fallback': h.penguji_1.is_fallback ? 'Ya' : 'Tidak',
    'Penguji 2': h.penguji_2.nama,
    'Prodi Penguji 2': h.penguji_2.program_studi,
    'Skor Penguji 2 (%)': Math.round(h.penguji_2.hybrid_score * 100),
    'BM25 Penguji 2 (%)': Math.round(h.penguji_2.lexical_score * 100),
    'SBERT Penguji 2 (%)': Math.round(h.penguji_2.semantic_score * 100),
    'Ranking Penguji 2': h.penguji_2.ranking_asli >= 0 ? h.penguji_2.ranking_asli + 1 : '-',
    'Penguji 2 Fallback': h.penguji_2.is_fallback ? 'Ya' : 'Tidak',
    'Status': h.kapasitas_habis ? 'Tidak lengkap (stok dosen habis)' : (h.penguji_1.nama === 'Gagal diproses' ? 'Gagal diproses' : 'Lengkap'),
  }));

  const wb = XLSX.utils.book_new();
  const ws = XLSX.utils.json_to_sheet(rows);
  ws['!cols'] = [
    { wch: 4 }, { wch: 25 }, { wch: 15 }, { wch: 60 },
    { wch: 30 }, { wch: 20 }, { wch: 14 }, { wch: 14 }, { wch: 14 }, { wch: 14 }, { wch: 15 },
    { wch: 30 }, { wch: 20 }, { wch: 14 }, { wch: 14 }, { wch: 14 }, { wch: 14 }, { wch: 15 },
    { wch: 28 },
  ];

  XLSX.utils.book_append_sheet(wb, ws, 'Hasil Rekomendasi');
  const tanggal = new Date().toISOString().slice(0, 10);
  XLSX.writeFile(wb, `hasil_rekomendasi_dosen_${tanggal}.xlsx`);
  showToast('Hasil berhasil diunduh!', 'success');
};
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}
.line-clamp-2 {
  display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    overflow: hidden;
}
</style>