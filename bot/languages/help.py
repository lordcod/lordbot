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


class CommandsPayload(TypedDict):
    categories_emoji: Dict[str, str]
    categories_name: Dict[str, Dict[str, str]]
    commands: List[CommandOption]


categories_emoji: Dict[str, str]
categories_name: Dict[str, Dict[str, str]]
categories: Dict[str, List[CommandOption]]
commands: List[CommandOption]


def get_command(name: str) -> CommandOption:
    expression = f"[?name == '{name}'||contains(aliases, '{name}')]|[0]"
    result = jmespath.search(expression, commands)
    return result


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
