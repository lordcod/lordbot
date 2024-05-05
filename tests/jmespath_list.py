
import jmespath

data = jmespath.search("[?@[0]==`1`]|[0]", [[0, "ban"], [1, "mute"]])
print(data)

l = [1, 2, 3, []]
*_, = l
_[3].append(4)
print(l)
print(_)
print(l == _, l is _)
