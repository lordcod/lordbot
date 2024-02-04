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
    url = f'{api}/channels/{channel_id}/messages'
    data = {
        "content": f"Hello <@{member_id}>"
    }
    headers = {
        "Authorization": f'Bot {token}',
        "Content-Type": "application/json"
    }

    data = orjson.dumps(data)

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as res:
            json = await res.json()
            return json

res = asyncio.run(main())
pprint.pprint(res, width=160)
