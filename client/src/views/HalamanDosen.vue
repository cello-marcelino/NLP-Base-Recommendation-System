<template>
  <div class="max-w-7xl mx-auto py-8">
    <div class="flex justify-between items-end mb-8">
      <div>
        <h2 class="text-3xl font-extrabold text-slate-800 tracking-tight">Pangkalan Data Dosen</h2>
        <p class="text-slate-500 mt-1">Daftar seluruh tenaga pendidik beserta rekam jejak akademik.</p>
      </div>
      <div class="bg-white border border-slate-200 px-4 py-2 rounded-xl shadow-sm text-sm font-semibold text-slate-700">
        Total: <span class="text-violet-600">{{ daftarDosen.length }}</span> Dosen
      </div>
    </div>

    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr
              class="bg-slate-50/50 border-b border-slate-200 text-xs uppercase tracking-widest text-slate-400 font-bold">
              <th class="p-5 font-bold">Informasi Dosen</th>
              <th class="p-5 font-bold">Bidang Keahlian</th>
              <th class="p-5 font-bold text-center">Rekam Jejak</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="(dosen, index) in daftarDosen" :key="index" class="hover:bg-slate-50/80 transition-colors group">
              <td class="p-5">
                <div class="font-bold text-slate-800 text-base">{{ dosen.NAMA }}</div>
                <div class="text-sm font-medium text-violet-600 mt-0.5">{{ dosen.PROGRAM_STUDI }}</div>
              </td>
              <td class="p-5 max-w-md">
                <div class="flex flex-wrap gap-1.5">
                  <span v-for="(skill, i) in formatArray(dosen.BIDANG_KEAHLIAN).slice(0, 4)" :key="i"
                    class="bg-slate-100 text-slate-600 px-2.5 py-1 rounded-md text-xs font-medium border border-slate-200">
                    {{ skill }}
                  </span>
                  <span v-if="formatArray(dosen.BIDANG_KEAHLIAN).length > 4"
                    class="bg-violet-50 text-violet-600 px-2 py-1 rounded-md text-xs font-bold">
                    +{{ formatArray(dosen.BIDANG_KEAHLIAN).length - 4 }}
                  </span>
                </div>
              </td>
              <td class="p-5 text-center">
                <button @click="bukaDetail(dosen)"
                  class="text-sm bg-white border border-slate-300 text-slate-600 font-semibold px-4 py-2 rounded-lg transition-all group-hover:border-violet-400 group-hover:text-violet-700 shadow-sm hover:shadow">
                  Lihat Detail
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <ModalDetail :isOpen="modalAktif" :dataDosen="dosenTerpilih" :tutupModal="tutupDetail" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api';
import ModalDetail from '../components/ModalDetail.vue';

const daftarDosen = ref([]);
const modalAktif = ref(false);
const dosenTerpilih = ref({});

onMounted(async () => {
  try {
    const respons = await api.getSemuaDosen();
    daftarDosen.value = respons.data;
  } catch (error) {
    console.error("Gagal mengambil data.");
  }
});

const formatArray = (text) => {
  if (!text) return [];
  let str = String(text).replace(/^\[|\]$/g, '').trim();
  let arr = str.includes('", "') ? str.split('", "') : str.split(',');
  return arr.map(s => s.replace(/(^")|("$)/g, '').trim()).filter(x => x && x !== '-');
};

const bukaDetail = (dosen) => { dosenTerpilih.value = dosen; modalAktif.value = true; };
const tutupDetail = () => { modalAktif.value = false; };
</script>