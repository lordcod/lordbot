import os
import orjson
from typing import Optional

from bot.misc.utils import lord_format

config = {}
memoization_dict = {}
resource_dict = {}


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
    # Logger.info(f"Added localization translation {TextColors.BLUE}{TextColors.BOLD}{foldername}/*.json")
    for filename in os.listdir(foldername):
        if not filename.endswith(".json"):
            continue
        filecontent = _load_file(f"{foldername}/{filename}")
        json_resource = _parse_json(filecontent)
        resource_dict[filename[:-5]] = json_resource
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


class TranslatePackageAPI:
    def __init__(self, path: str, dest: str, src: str) -> None:
        self.translator = self.get_translator()
        self.src = src
        self.dest = dest
        self.path = path
        self.src_dict: dict = resource_dict[src][path]

    def translate(self, text: str) -> str:
        text = str(text)
        return self.translator.translate(text, self.dest, self.src).text

    def get_translated_dict(self, src_dict: dict) -> dict:
        dest_dict = {}
        for key, value in src_dict.items():
            print('Translated process: '+key)
            if isinstance(value, dict):
                dest_dict[key] = self.get_translated_dict(value)
            elif isinstance(value, list):
                for num, text in enumerate(value):
                    dest_dict.setdefault(key, [])
                    dest_dict[key][num] = self.translate(text)
            else:
                dest_dict[key] = self.translate(value)
        return dest_dict

    def set_parser(self) -> None:
        trd = self.get_translated_dict(self.src_dict)
        resource_dict[self.dest][self.path] = trd
        parser(resource_dict[self.dest][self.path], self.dest, self.path)

    @staticmethod
    def get_translator():
        import googletrans
        translator = googletrans.Translator()
        return translator


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


def to_folder(foldername: str) -> str:
    for lang, data in resource_dict.items():
        with open(f"{foldername}/{lang}.json", "+wb") as file:
            jsondata = orjson.dumps(data)
            file.write(jsondata)


if __name__ == "__main__":
    from_folder("./bot/languages/localization")
    for lang in resource_dict.keys():
        print('Start translate '+lang)
        if lang in ('en', 'da', 'es'):
            continue
        tpapi = TranslatePackageAPI('help', lang, 'en')
        tpapi.set_parser()

    to_folder("./bot/languages/localization")
