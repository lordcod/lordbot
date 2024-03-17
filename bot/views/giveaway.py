

import asyncio
import nextcord
from bot.databases import localdb
from bot.misc import giveaway as misc_giveaway


GIVEAWAY_DB = localdb.get_table('giveaway')


class GiveawayConfirmView(nextcord.ui.View):
    def __init__(self, giveaway: 'misc_giveaway.Giveaway') -> None:
        self.giveaway = giveaway
        super().__init__()

    @nextcord.ui.button(label="Leave giveaway", style=nextcord.ButtonStyle.red)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        asyncio.create_task(interaction.delete_original_message())

        if not self.giveaway.check_participation(interaction.user.id):
            return

        self.giveaway.demote_participant(interaction.user.id)

        asyncio.create_task(self.giveaway.update_message())


class GiveawayView(nextcord.ui.View):
    @nextcord.ui.button(emoji="🎉", style=nextcord.ButtonStyle.blurple)
    async def participate(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        giveaway = misc_giveaway.Giveaway(
            interaction.guild, interaction.message.id)

        if giveaway.check_participation(interaction.user.id):
            await interaction.response.send_message(content="Are you sure you want to leave giveaway?",
                                                    view=GiveawayConfirmView(
                                                        giveaway),
                                                    ephemeral=True)
            return

        giveaway.promote_participant(interaction.user.id)

        await giveaway.update_message()
