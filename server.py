from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class KlinikTelkomedika:
    def __init__(self):
        self.klinik_data = {
            'Poli_Gigi': {'antrian': [], 'waktu_tunggu': 0},
            'Poli_Umum': {'antrian': [], 'waktu_tunggu': 0},
            'Poli_THT': {'antrian': [], 'waktu_tunggu': 0},
        }

    def daftar_poli(self):
        return list(self.klinik_data.keys())

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

# Akses RPC hanya untuk localhost
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

def main():
    server = SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler)
    server.register_introspection_functions()

    rumah_sakit = KlinikTelkomedika()
    server.register_instance(rumah_sakit)

    print("Server sedang berjalan...")
    server.serve_forever()

if __name__ == "__main__":
    main()
