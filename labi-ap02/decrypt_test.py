from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
with open("key.public", 'rb') as key_file:
    key = RSA.importKey(key_file.read())
cipher = PKCS1_OAEP.new(key)

sign = open("report.sig",'rb').read()
for i in range(128):
    print(cipher.decrypt(sign[i*128:(i+1)*128]).decode('utf-8'), end="")
