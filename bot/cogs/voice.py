import nextcord
from nextcord.ext import commands

from bot.views.selector_music import MusicView
from bot.misc.yandex_api import yandex_music_requests, Track
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

current_players = {}
queue = Queue()

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
        
        mes = await ctx.send("Загружаем трек")
        
        if finder := YANDEX_MUSIC_SEARCH.fullmatch(request):
            found = finder.group(2)
            tracks = await yandex_music_requests.get_list(found)
            track = tracks[0]
        else:
            tracks = await yandex_music_requests.search(request)
            view = MusicView(ctx.guild.id, queue, MusicPlayer(voice, mes, ctx.guild.id), tracks)
            
            await mes.edit(content=None, embed=view.embed, view=view)
            return
        
        if queue.check_retry(ctx.guild.id, track):
            await ctx.send('Музыка уже добавлена!!!')
            return 
        
        
        token = queue.add(
            ctx.guild.id,
            track
        )
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
        voice = ctx.guild.voice_client
        plr = current_players.get(ctx.guild.id)
        if voice and voice.is_playing() and plr is not None:
            await plr.stop()
            await ctx.send("Music on stop")
    
    @commands.command()
    async def skip(self, ctx: commands.Context):
        voice = ctx.guild.voice_client
        plr = current_players.get(ctx.guild.id)
        if voice and voice.is_playing() and plr is not None:
            await plr.skip()



def setup(bot: commands.Bot):
    bot.add_cog(Voice(bot))