from cryptography.fernet import Fernet
import random


def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)

def randfloat(a: float | int, b: float | int, scope: int = 14) -> float:
    return random.randint(int(a*10**scope), int(b*10**scope)) / 10**scope


# def randnumtk(a: float | int, b: float | int) -> tuple[bytes, bytes]:
#     key = Fernet.generate_key()
#     return encrypt(str(randfloat(a, b)).encode(), key), key
# print(decrypt(*randnumtk(1,10)))

# message = str(randfloat(99.9, 100.0, 100)).encode()
# key = Fernet.generate_key()
# token = encrypt(message, key)
# res = decrypt(token, key)

