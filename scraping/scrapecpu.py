from bs4 import BeautifulSoup
import requests
import json
from tqdm import tqdm

url = "https://thesystemone.com/processor"

# Membuat class data yang fungsinya untuk membuat processor menjadi satu objek
class data_part:
    def __init__(self, nama_part):
        self.nama_part = nama_part

#     def print_objek(self):
#         print(f'''
#             Judul Drama: {self.judul_drama}
#             Jenis Drama: {self.jenis_drama}
#             Tahun Pembuatan: {self.tahun_pembuatan}
#             Jumlah Episode: {self.jumlah_episode}
#             Rating Drama: {self.rating_drama}
#         ''')

# Membuat sebuah array untuk menampung objek processor
list_part = []

halaman = 1

# for page in range(1,6):
#     page = requests.get(url+"?page="+str(halaman))
#     halaman += 1
#     print(page)

for page in range(1, 7):
    print ('Scrapping Halaman : ', halaman)
    page = requests.get(url+"?page="+str(halaman))
    halaman += 1
    soup = BeautifulSoup(page.text, 'html.parser')
    parts = soup.findAll('div', 'product-item-container')

    for part in tqdm(parts):

        # Kolom Judul Drama
        try :
            nama = ''.join(part.find('h4').text.split('\n'))
        except (AttributeError) :
            continue

        # try : 
        #     info_drama = drama.find('span', 'text-muted').text.split('-')
        # except (IndexError): 
        #     continue
        
        # # Kolom Jenis Drama
        # jenis_drama = info_drama[0].replace(' ', '')

        # # Kolom Tahun Pembuatan Drama
        # info_drama_2 = info_drama[1].split(',')
        # tahun_pembuatan = info_drama_2[0].replace(' ', '')

        # # Kolom Jumlah Episode
        # jumlah_episode = int(info_drama_2[1].replace(' ', '').replace('episodes', ''))

        # # Kolom Rating Drama
        # rating_drama = float(drama.find('span', 'p-l-xs score').text)
        
        # Membuat objek drama baru
        part_baru = data_part(nama)
        # drama_baru.print_objek()

        # Menambahkan objek drama baru ke dalam array
        list_part.append(part_baru)

# Meng-export list_drama ke dalam file berformat json
with open("cpulist.json", "w") as write_file:
    json.dump([obj.__dict__ for obj in list_part], write_file, indent=4)