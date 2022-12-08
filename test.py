from re import sub
from decimal import Decimal

m = "Rp 999,999,999"
value = int(sub(r'[^\d.]', '', m))
print(value+1)