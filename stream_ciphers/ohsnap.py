from requests import get
from tqdm import trange

"""
https://kevinliu.me/posts/rc4/
https://en.wikipedia.org/wiki/Fluhrer,_Mantin_and_Shamir_attack
"""

def xor(b1, b2):
    return bytes(p^q for p, q in zip(b1, b2))

URL = "https://aes.cryptohack.org/oh_snap/send_cmd"

def encrypt(iv, ct):
    r = get(f"{URL}/{ct.hex()}/{iv.hex()}")
    # print(r)
    return bytes.fromhex(r.json()["error"].split("command: ")[-1].strip())

key = b"crypto{"
a = len(key)
while 1:
    candidates = list(0 for _ in range(256))
    for x in trange(256):
        iv = bytes([a+3, 255, x])
        enc = encrypt(iv, b"\0")
        O = enc[0] # ^ b"\0"
        S = list(range(256))
        j = 0
        for i in range(a+3):
            j = (j + S[i] + (iv+key)[i]) % 256
            S[i], S[j] = S[j], S[i]
        candidates[(O - j - S[a+3]) % 256] += 1
    mx = max(candidates)
    print("Candidates:")
    for i, c in enumerate(candidates):
        if c == mx:
            k = i.to_bytes()
            print(k)
    key += k
    a += 1
    print(key)