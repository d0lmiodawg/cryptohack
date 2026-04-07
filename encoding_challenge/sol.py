from pwn import remote
import json
import base64
from Crypto.Util.number import long_to_bytes
import codecs

r = remote('socket.cryptohack.org', 13377, level = 'debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(d):
    request = json.dumps(d).encode()
    r.sendline(request)

while True:
    received = json_recv()
    encoding = received["type"]
    c = received["encoded"]
    if encoding == "base64":
        decoded = base64.b64decode(c).decode()
    elif encoding == "hex":
        decoded = bytes.fromhex(c).decode()
    elif encoding == "rot13":
        decoded = codecs.decode(c, 'rot_13')
    elif encoding == "bigint":
        decoded = long_to_bytes(int(c, 16)).decode()
    elif encoding == "utf-8":
        decoded = "".join(chr(i) for i in c)

    json_send({"decoded": decoded})

