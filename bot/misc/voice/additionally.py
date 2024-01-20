import nextcord

from .yandex_api import Track
from .config import path

import io
import random
import asyncio
from typing import Union, Optional

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
            return
        elif self.guild_id in current_players:
            return 
        
        current_players[self.guild_id] = self 
        
        await self.play()
    
    async def update_message(self):
        embed = nextcord.Embed(
            title=f"{self.data.title} - {', '.join(self.data.artist_names)}",
            description=(
                f"Major: {self.data.major}"
                f"Diration: {self.data.diration}"
            )
        )
        print(self.data.image)
        embed.set_thumbnail(self.data.get_image())
        
        await self.message.edit(embed=embed)
    
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
        music_bytes = await self.data.download_bytes()
        byio = io.BytesIO(music_bytes)
        source = nextcord.FFmpegPCMAudio(byio, pipe=True, executable=path)
        source = nextcord.PCMVolumeTransformer(source, volume=0.5)
        
        asyncio.create_task(self.update_message())
        self.voice.play(source, after=self.callback)


current_players = {}
queue = Queue()