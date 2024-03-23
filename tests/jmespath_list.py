
import jmespath

data = jmespath.search("[?@[0]==`1`]|[0]", [[0, "ban"], [1, "mute"]])
print(data)
