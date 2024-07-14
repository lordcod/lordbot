from functools import lru_cache


@lru_cache()
def factorial(n: int):
    if n == 1:
        return 1
    return n*factorial(n-1)


for i in range(100, 0, -1):
    if factorial(i) == i**3-i:
        print(factorial(i), i**3-i)
        print(i)
        break
