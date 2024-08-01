import os
import random
import string
from threading import local
import googletrans
import orjson
from typing import Optional, Dict, List

try:
    from .translator import translate_dict as _translate_dict
except ImportError:
    from translator import translate_dict as _translate_dict

try:
    from bot.resources.ether import Emoji
    from bot.misc.utils import AdditEmoji
except ImportError:
    Emoji = None

config = {}
default_languages = ["da", "de", "en", "es", "fr",  "pl", "ru", "tr"]
memoization_dict = {}
resource_dict = {}

translator = googletrans.Translator()


def translate(text, dest, src='auto'):
    return translator.translate(text, dest, src).text


def _load_file(filename: str) -> bytes:
    with open(filename, "rb") as f:
        return f.read()


def _parse_json(content: str) -> dict:
    return orjson.loads(content)


def add_res_translation(key: str, value: str, locale: str):
    resource_dict.setdefault(locale, {})
    data = resource_dict[locale]
    data_keys = key.split(".")
    for num, tk in enumerate(data_keys, start=1):
        if num >= len(data_keys):
            data[tk] = value
            break
        if not isinstance(data.get(tk), dict):
            data[tk] = {}
        data = data[tk]


def add_translation(
    key: str,
    value: str,
    locale: Optional[str] = None,
    loadable: bool = False
) -> None:
    locale = locale or config.get("locale")
    memoization_dict.setdefault(locale, {})
    memoization_dict[locale][key] = value
    if not loadable:
        add_res_translation(key, value, locale)


def add_dict_translations(path: str, data: Dict[str, str]):
    for loc, text in data.items():
        add_translation(path, text, loc)


def translate_dict(src: str, dest: str, src_dict: dict) -> dict:
    dest_dict = {}
    for key, value in src_dict.items():
        if isinstance(value, dict):
            dest_dict[key] = translate_dict(src, dest, value)
        elif isinstance(value, list):
            for num, text in enumerate(value):
                dest_dict.setdefault(key, [])
                dest_dict[key][num] = translate(
                    text, dest, src)
        else:
            dest_dict[key] = translate(value, dest, src)
    return dest_dict


def translation_with_languages(locale: str, text: str, languages: List[str]) -> dict:
    data = {}
    data[locale] = text

    if locale in languages:
        languages.remove(locale)

    for dest in languages:
        tran_text = translate(text, dest)
        data[dest] = tran_text

    return data


def _parser_foo_any_locales(locale: str, data: dict, new_data: dict):
    for key, value in data.items():
        if isinstance(value, dict):
            if not isinstance(new_data.get(key), dict):
                new_data[key] = {}
            _parser_foo_any_locales(locale, value, new_data[key])
        else:
            if not isinstance(new_data.get(key), dict):
                new_data[key] = {}
            new_data[key][locale] = value


def to_any_locales() -> dict:
    new_data = {}
    for loc, data in resource_dict.items():
        _parser_foo_any_locales(loc, data, new_data)
    return new_data


def to_i18n_translation(data: dict, path: Optional[str] = None) -> None:
    for key, value in data.items():
        if set(default_languages) & set(value.keys()):
            add_dict_translations(f"{path+'.' if path else ''}{key}", value)
        else:
            to_i18n_translation(value, f"{path+'.' if path else ''}{key}")


def from_folder(foldername: str) -> None:
    for filename in os.listdir(foldername):
        if not filename.endswith(".json"):
            continue
        filecontent = _load_file(f"{foldername}/{filename}")
        json_resource = _parse_json(filecontent)
        resource_dict[filename[:-5]] = json_resource
        parser(json_resource, filename[:-5])


def to_folder(foldername: str) -> str:
    for lang, data in resource_dict.items():
        with open(f"{foldername}/{lang}.json", "+wb") as file:
            jsondata = orjson.dumps(data)
            file.write(jsondata)


def from_file(filename: str) -> None:
    global resource_dict
    filecontent = _load_file(filename)
    json_resource = _parse_json(filecontent)
    resource_dict = json_resource
    for lang, data in resource_dict.items():
        parser(data, lang)


def to_file(filename: str) -> str:
    jsondata = orjson.dumps(resource_dict)
    with open(filename, 'wb+') as file:
        file.write(jsondata)


def to_zip(filename: str) -> str:
    import shutil
    import os
    dirname = '_temp_localization_' + \
        ''.join([random.choice(string.hexdigits) for _ in range(4)])
    os.mkdir(dirname)

    filecontent = _load_file(filename)
    json_resource = _parse_json(filecontent)
    for lang, data in json_resource.items():
        with open(f'{dirname}/{lang}.json', 'wb+') as file:
            file.write(orjson.dumps(data))

    shutil.make_archive('localization', 'zip', dirname)
    for lang in json_resource.keys():
        os.remove(f'{dirname}/{lang}.json')
    os.rmdir(dirname)


def parser(
    json_resource: dict,
    locale: Optional[str] = None,
    prefix: Optional[str] = None,
    loadable: bool = True,
) -> None:
    for key, value in list(json_resource.items()):
        if isinstance(value, dict):
            parser(
                value, locale, f"{prefix+'.' if prefix else ''}{key}", loadable=loadable
            )
        else:
            add_translation(
                f"{prefix+'.' if prefix else ''}{key}", value, locale, loadable=loadable
            )


def t(locale: Optional[str] = None, path: Optional[str] = None, **kwargs) -> str:
    if path is None:
        return

    lang = locale

    if locale not in memoization_dict or path not in memoization_dict[locale]:
        locale = config.get("locale")

    try:
        data = memoization_dict[locale][path]
    except KeyError:
        return f'{lang}.{path}'

    if not data:
        return data

    if 'emoji' in kwargs and isinstance(kwargs['emoji'], AdditEmoji):
        kwargs['Emoji'] = kwargs.pop('emoji')
    else:
        kwargs['Emoji'] = Emoji

    return data.format(**kwargs)


if __name__ == "__main__":
    # from_file("./bot/languages/localization.json")

    # load i18n key
    # filecontent = _load_file("./bot/languages/localization_any.json")
    # json_resource = _parse_json(filecontent)
    # for lang in json_resource:
    #     print(lang)
    #     data = json_resource[lang]
    #     parser(data, lang, loadable=False)

    # to_zip("./bot/languages/localization_any.json")

    # for key, value in _parse_json(_load_file("add_temp_loc_ru.json")).items():
    #     add_translation(key, value, 'ru')
    # for key, value in _parse_json(_load_file("add_temp_loc_en.json")).items():
    #     add_translation(key, value, 'en')

    # with open(r'bot\languages\localization_any.json', 'wb') as file:
    #     file.write(orjson.dumps(memoization_dict))

    # for locale, data in _parse_json(_load_file(("./bot/languages/localization.json"))).items():
    #     with open(f'localization/{locale}.json', 'wb+') as file:
    #         file.write(orjson.dumps(data))

    # with open('bot/languages/temp_loc.json', 'rb') as file:
    #     dataloc = orjson.loads(file.read())
    #     for loc, data in dataloc.items():
    #         parser(data, loc, loadable=False)

    # Translation dict
    # for lang in default_languages:
    #     if lang == "en":
    #         continue
    #     print(lang)
    #     trd = translate_dict(
    #         "en", lang, resource_dict['en']['delcat'])
    #     print(trd)
    #     parser(trd, lang, "delcat", loadable=False)

    # Translate to default languages
    # data = translation_with_languages(
    #     "ru", "Команда для начала игры в блэкджек. Игроки должны ставить ставки и пытаться набрать 21 очко, обыгрывая дилера.",
    #     default_languages)
    # print(orjson.dumps(data).decode())

    # Translation to default languages and added
    # add_dict_translations(
    #     "settings.module-name.role-reactions", translation_with_languages("en", "Reaction Roles", default_languages))

    # To any locales format
    # data = to_any_locales()
    # with open("test_loc.json", "+wb") as file:
    #     jsondata = orjson.dumps(data)
    #     file.write(jsondata)

    # To i18n format as any locales format
    # to_i18n_translation(_parse_json(_load_file("test_loc.json")))

    to_file("localization_test.json")
