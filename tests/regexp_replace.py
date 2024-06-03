import re

str = "{hello}@gmail.com"
print(re.sub(r"\{([a-zA-Z]+)\}", r"\1w", str))
