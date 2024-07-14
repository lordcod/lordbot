from typing import List, Dict, Tuple, TypedDict, Union, NotRequired
import googletrans
import jmespath
import orjson


class CommandOption(TypedDict):
    name: str
    category: str
    aliases: List[str]
    arguments: List[Union[Dict[str, str], str]]
    examples: NotRequired[List[Tuple[str, Dict[str, str]]]]
    descriptrion: Dict[str, str]
    brief_descriptrion: Dict[str, str]
    allowed_disabled: bool
    reactions: NotRequired[Dict[str, Dict[str, str]]]
    with_group: NotRequired[bool]
    commands_group: NotRequired[List[str]]

    def get_arguments(self, locale: str) -> List[str]:
        arguments = []
        for arg in self.get('arguments', []):
            if isinstance(arg, dict):
                arguments.append(arg.get(locale, arg['en']))
            else:
                arguments.append(arg)
        return arguments


class CommandsPayload(TypedDict):
    categories_emoji: Dict[str, str]
    categories_name: Dict[str, Dict[str, str]]
    commands: List[CommandOption]


categories_emoji: Dict[str, str]
categories_name: Dict[str, Dict[str, str]]
categories: Dict[str, List[CommandOption]]
commands: List[CommandOption]

all_reactions_command = ["airkiss", "angrystare", "bite", "bleh", "blush", "brofist", "celebrate", "cheers", "clap", "confused", "cool", "cry", "cuddle", "dance", "drool", "evillaugh", "facepalm", "handhold", "happy", "headbang", "hug", "kiss", "laugh", "lick", "love", "mad", "nervous", "no", "nom", "nosebleed", "nuzzle",
                         "nyah", "pat", "peek", "pinch", "poke", "pout", "punch", "roll", "run", "sad", "scared", "shout", "shrug", "shy", "sigh", "sip", "slap", "sleep", "slowclap", "smack", "smile", "smug", "sneeze", "sorry", "stare", "stop", "surprised", "sweat", "thumbsup", "tickle", "tired", "wave", "wink", "woah", "yawn", "yay", "yes"]


def get_command(name: str) -> CommandOption:
    if name in all_reactions_command:
        name = 'reactions'
    expression = f"[?name == '{name}'||contains(aliases, '{name}')]|[0]"
    result = jmespath.search(expression, commands)
    if result is not None:
        return CommandOption(result)


with open("bot/languages/commands_data.json", "rb") as file:
    content = file.read()
    _commands: CommandsPayload = orjson.loads(content)
    categories_emoji = _commands["categories_emoji"]
    categories_name = _commands["categories_name"]
    commands = _commands["commands"]
    categories = {}
    for cmd in _commands["commands"]:
        categories.setdefault(cmd["category"], [])
        categories[cmd["category"]].append(cmd)

if __name__ == "__main__":
    translator = googletrans.Translator()

    def translate(text: str, lang: str) -> str:
        return translator.translate(text, lang, "en").text

    locales = ["ru", "id", "da", "de", "es", "fr", "pl", "tr"]

    for num, cmd_data in enumerate(commands, start=1):
        if not cmd_data.get("examples"):
            continue
        print(
            f"The process of translating the {cmd_data.get('name')} command({num}/{len(commands)})"
        )
        examples = cmd_data.get("examples")
        for exp in examples:
            new_examples = {}
            text = exp[1]
            new_examples["en"] = text
            for loc in locales:
                new_examples[loc] = translate(text, loc)
            exp[1] = new_examples

    with open("new_commands_lang.json", "+wb") as file:
        file.write(orjson.dumps(commands))
