import emoji
import regex
import orjson

data = regex.findall(r"\{([a-zA-Z0-9\-\_\. ]+)\}", orjson.dumps(
    {"message": "{member.displayName} Hey!", "type": "1"}).decode())


def split_emoji(text):
    emojis = regex.findall(r'<a?:.+?:\d{18}>', text)
    data = regex.findall(r'\X', text)
    emojis.extend(set(data) & set(emoji.EMOJI_DATA.keys()))
    return emojis


def is_emoji(text: str) -> bool:
    text = text.strip()
    if regex.fullmatch(r'<a?:.+?:\d{18}>', text):
        return True
    if text in emoji.EMOJI_DATA:
        return True
    return False


print(split_emoji("©️   ❤️ 🇺🇸"))
