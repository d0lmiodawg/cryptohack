from Crypto.PublicKey import RSA
with open("cert.der", "rb") as f:
    cert = f.read()
print(RSA.import_key(cert).n)