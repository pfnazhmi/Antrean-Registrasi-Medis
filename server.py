from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading
from datetime import datetime

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class ServerThread(threading.Thread):
    def __init__(self, server):
        threading.Thread.__init__(self)
        self.server = server

    def run(self):
        print("Server sedang berjalan...")
        self.server.serve_forever()

class KlinikTelkomedika:
    def __init__(self):
        self.klinik_data = {
            'Poli Gigi': {'antrian': [], 'waktu_tunggu': 0,'buka_jam': datetime.strptime('08:00', '%H:%M'), 'tutup_jam': datetime.strptime('16:00', '%H:%M')},
            'Poli Umum': {'antrian': [], 'waktu_tunggu': 0,'buka_jam': datetime.strptime('06:00', '%H:%M'), 'tutup_jam': datetime.strptime('20:00', '%H:%M')},
            'Poli THT': {'antrian': [], 'waktu_tunggu': 0,'buka_jam': datetime.strptime('07:00', '%H:%M'), 'tutup_jam': datetime.strptime('17:00', '%H:%M')},
        }

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

    def daftar_antrian(self, klinik):
        return self.klinik_data[klinik]['antrian']

    def daftar_waktu_tunggu(self, klinik):
        return self.klinik_data[klinik]['waktu_tunggu']

    def tambah_antrian(self, klinik, pasien):
        nomor_antrean = len(self.klinik_data[klinik]['antrian']) + 1
        self.klinik_data[klinik]['antrian'].append({'nomor_antrean': nomor_antrean, 'pasien': pasien})
        waktu_tunggu = nomor_antrean * 10  # Asumsi setiap pasien butuh 10 menit
        self.klinik_data[klinik]['waktu_tunggu'] = waktu_tunggu
        return nomor_antrean, waktu_tunggu

    def lihat_data_pasien(self, klinik, nomor_antrean):
        pasien_data = self.klinik_data[klinik]['antrian'][nomor_antrean - 1]['pasien']
        return pasien_data

def main():
    server = SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler)
    server.register_introspection_functions()

    rumah_sakit = KlinikTelkomedika()
    server.register_instance(rumah_sakit)

    server_thread = ServerThread(server)
    server_thread.start()

if __name__ == "__main__":
    main()
