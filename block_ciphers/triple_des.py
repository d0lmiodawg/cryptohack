from requests import get

def xor(b1, b2):
    return bytes(p^q for p, q in zip(b1, b2))

URL = "https://aes.cryptohack.org/triple_des"

null = int(0).to_bytes(8)
# https://en.wikipedia.org/wiki/Weak_key
# These keys make the cipher invert itself
weak_key = bytes.fromhex("0101010101010101"+"FEFEFEFEFEFEFEFE"+"0101010101010101")

def encrypt(key, pt):
    return bytes.fromhex(get(f"{URL}/encrypt/{key.hex()}/{pt.hex()}").json()["ciphertext"])

def encrypt_flag(key):
    return bytes.fromhex(get(f"{URL}/encrypt_flag/{key.hex()}").json()["ciphertext"])

c_flag = encrypt_flag(weak_key)
print(encrypt(weak_key, c_flag))