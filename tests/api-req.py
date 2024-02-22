import aiohttp
import asyncio
import orjson

translate_apikey = "t1.9euelZqcmpnOnJ6dmZOXkJWNnMeane3rnpWaismTkM3GlY2KjsnLm5vHycvl8_cNaiJR-e9rbT57_t3z900YIFH572ttPnv-zef1656Vmo_NjZXOnc2Ryo6PlpDKxpiR7_zF656Vmo_NjZXOnc2Ryo6PlpDKxpiR.1A0uF6qsPxYm4Yb3YWD9xEgEZ982LsUr3-LnJ3hHl5DXAl7GsrMayZ55KYE4sldF2WZrPkVQROQUbBT-eUsNBg"
yakey = "y0_AgAAAAA8S1W0AATuwQAAAADo6A_hN4LtuLMQT5umpUUuwSYI9d07zbE"


async def main():
    url = "https://translate.api.cloud.yandex.net/translate/v2/translate"
    payload = {
        "sourceLanguageCode": "en",
        "targetLanguageCode": "ru",
        "texts": [
            "The bot is designed to facilitate server management and is equipped with various automation tool"
        ]
    }
    payload = orjson.dumps(payload).decode()
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(translate_apikey)
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers) as res:
            json = await res.read()
            print(json)

if __name__ == "__main__":
    asyncio.run(main())
