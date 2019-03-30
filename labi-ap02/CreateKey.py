from Crypto.PublicKey import RSA

key = RSA.generate(1024)
with open( "key.priv", "wb" ) as fout:
    fout.write(key.publickey().exportKey())

with open( "key.public", "wb" ) as fout:
    fout.write(key.exportKey())

