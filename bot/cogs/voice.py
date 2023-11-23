import nextcord

from nextcord.ext import commands
from bot.misc.yandex_api import yandex_music_requests,Track
from bot.views import views
import asyncio
import aiohttp
import time
import io
import re

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


class Voice(commands.Cog):
    def __init__(self,bot:commands.Bot) -> None:
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def join(self,ctx):
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            await ctx.send("Бот зашел в голосовой канал")
        else:
            await ctx.send("Вы не находетесь в голосовом канале")
    
    @commands.command(pass_context=True)
    async def leave(self,ctx):
        if (ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
            await ctx.send("Бот покинул голосовой канал")
        else:
            await ctx.send("Бот не находится в голосовом канале")
    
    @commands.command(pass_context=True)
    async def play(self,ctx:commands.Context,*,req:str=None):
        voice = ctx.guild.voice_client
        
        if not req:
            await ctx.send("Вы не указали название или ссылку")
            return
        elif not voice:
            if not (ctx.author.voice):
                await ctx.send("Вы не находетесь в голосовом канале")
                return
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            if voice.channel in ctx.guild.stage_channels:
                    await ctx.guild.me.edit(suppress=False)
        elif voice.is_playing():
            await ctx.send("Музыка уже производиться, повторите попытку позже")
            return
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(req) as responce:
                    pass
        except:
            tracks = await yandex_music_requests.search(req)
            track = tracks[0]
        else:
            finder =  re.fullmatch('https://music.yandex.ru/album/(\d+)/track/(\d+)(.*)', req)
            if not finder:
                ctx.send("Трек не найден")
                return
            
            found = finder.groups()[1]
            tracks = await yandex_music_requests.get_list(found)
            track = tracks[0]
        mes = await ctx.send("Скачиваем трек")
        
        track_byte = await track.download_bytes()
        byio = io.BytesIO(track_byte)
        source = nextcord.FFmpegPCMAudio(byio,pipe=True,executable=path)
        source = nextcord.PCMVolumeTransformer(source,volume=0.5)
        voice.play(source)
        
        await mes.edit(content=f"Песня:{track.title}\nАртист(ы):{', '.join(track.artist_names)}")
    
    @commands.command(name="volume")
    async def volume(self,ctx:commands.Context,vol:int=None):
        voice:nextcord.VoiceClient = ctx.guild.voice_client
        if vol:
            if vol > 100:
                vol = 100
            elif vol < 0:
                vol = 0
            if voice:
                if voice.is_playing():
                    voice.source.volume = vol/100
                    await ctx.send(f"Текущая громкость: {vol}")
        else:
            if voice:
                if voice.is_playing():
                    await ctx.send(f"Текущая громкость: {voice.source.volume * 100}")
    
    @commands.command(name="pause")
    async def pause(self,ctx:commands.Context):
        voice:nextcord.VoiceClient = ctx.guild.voice_client
        if voice:
            if voice.is_playing():
                voice.pause()
                await ctx.send("Music on pause")
    
    @commands.command(name="resume")
    async def resume(self,ctx:commands.Context):
        voice:nextcord.VoiceClient = ctx.guild.voice_client
        if voice:
            if voice.is_paused():
                voice.resume()
                await ctx.send("Music on resume")
    
    @commands.command(name="stop")
    async def stop(self,ctx:commands.Context):
        voice:nextcord.VoiceClient = ctx.guild.voice_client
        if voice:
            if voice.is_playing():
                voice.stop()
                await ctx.send("Music on stop")


def setup(bot):
    bot.add_cog(Voice(bot))