import emoji
import regex
import orjson
import unittest
import random

data = regex.findall(r"\{([a-zA-Z0-9\-\_\. ]+)\}", orjson.dumps(
    {"message": "{member.displayName} Hey!", "type": "1"}).decode())


def split_emoji(text):
    emojis = regex.findall(r'<a?:.+?:\d{18}>', text)
    data = regex.findall(r'\X', text)
    emojis.extend(set(data) & set(emoji.EMOJI_DATA.keys()))
    return emojis


def split_emoji_for(text):
    emojis = regex.findall(r'<a?:.+?:\d{18}>', text)
    data = regex.findall(r'\X', text)
    for d in data:
        if d in set(emoji.EMOJI_DATA.keys()):
            emojis.append(d)
    return emojis


def is_emoji(text: str) -> bool:
    text = text.strip()
    if regex.fullmatch(r'<a?:.+?:\d{18}>', text):
        return True
    if text in emoji.EMOJI_DATA:
        return True
    return False


text = ''
for _ in range(100):
    text += ''.join(random.choices(list(emoji.EMOJI_DATA.keys()), k=8))
for i in range(100):
    text += f'{i}losl'


class Test(unittest.TestResult):
    # 0.004
    # 0.014
    def test_is_emoji(self):
        return split_emoji(text)

    # 0.004
    # 0.294
    def test_is_emoji_for(self):
        return split_emoji_for(text)


if __name__ == "__main__":
    unittest.main()
