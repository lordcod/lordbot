import nextcord

from bot.misc.utils import AsyncSterilization


from ... import ideas
from bot.views.settings._view import DefaultSettingsView

from bot.databases import GuildDateBases
from bot.databases.varstructs import IdeasPayload

from typing import Optional


@AsyncSterilization
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

        view = await SuggestView(interaction.guild, channel)
        await interaction.response.edit_message(embed=view.embed, view=view)


@AsyncSterilization
class SuggestView(DefaultSettingsView):
    embed: nextcord.Embed = None

    async def __init__(self, guild: nextcord.Guild, channel: Optional[nextcord.TextChannel] = None) -> None:
        self.gdb = GuildDateBases(guild.id)
        self.idea_datas: IdeasPayload = await self.gdb.get('ideas')
        color = await self.gdb.get('color')

        self.embed = nextcord.Embed(
            title="Ideas",
            description="The ideas module allows you to collect, discuss and evaluate user suggestions. It organizes ideas in one place, allows you to vote for them and track their status.",
            color=color
        )
        self.embed.add_field(
            name='',
            value='> Choose a channel where ideas will be offered'
        )

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
        await self.gdb.set_on_json('ideas', 'channel_suggest_id', self.channel.id)

        view = await SuggestView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)
