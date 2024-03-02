import os
import orjson
from typing import Optional
from bot.misc.logger import Logger, TextColors
from bot.misc.utils import lord_format

config = {}
memoization_dict = {}


def _load_file(filename: str) -> bytes:
    with open(filename, 'rb') as f:
        return f.read()


def _parse_json(content: str) -> dict:
    return orjson.loads(content)


def add_translation(key: str, value: str, locale: Optional[str] = None) -> None:
    locale = locale or config.get('locale')
    memoization_dict.setdefault(locale, {})
    memoization_dict[locale][key] = value


def from_folder(foldername: str) -> None:
    Logger.info(
        f"Added localization translation {TextColors.BLUE}{TextColors.BOLD}{foldername}/*.json")
    for filename in os.listdir(foldername):
        if not filename.endswith(".json"):
            continue
        filecontent = _load_file(f"{foldername}/{filename}")
        json_resource = _parse_json(filecontent)
        parser(json_resource, filename[:-5])


def parser(json_resource: dict, locale: Optional[str] = None, prefix: Optional[str] = None) -> None:
    for key, value in json_resource.items():
        if isinstance(value, dict):
            parser(
                value,
                locale,
                f"{prefix+'.' if prefix else ''}{key}"
            )
        else:
            add_translation(
                f"{prefix+'.' if prefix else ''}{key}", value, locale)


def t(
    locale: Optional[str] = None,
    path: Optional[str] = "",
    **kwargs
) -> str:
    if locale not in memoization_dict:
        locale = config.get('locale')
    if path not in memoization_dict[locale]:
        data = memoization_dict[config.get('locale')][path]
    else:
        data = memoization_dict[locale][path]

    return lord_format(data, kwargs)
