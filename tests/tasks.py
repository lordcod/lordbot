# 2 7 5 6 1 4 8
# 3


def task_4():
    ages = list(map(int, input().split()))

    woman_general = 0
    woman_ages = []

    man_general = 0
    man_ages = []

    for a in ages:
        if a > 0:
            woman_ages.append(a)
            woman_general += a
        else:
            a = abs(a)
            man_ages.append(a)
            man_general += a

    if (man_general/len(man_ages)-woman_general/len(woman_ages)) >= 10:
        print('YES')
    else:
        print('NO')


def task_8(numbers):
    numbers = list(map(int, input().split()))

    min_0 = numbers[0]
    min_1 = numbers[1] if numbers[1] > numbers[0] else numbers[0]

    for n in numbers[2:]:
        if min_0 > n:
            min_1 = min_0
            min_0 = n

    print(min_0, min_1)


def task_3():
    from itertools import product

    count = int(input())
    numbers = list(map(int, input().split()))
    multiples = list(map(int, input().split()))

    for m, a, b in product(multiples, numbers, numbers):
        print(m, a, b)
        if (a + b) % m == 0:
            print(a + b)
            break


if __name__ == "__main__":
    import random
    print(' '.join([str(random.randint(1, 100)) for _ in range(100)]))
    task_3()
