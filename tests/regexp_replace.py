import re

str = "{hello}@gmail.com"
print(re.sub(r"\{[a-zA-Z]+\}", "wed", str))
