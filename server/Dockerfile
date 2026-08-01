FROM python:3.9-slim

WORKDIR /app

# Install dependencies (termasuk C++ build tools jika dibutuhkan oleh library NLP)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh kode server
COPY . .

# Membuat direktori storage jika belum ada
RUN mkdir -p /app/storage/cache /app/storage/data

EXPOSE 5000

# Menjalankan server Flask
CMD ["python", "run.py"]
