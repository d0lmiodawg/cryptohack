from Crypto.Cipher import AES
from hashlib import md5
from requests import get
URL = "https://aes.cryptohack.org/passwords_as_keys"
c = get(f"{URL}/encrypt_flag").json()["ciphertext"]

with open("words", "r") as f:
    keys = [md5(w.strip().encode()).digest().hex() for w in f.readlines()]

def decrypt(ciphertext, password_hash):
    ciphertext = bytes.fromhex(ciphertext)
    key = bytes.fromhex(password_hash)

    cipher = AES.new(key, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return {"error": str(e)}

    return decrypted

crib = b"crypto"
for key in keys:
    pt = decrypt(c, key)
    if pt[:6] == crib:
        print(pt)

