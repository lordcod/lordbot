import nextcord
from nextcord.ext import commands

from bot.views.selector_music import MusicView
from bot.misc.voice import *
from bot.misc.utils import clamp

import re
import yt_dlp

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


class Voice(commands.Cog):
    bot: commands.Bot
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.command()
    async def join(self, ctx: commands.Context):
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            await ctx.send("The bot entered the voice channel")
        else:
            await ctx.send("You are not in the voice channel")
    
    @commands.command()
    async def leave(self, ctx: commands.Context):
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
            await ctx.send("The bot has left the voice channel")
        else:
            await ctx.send("The bot is not in the voice channel")
    
    @commands.command()
    async def play(self, ctx:commands.Context, *, request: str):
        voice = ctx.guild.voice_client
        
        if voice is None:
            if not (ctx.author.voice):
                await ctx.send("You are not in the voice channel")
                return
            
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            if voice.channel in ctx.guild.stage_channels: await ctx.guild.me.edit(suppress=False)
        
        mes = await ctx.send("Uploading a track")
        
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
            await ctx.send('Music has already been added!')
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
            await ctx.send("You did not specify the name or id")
            return
        elif not voice:
            if (ctx.author.voice):
                channel = ctx.message.author.voice.channel
                voice = await channel.connect()
                if voice.channel in ctx.guild.stage_channels:
                    await ctx.guild.me.edit(suppress=False)
            else:
                await ctx.send("You are not in the voice channel")
                return
        elif voice.is_playing():
            await ctx.send("The music is already being produced, please try again later")
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
            await ctx.send(f"Current volume: {vol}")
        elif voice and voice.is_playing():
            await ctx.send(f"Current volume: {voice.source.volume * 100}")
    
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