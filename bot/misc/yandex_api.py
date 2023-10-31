import aiohttp
import asyncio
import orjson
from bs4 import BeautifulSoup
from hashlib import md5

api = 'https://api.music.yandex.net'
token = 'y0_AgAAAAA8S1W0AAG8XgAAAADrChJ46-a4hy0gTUesY2pHjjc3tpPbYw8'
headers = {'Authorization': f'OAuth {token}'}
SIGN_SALT = 'XGRlBW9FXlekgbPrRHuSiA'

class Downald_info:
    def __init__(self,bs_data: BeautifulSoup) -> None:
        host = bs_data.find('host')
        self.host = host.contents[0]
        
        ts = bs_data.find('ts')
        self.ts = ts.contents[0]
        
        path = bs_data.find('path')
        self.path = path.contents[0]
        self.path = self.path
        
        s = bs_data.find('s')
        self.s = s.contents[0]
        
        sign = md5((SIGN_SALT + self.path[1::] + self.s).encode('utf-8')).hexdigest()
        self.sign = sign
    
    @property
    def link(self):
        host = self.host
        sign = self.sign
        ts = self.ts
        path = self.path
        
        return f'https://{host}/get-mp3/{sign}/{ts}{path}'

class yandex_music_requests:
    @staticmethod
    async def download_track(downloadInfoUrl):
        async with aiohttp.ClientSession() as session:
            async with session.get(downloadInfoUrl) as res:
                data = await res.read()
                Bs_data = BeautifulSoup(data, "xml")
                link = Downald_info(Bs_data).link
                return link
    
    @staticmethod
    async def download_info(track_id,bitrateInKbps=192):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{api}/tracks/{track_id}/download-info',headers=headers) as res:
                js = await res.json()
                print(js)
                results = js['result']
                for res in results:
                    if res['bitrateInKbps'] == bitrateInKbps:
                        diu = res['downloadInfoUrl']
                        return diu
                    raise Exception('bitrateInKbps error')
    
    @staticmethod
    async def search(text):
        params = {
            'text':text,
            'nocorrect':'False',
            'type':'all',
            'page':'0',
            'playlist-in-best': 'True'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{api}/search',headers=headers,params=params) as res:
                js = await res.json()
                print(js)
                track_id = js['result']['best']['result']['id']
                album_id = js['result']['best']['result']['albums'][0]['id']
                ids = f'{track_id}:{album_id}'
                return track_id

class track_method_yandex_music(yandex_music_requests):
    track = None
    
    def __init__(self,id) -> None:
        self.track = id
    
    async def download_link(self) -> str:
        if self.track is None:
            return None
        uri = await self.download_info(self.track)
        link = await self.download_track(uri)
        return link

    async def download_bytes(self) -> bytes:
        if self.track is None:
            return None
        link = await self.download_link()
        
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as res:
                data = await res.read()
                return data
    
    async def download(self,name) -> None:
        if self.track is None:
            return None
        bytes = await self.download_bytes()
        with open(name,'wb') as file:
            file.write(bytes)
    
    @classmethod
    async def search(cls,text):
        ids = await super().search(text)
        return cls(ids)

class track:
    pass


async def main():
    track = await track_method_yandex_music.search('не по любви')
    print(track.track)
    await track.download('audio.mp3')

asyncio.run(main())