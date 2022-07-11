from datetime import datetime
from bloomfilter import *


filename = 'address.txt'
bloom = BloomFilter(420000000, 0.007)
print(f'[--------] Bloom size: {bloom.size}')
print(f'[--------] Hash funcs: {bloom.hash_count}')
now = datetime.now()
time = now.strftime("%H:%M:%S")
print(f"[{time}] Creating bloomfilter from {filename}")
counter = 0
with open(filename) as in_file:
    for addr in in_file:
        bloom.insert_mm(addr.strip())
        #bloom.insert_fnv(addr.strip())
        counter +=1        
now = datetime.now()
time = now.strftime("%H:%M:%S")
print(f"[{time}] Bloomfilter ready: {counter} elements")
with open("count.txt", "w") as cf:
	cf.write(f"{counter}\n")
bloomfile = 'bloomfile_btc.bf'
print(f'[--------] Writing bloomfilter to {bloomfile}')
with open(bloomfile, 'wb') as fb:
    bloom.bit_array.tofile(fb)
now = datetime.now()
time = now.strftime("%H:%M:%S")
print(f"[{time}] Bloomfilter written")
print(f"[--------] Done")
input()
