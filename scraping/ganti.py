import json

a = open('cpu.json')
list = []

cpulist = json.load(a)

for i in cpulist:
    data = {
        'CPU':i["CPU"].upper(),
        'Harga':i["Harga"],
        'Score':i["Score"]
    }
    list.append(data)

print(list)

# Meng-export list_drama ke dalam file berformat json
with open("cpulist.json", "w") as write_file:
    json.dump(list, write_file, indent=4)