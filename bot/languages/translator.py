import re
import aiohttp
import orjson
import requests


async def translate_yandex(*args: str, lang: str) -> list[str]:
    url = "https://translate.api.cloud.yandex.net/translate/v2/translate"
    data = {
        "targetLanguageCode": lang,
        "texts": args,
        "folderId": "b1gb9e5i9v46102ckdku",
        "speller": True
    }
    headers = {
        "Authorization": "Api-Key AQVN2JHwywrbp1f1pcPZiC63VBnOVxNpAUPq0SXF"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            response.raise_for_status()
            json = await response.json()

    texts = []
    for data in json['translations']:
        texts.append(data['text'])
    return texts


def find_no_trans(texts: list[str]):
    glossary = []
    que = []
    for text in texts:
        for fmr in re.findall(
                r'\{[a-zA-Z0-9\.,_:]+\}|`[a-zA-Z0-9\.,_:]+`', text):
            if fmr in que:
                continue
            que.append(fmr)
            glossary.append({
                "sourceText": fmr,
                "translatedText": fmr,
                "exact": False
            })
    print(len(que))
    return glossary


def translate_yandex_basic(*args: str, lang: str) -> list[str]:
    url = "https://translate.api.cloud.yandex.net/translate/v2/translate"
    data = {
        "sourceLanguageCode": "en",
        "targetLanguageCode": lang,
        "texts": args,
        "folderId": "b1gb9e5i9v46102ckdku",
        "speller": True,
        "glossaryConfig": {
            "glossaryData": {
                "glossaryPairs": find_no_trans(args)
            }
        },
    }
    headers = {
        "Authorization": "Api-Key AQVN2JHwywrbp1f1pcPZiC63VBnOVxNpAUPq0SXF"
    }
    response = requests.post(url, json=data, headers=headers)
    json = response.json()
    if not response.ok:
        print(response)
        print(json)
        response.raise_for_status()

    texts = []
    for data in json['translations']:
        texts.append(data['text'])
    return texts


def translate_dict(data: dict, lang: str) -> dict:
    texts = translate_yandex_basic(*data.values(), lang=lang)
    res = dict(zip(data.keys(), texts))
    return res


if __name__ == '__main__':
    with open('add_temp_loc.json', 'rb') as file:
        resource = orjson.loads(file.read())
    count = int(len(resource) / 2)
    res1 = translate_dict(dict(list(resource.items())[:count]), 'ru')
    res2 = translate_dict(dict(list(resource.items())[count:]), 'ru')
    res = res1 | res2
    with open('add_temp_loc_ru.json', 'wb+') as file:
        file.write(orjson.dumps(res))
