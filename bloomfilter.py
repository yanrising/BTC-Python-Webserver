from bitarray import bitarray
from datetime import datetime
import math
import mmh3
import xxhash
 
class BloomFilter(object):

    def __init__(self, items_count, fp_prob, bloomfile=None):
            self.size = int(-(items_count * math.log(fp_prob))/(math.log(2)**2))
            self.hash_count = int((self.size/items_count) * math.log(2))
            if bloomfile == None:
                self.bit_array = bitarray(self.size)
                self.bit_array.setall(0)
                self.bit_array.fill()
            else:
                now = datetime.now() # current date and time
                time = now.strftime("%H:%M:%S")
                print(f"[{time}] Creating bloomfilter from {bloomfile}")
                with open(bloomfile, 'rb') as fb:
                    a = bitarray()
                    a.fromfile(fb)
                    self.bit_array = a         
                now = datetime.now() # current date and time
                time = now.strftime("%H:%M:%S")
                print(f"[{time}] Bloomfilter ready")

    def insert_mm(self, item):
        for i in range(self.hash_count):
            digest = mmh3.hash128(item, i) % self.size
            self.bit_array[digest] = True
 
    def lookup_mm(self, item):
        for i in range(self.hash_count):
            digest = mmh3.hash128(item, i) % self.size
            if self.bit_array[digest] == False:
                return False
        return True
        
    def insert_xx(self, item):
        for i in range(self.hash_count):
            digest = xxhash.xxh3_128(item, i).intdigest() % self.size
            self.bit_array[digest] = True
 
    def lookup_xx(self, item):
        for i in range(self.hash_count):
            digest = xxhash.xxh3_128(item, i).intdigest() % self.size
            if self.bit_array[digest] == False:
                return False
        return True
        
    def fnv1a(self, x, y):
        offset = 0xcbf29ce484222325
        prime = 0x100000001b3
        hash_val = offset
        x = bytearray(x, 'utf-8')
        for i in x:
            hash_val ^= i*y
            hash_val *= prime
            hash_val &= 0xFFFFFFFFFFFFFFFFFF
            #hash_val &= 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        return hash_val
    
    def insert_fnv(self, item):
        for i in range(self.hash_count):
            digest = self.fnv1a(item, i) % self.size
            self.bit_array[digest] = True
 
    def lookup_fnv(self, item):
        for i in range(self.hash_count):
            digest = self.fnv1a(item, i) % self.size
            if self.bit_array[digest] == False:
                return False
        return True
               
    def get_bytes(self):
        return self.bit_array
