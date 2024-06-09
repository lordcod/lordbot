import nextcord

from bot.misc.utils import to_async

from ... import ideas
from bot.views.settings._view import DefaultSettingsView

from bot.databases import GuildDateBases
from bot.databases.varstructs import IdeasPayload

from typing import Optional


@to_async
class DropDown(nextcord.ui.ChannelSelect):
    async def __init__(
        self,
        guild_id: int
    ) -> None:
        gdb = GuildDateBases(guild_id)
        self.idea_data = await gdb.get('ideas')

        super().__init__(channel_types=[nextcord.ChannelType.text])

    async def callback(self, interaction: nextcord.Interaction) -> None:
        channel = self.values[0]

        view = await OffersView(interaction.guild, channel)
        await interaction.response.edit_message(embed=view.embed, view=view)


@to_async
class OffersView(DefaultSettingsView):
    embed: nextcord.Embed = None

    async def __init__(self, guild: nextcord.Guild, channel: Optional[nextcord.TextChannel] = None) -> None:
        self.gdb = GuildDateBases(guild.id)
        self.idea_datas: IdeasPayload = await self.gdb.get('ideas')
        channel_approved_id = self.idea_datas.get('channel_offers_id')

        super().__init__()

        if channel is not None:
            self.channel = channel
            self.edit.disabled = False

        cdd = await DropDown(guild.id)
        self.add_item(cdd)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = await ideas.IdeasView(interaction.guild)

        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Edit', style=nextcord.ButtonStyle.blurple, disabled=True)
    async def edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.gdb.set_on_json('ideas', 'channel_offers_id', self.channel.id)

        view = await OffersView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)
