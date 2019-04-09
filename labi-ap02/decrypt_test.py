from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from sys import exit
from random import randrange

with open("key.public", 'rb') as key_file:
    key = RSA.importKey(key_file.read())
cipher = PKCS1_OAEP.new(key)

with open("report.sig",'rb') as rep:
    sign = rep.read()

with open("report.csv",'rb') as rep:
    original = rep.read()
original = original.replace(b'\r',b'')
decrypted =           b""
try:
    i = 0
    while(1):
        decrypted += (cipher.decrypt(sign[i*128:(i+1)*128]))
        i += 1
except:
    pass
decrypted = decrypted.strip(b' ')
assert len(decrypted) == len(original)
for i in range(30):
    c_test = randrange(0,len(decrypted)-1)
    assert(decrypted[c_test] == original[c_test])
