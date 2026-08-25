---
name: performance-investigation
description: Gunakan skill ini ketika user melaporkan sesuatu terasa lambat, atau minta optimasi performance.
---

# Performance Investigation

## Langkah
1. Correctness dulu: pastikan behavior sudah benar sebelum dioptimasi
2. Profiling: ukur response time, query count, CPU/memory usage untuk menemukan bottleneck nyata
3. Identify bottleneck: cari root cause spesifik, jangan menebak, contoh EXPLAIN query kalau dicurigai database
4. Optimize: perbaiki bagian yang jadi bottleneck saja
5. Measure again: bandingkan angka sebelum dan sesudah perubahan

## Larangan
Jangan langsung menambah server/instance atau cache tanpa data yang menunjukkan itu solusinya, lihat `rules/scalability-performance.md`.
