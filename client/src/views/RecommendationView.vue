<template>
  <div class="max-w-7xl mx-auto py-8">



    <!-- Header -->
    <div class="mb-8 flex flex-col md:flex-row md:justify-between md:items-end gap-4">
      <div>
        <h1 class="text-3xl font-extrabold text-surface-900 tracking-tight">
          <span class="text-primary-600">Recommendation</span> System
        </h1>
        <p class="text-surface-500 mt-1 font-medium">
          Hybrid NLP Recommendation System with
          <span class="text-blue-500 font-bold">BM25</span> &
          <span class="text-fuchsia-500 font-bold">SBERT</span> Model
        </p>
      </div>
      <button @click="handleRefresh" :disabled="isRefreshing"
        class="group flex items-center gap-2 bg-white hover:bg-amber-50 border border-surface-200 hover:border-amber-200 text-surface-600 hover:text-amber-700 px-4 py-2 rounded-xl text-sm font-bold shadow-sm transition-all active:scale-95">
        <svg :class="['w-4 h-4', isRefreshing ? 'animate-spin text-amber-600' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        {{ isRefreshing ? 'Menyinkronkan AI...' : 'Sinkronisasi Data AI' }}
      </button>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
      <!-- LEFT PANEL -->
      <div class="lg:col-span-4 space-y-6">
        <div class="bg-white border border-surface-200 rounded-2xl shadow-sm p-6 relative overflow-hidden">
          <div v-if="isProcessing" class="absolute inset-0 bg-linear-to-br from-primary-50 to-white/20 opacity-60 z-10"></div>

          <h2 class="text-sm font-bold text-surface-400 mb-5 uppercase tracking-widest relative z-20">Data Rencana Skripsi</h2>

          <div class="space-y-5 relative z-20">
            <!-- Judul -->
            <div>
              <label class="block text-sm font-bold text-surface-700 mb-1.5">Judul Proposal</label>
              <input v-model="judulInput" type="text" placeholder="Contoh: Sistem Rekomendasi NLP..."
                class="w-full p-3 bg-surface-50 border border-surface-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-all text-sm font-medium" />
            </div>

            <!-- Abstrak -->
            <div>
              <label class="block text-sm font-bold text-surface-700 mb-1.5">Abstrak Penelitian</label>
              <textarea v-model="abstrakInput" rows="5" placeholder="Latar belakang dan metode..."
                class="w-full p-3 bg-surface-50 border border-surface-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-all text-sm resize-none"></textarea>
            </div>

            <!-- Mode pembobotan -->
            <div class="bg-surface-50 border border-surface-100 p-4 rounded-xl">
              <div class="flex justify-between items-center mb-3">
                <label class="block text-sm font-bold text-surface-700">Mode Pembobotan AI</label>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="isAdaptifMode" class="sr-only peer" />
                  <div class="w-9 h-5 bg-surface-300 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-0.5 after:bg-white after:border-surface-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-primary-600"></div>
                </label>
              </div>

              <div v-if="isAdaptifMode" class="bg-primary-50 border border-primary-100 p-3 rounded-lg text-xs text-primary-700 font-medium leading-relaxed animate-fade-in">
                <span class="font-bold text-primary-800">✨ Adaptif Otomatis:</span> AI menganalisis kerumitan istilah pada judul untuk menentukan keseimbangan Leksikal &amp; Semantik secara dinamis.
              </div>

              <div v-else class="animate-fade-in">
                <div class="flex justify-between items-center mb-2">
                  <span class="text-[10px] font-mono font-bold bg-surface-200 text-surface-700 px-2 py-0.5 rounded">Manual</span>
                  <span class="text-[10px] font-mono font-bold bg-primary-100 text-primary-700 px-2 py-0.5 rounded">L:{{ bobotLexical }}% | S:{{ 100 - bobotLexical }}%</span>
                </div>
                <input type="range" v-model="bobotLexical" min="0" max="100" step="10" class="w-full h-1.5 bg-surface-200 rounded-lg appearance-none cursor-pointer accent-primary-600" />
                <div class="flex justify-between text-[10px] font-bold text-surface-400 uppercase mt-1.5">
                  <span>BM25 (Leksikal)</span><span>SBERT (Semantik)</span>
                </div>
              </div>
            </div>

            <!-- Top-K + Tombol -->
            <div class="flex gap-3">
              <div class="w-1/3">
                <label class="block text-sm font-bold text-surface-700 mb-1.5">Batas (Top-K)</label>
                <input v-model="kRank" type="number" min="1" max="20"
                  class="w-full p-3 bg-surface-50 border border-surface-200 rounded-xl text-center font-bold text-surface-700 outline-none focus:border-primary-400" />
              </div>
              <button @click="jalankanPipelineSSE" :disabled="isProcessing"
                class="w-2/3 bg-primary-600 hover:bg-primary-700 disabled:bg-surface-300 text-white font-bold rounded-xl transition-all active:scale-95 shadow-md shadow-primary-200 mt-6 relative overflow-hidden">
                <span v-if="isProcessing" class="absolute inset-0 w-full h-full bg-white/20 animate-pulse"></span>
                <span class="relative z-10 flex items-center justify-center gap-2 py-3">
                  <svg v-if="isProcessing" class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  {{ isProcessing ? 'Memproses API...' : 'Mulai Analisis AI' }}
                </span>
              </button>
            </div>
          </div>
        </div>

        <!-- Info card: arsitektur hybrid -->
        <div class="bg-white border border-surface-200 rounded-2xl shadow-sm p-5">
          <h3 class="text-xs font-bold text-surface-400 uppercase tracking-widest mb-4">Arsitektur Hybrid Retrieval</h3>
          <div class="space-y-3 text-xs">
            <div class="flex gap-3 items-start">
              <div class="w-7 h-7 rounded-lg bg-blue-100 flex items-center justify-center shrink-0 mt-0.5">
                <span class="text-blue-600 font-extrabold text-[10px]">BM25</span>
              </div>
              <div>
                <div class="font-bold text-surface-700">Pencocokan Leksikal (BM25)</div>
                <div class="text-surface-500 leading-relaxed mt-0.5">Algoritma probabilistik berbasis TF-IDF. Memberikan skor tinggi untuk kata yang jarang tetapi relevan. Efisien untuk menemukan kandidat awal dari korpus besar.</div>
              </div>
            </div>
            <div class="border-t border-surface-100 pt-3 flex gap-3 items-start">
              <div class="w-7 h-7 rounded-lg bg-fuchsia-100 flex items-center justify-center shrink-0 mt-0.5">
                <span class="text-fuchsia-600 font-extrabold text-[10px]">SB</span>
              </div>
              <div>
                <div class="font-bold text-surface-700">Pemeringkatan Semantik (SBERT)</div>
                <div class="text-surface-500 leading-relaxed mt-0.5">Sentence-BERT mengubah teks menjadi vektor 768 dimensi. Kesamaan dihitung dengan Cosine Similarity — menangkap makna tersirat yang tidak bisa ditemukan BM25.</div>
              </div>
            </div>
            <div class="border-t border-surface-100 pt-3 flex gap-3 items-start">
              <div class="w-7 h-7 rounded-lg bg-primary-100 flex items-center justify-center shrink-0 mt-0.5">
                <span class="text-primary-600 font-extrabold text-[10px]">⊕</span>
              </div>
              <div>
                <div class="font-bold text-surface-700">Skor Gabungan (Hybrid)</div>
                <div class="text-surface-500 leading-relaxed mt-0.5">Skor akhir = (α × BM25) + (β × SBERT). Bobot α dan β dapat ditetapkan manual atau dioptimalkan secara adaptif oleh model.</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- RIGHT PANEL: PIPELINE (Extracted to ProgressStepper) -->
      <ProgressStepper 
        class="lg:col-span-8 space-y-4"
        :hasStarted="hasStarted"
        :pipeline="pipeline"
        :judulInput="judulInput"
        :abstrakInput="abstrakInput"
        :kRank="kRank"
        :isAdaptifMode="isAdaptifMode"
        :bobotLexical="bobotLexical"
        :metadataMesin="metadataMesin"
        :hasilRekomendasi="hasilRekomendasi"
        @bukaDetail="bukaDetail"
      />
    </div>

    <XaiModal :isOpen="modalAktif" :dataDosen="dosenTerpilih" :tutupModal="tutupDetail" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api.js';
import { streamProgress } from '../services/stream.js';
import XaiModal from '../components/XaiModal.vue';
import ProgressStepper from '../components/ProgressStepper.vue';
import { showToast } from '../utils/toast.js';

const judulInput = ref('');
const abstrakInput = ref('');
const kRank = ref(5);
const bobotLexical = ref(30);



const isProcessing = ref(false);
const isRefreshing = ref(false);
const hasStarted = ref(false);

const hasilRekomendasi = ref([]);
const metadataMesin = ref({
  teks_asli: '',
  teks_ekspansi: '',
  kata_diekspansi: {},
  token_unigram: [],
  token_bigram: []
});

const isAdaptifMode = ref(true);
const modalAktif = ref(false);
const dosenTerpilih = ref({});

const pipeline = ref([
  { id: 1, title: 'Penerimaan & Validasi Data Masukan', icon: '1', desc: 'Menerima teks judul dan abstrak, validasi parameter API', status: 'idle', open: false },
  { id: 2, title: 'Prapemrosesan & Perluasan Kueri', icon: '2', desc: 'Case folding, stopword removal, ekspansi sinonim, tokenisasi N-gram', status: 'idle', open: false },
  { id: 3, title: 'Pencocokan Leksikal (BM25)', icon: '3', desc: 'Seleksi kandidat berdasarkan TF-IDF — mencocokkan kata kunci secara persis', status: 'idle', open: false },
  { id: 4, title: 'Pemeringkatan Semantik (SBERT)', icon: '4', desc: 'Cosine similarity vektor 768D — menangkap kemiripan makna & KeyBERT extraction', status: 'idle', open: false },
  { id: 5, title: 'Kalkulasi Hybrid & Peringkat Akhir', icon: '5', desc: 'Menggabungkan skor BM25 dan SBERT dengan bobot α dan β', status: 'idle', open: false }
]);



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

// ── Pipeline utama dengan SSE ──
const jalankanPipelineSSE = () => {
  if (!judulInput.value || !abstrakInput.value) {
    showToast('Lengkapi Judul dan Abstrak terlebih dahulu!', 'error');
    return;
  }

  isProcessing.value = true;
  hasStarted.value = true;
  hasilRekomendasi.value = [];
  metadataMesin.value = { teks_asli: '', teks_ekspansi: '', kata_diekspansi: {}, token_unigram: [], token_bigram: [] };
  pipeline.value.forEach(p => { p.status = 'idle'; p.open = false; });

  const decLex = isAdaptifMode.value ? -1 : bobotLexical.value / 100;
  const decSem = isAdaptifMode.value ? -1 : (100 - bobotLexical.value) / 100;

  pipeline.value[0].status = 'running'; pipeline.value[0].open = true;

  streamProgress(
    judulInput.value, 
    abstrakInput.value, 
    kRank.value, 
    decLex, 
    decSem,
    (data) => {
      // onMessage: handle progress updates
      const stepIndex = data.step - 1;
      if (stepIndex >= 0 && stepIndex < pipeline.value.length) {
        if (stepIndex > 0) {
           pipeline.value[stepIndex - 1].status = 'done';
           pipeline.value[stepIndex - 1].open = false;
        }
        pipeline.value[stepIndex].status = 'running';
        pipeline.value[stepIndex].open = true;
      }
      if (data.metadata_mesin) {
        metadataMesin.value = data.metadata_mesin;
      }
    },
    (error) => {
      // onError
      const act = pipeline.value.find(p => p.status === 'running');
      if (act) act.status = 'error';
      showToast('Gagal memproses rekomendasi.', 'error');
      isProcessing.value = false;
    },
    (data) => {
      // onComplete
      pipeline.value.forEach(p => { p.status = 'done'; p.open = false; });
      if (data.hasil_rekomendasi) {
         hasilRekomendasi.value = data.hasil_rekomendasi;
      }
      if (data.metadata_mesin) {
         metadataMesin.value = data.metadata_mesin;
      }
      pipeline.value[4].open = true; // Open the last step to show results
      showToast('Analisis rekomendasi berhasil diproses!', 'success');
      isProcessing.value = false;
    }
  );
};

const bukaDetail = (dosen) => { dosenTerpilih.value = dosen; modalAktif.value = true; };
const tutupDetail = () => { modalAktif.value = false; };
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
