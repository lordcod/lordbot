from httpx import delete
import nextcord

from bot.languages import i18n
from bot.misc.utils import AsyncSterilization
from bot.views.information_dd import get_info_dd


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
        self.gdb = GuildDateBases(guild_id)
        self.idea_data = await self.gdb.get('ideas')
        locale = await self.gdb.get('language')

        super().__init__(placeholder=i18n.t(locale, 'settings.ideas.channel.dropdown'),
                         channel_types=[nextcord.ChannelType.text])

    async def callback(self, interaction: nextcord.Interaction) -> None:
        channel = self.values[0]

        view = await ApprovedView(interaction.guild, channel)
        await interaction.response.edit_message(embed=view.embed, view=view)


@AsyncSterilization
class ApprovedView(DefaultSettingsView):
    embed: nextcord.Embed = None

    async def __init__(self, guild: nextcord.Guild, channel: Optional[nextcord.TextChannel] = None) -> None:
        self.gdb = GuildDateBases(guild.id)
        self.idea_data: IdeasPayload = await self.gdb.get('ideas')
        channel_approved_id = self.idea_data.get('channel_approved_id')
        color = await self.gdb.get('color')
        locale = await self.gdb.get('language')

        self.embed = nextcord.Embed(
            title=i18n.t(locale, 'settings.ideas.init.title'),
            description=i18n.t(locale, 'settings.ideas.init.description'),
            color=color
        )
        self.embed.add_field(
            name='',
            value=i18n.t(locale, 'settings.ideas.approved')
        )

        super().__init__()

        self.back.label = i18n.t(locale, 'settings.button.back')
        self.edit.label = i18n.t(locale, 'settings.button.edit')
        self.delete.label = i18n.t(locale, 'settings.button.delete')

        if channel is not None:
            self.channel = channel
            self.edit.disabled = False
        if channel_approved_id is not None:
            self.delete.disabled = False

        if channel or (channel := guild.get_channel(channel_approved_id)):
            self.add_item(get_info_dd(
                placeholder=i18n.t(locale, 'settings.ideas.init.value.approved',
                                   channel=f"#{channel.name}")
            ))
        else:
            self.add_item(get_info_dd(
                placeholder=i18n.t(locale, 'settings.ideas.init.value.approved',
                                   channel=i18n.t(locale, 'settings.ideas.init.unspecified'))
            ))

        cdd = await DropDown(guild.id)
        self.add_item(cdd)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = await ideas.IdeasView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Edit', style=nextcord.ButtonStyle.blurple, disabled=True)
    async def edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        idea_data = self.idea_data
        idea_data['channel_approved_id'] = self.channel.id
        await self.gdb.set('ideas', idea_data)

        view = await ApprovedView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Delete', style=nextcord.ButtonStyle.red, disabled=True)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        idea_data = self.idea_data
        idea_data.pop('channel_approved_id')
        await self.gdb.set('ideas', idea_data)

        view = await ApprovedView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)
