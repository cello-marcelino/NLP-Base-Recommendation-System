# Scalability & Performance

Aturan stateless service, caching, background processing, dan performance measurement. Berlaku saat desain sistem yang menyangkut load atau kecepatan.

---

## Stateless Application
Application server sebaiknya stateless, jangan jadikan memory lokal server sebagai source of truth. Gunakan Database, Redis, atau Object Storage untuk state yang harus dibagikan antar-instance.

## Horizontal Scaling
```
Load Balancer -> API-1, API-2, API-3 -> Database
```
Application harus bisa dijalankan lebih dari satu instance kalau workload membutuhkannya.

## Background Processing
Operasi berat yang tidak harus selesai dalam satu HTTP request dipindah ke background worker:
```
HTTP Request -> Queue -> Worker -> Heavy Processing
```
Contoh: email, report generation, ML inference batch, data import, image processing, scheduled processing.

## Pagination
Endpoint yang mengembalikan collection besar wajib pagination.
```
# Salah
GET /users

# Benar
GET /users?page=1&limit=20
```

## Caching
Setiap cache harus punya lifecycle yang jelas: Key, TTL, Source of Truth, Invalidation Strategy, Fallback.
```
Cache miss -> Database -> Cache -> Response
```
- Jangan gunakan cache sebagai satu-satunya source of truth kecuali memang dirancang demikian
- Jangan tambahkan cache tanpa alasan yang jelas
- Kalau sistem butuh high availability, siapkan fallback saat cache gagal

## Performance
Optimization harus berdasarkan measurement, jangan premature optimization:
```
Correctness -> Profiling -> Identify bottleneck -> Optimize -> Measure again
```
Metrics yang relevan: response time, CPU usage, memory usage, database latency, query count, throughput, error rate.

Alur yang benar:
```
API lambat -> Profiling -> Database query lambat -> EXPLAIN query
-> Add/optimize index -> Measure
```
Bukan langsung "API lambat -> tambah server". Gunakan skill `performance-investigation`.
