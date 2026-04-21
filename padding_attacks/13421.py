#!/usr/bin/env python3

from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
from os import urandom

from utils import listener

FLAG = 'crypto{?????????????????????????????????????????????????????}'

class Challenge:
    def __init__(self):
        self.before_input = "Let's practice padding oracle attacks! Recover my message and I'll send you a flag.\n"
        self.message = urandom(16).hex()
        self.key = urandom(16)

    def get_ct(self):
        iv = urandom(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        ct = cipher.encrypt(self.message.encode("ascii"))
        return {"ct": (iv+ct).hex()}

    def check_padding(self, ct):
        ct = bytes.fromhex(ct)
        iv, ct = ct[:16], ct[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        pt = cipher.decrypt(ct)  # does not remove padding
        try:
            unpad(pt, 16)
        except ValueError:
            good = False
        else:
            good = True
        return {"result": good}

    def check_message(self, message):
        if message != self.message:
            self.exit = True
            return {"error": "incorrect message"}
        return {"flag": FLAG}

    #
    # This challenge function is called on your input, which must be JSON
    # encoded
    #
    def challenge(self, msg):
        if "option" not in msg or msg["option"] not in ("encrypt", "unpad", "check"):
            return {"error": "Option must be one of: encrypt, unpad, check"}

        if msg["option"] == "encrypt": return self.get_ct()
        elif msg["option"] == "unpad": return self.check_padding(msg["ct"])
        elif msg["option"] == "check": return self.check_message(msg["message"])

import builtins; builtins.Challenge = Challenge # hack to enable challenge to be run locally, see https://cryptohack.org/faq/#listener
listener.start_server(port=13421)


# msg0_hex = b""
# for cnt in range(1, 17):
#     for i in range(256):
#         print(cnt, msg0_hex)
#         hx = i.to_bytes().hex().encode("ascii")
#         ct0 = ct[:16-2*cnt] + xor(xor(ct[16-2*cnt:16], hx+msg0_hex), (cnt*2).to_bytes()*2*cnt)
#         # print(len(iv_), len(ct))
#         if unpad(iv, ct0 + ct[16:]):
#             msg0_hex = hx + msg0_hex
#             print(msg0_hex)
#             break
#     else:
#         print("ERROR")
#         exit()

# msg1_hex = b""
# for cnt in range(1, 17):
#     for i in range(256):
#         hx = i.to_bytes().hex().encode("ascii")
#         iv_ = iv[:16-2*cnt] + xor(xor(iv[16-2*cnt:16], hx+msg1_hex), (cnt*2).to_bytes()*2*cnt)
#         # print(len(iv_), len(ct))
#         if unpad(iv, ct[:16]):
#             msg1_hex = hx + msg1_hex
#             print(msg0_hex + msg1_hex)
#             break
#     else:
#         print("ERROR")
#         exit()