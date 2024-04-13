from cryptography.fernet import Fernet
import random

def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)

mes = 10
r1 = mes.to_bytes()
r2 = bytes(mes)
r3 = str(mes).encode()

message = str(random.randint(1, 10)).encode()
key = Fernet.generate_key()
token = encrypt(message, key)
res = decrypt(token, key).decode()

