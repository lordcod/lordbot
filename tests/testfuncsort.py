
def printint(num: int):
    def wrapped(func):
        print(num)

        def inner():
            return
        return inner
    return wrapped
