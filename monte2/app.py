from flask import Flask, render_template, url_for
import random
import math
import mysql.connector  # Pastikan library ini diinstal

# Konfigurasi database
db_config = {
    'user': 'root',
    'password': '',  # Ganti dengan password MySQL Anda
    'host': 'localhost',
    'database': 'smk_pendaftaran',
}

# Fungsi untuk mengambil data dari database
def fetch_data():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    query = "SELECT tahun, jumlah FROM daftar ORDER BY tahun ASC"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

# Fungsi untuk menghitung probabilitas, kumulatif, dan interval
def calculate_interval(data):
    total = sum(row['jumlah'] for row in data)
    kumulatif = 0
    interval_data = []
    
    for row in data:
        probabilitas = row['jumlah'] / total
        kumulatif += probabilitas
        interval = f"{math.ceil((kumulatif - probabilitas) * 1000)} - {math.floor(kumulatif * 1000)}"
        interval_data.append({
            'tahun': row['tahun'],
            'jumlah_pendaftar': row['jumlah'],
            'probabilitas': round(probabilitas, 4),
            'kumulatif': round(kumulatif, 4),
            'interval': interval
        })
    
    return interval_data

# Fungsi untuk menghasilkan bilangan acak menggunakan LCG
def generate_random_numbers(count, a=1103515245, c=12345, m=2**31):
    zi = random.randint(0, m - 1)  # Nilai awal (seed)
    lcg_data = []
    
    for _ in range(count):
        a_zi_c = a * zi + c
        mod_result = a_zi_c % m
        three_digit = mod_result % 1000
        lcg_data.append({
            'zi': zi,
            'a_zi_c': a_zi_c,
            'mod_result': mod_result,
            'three_digit': three_digit
        })
        zi = mod_result  # Update nilai Zi
    
    return lcg_data

# Fungsi untuk memprediksi pendaftaran berdasarkan bilangan acak dan interval
def predict_registration(interval_data, random_numbers):
    hasil_prediksi = []
    tahun_awal = interval_data[-1]['tahun'] + 1
    
    for i, rand in enumerate(random_numbers):
        prediksi = None
        for interval in interval_data:
            min_interval, max_interval = map(int, interval['interval'].split(" - "))
            if min_interval <= rand['three_digit'] <= max_interval:
                prediksi = interval['jumlah_pendaftar']
                break
        
        hasil_prediksi.append({
            'tahun': tahun_awal + i,
            'jumlah_calon_peserta': prediksi
        })
    
    return hasil_prediksi

# Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tentang_saya")
def tentang_saya():
    return render_template("tentang_saya.html")

@app.route("/bilangan_sebelumnya")
def bilangan_sebelumnya():
    data_sebelumnya = fetch_data()
    return render_template("bilangan_sebelumnya.html", data_sebelumnya=data_sebelumnya)

@app.route("/monte2")
def monte_carlo():
    data_sebelumnya = fetch_data()
    
    # Hitung interval data
    interval_data = calculate_interval(data_sebelumnya)
    
    # Generate bilangan acak
    lcg_data = generate_random_numbers(5)  # Misalnya, 5 tahun prediksi
    
    # Prediksi pendaftaran
    hasil_prediksi = predict_registration(interval_data, lcg_data)
    
    return render_template(
        "monte2.html",
        interval_data=interval_data,
        lcg_data=lcg_data,
        hasil_prediksi=hasil_prediksi
    )

if __name__ == "__main__":
    app.run(debug=True)
