import orjson
import requests
import os
from dotenv import load_dotenv

load_dotenv()

apikey = os.getenv('YOUTUBE_API_KEY')


def get_channel_ids(ids: list[str]) -> dict:
    url = 'https://www.googleapis.com/youtube/v3/channels'
    params = list({
        'part': 'snippet,id',
        'type': 'channel',
        'maxResults': 15,
        'key': apikey
    }.items())

    for id in ids:
        params.append(('id', id))

    res = requests.get(url, params=params)
    return res.json()


print(orjson.dumps(get_channel_ids([input('> ')])).decode())
