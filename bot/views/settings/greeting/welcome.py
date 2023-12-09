import nextcord

from ..greeting import Greeting
from ...settings import DefaultSettingsView

from bot.misc import utils
from bot.resources.ether import Emoji
from bot.views import views
from bot.databases.db import GuildDateBases
from bot.languages.settings.greeting import welcome as welcome_lang
from bot.languages.settings import button as button_name



class Modal(nextcord.ui.Modal):
    def __init__(self, guild: nextcord.Guild, channel: nextcord.TextChannel) -> None:
        self.channel = channel
        
        self.gdb = GuildDateBases(guild.id)
        locale = self.gdb.get('language')
        
        super().__init__(welcome_lang.modal_title.get(locale))
        
        self.message = nextcord.ui.TextInput(
            label=welcome_lang.modal_label.get(locale),
            placeholder=welcome_lang.modal_placeholder.get(locale)
        )
        self.add_item(self.message)
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        message = self.message.value
        data = {
            'channel_id': self.channel.id,
            'message':message,
        }
        self.gdb.set('greeting_message',data)
        
        
        view = ViewBuilder(interaction.guild, self.channel)
        
        await interaction.message.edit(embed=view.embed, view=view)


class DropDownBuilder(nextcord.ui.ChannelSelect):
    def __init__(self,guild_id) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        
        super().__init__(
            placeholder=welcome_lang.dropdown_placeholder.get(locale),
            channel_types=[nextcord.ChannelType.news, nextcord.ChannelType.text]
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        channel = self.values[0]
        
        view = ViewBuilder(interaction.guild, channel)
        
        await interaction.message.edit(embed=view.embed, view=view)

class ViewBuilder(DefaultSettingsView):
    embed: nextcord.Embed
    
    def __init__(self, guild: nextcord.Guild, channel: nextcord.TextChannel = None) -> None:
        self.channel = channel
        self.gdb = GuildDateBases(guild.id)
        
        locale = self.gdb.get('language')
        colour = self.gdb.get('color')
        greeting_message: dict  = self.gdb.get('greeting_message')
        
        super().__init__()
        
        self.back.label = button_name.back.get(locale)
        self.install.label = welcome_lang.button_install.get(locale)
        self.view.label = welcome_lang.button_view.get(locale)
        self.delete.label = welcome_lang.button_delete.get(locale)
        
        
        DDB = DropDownBuilder(guild.id)
        self.add_item(DDB)
        
        self.embed = nextcord.Embed(
            title=welcome_lang.embed_title.get(locale),
            description=welcome_lang.embed_description.get(locale),
            color=colour
        )
        
        if greeting_message:
            channel_id = greeting_message.get('channel_id')
            channel_data = guild.get_channel(channel_id)
            if not channel:
                self.channel = channel_data
            
            if channel_data:
                self.view.disabled = False
                self.delete.disabled = False
                
                
                self.embed.add_field(
                    name=welcome_lang.field_successful.get(locale),
                    value=channel_data.mention
                )
            else:
                self.embed.add_field(
                    name=welcome_lang.field_failure.get(locale),
                    value=''
                )
        
        if self.channel:
            self.install.disabled = False
    
    @nextcord.ui.button(label='Back',style=nextcord.ButtonStyle.red,row=1)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = Greeting(interaction.guild)
        
        await interaction.message.edit(embed=view.embed, view=view)
    
    @nextcord.ui.button(label='Install message',style=nextcord.ButtonStyle.success,disabled=True,row=1)
    async def install(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        modal = Modal(interaction.guild, self.channel)
        
        await interaction.response.send_modal(modal)
    
    
    @nextcord.ui.button(label='View message',style=nextcord.ButtonStyle.blurple,disabled=True,row=2)
    async def view(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        greeting_message: dict  = self.gdb.get('greeting_message')
        
        content: str = greeting_message.get('message')
        
        guild_payload = utils.GuildPayload(interaction.guild).to_dict()
        member_payload = utils.MemberPayload(interaction.user).to_dict()
        data_payload = guild_payload|member_payload
        
        templete = utils.GreetingTemplate(content)
        message_format = templete.safe_substitute(data_payload)
        message_data = await utils.generate_message(message_format)
        
        await interaction.response.send_message(**message_data,ephemeral=True)
    
    @nextcord.ui.button(label='Delete message',style=nextcord.ButtonStyle.red,disabled=True,row=2)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.gdb.set('greeting_message',{})
        
        
        view = ViewBuilder(interaction.guild)
        
        await interaction.message.edit(embed=view.embed, view=view)