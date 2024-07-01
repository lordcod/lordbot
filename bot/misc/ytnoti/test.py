import asyncio
import aiohttp
import os

from base import YoutubeNotifier


os.environ["NGROK_AUTHTOKEN"] = '2idn5VtI3VLIH322MHxEKxzFHi3_3eNg48oj1utTb3n3uvdzV'


async def get_channel_id():
    print('run')
    session = aiohttp.ClientSession()
    url = 'https://youtube.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'type': 'channel',
        'maxResults': 15,
        'q': input('>'),
        'key': 'AIzaSyBUheMDO7fGXa8ywq2N9hgvDs2V35s67Fo'
    }

    print('req')
    async with session.get(url, params=params) as res:
        res.raise_for_status()
        json = await res.json()
    await session.close()

    for i, data in enumerate(json['items']):
        channel_id = data['id']['channelId']
        channel_name = data['snippet']['title']
        print(f'{i}. {channel_id=}, {channel_name=}')

    i = int(input('>'))
    channel_id = json['items'][i]['id']['channelId']
    channel_name = json['items'][i]['snippet']['title']
    print(f'{channel_id=}, {channel_name=}')
    return channel_id


async def main():
    channel_id = await get_channel_id()
    ytn = YoutubeNotifier()
    ytn.add_subscribed(channel_id)
    await ytn.run()

asyncio.run(main())
