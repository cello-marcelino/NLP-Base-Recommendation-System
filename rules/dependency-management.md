# Dependency Management

Aturan pengelolaan dependency atau library eksternal. Berlaku saat menambah atau update package.

---

- **Python Virtual Environment**: Pada proyek Python, selalu gunakan virtual environment (`venv`, `poetry`, `uv`, atau `pipenv`) untuk mengisolasi dependensi. Dilarang menginstal package langsung ke environment global sistem.
- Hindari dependency yang tidak digunakan
- Lock dependency version di production (misal: `requirements.txt`, `poetry.lock`, `Pipfile.lock`, atau `uv.lock`)
- Review dependency sebelum ditambahkan
- Update dependency secara berkala
- Monitor known security vulnerability
- Jangan menambahkan library untuk masalah yang bisa diselesaikan sederhana dengan standard library
