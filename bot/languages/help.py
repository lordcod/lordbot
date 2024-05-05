
from typing import List, Dict, Optional, TypedDict
import googletrans
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


with open("bot/languages/commands_data.json", "rb") as file:
    content = file.read()
    commands = orjson.loads(content)
    for cmd in commands:
        categories.setdefault(cmd.get('category'), [])
        categories[cmd.get('category')].append(cmd)

translator = googletrans.Translator()


def translate(text: str, lang: str) -> str:
    return translator.translate(text, lang, 'en').text


locales = [
    'ru',
    'id',
    'da',
    'de',
    'es',
    'fr',
    'pl',
    'tr'
]

if __name__ == "__main__":
    for num, cmd_data in enumerate(commands, start=1):
        if not cmd_data.get('examples'):
            continue
        print(
            f"The process of translating the {cmd_data.get('name')} command({num}/{len(commands)})")
        examples = cmd_data.get('examples')
        for exp in examples:
            new_examples = {}
            text = exp[1]
            new_examples['en'] = text
            for loc in locales:
                new_examples[loc] = translate(text, loc)
            exp[1] = new_examples

    with open("new_commands_lang.json", "wb+") as file:
        file.write(orjson.dumps(commands))
