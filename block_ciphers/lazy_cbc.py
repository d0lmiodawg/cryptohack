from requests import get
from Crypto.Cipher import AES

def xor(b1, b2):
    return bytes(p^q for p, q in zip(b1, b2))


URL = "https://aes.cryptohack.org/lazy_cbc"
pt = b"a"*16
ct = bytes.fromhex(get(f"{URL}/encrypt/{pt.hex()}").json()["ciphertext"])