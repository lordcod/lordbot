
import nextcord

from bot.resources.ether import Emoji
from bot.views.settings._view import DefaultSettingsView
from bot.views.settings.notification.farewell import FarewellView
from bot.views.settings.notification.twitch import TwitchView
from bot.views.settings.notification.youtube import YoutubeView
from .welcomer import WelcomerView


from bot.misc import utils
from bot.languages import i18n
from bot.views import settings_menu
from bot.databases import GuildDateBases

distribution = {
    'welcomer': WelcomerView,
    'farewell': FarewellView,
    'twitch': TwitchView,
    'youtube': YoutubeView,
}


@utils.AsyncSterilization
class NotificationDropDown(nextcord.ui.StringSelect):
    async def __init__(self, guild_id: int) -> None:
        gdb = GuildDateBases(guild_id)
        get_emoji = await utils.get_emoji_wrap(gdb)

        options = [
            nextcord.SelectOption(
                label='Welcomer',
                value='welcomer',
                description=get_emoji('welcmes'),
                emoji=get_emoji
            ),
            nextcord.SelectOption(
                label='Farewell',
                value='farewell',
                description='',
                emoji=get_emoji('reject')
            ),
            nextcord.SelectOption(
                label='Twitch',
                value='twitch',
                description='',
                emoji=get_emoji('twitch')
            ),
            nextcord.SelectOption(
                label='Youtube',
                value='youtube',
                description='',
                emoji=get_emoji('youtube')
            ),
        ]
        super().__init__(options=options)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = self.values[0]
        view = await distribution[value](interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)


@utils.AsyncSterilization
class NotificationView(DefaultSettingsView):
    embed: nextcord.Embed

    async def __init__(self, guild: nextcord.Guild) -> None:
        self.gdb = GuildDateBases(guild.id)
        locale = await self.gdb.get('language')
        color = await self.gdb.get('color')

        self.embed = nextcord.Embed(
            title='Notification Control Panel',
            color=color,
            description='The notification module is designed for automatic integration with popular streaming platforms such as Twitch and YouTube, and is also equipped with greetings to new members and farewells.'
        )

        super().__init__()

        self.back.label = i18n.t(locale, 'settings.button.back')
        self.add_item(await NotificationDropDown(guild.id))

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = await settings_menu.SettingsView(interaction.user)

        await interaction.response.edit_message(embed=view.embed, view=view)
