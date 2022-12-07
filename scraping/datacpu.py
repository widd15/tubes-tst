import json
import re
from difflib import SequenceMatcher

a = open('cpulist.json')
b = open('scorecpu.json')

list = []

cpulist = json.load(a)
scorecpu = json.load(b)

# for i in cpulist:
#     print(i["Harga"])

# for i in scorecpu:
#     print(i)

# a = "AMD APU a8-9600"
# b = (cpulist[1].get('CPU'))

# print(re.sub('\s+', '', a.strip()))
# print(re.sub('\s+', '', b.strip()))

# if (re.sub('\s+', '', b.strip().lower())).find(re.sub('\s+', '', a.strip().lower())) != -1:
#     print("A")
# else:
#     print("B")
def is_string_similar(s1: str, s2: str, threshold: float) -> bool:
    return SequenceMatcher(a=s1, b=s2).ratio() > threshold

for i in scorecpu:
    for j in cpulist:
        if is_string_similar(s1=i["CPU"],s2=j["CPU"], threshold=0.66):
            print(i["CPU"], "match", j["CPU"])
# is_string_similar(s1=i["CPU"],s2=j["CPU"])
