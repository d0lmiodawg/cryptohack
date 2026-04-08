from requests import get

def xor(b1, b2):
    return bytes(p^q for p, q in zip(b1, b2))

URL = "https://aes.cryptohack.org/bean_counter"


def encrypt():
    return bytes.fromhex(get(f"{URL}/encrypt").json()["encrypted"])

# typo in source makes the counter not change. Find the encrypted counter value by xoring with known png header
ct = encrypt()
png_header = bytes.fromhex("89504E470D0A1A0A"+"0000000D"+"49484452")
xor_key = xor(png_header, ct[:16])
with open("bean_flag.png", 'wb') as f:
    f.write(xor(ct, xor_key*(len(ct)//16)))