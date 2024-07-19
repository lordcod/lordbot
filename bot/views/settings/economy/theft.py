from typing import Optional
import nextcord
from bot.databases import GuildDateBases
from bot.misc.utils import TimeCalculator, AsyncSterilization

from bot.resources.info import DEFAULT_ECONOMY_SETTINGS
from .. import economy
from .._view import DefaultSettingsView


@AsyncSterilization
class TheftView(DefaultSettingsView):
    embed: nextcord.Embed

    async def __init__(self, guild: nextcord.Guild, value: Optional[str] = None) -> None:
        self.value = value
        self.embed = (await economy.Economy(guild)).embed

        super().__init__()

        if value:
            self.edit.disabled = False
            self.reset.disabled = False

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = await economy.Economy(interaction.guild)
        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Edit', style=nextcord.ButtonStyle.success, disabled=True)
    async def edit(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        return
        if self.value in reward_names:
            modal = await RewardBonusModal(interaction.guild, self.value)
        if self.value == 'work':
            modal = await WorkBonusModal(interaction.guild)
        if self.value == 'bet':
            modal = await BetBonusModal(interaction.guild)
        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label='Reset', style=nextcord.ButtonStyle.blurple, disabled=True)
    async def reset(self,
                    button: nextcord.ui.Button,
                    interaction: nextcord.Interaction):
        return
        gdb = GuildDateBases(interaction.guild_id)
        await gdb.set_on_json('economic_settings', self.value, DEFAULT_ECONOMY_SETTINGS[self.value])

        view = await BonusView(interaction.guild, self.value)
        await interaction.message.edit(embed=view.embed, view=view)
