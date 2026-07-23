<template>
  <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
    
    <!-- Header Dashboard -->
    <div class="flex flex-col md:flex-row md:justify-between md:items-end gap-5 mb-8">
      <div>
        <h2 class="text-3xl font-extrabold text-surface-800 tracking-tight">Manajemen Dosen</h2>
        <p class="text-surface-500 mt-1">Kelola profil, portofolio, dan rekam jejak dosen untuk mesin AI.</p>
      </div>
      
      <div class="flex items-center w-full md:w-auto">
        <button @click="bukaModalTambah" class="w-full md:w-auto flex justify-center items-center gap-2 bg-primary-600 hover:bg-primary-700 text-white px-5 py-2.5 rounded-xl shadow-sm font-medium transition-all focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 outline-none">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
          Tambah Dosen
        </button>
      </div>
    </div>

    <!-- Tabel Data (Sesuai Gaya Pangkalan Data) -->
    <div class="bg-white rounded-2xl shadow-sm border border-surface-200 overflow-hidden mb-6">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-surface-50/50 border-b border-surface-200 text-xs uppercase tracking-widest text-surface-400 font-bold">
              <th class="p-5 font-bold">Informasi Dosen</th>
              <th class="p-5 font-bold">Bidang Keahlian</th>
              <th class="p-5 font-bold text-center">Aksi Manajemen</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-surface-100">
            <!-- Empty State -->
            <tr v-if="daftarDosen.length === 0">
              <td colspan="3" class="p-10 text-center">
                <div class="flex flex-col items-center justify-center text-surface-400">
                  <svg class="w-12 h-12 mb-3 text-surface-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path></svg>
                  <span class="font-bold text-base text-surface-500">Data dosen masih kosong.</span>
                  <span class="text-sm mt-1">Silakan tambahkan data baru untuk mesin AI.</span>
                </div>
              </td>
            </tr>
            
            <!-- Data Rows -->
            <tr v-for="dosen in daftarDosen" :key="dosen.id_dosen" class="hover:bg-surface-50/80 transition-colors group">
              <td class="p-5">
                <div class="font-bold text-surface-800 text-base">{{ dosen.nama }}</div>
                <div class="text-sm font-medium text-primary-600 mt-0.5">{{ dosen.program_studi || '-' }}</div>
              </td>
              <td class="p-5 max-w-md">
                <div class="flex flex-wrap gap-1.5">
                  <span v-for="(skill, i) in formatKeahlian(dosen.bidang_keahlian)" :key="i"
                    class="bg-surface-100 text-surface-600 px-2.5 py-1 rounded-md text-[10px] font-bold border border-surface-200 uppercase tracking-wider">
                    {{ skill }}
                  </span>
                </div>
              </td>
              <td class="p-5 text-center">
                <div class="flex justify-center gap-2">
                  <button @click="bukaModalEdit(dosen)" class="text-sm bg-white border border-surface-300 text-surface-600 font-semibold px-3 py-1.5 rounded-lg transition-all hover:border-primary-400 hover:bg-primary-50 hover:text-primary-700 shadow-sm" title="Edit">
                    Edit
                  </button>
                  <button @click="hapusData(dosen.id_dosen)" class="text-sm bg-white border border-surface-300 text-surface-600 font-semibold px-3 py-1.5 rounded-lg transition-all hover:border-red-400 hover:bg-red-50 hover:text-red-600 shadow-sm" title="Hapus">
                    Hapus
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Form Minimalis -->
    <transition enter-active-class="ease-out duration-300" enter-from-class="opacity-0" enter-to-class="opacity-100" leave-active-class="ease-in duration-200" leave-from-class="opacity-100" leave-to-class="opacity-0">
      <div v-if="tampilkanModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
        
        <!-- Backdrop -->
        <div class="fixed inset-0 bg-surface-800/40 backdrop-blur-sm transition-opacity" @click="tampilkanModal = false"></div>

        <!-- Panel Form -->
        <transition enter-active-class="ease-out duration-300" enter-from-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95" enter-to-class="opacity-100 translate-y-0 sm:scale-100" leave-active-class="ease-in duration-200" leave-from-class="opacity-100 translate-y-0 sm:scale-100" leave-to-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
          <div v-if="tampilkanModal" class="relative w-full max-w-2xl bg-white rounded-2xl shadow-xl border border-surface-200 overflow-hidden transform transition-all flex flex-col max-h-[90vh]">
            
            <div class="px-6 py-5 border-b border-surface-100 flex justify-between items-center bg-surface-50/50">
              <h3 class="text-lg font-extrabold text-surface-800">{{ isEdit ? 'Edit Profil Dosen' : 'Tambah Dosen Baru' }}</h3>
              <button @click="tampilkanModal = false" class="text-surface-400 hover:text-red-500 transition-colors outline-none">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
              </button>
            </div>

            <form @submit.prevent="simpanData" class="px-6 py-5 space-y-5 overflow-y-auto custom-scrollbar">
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-bold text-surface-700 mb-1.5">Nama Lengkap</label>
                  <input v-model="formData.nama" type="text" placeholder="Gelar & Nama" required 
                    class="w-full px-4 py-2.5 bg-white border border-surface-200 rounded-xl shadow-sm text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-all placeholder-surface-400 text-surface-700 font-medium" />
                </div>
                <div>
                  <label class="block text-sm font-bold text-surface-700 mb-1.5">Program Studi</label>
                  <input v-model="formData.program_studi" type="text" placeholder="Contoh: Teknik Informatika" required 
                    class="w-full px-4 py-2.5 bg-white border border-surface-200 rounded-xl shadow-sm text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-all placeholder-surface-400 text-surface-700 font-medium" />
                </div>
              </div>

              <div>
                <label class="block text-sm font-bold text-surface-700 mb-1.5">Bidang Keahlian</label>
                <textarea v-model="formData.bidang_keahlian" rows="2" placeholder="Pisahkan dengan koma (Contoh: Data Mining, AI)" 
                  class="w-full px-4 py-2.5 bg-white border border-surface-200 rounded-xl shadow-sm text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-all placeholder-surface-400 text-surface-700 font-medium"></textarea>
              </div>

              <div>
                <label class="block text-sm font-bold text-surface-700 mb-1.5">Publikasi Jurnal</label>
                <textarea v-model="formData.jurnal" rows="3" placeholder="Daftar publikasi jurnal dosen..." 
                  class="w-full px-4 py-2.5 bg-white border border-surface-200 rounded-xl shadow-sm text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-all placeholder-surface-400 text-surface-700 font-medium"></textarea>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-bold text-surface-700 mb-1.5">Riwayat Bimbingan</label>
                  <textarea v-model="formData.judul_bimbing" rows="3" placeholder="Judul skripsi yang pernah dibimbing..." 
                    class="w-full px-4 py-2.5 bg-white border border-surface-200 rounded-xl shadow-sm text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-all placeholder-surface-400 text-surface-700 font-medium"></textarea>
                </div>
                <div>
                  <label class="block text-sm font-bold text-surface-700 mb-1.5">Riwayat Pengujian</label>
                  <textarea v-model="formData.judul_uji" rows="3" placeholder="Judul skripsi yang pernah diuji..." 
                    class="w-full px-4 py-2.5 bg-white border border-surface-200 rounded-xl shadow-sm text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-all placeholder-surface-400 text-surface-700 font-medium"></textarea>
                </div>
              </div>

            </form>

            <div class="px-6 py-4 bg-surface-50/80 border-t border-surface-100 flex justify-end gap-3 rounded-b-2xl shrink-0">
              <button type="button" @click="tampilkanModal = false" class="px-5 py-2.5 border border-surface-300 shadow-sm text-sm font-bold rounded-xl text-surface-600 bg-white hover:bg-surface-50 hover:text-surface-800 transition-colors">
                Batal
              </button>
              <button type="button" @click="simpanData" :disabled="statusMenyimpan" class="inline-flex items-center px-6 py-2.5 border border-transparent shadow-sm text-sm font-bold rounded-xl text-white bg-primary-600 hover:bg-primary-700 transition-all disabled:opacity-70 disabled:cursor-not-allowed">
                <svg v-if="statusMenyimpan" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ statusMenyimpan ? 'Menyimpan...' : 'Simpan Data' }}
              </button>
            </div>

          </div>
        </transition>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api';
import { showToast } from '../utils/toast';

const daftarDosen = ref([]);
const tampilkanModal = ref(false);
const isEdit = ref(false);
const statusMenyimpan = ref(false);
const idTerpilih = ref(null);

const formData = ref({
  nama: '', program_studi: '', bidang_keahlian: '', jurnal: '', judul_bimbing: '', judul_uji: '', riwayat_pendidikan: ''
});

// Format Badge (Sama persis dengan komponen HalamanDosen)
const formatKeahlian = (text) => {
  if (!text) return [];
  let str = String(text).replace(/^\[|\]$/g, '').trim();
  let arr = str.includes('", "') ? str.split('", "') : str.split(',');
  return arr.map(s => s.replace(/(^")|("$)/g, '').trim()).filter(x => x && x !== '-');
};

// Normalisasi dari Backend (Adaptor UPPERCASE MySQL ke Lowercase)
const normalisasiDataBackend = (rawDataArray) => {
  if (!Array.isArray(rawDataArray)) return [];
  
  return rawDataArray.map(item => {
    // PENCARI ID SUPER KEBAL: Mencari kunci ID tanpa memedulikan huruf besar/kecil
    let idDosenDitemukan = null;
    for (const key in item) {
      const lowerKey = key.toLowerCase();
      if (lowerKey === 'id' || lowerKey === 'id_dosen') {
        idDosenDitemukan = item[key];
        break;
      }
    }

    return {
      id_dosen: idDosenDitemukan, // Menggunakan ID yang sudah pasti ketemu
      nama: item.nama || item.NAMA || '',
      program_studi: item.program_studi || item.PROGRAM_STUDI || '',
      bidang_keahlian: item.bidang_keahlian || item.BIDANG_KEAHLIAN || '',
      jurnal: item.jurnal || item.JURNAL || '',
      judul_bimbing: item.judul_bimbing || item.JUDUL_BIMBING || '',
      judul_uji: item.judul_uji || item.JUDUL_UJI || '',
      riwayat_pendidikan: item.riwayat_pendidikan || item.RIWAYAT_PENDIDIKAN || ''
    };
  });
};

const muatData = async () => {
  try {
    const res = await api.getSemuaDosen();
    const rawArray = res.data ? res.data : res;
    daftarDosen.value = normalisasiDataBackend(rawArray);
  } catch (error) {
    console.error(error);
    showToast('Gagal memuat data dosen dari server.', 'error');
  }
};

const bukaModalTambah = () => {
  isEdit.value = false;
  formData.value = { nama: '', program_studi: '', bidang_keahlian: '', jurnal: '', judul_bimbing: '', judul_uji: '', riwayat_pendidikan: '' };
  tampilkanModal.value = true;
};

const bukaModalEdit = (dosen) => {
  isEdit.value = true;
  idTerpilih.value = dosen.id_dosen;
  formData.value = { ...dosen };
  tampilkanModal.value = true;
};

const simpanData = async () => {
  if (!formData.value.nama || !formData.value.program_studi) {
    showToast('Nama dan Program Studi wajib diisi!', 'error');
    return;
  }

  statusMenyimpan.value = true;
  try {
    let res;
    if (isEdit.value) {
      if (!idTerpilih.value) {
        showToast('Sistem Gagal: ID tidak valid untuk diedit!', 'error');
        statusMenyimpan.value = false;
        return;
      }
      res = await api.editDosen(idTerpilih.value, formData.value);
    } else {
      res = await api.tambahDosen(formData.value);
    }

    if (res.status === 'sukses') {
      showToast('Berhasil! Sinkronisasi AI di latar belakang berjalan.', 'success');
      tampilkanModal.value = false;
      muatData();
    } else {
      showToast(res.pesan || 'Gagal menyimpan data.', 'error');
    }
  } catch (error) {
    console.error(error);
    showToast('Terjadi kesalahan jaringan atau server.', 'error');
  } finally {
    statusMenyimpan.value = false;
  }
};

const hapusData = async (id) => {
  if (!id) {
    showToast('Sistem Gagal: ID Dosen tidak ditemukan di database!', 'error');
    console.log("Data ID Kosong:", id);
    return;
  }

  if (!confirm('Yakin ingin menghapus data dosen ini? Data tidak dapat dikembalikan.')) return;
  
  try {
    const res = await api.hapusDosen(id);
    if (res.status === 'sukses') {
      showToast('Data dihapus! Sinkronisasi AI sedang berjalan.', 'success');
      muatData();
    } else {
      showToast(res.pesan || 'Gagal menghapus data.', 'error');
    }
  } catch (error) {
    console.error(error);
    showToast('Terjadi kesalahan saat menghapus.', 'error');
  }
};

onMounted(() => {
  muatData();
});
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1; /* Setara dengan gray-300/surface-300 */
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94a3b8; /* Setara dengan gray-400/surface-400 */
}
</style>