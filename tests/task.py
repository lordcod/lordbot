import re
import sys
from typing import Any


# COLORS = 8  # count
# SIZE = 1024*512  # pixels
# MEMORY = 23 * 8_388_608   # bits
# ARHIVATOR_REDUCE_SIZE = 4
# ARHIVATOR_REDUCE_COUNT = 3


# MEMORE_SIZE_PICTURE = SIZE * 3  # 2^3 == COLORS
# MEMORY_INFO = MEMORY-MEMORE_SIZE_PICTURE

# RESULT_bits = (MEMORY_INFO/ARHIVATOR_REDUCE_SIZE **
#                ARHIVATOR_REDUCE_COUNT)+MEMORE_SIZE_PICTURE

# print(RESULT_bits/8_192)  # 557

# exit()


class BoolVar:
    def __init__(self, value):
        self.value = value
        # print("INIT =", value)

    # '-' — возражения "нет"
    def __neg__(self):
        return BoolVar(not self.value)

    # '+' — дизъюнкция "или"
    def __add__(self, other):
        return BoolVar(self.value or other.value)

    # '*' — конъюнкция "и"
    def __mul__(self, other):
        return BoolVar(self.value and other.value)

    # '>' — импликация "если ..., тогда"
    def __gt__(self, other):
        return BoolVar((not self.value) or other.value)

    # '=' — эквивалентность "ровно"
    def __eq__(self, other):
        return BoolVar(self.value == other.value)

    # строковое представление значения
    def __str__(self):
        return "1" if self.value else "0"

    def __format__(self, format_spec):
        return format(str(self), format_spec)

    def __or__(self, value: Any):
        return BoolVar(not (self.value and value.value))


infuncs = sys.argv[1:]
_variables = []
for infc in infuncs:
    infc.replace('=', '==')
    _variables.extend(re.findall(r"[A-Za-z]", infc))
variables = sorted(set(_variables))

header = [""]*2
for key in variables:
    header[0] += "-"*7 + "+"
    header[1] += str(key).center(7)+"|"
header[0] += ("-+" + "-"*7)*len(infuncs)
header[1] += " | Result"*len(infuncs)
print("\n".join(header + header[0:1]))

vars_for_eval = {}
for variant in range(1 << len(variables)):
    for i, key in reversed(list(enumerate(reversed(variables)))):
        vars_for_eval[key] = BoolVar(variant & (1 << i))
        print(f" {vars_for_eval[key]:<5}", end=" |")

    for infc in infuncs:
        result = eval(infc, {}, vars_for_eval)
        print(f" | {result:<5}", end=" ")
    print()

print(header[0])
