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

if __name__ == "__main__":
    key = b"DEoExZ0Cm7k8Rbvi6IJuy1whmXUhCsF-8XLZPUZSTDE="
    token = b"gAAAAABmEn4BtmdX54L1A2CaqbVB_dG1uTM4yZ78TeiTo3fBFmTKhciKdYuE_N3IBNRYERJMs2xRd_TxtoSeWdLVxY6B4CMSRTINXP6GNNnNjRXYXUxcDf239uYbypxVVUrtQcIITHGCuWu3QxMfijfT6nZs1Ud51KNgfmCI5xYxB3jNBfKXFAdqFpIrcnVkD7lxG7Fo3UzhilrdznjuH1Ersoj0tC8OWQ=="
    res = decrypt(token, key)
    print(int.from_bytes(res))


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
