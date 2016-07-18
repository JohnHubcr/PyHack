from Crypto.PublicKey import RSA

newKey = RSA.generate(2048, e=65537)
publicKey = newKey.publickey().exportKey("PEM")
privateKey = newKey.exportKey("PEM")

print publicKey
print privateKey
