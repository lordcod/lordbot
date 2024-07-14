import asyncio
from yandex_music_api import Client
import os
from dotenv import load_dotenv
load_dotenv()
token = os.environ.get('yandex_api_token')


async def main():
    client = Client(token)
    await client.identify()

    trks = await client.get_likes_tracks()
    for t in trks:
        print(await t.download_link())
        input()

if __name__ == '__main__':
    asyncio.run(main())
