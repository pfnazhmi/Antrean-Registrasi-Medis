# import tkinter, xmlrpc, dan datetime
import tkinter as tk
from tkinter import messagebox, simpledialog
from xmlrpc.client import ServerProxy
from datetime import datetime

# membuat class Antrean Medis GUI
class AntreanMedisGUI:
    def __init__(self, master):
        # membuat atribut kelas 
        self.master = master
        self.master.title("Antrean Medis Telkomedika")

        # self.server = ServerProxy('http://192.168.18.87:8000')
        # self.selected_klinik = tk.StringVar(self.master)
        self.server = ServerProxy('http://localhost:8000')
        self.selected_klinik = tk.StringVar(self.master)

        self.create_widgets()

    def create_widgets(self):
        # membuat widget yang diperlukan
        self.font_style = ("Poppins", 12)
        button_style = {'padx': 10, 'pady': 5, 'font': self.font_style}

        # membuat label
        self.label = tk.Label(
            self.master, text="Selamat Datang di Antrean Medis Telkomedika", 
            font=self.font_style)
        self.label.pack(pady=10)

        # membuat button lihat poli
        self.button_poli = tk.Button(
            self.master, text="Lihat Poli", 
            command=self.lihat_poli, 
            **button_style)
        self.button_poli.pack()

        # membuat label
        self.label_klinik = tk.Label(
            self.master, text="Pilih Klinik:", 
            font=self.font_style)
        self.label_klinik.pack()

        # menginisiasi list klinik dan selected klinik
        klinik_list = [f"{klinik} ({status})" for klinik, status in self.server.lihat_poli()]
        self.selected_klinik.set(klinik_list[0])

        # membuat option menu klinik yang akan dipilih
        self.option_menu_klinik = tk.OptionMenu(
            self.master, 
            self.selected_klinik, 
            *klinik_list)
        self.option_menu_klinik.config(font=self.font_style)
        self.option_menu_klinik.pack(pady=10)

        # membuat button lihat antrian
        self.button_lihat_antrian = tk.Button(
            self.master, text="Lihat Antrian", 
            command=self.lihat_antrian,
            **button_style)
        self.button_lihat_antrian.pack(pady=5)

        # membuat button mendaftar
        self.button_mendaftar = tk.Button(
            self.master, text="Mendaftar", 
            command=self.mendaftar, 
            **button_style)
        self.button_mendaftar.pack(padx=5)

        # membuat button lihat data pasien
        self.button_lihat_data = tk.Button(
            self.master, text="Lihat Data Pasien", 
            command=self.lihat_data,
            **button_style)
        self.button_lihat_data.pack(padx=5)

        # membuat button keluar program
        self.button_exit = tk.Button(
            self.master, text="Keluar", 
            command=self.master.destroy, 
            bg='red', fg='white',
            **button_style)
        self.button_exit.pack(pady=10)

    def lihat_poli(self):
        # menampilkan data dari method lihat_poli dari server
        try:
            klinik_info = self.server.lihat_poli()
            poli_str = "\n".join([f"{klinik}: {status}" for klinik, status in klinik_info])
            messagebox.showinfo("Info Poli", f"Informasi Poli di Telkomedika:\n{poli_str}")
        except Exception as e:
            messagebox.showerror("Kesalahan", f"Terjadi kesalahan: {e}")

    def lihat_antrian(self):
        # menampilkan method daftar_antrian dari server
        klinik = self.selected_klinik.get()
        clinic_name = klinik.split(' (')[0]
        status = klinik.split(' (')[1].rstrip(')')
        if clinic_name and status == 'Buka':
            try:
                antrian = self.server.daftar_antrian(clinic_name)
                waktu_tunggu = self.server.daftar_waktu_tunggu(clinic_name)
                if not antrian:
                    messagebox.showinfo("Antrian", f'Tidak ada antrian di {clinic_name}')
                else:
                    antrian_str = "\n".join([f"{data['nomor_antrean']}. {data['pasien']['nama']}" for data in antrian])
                    messagebox.showinfo("Antrian", f'Antrian {clinic_name}:\n{antrian_str}\nWaktu Tunggu: {waktu_tunggu} menit')
            except Exception as e:
                messagebox.showerror("Kesalahan", f"Terjadi kesalahan: {e}")
        else:
            messagebox.showerror("Antrian", f'Klinik sudah tutup')

    def mendaftar(self):
        # menjalankan method tambah_antrian dari server
        try:
            klinik = self.selected_klinik.get()
            clinic_name = klinik.split(' (')[0]
            status = klinik.split(' (')[1].rstrip(')')
            if status == 'Tutup' :
                messagebox.showerror("Mendaftar", f'Klinik Sudah Tutup')
            elif klinik and status == 'Buka':
                nomor_rekam_medis = simpledialog.askstring("Nomor Rekam Medis", "Masukkan nomor rekam medis:")
                nama = simpledialog.askstring("Nama", "Masukkan nama:")
                tanggal_lahir = simpledialog.askstring("Tanggal Lahir", "Masukkan tanggal lahir (YYYY-MM-DD):")

                if nomor_rekam_medis and nama and tanggal_lahir:
                    nomor_antrean, waktu_tunggu = self.server.tambah_antrian(
                        clinic_name,
                        {'nomor_rekam_medis': nomor_rekam_medis, 'nama': nama, 'tanggal_lahir': datetime.strptime(tanggal_lahir, '%Y-%m-%d')})
                    
                    messagebox.showinfo("Mendaftar", f'Anda telah mendaftar di {clinic_name}. Nomor Antrean: {nomor_antrean}\nPerkiraan waktu tunggu: {waktu_tunggu} menit')   

        except Exception as e:
            messagebox.showerror("Kesalahan", f"Terjadi kesalahan: {e}")

    def lihat_data(self):
        # menampilkan method lihat data pasien dari server
        klinik = self.selected_klinik.get()
        clinic_name = klinik.split(' (')[0]
        status = klinik.split(' (')[1].rstrip(')')

        if status == 'Tutup':
            messagebox.showerror("Mendaftar", f'Klinik Sudah Tutup')
        elif clinic_name and status =='Buka':
            nomor_antrean = simpledialog.askinteger("Masukkan Nomor Antrean", "Masukkan nomor antrean:")
            if nomor_antrean:
                try:
                    pasien_data = self.server.lihat_data_pasien(clinic_name, nomor_antrean)
                    messagebox.showinfo("Data Pasien", f'Data Pasien:\n{pasien_data}')
                except Exception as e:
                    messagebox.showerror("Kesalahan", f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AntreanMedisGUI(root)
    root.mainloop()