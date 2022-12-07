from bs4 import BeautifulSoup
import requests
import json
from tqdm import tqdm

url = "https://thesystemone.com/processor"

# Membuat sebuah array untuk menampung objek processor
list = []

halaman = 1

for page in range(1, 7):
    print ('Scrapping Halaman : ', halaman)
    page = requests.get(url+"?page="+str(halaman))
    halaman += 1
    soup = BeautifulSoup(page.text, 'html.parser')
    parts = soup.findAll('div', 'product-item-container')

    for part in tqdm(parts):
        cpu = part.find('h4').text.strip()
        harga = part.find('span', 'price-new').text.strip()
        score = 0
        data = {
            'CPU':cpu,
            'Harga':harga,
            'Score':score
        }
        list.append(data)

print(list)

# Meng-export list_drama ke dalam file berformat json
with open("cpulist.json", "w") as write_file:
    json.dump(list, write_file, indent=4)