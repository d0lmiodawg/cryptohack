from requests import get
from string import printable

def xor(b1, b2):
    return bytes(p^q for p, q in zip(b1, b2))

URL = "https://aes.cryptohack.org/ctrime"


def encrypt(pt):
    return bytes.fromhex(get(f"{URL}/encrypt/{pt.hex()}").json()["ciphertext"])

# https://en.wikipedia.org/wiki/CRIME
# Length of compressed data depends on whether part of the data repeats

flag = b"crypto{"
while True:
    L = len(encrypt(flag+b"\x01\0\0\0\0"))
    for c in printable:
        char = c.encode()
        l = len(encrypt(flag+char+b"\0\0\0\0"))
        print(flag+char, f"\t{l}", end="\r", flush=True)
        if l < L:
            flag += char
            break