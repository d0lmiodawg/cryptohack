from requests import get

def xor(b1, b2):
    return bytes(p^q for p, q in zip(b1, b2))

URL = "https://aes.cryptohack.org/symmetry"


def encrypt(pt, iv):
    return bytes.fromhex(get(f"{URL}/encrypt/{pt.hex()}/{iv.hex()}").json()["ciphertext"])

def encrypt_flag():
    c = bytes.fromhex(get(f"{URL}/encrypt_flag").json()["ciphertext"])
    iv = c[:16]
    ct = c[16:]
    return iv, ct

# OFB encryption and decryption are identical
iv, c_flag = encrypt_flag()
print(encrypt(c_flag, iv))