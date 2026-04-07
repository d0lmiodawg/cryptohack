from requests import get
from Crypto.Util.Padding import pad, unpad

URL = "https://aes.cryptohack.org/ecb_oracle"
def encrypt(msg: bytes):
    return bytes.fromhex(get(f"{URL}/encrypt/{msg.hex()}").json()["ciphertext"])
    # return get(f"{URL}/encrypt/{msg.hex()}/").json()["ciphertext"]

pt = b"u1n5_h473_3cb}"
while True:
    for i in range(32, 255):
        print(i.to_bytes(1) + pt, end="\r", flush=True)
        c = encrypt(pad(i.to_bytes(1) + pt, 16) + (len(pt)+8)*b"X")
        if (c[:16] == c[-16:] and len(pt) < 15) or (c[:16] == c[-32:-16] and len(pt) >= 15):
            pt = i.to_bytes(1) + pt
            print()
            break