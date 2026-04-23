from requests import get
from string import printable

from tqdm import tqdm


def xor(b1, b2):
    return bytes(p ^ q for p, q in zip(b1, b2))


def pad(c, m0, c0):
    d = get(f"{URL}/send_msg/{c.hex()}/{m0.hex()}/{c0.hex()}").json()
    assert "error" in d or "msg" in d
    return "msg" in d


URL = "https://aes.cryptohack.org/paper_plane"
flag_dict = get(f"{URL}/encrypt_flag").json()
cf = bytes.fromhex(flag_dict["ciphertext"])
m0f = bytes.fromhex(flag_dict["m0"])
c0f = bytes.fromhex(flag_dict["c0"])

flag = b"crypto{h3ll0_t3l"
# flag = b""
if len(flag) > 0:
    m0f = flag[-16:]
    c0f = cf[len(flag) - 16 : len(flag)]
# print(m0f)
# print(cf, "\n", c0f)
for b in range(len(flag) // 16, len(cf) // 16):
    block = b""
    for i in range(16):
        for ch_ in b"\n" + printable.encode():
        # for ch_ in range(256):
            ch = ch_.to_bytes()
            print(ch, "      ", end="\r", flush=True)
            c0 = c0f[: -1 - i] + xor(
                xor(ch + block, c0f[-1 - i :]),
                (i + 1).to_bytes() * (i + 1),
            )
            res = pad(cf[b * 16 : (b + 1) * 16], m0f, c0)
            if res:
                # print(ch_)
                block = ch + block
                print(flag + block, "     ")
                break
    flag += block
    m0f = block
    c0f = cf[b * 16 : (b + 1) * 16]
