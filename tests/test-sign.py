import inspect


def get(m: str, /, mes: str = 'home', *, h: str) -> None:
    print(mes)


signat = inspect.signature(get)
print(signat.parameters)
for name, param in signat.parameters.items():
    print(name, param.kind)
    if param.default is param.empty:
        print('Not default')
    else:
        print('Default:', param.default)
