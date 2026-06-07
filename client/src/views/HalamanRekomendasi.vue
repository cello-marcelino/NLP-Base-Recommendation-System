<template>
  <div class="max-w-7xl mx-auto py-8">

    <div v-if="isModelWarmingUp"
      class="fixed inset-0 bg-white/90 backdrop-blur-md z-50 flex flex-col items-center justify-center">
      <div class="w-16 h-16 border-4 border-primary-100 border-t-primary-600 rounded-full animate-spin mb-6"></div>
      <h2 class="text-2xl font-extrabold text-surface-800">Menyiapkan Server SIREDO...</h2>
      <p class="text-surface-500 mt-2 text-sm font-medium animate-pulse">Memuat arsitektur SBERT ke dalam memori.</p>
    </div>

    <div class="mb-8 flex flex-col md:flex-row md:justify-between md:items-end gap-4">
      <div>
        <h1 class="text-3xl font-extrabold text-surface-900 tracking-tight">
          NLP <span class="text-primary-600">Recommendation System</span>
        </h1>
        <p class="text-surface-500 mt-1 font-medium">Visualisasi Metode dan Komputasi Teknis Sistem Rekomendasi
          menggunakan model SBERT & BM25</p>
      </div>
      <button @click="handleRefresh" :disabled="isRefreshing"
        class="group flex items-center gap-2 bg-white hover:bg-primary-50 border border-surface-200 hover:border-primary-200 text-surface-600 hover:text-primary-700 px-4 py-2 rounded-xl text-sm font-bold shadow-sm transition-all active:scale-95">
        <svg
          :class="['w-4 h-4', isRefreshing ? 'animate-spin text-primary-600' : 'group-hover:rotate-180 transition-transform duration-500']"
          fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15">
          </path>
        </svg>
        {{ isRefreshing ? 'Menyegarkan Server...' : 'Refresh Server' }}
      </button>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">

      <div class="lg:col-span-4 space-y-6">

        <div class="bg-white border border-surface-200 rounded-2xl shadow-sm p-6 relative overflow-hidden">
          <div v-if="isProcessing" class="absolute inset-0 bg-linear-to-br from-primary-50 to-white/20 opacity-60">
          </div>

          <h2 class="text-sm font-bold text-surface-400 mb-5 uppercase tracking-widest relative z-10">Parameter Model
          </h2>
          <div class="space-y-5 relative z-10">
            <div>
              <label class="block text-sm font-bold text-surface-700 mb-1.5">Judul Tugas Akhir</label>
              <input v-model="judulInput" type="text" placeholder="Ketik rencana judul..."
                class="w-full p-3 bg-surface-50 border border-surface-200 rounded-xl focus:ring-4 focus:ring-primary-50 focus:border-primary-400 outline-none transition-all text-sm font-medium">
            </div>
            <div>
              <label class="block text-sm font-bold text-surface-700 mb-1.5">Abstrak Penelitian</label>
              <textarea v-model="abstrakInput" rows="5" placeholder="Jelaskan secara singkat masalah dan metode..."
                class="w-full p-3 bg-surface-50 border border-surface-200 rounded-xl focus:ring-4 focus:ring-primary-50 focus:border-primary-400 outline-none transition-all text-sm resize-none"></textarea>
            </div>
            <div class="bg-surface-50 border border-surface-100 p-4 rounded-xl">
              <div class="flex justify-between items-center mb-2">
                <label class="block text-sm font-bold text-surface-700">Distribusi Bobot AI</label>
                <span class="text-[10px] font-mono font-bold bg-primary-100 text-primary-700 px-2 py-0.5 rounded">
                  L:{{ bobotLexical }}% | S:{{ 100 - bobotLexical }}%
                </span>
              </div>
              <input type="range" v-model="bobotLexical" min="0" max="100" step="10"
                class="w-full h-1.5 bg-surface-200 rounded-lg appearance-none cursor-pointer accent-primary-600">
              <div class="flex justify-between text-[10px] font-bold text-surface-400 uppercase mt-1.5">
                <span>Leksikal (BM25)</span>
                <span>Semantik (SBERT)</span>
              </div>
            </div>
            <div class="flex gap-3">
              <div class="w-1/3">
                <label class="block text-sm font-bold text-surface-700 mb-1.5">Top-K</label>
                <input v-model="kRank" type="number" min="1" max="20"
                  class="w-full p-3 bg-surface-50 border border-surface-200 rounded-xl text-center font-bold text-surface-700 outline-none focus:border-primary-400">
              </div>
              <button @click="jalankanPipeline" :disabled="isProcessing"
                class="w-2/3 bg-primary-600 hover:bg-primary-700 disabled:bg-surface-300 disabled:text-surface-500 text-white font-bold rounded-xl transition-all active:scale-95 shadow-sm shadow-primary-200 mt-6 relative overflow-hidden">
                <span v-if="isProcessing" class="absolute inset-0 w-full h-full bg-white/20 animate-pulse"></span>
                <span class="relative z-10 flex items-center justify-center gap-2">
                  <svg v-if="isProcessing" class="w-4 h-4 animate-spin" fill="none" stroke="currentColor"
                    viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15">
                    </path>
                  </svg>
                  {{ isProcessing ? 'Menganalisis...' : 'Jalankan Model' }}
                </span>
              </button>
            </div>
          </div>
        </div>

        <div class="bg-white border border-surface-200 rounded-2xl p-6 shadow-sm">
          <div class="flex justify-between items-center mb-3">
            <span class="font-bold text-sm text-surface-700">Status Komputasi Server</span>
            <span class="font-bold text-primary-600">{{ progressPct }}%</span>
          </div>
          <div class="w-full bg-surface-100 rounded-full h-2 mb-3 overflow-hidden">
            <div
              :class="['h-2 rounded-full transition-all duration-500 ease-out', progressPct === 100 ? 'bg-emerald-500' : 'bg-primary-500']"
              :style="{ width: progressPct + '%' }"></div>
          </div>
          <p class="text-xs font-mono text-surface-500">{{ progressMsg }}</p>
        </div>

      </div>

      <div class="lg:col-span-8 space-y-4">

        <div v-if="!hasStarted"
          class="h-full min-h-400px flex flex-col items-center justify-center border-2 border-dashed border-surface-200 rounded-2xl bg-surface-50/50 text-surface-400">
          <svg class="w-16 h-16 mb-4 text-surface-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z">
            </path>
          </svg>
          <span class="font-bold text-surface-500">Menunggu Injeksi Parameter...</span>
        </div>

        <div v-for="step in pipeline" :key="step.id" v-show="hasStarted && step.status !== 'idle'"
          :class="['rounded-2xl border transition-all duration-500 overflow-hidden relative', step.status === 'running' ? 'border-primary-300 shadow-lg shadow-primary-100/50 bg-white scale-[1.01]' : 'border-surface-200 bg-white']">

          <div v-if="step.status === 'running'" class="absolute top-0 left-0 h-0.5 bg-primary-500 animate-pulse"
            style="width: 100%;"></div>

          <div @click="step.open = !step.open"
            class="flex items-center justify-between p-5 cursor-pointer select-none bg-white">
            <div class="flex items-center gap-4">
              <div
                :class="['w-10 h-10 rounded-xl flex items-center justify-center text-lg font-bold transition-all', step.status === 'running' ? 'bg-primary-100 text-primary-600 animate-pulse' : 'bg-surface-100 text-surface-500']">
                {{ step.status === 'done' ? '✓' : step.icon }}
              </div>
              <div>
                <h3 class="font-bold text-surface-800 text-sm">{{ step.title }}</h3>
                <p class="text-xs text-surface-500 font-medium mt-0.5">{{ step.desc }}</p>
              </div>
            </div>
            <span
              :class="['text-[10px] font-bold px-3 py-1 rounded-lg uppercase tracking-wider', step.status === 'running' ? 'bg-primary-100 text-primary-700' : 'bg-emerald-50 text-emerald-600']">
              {{ step.status }}
            </span>
          </div>

          <div v-show="step.open" class="p-5 border-t border-surface-100 bg-surface-50/30">

            <div v-if="step.id === 1" class="space-y-4">
              <div class="bg-white border border-surface-200 p-5 rounded-xl shadow-sm">

                <div class="text-[10px] font-bold text-surface-400 uppercase tracking-widest mb-4 text-center">Alur
                  Pengiriman Data ke Server</div>
                <div
                  class="flex flex-col md:flex-row items-center justify-center gap-3 text-xs font-bold text-center mb-6">
                  <div
                    class="px-4 py-2.5 bg-primary-50 border border-primary-100 text-primary-700 rounded-lg w-full md:w-auto shadow-sm">
                    Input Form Klien</div>
                  <div class="text-surface-300 hidden md:block">→</div>
                  <div
                    class="px-4 py-2.5 bg-amber-50 border border-amber-100 text-amber-700 rounded-lg w-full md:w-auto shadow-sm">
                    Pengecekan Validitas</div>
                  <div class="text-surface-300 hidden md:block">→</div>
                  <div
                    class="px-4 py-2.5 bg-emerald-50 border border-emerald-100 text-emerald-700 rounded-lg w-full md:w-auto shadow-sm">
                    Server Menerima Data</div>
                </div>

                <div class="border-t border-surface-100 pt-5">
                  <div class="text-[10px] font-bold text-surface-400 uppercase tracking-widest mb-3">Ringkasan Parameter
                    Terkirim</div>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">

                    <div class="bg-surface-50 p-4 rounded-xl border border-surface-100 flex flex-col gap-1.5">
                      <div class="flex items-center gap-2 text-[11px] font-bold text-surface-500 uppercase">
                        <div class="w-5 h-5 rounded bg-primary-100 text-primary-600 flex items-center justify-center">
                          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                          </svg></div>
                        Topik Utama (Judul)
                      </div>
                      <div class="text-sm font-bold text-surface-800">{{ judulInput }}</div>
                    </div>

                    <div class="bg-surface-50 p-4 rounded-xl border border-surface-100 flex flex-col gap-1.5">
                      <div class="flex items-center gap-2 text-[11px] font-bold text-surface-500 uppercase">
                        <div class="w-5 h-5 rounded bg-blue-100 text-blue-600 flex items-center justify-center"><svg
                            class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M4 6h16M4 12h16m-7 6h7"></path>
                          </svg></div>
                        Konteks (Abstrak)
                      </div>
                      <div class="text-xs font-medium text-surface-600 line-clamp-3 italic">"{{ abstrakInput }}"</div>
                    </div>

                    <div class="bg-surface-50 p-4 rounded-xl border border-surface-100 flex flex-col gap-1.5">
                      <div class="flex items-center gap-2 text-[11px] font-bold text-surface-500 uppercase">
                        <div class="w-5 h-5 rounded bg-emerald-100 text-emerald-600 flex items-center justify-center">
                          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7">
                            </path>
                          </svg>
                        </div>
                        Target Keluaran
                      </div>
                      <div class="text-sm font-bold text-surface-800">Menyaring Top <span class="text-emerald-600">{{
                        kRank }}</span> Kandidat Terbaik</div>
                    </div>

                    <div class="bg-surface-50 p-4 rounded-xl border border-surface-100 flex flex-col gap-1.5">
                      <div class="flex items-center gap-2 text-[11px] font-bold text-surface-500 uppercase">
                        <div class="w-5 h-5 rounded bg-fuchsia-100 text-fuchsia-600 flex items-center justify-center">
                          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4">
                            </path>
                          </svg>
                        </div>
                        Konfigurasi AI
                      </div>
                      <div class="text-sm font-bold text-surface-800 flex items-center gap-2">
                        <span class="text-blue-600">Leksikal: {{ bobotLexical }}%</span>
                        <span class="text-surface-300">|</span>
                        <span class="text-fuchsia-600">Semantik: {{ 100 - bobotLexical }}%</span>
                      </div>
                    </div>

                  </div>
                </div>

              </div>
            </div>

            <div v-if="step.id === 2" class="bg-white border border-surface-200 p-4 rounded-xl shadow-sm">
              <div class="text-[10px] font-bold text-surface-400 uppercase tracking-widest mb-3">Hasil Pemotongan Token
                (Front-end view)</div>
              <p class="text-xs text-surface-500 mb-3 font-medium">Teks diubah menjadi huruf kecil (lowercasing), tanda
                baca dihapus, dan kata hubung (stop-words) dibuang untuk meringankan beban komputasi AI.</p>
              <div class="flex flex-wrap gap-2 bg-surface-50 p-4 rounded-lg border border-surface-100">
                <span v-for="token in sampleTokens" :key="token"
                  class="bg-white text-surface-600 border border-surface-200 shadow-sm px-2.5 py-1.5 rounded-md text-xs font-semibold">
                  {{ token }}
                </span>
              </div>
            </div>

            <div v-if="step.id === 3" class="space-y-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="p-4 border border-blue-200 bg-blue-50/50 rounded-xl shadow-sm">
                  <div class="flex items-center gap-2 mb-2">
                    <span
                      class="w-6 h-6 rounded bg-blue-100 text-blue-600 flex items-center justify-center text-xs font-bold">1</span>
                    <div class="font-bold text-blue-800 text-sm">Lexical Engine (BM25)</div>
                  </div>
                  <p class="text-xs text-blue-700 font-medium leading-relaxed">Mengevaluasi kecocokan eksak kata per
                    kata. Semakin sering kata kunci unik muncul di dalam riwayat jurnal dosen, semakin tinggi skornya
                    (TF-IDF based).</p>
                </div>

                <div class="p-4 border border-fuchsia-200 bg-fuchsia-50/50 rounded-xl shadow-sm">
                  <div class="flex items-center gap-2 mb-2">
                    <span
                      class="w-6 h-6 rounded bg-fuchsia-100 text-fuchsia-600 flex items-center justify-center text-xs font-bold">2</span>
                    <div class="font-bold text-fuchsia-800 text-sm">Semantic Engine (SBERT)</div>
                  </div>
                  <p class="text-xs text-fuchsia-700 font-medium leading-relaxed">Mengubah keseluruhan kalimat menjadi
                    array matematika N-Dimensi, lalu menghitung jarak kedekatannya <span
                      class="font-mono text-[10px] bg-fuchsia-100 px-1 rounded">(Cosine Similarity)</span> agar AI paham
                    makna konteksnya.</p>
                </div>
              </div>

              <div v-if="step.status === 'done'"
                class="flex items-center gap-3 text-emerald-700 font-bold text-xs bg-emerald-50 p-3 rounded-xl border border-emerald-100 shadow-sm">
                <span
                  class="w-5 h-5 rounded-full bg-emerald-200 flex items-center justify-center text-emerald-800">✓</span>
                Vektor berhasil diekstraksi dan skor kemiripan telah selesai dihitung oleh Server.
              </div>
            </div>

            <div v-if="step.id === 4" class="space-y-4">
              <div class="bg-white border border-surface-700 p-5 rounded-xl text-center shadow-inner">
                <div class="text-primary-700 text-xs font-bold uppercase tracking-widest mb-2">Formula Penggabungan
                  Bobot
                </div>
                <div class="text-lg md:text-xl text-primary-400 font-mono font-bold tracking-wider">
                  Score = ({{ bobotLexical / 100 }} × <span class="text-blue-400">BM25</span>) + ({{ (100 -
                    bobotLexical) / 100 }} × <span class="text-fuchsia-400">SBERT</span>)
                </div>
              </div>

              <div v-if="hasilRekomendasi.length > 0"
                class="bg-white border border-surface-200 rounded-xl overflow-hidden shadow-sm">
                <table class="w-full text-left text-xs border-collapse">
                  <thead class="bg-surface-50 text-surface-500 font-bold uppercase tracking-wider">
                    <tr>
                      <th class="p-3 border-b border-surface-200">Nama Kandidat</th>
                      <th class="p-3 border-b border-surface-200 text-center text-blue-600">Lexical ({{ bobotLexical
                        }}%)
                      </th>
                      <th class="p-3 border-b border-surface-200 text-center text-fuchsia-600">Semantic ({{ 100 -
                        bobotLexical }}%)</th>
                      <th class="p-3 border-b border-surface-200 text-center text-primary-700">Hybrid</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-surface-100 font-mono">
                    <tr v-for="dosen in hasilRekomendasi.slice(0, 3)" :key="dosen.NAMA">
                      <td class="p-3 font-sans font-bold text-surface-700">{{ dosen.NAMA }}</td>
                      <td class="p-3 text-center text-surface-500">{{ dosen['Lexical Score'] }}</td>
                      <td class="p-3 text-center text-surface-500">{{ dosen['Semantic Score'] }}</td>
                      <td class="p-3 text-center font-bold text-primary-700 bg-primary-50/50">{{ dosen['Hybrid Score']
                        }}
                      </td>
                    </tr>
                  </tbody>
                </table>
                <div
                  class="p-2 text-center text-[10px] font-bold text-surface-400 bg-surface-50/80 uppercase tracking-widest border-t border-surface-100">
                  Pratinjau Kalkulasi (Menampilkan Top 3)
                </div>
              </div>
            </div>

            <div v-if="step.id === 5 && hasilRekomendasi.length > 0">
              <div class="bg-primary-50 border border-primary-100 p-5 rounded-xl mb-5 flex items-start gap-4 shadow-sm">
                <div>
                  <div class="text-xs font-bold text-primary-400 uppercase tracking-widest mb-1">Rekomendasi Utama (Rank
                    1)</div>
                  <div class="font-extrabold text-primary-900 text-lg">{{ hasilRekomendasi[0].NAMA }}</div>
                  <div class="text-sm text-primary-700 mt-1 font-medium">{{
                    formatArray(hasilRekomendasi[0].BIDANG_KEAHLIAN).join(', ') }}</div>
                </div>
              </div>

              <div class="border border-surface-200 rounded-xl overflow-hidden bg-white shadow-sm">
                <table class="w-full text-left border-collapse">
                  <thead
                    class="bg-surface-50 border-b border-surface-200 text-xs font-bold text-surface-500 uppercase tracking-wider">
                    <tr>
                      <th class="p-4 w-16 text-center">Rank</th>
                      <th class="p-4">Dosen Pembimbing</th>
                      <th class="p-4 text-center">Compability Score</th>
                      <th class="p-4 text-center">Aksi</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-surface-100 text-sm">
                    <tr v-for="(dosen, index) in hasilRekomendasi" :key="index"
                      class="hover:bg-surface-50 transition-colors">
                      <td class="p-4 text-center">
                        <span
                          class="bg-surface-100 text-surface-600 font-extrabold px-3 py-1.5 rounded-lg text-xs shadow-sm">{{
                            index + 1 }}</span>
                      </td>
                      <td class="p-4">
                        <div class="font-bold text-surface-800">{{ dosen.NAMA }}</div>
                        <div class="text-xs text-surface-500 mt-1 truncate max-w-50">{{ dosen.PROGRAM_STUDI }}</div>
                      </td>
                      <td class="p-4 text-center">
                        <span
                          class="text-primary-600 font-extrabold bg-primary-50 border border-primary-100 px-3 py-1 rounded-lg">{{
                            dosen['Hybrid Score'] }}</span>
                      </td>
                      <td class="p-4 text-center">
                        <button @click="bukaDetail(dosen)"
                          class="text-xs font-bold bg-white border border-surface-300 text-surface-600 hover:border-primary-500 hover:bg-primary-50 hover:text-primary-700 px-4 py-2 rounded-lg transition-all shadow-sm">
                          Riwayat
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

          </div>
        </div>
      </div>

    </div>
    <ModalDetail :isOpen="modalAktif" :dataDosen="dosenTerpilih" :tutupModal="tutupDetail" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api';
import ModalDetail from '../components/ModalDetail.vue';
import { daftarStopwords } from '../utils/stopwords.js';
import { showToast } from '../utils/toast.js';

const judulInput = ref('');
const abstrakInput = ref('');
const kRank = ref(10);
const bobotLexical = ref(40);
const isModelWarmingUp = ref(true);

const isProcessing = ref(false);
const isRefreshing = ref(false);
const hasStarted = ref(false);
const progressPct = ref(0);
const progressMsg = ref('Menunggu eksekusi...');
const sampleTokens = ref([]);
const hasilRekomendasi = ref([]);

const modalAktif = ref(false);
const dosenTerpilih = ref({});

const pipeline = ref([
  { id: 1, title: 'Validasi Parameter Input', icon: '1', desc: 'Struktur request gateway & payload guard', status: 'idle', open: false },
  { id: 2, title: 'Preprocessing Teks', icon: '2', desc: 'Case-folding, regex filter & stopwords array', status: 'idle', open: false },
  { id: 3, title: 'Inferensi Model AI', icon: '3', desc: 'Komputasi formula BM25 & SBERT Cosine Distance', status: 'idle', open: false },
  { id: 4, title: 'Kalkulasi Hybrid Dinamis', icon: '4', desc: 'Min-Max Normalization & linear blending', status: 'idle', open: false },
  { id: 5, title: 'Tabel Peringkat (K-Rank)', icon: '5', desc: 'Hasil pengurutan descending vector tertinggi', status: 'idle', open: false }
]);

const formatArray = (text) => {
  if (!text) return [];
  let str = String(text).replace(/^\[|\]$/g, '').trim();
  let arr = str.includes('", "') ? str.split('", "') : str.split(',');
  return arr.map(s => s.replace(/(^")|("$)/g, '').trim()).filter(x => x && x !== '-');
};

onMounted(async () => {
  try { await api.getSemuaDosen(); }
  catch (e) { showToast("Gagal memuat awalan Server", "error"); }
  finally { setTimeout(() => { isModelWarmingUp.value = false; }, 800); }
});

const handleRefresh = async () => {
  isRefreshing.value = true;
  try {
    const res = await api.refreshServer();
    showToast(res.pesan, 'success');
  } catch (error) {
    showToast(error.message, 'error');
  } finally {
    isRefreshing.value = false;
  }
};

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));
const ekstraksiToken = (teks) => teks.toLowerCase()
  .replace(/[^a-z0-9\s]/g, "")
  .split(/\s+/)
  .filter(t => t.length > 2 && !daftarStopwords.includes(t))
  .filter((v, i, a) => a.indexOf(v) === i)
  .slice(0, 15);

const jalankanPipeline = async () => {
  if (!judulInput.value || !abstrakInput.value) {
    showToast("Lengkapi Judul dan Abstrak terlebih dahulu!", "error");
    return;
  }

  isProcessing.value = true;
  hasStarted.value = true;
  hasilRekomendasi.value = [];
  pipeline.value.forEach(p => { p.status = 'idle'; p.open = false; });

  try {
    progressMsg.value = 'Membaca param input...'; progressPct.value = 10;
    pipeline.value[0].status = 'running'; pipeline.value[0].open = true; await sleep(600); pipeline.value[0].status = 'done'; pipeline.value[0].open = false;

    progressMsg.value = 'Tokenisasi teks...'; progressPct.value = 30;
    pipeline.value[1].status = 'running'; pipeline.value[1].open = true; sampleTokens.value = ekstraksiToken(judulInput.value + " " + abstrakInput.value); await sleep(800); pipeline.value[1].status = 'done'; pipeline.value[1].open = false;

    progressMsg.value = 'Komputasi Server AI...'; progressPct.value = 60;
    pipeline.value[2].status = 'running'; pipeline.value[2].open = true;

    const decLex = bobotLexical.value / 100;
    const decSem = (100 - bobotLexical.value) / 100;

    const respons = await api.getRekomendasi(judulInput.value, abstrakInput.value, kRank.value, decLex, decSem);
    hasilRekomendasi.value = respons.data;

    progressPct.value = 85; pipeline.value[2].status = 'done'; pipeline.value[2].open = false;

    progressMsg.value = 'Kalkulasi Hybrid Dinamis...'; progressPct.value = 95;
    pipeline.value[3].status = 'running'; pipeline.value[3].open = true; await sleep(1000); pipeline.value[3].status = 'done'; pipeline.value[3].open = false;

    progressMsg.value = 'Proses selesai.'; progressPct.value = 100;
    pipeline.value[4].status = 'running'; pipeline.value[4].open = true; await sleep(400); pipeline.value[4].status = 'done';

    showToast("Analisis rekomendasi berhasil!", "success");

  } catch (error) {
    progressMsg.value = 'Error Server.';
    const act = pipeline.value.find(p => p.status === 'running'); if (act) act.status = 'error';
    showToast(error.message, "error");
  } finally {
    isProcessing.value = false;
  }
};

const bukaDetail = (dosen) => { dosenTerpilih.value = dosen; modalAktif.value = true; };
const tutupDetail = () => { modalAktif.value = false; };
</script>