<template>
  <div>
    <!-- Empty state -->
    <div v-if="!hasStarted" class="h-full min-h-96 flex flex-col items-center justify-center border-2 border-dashed border-surface-200 rounded-2xl bg-surface-50/50 text-surface-400">
      <svg class="w-16 h-16 mb-4 text-surface-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
      </svg>
      <span class="font-bold text-surface-500">Panel proses analisis AI akan muncul di sini.</span>
      <span class="text-sm text-surface-400 mt-1">Isi judul &amp; abstrak lalu klik <strong>Mulai Analisis AI</strong></span>
    </div>

    <!-- ───────────── STEP 1: Input ───────────── -->
    <div v-show="hasStarted && pipeline[0].status !== 'idle'" :class="stepClass(pipeline[0])">
      <div v-if="pipeline[0].status === 'running'" class="absolute top-0 left-0 h-0.5 bg-primary-500 animate-pulse w-full"></div>
      <div @click="pipeline[0].open = !pipeline[0].open" class="flex items-center justify-between p-5 cursor-pointer select-none">
        <div class="flex items-center gap-4">
          <div :class="stepIconClass(pipeline[0])">{{ pipeline[0].status === 'done' ? '✓' : pipeline[0].icon }}</div>
          <div>
            <h3 class="font-bold text-surface-800 text-sm">{{ pipeline[0].title }}</h3>
            <p class="text-xs text-surface-500 font-medium mt-0.5">{{ pipeline[0].desc }}</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <span :class="stepBadgeClass(pipeline[0])">{{ pipeline[0].status === 'done' ? 'Selesai' : 'Proses' }}</span>
          <svg :class="['w-4 h-4 text-surface-400 transition-transform', pipeline[0].open ? 'rotate-180' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
        </div>
      </div>

      <div v-show="pipeline[0].open" class="px-5 pb-5 border-t border-surface-100 bg-surface-50/30 animate-fade-in space-y-4 pt-4">
        <!-- Teks yang dikirim -->
        <div>
          <div class="text-[10px] font-bold text-surface-400 uppercase tracking-widest mb-2">Teks Mentah yang Dikirim ke Server</div>
          <div class="p-4 bg-white border border-surface-200 rounded-xl text-xs font-mono text-surface-600 leading-relaxed border-l-4 border-l-primary-400">
            "{{ judulInput }} {{ abstrakInput }}"
          </div>
        </div>

        <!-- Statistik input -->
        <div class="grid grid-cols-3 gap-3">
          <div class="bg-white border border-surface-200 rounded-xl p-3 text-center">
            <div class="text-2xl font-extrabold text-primary-600">{{ judulInput.split(' ').filter(w => w).length }}</div>
            <div class="text-[10px] font-bold text-surface-400 uppercase tracking-wider mt-1">Kata Judul</div>
          </div>
          <div class="bg-white border border-surface-200 rounded-xl p-3 text-center">
            <div class="text-2xl font-extrabold text-primary-600">{{ abstrakInput.split(' ').filter(w => w).length }}</div>
            <div class="text-[10px] font-bold text-surface-400 uppercase tracking-wider mt-1">Kata Abstrak</div>
          </div>
          <div class="bg-white border border-surface-200 rounded-xl p-3 text-center">
            <div class="text-2xl font-extrabold text-primary-600">{{ kRank }}</div>
            <div class="text-[10px] font-bold text-surface-400 uppercase tracking-wider mt-1">Top-K Target</div>
          </div>
        </div>

        <!-- Mode yang digunakan -->
        <div class="bg-primary-50 border border-primary-100 rounded-xl p-4">
          <div class="text-[10px] font-bold text-primary-500 uppercase tracking-widest mb-2">Parameter yang Dikirim ke API</div>
          <div class="grid grid-cols-2 gap-2 font-mono text-xs">
            <div class="bg-white rounded-lg px-3 py-2 border border-primary-100">
              <span class="text-surface-400">mode_bobot:</span>
              <span class="text-primary-700 font-bold ml-1">{{ isAdaptifMode ? 'adaptif (-1)' : 'manual' }}</span>
            </div>
            <div class="bg-white rounded-lg px-3 py-2 border border-primary-100">
              <span class="text-surface-400">top_k:</span>
              <span class="text-primary-700 font-bold ml-1">{{ kRank }}</span>
            </div>
            <div class="bg-white rounded-lg px-3 py-2 border border-primary-100">
              <span class="text-surface-400">α_lexical:</span>
              <span class="text-blue-600 font-bold ml-1">{{ isAdaptifMode ? 'auto' : (bobotLexical / 100).toFixed(2) }}</span>
            </div>
            <div class="bg-white rounded-lg px-3 py-2 border border-primary-100">
              <span class="text-surface-400">β_semantic:</span>
              <span class="text-fuchsia-600 font-bold ml-1">{{ isAdaptifMode ? 'auto' : ((100 - bobotLexical) / 100).toFixed(2) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ───────────── STEP 2: Preprocessing ───────────── -->
    <div v-show="hasStarted && pipeline[1].status !== 'idle'" :class="stepClass(pipeline[1])">
      <div v-if="pipeline[1].status === 'running'" class="absolute top-0 left-0 h-0.5 bg-primary-500 animate-pulse w-full"></div>
      <div @click="pipeline[1].open = !pipeline[1].open" class="flex items-center justify-between p-5 cursor-pointer select-none">
        <div class="flex items-center gap-4">
          <div :class="stepIconClass(pipeline[1])">{{ pipeline[1].status === 'done' ? '✓' : pipeline[1].icon }}</div>
          <div>
            <h3 class="font-bold text-surface-800 text-sm">{{ pipeline[1].title }}</h3>
            <p class="text-xs text-surface-500 font-medium mt-0.5">{{ pipeline[1].desc }}</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <span :class="stepBadgeClass(pipeline[1])">{{ pipeline[1].status === 'done' ? 'Selesai' : 'Proses' }}</span>
          <svg :class="['w-4 h-4 text-surface-400 transition-transform', pipeline[1].open ? 'rotate-180' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
        </div>
      </div>

      <div v-show="pipeline[1].open" class="px-5 pb-5 border-t border-surface-100 bg-surface-50/30 animate-fade-in space-y-4 pt-4">
        <!-- Tahapan preprocessing -->
        <div>
          <div class="text-[10px] font-bold text-surface-400 uppercase tracking-widest mb-3">Alur Prapemrosesan Teks</div>
          <div class="flex items-center gap-2 overflow-x-auto pb-2">
            <div v-for="(step, i) in [
              { label: 'Teks Asli', color: 'bg-surface-100 text-surface-600 border-surface-200' },
              { label: 'Case Folding', color: 'bg-amber-50 text-amber-700 border-amber-200' },
              { label: 'Stopword Removal', color: 'bg-orange-50 text-orange-700 border-orange-200' },
              { label: 'Ekspansi Sinonim', color: 'bg-yellow-50 text-yellow-700 border-yellow-200' },
              { label: 'Tokenisasi', color: 'bg-emerald-50 text-emerald-700 border-emerald-200' },
              { label: 'N-gram', color: 'bg-teal-50 text-teal-700 border-teal-200' },
            ]" :key="i" class="flex items-center gap-2 shrink-0">
              <div :class="['px-3 py-1.5 rounded-lg border text-[10px] font-bold whitespace-nowrap', step.color]">{{ step.label }}</div>
              <span v-if="i < 5" class="text-surface-300 font-bold">→</span>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Ekspansi sinonim -->
          <div class="bg-white border border-surface-200 p-4 rounded-xl shadow-sm">
            <div class="text-[10px] font-bold text-amber-500 uppercase tracking-widest mb-3 flex items-center gap-2">
              <span class="text-base">📚</span> Perluasan Sinonim (Query Expansion)
            </div>
            <div class="text-[10px] text-surface-400 mb-3 leading-relaxed">
              Singkatan / istilah teknis diubah ke bentuk lengkap agar BM25 dapat mencocokkan lebih banyak dokumen relevan.
            </div>
            <div v-if="Object.keys(metadataMesin.kata_diekspansi || {}).length === 0" class="text-xs text-surface-400 font-medium py-2 italic">
              Sistem tidak menemukan singkatan yang perlu diekspansi.
            </div>
            <div v-else class="space-y-2 font-mono text-xs">
              <div v-for="(hasil, asli) in metadataMesin.kata_diekspansi" :key="asli"
                class="flex items-center gap-2 bg-amber-50 p-2 rounded border border-amber-100 text-amber-800">
                <span class="font-bold bg-amber-200 px-1.5 py-0.5 rounded">{{ asli }}</span>
                <span class="text-amber-400 font-bold">➔</span>
                <span>{{ hasil }}</span>
              </div>
            </div>
          </div>

          <!-- Tokenisasi -->
          <div class="bg-white border border-surface-200 p-4 rounded-xl shadow-sm">
            <div class="text-[10px] font-bold text-emerald-500 uppercase tracking-widest mb-3 flex items-center gap-2">
              <span class="text-base">✂️</span> Hasil Tokenisasi
            </div>
            <div class="text-[10px] text-surface-400 mb-3 leading-relaxed">
              Teks dipecah menjadi <strong class="text-emerald-600">unigram</strong> (kata tunggal) dan <strong class="text-teal-600">bigram</strong> (dua kata berurutan) untuk meningkatkan akurasi pencocokan frasa.
            </div>
            <div class="flex flex-wrap gap-1.5 max-h-28 overflow-y-auto content-start">
              <span v-for="token in metadataMesin.token_unigram" :key="'u'+token"
                class="bg-emerald-50 text-emerald-700 border border-emerald-100 px-2 py-0.5 rounded text-[10px] font-mono font-bold">
                {{ token }}
              </span>
              <span v-for="bg in metadataMesin.token_bigram" :key="'b'+bg"
                class="bg-teal-50 text-teal-700 border border-teal-100 px-2 py-0.5 rounded text-[10px] font-mono font-bold">
                {{ bg }}
              </span>
            </div>
            <div class="flex gap-3 mt-3 pt-3 border-t border-surface-100">
              <div class="text-[10px] text-surface-400">
                <span class="inline-block w-2 h-2 rounded bg-emerald-200 mr-1 align-middle"></span>
                Unigram: <strong class="text-emerald-700">{{ (metadataMesin.token_unigram || []).length }}</strong>
              </div>
              <div class="text-[10px] text-surface-400">
                <span class="inline-block w-2 h-2 rounded bg-teal-200 mr-1 align-middle"></span>
                Bigram: <strong class="text-teal-700">{{ (metadataMesin.token_bigram || []).length }}</strong>
              </div>
            </div>
          </div>
        </div>

        <!-- Teks ekspansi vs asli -->
        <div v-if="metadataMesin.teks_ekspansi && metadataMesin.teks_ekspansi !== metadataMesin.teks_asli" class="bg-surface-50 border border-surface-100 rounded-xl p-4">
          <div class="text-[10px] font-bold text-surface-400 uppercase tracking-widest mb-3">Perbandingan Teks Sebelum & Sesudah Ekspansi</div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs font-mono">
            <div>
              <div class="text-[10px] text-surface-400 mb-1 font-bold">SEBELUM:</div>
              <div class="bg-white border border-surface-200 p-3 rounded-lg text-surface-500 leading-relaxed italic">{{ metadataMesin.teks_asli }}</div>
            </div>
            <div>
              <div class="text-[10px] text-emerald-500 mb-1 font-bold">SESUDAH:</div>
              <div class="bg-white border border-emerald-200 p-3 rounded-lg text-surface-700 leading-relaxed">{{ metadataMesin.teks_ekspansi }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ───────────── STEP 3: BM25 ───────────── -->
    <div v-show="hasStarted && pipeline[2].status !== 'idle'" :class="stepClass(pipeline[2])">
      <div v-if="pipeline[2].status === 'running'" class="absolute top-0 left-0 h-0.5 bg-blue-500 animate-pulse w-full"></div>
      <div @click="pipeline[2].open = !pipeline[2].open" class="flex items-center justify-between p-5 cursor-pointer select-none">
        <div class="flex items-center gap-4">
          <div :class="[stepIconClass(pipeline[2]), pipeline[2].status !== 'done' ? 'bg-blue-100! text-blue-600!' : '']">
            {{ pipeline[2].status === 'done' ? '✓' : pipeline[2].icon }}
          </div>
          <div>
            <h3 class="font-bold text-surface-800 text-sm">{{ pipeline[2].title }}</h3>
            <p class="text-xs text-surface-500 font-medium mt-0.5">{{ pipeline[2].desc }}</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <span :class="[stepBadgeClass(pipeline[2]), pipeline[2].status !== 'done' ? 'bg-blue-100! text-blue-700!' : '']">
            {{ pipeline[2].status === 'done' ? 'Selesai' : 'Proses' }}
          </span>
          <svg :class="['w-4 h-4 text-surface-400 transition-transform', pipeline[2].open ? 'rotate-180' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
        </div>
      </div>

      <div v-show="pipeline[2].open" class="px-5 pb-5 border-t border-surface-100 bg-surface-50/30 animate-fade-in space-y-4 pt-4">
        <!-- Rumus BM25 -->
        <div class="bg-blue-50 border border-blue-100 rounded-xl p-4">
          <div class="text-[10px] font-bold text-blue-500 uppercase tracking-widest mb-2">Formula BM25 (Okapi BM25)</div>
          <div class="font-mono text-xs text-blue-800 bg-white rounded-lg p-3 border border-blue-100 text-center leading-relaxed">
            Score(D,Q) = Σ IDF(qᵢ) × <span class="font-bold">[ f(qᵢ,D) × (k₁+1) ]</span> / <span class="font-bold">[ f(qᵢ,D) + k₁ × (1−b+b×|D|/avgdl) ]</span>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-2 mt-3 text-[10px] font-mono">
            <div class="bg-white rounded px-2 py-1.5 border border-blue-100 text-center">
              <div class="text-blue-500 font-bold">f(qᵢ,D)</div>
              <div class="text-surface-500 mt-0.5">Frek. term di dok.</div>
            </div>
            <div class="bg-white rounded px-2 py-1.5 border border-blue-100 text-center">
              <div class="text-blue-500 font-bold">IDF(qᵢ)</div>
              <div class="text-surface-500 mt-0.5">Kejarangan term</div>
            </div>
            <div class="bg-white rounded px-2 py-1.5 border border-blue-100 text-center">
              <div class="text-blue-500 font-bold">k₁ = 1.5</div>
              <div class="text-surface-500 mt-0.5">Saturasi frekuensi</div>
            </div>
            <div class="bg-white rounded px-2 py-1.5 border border-blue-100 text-center">
              <div class="text-blue-500 font-bold">b = 0.75</div>
              <div class="text-surface-500 mt-0.5">Normalisasi panjang</div>
            </div>
          </div>
        </div>

        <!-- Pencocokan kata -->
        <div v-if="hasilRekomendasi.length > 0" class="bg-white border border-blue-200 p-5 rounded-xl shadow-sm">
          <div class="flex justify-between items-end border-b border-blue-100 pb-3 mb-4">
            <div>
              <div class="text-[10px] font-bold text-blue-500 uppercase tracking-widest mb-1">Kandidat Terbaik BM25</div>
              <div class="font-bold text-blue-900 text-sm">{{ hasilRekomendasi[0].NAMA }}</div>
              <div class="text-[10px] text-surface-400 mt-0.5">{{ hasilRekomendasi[0].PROGRAM_STUDI }}</div>
            </div>
            <div class="text-right">
              <div class="text-[10px] font-bold text-blue-400 uppercase tracking-widest">Skor Leksikal</div>
              <div class="text-2xl font-extrabold text-blue-600">{{ Math.round(hasilRekomendasi[0]['Lexical Score'] * 100) }}%</div>
            </div>
          </div>

          <div class="text-[10px] font-bold text-surface-400 uppercase tracking-widest mb-2">Irisan Token Kueri ↔ Profil Dosen</div>
          <div class="flex flex-wrap gap-1.5 max-h-28 overflow-y-auto content-start p-2 bg-surface-50 rounded-lg">
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
          <div class="mt-3 flex justify-between text-[10px] text-surface-400 font-medium">
            <span>🔵 Kata ditemukan di profil dosen</span>
            <span>⚪ Kata tidak ditemukan</span>
          </div>

          <!-- Top 3 skor BM25 -->
          <div class="mt-4">
            <div class="text-[10px] font-bold text-surface-400 uppercase tracking-widest mb-2">Perbandingan Top-3 Skor BM25</div>
            <div class="space-y-2">
              <div v-for="(d, i) in hasilRekomendasi.slice(0, 3)" :key="'bm25_'+i" class="flex items-center gap-3">
                <div class="text-[10px] font-bold text-surface-400 w-4 shrink-0">{{ i+1 }}</div>
                <div class="text-[10px] font-medium text-surface-600 w-24 shrink-0 truncate">{{ d.NAMA.split(' ')[0] }}</div>
                <div class="flex-1 bg-surface-100 rounded-full h-2 overflow-hidden">
                  <div class="bg-blue-400 h-2 rounded-full transition-all duration-700" :style="`width: ${Math.round(d['Lexical Score'] * 100)}%`"></div>
                </div>
                <div class="text-[10px] font-bold text-blue-600 w-8 text-right">{{ Math.round(d['Lexical Score'] * 100) }}%</div>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-blue-50 border border-blue-100 rounded-xl p-3 text-xs text-blue-700 font-medium leading-relaxed">
          <span class="font-bold text-blue-800 uppercase text-[10px]">💡 Interpretasi:</span>
          BM25 mengutamakan kata yang jarang muncul di seluruh korpus (IDF tinggi) namun sering di dokumen ini (TF tinggi). Kata teknis seperti "machine learning" mendapat bobot lebih tinggi dari kata umum seperti "sistem".
        </div>
      </div>
    </div>

    <!-- ───────────── STEP 4: SBERT ───────────── -->
    <div v-show="hasStarted && pipeline[3].status !== 'idle'" :class="stepClass(pipeline[3])">
      <div v-if="pipeline[3].status === 'running'" class="absolute top-0 left-0 h-0.5 bg-fuchsia-500 animate-pulse w-full"></div>
      <div @click="pipeline[3].open = !pipeline[3].open" class="flex items-center justify-between p-5 cursor-pointer select-none">
        <div class="flex items-center gap-4">
          <div :class="[stepIconClass(pipeline[3]), pipeline[3].status !== 'done' ? 'bg-fuchsia-100! text-fuchsia-600!' : '']">
            {{ pipeline[3].status === 'done' ? '✓' : pipeline[3].icon }}
          </div>
          <div>
            <h3 class="font-bold text-surface-800 text-sm">{{ pipeline[3].title }}</h3>
            <p class="text-xs text-surface-500 font-medium mt-0.5">{{ pipeline[3].desc }}</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <span :class="[stepBadgeClass(pipeline[3]), pipeline[3].status !== 'done' ? 'bg-fuchsia-100! text-fuchsia-700!' : '']">
            {{ pipeline[3].status === 'done' ? 'Selesai' : 'Proses' }}
          </span>
          <svg :class="['w-4 h-4 text-surface-400 transition-transform', pipeline[3].open ? 'rotate-180' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
        </div>
      </div>

      <div v-show="pipeline[3].open" class="px-5 pb-5 border-t border-surface-100 bg-surface-50/30 animate-fade-in space-y-4 pt-4">
        <!-- Konsep vektor SBERT -->
        <div class="bg-fuchsia-50 border border-fuchsia-100 rounded-xl p-4">
          <div class="text-[10px] font-bold text-fuchsia-500 uppercase tracking-widest mb-2">Cara Kerja SBERT & Cosine Similarity</div>
          <div class="flex items-center gap-3 flex-wrap text-xs font-mono">
            <div class="bg-white rounded-lg px-3 py-2 border border-fuchsia-100 text-center">
              <div class="text-fuchsia-400 text-[10px] mb-1">Teks Kueri</div>
              <div class="text-fuchsia-700 font-bold">→ Vektor 768D</div>
            </div>
            <div class="text-fuchsia-300 font-bold text-lg">⊕</div>
            <div class="bg-white rounded-lg px-3 py-2 border border-fuchsia-100 text-center">
              <div class="text-fuchsia-400 text-[10px] mb-1">Profil Dosen</div>
              <div class="text-fuchsia-700 font-bold">→ Vektor 768D</div>
            </div>
            <div class="text-fuchsia-300 font-bold text-lg">→</div>
            <div class="bg-fuchsia-100 rounded-lg px-3 py-2 border border-fuchsia-200 text-center">
              <div class="text-fuchsia-500 text-[10px] mb-1">Cosine Sim.</div>
              <div class="text-fuchsia-800 font-bold">cos(θ) ∈ [0,1]</div>
            </div>
          </div>
          <div class="mt-3 text-[10px] font-mono text-fuchsia-700 bg-white rounded-lg p-2 border border-fuchsia-100 text-center">
            similarity = (A · B) / (‖A‖ × ‖B‖)
          </div>
        </div>

        <!-- Kandidat terbaik SBERT -->
        <div v-if="hasilRekomendasi.length > 0" class="bg-white border border-fuchsia-200 p-5 rounded-xl shadow-sm">
          <div class="flex justify-between items-end border-b border-fuchsia-100 pb-3 mb-4">
            <div>
              <div class="text-[10px] font-bold text-fuchsia-500 uppercase tracking-widest mb-1">Kandidat Terbaik SBERT</div>
              <div class="font-bold text-fuchsia-900 text-sm">{{ hasilRekomendasi[0].NAMA }}</div>
              <div class="text-[10px] text-surface-400 mt-0.5">{{ hasilRekomendasi[0].PROGRAM_STUDI }}</div>
            </div>
            <div class="text-right">
              <div class="text-[10px] font-bold text-fuchsia-400 uppercase tracking-widest">Cosine Similarity</div>
              <div class="text-2xl font-extrabold text-fuchsia-600">{{ Math.round(hasilRekomendasi[0]['Semantic Score'] * 100) }}%</div>
            </div>
          </div>

          <!-- Progress bar kemiripan -->
          <div class="mb-4">
            <div class="flex justify-between text-[10px] font-bold text-surface-500 uppercase mb-1">
              <span>Kemiripan Makna (Cosine Similarity)</span>
              <span>{{ Math.round(hasilRekomendasi[0]['Semantic Score'] * 100) }} / 100</span>
            </div>
            <div class="w-full bg-surface-100 rounded-full h-3 overflow-hidden">
              <div class="bg-linear-to-r from-fuchsia-400 to-fuchsia-600 h-3 rounded-full transition-all duration-1000" :style="`width: ${Math.round(hasilRekomendasi[0]['Semantic Score'] * 100)}%`"></div>
            </div>
            <div class="flex justify-between text-[10px] text-surface-400 mt-1">
              <span>0 (tidak relevan)</span><span>50 (cukup relevan)</span><span>100 (sangat relevan)</span>
            </div>
          </div>

          <!-- KeyBERT frasa -->
          <div class="mb-4">
            <div class="text-[10px] font-bold text-fuchsia-500 uppercase tracking-widest mb-2">Topik Dominan Dosen (KeyBERT Extraction)</div>
            <div class="text-[10px] text-surface-400 mb-2 leading-relaxed">KeyBERT mengekstrak frasa paling representatif dari profil publikasi dosen menggunakan embedding BERT.</div>
            <div class="flex flex-wrap gap-2">
              <div v-if="parseSemantik(hasilRekomendasi[0]).length === 0" class="text-xs text-surface-400 font-medium italic">Tidak ada frasa dominan terdeteksi.</div>
              <span v-for="(frasa, idx) in parseSemantik(hasilRekomendasi[0])" :key="idx"
                class="bg-fuchsia-50 text-fuchsia-700 border border-fuchsia-200 px-3 py-1.5 rounded-lg text-xs font-mono font-bold shadow-sm flex items-center gap-1.5">
                <span class="w-1.5 h-1.5 rounded-full bg-fuchsia-500 shrink-0"></span> {{ frasa }}
              </span>
            </div>
          </div>

          <!-- Top 3 skor semantik -->
          <div>
            <div class="text-[10px] font-bold text-surface-400 uppercase tracking-widest mb-2">Perbandingan Top-3 Skor SBERT</div>
            <div class="space-y-2">
              <div v-for="(d, i) in hasilRekomendasi.slice(0, 3)" :key="'sbert_'+i" class="flex items-center gap-3">
                <div class="text-[10px] font-bold text-surface-400 w-4 shrink-0">{{ i+1 }}</div>
                <div class="text-[10px] font-medium text-surface-600 w-24 shrink-0 truncate">{{ d.NAMA.split(' ')[0] }}</div>
                <div class="flex-1 bg-surface-100 rounded-full h-2 overflow-hidden">
                  <div class="bg-fuchsia-400 h-2 rounded-full transition-all duration-700" :style="`width: ${Math.round(d['Semantic Score'] * 100)}%`"></div>
                </div>
                <div class="text-[10px] font-bold text-fuchsia-600 w-8 text-right">{{ Math.round(d['Semantic Score'] * 100) }}%</div>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-fuchsia-50 border border-fuchsia-100 rounded-xl p-3 text-xs text-fuchsia-700 font-medium leading-relaxed">
          <span class="font-bold text-fuchsia-800 uppercase text-[10px]">💡 Interpretasi:</span>
          SBERT memahami makna kontekstual. "Jaringan syaraf tiruan" dan "deep learning" akan memiliki cosine similarity tinggi meskipun tidak ada kata yang sama persis — berbeda dengan BM25 yang hanya mencocokkan kata per kata.
        </div>
      </div>
    </div>

    <!-- ───────────── STEP 5: Hybrid Ranking ───────────── -->
    <div v-show="hasStarted && pipeline[4].status !== 'idle'" :class="stepClass(pipeline[4])">
      <div v-if="pipeline[4].status === 'running'" class="absolute top-0 left-0 h-0.5 bg-primary-500 animate-pulse w-full"></div>
      <div @click="pipeline[4].open = !pipeline[4].open" class="flex items-center justify-between p-5 cursor-pointer select-none">
        <div class="flex items-center gap-4">
          <div :class="stepIconClass(pipeline[4])">{{ pipeline[4].status === 'done' ? '✓' : pipeline[4].icon }}</div>
          <div>
            <h3 class="font-bold text-surface-800 text-sm">{{ pipeline[4].title }}</h3>
            <p class="text-xs text-surface-500 font-medium mt-0.5">{{ pipeline[4].desc }}</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <span :class="stepBadgeClass(pipeline[4])">{{ pipeline[4].status === 'done' ? 'Selesai' : 'Proses' }}</span>
          <svg :class="['w-4 h-4 text-surface-400 transition-transform', pipeline[4].open ? 'rotate-180' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
        </div>
      </div>

      <div v-show="pipeline[4].open" class="px-5 pb-5 border-t border-surface-100 bg-surface-50/30 animate-fade-in space-y-6 pt-4">

        <!-- Diagram alur penyaringan + kalkulasi hybrid -->
        <div v-if="hasilRekomendasi.length > 0" class="grid grid-cols-1 md:grid-cols-12 gap-4">

          <!-- Funnel penyaringan -->
          <div class="md:col-span-4 bg-white border border-surface-200 rounded-xl p-4 flex flex-col items-center justify-center space-y-2">
            <div class="text-[10px] font-bold text-surface-400 uppercase tracking-widest mb-2">Funnel Penyaringan Kandidat</div>
            <div class="bg-surface-100 text-surface-600 font-bold text-xs px-4 py-1.5 rounded-lg w-[95%] text-center border border-surface-200">
              Pangkalan Data Dosen
            </div>
            <div class="text-surface-300 text-xs">▼ BM25 seleksi awal</div>
            <div class="bg-blue-100 text-blue-700 font-bold text-xs px-4 py-1.5 rounded-lg w-[78%] text-center border border-blue-200">
              Kandidat BM25
            </div>
            <div class="text-surface-300 text-xs">▼ SBERT re-rank</div>
            <div class="bg-fuchsia-100 text-fuchsia-700 font-bold text-xs px-4 py-1.5 rounded-lg w-[60%] text-center border border-fuchsia-200">
              Hybrid Score
            </div>
            <div class="text-surface-300 text-xs">▼ Ambil Top-K</div>
            <div class="bg-primary-500 text-white font-bold text-xs px-4 py-1.5 rounded-lg w-[44%] text-center shadow-md shadow-primary-200">
              Top {{ kRank }} Hasil
            </div>
          </div>

          <!-- Formula hybrid -->
          <div class="md:col-span-8 bg-white border border-surface-200 rounded-xl p-4 flex flex-col justify-center space-y-4">
            <div class="text-[10px] font-bold text-surface-400 uppercase tracking-widest">Formula Skor Hybrid (Peringkat #1)</div>

            <div class="bg-surface-50 rounded-xl p-4 border border-surface-100">
              <div class="text-[10px] text-surface-400 font-bold mb-3 uppercase">Score_hybrid = α × Score_BM25 + β × Score_SBERT</div>
              <div class="flex items-center justify-center gap-2 text-sm font-mono flex-wrap">
                <div class="text-center">
                  <div class="text-surface-400 text-[10px]">α (bobot leksikal)</div>
                  <div class="text-blue-600 font-extrabold text-lg">{{ isAdaptifMode ? hasilRekomendasi[0]['Alpha'] ?? '?' : (bobotLexical / 100).toFixed(2) }}</div>
                </div>
                <span class="text-surface-400">×</span>
                <div class="text-center">
                  <div class="text-surface-400 text-[10px]">Skor BM25</div>
                  <div class="text-blue-600 font-extrabold text-lg">{{ hasilRekomendasi[0]['Lexical Score'] }}</div>
                </div>
                <span class="text-surface-400 font-extrabold text-xl">+</span>
                <div class="text-center">
                  <div class="text-surface-400 text-[10px]">β (bobot semantik)</div>
                  <div class="text-fuchsia-600 font-extrabold text-lg">{{ isAdaptifMode ? hasilRekomendasi[0]['Beta'] ?? '?' : ((100 - bobotLexical) / 100).toFixed(2) }}</div>
                </div>
                <span class="text-surface-400">×</span>
                <div class="text-center">
                  <div class="text-surface-400 text-[10px]">Skor SBERT</div>
                  <div class="text-fuchsia-600 font-extrabold text-lg">{{ hasilRekomendasi[0]['Semantic Score'] }}</div>
                </div>
                <span class="text-surface-400 font-extrabold text-xl">=</span>
                <div class="text-center bg-primary-100 px-4 py-2 rounded-xl border border-primary-200">
                  <div class="text-primary-500 text-[10px] uppercase tracking-wider">Skor Akhir</div>
                  <div class="text-primary-700 font-extrabold text-2xl">{{ hasilRekomendasi[0]['Hybrid Score'] }}</div>
                </div>
              </div>
            </div>

            <!-- Kontribusi visual -->
            <div>
              <div class="text-[10px] font-bold text-surface-400 uppercase tracking-widest mb-2">Kontribusi Komponen (Peringkat #1)</div>
              <div class="flex h-6 rounded-full overflow-hidden border border-surface-200">
                <div class="bg-blue-400 h-full transition-all duration-700 flex items-center justify-center"
                  :style="`width: ${isAdaptifMode ? 50 : bobotLexical}%`">
                  <span class="text-[9px] font-bold text-white whitespace-nowrap px-1">BM25 {{ isAdaptifMode ? '~50' : bobotLexical }}%</span>
                </div>
                <div class="bg-fuchsia-400 h-full flex-1 flex items-center justify-center">
                  <span class="text-[9px] font-bold text-white whitespace-nowrap px-1">SBERT {{ isAdaptifMode ? '~50' : (100 - bobotLexical) }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Tabel hasil akhir -->
        <div v-if="hasilRekomendasi.length > 0">
          <div class="text-[10px] font-bold text-surface-400 uppercase tracking-widest mb-3">Tabel Peringkat Akhir — Top {{ kRank }} Rekomendasi Dosen Pembimbing</div>
          <div class="border border-surface-200 rounded-xl overflow-hidden bg-white shadow-sm">
            <table class="w-full text-left border-collapse">
              <thead class="bg-surface-50 border-b border-surface-200 text-[10px] font-bold text-surface-500 uppercase tracking-wider font-mono">
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
                <!-- DosenCard replaces the table rows -->
                <DosenCard 
                  v-for="(dosen, index) in hasilRekomendasi" 
                  :key="index"
                  :dosen="dosen"
                  :index="index"
                  @click="$emit('bukaDetail', dosen)"
                />
              </tbody>
            </table>
          </div>
          <div class="text-[10px] text-surface-400 mt-2 text-center">Klik baris untuk melihat detail profil dosen</div>
        </div>

        <!-- Interpretasi skor -->
        <div v-if="hasilRekomendasi.length > 0" class="bg-primary-50 border border-primary-100 rounded-xl p-4">
          <div class="text-[10px] font-bold text-primary-500 uppercase tracking-widest mb-3">Panduan Interpretasi Skor Rekomendasi</div>
          <div class="grid grid-cols-3 gap-3 text-xs">
            <div class="bg-white rounded-lg p-3 border border-red-100 text-center">
              <div class="text-red-500 font-extrabold text-lg mb-1">&lt; 40%</div>
              <div class="text-red-400 font-bold text-[10px] uppercase">Kurang Relevan</div>
              <div class="text-surface-500 text-[10px] mt-1">Perlu pertimbangan tambahan</div>
            </div>
            <div class="bg-white rounded-lg p-3 border border-amber-100 text-center">
              <div class="text-amber-500 font-extrabold text-lg mb-1">40–70%</div>
              <div class="text-amber-400 font-bold text-[10px] uppercase">Cukup Relevan</div>
              <div class="text-surface-500 text-[10px] mt-1">Relevan dengan topik umum</div>
            </div>
            <div class="bg-white rounded-lg p-3 border border-emerald-100 text-center">
              <div class="text-emerald-500 font-extrabold text-lg mb-1">&gt; 70%</div>
              <div class="text-emerald-400 font-bold text-[10px] uppercase">Sangat Relevan</div>
              <div class="text-surface-500 text-[10px] mt-1">Rekomendasi kuat</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import DosenCard from './DosenCard.vue';

const props = defineProps({
  hasStarted: Boolean,
  pipeline: Array,
  judulInput: String,
  abstrakInput: String,
  kRank: Number,
  isAdaptifMode: Boolean,
  bobotLexical: Number,
  metadataMesin: Object,
  hasilRekomendasi: Array
});

defineEmits(['bukaDetail']);

const stepClass = (step) => [
  'rounded-2xl border transition-all duration-500 overflow-hidden relative bg-white',
  step.status === 'running'
    ? 'border-primary-400 shadow-lg shadow-primary-100/50 scale-[1.01]'
    : 'border-surface-200 opacity-85 hover:opacity-100'
];

const stepIconClass = (step) => [
  'w-10 h-10 rounded-xl flex items-center justify-center text-lg font-bold transition-all',
  step.status === 'running'
    ? 'bg-primary-100 text-primary-600 animate-pulse'
    : step.status === 'done'
      ? 'bg-emerald-100 text-emerald-600'
      : 'bg-surface-100 text-surface-500'
];

const stepBadgeClass = (step) => [
  'text-[10px] font-bold px-3 py-1 rounded-lg uppercase tracking-wider',
  step.status === 'running' ? 'bg-primary-100 text-primary-700' : 'bg-surface-100 text-surface-600'
];

const cekLexical = (token, dosen) => {
  if (!dosen || !dosen['Irisan Kata (Lexical)'] || dosen['Irisan Kata (Lexical)'] === '-') return false;
  return dosen['Irisan Kata (Lexical)'].split(', ').includes(token);
};

const parseSemantik = (dosen) => {
  if (!dosen || !dosen['Frasa Terkait (KeyBERT)'] || dosen['Frasa Terkait (KeyBERT)'] === '-') return [];
  return dosen['Frasa Terkait (KeyBERT)'].split(', ');
};
</script>
