import nextcord
from nextcord import utils

from bot.databases.db import GuildDateBases
from bot.misc.voice.yandex_api import Track

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
                    label=str(track),
                    value=track.id
                )
                for track in tracks[:25]
            ]
        )
    
    async def callback(self, inter: nextcord.Interaction):
        track_id = int(self.values[0])
        track = utils.get(self.tracks, id=track_id)
        
        if self.queue.check_retry(
            inter.guild_id,
            track
        ):
            await inter.response.send_message(content="The track is already in the queue!", ephemeral=True)
            return 
        
        token = self.queue.add(
            inter.guild_id,
            track
        )
        await self.player.process(token)

class MusicView(nextcord.ui.View):
    embed: nextcord.Embed
    
    def __init__(self, guild_id, queue, player, tracks: List[Track]) -> None:
        gdb = GuildDateBases(guild_id)
        color = gdb.get('color')
        self.embed = nextcord.Embed(title="Choose the track you are interested in!", color=color)
        
        super().__init__(timeout=None)
        
        TDD = MusicDropDown(guild_id, queue, player, tracks)
        self.add_item(TDD)

