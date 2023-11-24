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
        reacts  = gdb.get('reactions')
        emoji = self.emoji.value
        channel_id = self.channel_id
        
        if channel_id in reacts:
            await interaction.response.send_message(reaction_langs.addres.cherror.get(locale))
            return
        
        check_emoji = is_emoji(emoji)
        if not check_emoji:
            await interaction.response.send_message(
                content=reaction_langs.addres.emo_cor_error.get(locale),
                ephemeral=True
            )
            return
        
        try:
            await interaction.guild.fetch_emoji(check_emoji.get('id'))
        except:
            await interaction.response.send_message(
                reaction_langs.addres.emo_gi_error.get(locale),
                ephemeral=True
            )
            return
        
        reacts[channel_id] = []
        reacts[channel_id].append(emoji)
        
        gdb.set('reactions',reacts)
        
        view = reactions.AutoReactions(interaction.guild)
        await interaction.message.edit(embed=view.embed,view=view)

class DropDownBuilder(nextcord.ui.ChannelSelect):
    def __init__(self,guild_id) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        
        super().__init__(
            placeholder=reaction_langs.addres.ph.get(locale)
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        channel = self.values[0]
        await interaction.response.send_modal(ModalsBuilder(interaction.guild_id,channel.id))

class ViewBuilder(DefaultSettingsView):
    def __init__(self,guild_id: int) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        
        super().__init__()
        
        self.back.label = button_name.back.get(locale)
        
        DDB = DropDownBuilder(guild_id)
        
        self.add_item(DDB)
    
    
    @nextcord.ui.button(label='Back',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = reactions.AutoReactions(interaction.guild)
        
        await interaction.message.edit(embed=view.embed,view=view)