import requests

# Penggantian dengan URL yang sesuai
url = "http://localhost:8000/update-user-data"  # Ganti dengan URL yang sesuai

# Data yang akan Anda kirim sebagai permintaan PUT
data = {
    "nama": "dimas",
    "gender": "pria",  # Ganti dengan jenis kelamin yang sesuai
    "ulang_tahun": "1990-01-01"  # Ganti dengan ulang tahun yang sesuai
}

# Header dengan token akses yang sesuai
headers = {
    "Authorization": "Bearer e33f815f-5efb-53f7-db3e-1b8314a776dd"  # Ganti dengan token akses yang sesuai
}

# Mengirim permintaan PUT ke endpoint
response = requests.put(url, json=data, headers=headers)

# Memeriksa respons dari server
if response.status_code == 200:
    print("Data berhasil diperbarui:", response.json())
elif response.status_code == 401:
    print("Token akses kadaluarsa atau tidak valid.")
elif response.status_code == 404:
    print("Data pengguna tidak ditemukan.")
else:
    print("Terjadi kesalahan:", response.status_code, response.text)
