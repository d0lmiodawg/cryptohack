import pwn
import json
conn = pwn.remote("socket.cryptohack.org", 11112)
conn.sendline(json.dumps({"buy":"flag"}))
while True:
    print(conn.recvline())