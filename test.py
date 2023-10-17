import aiohttp
import asyncio
import re

while True:
    rgx = 'https://music.yandex.ru/album/([0-9]+)(/track/([0-9]+))*(.*)'
    arg = input("Enter a link: ")
    
    result = re.fullmatch(rgx,arg)
    if result:
        print(result.groups())
        print(result.groups()[0])
        print(result.groups()[2])
    else:
        print("No res")