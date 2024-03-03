
from typing import List, Dict, Optional, TypedDict
import jmespath
import orjson


class CommandOption(TypedDict):
    name: str
    category: str
    aliases: List[str]
    arguments: List[str]
    examples: Optional[List[List[str]]]
    descriptrion: Dict[str, str]
    brief_descriptrion: Dict[str, str]
    allowed_disabled: bool


categories_emoji: Dict[str, str] = {
    "economy": "💎",
    "major": "👑",
    "voice": "🎤",
    "moderation": "⚠",
}

categories_name:  Dict[str, Dict[str, str]] = {
    "economy": {
        "ru": "Экономика",
        "en": "Economy",
        "id": "Ekonomi",
        "da": "Økonomi",
        "de": "Wirtschaft",
        "es": "Economía",
        "fr": "Économie",
        "pl": "Gospodarka",
        "tr": "Ekonomi"
    },
    "major": {
        "ru": "Главное",
        "en": "Major",
        "id": "Mayor",
        "da": "Stor",
        "de": "Wichtigsten",
        "es": "Mayor",
        "fr": "Majeur",
        "pl": "Major",
        "tr": "Büyük"
    },
    "voice": {
        "ru": "Голос",
        "en": "Voice",
        "id": "Suara",
        "da": "Stemme",
        "de": "Stimme",
        "es": "Voz",
        "fr": "Voix",
        "pl": "Głos",
        "tr": "Ses"
    },
    "moderation": {
        "ru": "Модерационные",
        "en": "Moderation",
        "id": "Moderasi",
        "da": "Moderation",
        "de": "Moderation",
        "es": "Moderación",
        "fr": "Modération",
        "pl": "Moderacja",
        "tr": "Ilımlılık"
    },
}

categories: Dict[str, List[CommandOption]] = {}


commands: List[CommandOption] = []


def get_command(name: str) -> CommandOption:
    expression = f"[?name == '{name}'||contains(aliases, '{name}')]|[0]"
    result = jmespath.search(expression, commands)
    return result


with open("commands_lang.json", "rb") as file:
    content = file.read()
    commands = orjson.loads(content)
    for cmd in commands:
        if cmd.get('category') not in categories:
            categories[cmd.get('category')] = []
        categories[cmd.get('category')].append(cmd)
