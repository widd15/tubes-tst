from bs4 import BeautifulSoup
import requests
import json

url = "https://browser.geekbench.com/opencl-benchmarks"

# Membuat class data yang fungsinya untuk membuat gpu menjadi satu objek
class data_part:
    def __init__(self, nama_part):
        self.nama_part = nama_part

# Membuat sebuah array untuk menampung objek benchmark gpu
list = []

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
table = soup.find('table', 'benchmark-chart-table')

for row in table.tbody.find_all('tr'):    
    # Find all data for each column
    columns = row.find_all('td')

    if(columns != []):
        name = columns[0].text.strip().replace("\n\n\n", " ")
        score = columns[1].text.strip()


        data = {
            'GPU':name,
            'Score':score
        }
        list.append(data)

# # Meng-export list ke dalam file berformat json
with open("scoregpu.json", "w") as write_file:
    json.dump(list, write_file, indent=4)