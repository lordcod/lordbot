import string
import emoji
import regex
import orjson
import unittest
import random

data = regex.findall(r"\{([a-zA-Z0-9\-\_\. ]+)\}", orjson.dumps(
    {"message": "{member.displayName} Hey!", "type": "1"}).decode())


def multi_delete(list_: list, deleted: list) -> None:
    elements = sorted(deleted, reverse=True)
    for elm in elements:
        while elm in list_:
            list_.remove(elm)


def multi_accept(list_: list, accepted: list) -> None:
    new_list = []
    elements = sorted(accepted, reverse=True)
    for elm in elements:
        while elm in list_:
            new_list.append(elm)
    list_.clear()
    list_.extend(new_list)


def split_emoji(text):
    emojis = regex.findall(r'<a?:.+?:\d{18,}>', text)
    data = regex.findall(r'\X', text)
    basic_emojis = set(data) & set(emoji.EMOJI_DATA.keys())
    multi_accept(data, basic_emojis)
    return emojis + data


def split_emoji_for(text):
    emojis = regex.findall(r'<a?:.+?:\d{18,}>', text)
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


def mixed(list_: list) -> list:
    ret = []
    for _ in range(len(list_)):
        res = random.choice(list_)
        list_.remove(res)
        ret.append(res)
    return ret


text = ''.join(mixed([''.join(random.choices(list(emoji.EMOJI_DATA.keys()), k=8)) for _ in range(100)] + [''.join(random.choices(string.printable, k=9)) for i in range(100)]))

print(len(text))


class Test(unittest.TestCase):
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
