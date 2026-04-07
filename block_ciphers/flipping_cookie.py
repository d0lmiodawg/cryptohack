from requests import get

def xor(b1, b2):
    return bytes(p^q for p, q in zip(b1, b2))


URL = "https://aes.cryptohack.org/flipping_cookie"
c = bytes.fromhex(get(f"{URL}/get_cookie").json()["cookie"])
iv = c[:16]
ct = c[16:]
print(iv, ct)
iv = xor(xor(b"admin=False;expi", b"admin=True;;expir"), iv)
print(get(f"{URL}/check_admin/{ct.hex()}/{iv.hex()}").text)