import string


def to_base(num: str, base: int) -> int:
    fn = 0
    for i, n in enumerate(reversed(num)):
        if not n.isdigit():
            n = 10+string.ascii_uppercase.find(n)
        if int(n) > base:
            raise TypeError('n > base')
        fn += base**i*int(n)
    return fn


def from_base(num: int, base: int) -> int:
    fn = 0
    while num:
        remains = num % base
        fn = fn*10+remains
        num //= base
    return str(fn)[::-1]


print(to_base('10011A', 12), int('10011A', 12))
print(to_base('10011A', 12), int('10011A', 12))

print(from_base(103829, 2) == bin(103829)[2:])
