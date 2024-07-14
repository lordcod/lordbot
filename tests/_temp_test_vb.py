import asyncio
import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
token = os.environ['lordcord_token']

bot = commands.Bot()


async def main():
    await bot.login(token)
    print(bot.application_id)
    await bot.http._HTTPClient__session.close()

if __name__ == '__main__':
    asyncio.run(main())
