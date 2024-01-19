import nextcord

from nextcord.ext import commands
from bot.misc.yandex_api import yandex_music_requests
from bot.misc.utils import clamp

import io
import re
import random
import asyncio
import aiohttp
import yt_dlp
from typing import Union, Optional, List


path = 'ffmpeg'

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}  

FFMPEG_OPTIONS = {'options': '-vn'}
YOUTUBE_LINK_SEARCH = re.compile(r'https://www.youtube.com/watch?v=([a-zA-Z0-9_]+)')
YANDEX_MUSIC_SEARCH = re.compile(r'https://music.yandex.ru/album/(\d+)/track/(\d+)(.*)')

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
    
    def check_retry(self, guild_id, track_bytes: bytes, title: str, artist_names: List[str]) -> bool:
        for data in self.get_all(guild_id):
            if (
                data.get('bytes') == track_bytes and
                data.get('title') == title and
                data.get('artist_names') == artist_names
            ):
                return True
        return False
    
    def add(self, guild_id, track_bytes: bytes, title: str, artist_names: List[str]) -> int:
        self.register_guild(guild_id)
        token = self.token_generator()
        
        data = {
            'bytes': track_bytes,
            'title': title,
            'artist_names': artist_names,
            'token': token
        }
        
        self.data[guild_id].append(data)
        
        return token
    
    def remove(self, guild_id, token: Optional[int] = None) -> None:
        self.register_guild(guild_id)
        data = self.get(guild_id)
        
        if data is not None and (token is None or data.get('token') == token):
            self.data[guild_id].pop(0)
    
    def clear(self, guild_id) -> None:
        self.data[guild_id] = []
    
    def get(self, guild_id) -> Optional[dict]:
        self.register_guild(guild_id)
        
        try:
            return self.data[guild_id][0]
        except IndexError:
            return None

current_players = {}
queue = Queue()

class MusicPlayer:
    def __init__(self, voice: Union[nextcord.VoiceClient, nextcord.VoiceProtocol], message: nextcord.Message, guild_id: int) -> None:
        self.voice = voice
        self.message = message
        self.guild_id = guild_id
        
        self.data = queue.get(guild_id)
    
    async def process(self, token: Optional[int] = None):
        if self.data is None:
            return
        elif self.guild_id in current_players:
            return 
        
        print(self.data.get('token'), token)
        
        current_players[self.guild_id] = self 
        
        await self.play()
    
    async def update_message(self):
        await self.message.edit(
            content=(
                f"Песня: {self.data.get('title')}\n"
                f"Артист(ы): {', '.join(self.data.get('artist_names'))}"
            )
        )
    
    async def callback(self, err):
        queue.remove(self.guild_id, self.data.get('token'))
        current_players.pop(self.guild_id)
        
        player = self.__class__(self.voice, self.message, self.guild_id)
        await player.process()
    
    async def play(self):
        music_bytes = self.data.get('bytes')
        byio = io.BytesIO(music_bytes)
        source = nextcord.FFmpegPCMAudio(byio, pipe=True, executable=path)
        source = nextcord.PCMVolumeTransformer(source, volume=0.5)
        
        asyncio.create_task(self.update_message())
        self.voice.play(source, after=self.callback)


class Voice(commands.Cog):
    bot: commands.Bot
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.command()
    async def join(self, ctx: commands.Context):
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            await ctx.send("Бот зашел в голосовой канал")
        else:
            await ctx.send("Вы не находетесь в голосовом канале")
    
    @commands.command()
    async def leave(self, ctx: commands.Context):
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
            await ctx.send("Бот покинул голосовой канал")
        else:
            await ctx.send("Бот не находится в голосовом канале")
    
    @commands.command()
    async def play(self, ctx:commands.Context, *, request: str):
        voice = ctx.guild.voice_client
        
        if voice is None:
            if not (ctx.author.voice):
                await ctx.send("Вы не находетесь в голосовом канале")
                return
            
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            if voice.channel in ctx.guild.stage_channels: await ctx.guild.me.edit(suppress=False)
        
        
        if finder := YANDEX_MUSIC_SEARCH.fullmatch(request):
            found = finder.group(2)
            tracks = await yandex_music_requests.get_list(found)
            track = tracks[0]
        else:
            tracks = await yandex_music_requests.search(request)
            track = tracks[0]
        
        mes = await ctx.send("Скачиваем трек")
        
        track_bytes = await track.download_bytes()
        
        if queue.check_retry(
            ctx.guild.id,
            track_bytes,
            track.title,
            track.artist_names
        ):
            await ctx.send('Музыка уже добавлена!!!')
            return 
        
        
        token = queue.add(
            ctx.guild.id,
            track_bytes,
            track.title,
            track.artist_names
        )
        if current_players.get(ctx.guild.id) is None:
            player = MusicPlayer(voice, mes, ctx.guild.id)
            await player.process(token)
    
    
    @commands.command(pass_context=True)
    async def playyt(self,ctx:commands.Context, *, arg):
        voice = ctx.guild.voice_client
        
        if not arg:
            await ctx.send("Вы не указали название или id")
            return
        elif not voice:
            if (ctx.author.voice):
                channel = ctx.message.author.voice.channel
                voice = await channel.connect()
                if voice.channel in ctx.guild.stage_channels:
                    await ctx.guild.me.edit(suppress=False)
            else:
                await ctx.send("Вы не находетесь в голосовом канале")
                return
        elif voice.is_playing():
            await ctx.send("Музыка уже производиться, повторите попытку позже")
            return
        
        mes = await ctx.send("Download track")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if YOUTUBE_LINK_SEARCH.fullmatch(arg):
                info = ydl.extract_info(arg, download=False)
            else:
                info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
        
        for i in info['formats']:
            if i["audio_ext"] == "webm":
                url = i["url"]
                break
        else:
            print('Stop!')
            return
        
        source = nextcord.FFmpegPCMAudio(url, pipe=True, executable=path)
        source = nextcord.PCMVolumeTransformer(source, volume=0.5)
        async def callback(err):
            await voice.disconnect()
        voice.play(source,after=callback)
        await mes.edit(content=f"Title: {info['title']}")
    
    
    @commands.command(name="volume")
    async def volume(self,ctx:commands.Context, vol: int = None):
        voice: nextcord.VoiceClient = ctx.guild.voice_client
        if voice and voice.is_playing() and vol:
            vol = clamp(vol, 1, 100)
            
            voice.source.volume = vol/100
            await ctx.send(f"Текущая громкость: {vol}")
        elif voice and voice.is_playing():
            await ctx.send(f"Текущая громкость: {voice.source.volume * 100}")
    
    @commands.command(name="pause")
    async def pause(self, ctx:commands.Context):
        voice:nextcord.VoiceClient = ctx.guild.voice_client
        if voice and voice.is_playing():
            voice.pause()
            await ctx.send("Music on pause")
    
    @commands.command(name="resume")
    async def resume(self,ctx:commands.Context):
        voice:nextcord.VoiceClient = ctx.guild.voice_client
        if voice and voice.is_paused():
            voice.resume()
            await ctx.send("Music on resume")
    
    @commands.command(name="stop")
    async def stop(self,ctx:commands.Context):
        voice: nextcord.VoiceClient = ctx.guild.voice_client
        if voice and voice.is_playing():
            current_players.pop(ctx.guild.id)
            voice.stop()
            await ctx.send("Music on stop")


def setup(bot: commands.Bot):
    bot.add_cog(Voice(bot))