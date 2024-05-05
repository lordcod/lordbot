from typing import List, Dict, Optional, Tuple, TypedDict, Union
import googletrans
import jmespath
import orjson


class CommandOption(TypedDict):
    name: str
    category: str
    aliases: List[str]
    arguments: List[Union[Dict[str, str], str]]
    examples: Optional[List[Tuple[str, Dict[str, str]]]]
    descriptrion: Dict[str, str]
    brief_descriptrion: Dict[str, str]
    allowed_disabled: bool
    reactions: Optional[Dict[str, Dict[str, str]]]


categories_emoji: Dict[str, str] = {
    "economy": "💎",
    "major": "👑",
    "voice": "🎤",
    "moderation": "⚠",
    "reactions": "🎭"
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
    "reactions": {
        "da": "Reaktioner",
        "de": "Reaktionen",
        "en": "Reactions",
        "es": "Reacciones",
        "fr": "Réactions",
        "id": "Reaksi",
        "pl": "Reakcje",
        "ru": "Реакции",
        "tr": "Reaksiyonlar"
    }
}

categories: Dict[str, List[CommandOption]] = {}


commands: List[CommandOption] = []

all_reactions_command = ["airkiss", "angrystare", "bite", "bleh", "blush", "brofist", "celebrate", "cheers", "clap", "confused", "cool", "cry", "cuddle", "dance", "drool", "evillaugh", "facepalm", "handhold", "happy", "headbang", "hug", "kiss", "laugh", "lick", "love", "mad", "nervous", "no", "nom", "nosebleed", "nuzzle",
                         "nyah", "pat", "peek", "pinch", "poke", "pout", "punch", "roll", "run", "sad", "scared", "shout", "shrug", "shy", "sigh", "sip", "slap", "sleep", "slowclap", "smack", "smile", "smug", "sneeze", "sorry", "stare", "stop", "surprised", "sweat", "thumbsup", "tickle", "tired", "wave", "wink", "woah", "yawn", "yay", "yes"]


def get_command(name: str) -> CommandOption:
    if name in all_reactions_command:
        name = 'reactions'
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
