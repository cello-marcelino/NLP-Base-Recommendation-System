<template>
  <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">

    <!-- Header Dashboard -->
    <div class="flex flex-col md:flex-row md:justify-between md:items-end gap-5 mb-6">
      <div>
        <h2 class="text-3xl font-extrabold text-surface-800 tracking-tight">Riwayat Rekomendasi</h2>
        <p class="text-surface-500 mt-1">Pantau rekam jejak pengujian skripsi dan hasil rekomendasi AI mahasiswa.</p>
      </div>
      <div class="flex items-center w-full md:w-auto">
        <button
          @click="muatData"
          :disabled="sedangMemuat"
          class="w-full md:w-auto flex justify-center items-center gap-2 bg-white border border-surface-200 hover:bg-surface-50 disabled:opacity-60 disabled:cursor-not-allowed text-surface-700 px-5 py-2.5 rounded-xl shadow-sm font-medium transition-all focus:ring-2 focus:ring-surface-200 outline-none"
        >
          <svg class="w-5 h-5" :class="{ 'animate-spin': sedangMemuat }" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
          {{ sedangMemuat ? 'Memuat...' : 'Segarkan Data' }}
        </button>
      </div>
    </div>

    <!-- Kartu Ringkasan -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
      <div class="bg-white border border-surface-200 rounded-2xl p-5 flex items-center gap-4 shadow-sm">
        <div class="shrink-0 w-11 h-11 rounded-xl bg-primary-50 text-primary-600 flex items-center justify-center">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2"></path></svg>
        </div>
        <div>
          <p class="text-xs font-bold uppercase tracking-wider text-surface-400">Total Pengujian</p>
          <p class="text-2xl font-extrabold text-surface-800 tabular-nums">{{ daftarRiwayat.length }}</p>
        </div>
      </div>

      <div class="bg-white border border-surface-200 rounded-2xl p-5 flex items-center gap-4 shadow-sm">
        <div class="shrink-0 w-11 h-11 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
        </div>
        <div>
          <p class="text-xs font-bold uppercase tracking-wider text-surface-400">Hari Ini</p>
          <p class="text-2xl font-extrabold text-surface-800 tabular-nums">{{ jumlahHariIni }}</p>
        </div>
      </div>

      <div class="bg-white border border-surface-200 rounded-2xl p-5 flex items-center gap-4 shadow-sm">
        <div class="shrink-0 w-11 h-11 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        </div>
        <div>
          <p class="text-xs font-bold uppercase tracking-wider text-surface-400">Pengujian Terakhir</p>
          <p class="text-sm font-bold text-surface-800 mt-1">{{ aktivitasTerakhir }}</p>
        </div>
      </div>
    </div>

    <!-- Tabel Riwayat Utama -->
    <div class="bg-white rounded-2xl shadow-sm border border-surface-200 overflow-hidden mb-6">

      <div class="p-4 border-b border-surface-100 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div class="relative w-full sm:w-80">
          <svg class="w-4 h-4 text-surface-400 absolute left-3.5 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11a6 6 0 11-12 0 6 6 0 0112 0z"></path></svg>
          <input
            v-model="pencarian"
            type="text"
            placeholder="Cari judul skripsi..."
            class="w-full pl-10 pr-3 py-2.5 text-sm rounded-xl border border-surface-200 bg-surface-50/60 focus:bg-white focus:ring-2 focus:ring-primary-100 focus:border-primary-300 outline-none transition-all"
          />
        </div>
        <span class="text-xs font-semibold text-surface-400 sm:pr-1">
          Menampilkan {{ daftarRiwayatTersaring.length }} dari {{ daftarRiwayat.length }} riwayat
        </span>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-surface-50/50 border-b border-surface-200 text-xs uppercase tracking-widest text-surface-400 font-bold">
              <th class="p-5 font-bold w-48">Waktu Uji</th>
              <th class="p-5 font-bold">Judul Skripsi Mahasiswa</th>
              <th class="p-5 font-bold text-center">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-surface-100">

            <!-- Skeleton loading -->
            <template v-if="sedangMemuat">
              <tr v-for="n in 4" :key="'skeleton-' + n">
                <td class="p-5"><div class="h-3.5 w-28 rounded bg-surface-100 animate-pulse"></div></td>
                <td class="p-5">
                  <div class="h-3.5 w-56 rounded bg-surface-100 animate-pulse mb-2"></div>
                  <div class="h-3 w-72 rounded bg-surface-100 animate-pulse"></div>
                </td>
                <td class="p-5 text-center"><div class="h-8 w-28 rounded-lg bg-surface-100 animate-pulse mx-auto"></div></td>
              </tr>
            </template>

            <!-- Empty state: belum pernah ada riwayat -->
            <tr v-else-if="daftarRiwayat.length === 0">
              <td colspan="3" class="p-10 text-center">
                <div class="flex flex-col items-center justify-center text-surface-400">
                  <svg class="w-12 h-12 mb-3 text-surface-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                  <span class="font-bold text-base text-surface-500">Belum ada riwayat.</span>
                  <span class="text-sm mt-1">Log akan muncul saat ada yang menggunakan sistem rekomendasi.</span>
                </div>
              </td>
            </tr>

            <!-- Empty state: pencarian tidak ditemukan -->
            <tr v-else-if="daftarRiwayatTersaring.length === 0">
              <td colspan="3" class="p-10 text-center">
                <div class="flex flex-col items-center justify-center text-surface-400">
                  <svg class="w-12 h-12 mb-3 text-surface-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-4.35-4.35M17 11a6 6 0 11-12 0 6 6 0 0112 0z"></path></svg>
                  <span class="font-bold text-base text-surface-500">Judul tidak ditemukan.</span>
                  <span class="text-sm mt-1">Coba gunakan kata kunci lain.</span>
                </div>
              </td>
            </tr>

            <tr v-for="riwayat in daftarRiwayatTersaring" :key="riwayat.id_log" class="hover:bg-surface-50/80 transition-colors group">
              <td class="p-5 text-sm font-medium text-surface-600 whitespace-nowrap">
                {{ formatTanggal(riwayat.created_at) }}
              </td>
              <td class="p-5">
                <div class="font-bold text-primary-500 text-sm line-clamp-1" :title="riwayat.judul_mhs">{{ riwayat.judul_mhs }}</div>
                <div class="text-xs text-surface-500 mt-1 line-clamp-2" :title="riwayat.abstrak_mhs">{{ riwayat.abstrak_mhs }}</div>
              </td>
              <td class="p-5 text-center">
                <button @click="bukaDetailModal(riwayat)" class="text-sm bg-white border border-surface-300 text-surface-600 font-semibold px-4 py-2 rounded-lg transition-all hover:border-primary-400 hover:bg-primary-50 hover:text-primary-700 shadow-sm whitespace-nowrap inline-flex items-center gap-1.5">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>
                  Lihat 3 Teratas
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Detail Hasil JSON -->
    <transition enter-active-class="ease-out duration-300" enter-from-class="opacity-0" enter-to-class="opacity-100" leave-active-class="ease-in duration-200" leave-from-class="opacity-100" leave-to-class="opacity-0">
      <div v-if="modalAktif" class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
        <div class="fixed inset-0 bg-surface-800/40 backdrop-blur-sm transition-opacity" @click="modalAktif = false"></div>

        <transition enter-active-class="ease-out duration-300" enter-from-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95" enter-to-class="opacity-100 translate-y-0 sm:scale-100" leave-active-class="ease-in duration-200" leave-from-class="opacity-100 translate-y-0 sm:scale-100" leave-to-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
          <div v-if="modalAktif" class="relative w-full max-w-4xl bg-white rounded-2xl shadow-xl border border-surface-200 overflow-hidden transform transition-all flex flex-col max-h-[90vh]">

            <div class="px-6 py-5 border-b border-surface-100 flex justify-between items-center bg-surface-50/50">
              <div>
                <h3 class="text-lg font-extrabold text-surface-800">Detail Hasil Rekomendasi</h3>
                <p class="text-xs text-surface-400 font-medium mt-0.5">{{ formatTanggal(riwayatTerpilih?.created_at) }}</p>
              </div>
              <button @click="modalAktif = false" class="text-surface-400 hover:text-red-500 transition-colors outline-none rounded-lg p-1.5 hover:bg-surface-100">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
              </button>
            </div>

            <div class="p-6 overflow-y-auto custom-scrollbar">

              <div class="bg-surface-50 border border-surface-200 rounded-xl p-4 mb-6">
                <h4 class="text-sm font-bold text-surface-500 uppercase tracking-wider mb-2">Data Input Skripsi</h4>
                <p class="font-bold text-surface-800 text-lg mb-2">{{ riwayatTerpilih?.judul_mhs }}</p>
                <p class="text-sm text-surface-600 leading-relaxed">{{ riwayatTerpilih?.abstrak_mhs }}</p>
              </div>

              <h4 class="text-sm font-bold text-surface-500 uppercase tracking-wider mb-3">Top 3 Dosen Pembimbing</h4>

              <div class="space-y-3">
                <div
                  v-for="(dosen, index) in daftarDosenHasil"
                  :key="index"
                  class="rounded-xl border p-4 transition-all"
                  :class="index === 0 ? 'border-amber-200 bg-amber-50/50' : 'border-surface-200 bg-white'"
                >
                  <div class="flex items-center justify-between gap-3 mb-3">
                    <div class="flex items-center gap-3 min-w-0">
                      <span
                        class="shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-extrabold border"
                        :class="lencanaPeringkat(index).kelas"
                      >
                        {{ lencanaPeringkat(index).label }}
                      </span>
                      <span class="font-bold text-surface-800 truncate">{{ dosen.nama }}</span>
                    </div>
                    <span class="shrink-0 text-lg font-extrabold text-primary-600 tabular-nums">{{ (dosen.skor_hybrid * 100).toFixed(2) }}%</span>
                  </div>

                  <div class="space-y-2">
                    <div>
                      <div class="flex justify-between text-xs font-semibold text-surface-500 mb-1">
                        <span>Semantik (AI)</span>
                        <span class="tabular-nums">{{ (dosen.skor_semantik * 100).toFixed(2) }}%</span>
                      </div>
                      <div class="h-1.5 w-full rounded-full bg-surface-100 overflow-hidden">
                        <div class="h-full rounded-full bg-indigo-400" :style="{ width: Math.min(dosen.skor_semantik * 100, 100) + '%' }"></div>
                      </div>
                    </div>
                    <div>
                      <div class="flex justify-between text-xs font-semibold text-surface-500 mb-1">
                        <span>Leksikal (BM25)</span>
                        <span class="tabular-nums">{{ (dosen.skor_leksikal * 100).toFixed(2) }}%</span>
                      </div>
                      <div class="h-1.5 w-full rounded-full bg-surface-100 overflow-hidden">
                        <div class="h-full rounded-full bg-primary-400" :style="{ width: Math.min(dosen.skor_leksikal * 100, 100) + '%' }"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

            </div>

            <div class="px-6 py-4 bg-surface-50/80 border-t border-surface-100 flex justify-end rounded-b-2xl shrink-0">
              <button @click="modalAktif = false" class="px-6 py-2.5 bg-primary-600 hover:bg-primary-700 text-white font-bold rounded-xl shadow-sm transition-all">
                Tutup Jendela
              </button>
            </div>

          </div>
        </transition>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '../services/api';
import { showToast } from '../utils/toast';

const daftarRiwayat = ref([]);
const sedangMemuat = ref(false);
const pencarian = ref('');
const modalAktif = ref(false);
const riwayatTerpilih = ref(null);
const daftarDosenHasil = ref([]);

const formatTanggal = (dateString) => {
  if (!dateString) return '-';
  const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
  return new Date(dateString).toLocaleDateString('id-ID', options);
};

// Riwayat yang tampil di tabel, tersaring berdasarkan judul skripsi
const daftarRiwayatTersaring = computed(() => {
  const kata = pencarian.value.trim().toLowerCase();
  if (!kata) return daftarRiwayat.value;
  return daftarRiwayat.value.filter(r => (r.judul_mhs || '').toLowerCase().includes(kata));
});

// Jumlah pengujian yang dilakukan hari ini
const jumlahHariIni = computed(() => {
  const hariIni = new Date().toDateString();
  return daftarRiwayat.value.filter(r => r.created_at && new Date(r.created_at).toDateString() === hariIni).length;
});

// Waktu pengujian paling baru (asumsi data terurut terbaru lebih dulu)
const aktivitasTerakhir = computed(() => {
  if (daftarRiwayat.value.length === 0) return 'Belum ada aktivitas';
  return formatTanggal(daftarRiwayat.value[0].created_at);
});

// Lencana peringkat 1, 2, 3 pada modal detail
const lencanaPeringkat = (index) => {
  const gaya = [
    { label: '1', kelas: 'bg-amber-100 text-amber-700 border-amber-300' },
    { label: '2', kelas: 'bg-surface-100 text-surface-600 border-surface-300' },
    { label: '3', kelas: 'bg-orange-100 text-orange-700 border-orange-300' },
  ];
  return gaya[index] || { label: String(index + 1), kelas: 'bg-surface-100 text-surface-600 border-surface-300' };
};

const muatData = async () => {
  sedangMemuat.value = true;
  try {
    const res = await api.getRiwayat();
    if (res.status === 'sukses') {
      daftarRiwayat.value = res.data || [];
    } else {
      showToast('Gagal memuat riwayat', 'error');
    }
  } catch (error) {
    console.error(error);
    showToast('Terjadi kesalahan jaringan.', 'error');
  } finally {
    sedangMemuat.value = false;
  }
};

// BUG FIX: PENCARI SKOR SUPER KEBAL (Case-Insensitive & Kata Kunci Pendek)
const ekstrakSkor = (objekDosen, daftarKataKunci) => {
  // 1. Ambil semua kunci yang ada di JSON objek dosen tersebut
  const daftarKunciJSON = Object.keys(objekDosen);

  // 2. Loop setiap kata kunci tebakan kita
  for (const kataKunci of daftarKataKunci) {
    const kataKunciLower = kataKunci.toLowerCase();

    // 3. Cari apakah ada kunci di JSON yang MENGANDUNG kata tebakan kita (mengabaikan kapitalisasi)
    const kunciCocok = daftarKunciJSON.find(k => k.toLowerCase().includes(kataKunciLower));

    // 4. Jika ketemu, kembalikan angkanya
    if (kunciCocok && objekDosen[kunciCocok] !== undefined && objekDosen[kunciCocok] !== null) {
      return parseFloat(objekDosen[kunciCocok]);
    }
  }

  return 0; // Jika benar-benar tidak ditemukan satupun
};

const bukaDetailModal = (riwayat) => {
  riwayatTerpilih.value = riwayat;

  try {
    let rawDataArray = typeof riwayat.hasil_rekomendasi_json === 'string'
      ? JSON.parse(riwayat.hasil_rekomendasi_json)
      : riwayat.hasil_rekomendasi_json || [];

    // Membatasi Top-3 dan menarik skor dengan aman
    daftarDosenHasil.value = rawDataArray.slice(0, 3).map(dosen => ({
      nama: dosen.nama || dosen.NAMA || 'Nama Tidak Diketahui',

      // Kita cukup berikan kata kunci dasar (huruf kecil), fungsi akan otomatis mencarikan kecocokannya
      skor_hybrid: ekstrakSkor(dosen, ['hybrid', 'akhir', 'total']),
      skor_semantik: ekstrakSkor(dosen, ['semantic', 'semantik', 'sem']),
      skor_leksikal: ekstrakSkor(dosen, ['lexical', 'leksikal', 'lex'])
    }));

    modalAktif.value = true;
  } catch (error) {
    console.error("Gagal parse JSON riwayat:", error);
    showToast('Format data hasil rekomendasi rusak.', 'error');
    daftarDosenHasil.value = [];
  }
};

onMounted(() => {
  muatData();
});
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

.line-clamp-1 { display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden; }
.line-clamp-2 { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
</style>