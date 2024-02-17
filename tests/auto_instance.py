from typing import Self


@lambda _: _()
class Timeout:
    _instance = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        print('__init__')
        self.data = {}

    def get(self, name: str) -> str:
        return self.data.get(name)

    def set(self, name: str, value: str) -> None:
        self.data[name] = value
