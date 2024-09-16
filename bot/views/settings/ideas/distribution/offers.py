import nextcord

from bot.languages import i18n
from bot.misc.utils import AsyncSterilization
from bot.views.information_dd import get_info_dd


from bot.databases import GuildDateBases
from bot.databases.varstructs import IdeasPayload
from .base import ViewOptionItem

from typing import Optional


@AsyncSterilization
class ChannelsDropDown(nextcord.ui.ChannelSelect):
    async def __init__(
        self,
        guild_id: int
    ) -> None:
        gdb = GuildDateBases(guild_id)
        self.idea_data = await gdb.get('ideas')
        locale = await gdb.get('language')

        super().__init__(placeholder=i18n.t(locale, 'settings.ideas.channel.dropdown'), channel_types=[nextcord.ChannelType.text])

    async def callback(self, interaction: nextcord.Interaction) -> None:
        channel = self.values[0]

        view = await OffersView(interaction.guild, channel)
        await interaction.response.edit_message(embed=view.embed, view=view)


@AsyncSterilization
class OffersView(ViewOptionItem):
    label: str = 'settings.ideas.dropdown.offers.title'
    description: str = 'settings.ideas.dropdown.offers.description'
    emoji: str = 'ideas'

    async def __init__(self, guild: nextcord.Guild, channel: Optional[nextcord.TextChannel] = None) -> None:
        self.gdb = GuildDateBases(guild.id)
        self.idea_data: IdeasPayload = await self.gdb.get('ideas')
        channel_offers_id = self.idea_data.get('channel_offers_id')
        color = await self.gdb.get('color')
        locale = await self.gdb.get('language')

        self.embed = nextcord.Embed(
            title=i18n.t(locale, 'settings.ideas.init.title'),
            description=i18n.t(locale, 'settings.ideas.init.description'),
            color=color
        )
        self.embed.add_field(
            name='',
            value=i18n.t(locale, 'settings.ideas.offers.field')
        )

        super().__init__()

        channel_value = i18n.t(locale, 'settings.ideas.init.unspecified')
        if channel or (channel := guild.get_channel(channel_offers_id)):
            self.channel = channel
            self.edit.disabled = False
            channel_value = f"#{channel.name}"
        self.add_item(get_info_dd(
            placeholder=i18n.t(locale, 'settings.ideas.value.offers',
                               channel=channel_value)
        ))

        cdd = await ChannelsDropDown(guild.id)
        self.add_item(cdd)

        self.back.label = i18n.t(locale, 'settings.button.back')
        self.edit.label = i18n.t(locale, 'settings.button.edit')

    @nextcord.ui.button(label='Edit', style=nextcord.ButtonStyle.blurple, disabled=True)
    async def edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.gdb.set_on_json('ideas', 'channel_offers_id', self.channel.id)

        view = await OffersView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)
