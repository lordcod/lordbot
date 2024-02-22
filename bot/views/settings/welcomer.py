import nextcord

from bot.views.settings._view import DefaultSettingsView

from bot.misc import utils
from bot.languages import i18n
from bot.views import settings_menu
from bot.databases.db import GuildDateBases


class Modal(nextcord.ui.Modal):
    def __init__(self, guild: nextcord.Guild, channel: nextcord.TextChannel) -> None:
        self.channel = channel

        self.gdb = GuildDateBases(guild.id)
        locale = self.gdb.get('language')

        super().__init__(i18n.t(locale, 'settings.welcomer.modal.title'))

        self.message = nextcord.ui.TextInput(
            label=i18n.t(locale, 'settings.welcomer.modal.label'),
            placeholder=i18n.t(locale, 'settings.welcomer.modal.placeholder')
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


class ChannelsDropDown(nextcord.ui.ChannelSelect):
    def __init__(self, guild_id) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')

        super().__init__(
            placeholder=i18n.t(
                locale, 'settings.welcomer.dropdown-placeholder'),
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

        self.back.label = i18n.t(locale, 'settings.button.back')
        self.install.label = i18n.t(locale, 'settings.welcomer.button.install')
        self.preview.label = i18n.t(locale, 'settings.welcomer.button.view')
        self.delete.label = i18n.t(locale, 'settings.welcomer.button.delete')

        DDB = ChannelsDropDown(guild.id)
        self.add_item(DDB)

        self.embed = nextcord.Embed(
            title=i18n.t(locale, 'settings.welcomer.embed.title'),
            description=i18n.t(locale, 'settings.welcomer.embed.description'),
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
                name=i18n.t(locale, 'settings.welcomer.embed.field.failure'),
                value=''
            )

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = settings_menu.SettingsView(interaction.user)

        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Install message', style=nextcord.ButtonStyle.success)
    async def install(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        modal = Modal(interaction.guild, self.channel)

        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label='View message', style=nextcord.ButtonStyle.blurple)
    async def preview(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        greeting_message: dict = self.gdb.get('greeting_message')

        content: str = greeting_message.get('message')

        guild_payload = utils.GuildPayload(interaction.guild).to_dict()
        member_payload = utils.MemberPayload(interaction.user).to_dict()
        data_payload = guild_payload | member_payload

        message_format = utils.lord_format(content, data_payload)

        message_data = await utils.generate_message(message_format)

        await interaction.response.send_message(**message_data, ephemeral=True)

    @nextcord.ui.button(label='Delete message', style=nextcord.ButtonStyle.red)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.gdb.set('greeting_message', {})

        view = self.__class__(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)
