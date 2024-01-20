import aiohttp
import asyncio
import orjson
from bs4 import BeautifulSoup
from hashlib import md5
from typing import Union, List, Dict, Optional

api = 'https://api.music.yandex.net'
token = 'y0_AgAAAAA8S1W0AAG8XgAAAAD4h-juDmBNcIrGQy-iogg0enrtK802o0k'
headers = {'Authorization': f'OAuth {token}'}
SIGN_SALT = 'XGRlBW9FXlekgbPrRHuSiA'

def decode_download_info(bs_data: BeautifulSoup) -> None:
    host = bs_data.find('host').contents[0]
    ts = bs_data.find('ts').contents[0]
    path = bs_data.find('path').contents[0]
    s = bs_data.find('s').contents[0]
    sign = md5((SIGN_SALT + path[1::] + s).encode('utf-8')).hexdigest()
    
    return f'https://{host}/get-mp3/{sign}/{ts}{path}'

class NotFound(Exception):
    def __init__(self, message: str, *, ids: Optional[Union[List[Union[str, int]], int, str]] = None, request: Optional[str] = None) -> None:
        super().__init__(message)
        self.message = message
        self.ids = ids
        self.request = request
    
    def __str__(self) -> str:
        return self.message


class Playlist:
    def __init__(self,data: dict) -> None:
        self.owner: dict = data.get('owner')
        self.id: int = data.get('uid')
        self.kind = data.get('kind')
        self.title = data.get('title')
        self.description = data.get('description')
        self.tags = data.get('tags')

class Album:
    def __init__(self,data: dict) -> None:
        self.id:int = data.get('id')
        self.title:str = data.get('title')
        self.type:str = data.get('metaType')
        self.year:int = data.get('year')
        self.release_date:str = data.get('releaseDate')
        self.image:str = data.get('ogImage')
        self.artists:List[Artist] = [Artist(artist) for artist in data.get('artists',[])]
        self.labels:dict = data.get('labels')

class Artist:
    def __init__(self,data: dict) -> None:
        self.id:int = data.get('id')
        self.name:str = data.get('name')
        self.cover:dict = data.get('cover')
        self.avatar:str = self.cover and self.cover.get('uri')

class Track:
    def __init__(self, data: dict) -> None:
        self.data = data
        self.id:int = data.get('id')
        self.title:str = data.get('title')
        self.major:dict = data.get('major')
        self.image:str = data.get('ogImage')
        self.diration:float = data.get('durationMs', 0)/1000
        self.artists:List[Artist] = [Artist(artist) for artist in data.get('artists', [])]
        self.artist_names:List[str] = [art.name for art in self.artists]
        self.albums:List[Album] = [Album(album) for album in data.get('albums', [])]
    
    def get_image(self, size = "1080x1080"):
        return f'https://{self.image.replace("%%", size)}'
    
    def __str__(self) -> str:
        return f"{self.title} - {' ,'.join(self.artist_names)}"
    
    
    async def download_link(self) -> str:
        uri = await yandex_music_requests.download_info(self.id)
        link = await yandex_music_requests.download_track(uri)
        return link

    async def download_bytes(self) -> bytes:
        link = await self.download_link()
        
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as res:
                data = await res.read()
                return data
    
    async def download(
        self,
        filename:str
    ) -> None:
        bytes = await self.download_bytes()
        
        with open(filename,'wb') as file:
            file.write(bytes)

de_list = {
    'artist': Artist,
    'album': Album,
    'track': Track,
    'playlist':Playlist
}

class yandex_music_requests:
    @staticmethod
    async def download_track(
        downloadInfoUrl: str
    ) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(downloadInfoUrl) as res:
                data = await res.read()
                bs_data = BeautifulSoup(data, "xml")
                link = decode_download_info(bs_data)
                return link
    
    @staticmethod
    async def download_info(
        track_id: Union[int,str],
        bitrateInKbps: int = 192
    ) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{api}/tracks/{track_id}/download-info', headers=headers) as res:
                js = await res.json()
                results = js.get('result', [])
                for res in results:
                    if res['bitrateInKbps'] == bitrateInKbps:
                        diu = res['downloadInfoUrl']
                        return diu
                else:
                    raise Exception('bitrateInKbps error')
    
    @staticmethod
    async def search(
        text: str,
        object_type: str = 'track',
    )-> Union[List[Union[Artist, Album, Track, Playlist]],Artist, Album, Track, Playlist]:
        params = {
            'text':text,
            'nocorrect':'False',
            'type':'all',
            'page':'0',
            'playlist-in-best': 'True'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{api}/search',headers=headers,params=params) as res:
                if res.status == 400: raise NotFound(f"{object_type}s not found", request=text)
                
                js = await res.json()
                ostype = object_type+'s' if object_type != 'best' else object_type
                if object_type == 'best':
                    return de_list[js['result']['best']['type']](js['result']['best']['result'])
                return [de_list[object_type](res) for res in js['result'][ostype]['results']]

    @staticmethod
    async def get_list(
        ids: Union[List[Union[str, int]], int, str],
        object_type: str='track',
    ) -> List[Union[Artist, Album, Track, Playlist]]:
        params = {'with-positions': 'True', f'{object_type}-ids': ids}

        url = f"{api}/{object_type}s{'/list' if object_type == 'playlist' else ''}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url,params=params) as res:
                if res.status == 400: raise NotFound(f"{object_type}s not found", ids=ids)
                
                data = await res.json()
        res = [de_list[object_type](obj) for obj in data.get('result', [])]
        return res

async def main():
    track = (await yandex_music_requests.get_list(117276354))[0]
    print(track.data)

if __name__ == "__main__":
    asyncio.run(main())