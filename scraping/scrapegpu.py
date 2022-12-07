from bs4 import BeautifulSoup
import requests
import json
from tqdm import tqdm

url = "https://thesystemone.com/graphics-card"

# Membuat sebuah array untuk menampung objek processor
list = []

halaman = 1

for page in range(1, 8):
    print ('Scrapping Halaman : ', halaman)
    page = requests.get(url+"?page="+str(halaman))
    halaman += 1
    soup = BeautifulSoup(page.text, 'html.parser')
    parts = soup.findAll('div', 'product-item-container')

    for part in tqdm(parts):
        gpu = part.find('h4').text.strip()
        harga = part.find('span', 'price-new').text.strip()
        data = {
            'GPU':gpu,
            'Harga':harga,
            'Score':0
        }
        list.append(data)

print(list)


# Meng-export list_drama ke dalam file berformat json
with open("gpulist.json", "w") as write_file:
    json.dump(list, write_file, indent=4)