from bs4 import BeautifulSoup
import requests
import json

url = "https://www.pcpartrank.com/GPU/"

# Membuat class data yang fungsinya untuk membuat gpu menjadi satu objek
class data_part:
    def __init__(self, nama_part):
        self.nama_part = nama_part

# Membuat sebuah array untuk menampung objek benchmarkgpu
list = []

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
table = soup.find('table', 'rankingTable')

for row in table.tbody.find_all('tr'):    
    # Find all data for each column
    columns = row.find_all('td')

    if(columns != []):
        brand = columns[0].text.strip()
        model = columns[1].text.strip()
        gpu = columns[2].text.strip()
        score = columns[3].text.strip()
        samplesize = columns[4].text.strip()

        data = {
            'GPU':gpu,
            'Score':score
        }
        list.append(data)

# # Meng-export list ke dalam file berformat json
with open("scoregpu.json", "w") as write_file:
    json.dump(list, write_file, indent=4)