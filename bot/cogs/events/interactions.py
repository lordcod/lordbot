import logging
import nextcord
from nextcord.ext import commands

from bot.databases import GuildDateBases
from bot.misc.lordbot import LordBot

_log = logging.getLogger(__name__)


class InteractionsEvent(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        bot.set_event(self.on_item_not_found, name='on_view_not_found')
        bot.set_event(self.on_item_not_found, name='on_modal_not_found')
        super().__init__()

    async def on_item_not_found(self, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        color = await gdb.get('color')

        embed = nextcord.Embed(
            title="The interaction time has expired",
            description="If you need to use the interaction, call the associated command",
            color=color
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(InteractionsEvent(bot))
