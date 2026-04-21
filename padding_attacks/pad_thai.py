import pwn
from json import dumps, loads
from tqdm import trange

conn = pwn.remote("socket.cryptohack.org", 13421)

def send(d: dict):
    conn.sendline(dumps(d).encode())
    m = conn.recvline()
    try:
        return loads(m)
    except:
        print(m)
        exit()

def xor(b1, b2):
    return bytes(p^q for p, q in zip(b1, b2))

print(conn.recvline())
msg = bytes.fromhex(send({"option": "encrypt"})["ct"])
iv = msg[:16]
ct = msg[16:]

def unpad(i: bytes, c: bytes):
    d = send({"option": "unpad", "ct": (i+c).hex()})
    try:
        return d["result"]
    except:
        print(d)

msg0_hex = b""
for cnt in range(1, 17):
    for i in b"0123456789abcdef":
        hx = i.to_bytes()
        ct0 = ct[:16-cnt] + xor(xor(ct[16-cnt:16], hx+msg0_hex), cnt.to_bytes()*cnt)
        if unpad(iv, ct0 + ct[16:]):
            msg0_hex = hx + msg0_hex
            print(msg0_hex)
            break
    else:
        print("ERROR")
        exit()

msg1_hex = b""
for cnt in range(1, 17):
    for i in b"0123456789abcdef":
        hx = i.to_bytes()
        iv_ = iv[:16-cnt] + xor(xor(iv[16-cnt:16], hx+msg1_hex), cnt.to_bytes()*cnt)
        if unpad(iv_, ct[:16]):
            msg1_hex = hx + msg1_hex
            print(msg1_hex)
            break
    else:
        print("ERROR")
        exit()

print(send({"option": "check", "message": (msg1_hex + msg0_hex).decode("ascii")}))