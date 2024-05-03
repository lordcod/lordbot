
from logging.config import valid_ident
from typing import Optional
import nextcord
from bot.databases import GuildDateBases
from bot.misc.utils import TimeCalculator
from bot.resources.info import DEFAULT_ECONOMY_SETTINGS
from .. import economy
from .._view import DefaultSettingsView


reward_names = {
    'daily': 'Daily reward',
    'weekly': 'Weekly reward',
    'monthly': 'Monthly reward'
}


class RewardBonusModal(nextcord.ui.Modal):
    def __init__(self, guild: nextcord.Guild, value: str) -> None:
        self.gdb = GuildDateBases(guild.id)
        self.economy_settings = self.gdb.get('economic_settings', {})
        self.value = value
        previous = self.economy_settings.get(value)
        super().__init__(reward_names[value], timeout=300)
        self.bonus = nextcord.ui.TextInput(
            label=reward_names[value],
            placeholder=previous,
            max_length=6
        )
        self.add_item(self.bonus)

    async def callback(self, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        economy_settings = gdb.get('economic_settings')
        bonus = self.bonus.value

        if not bonus.isdigit():
            return

        economy_settings[self.value] = int(bonus)

        gdb.set('economic_settings', economy_settings)

        view = BonusView(interaction.guild)
        await interaction.message.edit(embed=view.embed, view=view)


class WorkBonusModal(nextcord.ui.Modal):
    def __init__(self, guild: nextcord.Guild) -> None:
        super().__init__('Work', timeout=300)
        self.gdb = GuildDateBases(guild.id)
        self.economy_settings = self.gdb.get('economic_settings', {})
        work_data = self.economy_settings.get('work')
        _min_work_previous = work_data.get('min')
        _max_work_previous = work_data.get('max')
        _cooldwon_previous = work_data.get('cooldown')

        self.min_work = nextcord.ui.TextInput(
            label='Minimum payment for work',
            placeholder=_min_work_previous,
            required=False,
            max_length=6
        )
        self.add_item(self.min_work)

        self.max_work = nextcord.ui.TextInput(
            label='Maximum payment for work',
            placeholder=_max_work_previous,
            required=False,
            max_length=6
        )
        self.add_item(self.max_work)

        self.cooldown = nextcord.ui.TextInput(
            label='Cooldown',
            placeholder=_cooldwon_previous,
            required=False,
            max_length=20
        )
        self.add_item(self.cooldown)

    async def callback(self, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        cooldown = None

        if not (self.min_work.value or self.min_work.value or self.cooldown.value):
            await interaction.response.send_message("At least one value must be filled in", ephemeral=True)
            return
        if (self.min_work.value and not self.min_work.value.isdigit()) or (self.max_work.value and not self.max_work.value.isdigit()):
            await interaction.response.send_message("The value must be an integer number", ephemeral=True)
            return
        if self.cooldown.value:
            try:
                cooldown = TimeCalculator().convert(self.cooldown.value)
            except TypeError:
                await interaction.response.send_message("Incorrect time format", ephemeral=True)
                return

        economy_settings = gdb.get('economic_settings')
        work_data = self.economy_settings.get('work')

        if self.min_work.value:
            work_data['min'] = int(self.min_work.value)
        if self.max_work.value:
            work_data['max'] = int(self.max_work.value)
        if cooldown:
            work_data['cooldown'] = cooldown

        economy_settings['work'] = work_data
        gdb.set('economic_settings', economy_settings)

        view = BonusView(interaction.guild)
        await interaction.message.edit(embed=view.embed, view=view)


class BetBonusModal(nextcord.ui.Modal):
    def __init__(self, guild: nextcord.Guild) -> None:
        super().__init__('Bet', timeout=300)
        self.gdb = GuildDateBases(guild.id)
        self.economy_settings = self.gdb.get('economic_settings', {})
        work_data = self.economy_settings.get('bet')
        _min_bet_previous = work_data.get('min')
        _max_bet_previous = work_data.get('max')

        self.min_bet = nextcord.ui.TextInput(
            label='Minimum bid',
            placeholder=_min_bet_previous,
            required=False,
            max_length=6
        )
        self.add_item(self.min_bet)

        self.max_bet = nextcord.ui.TextInput(
            label='Maximum bid',
            placeholder=_max_bet_previous,
            required=False,
            max_length=6
        )
        self.add_item(self.max_bet)

    async def callback(self, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)

        if not (self.min_bet.value or self.min_bet.value):
            await interaction.response.send_message("At least one value must be filled in", ephemeral=True)
            return
        if (self.min_bet.value and not self.min_bet.value.isdigit()) or (self.max_bet.value and not self.max_bet.value.isdigit()):
            await interaction.response.send_message("The value must be an integer number", ephemeral=True)
            return

        economy_settings = gdb.get('economic_settings')
        bet_data = self.economy_settings.get('bet')
        if self.min_bet.value:
            bet_data['min'] = int(self.min_bet.value)
        if self.max_bet.value:
            bet_data['max'] = int(self.max_bet.value)
        economy_settings['bet'] = bet_data

        gdb.set('economic_settings', economy_settings)

        view = BonusView(interaction.guild)
        await interaction.message.edit(embed=view.embed, view=view)


class BonusDropDown(nextcord.ui.StringSelect):
    def __init__(self, guild_id: int, selected_value: Optional[str] = None):
        self.gdb = GuildDateBases(guild_id)
        self.economy_settings = self.gdb.get('economic_settings', {})
        options = [
            nextcord.SelectOption(
                label='Daily reward',
                value='daily',
                default='daily' == selected_value
            ),
            nextcord.SelectOption(
                label='Weekly reward',
                value='weekly',
                default='weekly' == selected_value
            ),
            nextcord.SelectOption(
                label='Monthly reward',
                value='monthly',
                default='monthly' == selected_value
            ),
            nextcord.SelectOption(
                label='Work',
                value='work',
                default='work' == selected_value
            ),
            nextcord.SelectOption(
                label='Bet',
                value='bet',
                default='bet' == selected_value
            )
        ]

        super().__init__(
            placeholder="Setting up bonus amounts",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = self.values[0]
        view = BonusView(interaction.guild, value)
        await interaction.response.edit_message(embed=view.embed, view=view)


class BonusView(DefaultSettingsView):
    embed: nextcord.Embed

    def __init__(self, guild: nextcord.Guild, value: Optional[str] = None) -> None:
        self.value = value
        self.embed = economy.Economy(guild).embed

        super().__init__()

        if value:
            self.edit.disabled = False
            self.reset.disabled = False
        self.add_item(BonusDropDown(guild.id, value))

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = economy.Economy(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Edit', style=nextcord.ButtonStyle.success, disabled=True)
    async def edit(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        if self.value in reward_names:
            modal = RewardBonusModal(interaction.guild, self.value)
        if self.value == 'work':
            modal = WorkBonusModal(interaction.guild)
        if self.value == 'bet':
            modal = BetBonusModal(interaction.guild)
        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label='Reset', style=nextcord.ButtonStyle.blurple, disabled=True)
    async def reset(self,
                    button: nextcord.ui.Button,
                    interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)

        economy_settings = gdb.get('economic_settings')
        economy_settings[self.value] = DEFAULT_ECONOMY_SETTINGS[self.value]
        gdb.set('economic_settings', economy_settings)

        view = BonusView(interaction.guild, self.value)
        await interaction.message.edit(embed=view.embed, view=view)
