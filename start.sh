#!/bin/bash

# Pastikan file .env ada
if [ ! -f .env ]; then
  echo "Error: File .env tidak ditemukan. Pastikan file .env tersedia."
  exit 1
fi

# Buat dan aktifkan virtual environment
if [ ! -d "venv" ]; then
  echo "Membuat virtual environment..."
  python3 -m venv venv
fi

echo "Mengaktifkan virtual environment..."
source venv/bin/activate

# Instal semua dependensi yang diperlukan
echo "Memasang dependensi Python..."
pip install -r requirements.txt

# Menjalankan aplikasi Flask
echo "Menjalankan aplikasi Flask..."
python app.py
