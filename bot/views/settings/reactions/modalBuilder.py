import nextcord
from bot.databases.db import GuildDateBases
from bot.misc.utils import is_emoji
from  .. import reactions
from ...settings import DefaultSettingsView
from bot.languages.settings import (
    reactions as reaction_langs,
    button as button_name
)


class ModalsBuilder(nextcord.ui.Modal):
    def __init__(self,guild_id,channel_id) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        
        self.channel_id = channel_id
        super().__init__(reaction_langs.addres.title.get(locale))
        
        self.emoji = nextcord.ui.TextInput(
            label=reaction_langs.addres.tilabel.get(locale),
            placeholder='<[a]:name:id>'
        )
        
        self.add_item(self.emoji)
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        locale = gdb.get('language')
        reacts: dict  = gdb.get('reactions')
        emoji = self.emoji.value
        channel_id = self.channel_id
        
        reacts[channel_id] = []
        reacts[channel_id].append(emoji)
        
        gdb.set('reactions',reacts)
        
        view = reactions.AutoReactions(interaction.guild)
        await interaction.message.edit(embed=view.embed,view=view)
