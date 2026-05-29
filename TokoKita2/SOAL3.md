## Modifikasi Aplikasi Backend (main.py)
Ubah main.py pada seluruh backend agar memiliki 2 endpoint baru untuk mensimulasikan beban yang tidak seimbang. Tambahkan routing berikut di bagian bawah sebelum if __name__ == "__main__": pada backend1/main.py dan backend2/main.py:  

```py
# Endpoint Ringan
@app.route("/catalogue", methods=["GET"])
def catalogue():
    """Ringan. Hanya mengembalikan JSON data produk[cite: 126]."""
    return jsonify(PRODUCTS)

# Endpoint Sangat Berat
@app.route("/checkout", methods=["POST"])
def checkout():
    """Sangat Berat. Lakukan perulangan komputasi matematika kompleks (mencari bilangan prima hingga ke-10.000)[cite: 126]."""
    primes = []
    for possiblePrime in range(2, 10000):
        is_prime = True
        for num in range(2, int(possiblePrime ** 0.5) + 1):
            if possiblePrime % num == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(possiblePrime)
            
    return jsonify({"status": "success", "message": "Checkout complete"})
```

## Restriksi Resource pada Docker Compose
Tambahkan konfigurasi deploy.resources pada docker-compose.yml untuk setiap service backend agar maksimal hanya bisa menggunakan 0.5 CPU dan 128M Memory. Ubah docker-compose.yml menjadi seperti ini:

```yml
version: "3.8"

services:
  backend1:
    build: ./backend1
    ports:
      - "5001:5000"
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 128M

  backend2:
    build: ./backend2
    ports:
      - "5002:5000"
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 128M

  nginx:
    build: ./nginx
    ports:
      - "80:80"
    depends_on:
      - backend1
      - backend2
```

## Pembuatan Locust Script
Buat file locustfile.py  di dalam folder utama (TokoKita) sejajar dengan docker-compose.yml. Implementasikan User Behavior dengan weighting: 80% aktivitas user melihat barang (/catalogue) dan 20% melakukan pembelian (/checkout). Set wait time secara dinamis antara 1 sampai 3 detik.

```py
from locust import HttpUser, task, between

class FlashSaleUser(HttpUser):
    wait_time = between(1, 3)

    @task(8)
    def view_catalogue(self):
        self.client.get("/catalogue")

    @task(2)
    def checkout(self):
        self.client.post("/checkout")
```

sudah menginstall Locust: `pip install locust`

## Eksekusi Pengujian: Tahap 1
Pastikan NGINX menggunakan algoritma Round Robin biasa (tanpa weight).
Jalankan Locust di localhost:8089.
Lakukan pengujian dengan parameter ekstrem:
- Number of users: 500
- Spawn rate: 20 users/second
- Durasi: Biarkan berjalan tepat 3 menit.
Download laporan CSV dari Locust (Requests, Failures, dan Exceptions).

### Langkah-langkah
1. Buka nginx/nginx.conf dan pastikan NGINX menggunakan algoritma Round Robin biasa (tanpa weight). Ubah blok upstream menjadi:

```sh
upstream app {
    server backend1:5000;
    server backend2:5000;
}
```

2. Karena kamu menjalankan proyek ini di environment user khusus, pastikan kamu berada di direktori zika yang tepat saat menjalankan perintah Docker. Matikan servis lama (jika ada) dan build ulang container-nya:

```sh
docker-compose down
docker-compose up --build -d
```

3. Jalankan Locust di terminal lokalmu: `locust -f locustfile.py`

4. Buka browser dan akses http://localhost:8089. Lakukan pengujian dengan parameter ekstrem: Number of users: 500, Spawn rate: 20 users/second, dan biarkan berjalan tepat 3 menit.

5. Setelah 3 menit, hentikan test dan download laporan CSV dari Locust (Requests, Failures, dan Exceptions).

## Eksekusi Pengujian: Tahap 2
Matikan sistem. Ubah konfigurasi NGINX agar menggunakan algoritma dinamis Least Connection (least_conn;).
Jalankan ulang Docker Compose.
Lakukan pengujian Locust dengan parameter yang sama persis seperti Tahap 1 selama 3 menit.
Download kembali laporan CSV-nya.

### Langkah-langkah

1. Matikan sistem Docker kamu terlebih dahulu dengan perintah docker-compose down di terminal.

2. Ubah konfigurasi NGINX agar menggunakan algoritma dinamis Least Connection (least_conn). Buka nginx/nginx.conf dan ubah menjadi:

```
upstream app {
    least_conn;
    server backend1:5000;
    server backend2:5000;
}
```

3. Jalankan ulang Docker Compose dengan docker-compose up --build -d.

4. Lakukan pengujian Locust dengan parameter yang sama persis seperti Tahap 1 selama 3 menit, lalu download kembali laporan CSV-nya.
