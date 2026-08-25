# CI/CD

Aturan pipeline CI/CD. Berlaku saat mengubah workflow deployment.

---

Setiap perubahan yang masuk ke branch utama wajib lewat automated validation:
```
Push -> Lint -> Test -> Build -> Security Check -> Deploy
```
Deployment manual boleh dipakai untuk environment tertentu, tapi production deployment sebaiknya reproducible dan automated kalau maturity sistem sudah memadai.
