
data = (
    (1, 2, (3, (4, 9))),
    (5, 6, (7, (5, 10)))
)

for i, n, (i1, (n1, _)) in data:
    print(i, n, i1, n1)
