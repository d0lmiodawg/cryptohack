from requests import get

URL = "https://aes.cryptohack.org/block_cipher_starter"
r = get(f"{URL}/encrypt_flag")
cipher = r.json()["ciphertext"]
r = get(f"{URL}/decrypt/{cipher}")
print(bytes.fromhex(r.json()["plaintext"]))
