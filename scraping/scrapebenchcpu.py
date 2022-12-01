from bs4 import BeautifulSoup
import requests
import json

url = "https://www.pcpartrank.com/CPU/"

# Membuat class data yang fungsinya untuk membuat processor menjadi satu objek
class data_part:
    def __init__(self, nama_part):
        self.nama_part = nama_part

# Membuat sebuah array untuk menampung objek benchmarkprocessor
list = []

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
table = soup.find('table', 'rankingTable')

for row in table.tbody.find_all('tr'):    
    # Find all data for each column
    columns = row.find_all('td')

    if(columns != []):
        rank = columns[0].text.strip()
        brand = columns[1].text.strip()
        cpu = columns[2].text.strip()
        score = columns[3].text.strip()

        data = {
            'CPU':cpu,
            'Score':score
        }
        list.append(data)

# # Meng-export list ke dalam file berformat json
with open("scorecpu.json", "w") as write_file:
    json.dump(list, write_file, indent=4)