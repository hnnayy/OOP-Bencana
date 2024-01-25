import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

class Bencana:
    def __init__(self, nama, lokasi, tanggal):
        self.__nama = nama  # private
        self._lokasi = lokasi  # protected
        self.tanggal = datetime.now()  # public
        self.korban_meninggal_laki = 0
        self.korban_meninggal_perempuan = 0
        self.korban_terluka_laki = 0
        self.korban_terluka_perempuan = 0
        self.kerusakan = ""

    def tambah_korban_meninggal(self, jumlah, jenis_kelamin="Laki-laki"):
        if jenis_kelamin.lower() == "laki-laki":
            self.korban_meninggal_laki += jumlah
        elif jenis_kelamin.lower() == "perempuan":
            self.korban_meninggal_perempuan += jumlah

    def tambah_korban_terluka(self, jumlah, jenis_kelamin="Laki-laki"):
        if jenis_kelamin.lower() == "laki-laki":
            self.korban_terluka_laki += jumlah
        elif jenis_kelamin.lower() == "perempuan":
            self.korban_terluka_perempuan += jumlah

    def tambah_korban(self, jumlah, jenis_kelamin="Laki-laki", jenis_kecelakaan=None): #polimorfi
        if jenis_kecelakaan is not None:
            print(f"Tambahan korban dari kelas Bencana: {jumlah} {jenis_kelamin} pada kecelakaan {jenis_kecelakaan}")
        else:
            print(f"Tambahan korban dari kelas Bencana: {jumlah} {jenis_kelamin}")

    def total_korban(self):
        korban_meninggal = np.array([self.korban_meninggal_laki, self.korban_meninggal_perempuan])
        korban_terluka = np.array([self.korban_terluka_laki, self.korban_terluka_perempuan])

        return np.sum([korban_meninggal, korban_terluka])

    def persentase_kerusakan(self):
        total_korban = self.total_korban()
        if total_korban > 0:
            persentase = (len(self.kerusakan) / total_korban) * 100 #length fungsi
            return f"{persentase:.2f}% kerusakan pada wilayah bencana. Detail kerusakan belum diketahui"
        else:
            return "Tidak ada informasi kerusakan."

    def info_kerusakan(self, persentase_kerusakan):
        self.kerusakan = f"{persentase_kerusakan:.2f}% kerusakan pada wilayah bencana.  Detail kerusakan belum diketahui"

    def info_bencana(self):
        return {
            "Nama": self.__nama,
            "Lokasi": self._lokasi,
            "Tanggal": self.tanggal.strftime("%Y-%m-%d %H:%M:%S"),
            "Korban Meninggal Laki-laki": self.korban_meninggal_laki,
            "Korban Meninggal Perempuan": self.korban_meninggal_perempuan,
            "Korban Terluka Laki-laki": self.korban_terluka_laki,
            "Korban Terluka Perempuan": self.korban_terluka_perempuan,
            "Kerusakan": self.kerusakan
        }

    def bantuan_korban(self, bantuan):
        if self.total_korban() > 0:
            print(f"Bantuan {bantuan.jenis} sedang diberikan kepada korban bencana.")
        else:
            print("Tidak ada korban. Kerusakan harus segera diperbaiki.")

    def tanggapan_pemerintah(self):
        print("Pemerintah setempat langsung memberikan bantuan kepada para korban bencana.")

    def buat_posko(self, posko):
        print(f"Posko bencana {posko._Bencana__nama} telah didirikan di {posko._lokasi} untuk koordinasi dan penanganan.")

    def tambah_info(self, **kwargs): #key argument fungsi
        informasi = self.info_bencana()
        for key, value in kwargs.items():
            informasi[key] = value
        return informasi

    def ubah_nama_bencana(self):
        while True:
            nama_baru = input("Masukkan nama bencana baru (atau ketik 'selesai' jika tidak ingin mengubah): ")
            if nama_baru.lower() == 'selesai':
                break
            self.__nama = nama_baru
            print(f"Nama bencana berhasil diubah menjadi '{nama_baru}'.")

    def simpan_file(self, nama_file):
        columns = [
            "Nama",
            "Lokasi",
            "Tanggal",
            "Korban Meninggal Laki-laki",
            "Korban Meninggal Perempuan",
            "Korban Terluka Laki-laki",
            "Korban Terluka Perempuan",
            "Persentase Kerusakan"
        ]
        data = [self.info_bencana()]
        df = pd.DataFrame(data, columns=columns)

        if self.kerusakan:  # Periksa apakah ada informasi kerusakan
            persentase_kerusakan = float(self.kerusakan.split('%')[0])
        else:
            persentase_kerusakan = 0.0

        df.at[0, 'Persentase Kerusakan'] = persentase_kerusakan

        tabulasi_data = tabulate(df, headers='keys', tablefmt='plain')
        with open(nama_file, 'w') as file:
            file.write(tabulasi_data)


    def visualisasi(self):
        data = {
            'Korban Meninggal': [self.korban_meninggal_laki, self.korban_meninggal_perempuan],
            'Korban Terluka': [self.korban_terluka_laki, self.korban_terluka_perempuan]
        }

        df_visualize = pd.DataFrame(data, index=['Laki-laki', 'Perempuan'])
        df_visualize.plot(kind='bar', stacked=True)
        plt.title('Visualisasi Data Bencana Gempa Bumi')
        plt.xlabel('Jenis Kelamin')
        plt.ylabel('Jumlah')
        plt.show()

        sns.set_theme(style="whitegrid")

        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=df_visualize.index, y='Korban Meninggal', data=df_visualize, label='Meninggal', s=100)
        sns.scatterplot(x=df_visualize.index, y='Korban Terluka', data=df_visualize, label='Terluka', s=100, marker='X')

        plt.title('Visualisasi Data Bencana Gempa Bumi')
        plt.xlabel('Jenis Kelamin')
        plt.ylabel('Jumlah')
        plt.legend()
        plt.show()

class BantuanKorban(Bencana):
    def __init__(self, jenis, jumlah):
        super().__init__("Default", "Default", "Default")
        self.jenis = jenis
        self.jumlah = jumlah

class Posko(Bencana):
    def __init__(self, nama, lokasi):
        super().__init__("Default", "Default", "Default")
        self.__nama = nama
        self._lokasi = lokasi

    def tambah_korban(self, jumlah, jenis_kelamin="Laki-laki", jenis_kecelakaan=None):
        info_korban = f"Tambahan korban dari kelas Posko: {jumlah} {jenis_kelamin}"
        if jenis_kecelakaan is not None:
            info_korban += f" pada kecelakaan {jenis_kecelakaan}"
        print(info_korban)

    def tambah_info_posko(self, info):
        print(f"Informasi Posko: {info}")

# Penggunaan kelas dan metode
bencana_gempa = Bencana("Gempa Bumi", "Pesisir Selatan", "12 November 2023")
bencana_gempa.tambah_korban_meninggal(5, jenis_kelamin="Laki-laki")
bencana_gempa.tambah_korban_meninggal(5, jenis_kelamin="Perempuan")

bencana_gempa.tambah_korban_terluka(12, jenis_kelamin="Laki-laki")
bencana_gempa.tambah_korban_terluka(8, jenis_kelamin="Perempuan")

bencana_obj = Bencana("Gempa Bumi", "Pesisir Selatan", "12 November 2023")
bencana_obj.tambah_korban(5, jenis_kelamin="Laki-laki", jenis_kecelakaan="Gempa")

print("Info Bencana Sebelum Perubahan Nama:")
print(bencana_gempa.info_bencana())

bencana_gempa.ubah_nama_bencana()

print("Info Bencana Setelah Perubahan Nama:")
print(bencana_gempa.info_bencana())

print("Total Korban:", bencana_gempa.total_korban())
print("Total Kerusakan:", bencana_gempa.persentase_kerusakan())

bencana_gempa.info_kerusakan(35.0)
bencana_gempa.simpan_file("bencana.csv")

print("Info Bencana:")
print(bencana_gempa.info_bencana())

bantuan_makanan = BantuanKorban("Makanan", 500)
bencana_gempa.bantuan_korban(bantuan_makanan)

bencana_gempa.tanggapan_pemerintah()
info_tambahan = {'Status': 'Sedang Ditangani', 'Evakuasi': 'Sudah Dilakukan'}
informasi_lengkap = bencana_gempa.tambah_info(**info_tambahan)

print("Informasi Bencana Lengkap:")
for key, value in informasi_lengkap.items():
    print(f"{key}: {value}")

posko_gempa = Posko("Posko Gempa", "Lapangan dan Masjid Terdekat yang tidak terkena dampak")
bencana_gempa.buat_posko(posko_gempa)

# Penggunaan overloading
posko_gempa.tambah_korban(3, jenis_kelamin="Laki-laki", jenis_kecelakaan="Banjir")
posko_gempa.tambah_korban(2, jenis_kelamin="Perempuan")

bencana_gempa.visualisasi()
