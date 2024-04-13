from cryptography.fernet import Fernet
import random


def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)


def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)


if __name__ == "__main__":
    key = b"DEoExZ0Cm7k8Rbvi6IJuy1whmXUhCsF-8XLZPUZSTDE="
    token = b"gAAAAABmEn4BtmdX54L1A2CaqbVB_dG1uTM4yZ78TeiTo3fBFmTKhciKdYuE_N3IBNRYERJMs2xRd_TxtoSeWdLVxY6B4CMSRTINXP6GNNnNjRXYXUxcDf239uYbypxVVUrtQcIITHGCuWu3QxMfijfT6nZs1Ud51KNgfmCI5xYxB3jNBfKXFAdqFpIrcnVkD7lxG7Fo3UzhilrdznjuH1Ersoj0tC8OWQ=="
    res = decrypt(token, key)
    print(int.from_bytes(res))
