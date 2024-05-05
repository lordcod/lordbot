
from functools import singledispatch
from types import NoneType


@singledispatch
def func(arg) -> None:
    return


@func.register
def _(arg: int, arg2: int) -> int:
    return arg*arg2


@func.register
def _(arg: float) -> float:
    return arg*2


print(func(5, 2))
print(func(1.1))
print(func("lol"))
