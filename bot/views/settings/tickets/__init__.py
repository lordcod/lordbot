import nextcord

from bot.misc.tempvoice import TempVoiceModule
from bot.misc.utils import AsyncSterilization
from bot.views.settings.tempvoice import options_voice
from bot.views.settings.tempvoice.select_voice import TempVoiceSelectorView


from .._view import DefaultSettingsView

from bot.databases import GuildDateBases
from bot.views import settings_menu
from bot.languages import i18n


@AsyncSterilization
class TicketsView(DefaultSettingsView):
    embed: nextcord.Embed

    async def __init__(self, guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        color = await gdb.get('color')
        locale = await gdb.get('language')
        data = await gdb.get('tempvoice')

        self.embed = nextcord.Embed(
            title='Tickets',
            color=color,
            description='The tickets module allows you to create and manage support requests, helping participants to easily open tickets, and administrators to effectively track and solve them.'
        )

        super().__init__()

        if data:
            self.remove_item(self.create)
            self.remove_item(self.select)

            optns = await options_voice.TempVoiceDropDown(guild)
            self.add_item(optns)

            if data.get('enabled'):
                self.remove_item(self.enable)
            else:
                optns.disabled = True
                self.remove_item(self.disable)
        else:
            self.remove_item(self.enable)
            self.remove_item(self.disable)

        self.back.label = i18n.t(locale, 'settings.button.back')

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = await settings_menu.SettingsView(interaction.user)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Create', style=nextcord.ButtonStyle.blurple)
    async def create(self,
                     button: nextcord.ui.Button,
                     interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)

        category = await interaction.guild.create_category(name='Private Channels')
        panel_channel = await interaction.guild.create_text_channel(
            name='Control panel',
            category=category,
            overwrites={
                interaction.guild.default_role: nextcord.PermissionOverwrite(view_channel=True,
                                                                             read_message_history=True,
                                                                             send_messages=False)
            }
        )
        channel = await interaction.guild.create_voice_channel(
            name='[+] Create channel',
            category=category,
            user_limit=2,
            overwrites={
                interaction.guild.default_role: nextcord.PermissionOverwrite(view_channel=True,
                                                                             read_message_history=True,
                                                                             connect=True)
            }
        )

        data = {
            'enabled': True,
            'channel_id': channel.id,
            'category_id': category.id,
            'panel_channel_id': panel_channel.id,
            'type_message_panel': 1
        }

        await gdb.set('tempvoice', data)
        await TempVoiceModule.create_panel(interaction.guild)

        view = await TempVoiceView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Select', style=nextcord.ButtonStyle.success)
    async def select(self,
                     button: nextcord.ui.Button,
                     interaction: nextcord.Interaction):
        view = await TempVoiceSelectorView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Disable', style=nextcord.ButtonStyle.red)
    async def disable(self,
                      button: nextcord.ui.Button,
                      interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        await gdb.set_on_json('tempvoice', 'enabled', False)

        view = await TempVoiceView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Enable', style=nextcord.ButtonStyle.success)
    async def enable(self,
                     button: nextcord.ui.Button,
                     interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        await gdb.set_on_json('tempvoice', 'enabled', True)

        view = await TempVoiceView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)
