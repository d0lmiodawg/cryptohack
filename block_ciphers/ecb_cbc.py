from requests import get

def xor(b1, b2):
    return bytes(p^q for p, q in zip(b1, b2))


URL = "https://aes.cryptohack.org/ecbcbcwtf"
c = bytes.fromhex(get(f"{URL}/encrypt_flag").json()["ciphertext"])
iv = c[:16]
ct = list(c[16+i*16:32+i*16] for i in range(len(c)//16 - 1))
print(iv, ct)
for t in ct:
    out = bytes.fromhex(get(f"{URL}/decrypt/{t.hex()}").json()["plaintext"])
    pt = xor(out, iv)
    print(pt.decode(), end="")
    iv = t