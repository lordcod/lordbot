

def is_simple(num: float | int) -> bool:
    for i in range(int(num**0.5), 1, -1):
        if num % i == 0:
            print('Devision', i)
            return False
    return True


while True:
    try:
        print(is_simple(int(input())))
    except ValueError:
        continue
    except KeyboardInterrupt:
        break
