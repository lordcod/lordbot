class Test:
    def __init__(self, n: int) -> None:
        self.n = n


t = Test.__new__(Test)
print(t.n)
