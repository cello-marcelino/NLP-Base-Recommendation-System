from locust import HttpUser, task, between

DATA_PENCARIAN = [
    {
        "judul": "Pengembangan Sistem Pakar Diagnosa Penyakit Kulit",
        "abstrak": "Penelitian ini bertujuan membangun sistem pakar menggunakan metode forward chaining dan certainty factor untuk mendeteksi penyakit kulit berdasarkan gejala klinis.",
        "k_rank": 5,
        "bobot_lexical": 0.3,
        "bobot_semantic": 0.7
    },
    {
        "judul": "Analisis Sentimen Masyarakat terhadap Kebijakan Kampus di Twitter",
        "abstrak": "Menggunakan algoritma Naive Bayes dan Support Vector Machine (SVM) untuk mengklasifikasikan opini mahasiswa di media sosial ke dalam sentimen positif, negatif, dan netral.",
        "k_rank": 10,
        "bobot_lexical": 0.5,
        "bobot_semantic": 0.5
    },
    {
        "judul": "Penerapan Deep Learning untuk Deteksi Objek Kendaraan",
        "abstrak": "Menggunakan arsitektur YOLOv8 untuk mendeteksi dan menghitung jumlah kendaraan secara real-time pada rekaman CCTV persimpangan jalan raya.",
        "k_rank": 5,
        "bobot_lexical": 0.2,
        "bobot_semantic": 0.8
    }
]

class MahasiswaNormal(HttpUser):
    weight = 7
    wait_time = between(5.0, 15.0)

    @task
    def cari_rekomendasi(self):
        import random
        payload = random.choice(DATA_PENCARIAN)
        with self.client.post("/api/rekomendasi", json=payload, catch_response=True) as response:
            if response.status_code in [200, 503]:
                response.success()
            else:
                response.failure(f"Fail: {response.status_code}")

class MahasiswaAgresif(HttpUser):
    weight = 2
    wait_time = between(1.0, 2.0)

    @task
    def spam_rekomendasi(self):
        payload = DATA_PENCARIAN[0]
        with self.client.post("/api/rekomendasi", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Fail: {response.status_code}")

class PemeriksaStatus(HttpUser):
    weight = 1
    wait_time = between(2.0, 5.0)

    @task
    def cek_status_mesin(self):
        with self.client.get("/api/status", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            # Abaikan jika endpoint belum ada/error 404 agar tidak merusak log
            elif response.status_code == 404: 
                response.success()