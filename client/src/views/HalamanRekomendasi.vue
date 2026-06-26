<template>
  <div class="max-w-7xl mx-auto py-8">

    <div v-if="isModelWarmingUp" class="fixed inset-0 bg-white/90 backdrop-blur-md z-50 flex flex-col items-center justify-center transition-opacity duration-500">
      <div class="w-16 h-16 border-4 border-surface-200 border-t-primary-600 rounded-full animate-spin mb-4 shadow-sm"></div>
      <h2 class="text-2xl font-extrabold text-surface-800">Menghidupkan Mesin SIREDO...</h2>
      <div class="w-72 bg-surface-200 rounded-full h-2.5 mt-5 mb-2 overflow-hidden shadow-inner">
        <div class="bg-linear-to-r from-primary-500 to-primary-700 h-2.5 rounded-full transition-all duration-700 ease-out" :style="{ width: serverProgress + '%' }"></div>
      </div>
      <div class="flex items-center gap-2">
        <span class="text-primary-700 font-mono text-sm font-extrabold">{{ serverProgress }}%</span>
        <span class="text-surface-400 font-bold">|</span>
        <p class="text-surface-500 text-sm font-medium animate-pulse">{{ serverMessage }}</p>
      </div>
    </div>

    <div class="mb-8 flex flex-col md:flex-row md:justify-between md:items-end gap-4">
      <div>
        <h1 class="text-3xl font-extrabold text-surface-900 tracking-tight">
          <span class="text-primary-600">Recommendation</span> System
        </h1>
        <p class="text-surface-500 mt-1 font-medium">Hybird NLP Recommendation System with <span class="text-blue-500">BM25</span> & <span class="text-fuchsia-500">SBERT</span> Model</p>
      </div>
      <button @click="handleRefresh" :disabled="isRefreshing"
        class="group flex items-center gap-2 bg-white hover:bg-amber-50 border border-surface-200 hover:border-amber-200 text-surface-600 hover:text-amber-700 px-4 py-2 rounded-xl text-sm font-bold shadow-sm transition-all active:scale-95">
        <svg :class="['w-4 h-4', isRefreshing ? 'animate-spin text-amber-600' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
        {{ isRefreshing ? 'Menyinkronkan AI...' : 'Sinkronisasi Data AI' }}
      </button>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
      
      <div class="lg:col-span-4 space-y-6">
        <div class="bg-white border border-surface-200 rounded-2xl shadow-sm p-6 relative overflow-hidden">
          <div v-if="isProcessing" class="absolute inset-0 bg-linear-to-br from-primary-50 to-white/20 opacity-60 z-10"></div>
          
          <h2 class="text-sm font-bold text-surface-400 mb-5 uppercase tracking-widest relative z-20">Data Rencana Skripsi</h2>
          <div class="space-y-5 relative z-20">
            <div>
              <label class="block text-sm font-bold text-surface-700 mb-1.5">Judul Proposal</label>
              <input v-model="judulInput" type="text" placeholder="Contoh: Sistem Rekomendasi NLP..."
                class="w-full p-3 bg-surface-50 border border-surface-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-all text-sm font-medium">
            </div>
            <div>
              <label class="block text-sm font-bold text-surface-700 mb-1.5">Abstrak Penelitian</label>
              <textarea v-model="abstrakInput" rows="5" placeholder="Latar belakang dan metode..."
                class="w-full p-3 bg-surface-50 border border-surface-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-all text-sm resize-none"></textarea>
            </div>
            <div class="bg-surface-50 border border-surface-100 p-4 rounded-xl">
              <div class="flex justify-between items-center mb-3">
                <label class="block text-sm font-bold text-surface-700">Mode Pembobotan AI</label>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="isAdaptifMode" class="sr-only peer">
                  <div class="w-9 h-5 bg-surface-300 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-0.5 after:bg-white after:border-surface-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-primary-600"></div>
                </label>
              </div>

              <div v-if="isAdaptifMode" class="bg-primary-50 border border-primary-100 p-3 rounded-lg text-xs text-primary-700 font-medium leading-relaxed animate-fade-in">
                <span class="font-bold text-primary-800">✨ Adaptif Otomatis:</span> AI akan menganalisis kerumitan istilah pada judul Anda untuk menentukan keseimbangan Leksikal & Semantik yang paling optimal secara dinamis.
              </div>

              <div v-else class="animate-fade-in">
                <div class="flex justify-between items-center mb-2">
                  <span class="text-[10px] font-mono font-bold bg-surface-200 text-surface-700 px-2 py-0.5 rounded">Manual</span>
                  <span class="text-[10px] font-mono font-bold bg-primary-100 text-primary-700 px-2 py-0.5 rounded">L:{{ bobotLexical }}% | S:{{ 100 - bobotLexical }}%</span>
                </div>
                <input type="range" v-model="bobotLexical" min="0" max="100" step="10" class="w-full h-1.5 bg-surface-200 rounded-lg appearance-none cursor-pointer accent-primary-600">
                <div class="flex justify-between text-[10px] font-bold text-surface-400 uppercase mt-1.5">
                  <span>BM25</span><span>SBERT</span>
                </div>
              </div>
            </div>
            <div class="flex gap-3">
              <div class="w-1/3">
                <label class="block text-sm font-bold text-surface-700 mb-1.5">Batas (Top-K)</label>
                <input v-model="kRank" type="number" min="1" max="20"
                  class="w-full p-3 bg-surface-50 border border-surface-200 rounded-xl text-center font-bold text-surface-700 outline-none focus:border-primary-400">
              </div>
              <button @click="jalankanPipeline" :disabled="isProcessing"
                class="w-2/3 bg-primary-600 hover:bg-primary-700 disabled:bg-surface-300 text-white font-bold rounded-xl transition-all active:scale-95 shadow-md shadow-primary-200 mt-6 relative overflow-hidden">
                <span v-if="isProcessing" class="absolute inset-0 w-full h-full bg-white/20 animate-pulse"></span>
                <span class="relative z-10 flex items-center justify-center gap-2">
                  <svg v-if="isProcessing" class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                  {{ isProcessing ? 'Memproses API...' : 'Mulai Analisis AI' }}
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="lg:col-span-8 space-y-4">

        <div v-if="!hasStarted" class="h-full min-h-100 flex flex-col items-center justify-center border-2 border-dashed border-surface-200 rounded-2xl bg-surface-50/50 text-surface-400">
          <svg class="w-16 h-16 mb-4 text-surface-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
          <span class="font-bold text-surface-500">Panel Proses Analisis AI akan muncul di sini.</span>
        </div>

        <div v-for="step in pipeline" :key="step.id" v-show="hasStarted && step.status !== 'idle'"
          :class="['rounded-2xl border transition-all duration-500 overflow-hidden relative bg-white', step.status === 'running' ? 'border-primary-400 shadow-lg shadow-primary-100/50 scale-[1.01]' : 'border-surface-200 opacity-80 hover:opacity-100']">

          <div v-if="step.status === 'running'" class="absolute top-0 left-0 h-0.5 bg-primary-500 animate-pulse" style="width: 100%;"></div>

          <div @click="step.open = !step.open" class="flex items-center justify-between p-5 cursor-pointer select-none">
            <div class="flex items-center gap-4">
              <div :class="['w-10 h-10 rounded-xl flex items-center justify-center text-lg font-bold transition-all', step.status === 'running' ? 'bg-primary-100 text-primary-600 animate-pulse' : (step.status === 'done' ? 'bg-emerald-100 text-emerald-600' : 'bg-surface-100 text-surface-500')]">
                {{ step.status === 'done' ? '✓' : step.icon }}
              </div>
              <div>
                <h3 class="font-bold text-surface-800 text-sm">{{ step.title }}</h3>
                <p class="text-xs text-surface-500 font-medium mt-0.5">{{ step.desc }}</p>
              </div>
            </div>
            <span :class="['text-[10px] font-bold px-3 py-1 rounded-lg uppercase tracking-wider', step.status === 'running' ? 'bg-primary-100 text-primary-700' : 'bg-surface-100 text-surface-600']">
              {{ step.status === 'done' ? 'Selesai' : 'Proses' }}
            </span>
          </div>

          <div v-show="step.open" class="p-5 border-t border-surface-100 bg-surface-50/30">

            <div v-if="step.id === 1" class="space-y-3 animate-fade-in">
              <div class="text-[10px] font-bold text-surface-400 uppercase tracking-widest">Teks Mentah (Dikirim ke Peladen)</div>
              <div class="p-4 bg-surface-50 border border-surface-200 rounded-lg text-xs font-mono text-surface-600 leading-relaxed italic border-l-4 border-l-surface-400">
                "{{ judulInput }} {{ abstrakInput }}"
              </div>
            </div>

            <div v-if="step.id === 2" class="grid grid-cols-1 md:grid-cols-2 gap-4 animate-fade-in">
              <div class="bg-white border border-surface-200 p-4 rounded-xl shadow-sm">
                <div class="text-[10px] font-bold text-amber-500 uppercase tracking-widest mb-3 flex items-center gap-2"><span class="text-base">📚</span> Perluasan Sinonim (Ekspansi)</div>
                
                <div v-if="Object.keys(metadataMesin.kata_diekspansi).length === 0" class="text-xs text-surface-400 font-medium py-2">
                  Sistem tidak menemukan singkatan terkait kamus.
                </div>
                <div v-else class="space-y-2 font-mono text-xs">
                  <div v-for="(hasil, asli) in metadataMesin.kata_diekspansi" :key="asli" class="flex items-center gap-2 bg-amber-50/50 p-2 rounded border border-amber-100 text-amber-800">
                    <span class="font-bold">{{ asli }}</span> <span class="text-amber-400">➔</span> <span>{{ hasil }}</span>
                  </div>
                </div>
              </div>

              <div class="bg-white border border-surface-200 p-4 rounded-xl shadow-sm">
                <div class="text-[10px] font-bold text-emerald-500 uppercase tracking-widest mb-3 flex items-center gap-2"><span class="text-base">✂️</span> Pemotongan Kata (Tokenisasi)</div>
                <div class="flex flex-wrap gap-1.5 h-19 overflow-y-auto content-start">
                  <span v-for="token in metadataMesin.token_unigram" :key="'u'+token" class="bg-emerald-50 text-emerald-700 border border-emerald-100 px-2 py-0.5 rounded text-[10px] font-mono font-bold">
                    {{ token }}
                  </span>
                  <span v-for="bg in metadataMesin.token_bigram" :key="'b'+bg" class="bg-teal-50 text-teal-700 border border-teal-100 px-2 py-0.5 rounded text-[10px] font-mono font-bold">
                    {{ bg }}
                  </span>
                </div>
              </div>
            </div>

            <div v-if="step.id === 3" class="space-y-4 animate-fade-in">
              <div v-if="hasilRekomendasi.length > 0" class="bg-white border border-blue-200 p-5 rounded-xl shadow-sm">
                <div class="flex justify-between items-end border-b border-blue-100 pb-3 mb-4">
                  <div>
                    <div class="text-[10px] font-bold text-blue-500 uppercase tracking-widest mb-1">Pencocokan Dokumen (BM25 Match)</div>
                    <div class="font-bold text-blue-900 text-sm">Kandidat: {{ hasilRekomendasi[0].NAMA }}</div>
                  </div>
                  <div class="text-right">
                    <div class="text-[10px] font-bold text-blue-400 uppercase tracking-widest">Kecocokan Kata</div>
                    <div class="text-xl font-extrabold text-blue-600">{{ Math.round(hasilRekomendasi[0]['Lexical Score'] * 100) }}%</div>
                  </div>
                </div>
                
                <div class="flex flex-wrap gap-1.5 h-24 overflow-y-auto content-start p-2">
                  <span v-for="token in metadataMesin.token_unigram" :key="'match_'+token"
                    :class="[
                      'px-2.5 py-1.5 rounded-md text-xs font-mono font-bold transition-all duration-500 flex items-center gap-1.5',
                      cekLexical(token, hasilRekomendasi[0])
                        ? 'bg-blue-500 text-white shadow-md shadow-blue-200 border border-blue-600 scale-105'
                        : 'bg-white text-surface-400 border border-surface-200 line-through opacity-50'
                    ]">
                    <span v-if="cekLexical(token, hasilRekomendasi[0])" class="text-[9px]">✓</span>
                    {{ token }}
                  </span>
                </div>
                <div class="mt-4 p-3 bg-blue-50 rounded-lg text-xs text-blue-700 font-medium border border-blue-100">
                  <span class="font-bold uppercase tracking-widest text-[10px]">Logika TF-IDF:</span> Kata yang lebih spesifik/jarang muncul mendapat bobot yang lebih tinggi.
                </div>
              </div>
            </div>

            <div v-if="step.id === 4" class="space-y-4 animate-fade-in">
              <div v-if="hasilRekomendasi.length > 0" class="bg-white border border-fuchsia-200 p-5 rounded-xl shadow-sm">
                <div class="flex justify-between items-end border-b border-fuchsia-100 pb-3 mb-4">
                  <div>
                    <div class="text-[10px] font-bold text-fuchsia-500 uppercase tracking-widest mb-1">Proyeksi Kedekatan Vektor Makna</div>
                    <div class="font-bold text-fuchsia-900 text-sm">Kandidat: {{ hasilRekomendasi[0].NAMA }}</div>
                  </div>
                  <div class="text-right">
                    <div class="text-[10px] font-bold text-fuchsia-400 uppercase tracking-widest">Kemiripan Makna</div>
                    <div class="text-xl font-extrabold text-fuchsia-600">{{ Math.round(hasilRekomendasi[0]['Semantic Score'] * 100) }}%</div>
                  </div>
                </div>

                <div class="space-y-4">
                  <div>
                    <div class="flex justify-between text-[10px] font-bold text-surface-500 uppercase mb-1">
                      <span>Jarak Vektor N-Dimensi</span>
                      <span>Target Kedekatan</span>
                    </div>
                    <div class="w-full bg-surface-100 rounded-full h-2.5 overflow-hidden flex">
                      <div class="bg-linear-to-r from-fuchsia-400 to-fuchsia-600 h-2.5 rounded-full relative" :style="`width: ${Math.round(hasilRekomendasi[0]['Semantic Score'] * 100)}%`">
                        <span class="absolute right-0 top-0 bottom-0 w-1 bg-white/50 animate-ping"></span>
                      </div>
                    </div>
                  </div>

                  <div>
                    <div class="text-[10px] font-bold text-fuchsia-500 uppercase tracking-widest mb-2">Ekstraksi Topik Kandidat (KeyBERT)</div>
                    <div class="flex flex-wrap gap-2">
                      <div v-if="parseSemantik(hasilRekomendasi[0]).length === 0" class="text-xs text-surface-400 font-medium">Tidak ada frasa dominan.</div>
                      <span v-for="(frasa, idx) in parseSemantik(hasilRekomendasi[0])" :key="idx"
                        class="bg-fuchsia-50 text-fuchsia-700 border border-fuchsia-200 px-3 py-1.5 rounded-lg text-xs font-mono font-bold shadow-sm flex items-center gap-1.5">
                        <span class="w-1.5 h-1.5 rounded-full bg-fuchsia-500"></span> {{ frasa }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="step.id === 5" class="space-y-6 animate-fade-in">
              <div v-if="hasilRekomendasi.length > 0" class="grid grid-cols-1 md:grid-cols-12 gap-4">
                
                <div class="md:col-span-4 bg-surface-50 border border-surface-200 rounded-xl p-4 flex flex-col items-center justify-center space-y-2">
                  <div class="text-[10px] font-bold text-surface-400 uppercase tracking-widest mb-1">Penyaringan Kandidat</div>
                  <div class="bg-surface-200 text-surface-600 font-bold text-xs px-6 py-1 rounded w-[90%] text-center">Pangkalan Data</div>
                  <div class="text-surface-300 text-xs">▼</div>
                  <div class="bg-blue-100 text-blue-700 font-bold text-xs px-6 py-1 rounded w-[70%] text-center">Pencarian BM25</div>
                  <div class="text-surface-300 text-xs">▼</div>
                  <div class="bg-fuchsia-100 text-fuchsia-700 font-bold text-xs px-6 py-1 rounded w-[50%] text-center">Pemeringkatan SBERT</div>
                  <div class="text-surface-300 text-xs">▼</div>
                  <div class="bg-primary-500 text-white font-bold text-xs px-6 py-1.5 rounded w-[40%] text-center shadow-md">Hasil Top {{ kRank }}</div>
                </div>

                <div class="md:col-span-8 bg-white border border-surface-200 rounded-xl p-4 flex flex-col justify-center">
                  <div class="text-[10px] font-bold text-surface-400 uppercase tracking-widest mb-3 text-center">Perhitungan Matriks Kemiripan (Peringkat 1)</div>
                  
                  <div class="flex items-center justify-center gap-2 text-xs md:text-sm font-mono bg-surface-50 p-3 rounded-lg border border-surface-100">
                    <div class="text-center">
                      <div class="text-surface-400 text-[10px]">Bobot Kata</div>
                      <div class="text-blue-600 font-bold">0.{{ bobotLexical }}</div>
                    </div>
                    <span class="text-surface-400">×</span>
                    <div class="text-center">
                      <div class="text-surface-400 text-[10px]">Skor Leksikal</div>
                      <div class="text-blue-600 font-bold">{{ hasilRekomendasi[0]['Lexical Score'] }}</div>
                    </div>
                    <span class="text-surface-400 font-bold text-lg mx-1">+</span>
                    <div class="text-center">
                      <div class="text-surface-400 text-[10px]">Bobot Makna</div>
                      <div class="text-fuchsia-600 font-bold">0.{{ 100 - bobotLexical }}</div>
                    </div>
                    <span class="text-surface-400">×</span>
                    <div class="text-center">
                      <div class="text-surface-400 text-[10px]">Skor Semantik</div>
                      <div class="text-fuchsia-600 font-bold">{{ hasilRekomendasi[0]['Semantic Score'] }}</div>
                    </div>
                    <span class="text-surface-400 font-bold text-lg mx-1">=</span>
                    <div class="text-center bg-primary-100 px-3 py-1 rounded border border-primary-200">
                      <div class="text-primary-500 text-[10px] uppercase">Gabungan</div>
                      <div class="text-primary-700 font-extrabold text-base">{{ hasilRekomendasi[0]['Hybrid Score'] }}</div>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="hasilRekomendasi.length > 0" class="border border-surface-200 rounded-xl overflow-hidden bg-white shadow-sm">
                <table class="w-full text-left border-collapse">
                  <thead class="bg-surface-50 border-b border-surface-200 text-xs font-bold text-surface-500 uppercase tracking-wider font-mono">
                    <tr>
                      <th class="p-3 text-center">Peringkat</th>
                      <th class="p-3">Kandidat Dosen</th>
                      <th class="p-3 text-center text-blue-600">Kata (BM25)</th>
                      <th class="p-3 text-center text-fuchsia-600">Makna (SBERT)</th>
                      <th class="p-3 text-center text-primary-600">Skor Akhir</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-surface-100 text-sm">
                    <tr v-for="(dosen, index) in hasilRekomendasi" :key="index" class="hover:bg-surface-50 transition-colors font-mono">
                      <td class="p-3 text-center text-surface-400 font-bold">{{ index + 1 }}</td>
                      <td class="p-3">
                        <div class="font-bold text-surface-800 font-sans">{{ dosen.NAMA }}</div>
                        <div class="text-[10px] text-surface-500 mt-0.5 truncate max-w-50">{{ dosen.PROGRAM_STUDI }}</div>
                      </td>
                      <td class="p-3 text-center text-blue-600 font-bold bg-blue-50/30">{{ dosen['Lexical Score'] }}</td>
                      <td class="p-3 text-center text-fuchsia-600 font-bold bg-fuchsia-50/30">{{ dosen['Semantic Score'] }}</td>
                      <td class="p-3 text-center text-primary-700 font-extrabold bg-primary-50">{{ dosen['Hybrid Score'] }}</td>
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
import { showToast } from '../utils/toast.js';

const judulInput = ref('');
const abstrakInput = ref('');
const kRank = ref(5);
const bobotLexical = ref(30);

const isModelWarmingUp = ref(true);
const serverProgress = ref(0);
const serverMessage = ref('Menghubungkan ke peladen...');

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
  { id: 1, title: 'Penerimaan Data Masukan', icon: '1', desc: 'Menerima teks judul dan abstrak skripsi dari pengguna', status: 'idle', open: false },
  { id: 2, title: 'Prapemrosesan & Perluasan Kueri', icon: '2', desc: 'Penyamaan sinonim (Ekspansi) dan pemotongan kata (Tokenisasi)', status: 'idle', open: false },
  { id: 3, title: 'Pencocokan Kata (Leksikal BM25)', icon: '3', desc: 'Mengukur kecocokan kata kunci secara persis (TF-IDF)', status: 'idle', open: false },
  { id: 4, title: 'Pencocokan Makna (Semantik SBERT)', icon: '4', desc: 'Menganalisis kedekatan topik dan mengekstrak frasa (KeyBERT)', status: 'idle', open: false },
  { id: 5, title: 'Kalkulasi Gabungan & Peringkat Akhir', icon: '5', desc: 'Menghitung skor akhir dan menyusun peringkat kandidat', status: 'idle', open: false }
]);

const formatArray = (text) => {
  if (!text) return [];
  let str = String(text).replace(/^\[|\]$/g, '').trim();
  let arr = str.includes('", "') ? str.split('", "') : str.split(',');
  return arr.map(s => s.replace(/(^")|("$)/g, '').trim()).filter(x => x && x !== '-');
};

const cekLexical = (token, dosen) => {
  if (!dosen || !dosen['Irisan Kata (Lexical)'] || dosen['Irisan Kata (Lexical)'] === '-') return false;
  const irisan = dosen['Irisan Kata (Lexical)'].split(', ');
  return irisan.includes(token);
};

const parseSemantik = (dosen) => {
  if (!dosen || !dosen['Frasa Terkait (KeyBERT)'] || dosen['Frasa Terkait (KeyBERT)'] === '-') return [];
  return dosen['Frasa Terkait (KeyBERT)'].split(', ');
};

onMounted(() => {
  if (isModelWarmingUp.value) {
    pantauStatusServer();
  }
});

const pantauStatusServer = () => {
  const interval = setInterval(async () => {
    try {
      const res = await api.cekStatusServer();
      serverProgress.value = res.progress;
      serverMessage.value = res.pesan;

      if (res.ready) {
        clearInterval(interval);
        setTimeout(() => { isModelWarmingUp.value = false; }, 800);
      }
    } catch (e) {
      serverMessage.value = "Peladen Python belum menyala...";
    }
  }, 1500); 
};

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

const jalankanPipeline = async () => {
  if (!judulInput.value || !abstrakInput.value) {
    showToast("Lengkapi Judul dan Abstrak terlebih dahulu!", "error");
    return;
  }

  isProcessing.value = true;
  hasStarted.value = true;
  hasilRekomendasi.value = [];
  
  // Reset state
  metadataMesin.value = {
    teks_asli: '',
    teks_ekspansi: '',
    kata_diekspansi: {},
    token_unigram: [],
    token_bigram: []
  };

  pipeline.value.forEach(p => { p.status = 'idle'; p.open = false; });

  try {
    pipeline.value[0].status = 'running'; pipeline.value[0].open = true; 
    
    const decLex = isAdaptifMode.value ? -1 : bobotLexical.value / 100;
    const decSem = isAdaptifMode.value ? -1 : (100 - bobotLexical.value) / 100;
    
    const respons = await api.getRekomendasi(judulInput.value, abstrakInput.value, kRank.value, decLex, decSem);
    
    hasilRekomendasi.value = respons.data.hasil_rekomendasi;
    metadataMesin.value = respons.data.metadata_mesin;

    await sleep(800); 
    pipeline.value[0].status = 'done'; pipeline.value[0].open = false;

    pipeline.value[1].status = 'running'; pipeline.value[1].open = true; 
    await sleep(1500); 
    pipeline.value[1].status = 'done'; pipeline.value[1].open = false;

    pipeline.value[2].status = 'running'; pipeline.value[2].open = true;
    await sleep(1500);
    pipeline.value[2].status = 'done'; pipeline.value[2].open = false;

    pipeline.value[3].status = 'running'; pipeline.value[3].open = true; 
    await sleep(1500); 
    pipeline.value[3].status = 'done'; pipeline.value[3].open = false;

    pipeline.value[4].status = 'running'; pipeline.value[4].open = true; 
    await sleep(800); 
    pipeline.value[4].status = 'done';

    showToast("Analisis rekomendasi berhasil diproses!", "success");

  } catch (error) {
    const act = pipeline.value.find(p => p.status === 'running'); if (act) act.status = 'error';
    showToast("Gagal mengambil data dari peladen.", "error");
  } finally {
    isProcessing.value = false;
  }
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
  to { opacity: 1; transform: translateY(0); }
}
</style>
