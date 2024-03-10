import os
import orjson
import googletrans
from typing import Optional, Dict, List


config = {}
default_languages = ["da", "de", "en", "es", "fr", "id", "pl", "ru", "tr"]
memoization_dict = {}
resource_dict = {}


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
    key: str, value: str, locale: Optional[str] = None, loadable: bool = False
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
    translator = googletrans.Translator()
    dest_dict = {}
    for key, value in src_dict.items():
        if isinstance(value, dict):
            dest_dict[key] = translate_dict(src, dest, value)
        elif isinstance(value, list):
            for num, text in enumerate(value):
                dest_dict.setdefault(key, [])
                dest_dict[key][num] = translator.translate(text, dest, src).text
        else:
            dest_dict[key] = translator.translate(value, dest, src).text
    return dest_dict


def translation_with_languages(locale: str, text: str, languages: List[str]) -> dict:
    data = {}
    data[locale] = text

    if locale in languages:
        languages.remove(locale)

    translator = googletrans.Translator()

    for dest in languages:
        tran_text = translator.translate(text, dest, locale).text
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
        if not isinstance(value, dict):
            raise ValueError("Use another method")
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


def parser(
    json_resource: dict,
    locale: Optional[str] = None,
    prefix: Optional[str] = None,
    loadable: bool = True,
) -> None:
    for key, value in json_resource.items():
        if isinstance(value, dict):
            parser(
                value, locale, f"{prefix+'.' if prefix else ''}{key}", loadable=loadable
            )
        else:
            add_translation(
                f"{prefix+'.' if prefix else ''}{key}", value, locale, loadable=loadable
            )


def t(locale: Optional[str] = None, path: Optional[str] = "", **kwargs) -> str:
    if locale not in memoization_dict:
        locale = config.get("locale")
    if path not in memoization_dict[locale]:
        data = memoization_dict[config.get("locale")][path]
    else:
        data = memoization_dict[locale][path]

    return data.format_map(kwargs)


if __name__ == "__main__":
    from_folder("./bot/languages/localization")

    # Translation dict
    # for lang in default_languages:
    #     if lang == "en":
    #         continue
    #     print(lang)
    #     trd = translate_dict(
    #         "en", lang, resource_dict['en']["settings"]['music'])
    #     print(trd)
    #     parser(trd, lang, "settings.music", loadable=False)

    # Translate to default languages
    # data = translation_with_languages(
    #     "en", "Issues a sheet with all temporary bans that were issued by the bot", default_languages)
    # print(orjson.dumps(data).decode())

    # Translation to default languages and added
    # add_dict_translations(
    #     "help.record", translation_with_languages("en", "Record", default_languages))

    # To any locales format
    # data = to_any_locales()
    # with open("test_loc.json", "+wb") as file:
    #     jsondata = orjson.dumps(data)
    #     file.write(jsondata)

    # To i18n format as any locales format
    # to_i18n_translation(
    #     {
    #         "failed": {
    #             "da": "Rollen {role} kan ikke tildeles og bruges til integration eller af en bot.",
    #             "de": "Die Rolle {role} kann nicht zugewiesen werden und wird zur Integration oder von einem Bot verwendet.",
    #             "en": "The {role} role cannot be assigned and is used for integration or by a bot.",
    #             "es": "El rol {role} no se puede asignar y se usa para la integración o por un bot.",
    #             "fr": "Le rôle {role} ne peut pas être attribué et est utilisé pour l'intégration ou par un bot.",
    #             "id": "Peran {role} tidak dapat ditetapkan dan digunakan untuk integrasi atau dengan bot.",
    #             "pl": "Rola {role} nie można przypisać i służy do integracji lub przez bot.",
    #             "ru": "Роль {role} не может быть назначена, потому что используется для интеграции или бота.",
    #             "tr": "{role} rolü atanamaz ve entegrasyon veya bir bot tarafından kullanılır.",
    #         }
    #     }
    # )
    # print(resource_dict)

    # to_folder("./bot/languages/localization")
