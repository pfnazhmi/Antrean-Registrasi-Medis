import tkinter as tk
from tkinter import messagebox, simpledialog
from xmlrpc.client import ServerProxy

class AntreanMedisGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Antrean Medis Telkomedika")


        self.server = ServerProxy('http://localhost:8000')
        self.selected_klinik = tk.StringVar(self.master)

        self.create_widgets()

    def create_widgets(self):
        self.font_style = ("Poppins", 12)
        button_style = {'padx': 10, 'pady': 5, 'font': self.font_style}

        self.label = tk.Label(
            self.master, text="Selamat Datang di Antrean Medis Telkomedika", 
            font=self.font_style)
        self.label.pack(pady=10)

        self.button_poli = tk.Button(
            self.master, text="Lihat Poli", 
            command=self.lihat_poli, 
            **button_style)
        self.button_poli.pack()

        self.label_klinik = tk.Label(
            self.master, text="Pilih Klinik:", 
            font=self.font_style)
        self.label_klinik.pack()

        klinik_list = self.server.lihat_poli()
        self.selected_klinik.set(klinik_list[0])

        self.option_menu_klinik = tk.OptionMenu(
            self.master, 
            self.selected_klinik, 
            *klinik_list)
        self.option_menu_klinik.config(font=self.font_style)
        self.option_menu_klinik.pack()
        self.label.pack(pady=10)

        self.button_lihat_antrian = tk.Button(
            self.master, text="Lihat Antrian", 
            command=self.lihat_antrian,
            **button_style)
        self.button_lihat_antrian.pack()

        self.button_mendaftar = tk.Button(
            self.master, text="Mendaftar", 
            command=self.mendaftar, 
            **button_style)
        self.button_mendaftar.pack()

        self.button_lihat_data = tk.Button(
            self.master, text="Lihat Data Pasien", 
            command=self.lihat_data,
            **button_style)
        self.button_lihat_data.pack()

        self.button_exit = tk.Button(
            self.master, text="Keluar", 
            command=self.master.destroy, 
            bg='red', fg='white',
            **button_style)
        self.button_exit.pack(pady=10)

    def lihat_poli(self):
        try:
            klinik_list = self.server.lihat_poli()
            poli_str = "\n".join([f"{i}. {klinik}" for i, klinik in enumerate(klinik_list, 1)])
            messagebox.showinfo("Daftar Poli", f"Daftar Poli di Telkomedika:\n{poli_str}")
        except Exception as e:
            messagebox.showerror("Kesalahan", f"Terjadi kesalahan: {e}")

    def lihat_antrian(self):
        klinik = self.selected_klinik.get()
        if klinik:
            try:
                antrian = self.server.daftar_antrian(klinik)
                waktu_tunggu = self.server.daftar_waktu_tunggu(klinik)
                if not antrian:
                    messagebox.showinfo("Antrian", f'Tidak ada antrian di {klinik}')
                else:
                    antrian_str = "\n".join([f"{data['nomor_antrean']}. {data['pasien']['nama']}" for data in antrian])
                    messagebox.showinfo("Antrian", f'Antrian {klinik}:\n{antrian_str}\nWaktu Tunggu: {waktu_tunggu} menit')
            except Exception as e:
                messagebox.showerror("Kesalahan", f"Terjadi kesalahan: {e}")

    def mendaftar(self):
        try:
            klinik_list = self.server.lihat_poli()
            klinik = simpledialog.askstring("Pilih Klinik", "Pilih klinik:", initialvalue=klinik_list[0], parent=self.master)
            if klinik:
                nomor_rekam_medis = simpledialog.askstring("Nomor Rekam Medis", "Masukkan nomor rekam medis:")
                nama = simpledialog.askstring("Nama", "Masukkan nama:")
                tanggal_lahir = simpledialog.askstring("Tanggal Lahir", "Masukkan tanggal lahir (YYYY-MM-DD):")

                if nomor_rekam_medis and nama and tanggal_lahir:
                    nomor_antrean, waktu_tunggu = self.server.tambah_antrian(
                        klinik,
                        {'nomor_rekam_medis': nomor_rekam_medis, 'nama': nama, 'tanggal_lahir': tanggal_lahir}
                    )
                    messagebox.showinfo("Mendaftar", f'Anda telah mendaftar di {klinik}. Nomor Antrean: {nomor_antrean}\nPerkiraan waktu tunggu: {waktu_tunggu} menit')
        except Exception as e:
            messagebox.showerror("Kesalahan", f"Terjadi kesalahan: {e}")

    def lihat_data(self):
        klinik = self.selected_klinik.get()
        nomor_antrean = simpledialog.askinteger("Masukkan Nomor Antrean", "Masukkan nomor antrean:")

        if klinik and nomor_antrean:
            try:
                pasien_data = self.server.lihat_data_pasien(klinik, nomor_antrean)
                messagebox.showinfo("Data Pasien", f'Data Pasien:\n{pasien_data}')
            except Exception as e:
                messagebox.showerror("Kesalahan", f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AntreanMedisGUI(root)
    root.mainloop()
