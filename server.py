#untuk membuat server XML-RPC.
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading
from datetime import datetime

#untuk menentukan jalur permintaan yang diizinkan.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class ServerThread(threading.Thread):
    #Konstruktor menerima objek server sebagai parameter dan menyimpan objek server 
    def __init__(self, server):
        threading.Thread.__init__(self)
        self.server = server

    #Override dari metode run pada kelas induk (Thread) dan menampilkan pesan bahwa server sedang berjalan memulai server XML-RPC dengan memanggil serve_forever pada objek server.
    def run(self):
        print("Server sedang berjalan...")
        self.server.serve_forever()

# kelas yang merepresentasikan sebuah klinik dengan data terkait
class KlinikTelkomedika:

    #Inisialisasi klinik_data sebagai kamus (dictionary) yang berisi informasi poli-poli di klinik
    def __init__(self):
        self.klinik_data = {
            'Poli Gigi': {'antrian': [], 'waktu_tunggu': 0,'buka_jam': datetime.strptime('08:00', '%H:%M'), 'tutup_jam': datetime.strptime('16:00', '%H:%M')},
            'Poli Umum': {'antrian': [], 'waktu_tunggu': 0,'buka_jam': datetime.strptime('06:00', '%H:%M'), 'tutup_jam': datetime.strptime('20:00', '%H:%M')},
            'Poli THT': {'antrian': [], 'waktu_tunggu': 0,'buka_jam': datetime.strptime('07:00', '%H:%M'), 'tutup_jam': datetime.strptime('17:00', '%H:%M')},
            'Poli Bidan': {'antrian': [], 'waktu_tunggu': 0,'buka_jam': datetime.strptime('00:00', '%H:%M'), 'tutup_jam': datetime.strptime('23:59', '%H:%M')},
        }

    # method untuk informasi data klinik berupa klinik dan status (buka/tutup)
    def lihat_poli(self):
        poli_info = []
        now = datetime.now().time()

        for klinik, data in self.klinik_data.items():
            buka_jam = data['buka_jam'].time()
            tutup_jam = data['tutup_jam'].time()

            if buka_jam <= now <= tutup_jam:
                status = 'Buka'
            else:
                status = 'Tutup'

            poli_info.append((klinik, status))

        return poli_info

    # method untuk mengembalikan daftar antrian
    def daftar_antrian(self, klinik):
        return self.klinik_data[klinik]['antrian']
    
    # method untuk mengembalikan daftar waktu tunggu
    def daftar_waktu_tunggu(self, klinik):
        return self.klinik_data[klinik]['waktu_tunggu']
    
    # method untuk menambahkan antrian
    def tambah_antrian(self, klinik, pasien):
        nomor_antrean = len(self.klinik_data[klinik]['antrian']) + 1
        self.klinik_data[klinik]['antrian'].append({'nomor_antrean': nomor_antrean, 'pasien': pasien})
        waktu_tunggu = nomor_antrean * 10  # Asumsi setiap pasien butuh 10 menit
        self.klinik_data[klinik]['waktu_tunggu'] = waktu_tunggu
        return nomor_antrean, waktu_tunggu
    
    # method untuk mengembalikan data pasien
    def lihat_data_pasien(self, klinik, nomor_antrean):
        pasien_data = self.klinik_data[klinik]['antrian'][nomor_antrean - 1]['pasien']
        return pasien_data

# menjalankan server
def main():
    #server = SimpleXMLRPCServer(('http://192.168.18.87:8000'), requestHandler=RequestHandler)
    server = SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler)
    server.register_introspection_functions()

    _klinikTelkomedika = KlinikTelkomedika()
    server.register_instance(_klinikTelkomedika)

    server_thread = ServerThread(server)
    server_thread.start()

if __name__ == "__main__":
    main()
