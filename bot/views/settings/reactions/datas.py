from bot.databases.db import GuildDateBases
import nextcord
from bot.misc import utils
from bot.misc.utils import is_emoji
from  .. import reactions
from ...settings import DefaultSettingsView
from bot.languages.settings import (
    reactions as reaction_langs,
    button as button_name
)


class EditModalsBuilder(nextcord.ui.Modal):
    def __init__(self,guild_id,channel_id) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        
        self.channel_id = channel_id
        super().__init__(reaction_langs.datas.title.get(locale))
        
        self.emo = nextcord.ui.TextInput(
            label=reaction_langs.datas.tilabel.get(locale),
            placeholder='<[a]:name:id>'
        )
        
        self.add_item(self.emo)
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        locale = gdb.get('language')
        reacts = gdb.get('reactions')
        emoji = self.emo.value
        channel_id = self.channel_id
        
        
        check_emoji = is_emoji(emoji)
        if not check_emoji:
            await interaction.response.send_message(
                content=reaction_langs.datas.emo_cor_error.get(locale),
                ephemeral=True
            )
            return
        try:
            await interaction.guild.fetch_emoji(check_emoji.get('id'))
        except:
            await interaction.response.send_message(
                reaction_langs.datas.emo_gi_error.get(locale),
                ephemeral=True
            )
            return
        
        reacts[channel_id] = []
        reacts[channel_id].append(emoji)
        
        gdb.set('reactions',reacts)
        
        view = reactions.AutoReactions(interaction.guild)
        await interaction.message.edit(embed=view.embed,view=view)


class ReactData(DefaultSettingsView):
    def __init__(self,channel,channel_data) -> None:
        self.gdb = GuildDateBases(channel.guild.id)
        locale = self.gdb.get('language')
        self.forum_message  = self.gdb.get('reactions',{})
        
        self.channel_data = channel_data
        self.channel = channel
        super().__init__()
        
        self.back.label = button_name.back.get(locale)
        self.edit_reactions.label = reaction_langs.datas.editreact.get(locale)
        self.delete_reactions.label = reaction_langs.datas.delreact.get(locale)
    
    
    @nextcord.ui.button(label='Back',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = reactions.AutoReactions(interaction.guild)
        
        await interaction.message.edit(embed=view.embed,view=view)
    
    @nextcord.ui.button(label='Edit reaction',style=nextcord.ButtonStyle.primary,row=2)
    async def edit_reactions(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(EditModalsBuilder(interaction.guild_id,self.channel.id))
    
    @nextcord.ui.button(label='Delete reaction',style=nextcord.ButtonStyle.red,row=2)
    async def delete_reactions(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        channel_id = self.channel.id
        del self.forum_message[channel_id]
        
        self.gdb.set('reactions',self.forum_message)
        
        view = reactions.AutoReactions(interaction.guild)
        await interaction.message.edit(embed=view.embed,view=view)
