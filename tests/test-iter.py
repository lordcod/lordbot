

class IterTest:
    def __init__(self, start: int = 0, finish: int = 100):
        self.start = start
        self.finish = finish

    def __iter__(self):
        self.value = self.start
        return self

    def __next__(self):
        if self.finish >= self.start:
            value = self.value
            self.value += 1
            return value
        else:
            raise StopIteration


def gen_test(iter):
    yield from iter


if __name__ == "__main__":
    for i in IterTest(10, 15):
        print(i)
        if i == 15:
            break

    # for i in gen_test(range(1, 100)):
    #     print(i)
