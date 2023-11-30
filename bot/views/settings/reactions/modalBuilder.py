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
        
        self.emoji_1 = nextcord.ui.TextInput(
            label=reaction_langs.addres.tilabel.get(locale),
            placeholder='<a:name:id>',
            required=True
        )
        
        self.emoji_2 = nextcord.ui.TextInput(
            label=reaction_langs.addres.tilabel.get(locale),
            placeholder='<:name:id>',
            required=False
        )
        
        self.emoji_3 = nextcord.ui.TextInput(
            label=reaction_langs.addres.tilabel.get(locale),
            placeholder='😀',
            required=False
        )
        
        self.add_item(self.emoji_1)
        self.add_item(self.emoji_3)
        self.add_item(self.emoji_2)
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        reacts: dict  = gdb.get('reactions')
        emojis =[self.emoji_1.value]
        
        emoji_2 = self.emoji_2.value
        if emoji_2:
            emojis.append(emoji_2)
        
        emoji_3 = self.emoji_3.value
        if emoji_3:
            emojis.append(emoji_3)
        
        channel_id = self.channel_id
        reacts[channel_id] = emojis
        
        gdb.set('reactions',reacts)
        
        view = reactions.AutoReactions(interaction.guild)
        await interaction.message.edit(embed=view.embed,view=view)
