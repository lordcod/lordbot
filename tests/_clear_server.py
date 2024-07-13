import asyncio
import nextcord
import os
from dotenv import load_dotenv
load_dotenv()


async def main():
    client = nextcord.Client()
    await client.login(os.environ['lordcord_token'])

    guilds = await client.fetch_guilds().flatten()
    print(guilds)
    await client.http._HTTPClient__session.close()


if __name__ == '__main__':
    asyncio.run(main())
