

import asyncio
import nextcord
import time
from typing import TYPE_CHECKING, Optional
from bot.misc import giveaway as misc_giveaway
from bot.misc.utils import translate_to_timestamp

if TYPE_CHECKING:
    from bot.misc.giveaway import GiveawayConfig, Giveaway


class GiveawaySettingsSponsorDropDown(nextcord.ui.UserSelect):
    def __init__(self, member: nextcord.Member, guild_id: int, giveaway_config: 'GiveawayConfig') -> None:
        self.member = member
        self.giveaway_config = giveaway_config
        super().__init__(placeholder="Choose a giveaway sponsor")

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        return interaction.user == self.member

    async def callback(self, interaction: nextcord.Interaction) -> None:
        self.giveaway_config.sponsor = self.values[0]

        view = GiveawaySettingsView(
            self.member, interaction.guild_id, self.giveaway_config)
        await interaction.response.edit_message(embed=view.embed, view=view)


class GiveawaySettingsChannelDropDown(nextcord.ui.ChannelSelect):
    def __init__(self, member: nextcord.Member, guild_id: int, giveaway_config: 'GiveawayConfig') -> None:
        self.member = member
        self.giveaway_config = giveaway_config
        super().__init__(placeholder="Choose a giveaway channel", channel_types=[
            nextcord.ChannelType.news, nextcord.ChannelType.text])

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        return interaction.user == self.member

    async def callback(self, interaction: nextcord.Interaction) -> None:
        self.giveaway_config.channel = self.values[0]

        view = GiveawaySettingsView(
            self.member, interaction.guild_id, self.giveaway_config)
        await interaction.response.edit_message(embed=view.embed, view=view)


class GiveawaySettingsPrizeModal(nextcord.ui.Modal):
    def __init__(self, guild_id: int, giveaway_config: 'GiveawayConfig') -> None:
        self.giveaway_config = giveaway_config

        super().__init__("Settings Giveaway")

        self.prize = nextcord.ui.TextInput(
            label="Prize",
            max_length=200
        )
        self.add_item(self.prize)

        self.quantity = nextcord.ui.TextInput(
            label="Prize",
            max_length=2,
            required=False,
            default_value="1"
        )
        self.add_item(self.quantity)

    async def callback(self, interaction: nextcord.Interaction):
        if not self.quantity.value.isdigit():
            await interaction.response.send_message("Quantity format is invalid!")
            return

        self.giveaway_config.prize = self.prize.value
        self.giveaway_config.quantity = int(self.quantity.value)

        view = GiveawaySettingsView(
            interaction.user, interaction.guild_id, self.giveaway_config)
        await interaction.response.edit_message(embed=view.embed, view=view)


class GiveawaySettingsDescriptionModal(nextcord.ui.Modal):
    def __init__(self, guild_id: int, giveaway_config: 'GiveawayConfig') -> None:
        self.giveaway_config = giveaway_config

        super().__init__("Settings Giveaway")

        self.description = nextcord.ui.TextInput(
            label="Prize",
            style=nextcord.TextInputStyle.paragraph
        )
        self.add_item(self.description)

    async def callback(self, interaction: nextcord.Interaction):
        self.giveaway_config.description = self.description.value

        view = GiveawaySettingsView(
            interaction.user, interaction.guild_id, self.giveaway_config)
        await interaction.response.edit_message(embed=view.embed, view=view)


class GiveawaySettingsDateendModal(nextcord.ui.Modal):
    def __init__(self, guild_id: int, giveaway_config: 'GiveawayConfig') -> None:
        self.giveaway_config = giveaway_config

        super().__init__("Settings Giveaway")

        self.date_end = nextcord.ui.TextInput(
            label="Date end",
            style=nextcord.TextInputStyle.paragraph,
            placeholder=(
                "01.01.2023\n"
                "01.01.2023 12:30\n"
                "01.01.2023 12:30:45\n"
                "12:30\n"
                "1d2m3h4m5s"
            )
        )
        self.add_item(self.date_end)

    async def callback(self, interaction: nextcord.Interaction):
        date_end = translate_to_timestamp(self.date_end.value)

        if not date_end:
            await interaction.response.send_message("Date format is invalid!")
            return

        self.giveaway_config.date_end = date_end

        view = GiveawaySettingsView(
            interaction.user, interaction.guild_id, self.giveaway_config)
        await interaction.response.edit_message(embed=view.embed, view=view)


class GiveawaySettingsView(nextcord.ui.View):
    embed: nextcord.Embed

    def __init__(self, member: nextcord.Member, guild_id: int, giveaway_config: Optional['GiveawayConfig'] = None) -> None:
        self.giveaway_config = giveaway_config or misc_giveaway.GiveawayConfig()
        self.member = member
        super().__init__()
        self.add_item(GiveawaySettingsChannelDropDown(
            member, guild_id, self.giveaway_config))
        self.add_item(GiveawaySettingsSponsorDropDown(
            member, guild_id, self.giveaway_config))

        self.embed = nextcord.Embed(
            title=f"Giveaway prize: {self.giveaway_config.quantity if self.giveaway_config.quantity else 1} {self.giveaway_config.prize if self.giveaway_config.prize else 'no prize'}")

        self.embed.description = self.giveaway_config.description
        self.embed.add_field(
            name="Addtionally information",
            value=(
                f"Channel: {self.giveaway_config.channel.mention if self.giveaway_config.channel else 'no channel'}\n"
                f"Sponsor: {self.giveaway_config.sponsor.mention if self.giveaway_config.sponsor else member.mention}\n"
                f"Date end: {f'<t:{self.giveaway_config.date_end :.0f}:f>' if self.giveaway_config.date_end else 'no date end'}"
            )
        )

        if self.giveaway_config.prize:
            self.prize.style = nextcord.ButtonStyle.blurple
        if self.giveaway_config.description:
            self.description.style = nextcord.ButtonStyle.blurple
        if self.giveaway_config.date_end:
            self.date_end.style = nextcord.ButtonStyle.blurple

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        return interaction.user == self.member

    @nextcord.ui.button(label="Create giveaway", style=nextcord.ButtonStyle.success)
    async def create(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not (self.giveaway_config.prize
                and self.giveaway_config.date_end
                and self.giveaway_config.channel):
            await interaction.response.send_message("You have filled in all required forms!",
                                                    ephemeral=True)
            return
        if not self.giveaway_config.sponsor:
            self.giveaway_config.sponsor = interaction.user
        asyncio.create_task(interaction.delete_original_message())
        giveaway = await misc_giveaway.Giveaway.create_as_config(interaction.guild, self.giveaway_config)
        giveaway.lord_handler_timer.create_timer_handler(
            giveaway.giveaway_data.get('date_end')-time.time(),
            giveaway.complete(),
            f'giveaway:{giveaway.message_id}'
        )

    @nextcord.ui.button(label="Prize", style=nextcord.ButtonStyle.grey)
    async def prize(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(GiveawaySettingsPrizeModal(interaction.guild_id, self.giveaway_config))

    @nextcord.ui.button(label="Description", style=nextcord.ButtonStyle.grey)
    async def description(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(GiveawaySettingsDescriptionModal(interaction.guild_id, self.giveaway_config))

    @nextcord.ui.button(label="Date end", style=nextcord.ButtonStyle.grey)
    async def date_end(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(GiveawaySettingsDateendModal(interaction.guild_id, self.giveaway_config))


class GiveawayConfirmView(nextcord.ui.View):
    def __init__(self, giveaway: 'Giveaway') -> None:
        self.giveaway = giveaway
        super().__init__()

    @nextcord.ui.button(label="Leave giveaway", style=nextcord.ButtonStyle.red)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        asyncio.create_task(interaction.delete_original_message())

        if not await self.giveaway.check_participation(interaction.user.id):
            return

        await self.giveaway.demote_participant(interaction.user.id)
        await self.giveaway.update_message()


class GiveawayView(nextcord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @nextcord.ui.button(emoji="🎉", custom_id="giveaway", style=nextcord.ButtonStyle.blurple)
    async def participate(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        giveaway = misc_giveaway.Giveaway(
            interaction.guild, interaction.message.id)

        if giveaway.check_participation(interaction.user.id):
            await interaction.response.send_message(content="Are you sure you want to leave giveaway?",
                                                    view=GiveawayConfirmView(
                                                        giveaway),
                                                    ephemeral=True)
            return

        await giveaway.promote_participant(interaction.user.id)

        await giveaway.update_message()
