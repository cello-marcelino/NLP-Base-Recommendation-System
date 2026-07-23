const BASE_URL = 'http://127.0.0.1:5050/api';

export default {
  async getSemuaDosen() {
    const respons = await fetch(`${BASE_URL}/dosen`);
    if (!respons.ok) throw new Error('Gagal terhubung ke server');
    return await respons.json();
  },

  async getRekomendasi(judulMhs, abstrakMhs, kRank, bobotLexical, bobotSemantic) {
    const respons = await fetch(`${BASE_URL}/rekomendasi`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        judul: judulMhs,
        abstrak: abstrakMhs,
        k: kRank,
        bobot_lexical: bobotLexical,
        bobot_semantic: bobotSemantic
      })
    });
    if (!respons.ok) {
      const err = await respons.json();
      throw new Error(err.pesan || 'Terjadi kesalahan komputasi di server');
    }
    return await respons.json();
  },

  tambahDosen: async (dataDosen) => {
    const response = await fetch(`${BASE_URL}/admin/dosen`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dataDosen)
    });
    return response.json();
  },

  editDosen: async (idDosen, dataDosen) => {
    const response = await fetch(`${BASE_URL}/admin/dosen/${idDosen}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dataDosen)
    });
    return response.json();
  },

  hapusDosen: async (idDosen) => {
    const response = await fetch(`${BASE_URL}/admin/dosen/${idDosen}`, {
      method: 'DELETE'
    });
    return response.json();
  },

  // Tambahkan di bawah fungsi-fungsi CRUD Dosen sebelumnya
  getRiwayat: async () => {
    const response = await fetch(`${BASE_URL}/admin/riwayat`);
    return response.json();
  },

  async refreshServer() {
    const respons = await fetch(`${BASE_URL}/refresh`, { method: 'POST' });
    if (!respons.ok) throw new Error('Gagal menyegarkan server');
    return await respons.json();
  },

  async cekStatusServer() {
    const respons = await fetch(`${BASE_URL}/status`);
    if (!respons.ok) throw new Error('Gagal mengecek status server');
    return await respons.json();
  }
}
