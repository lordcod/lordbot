import aiohttp
import asyncio
import orjson

import pprint

api = "https://discord.com/api"
token = "MTA5NTcxMzk3NTUzMjAwNzQzNA.GdoeFJ.RuUbalItmQArVDmqcKLLK_2eImRpt-glwLyarI"

guild_id = 1165681101294030898
member_id = 636824998123798531
channel_id = 1165681102590050316


async def main():
    url = f"{api}/channels/{channel_id}/messages?limit=1"
    data = {
        "content": f"Hello <@{member_id}>",
        "components": [
            {
                "components": [
                    {
                        "custom_id": "22ed836987cba64bd6070e25a1543bdc",
                        "label": "Назад",
                        "style": 4,
                        "type": 2,
                    }
                ],
                "type": 1,
            },
            {
                "components": [
                    {
                        "custom_id": "00856d6d845c8e5e69e1f2c362da481d",
                        "max_values": 1,
                        "min_values": 1,
                        "options": [
                            {
                                "emoji": {"name": "🇬🇧"},
                                "label": "English (English)",
                                "value": "en",
                            },
                            {
                                "default": True,
                                "emoji": {"name": "🇷🇺"},
                                "label": "Russian (Pусский)",
                                "value": "ru",
                            },
                        ],
                        "placeholder": "Выберите язык для сервера:",
                        "type": 3,
                    }
                ],
                "type": 1,
            },
        ],
    }
    headers = {"Authorization": f"Bot {token}",
               "Content-Type": "application/json"}

    data = orjson.dumps(data)

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers=headers) as res:
            json = await res.json()
            return json


res = asyncio.run(main())
pprint.pprint(res, width=160)
