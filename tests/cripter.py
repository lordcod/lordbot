from cryptography.fernet import Fernet
import random


def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)


def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)


message = str(random.randint(1, 10)).encode()
key = Fernet.generate_key()
token = encrypt(message, key)
res = decrypt(token, key).decode()

print(res)
