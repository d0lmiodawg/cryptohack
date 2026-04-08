from requests import get

def xor(b1, b2):
    return bytes(p^q for p, q in zip(b1, b2))

# pt0 = dec(a)^key
# pt1 = dec(a)^a
# pt1^a = dec(a)
# pt0^pt1^a = key

URL = "https://aes.cryptohack.org/lazy_cbc"
a = b"a"*16
error = get(f"{URL}/receive/{(a*2).hex()}").json()["error"]
pt = bytes.fromhex(error.split("plaintext: ")[1])
pt0 = pt[:16]
pt1 = pt[16:]
key = xor(xor(pt0, pt1), a)
print(key.hex())
flag = get(f"{URL}/get_flag/{key.hex()}").json()["plaintext"]
print(bytes.fromhex(flag))
# iv = c[:16]
# ct = c[16:]
# print(iv, ct)
# iv = xor(xor(b"admin=False;expi", b"admin=True;;expir"), iv)
# print(get(f"{URL}/check_admin/{ct.hex()}/{iv.hex()}").text)