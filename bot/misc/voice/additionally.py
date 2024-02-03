import nextcord

from .yandex_api import Track
from .config import path

import io
import random
import asyncio
from typing import Union, Optional

initally_num = 10

def addtional_convert(timestamp: int):
    if 10 > timestamp:
        return f"0{timestamp}"
    return str(timestamp)

def convertor_time(timestamp: Union[int, float]):
    timestamp = int(timestamp)
    
    seconds = addtional_convert(timestamp % 60)
    minutes = addtional_convert(timestamp // 60)
    
    return f"{minutes}:{seconds}"

class Queue:
    def __init__(self) -> None:
        self.data = {}
    
    def token_generator(self) -> int:
        val = random.randint(1000000, 9999999)
        return val
    
    def register_guild(self, guild_id):
        if guild_id not in self.data:
            self.data[guild_id] = []
    
    def get_all(self, guild_id):
        self.register_guild(guild_id)
        
        return self.data[guild_id]
    
    def check_retry(self, guild_id, track: Track) -> bool:
        for data in self.get_all(guild_id):
            if (
                data.id == track.id and
                data.title == track.title
            ):
                return True
        return False
    
    def add(self, guild_id, track: Track) -> int:
        self.register_guild(guild_id)
        
        self.data[guild_id].append(track)
        
        return track.id
    
    def remove(self, guild_id, token: Optional[int] = None) -> None:
        self.register_guild(guild_id)
        data = self.get(guild_id)
        
        if data is not None and (token is None or data.id == token):
            self.data[guild_id].pop(0)
    
    def clear(self, guild_id) -> None:
        self.data[guild_id] = []
    
    def get(self, guild_id) -> Optional[Track]:
        self.register_guild(guild_id)
        
        try:
            return self.data[guild_id][0]
        except IndexError:
            return None

class MusicPlayer:
    def __init__(self, voice: Union[nextcord.VoiceClient, nextcord.VoiceProtocol], message: nextcord.Message, guild_id: int) -> None:
        self.voice = voice
        self.message = message
        self.guild_id = guild_id
    
    async def process(self, token: Optional[int] = None):
        self.data = queue.get(self.guild_id)
        
        if self.data is None:
            await self.message.edit(
                content="I didn't find any tracks in the queue, so I finished the job!",
                embed=None,
                view=None
            )
            await self.voice.disconnect()
            return
        elif self.guild_id in current_players:
            await self.message.edit(
                content="The track has been added to the queue!", 
                embed=None,
                view=None
            )
            return 
        current_players[self.guild_id] = self 
        
        await self.play()
    
    async def update_message(self, num = 0, diration = 0):
        embed = nextcord.Embed(
            title=f"{self.data.title} - {', '.join(self.data.artist_names)}",
            description=(
                f"{'⬛' * num}"
                f"{'⬜' * (initally_num-num)}"
                f" ({convertor_time(diration)} - {convertor_time(self.data.diration)})"
            ),
            url=self.data.get_url()
        )
        embed.set_thumbnail(self.data.get_image())
        
        await self.message.edit(
            content=None,
            embed=embed,
            view=None
        )
    
    async def start_diration_update(self):
        loop = asyncio.get_event_loop()
        track_diration = self.data.diration
        delay = track_diration//initally_num
        
        for i in range(1, initally_num+1):
            loop.call_later((delay*i), asyncio.create_task, self.update_message(i, (delay*i)))
    
    async def callback(self, err):
        queue.remove(self.guild_id, self.data.id)
        current_players.pop(self.guild_id)
        
        player = self.__class__(self.voice, self.message, self.guild_id)
        await player.process()
    
    async def skip(self):
        self.voice.stop()
        await self.callback("Manual shutdown")
    
    async def stop(self):
        self.voice.stop()
        queue.clear(self.guild_id)
        current_players.pop(self.guild_id)
    
    async def play(self):
        asyncio.create_task(self.update_message())
        
        music_bytes = await self.data.download_bytes()
        byio = io.BytesIO(music_bytes)
        source = nextcord.FFmpegPCMAudio(byio, pipe=True, executable=path)
        source = nextcord.PCMVolumeTransformer(source, volume=0.5)
        
        self.voice.play(source, after=self.callback)
        
        asyncio.create_task(self.start_diration_update())


current_players = {}
queue = Queue()