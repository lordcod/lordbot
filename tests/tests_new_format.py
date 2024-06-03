class My_Dict_Subclass(dict):
    def __missing__(self, key):
        return '{'+key+'}'


x = {'Alice': 23, 'Bob': 24, 'Carl': 25}
my_dict = My_Dict_Subclass(x)
print('run{Bob}c{lol}lose'.format_map(My_Dict_Subclass(x)))
