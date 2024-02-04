import nextcord

from . import DefaultSettingsView

from bot.misc import utils
from bot.views import settings_menu
from bot.databases.db import GuildDateBases
from bot.languages.settings import (welcome as welcome_lang,
                                    button as button_name)


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
            'message': message,
        }
        self.gdb.set('greeting_message', data)

        view = WelcomerView(interaction.guild, self.channel)

        await interaction.message.edit(embed=view.embed, view=view)


class DropDownBuilder(nextcord.ui.ChannelSelect):
    def __init__(self, guild_id) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')

        super().__init__(
            placeholder=welcome_lang.dropdown_placeholder.get(locale),
            channel_types=[nextcord.ChannelType.news,
                           nextcord.ChannelType.text]
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        channel = self.values[0]

        view = WelcomerView(interaction.guild, channel)

        await interaction.message.edit(embed=view.embed, view=view)


class WelcomerView(DefaultSettingsView):
    embed: nextcord.Embed

    def __init__(self, guild: nextcord.Guild, select_channel: nextcord.TextChannel = None) -> None:
        self.gdb = GuildDateBases(guild.id)

        locale = self.gdb.get('language')
        color = self.gdb.get('color')
        greeting_message: dict = self.gdb.get('greeting_message')

        super().__init__()

        self.back.label = button_name.back.get(locale)
        self.install.label = welcome_lang.button_install.get(locale)
        self.preview.label = welcome_lang.button_view.get(locale)
        self.delete.label = welcome_lang.button_delete.get(locale)

        DDB = DropDownBuilder(guild.id)
        self.add_item(DDB)

        self.embed = nextcord.Embed(
            title=welcome_lang.embed_title.get(locale),
            description=welcome_lang.embed_description.get(locale),
            color=color
        )

        if (
            select_channel is not None or
            (greeting_message and
             (channel := guild.get_channel(greeting_message.get('channel_id')))
             )):
            self.channel = select_channel or channel
        else:
            self.install.disabled = True
            self.preview.disabled = True
            self.delete.disabled = True

            self.embed.add_field(
                name=welcome_lang.field_failure.get(locale),
                value=''
            )

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red, row=1)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = settings_menu.SettingsView(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Install message', style=nextcord.ButtonStyle.success, row=1)
    async def install(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        modal = Modal(interaction.guild, self.channel)

        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label='View message', style=nextcord.ButtonStyle.blurple, row=2)
    async def preview(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        greeting_message: dict = self.gdb.get('greeting_message')

        content: str = greeting_message.get('message')

        guild_payload = utils.GuildPayload(interaction.guild).to_dict()
        member_payload = utils.MemberPayload(interaction.user).to_dict()
        data_payload = guild_payload | member_payload

        templete = utils.GreetingTemplate(content)
        message_format = templete.safe_substitute(data_payload)
        message_data = await utils.generate_message(message_format)

        await interaction.response.send_message(**message_data, ephemeral=True)

    @nextcord.ui.button(label='Delete message', style=nextcord.ButtonStyle.red, row=2)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.gdb.set('greeting_message', {})

        view = self.__class__(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)
