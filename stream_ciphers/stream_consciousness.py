from requests import get
from string import printable

def xor(b1, b2):
    return bytes(p^q for p, q in zip(b1, b2))

cts = set()

# Start with "crypto{", and see if we can find text where we can inferr
# the next characters of any of the other messages. Then use this guess,
# and repeat.
guess = b"Dolly will think that I'm leaving"
while 1:
    try:
        URL = "https://aes.cryptohack.org/stream_consciousness"
        c1 = bytes.fromhex(get(f"{URL}/encrypt").json()["ciphertext"])
        c2 = bytes.fromhex(get(f"{URL}/encrypt").json()["ciphertext"])
        x = xor(xor(c1[:len(guess)], c2[:len(guess)]), guess)
        if all(ch in printable for ch in x.decode()):
            print(x.decode())
    except KeyboardInterrupt:
        break
