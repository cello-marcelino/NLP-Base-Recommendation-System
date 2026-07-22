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
