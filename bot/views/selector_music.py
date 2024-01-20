import nextcord
from nextcord import utils

from bot.databases.db import GuildDateBases
from bot.misc.yandex_api import Track

from typing import List

class MusicDropDown(nextcord.ui.Select):
    def __init__(self, guild_id, queue, player, tracks: List[Track]) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        self.tracks = tracks
        self.queue = queue
        self.player = player
        
        
        super().__init__(
            placeholder="Choose track",
            min_values=1,
            max_values=1,
            options=[
                nextcord.SelectOption(
                    label=track.title ,
                    description=", ".join(track.artist_names),
                    value=track.id
                )
                for track in tracks[:25]
            ]
        )
    
    async def callback(self, inter: nextcord.Interaction):
        await inter.response.defer(ephemeral=True)
        
        track_id = int(self.values[0])
        track = utils.get(self.tracks, id=track_id)
        
        if self.queue.check_retry(
            inter.guild_id,
            track
        ):
            await inter.edit_original_message(content="Трек уже присутствует в очереди!")
            return 
        
        token = self.queue.add(
            inter.guild_id,
            track
        )
        await self.player.process(token)
        
        await self.player.message.edit("Трек добавлен в очередь!", embed=None, view=None)

class MusicView(nextcord.ui.View):
    embed: nextcord.Embed
    
    def __init__(self, guild_id, queue, player, tracks: List[Track]) -> None:
        super().__init__(timeout=None)
        
        self.embed = nextcord.Embed(
            title="Выбери интересующий тебя трек!",
        )
        
        TDD = MusicDropDown(guild_id, queue, player, tracks)
        self.add_item(TDD)
