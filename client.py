from xmlrpc.client import ServerProxy
from datetime import datetime

def main():
    server = ServerProxy('http://localhost:8000')

    while True:
        print("\nMenu:")
        print("1. Daftar Poli")
        print("2. Lihat Antrian di Poli")
        print("3. Mendaftar di Poli")
        print("4. Lihat Data Pasien")
        print("0. Keluar")

        choice = input("Pilih menu (0-4): ")

        if choice == '0':
            break
        elif choice == '1':
            try:
                klinik_list = server.daftar_poli()
                print("Daftar Poli di Telkomedika:")
                for i, klinik in enumerate(klinik_list, 1):
                    print(f"{i}. {klinik}")
            except Exception as e:
                print(f"Terjadi kesalahan: {e}")
        elif choice == '2':
            try:
                klinik = input("Masukkan nama poli: ")
                antrian = server.daftar_antrian(klinik)
                waktu_tunggu = server.daftar_waktu_tunggu(klinik)
                if not antrian:
                    print(f'Tidak ada antrian di {klinik}')
                else:
                    print(f'Antrian {klinik}:\n{antrian}\nWaktu Tunggu: {waktu_tunggu} menit')
            except Exception as e:
                print(f"Terjadi kesalahan: {e}")
        elif choice == '3':
            try:
                klinik_list = server.daftar_poli()
                for i, klinik in enumerate(klinik_list, 1):
                    print(f"{i}. {klinik}")
                nama_poli = input("Masukkan nama klinik: ")
                nomor_rekam_medis = input("Masukkan nomor rekam medis: ")
                nama = input("Masukkan nama: ")
                while True:
                    try:
                        tanggal_lahir = input("Masukkan tanggal lahir (YYYY-MM-DD): ")
                        datetime.strptime(tanggal_lahir, '%Y-%m-%d')
                        break 
                    except ValueError:
                        print("Format tanggal salah. Coba lagi.")

                nomor_antrean, waktu_tunggu = server.tambah_antrian(nama_poli, {'nomor_rekam_medis': nomor_rekam_medis, 'nama': nama, 'tanggal_lahir': tanggal_lahir})
                print(f'Anda telah mendaftar di {nama_poli}. Nomor Antrean: {nomor_antrean}\nPerkiraan waktu tunggu: {waktu_tunggu} menit')
            except Exception as e:
                print(f"Terjadi kesalahan: {e}")
        elif choice == '4':
            try:
                klinik = input("Masukkan Nama poli: ")
                nomor_antrean = int(input("Masukkan Nama antrean: "))
                pasien_data = server.lihat_data_pasien(klinik, nomor_antrean)
                print(f'Data Pasien:\n{pasien_data}')
            except Exception as e:
                print(f"Terjadi kesalahan: {e}")
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
