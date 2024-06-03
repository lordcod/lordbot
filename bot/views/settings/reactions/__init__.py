import nextcord

from bot.languages import i18n
from bot.misc.utils import to_async

from .additional import InstallEmojiView
from .precise import ReactData
from .._view import DefaultSettingsView

from bot.views import settings_menu
from bot.databases import GuildDateBases
from bot.resources.ether import channel_types_emoji


@to_async
class DropDown(nextcord.ui.StringSelect):
    async def __init__(self, guild: nextcord.Guild):
        self.gdb = GuildDateBases(guild.id)
        locale = await self.gdb.get('language')
        self.reactions = await self.gdb.get('reactions')
        channels = list(filter(lambda item: item is not None,
                               [guild.get_channel(id)
                                for id in self.reactions]))

        options = [
            nextcord.SelectOption(
                label=chnl.name,
                emoji=channel_types_emoji[chnl.type.value],
                value=chnl.id
            )
            for chnl in channels
        ]

        if len(channels) <= 0:
            options.append(nextcord.SelectOption('SelectOption'))
            _disabled = True
        else:
            _disabled = False

        super().__init__(
            placeholder=i18n.t(locale, 'settings.reactions.init.placeholder'),
            min_values=1,
            max_values=1,
            options=options,
            disabled=_disabled
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        color = await gdb.get('color')
        locale = await gdb.get('language')

        value = self.values[0]
        value = int(value)

        channel = interaction.guild.get_channel(value)
        channel_data = self.reactions.get(value)

        embed = nextcord.Embed(
            title=i18n.t(locale, 'settings.reactions.init.brief'),
            description=i18n.t(
                locale, 'settings.reactions.init.dddesc',
                channel=channel.mention,
                emojis=', '.join([emo for emo in channel_data])
            ),
            color=color
        )

        await interaction.response.edit_message(embed=embed,
                                                view=ReactData(channel, channel_data))


@to_async
class AutoReactions(DefaultSettingsView):
    embed: nextcord.Embed

    async def __init__(self, guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        color = await gdb.get('color')
        locale = await gdb.get('language')

        self.embed = nextcord.Embed(
            title=i18n.t(locale, 'settings.reactions.init.title'),
            description=i18n.t(locale, 'settings.reactions.init.description'),
            color=color
        )

        super().__init__()

        self.back.label = i18n.t(locale, 'settings.button.back')
        self.addtion.label = i18n.t(locale, 'settings.button.add')

        dd = await DropDown(guild)
        self.add_item(dd)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = await settings_menu.SettingsView(interaction.user)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Add', style=nextcord.ButtonStyle.green)
    async def addtion(self,
                      button: nextcord.ui.Button,
                      interaction: nextcord.Interaction):
        view = await InstallEmojiView(interaction.guild_id)
        await interaction.response.edit_message(embed=None, view=view)
