# Testing

Aturan level testing dan kualitas test. Berlaku saat menulis atau mengubah test.

---

## Level
```
Unit Test -> Integration Test -> API Test -> End-to-End Test -> Load Test
```

Rules:
- Business logic penting wajib punya unit test
- Database interaction penting wajib punya integration test
- Critical API wajib punya API test
- Bug yang sudah ditemukan sebaiknya punya regression test
- Jangan hapus test hanya supaya build menjadi hijau
- Test harus deterministic

## Kualitas Test
Uji behavior, bukan implementation detail.
```
given input -> execute behavior -> verify expected result
```
Hindari test yang terlalu bergantung pada struktur internal class kalau behavior bisa diuji lewat public interface.

Gunakan skill `write-tests`.
