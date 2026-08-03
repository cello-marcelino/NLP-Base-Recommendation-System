FROM python:3.9-slim

WORKDIR /app

# Build argument: 'cpu' (default) atau 'gpu'
ARG DEVICE=cpu

# Install dependencies (termasuk C++ build tools jika dibutuhkan oleh library NLP)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 1. Install PyTorch sesuai target perangkat
# - Default (CPU): Mengunduh PyTorch CPU-Only (~180 MB) hemat memori & kuota
# - Opsional (GPU): Mengunduh PyTorch lengkap dengan CUDA
RUN if [ "$DEVICE" = "gpu" ]; then \
        echo "Menyiapkan PyTorch dengan dukungan GPU CUDA..." && \
        pip install --no-cache-dir torch ; \
    else \
        echo "Menyiapkan PyTorch CPU-Only (Default Ringan)..." && \
        pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu ; \
    fi

# 2. Install library pendukung lainnya
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh kode server
COPY . .

# Membuat direktori storage jika belum ada
RUN mkdir -p /app/storage/cache /app/storage/data

EXPOSE 5000

# Menjalankan server Flask
CMD ["python", "run.py"]
