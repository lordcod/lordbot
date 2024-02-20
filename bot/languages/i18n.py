import orjson
from typing import Optional
from bot.misc.utils import lord_format

memoization_dict = {}


def _load_file(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def _parse_json(content: str) -> dict:
    return orjson.loads(content)


def from_file(filename: str) -> None:
    filecontent = _load_file(filename)
    json_resource = _parse_json(filecontent)
    parser(json_resource)


def parser(json_resource: dict, prefix: str = '') -> None:
    for key, value in json_resource.items():
        if isinstance(value, dict):
            parser(
                value,
                f"{prefix+'.'if prefix else ''}{key}"
            )
        else:
            memoization_dict[
                f"{prefix+'.'if prefix else ''}{key}"] = value


def translate(locale: Optional[str] = "en", path: Optional[str] = "", **kwargs) -> str:
    return lord_format(
        memoization_dict[f"{locale}.{path}"],
        kwargs
    )


if __name__ == "__main__":
    from_file("./bot/languages/config.json")
    title = translate("en", path="bot-info.title", name="LordCord")
    print(title)
