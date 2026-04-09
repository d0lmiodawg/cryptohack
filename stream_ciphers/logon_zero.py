import pwn
from json import dumps

conn = pwn.remote("socket.cryptohack.org", 13399)
print(conn.recvline())
token = b"\0"*28
while 1:
    conn.sendline(dumps({"option": "reset_password", "token": token.hex()}).encode())
    print(conn.recvline())
    conn.sendline(dumps({"option": "authenticate", "password": ""}))
    print(conn.recvline())
    conn.sendline(dumps({"option": "reset_connection"}))
    print(conn.recvline())



# while 1:
#     try:
#         print(conn.recvline())
#     except EOFError:
#         break