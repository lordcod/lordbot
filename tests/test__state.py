import asyncio
import os

import aiohttp
from nextcord.http import HTTPClient
token = os.environ.get('lordcord_token')

http = HTTPClient(dispatch=lambda *args: print(*args))


async def main():
    data = await http.static_login(token)
    print(data)
    await asyncio.sleep(1.5)

    data = await http.get_guild(1150075015849574410)
    print(data)
    await asyncio.sleep(1.5)

    data = await http.get_member(1150075015849574410, 993866981755342988)
    print(data)
    await asyncio.sleep(1.5)

    guilds_data = {}
    data = await http.get_guilds(limit=100, with_counts=True)
    for d in data:
        guilds_data[d['id']] = (d['approximate_member_count'], d['name'])
    guilds_data = dict(
        sorted(list(guilds_data.items()), key=lambda item: item[1][0], reverse=True))
    print(guilds_data)
    print(len(guilds_data))
    await http.close()

if __name__ == '__main__':
    asyncio.run(main())
