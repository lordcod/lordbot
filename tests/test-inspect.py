import inspect


def test(string: str, number: int) -> bool:
    if not string.isdigit():
        return False
    strnum = int(string)
    return strnum == number
